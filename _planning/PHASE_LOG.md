# PHASE_LOG — hotel-booking-cancellation

Written when a phase closes. Checkpoints: [`CHECKPOINTS.md`](CHECKPOINTS.md)

## Table of contents

- [Phase 0](#phase-0)
- [Phase 1](#phase-1)
- [Phase 2](#phase-2)
- [Phase 3](#phase-3)
- [Phase 4](#phase-4)
- [Phase 5](#phase-5)
- [Phase 6](#phase-6)
- [Phase 7](#phase-7)
- [Phase 8](#phase-8)

---

## Phase 0

Problem and scaffold (1/9).

- **Status:** **done**
- **Date:** 2026-11-05
- **Work:** Repo scaffold. Phase 0 guide adopted. Product = cancel-risk service.
- **Next at the time:** EDA (2/9)

[↑ Contents](#table-of-contents)

---

## Phase 1

EDA (2/9).

- **Status:** **done**
- **Date:** 2026-11-06
- **Work:** CSV at `data/hotel_bookings.csv`. Notebook: load, missing values, target (~37% cancel), nunique, leakage and feature memo, `train_test_split` seed 42. **No fit.** `scripts/phase1_eda.py` mirrors the notebook.
- **TODOs covered:** Load, Missing, Target, Leakage/feature memo, train/val split
- **Next at the time:** Model training (3/9)

[↑ Contents](#table-of-contents)

---

## Phase 2

Model training (3/9).

- **Status:** **done**
- **Date:** 2026-11-06
- **Work:** `scripts/phase2_models.py` — logistic regression, random forest, XGBoost, small tune. Selected **XGBoost** (validation ROC-AUC about 0.9498).
- **Next at the time:** Export (4/9)

[↑ Contents](#table-of-contents)

---

## Phase 3

Export to `train.py` (4/9).

- **Status:** **done**
- **Date:** 2026-11-07
- **Work:** `src/train.py` — path from the file, XGBoost 150 rounds, `models/model.bin` = pickle `(dv, model)`.
- **Next at the time:** Deployment (5/9)

[↑ Contents](#table-of-contents)

---

## Phase 4

Model deployment (5/9).

- **Status:** **done**
- **Date:** 2026-11-07
- **Work:** `src/predict.py` loads the pickle, drops leakage columns, fills missing values, and serves Flask `POST /predict` on port 9696. One `Invoke-RestMethod` call returned `cancel_probability≈0.679`, `is_canceled=true`.
- **Next at the time:** Dependency and environment (6/9)

[↑ Contents](#table-of-contents)

---

## Phase 5

Dependency and environment (6/9).

- **Status:** **done**
- **Date:** 2026-11-08
- **Work:** `requirements.txt` pins pandas, numpy, scikit-learn, xgboost, and flask. README install path is use_e_drive → cd → activate → `pip install -r`. `python src/predict.py` on :9696 OK. Dockerfile was left for gate 7/9.
- **Next at the time:** Containerization (7/9)

[↑ Contents](#table-of-contents)

---

## Phase 6

Containerization (7/9).

- **Status:** **done**
- **Date:** 2026-11-09
- **Work:** `docker build -t hotel-cancel .` succeeded. `docker run --rm -d -p 9696:9696 --name hotel-cancel-api hotel-cancel` logged model load and Running on. Host `POST /predict` returned probability about 0.679, `is_canceled=true`. Container stopped after the test.
- **Next at the time:** Reproducibility (8/9)

[↑ Contents](#table-of-contents)

---

## Phase 7

Reproducibility (8/9).

- **Status:** **done**
- **Date:** 2026-11-09
- **Work:** README reproduce order and seed 42. `data/README.md` kept (CSV gitignored). `python src/train.py` smoke OK → `models/model.bin` (X_train 95512×254; a pandas `select_dtypes` warning only). Reproducibility score 1/1.
- **Next at the time:** Cloud deployment (9/9, bonus)

[↑ Contents](#table-of-contents)

---

## Phase 8

Cloud deployment (9/9, bonus).

- **Status:** **done**
- **Date:** 2026-11-10 (opened 2026-11-09)
- **Work:** Render Live https://hotel-cancel-api.onrender.com. `POST /predict` → probability about 0.6116, `is_canceled=true`. Cloud score **2/2**. Gates 1–9 complete.
- **Next:** Submit the repo URL and commit ID. Certificate name Heeju Yang. Peer reviews (3) are outside the build gates.

[↑ Contents](#table-of-contents)
