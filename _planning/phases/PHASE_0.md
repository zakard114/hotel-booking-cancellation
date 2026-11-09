# Phase 0 — Problem & scaffold (1/7)

### 목표

미드텀 문제·데이터·폴더·학습 루프를 고정한다. **코드를 학습하지 않는다.** 전체 모델/API/Docker는 다음 페이즈.

### 이미 있는 것

- 루트: `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\`
- `README.md`, `AGENTS.md`, `.gitignore`, stubs (`src/`, `Dockerfile`, `data/README.md`)
- 이 파일 + `gemini_packets/phase_0_paste.md`

### 할 일

1. README의 문제 한 줄·금지 주제를 읽고 자기 말로 말할 수 있게 한다.
2. `data/README.md`로 CSV를 **어떻게** 받을지만 이해한다 (지금 꼭 받지 않아도 됨; 받으려면 E:만, 5분 초과 시 중단).
3. Gemini에 [`../gemini_packets/phase_0_paste.md`](../gemini_packets/phase_0_paste.md) 전문을 붙인다.
4. 받은 가이드를 Cursor에 가져와 **타당성 체크** → 최종 지침만 남긴다.

### 하지 말 것

- EDA 노트북 채우기, 모델 학습, Flask/Docker 구현
- car price / telco / credit / clothing으로 주제 변경
- C:에 venv·캐시·CSV
- 커밋 (사용자가 시키기 전)
- 다음 페이즈 패킷을 미리 실행용으로 쓰기

### 성공 기준

- [ ] 문제·타깃(`is_canceled`)·데이터 출처를 말로 설명 가능
- [ ] 배우며 만들기 루프(패킷→Gemini→타당성)를 이해
- [ ] Phase 0 가이드가 수정필 없이 채택됨
- [ ] `PHASE_LOG.md` Phase 0에 “가이드 채택” 기록

### Gemini 패킷

붙여넣기 파일: `_planning/gemini_packets/phase_0_paste.md`
