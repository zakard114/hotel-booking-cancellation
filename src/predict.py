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
_AUDIT = deque(maxlen=100)
_STARTED = time.time()


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


def _record_audit(path, status, latency_ms, extra=None):
    row = {
        "time": time.strftime("%H:%M:%S"),
        "path": path,
        "status": status,
        "latency_ms": round(latency_ms, 1),
        "extra": extra or {},
    }
    with _AUDIT_LOCK:
        _AUDIT.appendleft(row)


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
    latencies = [r["latency_ms"] for r in predicts]
    avg_latency = round(sum(latencies) / len(latencies), 1) if latencies else None
    errors = sum(1 for r in rows if int(r["status"]) >= 400)
    return jsonify(
        {
            "uptime_s": int(time.time() - _STARTED),
            "request_count": len(rows),
            "predict_count": len(predicts),
            "flagged_count": len(flagged),
            "error_count": errors,
            "avg_latency_ms": avg_latency,
            "audit": rows[:40],
        }
    )


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
    )
    return body, status


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9696"))
    app.run(debug=False, host="0.0.0.0", port=port)
