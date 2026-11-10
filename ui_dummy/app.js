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

  // Defaults fill features the desk form does not edit (same shape as train DictVectorizer rows).
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

  function refreshBoard() {
    const n = state.log.length;
    const high = state.log.filter((r) => r.canceled).length;
    const avg = n
      ? (state.log.reduce((s, r) => s + r.p, 0) / n).toFixed(3)
      : "—";
    document.getElementById("m-count").textContent = String(n);
    document.getElementById("m-high").textContent = String(high);
    document.getElementById("m-avg").textContent = avg;
    document.getElementById("m-thr").textContent = state.threshold.toFixed(2);
    boardBody.innerHTML = state.log.length
      ? state.log
          .map(
            (r) =>
              `<tr class="${r.canceled ? "risk" : ""}"><td>${r.time}</td><td>${(r.p * 100).toFixed(1)}%</td><td>${r.canceled ? "1" : "0"}</td><td>${r.hotel}</td><td>${r.lead_time}</td><td><code>${r.trace}</code></td></tr>`
          )
          .join("")
      : '<tr><td colspan="6">No rows yet.</td></tr>';
  }

  function refreshOps() {
    refreshInspector();
    refreshLog();
    refreshBoard();
  }

  function recordPredict(data, p, source) {
    const canceled = p >= state.threshold;
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
          : "Mock fallback (API unreachable). Flag uses Ops decision threshold.";
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
    if (!res.ok) {
      throw new Error("HTTP " + res.status);
    }
    const json = await res.json();
    return Number(json.cancel_probability);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    predictBtn.classList.add("busy");
    predictBtn.disabled = true;
    openOps.disabled = true;

    try {
      const p = await predictViaApi(data);
      recordPredict(data, p, "api");
    } catch (err) {
      console.warn("API predict failed, using mock:", err);
      // Offline / file:// fallback so the draft still demos.
      let p = 0.14;
      p += Math.min(Number(data.lead_time) || 0, 365) / 900;
      if (data.hotel === "City Hotel") p += 0.08;
      if (data.deposit === "Non Refund") p -= 0.18;
      if (data.deposit === "No Deposit") p += 0.06;
      if (data.segment === "Groups") p += 0.14;
      if (data.segment === "Online TA") p += 0.05;
      if (data.segment === "Direct") p -= 0.04;
      if (Number(data.adults) >= 3) p += 0.03;
      if (Number(data.adr) > 150) p += 0.04;
      p = Math.max(0.02, Math.min(0.97, p));
      recordPredict(data, p, "mock");
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
    thresholdMsg.textContent = "Threshold saved for this session.";
    thresholdMsg.className = "form-msg saved";
    if (state.latest) {
      state.latest.canceled = state.latest.p >= state.threshold;
      state.log = state.log.map((r) => ({
        ...r,
        canceled: r.p >= state.threshold,
      }));
      applyVerdict(state.latest.p, state.latest.canceled);
      refreshOps();
    } else {
      document.getElementById("m-thr").textContent = state.threshold.toFixed(2);
    }
  });

  function showOps() {
    desk.hidden = true;
    opsStage.hidden = false;
    openOps.hidden = true;
    document.body.classList.add("mode-ops");
    document.body.classList.remove("mode-desk");
    refreshOps();
  }

  function showDesk() {
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
    });
  });

  document.body.classList.add("mode-desk");
  renderIdle();
  result.classList.add("show");
  refreshOps();
})();
