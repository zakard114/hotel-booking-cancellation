# Phase 6 · Containerization (7/9) — 최종 실행 가이드

Cursor 작성 초보 나레이션. 재미나이 없이 이 문서만으로 실행한다.

### 1. Why

로컬에서 `python src/predict.py`로 돌리던 Flask 예측 API를 **Docker 이미지**로 묶어, 다른 PC에서도 `docker run`만으로 같은 서비스를 띄우게 하는 단계다. 클라우드 배포(9/9)는 하지 않는다.

### 2. What

* **T1:** E: + 프로젝트 루트 + Docker Desktop 확인
* **T2:** 루트 `Dockerfile`을 실행 가능하게 채움 (줄 아래 3단 주석 포함)
* **T3:** `docker build -t hotel-cancel .`
* **T4:** `docker run -p 9696:9696 hotel-cancel`
* **T5:** 호스트에서 `POST /predict` 1건
* **T6 (선택):** README에 docker 한 줄

---

### 3. How

#### Step 1. 환경 (T1)

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
# use_e_drive.ps1: E: 캐시·도구 경로를 이 셸에 맞춘다.
# 목적(용도): 빌드/설치가 C:에 쌓이지 않게 한다.
# 이 시점: docker 작업 시작 전.

cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
```

* Docker Desktop이 **실행 중**인지 확인 (트레이 아이콘).
* **주의:** 로컬에서 이미 `python src/predict.py`가 9696을 쓰고 있으면, 컨테이너 테스트 전에 그 터미널에서 `CTRL+C`로 끈다.

* **확인:** 프로젝트 루트에 `Dockerfile`, `requirements.txt`, `src/`, `models/model.bin`이 보인다.
* **→ 닫는 TODO:** T1 환경

#### Step 2. Dockerfile 채우기 (T2)

루트 `Dockerfile`을 **아래 내용으로 통째로 교체**한다.  
(학습용: 지시문 줄 **바로 아래** 3단 주석. 말미에 Names 목록 몰아쓰지 말 것.)

```dockerfile
FROM python:3.11-slim
# FROM: 컨테이너의 출발 베이스 이미지를 고른다.
# 목적(용도): Python 3.11이 들어 있는 얇은 이미지에서 서비스를 돌리기 위함.
# 이 시점: Dockerfile 첫 줄 — 이후 층이 이 이미지 위에 쌓인다.

WORKDIR /app
# WORKDIR: 컨테이너 안 작업 폴더를 /app 으로 정한다.
# 목적(용도): COPY·RUN·CMD가 같은 경로 기준으로 실행되게 한다.
# 이 시점: 베이스 직후, 파일을 넣기 전.

COPY requirements.txt .
# COPY requirements.txt: 호스트의 pin 목록을 이미지 /app 으로 복사한다.
# 목적(용도): 나중에 pip가 설치할 패키지 목록을 이미지에 넣기 위함.
# 이 시점: 코드/모델보다 먼저 — deps 층만 캐시되게 하려는 관례.

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install: 이미지 안에서 requirements의 패키지를 설치한다.
# 목적(용도): 컨테이너에 pandas/sklearn/xgboost/flask 환경을 만든다.
# 이 시점: requirements만 복사된 직후.

COPY src/ ./src/
# COPY src/: 예측 서비스 코드를 이미지에 넣는다.
# 목적(용도): 컨테이너에서 predict.py를 실행할 수 있게 한다.
# 이 시점: deps 설치 후.

COPY models/ ./models/
# COPY models/: model.bin 등 학습 아티팩트를 이미지에 넣는다.
# 목적(용도): predict.py가 /app/models/model.bin 을 로드하게 한다.
# 이 시점: src 복사와 같은 단계 — 런타임에 모델이 있어야 한다.

EXPOSE 9696
# EXPOSE: 컨테이너가 9696 포트를 쓴다고 문서화한다.
# 목적(용도): 실행 시 -p 매핑할 포트를 분명히 한다.
# 이 시점: 파일·deps가 준비된 뒤, 시작 명령 직전.

