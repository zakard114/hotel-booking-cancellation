# Phase 7 — Reproducibility (8/9)

**Done** (2026-11-09).

## Table of contents

- [Goal](#goal)
- [Rubric](#rubric)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

A reviewer can follow the README from data download through the environment to `train.py` (and the notebook) without a missing step. This gate does not deploy to the cloud.

[↑ Contents](#table-of-contents)

---

## Rubric

Official maximum: 1.

- **0:** the notebook or train script cannot be run, or the data cannot be obtained
- **1:** the notebook and `train.py` rerun cleanly, and the data is either committed or the download path is clear

[↑ Contents](#table-of-contents)

---

## Output

- README reproduce section (data, seed, command order)
- `data/README.md`, pinned `requirements.txt`, `random_state=42` and XGBoost `seed=42`
- `python src/train.py` smoke OK (`X_train` 95512×254)

[↑ Contents](#table-of-contents)

---

## Out of scope

- Cloud deploy (gate 9/9)
- A new model or a rewrite of the API
- Data, venv, or caches under `C:\Users\...`
- Forcing the CSV into git (the download note is enough for the point)

[↑ Contents](#table-of-contents)

---

## Success

- [x] README order: data → venv → train → optional predict or docker
- [x] Seeds are visible in the docs or the code
- [x] `data/README.md` explains how to get the CSV
- [x] `python src/train.py` smoke OK
- [x] Reproducibility score = 1 with evidence

[↑ Contents](#table-of-contents)
