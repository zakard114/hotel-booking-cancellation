# Gemini에 그대로 붙여 넣기 — Phase 6 · Containerization (7/9)

역할: ML Zoomcamp 2026 미드텀 **Hotel Booking Cancellation** 의 Phase 6(컨테이너화) 튜터다.  
초보자용 **한글** Why → What → How → 확인. **작업 = 루트 `Dockerfile`을 실행 가능하게 채우고, `docker build` + `docker run`으로 Flask 예측 API를 컨테이너에서 기동한 뒤 HTTP 1건 확인**.  
클라우드 배포·재현성 전면 점검은 이번 게이트에서 하지 말 것.

## 규칙

- 이 글 사실만. 없는 이미지 태그·포트·경로·URL 날조 금지.
- Step마다 짧은 힌트·스켈레톤. 각 Step 끝 `→ 닫는 TODO: …`
- 게이트 **(7/9)** 고정.
- E: only. 빌드·설치·캐시 전: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`
- Docker Desktop이 이 PC에서 켜져 있어야 함. **빌드 컨텍스트는 E: 프로젝트 루트**를 쓴다. pip/Docker 캐시를 `C:\Users\...`에 두지 말 것(가능하면 E: / Docker Desktop 설정의 disk image 위치 유지).
- **금지:** 클라우드 배포(9/9), train/predict 비즈니스 로직 전면 재작성, 새 모델 학습, git 커밋에 `Co-authored-by` / Cursor / AI 트레일러.
- 끝: 질문 2~3개 + 「다음 지침은 허락 후」

## ⚠️ 필수 — beginner-lesson-comments 스타일 주석 (How 스켈레톤에 반드시 포함)

가이드의 **How**에 들어가는 Dockerfile 스켈레톤과 `docker build` / `docker run` 등 핵심 셸 명령에는, 아래 규칙을 **반드시** 지켜 주석을 달아라. (학습자가 그대로 따라 쓰게 하기 위함)

### 배치 (위치)

- 주석은 설명하는 **그 코드/명령 줄 바로 아래**(선호) 또는 같은 줄 옆. **코드와 인터리브**.
- **NEVER** 주석을 줄 **위**에만 두기.
- **NEVER** Dockerfile/명령 블록 **맨 끝**에 Names / 역할 / 목적 / 이 시점 목록을 몰아쓰기.
- 셀·파일 끝 “이름 목록 덤프” = **실패**. 처음부터 줄 아래로 다시 쓸 것.

### 형식 (새·혼란 API / 중요 지시문 첫 등장)

각 대상 줄 아래에 **3줄**:

```text
# 무엇: (이름 + 한 줄 정의)
# 목적(용도): 왜 쓰는지
# 이 시점: 지금 흐름에서 하는 역할
```

### 어디에 달 것인가 (이번 페이즈 포커스)

- **Dockerfile 지시문** 특히: `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD` (및 실제로 쓰는 `ENV` 등)
- **핵심 셸**: `docker build`, `docker run` (포트 매핑 `-p 9696:9696` 포함), HTTP 테스트 명령(`Invoke-RestMethod` 또는 `curl`)
- 메서드/함수 호출이 How에 나오면 같은 규칙 (줄 아래 3단)

### 어디에 달지 말 것인가

- 모든 사소한 줄에 3단 주석을 남발하지 말 것
- `for` / `if` 등 제어문 줄은 기본 스킵
- 같은 지시문이 반복되면 **첫 등장**만 자세히

### How 예시 형태 (RIGHT — 이 패턴으로 Dockerfile·run 명령을 쓸 것)

```dockerfile
FROM python:3.11-slim
# FROM: 컨테이너의 출발 베이스 이미지를 고른다.
# 목적(용도): Python이 이미 들어 있는 얇은 이미지에서 서비스를 돌리기 위함.
# 이 시점: Dockerfile의 첫 줄 — 이후 모든 층이 이 이미지 위에 쌓인다.

WORKDIR /app
# WORKDIR: 컨테이너 안 작업 폴더를 /app 으로 정한다.
# 목적(용도): COPY·RUN·CMD가 같은 경로 기준으로 실행되게 한다.
# 이 시점: 베이스 이미지 직후, 파일을 넣기 전.
```

```text
docker build -t hotel-cancel .
# docker build: Dockerfile로 이미지를 만든다.
# 목적(용도): 의존성·코드·모델을 한 이미지에 묶어 어디서든 같게 돌리기 위함.
# 이 시점: Dockerfile을 채운 뒤, 처음으로 이미지를 만드는 단계.
```

**WRONG (절대 금지):** 지시문만 쭉 나열한 뒤 파일 맨 아래에 `# Names: FROM, WORKDIR…` / `# 역할:` / `# 이 시점:` 목록.

