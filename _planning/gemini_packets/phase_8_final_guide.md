# Phase 8 · Cloud deployment (9/9, bonus) — 최종 실행 가이드

Cursor 작성 초보 나레이션. 재미나이 없이 이 문서만으로 실행한다.  
**이 게이트는 보너스(마지막 midterm 빌드 게이트).** 필수가 아니며, 닫기는 학습자가 명시할 때만.

### 1. Why

로컬 `docker run`으로 돌리던 취소 예측 API를 **인터넷에서 호출 가능한 주소**로 올리면, 피어가 내 PC 없이도 서비스를 볼 수 있다.  
공식 루브릭 **Cloud deployment (max 2, bonus)**:

| 점수 | 의미 |
|------|------|
| 0 | 클라우드 없음 |
| 1 | 문서에 **코드와 함께** 클라우드/k8s 배포법이 분명 |
| 2 | 배포용 코드 + **테스트 URL** 또는 **시연 영상/스크린샷** |

없어도 본전(현재 subtotal 13/16). Peer reviews는 제출 **후** 별도.

### 2. What

* **T1:** `predict.py`가 클라우드 `PORT` 환경변수를 읽게 한다 (없으면 9696)
* **T2:** `render.yaml` + `deploy/README.md` 확인·다듬기 (스캐폴드 있음)
* **T3:** Render(권장) 계정 → GitHub 연결 → Docker 서비스 배포
* **T4:** 공개 URL로 `POST /predict` 1건 (또는 실패 시 스크린샷/영상 증거)
* **T5:** README에 **Cloud** 절 + Evaluation Evidence (실 URL/시연이 생긴 뒤만 Score)
* **T6 (선택):** 코스 제출 폼 — repo URL + **Commit ID** · 이름 **Heeju Yang**
* **하지 말 것:** 8/9 재개방, 가짜 URL로 Score 올리기, C: 설치, Co-authored 커밋, 에이전트만으로 배포 완료·게이트 닫기

**기본 경로(이 PC):** `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\`  
**이미 있는 것:** `Dockerfile`, `src/predict.py`(host `0.0.0.0`), `models/model.bin`(로컬), deps pin, Docker (7/9) done

---

### 3. How

#### Step 0. 계정·전제 (막히면 여기서 멈춤 OK)

1. **GitHub**에 이 프로젝트가 원격으로 올라가 있어야 Render가 Dockerfile을 빌드한다. 없으면 먼저 push(커밋은 본인이 할 때만; AI trailer 금지).
2. [Render](https://render.com) 무료 계정 가입 (GitHub 로그인 권장).
3. Docker Desktop은 **로컬 재확인용**이지, 클라우드 빌드는 Render가 한다.

다른 플랫폼(Fly.io, Railway, AWS, 로컬 kind/k8s)도 루브릭상 가능. 이 가이드는 **Render + 기존 Dockerfile** 기준이다.

* **→ 닫는 TODO:** 계정·원격 준비

#### Step 1. PORT 환경변수 (T1)

Render는 컨테이너에 `PORT`를 넣는다. 지금 `predict.py`는 `9696` 고정이라 클라우드에서 포트가 안 맞을 수 있다.

`src/predict.py` 맨 아래 `if __name__ == "__main__":` 근처를 대략 이렇게 바꾼다:

```python
import os
# … 파일 상단 import들과 함께 두어도 됨

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9696"))
    # os.environ.get("PORT", "9696"): 클라우드가 준 포트가 있으면 쓰고, 없으면 로컬 9696.
    # 목적(용도): Render 등 호스트가 지정한 포트에서 Flask가 듣게 한다.
    # 이 시점: 서버를 켜기 직전.
    app.run(debug=False, host="0.0.0.0", port=port)
    # debug=False: 클라우드에서는 디버그 모드를 끈다.
```

로컬 확인:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
.\.venv\Scripts\Activate.ps1
python src\predict.py
```

* **확인:** 예전처럼 `:9696`에서 기동. (선택) `$env:PORT=9700; python src\predict.py` 후 9700으로 뜨는지.
* **→ 닫는 TODO:** T1 PORT

#### Step 2. 배포 설정 파일 확인 (T2)

루트에 이미 스캐폴드가 있다.

* `render.yaml` — Render Blueprint (Docker 웹 서비스)
* `deploy/README.md` — 클릭·연결 순서 메모

내용을 읽고, 서비스 이름·리전이 마음에 들면 그대로 둔다.  
**주의:** `models/model.bin`이 gitignore면 Render 빌드 컨텍스트에 모델이 없다 → 이미지에 모델이 빠져 기동 실패한다.

선택지 (하나만):

1. **권장 학습 경로:** 배포 전에 `models/model.bin`을 원격에 포함하거나, CI/릴리스에서 복사되도록 README에 명시 (용량·라이선스 스스로 판단).
2. 또는 Render **Docker** 배포 시, 로컬에서 `docker build`가 쓰는 것과 같이 **Git에 모델이 커밋된 브랜치**로 배포.
3. 모델 없이 올리면 `/predict` 전에 프로세스 크래시 → 그 화면 캡처만으로는 만점 어렵고, 문서(1점)만 노릴 수 있다.

