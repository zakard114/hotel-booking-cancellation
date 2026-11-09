FROM python:3.11-slim
# FROM: 컨테이너의 출발 베이스 이미지를 고른다.
# 목적(용도): Python 3.11이 들어 있는 얇은 이미지에서 서비스를 돌리기 위함.
# 이 시점: Dockerfile 첫 줄 — 이후 층이 이 이미지 위에 쌓인다.

WORKDIR /app
# WORKDIR: 컨테이너 안 작업 폴더를 /app 으로 정한다.
# 목적(용도): COPY·RUN·CMD가 같은 경로 기준으로 실행되게 한다.
# 이 시점: 베이스 직후, 파일을 넣기 전.

COPY requirements.txt .
# COPY requirements.txt: 호스트의 pin 목록을 이미지 /app 으로 복사한다.
# 목적(용도): 나중에 pip가 설치할 패키지 목록을 이미지에 넣기 위함.
# 이 시점: 코드/모델보다 먼저 — deps 층만 캐시되게 하려는 관례.

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install: 이미지 안에서 requirements의 패키지를 설치한다.
# 목적(용도): 컨테이너에 pandas/sklearn/xgboost/flask 환경을 만든다.
# 이 시점: requirements만 복사된 직후.

COPY src/ ./src/
# COPY src/: 예측 서비스 코드를 이미지에 넣는다.
# 목적(용도): 컨테이너에서 predict.py를 실행할 수 있게 한다.
# 이 시점: deps 설치 후.

COPY models/ ./models/
# COPY models/: model.bin 등 학습 아티팩트를 이미지에 넣는다.
# 목적(용도): predict.py가 /app/models/model.bin 을 로드하게 한다.
# 이 시점: src 복사와 같은 단계 — 런타임에 모델이 있어야 한다.

EXPOSE 9696
# EXPOSE: 컨테이너가 9696 포트를 쓴다고 문서화한다.
# 목적(용도): 실행 시 -p 매핑할 포트를 분명히 한다.
# 이 시점: 파일·deps가 준비된 뒤, 시작 명령 직전.

CMD ["python", "src/predict.py"]
# CMD: 컨테이너가 뜰 때 기본으로 실행할 명령이다.
# 목적(용도): Flask 예측 서버를 0.0.0.0:9696 에서 켠다.
# 이 시점: 이미지 정의의 마지막 — run 하면 이 명령이 돌아간다.
