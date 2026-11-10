# Roadmap protocol — Hotel Booking Cancellation

Course rubric items are the pipeline names. Each item has an execution gate `(x/9)`. This file maps those gates onto HoldRisk.

**Product boundary:** the cancel-risk service is the product (`is_canceled`). It is not a booking-site add-on.

- Checks: [`CHECKPOINTS.md`](CHECKPOINTS.md) — scores use the official rubric only
- Root: `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\`
- **n = 9** build gates. Peer reviews are after submit.

Read order: rubric role → gate `(x/9)` → what this repo did.

Official list: [ML Zoomcamp projects](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/projects/README.md)

## Table of contents

- [Problem description](#problem-description)
- [EDA](#eda)
- [Model training](#model-training)
- [Export notebook to script](#export-notebook-to-script)
- [Model deployment](#model-deployment)
- [Dependency and environment](#dependency-and-environment)
- [Containerization](#containerization)
- [Reproducibility](#reproducibility)
- [Cloud deployment](#cloud-deployment)
- [At a glance](#at-a-glance)

---

## Problem description

The entrance: problem, context, and who uses the result.

Gate work: target, metric, banned topics, repo skeleton, learning loop. No EDA or training code.

This repo: binary `is_canceled`. Kaggle hotel-booking-demand. **Done** 2026-11-05. README Problem is the score-2 evidence.

[↑ Contents](#table-of-contents)

---

## EDA

Check the table before any fit: missing values, target, features, leakage.

Gate work: how to get the data, drop leakage, EDA notebook, seeded split, feature draft.

This repo: `data/` + `notebooks/notebook.ipynb`. About 37% canceled. Post-booking columns excluded. **Done** 2026-11-06.

[↑ Contents](#table-of-contents)

---

## Model training

Compare models, tune, and record why one was chosen.

Gate work: same preprocessing and split, validation metric, selection note.

This repo: logistic regression, random forest, and XGBoost. Validation ROC-AUC. Winner XGBoost, about 0.95. **Done** 2026-11-06.

[↑ Contents](#table-of-contents)

---

## Export notebook to script

The exploration stays in the notebook. The final train run lives in a script.

Gate work: winning pipeline only, in `train.py`, preprocessor and model saved together.

This repo: `src/train.py` → `models/model.bin`. **Done** 2026-11-07.

[↑ Contents](#table-of-contents)

---

## Model deployment

Serve the model over HTTP.

Gate work: Flask `predict` and `health`. One local call succeeds.

This repo: `src/predict.py`. JSON in, cancel probability and label out. **Done** 2026-11-07.

[↑ Contents](#table-of-contents)

---

## Dependency and environment

Someone else can install the same libraries.

Gate work: pinned requirements and README install steps. Docker is the next gate, not this one.

This repo: `requirements.txt` pins and the README How to run block. **Done** 2026-11-08.

[↑ Contents](#table-of-contents)

---

## Containerization

The service runs from an image, including the OS libraries.

Gate work: Dockerfile, documented `build` and `run`, one prediction from the container. Gate 6/9 is already closed.

This repo: root `Dockerfile`, port 9696, health and predict from the container. **Done** 2026-11-09.

[↑ Contents](#table-of-contents)

---

## Reproducibility

A reviewer can rerun the notebook and `train.py` without guessing where the data is.

Gate work: download path, seeds, and command order in the README.

This repo: README reproduce steps, seed 42, `train.py` smoke. Score 1/1. **Done** 2026-11-09.

[↑ Contents](#table-of-contents)

---

## Cloud deployment

Optional public URL on top of the local image.

Gate work: Render (or equivalent) plus a README deploy section. Submit form: repo URL and commit ID. Certificate name: Heeju Yang.

This repo: **done** 2026-11-10. Live https://hotel-cancel-api.onrender.com — `POST /predict` → probability about 0.6116, `is_canceled=true`. Cloud score **2/2**.

[↑ Contents](#table-of-contents)

---

## At a glance

```text
Problem description            → (1/9) problem and loop        [done]
EDA                            → (2/9) data, EDA, features     [done]
Model training                 → (3/9) models, tune, select    [done]
Export notebook to script      → (4/9) train script, artifact  [done]
Model deployment               → (5/9) predict API             [done]
Dependency and environment     → (6/9) deps and venv           [done]
Containerization               → (7/9) Docker                  [done]
Reproducibility                → (8/9) reproduce path          [done]
Cloud deployment (bonus)       → (9/9) cloud and submit        [done]
Peer reviews (extra)           → after submit
```

Older `phases/PHASE_*` files keep their names. The mapping is:

| Gate | Older file (approx.) |
|------|----------------------|
| (1/9) | PHASE_0 |
| (2/9) | PHASE_1 |
| (3/9) | PHASE_2 |
| (4/9) | PHASE_3 |
| (5/9) | PHASE_4 |
| (6/9) and (7/9) | PHASE_5 split into deps and Docker |
| (8/9) and (9/9) | later files split into reproduce and cloud |

New notes use `(x/9)` plus the rubric name.

[↑ Contents](#table-of-contents)
