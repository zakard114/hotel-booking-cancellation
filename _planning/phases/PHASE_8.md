# Phase 8 — Cloud deployment (9/9, bonus)

**Done** (2026-11-10).

## Table of contents

- [Goal](#goal)
- [Rubric](#rubric)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Put the Flask API that already runs in Docker on a public host, and keep the deploy notes next to a real URL.

[↑ Contents](#table-of-contents)

---

## Rubric

Official maximum: 2.

- **0:** no cloud deploy
- **1:** the README (or a deploy note) explains how to deploy, next to the code
- **2:** deploy config exists, and there is a test URL or a demo capture

[↑ Contents](#table-of-contents)

---

## Output

- `render.yaml` and [`../../deploy/README.md`](../../deploy/README.md)
- Live URL: https://hotel-cancel-api.onrender.com
- Smoke: `POST /predict` → `cancel_probability≈0.6116`, `is_canceled=true`
- Certificate name: **Heeju Yang**

A push to `main` rebuilds the Render web service.

[↑ Contents](#table-of-contents)

---

## Out of scope

- Re-scoring reproducibility (8/9)
- Putting a URL in the evaluation table before the service is actually live
- Rewriting train or predict logic, or tuning a new model
- Secrets or image caches under `C:\Users\...`
- AI commit trailers

[↑ Contents](#table-of-contents)

---

## Success

- [x] Deploy steps and config files exist
- [x] Public URL: https://hotel-cancel-api.onrender.com
- [x] Gate 9/9 `done` and cloud score **2/2** (2026-11-10)
- [x] Gate 8/9 stays done

[↑ Contents](#table-of-contents)
