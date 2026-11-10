# Phase 8 final guide — cloud (9/9)

**Done** (2026-11-10). Live: https://hotel-cancel-api.onrender.com

## Table of contents

- [Split of work](#split-of-work)
- [Clicks](#clicks)
- [Smoke](#smoke)
- [Evidence](#evidence)
- [Failures](#failures)
- [Submission](#submission)

---

## Split of work

| Piece | State |
|-------|--------|
| In the repo | `PORT`, `debug=False`, tracked `models/model.bin`, `Dockerfile`, `render.yaml`, `deploy/README.md` |
| On Render | Blueprint applied, service **Live** |
| Do not do | Invent a URL, or raise the cloud score before the service is live |

Success bar: green **Live** and a host ending in `.onrender.com`.  
Cloud score **2/2**.

[↑ Contents](#table-of-contents)

---

## Clicks

1. https://render.com → sign in with GitHub
2. https://dashboard.render.com
3. **New +** → **Blueprint** (use a manual Web Service only if Blueprint is blocked)
4. Connect GitHub. If the repo is hidden: GitHub → Settings → Applications → Render → allow `zakard114/hotel-booking-cancellation`, then refresh
5. Select **`zakard114/hotel-booking-cancellation`**
6. Confirm root `render.yaml`, branch **`main`** → **Apply**
7. Confirm name `hotel-cancel-api`, region oregon, runtime docker, plan free, dockerfile `./Dockerfile`, context `.`, health check `/health`
8. Open service **`hotel-cancel-api`** → Logs / Events and wait for the build
9. Copy the Live URL. The free plan can take 30–60 seconds on the first request

Manual fallback: **New +** → **Web Service** → Docker → the same name, branch, Dockerfile, context, and free plan → **Create Web Service**.

[↑ Contents](#table-of-contents)

---

## Smoke

Replace `$base` with the Live URL. The JSON body is the same block as the root README. Expect `cancel_probability` and `is_canceled`.

Recorded result (2026-11-10): `cancel_probability≈0.611555278301239`, `is_canceled=true`.

`GET /` is the HoldRisk desk. `GET /health` is the health check. `POST /predict` is the score.

[↑ Contents](#table-of-contents)

---

## Evidence

1. Root README Cloud section has the real URL
2. `_planning/CHECKPOINTS.md` has the date and the URL
3. Cloud score is 2 because the URL is live, not because a document exists alone

[↑ Contents](#table-of-contents)

---

## Failures

| Symptom | Meaning |
|---------|---------|
| `COPY` / `models` / No such file | `model.bin` is missing from the build |
| `FileNotFoundError` … `model.bin` | The process cannot open the model at boot |
| pip / dependency ERROR | `requirements.txt` failed |
| Health check failed | `/health` did not answer, or `PORT` was not bound |

[↑ Contents](#table-of-contents)

---

## Submission

- Repo: https://github.com/zakard114/hotel-booking-cancellation
- Commit ID: the `main` SHA you submit
- Certificate name: **Heeju Yang**

[↑ Contents](#table-of-contents)
