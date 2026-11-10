# Checkpoints — Hotel Booking Cancellation (ML Zoomcamp 2026 Midterm)

**표로 진행 상태를 고정**하고, 증거가 생기기 전에는 Score/Claimed를 올리지 않는다.  
채점 항목은 **ML Zoomcamp 공식 루브릭만**. 진행할 때마다 이 파일과 README 하단 Evaluation을 같이 갱신한다.

관련: [`ML_ROADMAP_PROTOCOL.md`](ML_ROADMAP_PROTOCOL.md) · [`ROADMAP.md`](ROADMAP.md) · [`PHASE_LOG.md`](PHASE_LOG.md)

---

## A. Roadmap gates (루브릭 → 실행 게이트, n=9)

먼저 **공식 루브릭 이름**, 그다음 **(x/9) 실행 이름**.  
`Status`: `todo` / `doing` / `done`. 닫히기 전 다음 게이트 구현 지침 금지.

| Rubric (공식) | # | Gate (실행) | Status | Done when | Evidence |
|---------------|---|-------------|--------|-----------|----------|
| Problem description | 1/9 | 문제·성공 기준·학습 루프 | **done** | 문제·타깃·출처 설명. Phase 0 지침 채택. PHASE_LOG | 2026-11-05 |
| EDA | 2/9 | 데이터·전처리·EDA·피처 | **done** | 노트북 EDA+피처 초안. 누수 주의. split 시드 | 2026-11-06 notebook + data/hotel_bookings.csv |
| Model training | 3/9 | 다중 모델·튜닝·선정 | **done** | logistic+RF+XGB 비교·튜닝·선정 이유 | 2026-11-06 phase2_models.py XGB~0.95 AUC |
| Export notebook to script | 4/9 | train 스크립트·아티팩트 | **done** | `train.py`가 아티팩트 저장 | 2026-11-07 src/train.py → models/model.bin |
| Model deployment | 5/9 | 예측 웹 서비스 | **done** | 로컬 HTTP 예측 1건 | 2026-11-07 predict.py :9696 → cancel_probability~0.68 |
| Dependency and environment | 6/9 | deps·venv 고정 | **done** | deps 파일+README 설치/활성화 | 2026-11-08 requirements 5 pin + README How to run; predict :9696 OK |
| Containerization | 7/9 | Docker 이미지·실행 | **done** | build+run으로 API 기동 | 2026-11-09 hotel-cancel build+run :9696; POST cancel_probability≈0.679 |
| Reproducibility | 8/9 | 재현 점검·README 증거 | **done** | 남이 따라 할 수 있는 실행 경로 검증 (data 안내·시드·README·train/노트북) | 2026-11-09 README reproduce + train.py OK |
| Cloud deployment (bonus) | 9/9 | 클라우드·제출 마감 | **done** | (선택) URL/시연 + Commit ID 제출 준비 | 2026-11-10 Live https://hotel-cancel-api.onrender.com — POST /predict → cancel_probability≈0.6116, is_canceled=true |

Peer reviews = 제출 후(빌드 게이트 밖).

**지금:** Cloud deployment (bonus) / **(9/9) done**. Midterm build gates **1–9 전부 완료**. 다음은 제출·Peer reviews (빌드 게이트 밖).

---

## B. Course rubric (self-score, max 16 + peer extra)

공식: [projects README](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/projects/README.md).  
**Score는 실제 산출물이 있을 때만** 올린다.

| # | Criterion | Max | Score | What this repo has (Evidence) |
|---|-----------|----:|------:|-------------------------------|
| 1 | Problem description | 2 | 1 | README Problem 초안 + Phase 0 가이드. 맥락·사용처는 더 다듬을 여지 → 만점(2)은 README 보강 후 |
| 2 | EDA | 2 | 2 | notebook + `scripts/phase1_eda.py`: load/missing/target/leakage memo/seeded split |
| 3 | Model training | 3 | 3 | `scripts/phase2_models.py` — LR/RF/XGB + tune; winner XGB AUC~0.95 |
| 4 | Export notebook to script | 1 | 1 | `src/train.py` → `models/model.bin` (dv, xgb) |
| 5 | Reproducibility | 1 | 1 | README reproduce + data/README + seed 42; `python src/train.py` → model.bin (2026-11-09) |
| 6 | Model deployment | 1 | 1 | `src/predict.py` Flask POST /predict; 로컬 1건 성공 |
| 7 | Dependency / environment | 2 | 2 | requirements.txt 5==pin + README use_e_drive→venv→pip install -r; pyproject deps 비움·install truth=requirements |
| 8 | Containerization | 2 | 2 | `docker build -t hotel-cancel .` + run `-p 9696:9696`; POST /predict → cancel_probability≈0.679 |
| 9 | Cloud deployment (bonus) | 2 | 2 | Live https://hotel-cancel-api.onrender.com — POST /predict → cancel_probability≈0.6116, is_canceled=true (2026-11-10) |
| — | **Subtotal (course)** | **16** | **15** | |
| 10 | Peer reviews (extra) | 3 | 0 | 제출 후 동료 3건 |

---

## C. Phase checklists

### Phase 0 (1/9) — done

- [x] 문제 = 호텔 예약 취소 예측 (이진분류), 타깃 `is_canceled`
- [x] 데이터 = Kaggle `jessemostipak/hotel-booking-demand` (금지 주제 아님)
- [x] 제품 경계 = **취소 위험도 서비스가 메인** (부킹 앱 애드온 아님)
- [x] 루트 스캐폴드·README·금지 주제·E:·학습 루프 이해
- [x] Phase 0 가이드 채택 · PHASE_LOG

### Phase 1 (2/9) — done

- [x] CSV `data/hotel_bookings.csv` (E:)
- [x] Load: shape / dtypes / head
- [x] Missing: `isnull().sum`
- [x] Target ratio (~37% canceled)
- [x] Leakage + feature draft memo
- [x] notebook TODO: split을 Phase 1로 맞춤
- [x] `train_test_split(..., random_state=42)` — **no fit**
- [x] PHASE_LOG · A표 2/9 = done

### Phase 7 (8/9) — done

- [x] README How to run / Reproducibility (data → venv → train → 선택 predict/docker)
- [x] Seeds documented (`random_state=42`, XGB `seed=42`)
- [x] `data/README.md` download path (CSV gitignore 유지)
- [x] `python src/train.py` smoke OK → `models/model.bin`
- [x] Evaluation Reproducibility Score=1 + Evidence
- [x] 클라우드 없음

### Phase 8 (9/9, bonus) — done

- [x] `PORT` env in `predict.py` (cloud-ready; local default 9696)
- [x] `render.yaml` + `deploy/README.md` 절차 확인
- [x] Live URL https://hotel-cancel-api.onrender.com — POST /predict → cancel_probability≈0.6116, is_canceled=true
- [x] README Cloud 절 + Evaluation Cloud Score **2/2** (subtotal **15/16**)
- [ ] (선택) 제출: repo URL + Commit ID · Heeju Yang
- [x] 게이트 `done` — 학습자 「클라우드 끝」(2026-11-10)

---

## How we use this

1. 페이즈 시작할 때 **A**에서 해당 행을 `doing`으로.
2. 게이트 닫을 때 `done` + Evidence 채움. README **Evaluation** Score도 같이 올림.
3. 루브릭 점수는 피어/채점자 관점의 **정직한 self-score**. 없으면 0 유지.
4. Cursor는 사용자가 「체크포인트 갱신」/게이트 완료를 말할 때 이 표를 고친다.