CMD ["python", "src/predict.py"]
# CMD: 컨테이너가 뜰 때 기본으로 실행할 명령이다.
# 목적(용도): Flask 예측 서버를 0.0.0.0:9696 에서 켠다.
# 이 시점: 이미지 정의의 마지막 — run 하면 이 명령이 돌아간다.
```

* stub의 `print('Dockerfile stub…')` CMD는 **삭제**한다.
* **→ 닫는 TODO:** T2 Dockerfile

#### Step 3. 이미지 빌드 (T3)

```powershell
docker build -t hotel-cancel .
# docker build: 현재 폴더(Dockerfile)로 이미지를 만든다.
# 목적(용도): deps·코드·모델을 한 이미지로 묶는다.
# 이 시점: Dockerfile을 채운 뒤 첫 빌드.
```

* `.` = 빌드 컨텍스트 = **지금 cd 한 E: 루트**.
* 첫 빌드는 pip 때문에 몇 분 걸릴 수 있다. **5분 넘게 멈춘 것처럼 보이면** 로그에 진행이 있는지 보고, 완전 정지 시에만 중단·점검.
* **확인:** `Successfully tagged hotel-cancel:latest` (또는 동등) 메시지.
* **→ 닫는 TODO:** T3 build

#### Step 4. 컨테이너 실행 (T4)

```powershell
docker run --rm -p 9696:9696 hotel-cancel
# docker run: 이미지로 컨테이너를 띄운다.
# 목적(용도): 호스트 9696 ↔ 컨테이너 9696 으로 API를 연다.
# 이 시점: 빌드 성공 후 서비스 기동.
```

* `--rm`: 종료 시 컨테이너 자동 삭제 (연습용).
* `-p 9696:9696`: 왼쪽=호스트, 오른쪽=컨테이너.
* 로그에 `Model and DictVectorizer loaded` / `Running on` 이 보이면 OK.
* 이 터미널은 서버처럼 **계속 떠 있는 상태**가 정상. 테스트는 **다른 터미널**에서.

* **→ 닫는 TODO:** T4 run

#### Step 5. HTTP 1건 (T5)

**새 PowerShell** (컨테이너는 그대로 둔 채):

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:9696/predict -Method POST -ContentType "application/json" -Body '{"hotel":"Resort Hotel","lead_time":100,"arrival_date_year":2017,"arrival_date_month":"July","arrival_date_week_number":27,"arrival_date_day_of_month":1,"stays_in_weekend_nights":2,"stays_in_week_nights":3,"adults":2,"children":0,"babies":0,"meal":"BB","country":"PRT","market_segment":"Online TA","distribution_channel":"TA/TO","is_repeated_guest":0,"previous_cancellations":0,"previous_bookings_not_canceled":0,"reserved_room_type":"A","assigned_room_type":"A","booking_changes":0,"deposit_type":"No Deposit","agent":"240","company":"missing","days_in_waiting_list":0,"customer_type":"Transient","adr":100.0,"required_car_parking_spaces":0,"total_of_special_requests":1}'
# Invoke-RestMethod: HTTP 요청을 보내고 응답을 객체로 받는다.
# 목적(용도): 컨테이너 API가 취소 확률 JSON을 주는지 확인한다.
# 이 시점: docker run 으로 서버가 떠 있는 동안.
```

* **확인:** `cancel_probability` / `is_canceled` 필드가 보인다.
* **→ 닫는 TODO:** T5 HTTP 1건

#### Step 6. (선택) README (T6)

README How to run 근처에 한 줄만 추가해도 된다:

```text
docker build -t hotel-cancel . ; docker run --rm -p 9696:9696 hotel-cancel
```

클라우드 URL은 쓰지 말 것.

* **→ 닫는 TODO:** T6 (선택)

---

### 4. 확인 체크리스트

* [ ] `docker build -t hotel-cancel .` 성공
* [ ] `docker run -p 9696:9696 hotel-cancel` 후 Flask 기동
* [ ] 호스트에서 `/predict` 1건 응답
* [ ] 클라우드 없음 · 빌드는 E: 루트
* [ ] Dockerfile에 지시문 **줄 아래** 3단 주석 (말미 목록 없음)

다음 지침은 허락 후
