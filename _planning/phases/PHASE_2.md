# Phase 2 — Models (3/9)

**Done** (2026-11-06).

## Table of contents

- [Goal](#goal)
- [Output](#output)
- [Out of scope](#out-of-scope)
- [Success](#success)

---

## Goal

Train logistic regression, a random forest, and XGBoost. Compare them on the validation split and pick one. A small tune is part of the comparison.

[↑ Contents](#table-of-contents)

---

## Output

`scripts/phase2_models.py`. Selected model: XGBoost, validation ROC-AUC about 0.95. The target is about 37% canceled, so the comparison metric is ROC-AUC. Leakage columns are excluded. Seed is 42.

[↑ Contents](#table-of-contents)

---

## Out of scope

Final export in `train.py`, the service, Docker, and cloud.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Linear model plus tree models (three models)
- [x] Validation metric and a short reason for the winner
- [x] Same split and preprocessing for every model

[↑ Contents](#table-of-contents)
