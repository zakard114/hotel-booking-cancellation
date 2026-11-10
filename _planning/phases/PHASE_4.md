# Phase 4 — predict.py (5/9)

**Done** (2026-11-07).

## Table of contents

- [Goal](#goal)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Load the saved model and serve predictions over HTTP with Flask.

[↑ Contents](#table-of-contents)

---

## Output

`src/predict.py` plus one local request (`Invoke-RestMethod` or curl). Sample result: `cancel_probability≈0.679`, `is_canceled=true`.

[↑ Contents](#table-of-contents)

---

## Out of scope

A finished Docker image and any cloud deploy. A Dockerfile stub was allowed.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Service starts locally on port 9696
- [x] One sample JSON returns a prediction
- [x] Leakage columns are dropped before scoring

[↑ Contents](#table-of-contents)
