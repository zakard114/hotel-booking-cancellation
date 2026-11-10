# Cloud deploy notes (bonus, gate 9/9)

The service is **live**. Click path and smoke results are recorded here. Full click notes: [`../_planning/gemini_packets/phase_8_final_guide.md`](../_planning/gemini_packets/phase_8_final_guide.md).

**Live URL:** https://hotel-cancel-api.onrender.com  
Smoke (2026-11-10): `POST /predict` → `cancel_probability≈0.611555278301239`, `is_canceled=true`.

## Table of contents

- [What is already in the repo](#what-is-already-in-the-repo)
- [Deploy clicks](#deploy-clicks)
- [Failure hints](#failure-hints)
- [Manual alternative](#manual-alternative)
- [Submission](#submission)

---

## What is already in the repo

| Item | Value |
|------|--------|
| GitHub | https://github.com/zakard114/hotel-booking-cancellation (`main`) |
| Model | `models/model.bin` is tracked (`!models/model.bin`) |
| PORT | `src/predict.py` reads `os.environ.get("PORT", "9696")`, `debug=False`, `0.0.0.0` |
| Blueprint | root `render.yaml`, Docker, free plan |
| Desk | `GET /` serves HoldRisk. Ops board: `GET /ops/board` |

[↑ Contents](#table-of-contents)

---

## Deploy clicks

1. https://render.com — sign in with GitHub — https://dashboard.render.com
2. **New +** → **Blueprint**
3. Connect GitHub → repo **`zakard114/hotel-booking-cancellation`**
4. Confirm `render.yaml`, branch **`main`** → **Apply**
5. Check: name `hotel-cancel-api`, oregon, docker, free, `./Dockerfile`, context `.`, health check **`/health`**
6. Success: green **Live** and a header URL ending in `.onrender.com`
7. The free plan can cold-start for 30–60 seconds
8. Smoke with the body in the root README (`$base` = the live URL)

A push to `main` rebuilds this web service.

[↑ Contents](#table-of-contents)

---

## Failure hints

| Symptom | Meaning |
|---------|---------|
| `COPY` / `models` / `No such file` | The image build cannot see `model.bin` |
| `FileNotFoundError` … `model.bin` | The process cannot open the model path at boot |
| `libgomp` / `ImportError` (xgboost) | The slim image is missing OpenMP — check `libgomp1` in the Dockerfile |
| Health check failed | `/health` did not respond, or the process did not bind `PORT` |
| pip / dependency ERROR | `requirements.txt` failed to install |
| Live, but the desk is blank | Open `GET /` after the cold start, or call `GET /health` and `POST /predict` |

[↑ Contents](#table-of-contents)

---

## Manual alternative

**New +** → **Web Service** → Docker → Name `hotel-cancel-api`, Branch `main`, Dockerfile `./Dockerfile`, Context `.`, Free, Health check `/health` → **Create Web Service**.

[↑ Contents](#table-of-contents)

---

## Submission

- Repo: https://github.com/zakard114/hotel-booking-cancellation
- Commit ID: the `main` commit you submit
- Certificate name: **Heeju Yang**

[↑ Contents](#table-of-contents)
