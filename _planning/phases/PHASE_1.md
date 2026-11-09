# Phase 1 — Data & EDA (2/9)

### 목표

`hotel_bookings.csv`를 E: `data/`에 두고, 노트북에서 결측·타깃 분포·피처 초안·누수 주의·시드 고정 split까지. **모델 학습은 (3/9).**

### 이미 있는 것

- 루트: `E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation\`
- `data/README.md`, `notebooks/notebook.ipynb` (Phase 1 TODO)
- 패킷: [`../gemini_packets/phase_1_paste.md`](../gemini_packets/phase_1_paste.md)

### 할 일

1. `use_e_drive` 후 `data/README.md`대로 CSV 확보 (로그인/5분 초과 시 브라우저만).
2. 노트북: 로드 · 결측 · `is_canceled` 분포 · 관계 · 누수 후보 · 피처 초안 · seeded split.
3. Gemini에 `phase_1_paste.md` 전문 → 가이드를 Cursor에 가져와 수정필/수정불필.

### 하지 말 것

다중 모델 학습·튜닝, `train.py`/API/Docker, C: 저장, 커밋(시킬 때까지).

### 성공 기준

- [ ] CSV E: 로드
- [ ] 타깃·결측·피처/누수 메모
- [ ] train/val/test 시드·비율 고정
- [ ] 가이드 타당성 통과 후 실행

### Gemini 패킷

`_planning/gemini_packets/phase_1_paste.md`
