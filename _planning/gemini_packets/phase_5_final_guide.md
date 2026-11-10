# Phase 5 final guide — dependency and environment (6/9)

**Done** (2026-11-08).

## Table of contents

- [Why](#why)
- [What](#what)
- [How](#how)
- [Check](#check)

---

## Why

A reviewer needs the same library versions as the run that produced `model.bin` and the API. This gate is the pin file and the install steps, not the image.

[↑ Contents](#table-of-contents)

---

## What

- `requirements.txt` with `==` pins for pandas, numpy, scikit-learn, xgboost, and flask
- README: helper script (optional), `cd` to the clone, activate `.venv`, `pip install -r requirements.txt`
- Smoke import or `python src/predict.py` on port 9696

[↑ Contents](#table-of-contents)

---

## How

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/predict.py
```

`use_e_drive.ps1` points this shell at the E: caches so pip does not fill `C:`. Activate the venv before `pip` and `python`. Skip the helper script if you use default cache locations, and replace the `cd` path with your clone.

[↑ Contents](#table-of-contents)

---

## Check

- [x] Pins exist for the train and predict imports
- [x] README steps match the commands above
- [x] Predict starts without an import error
- [x] Docker was not required to close this gate

[↑ Contents](#table-of-contents)
