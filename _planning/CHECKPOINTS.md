# Checkpoints — Hotel Booking Cancellation (ML Zoomcamp 2026 Midterm)

The tables below are the status record. A score moves only when the evidence exists. Criteria are the official ML Zoomcamp rubric only. Update this file and the README evaluation together.

Related: [`ML_ROADMAP_PROTOCOL.md`](ML_ROADMAP_PROTOCOL.md) · [`ROADMAP.md`](ROADMAP.md) · [`PHASE_LOG.md`](PHASE_LOG.md)

## Table of contents

- [Roadmap gates](#roadmap-gates)
- [Course rubric](#course-rubric)
- [Phase checklists](#phase-checklists)
- [How we use this](#how-we-use-this)

---

## Roadmap gates

Official rubric name first, then the `(x/9)` execution name. Status is `todo`, `doing`, or `done`.

| Rubric | # | Gate | Status | Done when | Evidence |
|--------|---|------|--------|-----------|----------|
| Problem description | 1/9 | Problem, success bar, learning loop | **done** | Problem, target, and source are written. Phase 0 adopted. | 2026-11-05 |
| EDA | 2/9 | Data, preprocessing, EDA, features | **done** | Notebook EDA and feature draft. Leakage noted. Seeded split. | 2026-11-06 notebook + `data/hotel_bookings.csv` |
| Model training | 3/9 | Several models, tuning, selection | **done** | Logistic regression, random forest, and XGBoost compared. | 2026-11-06 `phase2_models.py`, XGBoost AUC about 0.95 |
| Export notebook to script | 4/9 | Train script and artifact | **done** | `train.py` saves the artifact | 2026-11-07 `src/train.py` → `models/model.bin` |
| Model deployment | 5/9 | Prediction web service | **done** | One local HTTP prediction | 2026-11-07 `predict.py` :9696 → cancel probability about 0.68 |
| Dependency and environment | 6/9 | Pinned deps and venv | **done** | Deps file plus README install steps | 2026-11-08 five pins in `requirements.txt`; predict on :9696 OK |
| Containerization | 7/9 | Docker image and run | **done** | `build` and `run` start the API | 2026-11-09 image `hotel-cancel` on :9696; POST probability about 0.679 |
| Reproducibility | 8/9 | Reproduce path and README evidence | **done** | Someone else can follow data, seed, README, and `train.py` | 2026-11-09 README reproduce steps; `train.py` OK |
| Cloud deployment (bonus) | 9/9 | Cloud and submit | **done** | Public URL plus a smoke call | 2026-11-10 https://hotel-cancel-api.onrender.com — probability about 0.6116, `is_canceled=true` |

Peer reviews happen after submit. They are outside the build gates.

**Now:** Cloud deployment (9/9) is **done**. Gates 1–9 are complete. Next is the submission form and peer reviews.

[↑ Contents](#table-of-contents)

---

## Course rubric

Official list: [projects README](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/projects/README.md). Raise a score only when the artifact exists.

| # | Criterion | Max | Score | Evidence |
|---|-----------|----:|------:|----------|
| 1 | Problem description | 2 | 2 | README Problem: user, target `is_canceled`, and product boundary |
| 2 | EDA | 2 | 2 | notebook + `scripts/phase1_eda.py`: load, missing, target, leakage memo, seeded split |
| 3 | Model training | 3 | 3 | `scripts/phase2_models.py` — logistic regression, random forest, XGBoost; winner XGBoost, AUC about 0.95 |
| 4 | Export notebook to script | 1 | 1 | `src/train.py` → `models/model.bin` (`dv`, `xgb`) |
| 5 | Reproducibility | 1 | 1 | README reproduce steps + `data/README.md` + seed 42; `python src/train.py` (2026-11-09) |
| 6 | Model deployment | 1 | 1 | `src/predict.py` Flask `POST /predict`; one local call succeeded |
| 7 | Dependency / environment | 2 | 2 | `requirements.txt` five `==` pins; README install path; install source is `requirements.txt` |
| 8 | Containerization | 2 | 2 | `docker build -t hotel-cancel .` and run `-p 9696:9696`; POST probability about 0.679 |
| 9 | Cloud deployment (bonus) | 2 | 2 | Live https://hotel-cancel-api.onrender.com — probability about 0.6116, `is_canceled=true` (2026-11-10) |
| — | **Subtotal** | **16** | **16** | |
| 10 | Peer reviews (extra) | 3 | 0 | three peer reviews after submit |

[↑ Contents](#table-of-contents)

---

## Phase checklists

### Phase 0 (1/9) — done

- [x] Problem: predict hotel booking cancellation (binary), target `is_canceled`
- [x] Data: Kaggle `jessemostipak/hotel-booking-demand` (not a banned topic)
- [x] Product boundary: the cancel-risk service is the product
- [x] Root scaffold, README, banned topics, E: drive, learning loop
- [x] Phase 0 guide adopted · PHASE_LOG

### Phase 1 (2/9) — done

- [x] CSV `data/hotel_bookings.csv` on E:
- [x] Load: shape, dtypes, head
- [x] Missing: `isnull().sum`
- [x] Target ratio (~37% canceled)
- [x] Leakage and feature draft
- [x] Notebook TODO includes the Phase 1 split
- [x] `train_test_split(..., random_state=42)` — no fit
- [x] PHASE_LOG · gate 2/9 = done

### Phase 7 (8/9) — done

- [x] README How to run (data → venv → train → optional predict/docker)
- [x] Seeds documented (`random_state=42`, XGBoost `seed=42`)
- [x] `data/README.md` download path (CSV stays gitignored)
- [x] `python src/train.py` smoke OK → `models/model.bin`
- [x] Reproducibility score 1 with evidence
- [x] Cloud was still out of this gate when it closed

### Phase 8 (9/9, bonus) — done

- [x] `PORT` env in `predict.py` (cloud-ready; local default 9696)
- [x] `render.yaml` + `deploy/README.md`
- [x] Live URL https://hotel-cancel-api.onrender.com — POST probability about 0.6116, `is_canceled=true`
- [x] README Cloud section + cloud score **2/2** (subtotal **16/16** after the problem section was filled in)
- [ ] Optional submit form: repo URL + commit ID · Heeju Yang
- [x] Gate `done` on 2026-11-10

[↑ Contents](#table-of-contents)

---

## How we use this

1. At the start of a phase, set that row in the gates table to `doing`.
2. When the gate closes, set `done` and fill Evidence. Raise the README score in the same edit.
3. Self-scores stay honest. Missing evidence stays 0.
4. Edit this table when a gate is actually finished.

[↑ Contents](#table-of-contents)
