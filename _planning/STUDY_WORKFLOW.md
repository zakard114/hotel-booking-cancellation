# 학습 워크플로 — 배우면서 만들기

**목표:** AI가 대신 끝까지 짜 주는 게 아니라, **페이즈마다 이해하고 직접 실행**한다.

## 역할

| 역할 | 하는 일 |
|------|---------|
| **나** | Gemini에 패킷 붙여넣기, 실행·질문, 가이드를 Cursor에 가져오기, diff 승인 |
| **Gemini** | 패킷만으로 초보 한글 Why→What→How→확인 가이드 (앞서 뛰기 금지) |
| **Cursor** | 페이즈 패킷 초안, 막힘 조언, **수정필/수정불필** 타당성 체크, 허락된 적용만 |

## 루프 (한 페이즈)

```text
Cursor 패킷 → Gemini 붙여넣기 → 초보 가이드
→ 막히면 Cursor → Gemini에 보고·다듬기
→ Cursor 타당성 체크 (수정필 / 수정불필)
→ 깨끗할 때만 「최종 지침」으로 실행
→ PHASE_LOG 갱신 → 다음 페이즈는 허락 후
```

부트스트랩(FULL): `E:\IT_SPACES\AI\.agents\skills\project-start-apply-skills\SKILL.md`  
스킬: `E:\IT_SPACES\AI\.agents\skills\phase-gemini-beginner-guide\SKILL.md`  
범용 로드맵(+이 프로젝트 대입): [`ML_ROADMAP_PROTOCOL.md`](ML_ROADMAP_PROTOCOL.md) · 스킬 `ml-project-roadmap-protocol`

## 완료 게이트 (3개 YES)

1. 내가 명령/노트북 셀을 실행했고 결과를 봤다  
2. AI 없이 1분 안에 이 페이즈가 뭘 하는지 말할 수 있다  
3. `PHASE_LOG.md`에 결과가 있고 내가 읽었다  

## 체크포인트

게이트·공식 루브릭을 표로 체크하며 진행: [`CHECKPOINTS.md`](CHECKPOINTS.md)  
README 하단 Evaluation도 증거가 생길 때마다 Score를 올린다.

## 실행 매체 (속도)

- **기본:** VS Code / Cursor에서 `scripts/*.py` 실행·편집. Cursor와 즉각 수정·주석 티키타카에 유리.
- **노트북:** 제출 서사·셀 단위 기록이 필요할 때만. 띄우기 비용이 크면 생략하고 `.py` 결과를 PHASE_LOG에 남긴다.
- **패킷 규칙:** 각 Step/셀이 **어느 게이트 TODO·체크리스트 항목을 닫는지** 한 줄로 명시한다 (시점 ↔ TODO 매핑).

## 지금 할 일

1. Problem / **(1/9) 완료**.  
2. EDA / **(2/9) 완료** (`notebooks/notebook.ipynb` + `scripts/phase1_eda.py`).  
3. 다음: Model training / **(3/9)** — 요청 시 패킷. 작업은 VS Code `.py` 우선.  