## 루브릭·게이트

- **공식:** Containerization (**max 2**)
- **게이트:** **(7/9)** — `docker build` + `docker run`으로 API 기동, HTTP로 예측 1건 응답
- **이전:** Dependency and environment **(6/9) = done** (`requirements.txt` 5 pin, README How to run, 로컬 `predict.py` :9696 OK)
- **열지 말 것:** Reproducibility **(8/9)** 전면 재현 감사, Cloud **(9/9)**

## 경로

| 무엇 | 경로 |
|------|------|
| 루트 (빌드 컨텍스트) | `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\` |
| Dockerfile (지금 stub) | `Dockerfile` |
| deps (이미 pin됨) | `requirements.txt` |
| 예측 서비스 | `src\predict.py` — Flask, `host=0.0.0.0`, **port 9696**, `POST /predict` |
| 모델 아티팩트 | `models\model.bin` |
| E: 헬퍼 | `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1` |

## 이미 있는 사실 (날조 금지)

- `requirements.txt`: `pandas==3.0.5`, `numpy==2.4.6`, `scikit-learn==1.9.0`, `xgboost==3.2.0`, `flask==3.1.3`
- `predict.py`는 프로젝트 루트 기준 `models/model.bin`을 로드한다 → 컨테이너에서도 **WORKDIR=/app** 이고 `models/`·`src/`가 그 아래에 있어야 함
- Dockerfile stub에 `FROM python:3.11-slim`, `WORKDIR /app`, 주석 처리된 COPY/RUN/EXPOSE/CMD 예시가 있음. stub의 `CMD print('Dockerfile stub…')` 는 이번 페이즈에서 **실제 predict CMD로 교체**

## TODO (닫을 것)

- [ ] T1 `use_e_drive` + 프로젝트 루트 `cd` + Docker Desktop 준비 확인
- [ ] T2 `Dockerfile` 채우기: python 베이스 → `WORKDIR` → `COPY requirements.txt` → `RUN pip install` → `COPY src/` + `COPY models/` → `EXPOSE 9696` → `CMD`로 `python src/predict.py` (또는 동등)
- [ ] T3 `docker build -t <이미지이름> .` (컨텍스트 = E: 루트)
- [ ] T4 `docker run -p 9696:9696 <이미지이름>` 으로 API 기동
- [ ] T5 호스트에서 HTTP **1건** (`POST /predict`) — 예: PowerShell `Invoke-RestMethod` 또는 `curl`
- [ ] T6 (선택) README에 docker build/run 한 줄 요약 — 필수는 아님. 클라우드 URL은 쓰지 말 것

## 순서

1. use_e_drive + cd 루트 + Docker Desktop → **환경 (T1)**
2. Dockerfile stub → 실행 가능 지시문으로 채움 (주석은 줄 **아래** 3단) → **T2**
3. `docker build` → **T3**
4. `docker run -p 9696:9696` → **T4**
5. HTTP 예측 1건 → **T5**
6. (선택) README docker one-liner → **T6**

## 하지 말 것

- AWS/GCP/Azure/Render 등 **클라우드 배포** (그건 9/9)
- `train.py` / `predict.py` 예측·전처리 로직 대규모 재작성 (경로/호스트가 이미 `0.0.0.0`이면 Docker용으로 충분)
- C:`\Users\...`에 빌드 캐시·venv·모델 복사본을 새로 만들기
- Co-authored / Cursor / AI 커밋 트레일러
- (8/9) 재현성 전면 리라이트와 이 게이트를 한 번에 섞기

## 성공 체크리스트

- [ ] `docker build` 성공 (이미지 생성)
- [ ] `docker run -p 9696:9696 …` 후 컨테이너에서 Flask 기동
- [ ] 호스트 → `http://localhost:9696/predict` (또는 동등)로 **1건** JSON 예측 응답
- [ ] 빌드 컨텍스트·문서가 E: 기준; 클라우드 없음
- [ ] How 가이드의 Dockerfile·핵심 docker 명령에 **줄 아래** 무엇/목적/이 시점 주석이 있음 (말미 목록 없음)

## 출력 형식

각 Step:

1. **Why** — 왜 이 단계인지  
2. **What** — 무엇을 만드는지  
3. **How** — 클릭·명령·Dockerfile 스켈레톤 (**위 주석 규칙 적용**)  
4. **확인** — 학습자가 스스로 확인할 질문  
5. 끝줄: `→ 닫는 TODO: T…`

문서 끝: 질문 2~3개 + **「다음 지침은 허락 후」**
