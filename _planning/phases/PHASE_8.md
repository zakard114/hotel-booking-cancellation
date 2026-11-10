# Phase 8 — Cloud deployment (9/9, bonus)

### 목표

로컬 Docker로 이미 돌아가는 Flask 예측 API를 **클라우드(또는 k8s)** 에 올리고, 공식 루브릭에 맞는 **배포 문서 + (가능하면) 테스트 URL/시연**을 남긴다.  
본 게이트는 **보너스**다. 필수 (1)–(8)은 이미 닫혔다.

### 루브릭 (공식, max 2)

- **0:** 클라우드 배포 없음
- **1:** README(또는 deploy 문서)에 **코드와 함께** 클라우드/k8s에 올리는 법이 분명하다
- **2:** 배포용 코드(IaC/설정)가 있고, **테스트용 URL** 또는 **시연 영상/스크린샷**이 있다

### 산출물 (목표)

- `render.yaml`(또는 Fly/다른 동등 설정) + `deploy/README.md` 배포 절
- (학습자 실행) 실제 배포 후 public URL 또는 시연 증거
- README Evaluation Cloud Evidence (URL/시연이 생긴 뒤에만 Score 올림)
- (선택) 제출 폼: repo URL + Commit ID · Certificate **Heeju Yang**

### 하지 말 것

- Reproducibility **(8/9)** 재개방·재채점
- 가짜/미배포 URL을 Evaluation에 넣고 Score를 미리 올리기
- train/predict 비즈니스 로직 전면 재작성·새 모델 튜닝
- C:`\Users\...`에 빌드 캐시·이미지·시크릿
- Co-authored / Cursor / AI 커밋 트레일러
- 커밋은 학습자가 시킬 때만

### 성공 기준 (닫을 때)

- [x] 배포 문서에 단계·설정 파일이 있다 (→ 최소 1점 가능)
- [x] (만점) 배포 코드 + 공개 URL 또는 시연 증거 — https://hotel-cancel-api.onrender.com
- [x] CHECKPOINTS (9/9) `done` + Evaluation Cloud Score **2/2** (사용자 「클라우드 끝」, 2026-11-10)
- [x] 8/9 Reproducibility는 **done 유지**
