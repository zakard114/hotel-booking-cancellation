# Phase 5 paste — dependency and environment (6/9)

Scope note. Pin `requirements.txt` and document the venv install. Do not build Docker.

## Table of contents

- [Rules](#rules)
- [Packages](#packages)
- [Order](#order)
- [Success](#success)

---

## Rules

- Gate **(6/9)** only. Containerization is 7/9. Cloud is 9/9.
- Read versions from the environment (`pip show`). Do not guess pins.
- E: only. Before install: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.
- Do not rewrite train or predict logic.
- Install source of truth: `requirements.txt`. `pyproject.toml` is not the install path.

[↑ Contents](#table-of-contents)

---

## Packages

Minimum set for train and predict: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `flask`. Optional notebook packages stay out of the required pin list.

[↑ Contents](#table-of-contents)

---

## Order

1. Activate the project `.venv`.
2. Record installed versions.
3. Write `package==version` lines in `requirements.txt`.
4. Put the same commands in the README How to run section.
5. Smoke: `python src/predict.py` imports and starts.

**Done** 2026-11-08. Five packages are pinned. Predict on port 9696 starts.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Required packages pinned
- [x] README install steps match the commands
- [x] Dockerfile left for the next gate

[↑ Contents](#table-of-contents)
