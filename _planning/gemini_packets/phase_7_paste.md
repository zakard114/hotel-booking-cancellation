# (참고) Phase 7 · Reproducibility (8/9) — 패킷 요약

최근 페이즈는 **Cursor가 초보 가이드를 직접 작성**한다.  
실행용 본문: [`phase_7_final_guide.md`](phase_7_final_guide.md).  
재미나이 붙여넣기가 필요하면 아래를 쓴다.

---

역할: ML Zoomcamp 2026 미드텀 **Hotel Booking Cancellation** Phase 7(재현성) 튜터.  
초보 **한글** Why → What → How → 확인.  
작업 = README 재현 절 정리 + 시드/데이터 안내 점검 + `train.py`(및 노트북) 재실행 가능 여부 확인.  
**클라우드(9/9) 금지.**

## 규칙

- 게이트 **(8/9)** 고정. 경로·시드·파일명을 바꾸지 말 것.
- E: only. 설치·실행 전: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`
- CSV는 gitignore (`data/*.csv`). 커밋 강요 금지 — `data/README.md` 다운로드로 충족.
- 금지: 클라우드, 새 모델 튜닝, C: 캐시, Co-authored/Cursor 커밋 트레일러.
- 끝: 「다음 지침은 허락 후」

## 루브릭 (공식 max 1)

1점 = 노트북과 train 스크립트를 오류 없이 다시 돌릴 수 있고, 데이터가 있거나 받는 법이 분명하다.

## 이미 있는 것

- `data/README.md` · `requirements.txt` 5 pin · `src/train.py` (`random_state=42`, XGB `seed=42`)
- `notebooks/notebook.ipynb` · Docker (7/9 done)

## TODO

- T1: README에 재현 순서(데이터→venv→train→선택 predict/docker)
- T2: 시드 문서화
- T3: `python src/train.py` 스모크
- T4: Evaluation / CHECKPOINTS Evidence
