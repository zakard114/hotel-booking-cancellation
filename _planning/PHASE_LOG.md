# PHASE_LOG — hotel-booking-cancellation

형식: 페이즈가 닫힐 때 Cursor가 짧게 쓰고, 학습자가 읽는다.  
체크포인트: [`CHECKPOINTS.md`](CHECKPOINTS.md)

---

## Phase 0 — Problem & scaffold (1/9)

- **상태:** **done**
- **날짜:** 2026-11-05
- **한 일:** 레포 스캐폴드. Gemini Phase 0 가이드 → 타당성 → 채택. 제품 = 취소 위험도 서비스(메인).
- **다음:** 당시 EDA (2/9)

---

## Phase 1 — EDA (2/9)

- **상태:** **done**
- **날짜:** 2026-11-06
- **한 일:** CSV 확보(`data/hotel_bookings.csv`). 노트북 Load/결측/타깃(~37% cancel)/nunique/누수·피처 메모/`train_test_split` seed=42. **fit 없음**. TODO를 Phase 1에 split 포함하도록 정리. VS Code용 `scripts/phase1_eda.py` 미러 추가.
- **커버한 TODO:** Load · Missing · Target · Leakage/Feature memo · Train/Val split
- **다음:** Model training **(3/9)**

---

## Phase 2 — Model training (3/9)

- **상태:** **done**
- **날짜:** 2026-11-06
- **한 일:** `scripts/phase2_models.py` — LR/RF/XGB, 소규모 튜닝, 선정 **XGBoost** (val ROC-AUC ~0.9498).
- **다음:** Export **(4/9)**

---

## Phase 3 — Export to train.py (4/9)

- **상태:** **done**
- **날짜:** 2026-11-07
- **한 일:** `src/train.py` — Path 루트, XGB rounds=150, `models/model.bin` = pickle `(dv, model)`.
- **다음:** Deployment **(5/9)**

---

## Phase 4 — Model deployment (5/9)

- **상태:** **done**
- **날짜:** 2026-11-07
- **한 일:** `src/predict.py` — Path 루트·pickle 로드·`predict_single`(누수 drop·결측·dv·DMatrix feature_names)·Flask POST `/predict` :9696. Invoke-RestMethod 1건 → `cancel_probability≈0.679` / `is_canceled=True`.
- **다음:** Dependency & environment **(6/9)**

---

## Phase 5 — Dependency and environment (6/9)

- **상태:** **done**
- **날짜:** 2026-11-08
- **한 일:** `requirements.txt` 5 pin (pandas/numpy/sklearn/xgboost/flask). README How to run = use_e_drive→cd→Activate→pip install -r→predict; install truth = requirements.txt. `python src/predict.py` :9696 OK. Dockerfile 미변경(7/9).
- **다음:** Containerization **(7/9)**

---

## Phase 6 — Containerization (7/9)

- **상태:** **done**
- **날짜:** 2026-11-09
- **한 일:** Dockerfile(주석 포함) 유지. `docker build -t hotel-cancel .` 성공(sha256:473abe55…). `docker run --rm -d -p 9696:9696 --name hotel-cancel-api hotel-cancel` → 로그 `Model loaded` / `Running on`. 호스트 `POST /predict` → `cancel_probability≈0.679` / `is_canceled=true`. README docker one-liner·Evaluation Containerization 2/2. 테스트 후 `docker stop hotel-cancel-api`.
- **다음:** Reproducibility **(8/9)**

---

## Phase 7 — Reproducibility (8/9)

- **상태:** **done**
- **날짜:** 2026-11-09
- **한 일:** README How to run/Reproducibility(데이터→venv→train→선택 predict/docker)·시드 42 문서화. `data/README.md` 유지(CSV gitignore). `python src/train.py` 스모크 OK → `models/model.bin` (X_train 95512×254; Pandas select_dtypes Warning만). Cursor `phase_7_final_guide.md`. Evaluation Reproducibility 1/1 · subtotal 13/16.
- **다음:** Cloud deployment **(9/9, 보너스)**

---

## Phase 8 — Cloud deployment (9/9, bonus)

- **상태:** **done**
- **날짜:** 2026-11-10 (닫기; 오픈 2026-11-09)
- **한 일:** Render Live https://hotel-cancel-api.onrender.com. POST /predict → cancel_probability≈0.6116, is_canceled=true. README Cloud Evidence + Evaluation **2/2** · subtotal **15/16**. 학습자 「클라우드 끝」으로 게이트 9/9 닫음. Midterm build gates 1–9 완료.
- **다음:** (선택) 제출 폼 repo URL + Commit ID · Certificate Heeju Yang · Peer reviews 3건 (빌드 게이트 밖).