`Dockerfile`은 이미 `COPY models/ ./models/` 이다. 원격 트리에 `models/model.bin`이 있는지 먼저 확인:

```powershell
git check-ignore -v models/model.bin
# 무시되면 배포 전에 전략(커밋 예외 / 다른 아티팩트 경로)을 정한다.
```

* **→ 닫는 TODO:** T2 설정·모델 전략

#### Step 3. Render에서 배포 (T3)

브라우저에서 (클릭 단위):

1. Render Dashboard → **New** → **Blueprint** (또는 Web Service).
2. 이 midterm GitHub repo 연결.
3. Blueprint면 루트 `render.yaml` 감지 → Apply.  
   Web Service 수동이면: **Environment = Docker**, Dockerfile path = `./Dockerfile`, Instance = Free.
4. 빌드 로그에서 `pip install` · `Model … loaded` 류 메시지 확인.
5. 서비스가 **Live**가 되면 공개 URL이 생긴다. 예: `https://hotel-cancel-xxxx.onrender.com`

무료 티어는 **콜드 스타트**로 첫 요청이 30–60초 걸릴 수 있다. 5분 넘게 빌드만 돌고 진행 로그가 없으면 중단·로그 점검.

Fly.io를 쓸 경우: `fly launch` / `fly.toml` 경로로 바꾸되, 같은 PORT·Dockerfile 원칙을 따른다.

* **→ 닫는 TODO:** T3 배포 시도

#### Step 4. URL 스모크 (T4)

PowerShell 예시 (URL은 본인 것으로 교체):

```powershell
$body = @{
  hotel = "City Hotel"
  lead_time = 50
  arrival_date_year = 2017
  arrival_date_month = "July"
  arrival_date_week_number = 27
  arrival_date_day_of_month = 1
  stays_in_weekend_nights = 1
  stays_in_week_nights = 2
  adults = 2
  children = 0
  babies = 0
  meal = "BB"
  country = "PRT"
  market_segment = "Online TA"
  distribution_channel = "TA/TO"
  is_repeated_guest = 0
  previous_cancellations = 0
  previous_bookings_not_canceled = 0
  reserved_room_type = "A"
  assigned_room_type = "A"
  booking_changes = 0
  deposit_type = "No Deposit"
  agent = "9"
  company = "missing"
  days_in_waiting_list = 0
  customer_type = "Transient"
  adr = 100.0
  required_car_parking_spaces = 0
  total_of_special_requests = 1
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "https://YOUR-SERVICE.onrender.com/predict" `
  -ContentType "application/json" -Body $body
```

* **확인:** JSON에 `cancel_probability`, `is_canceled`  
* 안 되면: Render 로그 스크린샷 또는 짧은 화면 녹화 → 루브릭 2점의 “video/screenshot of testing” 후보.
* 로컬 피처 키가 부족하면 422/500 가능 — 로컬 Docker에서 쓰던 **동일 JSON**을 재사용하는 것이 안전하다 (`_planning` Phase 6 가이드·본인 메모의 성공 페이로드).

* **→ 닫는 TODO:** T4 스모크/시연

#### Step 5. README·점수 (T5) — **증거가 생긴 뒤에만**

1. 루트 `README.md`에 **Cloud deployment** 짧은 절:
   - 플랫폼 (Render)
   - `render.yaml` / Docker
   - (실주소) public URL
   - 예시 `POST /predict`
2. `_planning/CHECKPOINTS.md` (9/9) Evidence 날짜
3. README Evaluation Cloud **Score**  
   - 문서만 → 1  
   - 코드+URL 또는 시연 → 2  
   - **아직이면 Score 0 유지** (지금 기본)

게이트를 `done`으로 바꾸는 것은 **학습자가 「클라우드 끝/게이트 닫아」라고 한 뒤**에만.

* **→ 닫는 TODO:** T5 문서·점수(증거 후)

#### Step 6. 제출 준비 (T6, 선택)

코스 midterm 제출 창에 대략:

* GitHub repo URL  
* **Commit ID** (배포·문서가 들어간 커밋 해시)  
* Certificate name: **Heeju Yang**

Peer review 3건은 제출 **이후** (이 페이즈 밖).

---

### 4. 확인 체크리스트

* [ ] `PORT` 환경변수 반영 (`debug=False` 권장)
* [ ] `render.yaml` / `deploy/README.md`로 배포 절차가 설명된다
* [ ] (만점) Live URL 또는 시연 파일/스크린샷
* [ ] Evaluation Cloud Score는 증거에만 맞춤 (가짜 URL 금지)
* [ ] (8/9) Reproducibility는 그대로 done
* [ ] E: only · Co-authored 커밋 없음

### 5. 이해 확인

1. Cloud 1점과 2점의 차이는 무엇인가?
2. 왜 Render에서 `PORT`를 읽어야 하나?
3. `model.bin`이 gitignore인데 Dockerfile이 `COPY models/` 하면 클라우드 빌드에서 무엇이 깨지나?

다음 지침은 허락 후.  
이 게이트를 닫으면 midterm **빌드 게이트는 끝** → 제출·Peer reviews(별도).
