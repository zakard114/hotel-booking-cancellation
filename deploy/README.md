# Cloud deploy notes (bonus · 9/9)

스캐폴드만. **실제 Live URL은 배포 성공 후에** 루트 README Evaluation / Cloud 절에 적는다.  
가짜 URL·미리 Score 올리기 금지. 실행 가이드: [`../_planning/gemini_packets/phase_8_final_guide.md`](../_planning/gemini_packets/phase_8_final_guide.md).

## 권장: Render + 기존 Dockerfile

1. GitHub에 이 레포 push. `models/model.bin`은 Render Docker `COPY`용으로 **의도적으로 추적**한다 (다른 `models/*.bin`은 무시).
2. [Render](https://render.com) → New → Blueprint → 루트 `render.yaml` 적용  
   또는 New → Web Service → Docker → Dockerfile `./Dockerfile`.
3. 빌드·기동 로그에서 모델 로드 확인.
4. Public URL로 `POST /predict` (JSON 본문은 로컬 Docker 때와 동일).
5. README에 URL + 짧은 절차. Evidence 생긴 뒤에만 Cloud Score 1 또는 2.

## 포트

클라우드 호스트는 보통 `PORT` 환경변수를 준다. `src/predict.py`가 이를 읽도록 Phase 8 가이드 T1을 따른다.

## 대안

Fly.io / Railway / AWS / 로컬 Kubernetes(kind)도 루브릭상 가능. 문서에 **코드와 함께** 단계를 남기면 1점, URL·시연까지 있으면 2점.

## 제출 (선택)

- Repo URL + **Commit ID**
- Certificate name: **Heeju Yang**
