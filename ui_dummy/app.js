(() => {
  const form = document.getElementById("form");
  const result = document.getElementById("result");
  const probEl = document.getElementById("prob");
  const verdictEl = document.getElementById("verdict");
  const meterFill = document.getElementById("meter-fill");
  const predictBtn = document.getElementById("predict");
  const toast = document.getElementById("toast");

  function mockProbability(values) {
    let p = 0.14;
    p += Math.min(Number(values.lead_time) || 0, 365) / 900;
    if (values.hotel === "City Hotel") p += 0.08;
    if (values.deposit === "Non Refund") p -= 0.18;
    if (values.deposit === "No Deposit") p += 0.06;
    if (values.segment === "Groups") p += 0.14;
    if (values.segment === "Online TA") p += 0.05;
    if (values.segment === "Direct") p -= 0.04;
    if (Number(values.adults) >= 3) p += 0.03;
    if (Number(values.adr) > 150) p += 0.04;
    return Math.max(0.02, Math.min(0.97, p));
  }

  function renderIdle() {
    probEl.textContent = "—";
    probEl.className = "prob";
    meterFill.style.setProperty("--p", "0%");
    verdictEl.innerHTML =
      '값을 넣고 예측을 누르면 취소 확률과 <strong>is_canceled</strong>가 여기에 뜹니다.';
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    predictBtn.classList.add("busy");
    predictBtn.disabled = true;

    window.setTimeout(() => {
      const p = mockProbability(data);
      const pct = (p * 100).toFixed(1) + "%";
      const canceled = p >= 0.5;

      meterFill.style.animation = "none";
      void meterFill.offsetHeight;
      meterFill.style.animation = "";
      meterFill.style.setProperty("--p", (p * 100).toFixed(1) + "%");

      probEl.textContent = pct;
      probEl.className = "prob " + (canceled ? "high" : "low");
      verdictEl.innerHTML = canceled
        ? `예상: <strong>is_canceled = 1</strong> · 취소 위험이 높습니다.`
        : `예상: <strong>is_canceled = 0</strong> · 유지 가능성이 더 큽니다.`;

      result.classList.add("show");
      predictBtn.classList.remove("busy");
      predictBtn.disabled = false;
    }, 320);
  });

  document.getElementById("reset").addEventListener("click", () => {
    form.reset();
    result.classList.remove("show");
    renderIdle();
    window.setTimeout(() => result.classList.add("show"), 40);
  });

  document.getElementById("ops").addEventListener("click", () => {
    toast.classList.add("show");
    window.setTimeout(() => toast.classList.remove("show"), 1800);
  });

  renderIdle();
  result.classList.add("show");
})();
