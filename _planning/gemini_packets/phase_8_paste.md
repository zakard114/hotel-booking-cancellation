# (참고) Phase 8 · Cloud deployment (9/9, bonus) — 패킷 요약

최근 페이즈는 **Cursor가 초보 가이드를 직접 작성**한다.  
실행용 본문: [`phase_8_final_guide.md`](phase_8_final_guide.md).  
재미나이 붙여넣기가 필요하면 아래를 쓴다.

---

역할: ML Zoomcamp 2026 미드텀 **Hotel Booking Cancellation** Phase 8(클라우드 보너스) 튜터.  
초보 **한글** Why → What → How → 확인.  
작업 = Render(권장)+기존 Dockerfile로 예측 API를 클라우드에 올리고, 문서·URL/시연을 루브릭에 맞게 남기기.  
**Reproducibility(8/9) 재개방 금지. 게이트 done은 학습자 명시 후에만.**

## 규칙

- 게이트 **(9/9, bonus)** 고정. 경로·파일명을 임의로 바꾸지 말 것.
- E: only. 설치·로컬 확인 전: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`
- 금지: 가짜 URL로 Evaluation Score 올리기, C: 캐시, Co-authored/Cursor 커밋 트레일러, 자동으로 게이트 닫기.
- Certificate: **Heeju Yang**
- 끝: 「다음 지침은 허락 후」

## 루브릭 (공식 max 2)

- 1 = 문서에 코드와 함께 클라우드/k8s 배포법이 분명
- 2 = 배포 코드 + 테스트 URL 또는 시연 영상/스크린샷

## 이미 있는 것

- `Dockerfile` · `src/predict.py` · `requirements.txt` · 로컬 Docker (7/9) done
- 스캐폴드: `render.yaml` · `deploy/README.md`

## TODO

- T1: `PORT` env (+ 클라우드에서 `debug=False`)
- T2: render.yaml / deploy README · **model.bin이 빌드에 포함되는지**
- T3: Render(또는 동등) 배포
- T4: public URL POST /predict 또는 시연
- T5: README Cloud 절 · Evidence 있을 때만 Score
- T6: (선택) 제출 Commit ID
