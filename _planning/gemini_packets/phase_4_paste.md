# Phase 4 paste — model deployment (5/9)

Scope note. Serve `models/model.bin` with Flask. One local prediction is the close condition. Docker is the next gate.

## Table of contents

- [Rules](#rules)
- [Paths](#paths)
- [Order](#order)
- [Success](#success)

---

## Rules

- Load the pickle once at boot.
- Drop `reservation_status` and `reservation_status_date` before `transform`.
- Fill missing values the same way as `train.py`.
- Listen on `0.0.0.0` port 9696 for the local run.
- Do not build the image and do not deploy.

[↑ Contents](#table-of-contents)

---

## Paths

| What | Path |
|------|------|
| Service | `src\predict.py` |
| Artifact | `models\model.bin` |
| Route | `POST /predict` |

[↑ Contents](#table-of-contents)

---

## Order

1. Load `(dv, model)`.
2. Accept one JSON booking and return `cancel_probability` and `is_canceled`.
3. Call it once from the host with `Invoke-RestMethod` or curl.

Local smoke: `cancel_probability≈0.679`, `is_canceled=true`. **Done** 2026-11-07.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Process starts on port 9696
- [x] One JSON prediction returns
- [x] No Docker build in this gate

[↑ Contents](#table-of-contents)
