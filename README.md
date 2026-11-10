> **DEPRECATED (2026-11-05)** - This midterm topic is **retired**. Active project: **Flight Delay Prediction** at `E:\IT_SPACES\AI\Projects\ml\flight-delay-prediction\`. Keep this folder for archive only; do not continue hotel-cancel work unless the user explicitly reopens it.
# Hotel Booking Cancellation

Binary classification midterm for **Machine Learning Zoomcamp 2026**.

Predict whether a hotel booking will be canceled (`is_canceled`) so operations can plan overbooking and staffing with less guesswork.

| | |
|---|---|
| Certificate name | Heeju Yang |
| Deadline | ~16??7 November 2026 |
| Dataset | [hotel-booking-demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) (Antonio et al.) |
| Repo path (local) | `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\` |

> Evidence scores stay at **0** until that criterion is actually done. Do not raise a claim early.

## Problem

Hotels take reservations that guests may cancel. A cancel/no-cancel model helps revenue and front-desk planning. This project trains several classifiers on a public hotel booking table, exports training to a script, and serves the chosen model behind a small HTTP API in Docker.

**Out of scope for midterm:** car price, telco churn, credit risk, clothing datasets; full cloud deploy is optional bonus only after local Docker works.

## How to run / Reproducibility

Install truth = `requirements.txt` (not `pyproject.toml`).  
CSV와 `models/model.bin`은 용량·gitignore로 **레포에 없을 수 있음** — 아래 순서로 받으면 노트북과 `train.py`를 다시 돌릴 수 있다.

**Seeds (재현):** `train_test_split(..., random_state=42)` · XGBoost `params["seed"]=42` (`src/train.py`, Phase 1–2와 동일).

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 1) Data — see data/README.md (Kaggle / browser ZIP / public mirror)
#    Expected: data/hotel_bookings.csv

# 2) Train (writes models/model.bin)
python src/train.py

# 3) Notebook (EDA + model selection): notebooks/notebook.ipynb

# 4) Optional — local API
python src/predict.py

# 5) Optional — Docker
docker build -t hotel-cancel . ; docker run --rm -p 9696:9696 hotel-cancel
```

## Cloud / How to run cloud

**Live URL:** https://hotel-cancel-api.onrender.com  
(Free tier may cold-start 30–60s+ on the first request.)

**HoldRisk desk UI:** open the Live URL `/` (Ops at top-right → Inspector / Log / API / Grafana).  
Health: `GET /health` · Predict: `POST /predict` · Ops board: `GET /ops/board`

```powershell
$base = "https://hotel-cancel-api.onrender.com"
$body = @{
  hotel = "City Hotel"; lead_time = 50
  arrival_date_year = 2017; arrival_date_month = "July"
  arrival_date_week_number = 27; arrival_date_day_of_month = 1
  stays_in_weekend_nights = 1; stays_in_week_nights = 2
  adults = 2; children = 0; babies = 0; meal = "BB"; country = "PRT"
  market_segment = "Online TA"; distribution_channel = "TA/TO"
  is_repeated_guest = 0; previous_cancellations = 0
  previous_bookings_not_canceled = 0
  reserved_room_type = "A"; assigned_room_type = "A"
  booking_changes = 0; deposit_type = "No Deposit"
  agent = "9"; company = "missing"; days_in_waiting_list = 0
  customer_type = "Transient"; adr = 100.0
  required_car_parking_spaces = 0; total_of_special_requests = 1
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$base/predict" `
  -ContentType "application/json" -Body $body
```

```bash
curl -X POST "https://hotel-cancel-api.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"hotel":"City Hotel","lead_time":50,"arrival_date_year":2017,"arrival_date_month":"July","arrival_date_week_number":27,"arrival_date_day_of_month":1,"stays_in_weekend_nights":1,"stays_in_week_nights":2,"adults":2,"children":0,"babies":0,"meal":"BB","country":"PRT","market_segment":"Online TA","distribution_channel":"TA/TO","is_repeated_guest":0,"previous_cancellations":0,"previous_bookings_not_canceled":0,"reserved_room_type":"A","assigned_room_type":"A","booking_changes":0,"deposit_type":"No Deposit","agent":"9","company":"missing","days_in_waiting_list":0,"customer_type":"Transient","adr":100.0,"required_car_parking_spaces":0,"total_of_special_requests":1}'
```

Sample smoke (2026-11-10): `cancel_probability≈0.611555278301239`, `is_canceled=True`.  
Deploy notes: [`deploy/README.md`](deploy/README.md).

## Project layout

```text
data/           # download instructions; CSV usually gitignored
notebooks/      # EDA + model selection notebook
src/train.py    # final training script → models/model.bin
src/predict.py  # Flask desk UI + POST /predict + GET /ops/board
ui_dummy/       # HoldRisk front-end (served at / and /ui/*)
Dockerfile      # container for the Flask predict API
_planning/      # roadmap, phase packs, Gemini paste files
```

## Learning workflow

We build **one phase at a time**: Cursor drafts a phase packet ??paste into Gemini for a beginner Korean guide ??refine if stuck ??Cursor runs **?섏젙??/ ?섏젙遺덊븘** validity check ??only the clean guide is the execution source.

See `_planning/STUDY_WORKFLOW.md` and skill `phase-gemini-beginner-guide`.

## Evaluation criteria (self-score)

Checkpoint tables use official ZoomCamp rubric only. **Score stays 0 until real evidence exists.**  
Working copy (roadmap gates + phase checklists): [`_planning/CHECKPOINTS.md`](_planning/CHECKPOINTS.md).

| # | Criterion | Max | Score | What this repo has (Evidence) |
|---|-----------|----:|------:|-------------------------------|
| 1 | Problem description | 2 | 1 | [Problem](#problem) + Phase 0 guide. Raise to 2 after richer context in README |
| 2 | EDA | 2 | 2 | notebook + scripts/phase1_eda.py (load, missing, target, leakage memo, seeded split) |
| 3 | Model training | 3 | 3 | scripts/phase2_models.py — LR/RF/XGB; winner XGB AUC~0.95 |
| 4 | Export notebook to script | 1 | 1 | src/train.py → models/model.bin |
| 5 | Reproducibility | 1 | 1 | data/README + README reproduce steps + seed 42; `python src/train.py` OK (2026-11-09) |
| 6 | Model deployment | 1 | 1 | Flask POST /predict; local JSON 1건 OK |
| 7 | Dependency / environment | 2 | 2 | requirements.txt 5==pin + README install/activate (use_e_drive→venv→pip -r) |
| 8 | Containerization | 2 | 2 | `docker build -t hotel-cancel .` + `docker run -p 9696:9696`; POST /predict OK |
| 9 | Cloud deployment (bonus) | 2 | 2 | Live https://hotel-cancel-api.onrender.com — POST /predict → cancel_probability≈0.6116, is_canceled=True |
| — | **Subtotal** | **16** | **15** | |
| 10 | Peer reviews (extra) | 3 | 0 | after 3 peer reviews |

Official criteria: [ML Zoomcamp projects README](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/projects/README.md).

## License / data

Dataset is third-party (Kaggle / original paper authors). Follow their license. This repo?셲 code will be whatever license you choose at submit time.
