# Phase 7 · Reproducibility (8/9) — 최종 실행 가이드

Cursor 작성 초보 나레이션. 재미나이 없이 이 문서만으로 실행한다.

### 1. Why

피어 리뷰어가 내 레포만 보고 **데이터 받기 → 환경 맞추기 → 노트북/`train.py` 다시 돌리기**까지 오류 없이 따라 할 수 있는지 최종 점검하는 단계다.  
공식 루브릭 **Reproducibility (max 1)**: 데이터가 커밋돼 있거나 **받는 법이 분명**하고, 노트북과 train 스크립트를 다시 실행할 수 있으면 1점.  
클라우드 배포(9/9)는 하지 않는다.

### 2. What

* **T1:** README에 **재현(Reproducibility)** 절 — 데이터 → venv → train → (선택) predict/docker
* **T2:** 시드 문서화 (`random_state=42`, XGB `seed=42`)
* **T3:** `data/README.md` 다운로드 경로가 살아 있는지 확인 (CSV는 gitignore 유지)
* **T4:** `python src/train.py` 스모크 (Model saved… / finished OK)
* **T5:** CHECKPOINTS·Evaluation Score=1 + Evidence (과장 금지)
* **하지 말 것:** 클라우드, 새 튜닝, C: 설치, Co-authored 커밋

---

### 3. How

#### Step 1. 환경 (공통)

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
# use_e_drive.ps1: E: 캐시·도구 경로를 이 셸에 맞춘다.
# 목적(용도): pip/학습이 C:에 쌓이지 않게 한다.
# 이 시점: 재현 점검 시작 전.

cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation

.\.venv\Scripts\Activate.ps1
# Activate.ps1: 프로젝트 .venv를 켠다.
# 목적(용도): requirements와 같은 패키지로 train/노트북을 돌린다.
# 이 시점: pip / python 직전.
```

* **확인:** 프롬프트에 `(.venv)` · 루트에 `requirements.txt`, `src/train.py`, `notebooks/notebook.ipynb`, `data/README.md`
* **→ 닫는 TODO:** 환경

#### Step 2. 데이터 접근 (T3)

CSV는 **git에 안 올라감** (`data/*.csv` gitignore). 대신 받는 법이 분명해야 한다.

1. `data/README.md`를 연다.
2. Option A(브라우저 ZIP) / B(Kaggle CLI) / C(공개 mirror URL) 중 하나로 `data/hotel_bookings.csv`를 **E: 프로젝트 `data/`** 에 둔다.
3. 이미 파일이 있으면 다시 받을 필요 없다.

```powershell
Test-Path .\data\hotel_bookings.csv
# Test-Path: 파일이 있으면 True.
# 목적(용도): train/노트북이 읽을 CSV가 있는지 확인.
# 이 시점: train 스모크 직전.
```

* **→ 닫는 TODO:** T3 데이터 안내

#### Step 3. README 재현 절 (T1·T2)

루트 `README.md`의 **How to run** 아래에 (또는 그 자리에) 다음이 **한눈에** 보이게 한다.

1. `use_e_drive` → cd → `.venv` Activate → `pip install -r requirements.txt`
2. 데이터: `data/README.md` 따라 CSV 배치
3. 시드: split `random_state=42`, XGBoost `seed=42` (`src/train.py`와 동일)
4. 학습: `python src/train.py` → `models/model.bin`
5. 노트북: `notebooks/notebook.ipynb` (EDA·모델 선정; 같은 시드)
6. (선택) API: `python src/predict.py` · Docker: 이미 있는 one-liner

* **주의:** `model.bin`도 보통 gitignore다. 피어는 CSV 받은 뒤 `train.py`로 다시 만들면 된다.
* **→ 닫는 TODO:** T1·T2 README

#### Step 4. train 스모크 (T4)

```powershell
python src/train.py
# train.py: CSV→전처리→XGB 학습→models/model.bin 저장.
# 목적(용도): 학습 스크립트가 오류 없이 끝까지 도는지 재현 증거.
# 이 시점: deps·CSV 준비 후.
```

* **확인:** `Model successfully saved to …\models\model.bin` 및 `train.py finished OK`
* Pandas `select_dtypes` **경고(Warning)** 만 뜨고 끝나면 OK (에러 아님).
* **5분 넘게 완전 정지**처럼 보이면 로그에 진행이 있는지 보고, 멈춤일 때만 중단·점검.
* (선택) 노트북은 Cursor/VS Code에서 `notebooks/notebook.ipynb`를 위에서 아래로 실행. Phase 1·2와 같은 셀·시드면 충분.

* **→ 닫는 TODO:** T4 train 스모크

#### Step 5. 체크포인트·점수 (T5)

증거가 생기면:

* `_planning/CHECKPOINTS.md` — (8/9) `done` + Evidence 날짜
* README Evaluation — Reproducibility **Score 1** + Evidence 한 줄
* `_planning/PHASE_LOG.md` — Phase 7 요약

클라우드 URL은 쓰지 말 것.

* **→ 닫는 TODO:** T5 점수

---

### 4. 확인 체크리스트

* [ ] README에 데이터·venv·train·시드 순서가 있다
* [ ] `data/README.md`로 CSV를 받을 수 있다 (커밋 강제 없음)
* [ ] `python src/train.py`가 오류 없이 끝난다
* [ ] Evaluation Reproducibility = 1 (Evidence 있음)
* [ ] 클라우드 없음 · E: only

### 5. 이해 확인

1. 왜 CSV를 git에 안 넣고도 Reproducibility 1점을 받을 수 있나?
2. `random_state=42`와 XGB `seed=42`는 각각 무엇을 같게 만드나?
3. 피어가 `model.bin` 없이 클론했다면 무엇을 먼저 돌려야 하나?

다음 지침은 허락 후 · 다음은 Cloud deployment **(9/9, 보너스)**
