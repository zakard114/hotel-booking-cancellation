# Phase 3 paste — export to train.py (4/9)

Scope note. Move the winning pipeline into `src/train.py` and save `models/model.bin`. Do not build the API.

## Table of contents

- [Rules](#rules)
- [Order](#order)
- [Success](#success)

---

## Rules

- Winner from Phase 2: XGBoost.
- Same leakage drop, same seed 42, DictVectorizer fit on train only.
- Save `(DictVectorizer, model)` with pickle.
- No Flask, no Docker, no cloud.

[↑ Contents](#table-of-contents)

---

## Order

1. Resolve the repo root from `Path(__file__)`, not from the shell cwd.
2. Read `data/hotel_bookings.csv`, drop leakage columns, split 80/20 with seed 42.
3. Fill numeric gaps with 0 and category gaps with `"missing"`.
4. `DictVectorizer` fit on train, transform validation only as a check.
5. `xgb.train` for 150 rounds with `seed=42`.
6. Write `models/model.bin`.

**Done** 2026-11-07.

[↑ Contents](#table-of-contents)

---

## Success

- [x] `python src/train.py` writes `models/model.bin`
- [x] The file loads as `(dv, model)` in `predict.py`

[↑ Contents](#table-of-contents)
