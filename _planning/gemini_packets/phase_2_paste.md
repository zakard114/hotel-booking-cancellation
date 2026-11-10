# Phase 2 paste — model training (3/9)

Scope note. Compare logistic regression, a random forest, and XGBoost on the Phase 1 split. Do not export `train.py` or start the API.

## Table of contents

- [Rules](#rules)
- [Order](#order)
- [Success](#success)

---

## Rules

- Same preprocessing and the same `random_state=42` split for every model.
- Drop `reservation_status` and `reservation_status_date`.
- Metric: ROC-AUC (the cancel rate is about 37%).
- A small depth or round sweep is enough. No giant search.
- Stay on E:. No Docker, no cloud, no commit trailer.

[↑ Contents](#table-of-contents)

---

## Order

1. Load the CSV and repeat the Phase 1 split.
2. Fit logistic regression and record validation ROC-AUC.
3. Fit a random forest and try a few `max_depth` values.
4. Fit XGBoost (`seed=42`) and try a few `num_boost_round` values.
5. Print the comparison and the winner.

Script: `scripts/phase2_models.py`. Result: XGBoost, validation ROC-AUC about 0.95. **Done** 2026-11-06.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Three model families on one split
- [x] Validation ROC-AUC printed for each
- [x] Winner named, with the leakage columns unused
- [x] No API and no Docker

[↑ Contents](#table-of-contents)
