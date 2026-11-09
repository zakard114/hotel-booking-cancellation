# Phase 5 — Dependency and environment (6/9)

### 목표

실행에 필요한 패키지를 `requirements.txt`(또는 `pyproject.toml`)에 **버전 고정**하고, README에 E: + venv 설치·활성화 절차를 문서화한다.

### 산출물

- pin된 deps 파일
- README How to run의 deps 구간이 따라 할 수 있게 채워짐

### 하지 말 것

- Dockerfile 작성·`docker build` (그건 **7/9**)
- 클라우드 (9/9)
- C:에 pip/uv 캐시·venv

### 성공 기준

- [x] deps 파일에 train/predict에 쓰는 패키지 버전이 박혀 있음
- [x] README에 `use_e_drive` → venv → `pip install -r requirements.txt`(또는 동등) 절차
- [x] 같은 환경에서 `python src/predict.py` 기동이 문서와 맞음
