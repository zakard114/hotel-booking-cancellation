# Phase 6 — Containerization (7/9)

**Done** (2026-11-09).

## Table of contents

- [Goal](#goal)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Fill the root `Dockerfile` and prove `docker build` plus `docker run -p 9696:9696` serves one prediction.

[↑ Contents](#table-of-contents)

---

## Output

- `Dockerfile` (Python base, requirements, `src/`, model, `EXPOSE 9696`, CMD `predict.py`)
- Image tag `hotel-cancel`
- Host `POST /predict` returned `cancel_probability≈0.679`, `is_canceled=true`

[↑ Contents](#table-of-contents)

---

## Out of scope

- Cloud deploy (gate 9/9)
- Rewriting train or predict logic
- Build cache or model copies under `C:\Users\...`
- `Co-authored-by` or other AI commit trailers

[↑ Contents](#table-of-contents)

---

## Success

- [x] `docker build -t hotel-cancel .` succeeded
- [x] `docker run -p 9696:9696` started the API
- [x] One host `POST /predict` returned JSON
- [x] No cloud URL was required for this gate

[↑ Contents](#table-of-contents)
