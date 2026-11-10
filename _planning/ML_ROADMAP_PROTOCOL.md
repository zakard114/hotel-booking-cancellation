# ML 프로젝트 범용 로드맵 프로토콜 + 호텔 예약 취소 대입

**코스 루브릭 요소**를 파이프라인 대명사로 두고, 각 요소에 **실행 게이트 `(x/9)`** 를 1:1에 가깝게 붙인 뒤, **Hotel Booking Cancellation** 을 대입한다.  
루브릭에 맞춰 단계를 늘리는 것이 원칙이다 (묶음은 예외적으로만).

**제품 경계:** 부킹 플랫폼 애드온이 아님. **메인 = 예약 취소 위험도 예측 서비스** (`is_canceled`).

- 스킬: `ml-project-roadmap-protocol`
- 루프: `phase-gemini-beginner-guide` · [`STUDY_WORKFLOW.md`](STUDY_WORKFLOW.md)
- 체크: [`CHECKPOINTS.md`](CHECKPOINTS.md) — Score는 **공식 루브릭만**
- 루트: `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\`
- **n = 9** (빌드 게이트). Peer reviews는 제출 후(표 밖).

읽는 법: **루브릭 의미 → 게이트 (x/9) 개요·용도 → 호텔 대입**.

공식: [ML Zoomcamp projects](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/projects/README.md)

---

## Problem description (max 2) · 로드맵 (1/9)

### 코스 루브릭 — 파이프라인에서의 역할

문제·맥락·사용 장면을 말해 주는 입구. 여기가 흐리면 이후 단계가 전부 공중분해된다.

### 로드맵 게이트 (1/9) — 문제·성공 기준·학습 루프

- 타깃·지표·금지 주제 확인, 레포 뼈대, 배우며 만들기 루프 고정.
- EDA/학습 코드는 하지 않음.

### 호텔 대입

- 이진분류 · `is_canceled` · 취소 위험도 API가 메인.
- Kaggle hotel-booking-demand · E: · 패킷→Gemini→타당성.
- **상태: done** (Phase 0 지침 채택, 2026-11-05).

---

## EDA (max 2) · 로드맵 (2/9)

### 코스 루브릭 — 파이프라인에서의 역할

표를 믿기 전 검증: 결측·범위·타깃·특성·중요도. “그냥 fit”을 막는다.

### 로드맵 게이트 (2/9) — 데이터 확보·전처리·EDA·피처

- 데이터 받는 법 문서화, 누수 제거, EDA 노트북, split 시드/비율.
- 넣을 컬럼 초안까지 (최종 튜닝은 다음).

### 호텔 대입

- `data/` + `notebooks/notebook.ipynb`.
- `is_canceled` 비율, 예약 이후 정보 제외, 범주/수치 분리.

---

## Model training (max 3) · 로드맵 (3/9)

### 코스 루브릭 — 파이프라인에서의 역할

여러 모델 비교·튜닝·선정. 한 모델·무튜닝은 낮은 점수.

### 로드맵 게이트 (3/9) — 다중 모델·튜닝·선정

- 동일 전처리·분할 위에서 후보 학습·검증 지표 비교·선정 이유 기록.

### 호텔 대입

- Logistic + RF + XGB · val ROC-AUC · 선정 한 줄 이유.

---

## Exporting notebook to script (max 1) · 로드맵 (4/9)

### 코스 루브릭 — 파이프라인에서의 역할

탐색(노트북) → 재현(스크립트). 최종 학습이 스크립트에 있어야 한다.

### 로드맵 게이트 (4/9) — train 스크립트·아티팩트

- 우승 파이프라인만 `train.py`로. 전처리기+모델 저장.

### 호텔 대입

- `src/train.py` → `models/` 또는 `artifacts/`.

---

## Model deployment (max 1) · 로드맵 (5/9)

### 코스 루브릭 — 파이프라인에서의 역할

모델을 HTTP 서비스로 제공. 제품 본체의 런타임.

### 로드맵 게이트 (5/9) — 예측 웹 서비스

- Flask/FastAPI `predict` (+ `health`). 로컬 1건 성공.

### 호텔 대입

- `src/predict.py` · JSON → 취소 확률/라벨.

---

## Dependency and environment (max 2) · 로드맵 (6/9)

### 코스 루브릭 — 파이프라인에서의 역할

남이 같은 라이브러리로 돌리게 함. deps 파일 + env/venv 안내.

### 로드맵 게이트 (6/9) — 의존성·가상환경 고정

- requirements/pyproject 등 버전 고정.
- README에 설치·활성화 절차 (E: / use_e_drive).
- **이 게이트에서는 Docker 필수가 아님** — 컨테이너는 다음.

### 호텔 대입

- 루트 deps를 import에 맞게 채움 · README How to run의 venv/pip 구간 완성.

---

## Containerization (max 2) · 로드맵 (7/9)

### 코스 루브릭 — 파이프라인에서의 역할

이미지로 OS까지 맞춰 서비스를 재현. Dockerfile + build/run 문서·실행.

### 로드맵 게이트 (7/9) — Docker 이미지·실행

- Dockerfile 완성, README에 build/run, 실제로 컨테이너에서 API 확인.
- deps(6/9)가 먼저 닫혀 있어야 함.

### 호텔 대입

- 루트 `Dockerfile` · 포트 매핑 · 컨테이너 health+predict.

---

## Reproducibility (max 1) · 로드맵 (8/9)

### 코스 루브릭 — 파이프라인에서의 역할

노트북·train·데이터 접근을 **남이 오류 없이** 따라 할 수 있는지.  
앞 게이트에서 쌓은 안내를 README/체크리스트로 **최종 검증**하는 단계.

### 로드맵 게이트 (8/9) — 재현 점검·README 증거

- 클린 클론(또는 동등) 관점으로: 데이터 받는 법, 시드, 명령 순서가 README에 있는지.
- Evaluation Evidence 링크를 채울 수 있는지 확인.
- 제출용 커밋을 아직 안 박아도 되지만, “이 커밋이면 재현된다” 후보를 정한다.

### 호텔 대입

- README Quick start / data / train / API / docker 문구 정리.
- `CHECKPOINTS`·Evaluation Score를 증거에 맞게 갱신 (과장 금지).
- **상태: done** (2026-11-09) — README reproduce + seed 42 + `train.py` 스모크 · Score 1/1.

---

## Cloud deployment (max 2, bonus) · 로드맵 (9/9)

### 코스 루브릭 — 파이프라인에서의 역할

로컬 Docker 위의 **보너스**. URL 또는 시연 증거. 없어도 본전.

### 로드맵 게이트 (9/9) — (선택) 클라우드·제출 마감

- (선택) Render/Fly 등 + README 배포 절.
- 제출 폼: repo URL + **Commit ID**. Certificate: Heeju Yang.
- 이후 Peer reviews 3건 (별도).

### 호텔 대입

- **상태: done** (2026-11-10). Live https://hotel-cancel-api.onrender.com — POST /predict → cancel_probability≈0.6116, is_canceled=true. Evaluation Cloud **2/2** · subtotal **15/16**. 가이드: `gemini_packets/phase_8_final_guide.md`.

---

## 한눈에

```text
Problem description            → (1/9) 문제·루프              [done]
EDA                            → (2/9) 데이터·EDA·피처         [done]
Model training                 → (3/9) 다중 모델·튜닝        [done]
Export notebook to script      → (4/9) train·아티팩트       [done]
Model deployment               → (5/9) 예측 API              [done]
Dependency and environment     → (6/9) deps·venv            [done]
Containerization               → (7/9) Docker               [done]
Reproducibility                → (8/9) 재현·README 증거     [done]
Cloud deployment (bonus)       → (9/9) 클라우드·제출        [done]
Peer reviews (extra)           → 제출 후
```

### 옛 PHASE 파일 매핑 (참고)

기존 `phases/PHASE_0`…`PHASE_6` 파일명은 당분간 유지할 수 있다. 의미 대응:

| 새 게이트 | 옛 파일 (대략) |
|----------|----------------|
| (1/9) | PHASE_0 |
| (2/9) | PHASE_1 |
| (3/9) | PHASE_2 |
| (4/9) | PHASE_3 |
| (5/9) | PHASE_4 |
| (6/9)+(7/9) | PHASE_5를 deps / Docker로 분할 |
| (8/9)+(9/9) | PHASE_6을 재현 / 클라우드·제출로 분할 |

새 패킷·로그는 **(x/9) + 루브릭 이름**을 기준으로 쓴다.
