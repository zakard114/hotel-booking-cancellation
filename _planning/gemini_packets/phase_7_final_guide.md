# Phase 7 final guide — reproducibility (8/9)

**Done** (2026-11-09).

## Table of contents

- [Why](#why)
- [What](#what)
- [How](#how)
- [Check](#check)

---

## Why

The earlier gates produced files. This gate checks that a stranger can rerun them from the README alone.

[↑ Contents](#table-of-contents)

---

## What

- README section: data → venv → `train.py` → optional predict or docker
- Seeds: `random_state=42`, XGBoost `seed=42`
- CSV stays gitignored; `data/README.md` is the download note
- Smoke: `python src/train.py` writes `models/model.bin`

[↑ Contents](#table-of-contents)

---

## How

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
.\.venv\Scripts\Activate.ps1
Test-Path .\data\hotel_bookings.csv
python src/train.py
```

`Test-Path` is the check that the CSV the script will read is actually there. `train.py` loads that CSV, fits the vectorizer and XGBoost, and saves `models/model.bin`.

Recorded smoke: `X_train` 95512×254. A pandas `select_dtypes` warning only.

[↑ Contents](#table-of-contents)

---

## Check

- [x] Command order is in the README
- [x] Seeds are in the code and the README
- [x] Download path is in `data/README.md`
- [x] Train smoke succeeded
- [x] Cloud was not part of this gate

[↑ Contents](#table-of-contents)
