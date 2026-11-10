"""
HoldRisk — hotel cancellation risk desk (Flask + XGBoost).
Usage:
    python src/predict.py
"""

from pathlib import Path
import os
import pickle
import time
import threading
from collections import deque

import pandas as pd
import xgboost as xgb
from flask import Flask, jsonify, request, send_from_directory

ROOT_DIR = Path(__file__).resolve().parents[1]
UI_DIR = ROOT_DIR / "ui_dummy"
model_path = ROOT_DIR / "models" / "model.bin"

with open(model_path, "rb") as f_in:
    dv, model = pickle.load(f_in)
# pickle.load: restore DictVectorizer + XGBoost from model.bin once at boot.

print("Model and DictVectorizer loaded successfully!")

# In-process audit ring for Ops Grafana tab (same host as Signet /ops/board role).
_AUDIT_LOCK = threading.Lock()
_AUDIT = deque(maxlen=200)
_STARTED = time.time()
_BUCKET_S = 30
_N_BUCKETS = 30  # last 15 minutes, Signet-style rate / latency windows
_SKIP_AUDIT_PATHS = {"/ops/board", "/health"}


def predict_single(customer_data):
    customer_data = dict(customer_data)
    customer_data.pop("reservation_status", None)
    customer_data.pop("reservation_status_date", None)
    customer_data.pop("decision_threshold", None)

    for key, val in customer_data.items():
        if isinstance(val, (int, float)):
            customer_data[key] = 0 if pd.isna(val) else val
        else:
            customer_data[key] = "missing" if pd.isna(val) else str(val)

    X = dv.transform([customer_data])
    features = list(dv.get_feature_names_out())
    dtest = xgb.DMatrix(X, feature_names=features)
    y_pred = model.predict(dtest)
    return float(y_pred[0])


def _record_audit(path, status, latency_ms, extra=None, method=None):
    row = {
        "time": time.strftime("%H:%M:%S"),
        "ts": time.time(),
        "method": method or "GET",
        "path": path,
        "status": int(status),
        "latency_ms": round(float(latency_ms), 1),
        "extra": extra or {},
    }
    with _AUDIT_LOCK:
        _AUDIT.appendleft(row)


def _percentile(values, q):
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(float(ordered[0]), 2)
    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return round(ordered[lo] * (1.0 - frac) + ordered[hi] * frac, 2)


def _ops_buckets(rows):
    now = time.time()
    origin = now - (_BUCKET_S * _N_BUCKETS)
    buckets = [{"rates": {}, "latencies": []} for _ in range(_N_BUCKETS)]
    for row in rows:
        ts = float(row.get("ts") or 0)
        if ts < origin:
            continue
        idx = int((ts - origin) / _BUCKET_S)
        idx = 0 if idx < 0 else min(idx, _N_BUCKETS - 1)
        bucket = buckets[idx]
        status = str(int(row.get("status") or 0))
        bucket["rates"][status] = bucket["rates"].get(status, 0) + 1
        bucket["latencies"].append(float(row.get("latency_ms") or 0))
    out = []
    for bucket in buckets:
        lats = bucket["latencies"]
        rates = {
            code: round(count / float(_BUCKET_S), 4)
            for code, count in bucket["rates"].items()
        }
        out.append(
            {
                "rates": rates,
                "p95": _percentile(lats, 0.95) if lats else 0.0,
                "p99": _percentile(lats, 0.99) if lats else 0.0,
                "n": sum(bucket["rates"].values()),
            }
        )
    return out


def _status_counts(rows):
    counts = {}
    for row in rows:
        key = str(int(row.get("status") or 0))
        counts[key] = counts.get(key, 0) + 1
    return counts


def _board_series(rows):
    chrono = list(reversed(rows))[-40:]
    latency_ms = [float(r.get("latency_ms") or 0) for r in chrono]
    cancel_p = []
    for row in chrono:
        extra = row.get("extra") or {}
        p = extra.get("cancel_probability")
        if p is None:
            continue
        cancel_p.append(round(float(p), 4))
    return {"latency_ms": latency_ms, "cancel_p": cancel_p}


app = Flask("hotel-cancellation")


@app.route("/", methods=["GET"])
def desk():
    return send_from_directory(UI_DIR, "index.html")


@app.route("/ui/<path:asset>", methods=["GET"])
def ui_assets(asset):
    return send_from_directory(UI_DIR, asset)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "uptime_s": int(time.time() - _STARTED)}), 200


@app.route("/ops/board", methods=["GET"])
def ops_board():
    # Ops Grafana tab: request audit for this process (no separate Grafana server required).
    with _AUDIT_LOCK:
        rows = list(_AUDIT)
    predicts = [r for r in rows if r["path"] == "/predict"]
    flagged = [
        r
        for r in predicts
        if (r.get("extra") or {}).get("is_canceled") is True
    ]
    latencies = [r["latency_ms"] for r in rows]
    avg_latency = round(sum(latencies) / len(latencies), 1) if latencies else None
    errors = sum(1 for r in rows if int(r["status"]) >= 400)
    n = len(rows)
    error_rate = round(errors / n, 4) if n else 0.0
    return jsonify(
        {
            "uptime_s": int(time.time() - _STARTED),
            "request_count": n,
            "predict_count": len(predicts),
            "flagged_count": len(flagged),
            "error_count": errors,
            "error_rate": error_rate,
            "avg_latency_ms": avg_latency,
            "stats": {
                "requests": n,
                "error_rate": error_rate,
                "avg_ms": avg_latency,
            },
            "buckets": _ops_buckets(rows),
            "series": _board_series(rows),
            "status_counts": _status_counts(rows),
            "audit": rows[:40],
        }
    )


@app.before_request
def _mark_request_start():
    request._holdrisk_t0 = time.perf_counter()


@app.after_request
def _audit_request(resp):
    path = request.path or "/"
    if path.startswith("/ui/") or path in _SKIP_AUDIT_PATHS:
        return resp
    if path == "/favicon.ico" or path.startswith("/apple-touch-icon"):
        return resp
    if path == "/predict":
        return resp
    t0 = getattr(request, "_holdrisk_t0", None)
    ms = (time.perf_counter() - t0) * 1000 if t0 is not None else 0.0
    _record_audit(path, resp.status_code, ms, method=request.method)
    return resp


@app.route("/predict", methods=["POST"])
def predict():
    t0 = time.perf_counter()
    customer = request.get_json(force=True, silent=True) or {}
    threshold = customer.get("decision_threshold", 0.5)
    try:
        threshold = float(threshold)
    except (TypeError, ValueError):
        threshold = 0.5
    threshold = min(0.95, max(0.05, threshold))

    try:
        probability = predict_single(customer)
        is_canceled = bool(probability >= threshold)
        result = {
            "cancel_probability": probability,
            "is_canceled": is_canceled,
            "decision_threshold": threshold,
        }
        status = 200
        body = jsonify(result)
    except Exception as exc:  # noqa: BLE001 — surface as JSON for the desk
        status = 500
        body = jsonify({"error": str(exc)})
        probability = None
        is_canceled = None

    _record_audit(
        "/predict",
        status,
        (time.perf_counter() - t0) * 1000,
        {
            "cancel_probability": probability,
            "is_canceled": is_canceled,
            "hotel": customer.get("hotel"),
            "lead_time": customer.get("lead_time"),
        },
        method="POST",
    )
    return body, status


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9696"))
    app.run(debug=False, host="0.0.0.0", port=port)
