# Phase 5 · Dependency and environment (6/9) — 최종 지침

타당성 수정필 반영본. 이 문서만 실행용으로 쓴다.

### 1. Why (왜 이 단계인가요?)

`src/predict.py` / `src/train.py`가 이 PC에서는 돌아가도, 다른 환경에서는 패키지 버전·누락으로 깨질 수 있습니다. 실제로 도는 버전을 `requirements.txt`에 `package==version`으로 고정하고, README에 설치 절차를 남깁니다. Docker·클라우드는 이번 게이트에서 하지 않습니다.

### 2. What (무엇을 해야 하나요?)

* **Step 1:** E: + 프로젝트 `.venv` 활성화
* **Step 2 (T1):** 필수 패키지 실제 버전 확인
* **Step 3 (T2):** `requirements.txt`에 확인한 버전 pin
* **Step 4 (T3):** README How to run에 설치 절차 채우기
* **Step 5 (T4):** import/기동 스모크 (포트 충돌 주의)
* **Step 6 (T5):** stub 정리 · Docker는 손대지 않음

### 3. How

#### Step 1. 환경 준비 (**VS Code 터미널**)

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
# use_e_drive.ps1: E: 쪽 캐시·도구 경로를 이 셸에 맞춥니다.
# 목적(용도): pip/설치가 C:에 쌓이지 않게 하기 위함입니다.
# 이 시점: 패키지 조회·설치 전에 한 번 켭니다.

cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation

.\.venv\Scripts\Activate.ps1
# Activate.ps1: 이 프로젝트 가상환경을 현재 터미널에 연결합니다.
# 목적(용도): 시스템 Python이 아니라 .venv 안의 패키지를 쓰게 합니다.
# 이 시점: pip show / pip install / predict 실행 직전입니다.
```

* **확인:** 프롬프트에 `(.venv)` 표시
* **→ 닫는 TODO:** 환경

#### Step 2. 설치된 버전 확인 (T1)

```powershell
python -c "import importlib.metadata as m; pkgs=['pandas','numpy','scikit-learn','xgboost','flask'];
[print(p, m.version(p)) for p in pkgs]"
# importlib.metadata.version: 설치된 배포판의 버전 문자열을 읽습니다.
# 목적(용도): requirements에 추측이 아닌 실제 버전을 적기 위함입니다.
# 이 시점: pin 파일을 쓰기 직전입니다.
```

(`pip show pandas numpy scikit-learn xgboost flask`도 가능. 오래 걸리면 위 `python -c` 사용.)

이 PC에서 확인된 값(그대로 pin에 사용):

```text
pandas==3.0.5
numpy==2.4.6
scikit-learn==1.9.0
xgboost==3.2.0
flask==3.1.3
```

* **→ 닫는 TODO:** T1 패키지 버전 확인

#### Step 3. `requirements.txt` pin (T2)

파일 역할: train/predict에 필요한 패키지 버전을 한곳에 고정하는 목록.

`requirements.txt` 내용을 아래로 교체 (가짜 예시 버전 쓰지 말 것):

```text
pandas==3.0.5
numpy==2.4.6
scikit-learn==1.9.0
xgboost==3.2.0
flask==3.1.3
```

* **→ 닫는 TODO:** T2 requirements.txt pin

#### Step 4. README How to run (T3)

README How to run에 **아래 블록만** 넣습니다(명령만, 주석 넣지 않음).

````markdown
```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/predict.py
```
````

가이드용(README에 넣지 말 것):

```text
# pip install -r requirements.txt: 목록에 적힌 패키지·버전을 설치합니다.
# 목적(용도): 문서와 같은 의존성으로 환경을 맞춥니다.
# 이 시점: venv 활성화 직후, 서버 기동 전.
```

* **→ 닫는 TODO:** T3 README How to run deps 채움

#### Step 5. 스모크 (T4)

```powershell
python src/predict.py
# python src/predict.py: 예측 HTTP 서비스를 켭니다.
# 목적(용도): pin 환경에서 import 에러 없이 기동되는지 봅니다.
# 이 시점: requirements·README 정리 후 검증.
```

* 9696에 서버가 **이미** 떠 있으면: 그 터미널에서 `CTRL+C` 후 재기동하거나, 서버 대신 import 스모크만 합니다.

```powershell
python -c "import pandas, numpy, sklearn, xgboost, flask; print('imports ok')"
# import …: 필수 패키지를 메모리에 올립니다.
# 목적(용도): 포트 충돌 없이 의존성만 빠르게 확인합니다.
# 이 시점: 서버가 이미 떠 있거나 기동을 생략할 때.
```

* **→ 닫는 TODO:** T4 스모크

#### Step 6. Stub·범위 점검 (T5)

* `requirements.txt` 옛 주석 stub 제거·정리
* `Dockerfile`은 **만들지/고치지 않음** (7/9)
* `pyproject.toml`은 비워 두거나, README에 「설치 진실 = `requirements.txt`」 한 줄만 명시

* **→ 닫는 TODO:** T5 stub·문서 점검

### 4. 확인

* [x] `requirements.txt`에 위 5개 `==version` pin
* [x] README에 `use_e_drive` → cd → venv → `pip install -r requirements.txt` 복붙 가능
* [x] Dockerfile 미변경으로 (6/9)만 닫음

다음 지침은 허락 후
