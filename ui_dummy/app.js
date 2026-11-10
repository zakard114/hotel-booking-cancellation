(() => {
  const form = document.getElementById("form");
  const result = document.getElementById("result");
  const probEl = document.getElementById("prob");
  const verdictEl = document.getElementById("verdict");
  const meterFill = document.getElementById("meter-fill");
  const predictBtn = document.getElementById("predict");
  const desk = document.getElementById("desk");
  const opsStage = document.getElementById("ops-stage");
  const openOps = document.getElementById("open-ops");
  const closeOps = document.getElementById("close-ops");
  const logList = document.getElementById("log-list");
  const boardBody = document.getElementById("board-body");
  const thresholdInput = document.getElementById("threshold");
  const thresholdMsg = document.getElementById("threshold-msg");
  const hintEl = document.querySelector(".hint");

  const state = {
    threshold: 0.5,
    latest: null,
    log: [],
  };

  function buildPayload(formValues) {
    return {
      hotel: formValues.hotel,
      lead_time: Number(formValues.lead_time),
      arrival_date_year: 2017,
      arrival_date_month: "July",
      arrival_date_week_number: 27,
      arrival_date_day_of_month: 1,
      stays_in_weekend_nights: 1,
      stays_in_week_nights: 2,
      adults: Number(formValues.adults),
      children: 0,
      babies: 0,
      meal: "BB",
      country: "PRT",
      market_segment: formValues.segment,
      distribution_channel: "TA/TO",
      is_repeated_guest: 0,
      previous_cancellations: 0,
      previous_bookings_not_canceled: 0,
      reserved_room_type: "A",
      assigned_room_type: "A",
      booking_changes: 0,
      deposit_type: formValues.deposit,
      agent: "9",
      company: "missing",
      days_in_waiting_list: 0,
      customer_type: "Transient",
      adr: Number(formValues.adr),
      required_car_parking_spaces: 0,
      total_of_special_requests: 1,
      decision_threshold: state.threshold,
    };
  }

  function newTrace() {
    return "hr-" + Math.random().toString(16).slice(2, 10);
  }

  function renderIdle() {
    probEl.textContent = "—";
    probEl.className = "prob";
    meterFill.style.setProperty("--p", "0%");
    verdictEl.innerHTML =
      "Enter values and run predict to see cancel probability and <strong>is_canceled</strong> here.";
  }

  function applyVerdict(p, canceled) {
    const pct = (p * 100).toFixed(1) + "%";
    meterFill.style.animation = "none";
    void meterFill.offsetHeight;
    meterFill.style.animation = "";
    meterFill.style.setProperty("--p", (p * 100).toFixed(1) + "%");
    probEl.textContent = pct;
    probEl.className = "prob " + (canceled ? "high" : "low");
    verdictEl.innerHTML = canceled
      ? `Forecast: <strong>is_canceled = 1</strong> · high cancel risk.`
      : `Forecast: <strong>is_canceled = 0</strong> · more likely to stay.`;
  }

  function refreshInspector() {
    const title = document.getElementById("insp-title");
    const kv = document.getElementById("insp-kv");
    const row = state.latest;
    if (!row) {
      title.textContent = "No prediction yet";
      title.className = "entry-title";
      [...kv.querySelectorAll("dd")].forEach((dd) => {
        dd.textContent = "—";
      });
      return;
    }
    title.textContent = row.canceled ? "High cancel risk" : "Likely to hold";
    title.className = "entry-title " + (row.canceled ? "stop" : "ok");
    const values = [
      row.canceled ? "FLAGGED" : "HOLD",
      (row.p * 100).toFixed(1) + "%",
      String(row.canceled ? 1 : 0),
      row.trace,
      row.time,
      row.hotel,
      String(row.lead_time),
      row.deposit,
      row.segment,
      String(row.adr),
    ];
    [...kv.querySelectorAll("dd")].forEach((dd, i) => {
      dd.textContent = values[i];
    });
  }

  function refreshLog() {
    if (!state.log.length) {
      logList.innerHTML = '<li class="log-empty">No predicts in this session yet.</li>';
      return;
    }
    logList.innerHTML = state.log
      .map((row) => {
        const cls = row.canceled ? "risk" : "hold";
        return `<li class="${cls}"><span class="t">${row.time}</span><span class="p">${(row.p * 100).toFixed(1)}%</span><span class="s">${row.canceled ? "flagged" : "hold"}</span><span class="d">${row.hotel} · lead ${row.lead_time} · ${row.segment}</span></li>`;
      })
      .join("");
  }

  const HOLD = "#6dcca4";
  const RISK = "#e39a94";
  const SEA = "#8fd0db";
  const SAFFRON = "#e28a1a";
  const GRID = "rgba(231,238,244,0.16)";
  const AXIS = "rgba(231,238,244,0.62)";

  let boardTimer = null;

  function stopBoard() {
    if (boardTimer) {
      clearInterval(boardTimer);
      boardTimer = null;
    }
  }

  function statusColor(status) {
    const code = Number(status);
    if (code >= 200 && code < 300) return HOLD;
    if (code >= 400) return RISK;
    return SAFFRON;
  }

  function drawSeries(svg, series, yMax) {
    if (!svg) return;
    const width = 640;
    const height = 180;
    const padL = 36;
    const padB = 22;
    const padT = 8;
    const padR = 8;
    const innerW = width - padL - padR;
    const innerH = height - padT - padB;
    const ceiling = yMax > 0 ? yMax : 1;
    const parts = [];
    for (let tick = 0; tick <= 3; tick += 1) {
      const y = padT + innerH - (innerH * tick) / 3;
      const label = (ceiling * tick) / 3;
      const text = ceiling >= 10 ? label.toFixed(0) : label.toFixed(2);
      parts.push(
        `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="${GRID}" />`
      );
      parts.push(
        `<text x="${padL - 6}" y="${y + 4}" fill="${AXIS}" font-size="11" text-anchor="end">${text}</text>`
      );
    }
    series.forEach((seriesItem) => {
      const values = seriesItem.values || [];
      if (!values.length) return;
      const points = values.map((value, index) => {
        const x =
          padL + (values.length === 1 ? innerW / 2 : (innerW * index) / (values.length - 1));
        const y = padT + innerH - (innerH * Math.min(value, ceiling)) / ceiling;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      });
      parts.push(
        `<polyline fill="none" stroke="${seriesItem.color}" stroke-width="2" points="${points.join(" ")}" />`
      );
    });
    svg.innerHTML = parts.join("");
  }

  function drawBars(svg, items, yMax) {
    if (!svg) return;
    const width = 640;
    const height = 180;
    const padL = 36;
    const padB = 28;
    const padT = 8;
    const padR = 8;
    const innerW = width - padL - padR;
    const innerH = height - padT - padB;
    const ceiling = yMax > 0 ? yMax : 1;
    const parts = [];
    for (let tick = 0; tick <= 3; tick += 1) {
      const y = padT + innerH - (innerH * tick) / 3;
      const label = (ceiling * tick) / 3;
      const text = ceiling >= 10 ? label.toFixed(0) : label.toFixed(1);
      parts.push(
        `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="${GRID}" />`
      );
      parts.push(
        `<text x="${padL - 6}" y="${y + 4}" fill="${AXIS}" font-size="11" text-anchor="end">${text}</text>`
      );
    }
    const n = Math.max(items.length, 1);
    const slot = innerW / n;
    const barW = Math.min(72, slot * 0.55);
    items.forEach((item, index) => {
      const h = (innerH * Math.min(item.value, ceiling)) / ceiling;
      const x = padL + slot * index + (slot - barW) / 2;
      const y = padT + innerH - h;
      parts.push(
        `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barW.toFixed(1)}" height="${Math.max(h, 0).toFixed(1)}" fill="${item.color}" />`
      );
      parts.push(
        `<text x="${(x + barW / 2).toFixed(1)}" y="${height - 8}" fill="${AXIS}" font-size="11" text-anchor="middle">${item.label}</text>`
      );
    });
    svg.innerHTML = parts.join("");
  }

  function renderLegend(id, items) {
    const box = document.getElementById(id);
    if (!box) return;
    box.replaceChildren();
    items.forEach((item) => {
      const span = document.createElement("span");
      const swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.background = item.color;
      span.append(swatch, document.createTextNode(item.label));
      box.appendChild(span);
    });
  }

  function paintCharts(board) {
    const buckets = board.buckets || [];
    const statuses = [];
    buckets.forEach((bucket) => {
      Object.keys(bucket.rates || {}).forEach((status) => {
        if (!statuses.includes(status)) statuses.push(status);
      });
    });
    statuses.sort();
    const rateSeries = statuses.map((status) => ({
      color: statusColor(status),
      label: status,
      values: buckets.map((bucket) => Number((bucket.rates || {})[status] || 0)),
    }));
    const rateMax = rateSeries.reduce((max, series) => Math.max(max, ...series.values, 0), 0);
    drawSeries(document.getElementById("chart-rate"), rateSeries, rateMax);
    renderLegend(
      "rate-legend",
      rateSeries.map((series) => ({ color: series.color, label: "HTTP " + series.label }))
    );

    const p95 = buckets.map((bucket) => Number(bucket.p95 || 0));
    const p99 = buckets.map((bucket) => Number(bucket.p99 || 0));
    let latMax = Math.max(...p95, ...p99, 0);
    const latSeries = [
      { color: SEA, values: p95 },
      { color: SAFFRON, values: p99 },
    ];
    const rawLat = (board.series && board.series.latency_ms) || [];
    if (latMax === 0 && rawLat.length) {
      latSeries.length = 0;
      latSeries.push({ color: SEA, values: rawLat.map(Number) });
      latMax = Math.max(...rawLat, 0);
      renderLegend("latency-legend", [{ color: SEA, label: "Latency ms" }]);
    } else {
      renderLegend("latency-legend", [
        { color: SEA, label: "P95" },
        { color: SAFFRON, label: "P99" },
      ]);
    }
    drawSeries(document.getElementById("chart-latency"), latSeries, latMax);

    const cancelP = (board.series && board.series.cancel_p) || [];
    drawSeries(
      document.getElementById("chart-prob"),
      [{ color: SAFFRON, values: cancelP.map(Number) }],
      1
    );
    renderLegend("prob-legend", [{ color: SAFFRON, label: "cancel_probability" }]);

    const counts = board.status_counts || {};
    const barItems = Object.keys(counts)
      .sort()
      .map((code) => ({
        label: code,
        value: Number(counts[code] || 0),
        color: statusColor(code),
      }));
    const barMax = barItems.reduce((max, item) => Math.max(max, item.value), 0);
    drawBars(document.getElementById("chart-status"), barItems, barMax);
    renderLegend(
      "status-legend",
      barItems.map((item) => ({ color: item.color, label: "HTTP " + item.label }))
    );
  }

  function paintAudit(rows) {
    const note = document.getElementById("audit-filter");
    if (!rows.length) {
      if (note) note.textContent = "No requests yet. Run a predict.";
      boardBody.innerHTML = '<tr><td colspan="8">No server audit rows yet. Run a predict.</td></tr>';
      return;
    }
    if (note) note.textContent = `${rows.length} line${rows.length === 1 ? "" : "s"} on this process.`;
    boardBody.innerHTML = rows
      .map((r) => {
        const ex = r.extra || {};
        const flagged = ex.is_canceled === true;
        const httpErr = Number(r.status) >= 400;
        const p =
          ex.cancel_probability != null
            ? (Number(ex.cancel_probability) * 100).toFixed(1) + "%"
            : "—";
        const flag =
          flagged ? "1" : ex.is_canceled === false ? "0" : "—";
        const cls = [httpErr ? "error" : "", flagged ? "risk" : ""].filter(Boolean).join(" ");
        return `<tr class="${cls}"><td>${r.time || "—"}</td><td class="status">${r.status ?? "—"}</td><td>${r.method || "—"}</td><td class="path">${r.path || "—"}</td><td class="num">${r.latency_ms ?? "—"}</td><td class="p">${p}</td><td class="flag">${flag}</td><td>${ex.hotel ?? "—"}</td></tr>`;
      })
      .join("");
  }

  async function refreshBoard() {
    document.getElementById("m-thr").textContent = state.threshold.toFixed(2);
    try {
      const res = await fetch("/ops/board");
      if (!res.ok) throw new Error("board " + res.status);
      const board = await res.json();
      const stats = board.stats || {};
      const requests = stats.requests ?? board.request_count ?? 0;
      const rate = Number(stats.error_rate ?? board.error_rate ?? 0);
      const avgMs = stats.avg_ms ?? board.avg_latency_ms;
      const flagged = board.flagged_count ?? 0;
      document.getElementById("m-requests").textContent = String(requests);
      const errEl = document.getElementById("m-errors");
      errEl.textContent = `${(rate * 100).toFixed(1)}%`;
      errEl.className = rate > 0 ? "stop" : "";
      document.getElementById("m-latency").textContent =
        avgMs == null ? "0 ms" : `${avgMs} ms`;
      document.getElementById("m-count").textContent = String(board.predict_count ?? 0);
      const highEl = document.getElementById("m-high");
      highEl.textContent = String(flagged);
      highEl.className = flagged > 0 ? "stop" : "";
      paintCharts(board);
      paintAudit(board.audit || []);
      const status = document.getElementById("grafana-status");
      if (status) {
        status.className = "note";
        status.textContent =
          "Requests per second by HTTP status, P95 and P99 latency, cancel probability, and the audit stream. Hold is green. Flagged cancel uses the risk color. A separate Grafana server is optional.";
      }
      return;
    } catch (_) {
      // Fall back to session log if board endpoint is cold/unavailable.
    }
    const n = state.log.length;
    const high = state.log.filter((r) => r.canceled).length;
    document.getElementById("m-requests").textContent = String(n);
    document.getElementById("m-errors").textContent = "—";
    document.getElementById("m-latency").textContent = "—";
    document.getElementById("m-count").textContent = String(n);
    document.getElementById("m-high").textContent = String(high);
    document.getElementById("m-high").className = high > 0 ? "stop" : "";
    paintCharts({
      buckets: [],
      series: { latency_ms: [], cancel_p: state.log.slice().reverse().map((r) => r.p) },
      status_counts: {},
    });
    const note = document.getElementById("audit-filter");
    if (note) note.textContent = "Session log only — board endpoint unavailable.";
    const status = document.getElementById("grafana-status");
    if (status) {
      status.className = "note";
      status.textContent = "The request board could not be read. Showing this session only.";
    }
    boardBody.innerHTML = state.log.length
      ? state.log
          .map(
            (r) =>
              `<tr class="${r.canceled ? "risk" : ""}"><td>${r.time}</td><td class="status">—</td><td>POST</td><td class="path">/predict</td><td class="num">—</td><td class="p">${(r.p * 100).toFixed(1)}%</td><td class="flag">${r.canceled ? "1" : "0"}</td><td>${r.hotel}</td></tr>`
          )
          .join("")
      : '<tr><td colspan="8">No rows yet.</td></tr>';
  }

  function loadGrafana() {
    refreshBoard().catch(() => {
      const status = document.getElementById("grafana-status");
      if (status) status.textContent = "The request board could not be read.";
    });
    stopBoard();
    boardTimer = setInterval(() => {
      const panel = document.querySelector('[data-panel="grafana"]');
      if (!panel || panel.hidden) {
        stopBoard();
        return;
      }
      refreshBoard().catch(() => {});
    }, 4000);
  }

  function refreshOps() {
    refreshInspector();
    refreshLog();
    refreshBoard();
  }

  function recordPredict(data, p, canceled, source) {
    const row = {
      p,
      canceled,
      hotel: data.hotel,
      lead_time: data.lead_time,
      deposit: data.deposit,
      segment: data.segment,
      adults: data.adults,
      adr: data.adr,
      trace: newTrace(),
      time: new Date().toLocaleTimeString(),
      source,
    };
    state.latest = row;
    state.log.unshift(row);
    if (state.log.length > 40) state.log.pop();
    applyVerdict(p, canceled);
    if (hintEl) {
      hintEl.textContent =
        source === "api"
          ? "Live model via POST /predict. Flag uses Ops decision threshold."
          : "Request failed — check that the Flask service is up.";
    }
    refreshOps();
  }

  async function predictViaApi(formValues) {
    const payload = buildPayload(formValues);
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(json.error || "HTTP " + res.status);
    }
    return {
      p: Number(json.cancel_probability),
      canceled: Boolean(json.is_canceled),
    };
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    predictBtn.classList.add("busy");
    predictBtn.disabled = true;
    openOps.disabled = true;

    try {
      const { p, canceled } = await predictViaApi(data);
      recordPredict(data, p, canceled, "api");
    } catch (err) {
      console.error(err);
      verdictEl.innerHTML = `Predict failed: <strong>${String(err.message || err)}</strong>`;
      if (hintEl) hintEl.textContent = "Could not reach POST /predict.";
    }

    result.classList.add("show");
    predictBtn.classList.remove("busy");
    predictBtn.disabled = false;
    openOps.disabled = false;
  });

  document.getElementById("reset").addEventListener("click", () => {
    form.reset();
    result.classList.remove("show");
    renderIdle();
    window.setTimeout(() => result.classList.add("show"), 40);
  });

  document.getElementById("set-threshold").addEventListener("click", () => {
    const v = Number(thresholdInput.value);
    if (!(v > 0.05 && v < 0.95)) {
      thresholdMsg.textContent = "Use a value between 0.05 and 0.95.";
      thresholdMsg.className = "form-msg bad";
      return;
    }
    state.threshold = v;
    thresholdMsg.textContent = "Threshold saved — next predict uses this cut.";
    thresholdMsg.className = "form-msg saved";
    document.getElementById("m-thr").textContent = state.threshold.toFixed(2);
  });

  function showOps() {
    desk.hidden = true;
    opsStage.hidden = false;
    openOps.hidden = true;
    document.body.classList.add("mode-ops");
    document.body.classList.remove("mode-desk");
    refreshOps();
    const current = document.querySelector(".ops-head .tab.on");
    if (current && current.getAttribute("data-tab") === "grafana") loadGrafana();
  }

  function showDesk() {
    stopBoard();
    opsStage.hidden = true;
    desk.hidden = false;
    openOps.hidden = false;
    document.body.classList.add("mode-desk");
    document.body.classList.remove("mode-ops");
  }

  openOps.addEventListener("click", showOps);
  closeOps.addEventListener("click", showDesk);

  document.querySelectorAll(".ops-head .tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      const name = btn.getAttribute("data-tab");
      document.querySelectorAll(".ops-head .tab").forEach((b) => {
        b.classList.toggle("on", b === btn);
        b.setAttribute("aria-selected", b === btn ? "true" : "false");
      });
      document.querySelectorAll("[data-panel]").forEach((panel) => {
        panel.hidden = panel.getAttribute("data-panel") !== name;
      });
      if (name === "grafana") loadGrafana();
      else stopBoard();
    });
  });

  document.body.classList.add("mode-desk");
  renderIdle();
  result.classList.add("show");
  refreshOps();
})();
