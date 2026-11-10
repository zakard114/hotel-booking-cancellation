# Phase 8 · Cloud — 학습자 클릭만

## 에이전트 완료 / 학습자만 할 일

| 구분 | 상태 |
|------|------|
| **에이전트 완료** | T1 `PORT`/`debug=False` · T2 `models/model.bin` git 추적 · `Dockerfile` · `render.yaml` · `deploy/README.md` · GitHub `main` push |
| **학습자만** | Render 가입/로그인 → Blueprint 클릭 배포 → Live URL 확인 → 스모크(T4) → README Evidence(T5) |
| **금지** | 가짜 Live URL · Cloud Score 임의 상향 · CHECKPOINTS 9/9 `done` (학습자 명시 전) |

**성공 기준:** 서비스 상태 **초록 Live** + 헤더 URL이 **`.onrender.com`**  
**레포:** `zakard114/hotel-booking-cancellation` · https://github.com/zakard114/hotel-booking-cancellation  
**게이트:** **done** (2026-11-10 · 학습자 「클라우드 끝」). Live https://hotel-cancel-api.onrender.com · Cloud Score **2/2**.

---

## 클릭 경로 (T3) — 번호만 따라가기

1. https://render.com → **Sign Up / Log in with GitHub**
2. https://dashboard.render.com 로그인 확인
3. **New +** → **Blueprint** (Web Service는 Blueprint가 막힐 때만)
4. **Connect GitHub** → 권한 허용  
   - 레포가 안 보이면 GitHub → Settings → Applications → Render → Repository access에서  
     `zakard114/hotel-booking-cancellation` 허용 후 새로고침
5. 레포 **`zakard114/hotel-booking-cancellation`** 선택
6. 루트 `render.yaml` 감지 확인 · 브랜치 **`main`** → **Apply**
7. 미리보기/설정이 아래와 같은지 확인:

| 항목 | 값 |
|------|-----|
| name | `hotel-cancel-api` |
| region | oregon |
| runtime | docker |
| plan | free |
| dockerfilePath | `./Dockerfile` |
| dockerContext | `.` |
| health check | **비움** |

8. 서비스 **`hotel-cancel-api`** → **Logs / Events**에서 빌드 대기
9. **본선 성공:** 상태 **Live** + 서비스 헤더의 `https://….onrender.com` URL 복사  
   - 예: `https://hotel-cancel-api.onrender.com` (접미사는 달라도 OK)  
   - Free 첫 요청은 30–60초+ 걸릴 수 있음 (콜드 스타트)

### Blueprint가 막힐 때만 (수동)

**New +** → **Web Service** → Docker → Name `hotel-cancel-api`, Branch `main`, Dockerfile `./Dockerfile`, Context `.`, Free, Health check 비움 → **Create Web Service**.

---

## 스모크 (T4) — Live URL 받은 뒤

PowerShell에서 `$base`만 본인 URL로 교체:

```powershell
$base = "https://YOUR-SERVICE.onrender.com"

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

Invoke-RestMethod -Method Post -Uri "$base/predict" `
  -ContentType "application/json" -Body $body
```

- **성공:** JSON에 `cancel_probability`, `is_canceled`
- **느림/타임아웃:** 60초 뒤 한 번 더
- **실패:** Render **Logs** 캡처 보관 (시연 Evidence)

`/` 만 치면 404가 정상 — 이 앱은 **`POST /predict`만** 있음.

---

## T5 (증거 생긴 뒤만)

1. 루트 `README.md` Cloud 절에 **실 Live URL** + 짧은 절차
2. `_planning/CHECKPOINTS.md` Evidence에 날짜·URL(또는 캡처 경로)
3. Evaluation Cloud Score: 문서만 **1** / Live·시연 **2** — 아직이면 **0**
4. 게이트 `done`은 「클라우드 끝 / 게이트 닫아」라고 한 뒤에만

---

## 실패 한 줄

| 증상 | 의미 |
|------|------|
| `COPY` / `models` / No such file | 원격에 `model.bin` 없음 |
| `FileNotFoundError` … `model.bin` | 기동 시 모델 경로 실패 |
| pip / dependency ERROR | `requirements.txt` 설치 실패 |
| Live인데 `/` 만 404 | `POST /predict`로 호출 |

---

## 제출 (선택, T6)

- Repo: https://github.com/zakard114/hotel-booking-cancellation  
- **Commit ID**  
- Certificate name: **Heeju Yang**
