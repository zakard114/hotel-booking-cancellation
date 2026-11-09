# Phase 7 — Reproducibility (8/9)

### 목표

남(피어 리뷰어)이 레포만 보고 **데이터 받기 → 환경 → 노트북/`train.py` 재실행**까지 오류 없이 따라 할 수 있게 README·시드·데이터 안내를 최종 점검한다. 클라우드 배포는 하지 않는다.

### 루브릭 (공식, max 1)

- **0:** 노트북·학습 스크립트를 실행할 수 없거나, 데이터가 없거나 받기 어렵다
- **1:** 노트북과 `train.py`를 오류 없이 다시 돌릴 수 있고, 데이터가 커밋돼 있거나 **받는 법이 분명**하다

### 산출물

- README **Reproducibility / 재현** 절 (데이터·시드·명령 순서)
- (이미 있음) `data/README.md` 다운로드 안내, `requirements.txt` pin, `random_state`/`seed=42`
- Phase 7 Cursor 초보 가이드 + CHECKPOINTS/Evaluation Evidence

### 하지 말 것

- 클라우드 배포 **(9/9)**
- 새 모델·튜닝·API 로직 전면 재작성
- C:`\Users\...`에 데이터·venv·캐시
- Co-authored / Cursor / AI 커밋 트레일러
- CSV를 강제로 git에 넣으라고 강요 (gitignore 유지; 다운로드 안내로 1점 충족)

### 성공 기준

- [x] README에 데이터 → venv → train → (선택) predict/docker 순서가 있다
- [x] 시드(`random_state=42`, XGB `seed=42`)가 문서 또는 코드에 드러난다
- [x] `data/README.md`로 CSV를 받을 수 있다 (CSV는 gitignore)
- [x] `python src/train.py` 스모크 OK (또는 동등 증거)
- [x] Evaluation Reproducibility Score=1 + Evidence
- [x] 클라우드 URL/배포 없음
