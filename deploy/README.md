# Cloud deploy notes (bonus · 9/9)

에이전트 쪽 스캐폴드는 끝남. **클릭·계정·스모크는 학습자.**  
전체 클릭 경로: [`../_planning/gemini_packets/phase_8_final_guide.md`](../_planning/gemini_packets/phase_8_final_guide.md).

**게이트 doing.** `done` / Cloud Score는 학습자 명시 + Live 증거 후에만. 가짜 URL 금지.

## 전제 (에이전트 완료)

| 항목 | 값 |
|------|-----|
| GitHub | https://github.com/zakard114/hotel-booking-cancellation (`main`) |
| 모델 | `models/model.bin` **git 추적** (`!models/model.bin`) |
| PORT | `src/predict.py` → `os.environ.get("PORT", "9696")`, `debug=False`, `0.0.0.0` |
| Blueprint | 루트 `render.yaml` · Docker Free |

## 학습자 클릭 (요약)

1. https://render.com → GitHub로 가입/로그인 → https://dashboard.render.com  
2. **New +** → **Blueprint**  
3. Connect GitHub → 레포 **`zakard114/hotel-booking-cancellation`**  
4. `render.yaml` 확인 · 브랜치 **`main`** → **Apply**  
5. 값이 맞는지 확인: name `hotel-cancel-api`, oregon, docker, free, `./Dockerfile`, context `.`, health check **없음**  
6. **성공:** 초록 **Live** + 헤더 **`.onrender.com`** URL 복사  
7. Free 콜드 스타트 30–60초+ 가능  
8. PowerShell 스모크 (`YOUR-SERVICE`만 교체) — body는 `phase_8_final_guide.md`와 동일:

```powershell
$base = "https://YOUR-SERVICE.onrender.com"
Invoke-RestMethod -Method Post -Uri "$base/predict" `
  -ContentType "application/json" -Body $body
```

9. README에 실 URL + 절차. Evidence 뒤에만 Cloud Score **1**(문서) 또는 **2**(Live/시연).

## 실패 로그 힌트

| 증상 | 의미 |
|------|------|
| `COPY` / `models` / `No such file` | 원격에 모델 없음 |
| `FileNotFoundError` … `model.bin` | 기동 시 모델 경로 실패 |
| pip / dependency ERROR | `requirements.txt` 설치 실패 |
| Live인데 `/` 만 404 | `POST /predict`만 있음 |

## 대안 (수동)

**New +** → **Web Service** → Docker → Name `hotel-cancel-api`, Branch `main`, Dockerfile `./Dockerfile`, Context `.`, Free, Health check 비움 → **Create Web Service**.

## 제출 (선택)

- Repo: https://github.com/zakard114/hotel-booking-cancellation  
- **Commit ID**  
- Certificate name: **Heeju Yang**
