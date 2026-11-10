# Phase 5 — Dependency and environment (6/9)

**Done** (2026-11-08).

## Table of contents

- [Goal](#goal)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Pin the packages the project needs and document how to create the environment on E:.

[↑ Contents](#table-of-contents)

---

## Output

- `requirements.txt` with pinned versions (install source of truth)
- README How to run: `use_e_drive` → venv → `pip install -r requirements.txt`

[↑ Contents](#table-of-contents)

---

## Out of scope

- Writing or building the Dockerfile (gate 7/9)
- Cloud (gate 9/9)
- pip or venv caches under `C:\Users\...`

[↑ Contents](#table-of-contents)

---

## Success

- [x] Train and predict packages are pinned
- [x] README has the install and activate steps
- [x] `python src/predict.py` starts in that environment

[↑ Contents](#table-of-contents)
