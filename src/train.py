"""
Training script for Hotel Booking Cancellation (XGBoost).
Usage (from project root or any cwd):
    python src/train.py
"""

from pathlib import Path
import pickle

import pandas as pd
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parents[1]
# Path(__file__).parents[1]: 이 파일(src/train.py) 기준 프로젝트 루트. 목적: cwd와 무관하게 data/models 찾기.
# 이 시점: 스크립트 시작, 경로 고정.

data_path = ROOT_DIR / "data" / "hotel_bookings.csv"

df = pd.read_csv(data_path)
# read_csv: CSV를 DataFrame으로 읽는다. 목적: 학습 원본 표를 올린다.
# 이 시점: 루트 경로가 잡힌 직후.

df = df.drop(
    columns=["reservation_status", "reservation_status_date"], errors="ignore"
)
# drop: 누수 후보 열 제거. 목적: 예약 이후 정보가 학습에 안 들어가게 한다.
# 이 시점: split 전.

df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
# train_test_split: 80/20·seed 42. 목적: Phase 1·2와 같은 분할 재현.
# 이 시점: 누수 제거 후.

y_train = df_train["is_canceled"].values
# values: 타깃을 배열로. 목적: 모델 label 입력.
# 이 시점: X/y 분리.
y_val = df_val["is_canceled"].values

X_train_df = df_train.drop(columns=["is_canceled"])
X_val_df = df_val.drop(columns=["is_canceled"])

num_cols = X_train_df.select_dtypes(include=["int64", "float64"]).columns
cat_cols = X_train_df.select_dtypes(include=["object", "category", "bool"]).columns

X_train_df[num_cols] = X_train_df[num_cols].fillna(0)
# fillna(0): 수치 결측 채움. 목적: NaN으로 학습이 깨지지 않게.
# 이 시점: DictVectorizer 직전.
X_train_df[cat_cols] = X_train_df[cat_cols].fillna("missing")
# fillna("missing"): 범주 결측을 문자열 범주로. 목적: country 등 빈칸 처리.
# 이 시점: 수치 채운 뒤.

X_val_df[num_cols] = X_val_df[num_cols].fillna(0)
X_val_df[cat_cols] = X_val_df[cat_cols].fillna("missing")

train_dicts = X_train_df.to_dict(orient="records")
# to_dict(orient="records"): 행→딕셔너리 리스트. 목적: DictVectorizer 입력.
# 이 시점: 결측 처리 후.
val_dicts = X_val_df.to_dict(orient="records")

dv = DictVectorizer(sparse=True)
# DictVectorizer: 딕셔너리→희소 행렬. 목적: 범주·수치를 모델용 피처로.
# 이 시점: T1 전처리.

X_train = dv.fit_transform(train_dicts)
# fit_transform: train 어휘 학습+변환. 목적: 인코딩 기준을 train에만 맞춤.
# 이 시점: DV fit.
X_val = dv.transform(val_dicts)
# transform: 같은 어휘로 val 변환. 목적: 누수 없이 검증 행렬 만들기(저장 전 검사용).
# 이 시점: fit 이후.

print("X_train shape:", X_train.shape)

features = list(dv.get_feature_names_out())
# get_feature_names_out: 열 이름 목록. 목적: DMatrix에 이름표 달기.
# 이 시점: XGB 학습 직전.

dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=features)
# DMatrix: XGB용 데이터. label=정답(y), feature_names=열 이름.
# 목적: 문제집(X)과 정답(y)을 짝짓고, 나중에 중요도 등에 이름을 쓰기 위함.
# 이 시점: train 호출 직전.

params = {
    "eta": 0.1,
    "max_depth": 6,
    "min_child_weight": 1,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "seed": 42,
}
# params: Phase 2 승자 설정. 목적: 동일 규칙으로 재학습.
# 이 시점: xgb.train 직전.

model = xgb.train(params, dtrain, num_boost_round=150)
# train: 부스팅 150라운드. 목적: Phase 2에서 고른 XGB를 아티팩트용으로 학습.
# 이 시점: T1 학습.

models_dir = ROOT_DIR / "models"
models_dir.mkdir(parents=True, exist_ok=True)
# mkdir: models 폴더 생성. 목적: 아티팩트 저장 위치 보장.
# 이 시점: T2 저장 직전.

output_file = models_dir / "model.bin"
with open(output_file, "wb") as f_out:
    pickle.dump((dv, model), f_out)
    # pickle.dump((dv, model)): 전처리기+모델을 한 파일에 저장. 목적: 나중에 predict가 같이 로드.
    # 이 시점: 학습이 끝난 직후.

print(f"Model successfully saved to {output_file}")


def main() -> None:
    print("train.py finished OK")


if __name__ == "__main__":
    main()
