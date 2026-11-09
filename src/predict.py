"""
Prediction service for Hotel Booking Cancellation (Flask + XGBoost).
Usage:
    python src/predict.py
"""

from pathlib import Path
import os
import pickle

import pandas as pd
import xgboost as xgb
from flask import Flask, jsonify, request

ROOT_DIR = Path(__file__).resolve().parents[1]
model_path = ROOT_DIR / "models" / "model.bin"

with open(model_path, "rb") as f_in:
    dv, model = pickle.load(f_in)
# pickle.load: 저장된 바이트 파일을 다시 파이썬 객체(튜플)로 역직렬화합니다.
# 목적(용도): 학습 때 사용한 전처리 규칙과 XGBoost 모델을 서비스 환경에 그대로 복원하기 위함입니다.
# 이 시점: predict.py가 실행되자마자 서버가 켜지기 전 딱 한 번 수행됩니다.

print("Model and DictVectorizer loaded successfully!")


def predict_single(customer_data):
    customer_data.pop("reservation_status", None)
    customer_data.pop("reservation_status_date", None)

    for key, val in customer_data.items():
        if isinstance(val, (int, float)):
            customer_data[key] = 0 if pd.isna(val) else val
        else:
            customer_data[key] = "missing" if pd.isna(val) else str(val)

    X = dv.transform([customer_data])
    # dv.transform: 학습 때 쓰인 DictVectorizer 규칙을 바탕으로 딕셔너리를 수치 행렬로 바꿉니다.
    # 목적(용도): 문자열 카테고리를 원핫 인코딩 수치 형태로 변환하기 위함입니다.
    # 이 시점: 사용자가 보낸 1건의 예약 데이터를 모델에 넣기 직전 전처리 단계입니다.

    features = list(dv.get_feature_names_out())
    dtest = xgb.DMatrix(X, feature_names=features)
    # xgb.DMatrix: XGBoost 전용 고성능 데이터 구조를 생성합니다.
    # 목적(용도): 학습 때와 feature_names를 일치시켜 ValueError를 방지하고 최적화된 예측을 수행하기 위함입니다.
    # 이 시점: 전처리가 끝난 행렬을 XGBoost 모델 입력용 객체로 감싸는 시점입니다.

    y_pred = model.predict(dtest)
    # model.predict: 모델을 통해 최종 이진 분류 예측값(취소 확률)을 산출합니다.
    # 목적(용도): 입력된 예약 정보가 취소될 확률을 수치로 얻기 위함입니다.
    # 이 시점: DMatrix 준비가 완료된 후 예측을 수행하는 마지막 단계입니다.

    return float(y_pred[0])


app = Flask("hotel-cancellation")


@app.route("/predict", methods=["POST"])
def predict():
    customer = request.get_json()
    probability = predict_single(customer)
    result = {
        "cancel_probability": probability,
        "is_canceled": bool(probability >= 0.5),
    }
    return jsonify(result)
    # jsonify: 파이썬 딕셔너리 데이터를 HTTP 응답용 JSON 형식으로 변환합니다.
    # 목적(용도): 클라이언트(API 요청자)가 읽을 수 있는 표준 JSON 형태로 결과를 돌려주기 위함입니다.
    # 이 시점: 예측 연산이 모두 끝난 후 응답을 전송하기 직전입니다.


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9696"))
    # os.environ.get: 환경변수 PORT를 읽고, 없으면 기본값 9696을 씁니다.
    # 목적(용도): 클라우드(Render 등)가 지정한 포트로 서버를 열기 위함입니다.
    app.run(debug=False, host="0.0.0.0", port=port)
    # app.run: Flask 웹 서버를 시작합니다.
    # debug=False: 배포용으로 디버그 모드를 끕니다.
