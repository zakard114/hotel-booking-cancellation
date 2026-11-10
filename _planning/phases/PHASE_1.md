# Phase 1 — Data and EDA (2/9)

**Done** (2026-11-06).

## Table of contents

- [Goal](#goal)
- [Already in the repo](#already-in-the-repo)
- [Work](#work)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Put `hotel_bookings.csv` on E: under `data/`. In the notebook: missing values, target rate, feature draft, leakage note, and a seeded split. Model training is gate 3/9.

[↑ Contents](#table-of-contents)

---

## Already in the repo

- `data/README.md`
- `notebooks/notebook.ipynb`
- `scripts/phase1_eda.py`
- Packet: [`../gemini_packets/phase_1_paste.md`](../gemini_packets/phase_1_paste.md)

[↑ Contents](#table-of-contents)

---

## Work

1. Get the CSV using `data/README.md` (browser if login or a long download blocks the CLI).
2. Load, missing values, `is_canceled` rate, leakage candidates, feature draft, seeded split.
3. No `fit`.

[↑ Contents](#table-of-contents)

---

## Out of scope

Training several models, tuning, `train.py`, the API, Docker, storing files on `C:`.

[↑ Contents](#table-of-contents)

---

## Success

- [x] CSV loaded from E:
- [x] Target, missing values, and feature/leakage memo
- [x] Train/val split with a fixed seed (`random_state=42`)
- [x] No model fit

[↑ Contents](#table-of-contents)
