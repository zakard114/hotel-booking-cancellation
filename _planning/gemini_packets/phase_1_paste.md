# Phase 1 paste — EDA (2/9)

Scope note for the EDA gate. Help with load, EDA, a feature draft, and a seeded split. Do not train a model or write the API.

## Table of contents

- [Rules](#rules)
- [Paths](#paths)
- [Data](#data)
- [Order](#order)
- [Out of scope](#out-of-scope)
- [Success](#success)
- [Output shape](#output-shape)

---

## Rules

- Use only facts in this note. Do not invent URLs, commands, or numbers.
- Short Why / What / How / check per step. Do not paste a finished training script.
- Gate stays **EDA (2/9)**.
- Topic stays `is_canceled`.
- Caches and the venv stay on **E:**. Before install or download: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.
- Forbidden here: model training, tuning, `predict.py`, Docker, commit, cloud.
- If a download exceeds five minutes or needs a Kaggle login, switch to the browser and stop waiting.
- End with two or three check questions and “next guide after permission”.

[↑ Contents](#table-of-contents)

---

## Paths

| What | Path |
|------|------|
| Root | `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\` |
| Data note | `data\README.md` |
| Expected CSV | `data\hotel_bookings.csv` |
| Notebook | `notebooks\` |
| Cache | `E:\IT_SPACES\AI\.cache\` |
| Plan | `_planning\` |

[↑ Contents](#table-of-contents)

---

## Data

- Source: Kaggle `jessemostipak/hotel-booking-demand`
- Target: `is_canceled`
- Follow `data/README.md` only for the download. Do not add a new URL in this packet.
- If the CSV is missing, explain the README steps. If it is present, start at load.

[↑ Contents](#table-of-contents)

---

## Order

1. **Load** — read the CSV and check shape, columns, and `is_canceled`
2. **EDA** — missing values, target rate, a few category and numeric spreads
3. **Leakage** — columns known only after the booking outcome
4. **Feature draft** — keep, drop, and a short preprocessing note. No training code
5. **Seeded split** — fixed seed. No `fit`, no `predict`, no model object

[↑ Contents](#table-of-contents)

---

## Out of scope

- venv or downloads under `C:\Users\...`
- Banned datasets
- A score leaderboard or a grid search
- Flask, Dockerfile, or cloud
- Invented files or metrics

[↑ Contents](#table-of-contents)

---

## Success

- [x] CSV ready from `data/README.md`
- [x] Load plus `is_canceled` checked
- [x] Missing values and target rate recorded
- [x] Leakage candidates listed
- [x] Feature keep/drop draft
- [x] Seeded train/val split only
- [x] No training, API, or Docker

[↑ Contents](#table-of-contents)

---

## Output shape

Each step: Why, What, How (a short hint), and one check line.  
At the end: two or three questions, then “next guide after permission”.

[↑ Contents](#table-of-contents)
