# Phase 6 — Containerization (7/9)

### 목표

루트 `Dockerfile`을 실행 가능하게 채우고, `docker build` + `docker run -p 9696:9696`으로 Flask 예측 API(`src/predict.py`)를 컨테이너에서 기동한 뒤 HTTP 예측 1건을 확인한다.

### 산출물

- 동작하는 `Dockerfile` (python 베이스, requirements + src + model, EXPOSE 9696, CMD predict)
- 로컬에서 빌드·실행된 이미지/컨테이너
- (선택) README docker build/run one-liner

### 하지 말 것

- 클라우드 배포 **(9/9)** — 이 게이트와 합치지 않음
- train/predict 비즈니스 로직 전면 재작성
- C:`\Users\...`에 빌드 캐시·모델 복사
- Co-authored / Cursor / AI 커밋 트레일러

### 성공 기준

- [x] `docker build` 성공
- [x] `docker run -p 9696:9696 …` 후 API 기동
- [x] 호스트에서 HTTP `POST /predict` 1건 응답
- [x] 빌드 컨텍스트·안내는 E: 기준 (`use_e_drive` 문서화 가능)
- [x] 클라우드 URL/배포 없음
