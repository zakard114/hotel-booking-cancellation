"""Phase 2 · Model training (3/9)

VS Code / 터미널에서 실행:
  . E:\\IT_SPACES\\AI\\scripts\\use_e_drive.ps1
  cd E:\\IT_SPACES\\AI\\Projects\\ml\\hotel-booking-cancellation
  .\\.venv\\Scripts\\python.exe scripts\\phase2_models.py

타깃 ~37% cancel → ROC-AUC로 비교. 누수 컬럼 제외. seed=42.
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import xgboost as xgb

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "hotel_bookings.csv"

LEAKAGE_COLS = ["reservation_status", "reservation_status_date"]

df = pd.read_csv(CSV)
# read_csv: 디스크의 CSV를 DataFrame으로 읽는다. 목적: 학습 원본 표를 메모리에 올린다.
# 이 시점: Phase 2 시작, Phase 1과 같은 파일 경로.

df = df.drop(columns=LEAKAGE_COLS, errors="ignore")
# drop: 지정 열을 표에서 뺀다. 목적: 예약 이후 정보(누수)를 학습에 안 넣는다.
# 이 시점: 로드 직후, split·피처 만들기 전.

df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
# train_test_split: 행을 훈련/검증으로 나눈다. 목적: Phase 1과 같은 80/20·시드로 재현한다.
# 이 시점: 누수 열 제거 후, X/y 분리 직전.

y_train = df_train["is_canceled"].values
# values: 시리즈를 넘파이 배열로 만든다. 목적: 모델이 기대하는 y 형태로 맞춘다.
# 이 시점: train 표에서 타깃만 분리.
y_val = df_val["is_canceled"].values


def prepare_xy(frame: pd.DataFrame):
    X = frame.drop(columns=["is_canceled"]).copy()
    # drop is_canceled: 타깃을 피처에서 뺀다. 목적: X에 정답이 섞이지 않게 한다.
    # 이 시점: 전처리 파이프라인 입력을 만들 때.
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            X[col] = X[col].fillna(0)
            # fillna(0): 숫자 빈칸을 0으로 채운다. 목적: NaN 때문에 변환/학습이 깨지지 않게 한다.
            # 이 시점: DictVectorizer 직전, children/agent 등 결측 처리.
        else:
            X[col] = X[col].fillna("missing").astype(str)
            # fillna("missing"): 범주 빈칸을 문자열 범주로 둔다. 목적: country 등 결측을 한 카테고리로 취급.
            # 이 시점: 범주 열 인코딩 직전.
    return X


X_train_df = prepare_xy(df_train)
X_val_df = prepare_xy(df_val)

train_dicts = X_train_df.to_dict(orient="records")
# to_dict(orient="records"): 각 행을 {열이름:값} 딕셔너리 리스트로 만든다. 목적: DictVectorizer 입력 형식.
# 이 시점: 결측 처리 후, 원-핫/벡터화 직전.
val_dicts = X_val_df.to_dict(orient="records")

dv = DictVectorizer(sparse=True)
# DictVectorizer: 딕셔너리 행을 숫자 행렬로 바꾼다. 목적: 범주·수치를 모델이 먹는 피처 행렬로 만든다.
# 이 시점: T1 전처리. sparse=True로 메모리 절약(호텔 데이터 범주 많음).

X_train = dv.fit_transform(train_dicts)
# fit_transform: 열 이름(범주 수준)을 익히며 행렬로 변환한다. 목적: train에만 맞춰 어휘를 고정한다.
# 이 시점: 검증 누수 없이 train 기준으로 인코딩.
X_val = dv.transform(val_dicts)
# transform: 이미 익힌 어휘로만 변환한다. 목적: val에 새 범주가 있어도 train 기준으로 맞춘다.
# 이 시점: fit 이후, 모델 학습 전.

# --- T2 Logistic Regression ---
model_lr = LogisticRegression(max_iter=1000, random_state=42)
# LogisticRegression: 선형 로지스틱 분류기. 목적: 단순·해석 쉬운 기준 모델.
# 이 시점: T2, 첫 모델.
model_lr.fit(X_train, y_train)
# fit: 계수(가중치)를 데이터에 맞춘다. 목적: 취소 확률을 선형으로 학습한다.
# 이 시점: X_train/y_train 준비 직후.
y_pred_lr = model_lr.predict_proba(X_val)[:, 1]
# predict_proba: 클래스별 확률. [:,1]은 취소(1) 확률. 목적: ROC-AUC용 점수.
# 이 시점: LR fit 직후 val 평가.
auc_lr = roc_auc_score(y_val, y_pred_lr)
# roc_auc_score: 순위 기반 AUC. 목적: 불균형(~37% cancel)에서도 비교 가능한 지표.
# 이 시점: 세 모델 공통 비교 지표.
print("LR ROC-AUC:", round(auc_lr, 4))

# --- T3 Random Forest ---
model_rf = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
)
# RandomForestClassifier: 여러 결정나무 투표. 목적: 비선형 패턴 기준 모델.
# 이 시점: T3. max_depth로 과적합·시간 조절(작은 튜닝 시작점).
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict_proba(X_val)[:, 1]
auc_rf = roc_auc_score(y_val, y_pred_rf)
print("RF ROC-AUC:", round(auc_rf, 4))

# --- T3 small tune: try a couple of depths ---
best_rf_auc = auc_rf
best_rf = model_rf
for depth in (8, 12):
    # 작은 그리드: max_depth만 몇 개. 목적: T5 간단 튜닝(거대 서치 금지).
    # 이 시점: 기본 RF 점수 본 뒤.
    m = RandomForestClassifier(
        n_estimators=100, max_depth=depth, random_state=42, n_jobs=-1
    )
    m.fit(X_train, y_train)
    a = roc_auc_score(y_val, m.predict_proba(X_val)[:, 1])
    print(f"RF depth={depth} ROC-AUC:", round(a, 4))
    if a > best_rf_auc:
        best_rf_auc = a
        best_rf = m

# --- T4 XGBoost ---
dtrain = xgb.DMatrix(X_train, label=y_train)
# DMatrix: XGBoost 전용 데이터 포맷. 목적: 부스팅 학습/예측 입력.
# 이 시점: T4, sklearn 행렬을 XGB로 넘길 때.
dval = xgb.DMatrix(X_val, label=y_val)

xgb_params = {
    "eta": 0.1,
    "max_depth": 6,
    "min_child_weight": 1,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "seed": 42,
}
# params: 학습률·깊이·목적함수. 목적: 이진 분류 + AUC 모니터링.
# 이 시점: xgb.train 호출 직전.

model_xgb = xgb.train(xgb_params, dtrain, num_boost_round=100)
# train: 부스팅 라운드를 돌리며 트리를 쌓는다. 목적: RF보다 강한 비선형 모델 후보.
# 이 시점: T4 본학습.
y_pred_xgb = model_xgb.predict(dval)
# predict: 각 행의 취소 확률(대략). 목적: val AUC 계산.
# 이 시점: XGB 학습 직후.
auc_xgb = roc_auc_score(y_val, y_pred_xgb)
print("XGB ROC-AUC:", round(auc_xgb, 4))

best_xgb_auc = auc_xgb
best_xgb_rounds = 100
for rounds in (50, 150):
    m = xgb.train(xgb_params, dtrain, num_boost_round=rounds)
    a = roc_auc_score(y_val, m.predict(dval))
    print(f"XGB rounds={rounds} ROC-AUC:", round(a, 4))
    if a > best_xgb_auc:
        best_xgb_auc = a
        best_xgb_rounds = rounds
        model_xgb = m

# --- T5 comparison ---
print("\n=== Comparison (val ROC-AUC) ===")
print(f"LogisticRegression: {auc_lr:.4f}")
print(f"RandomForest(best): {best_rf_auc:.4f}")
print(f"XGBoost(best, rounds={best_xgb_rounds}): {best_xgb_auc:.4f}")

scores = {
    "logistic": auc_lr,
    "random_forest": best_rf_auc,
    "xgboost": best_xgb_auc,
}
winner = max(scores, key=scores.get)
# max(..., key=): 점수가 가장 큰 키. 목적: 비교표에서 우승 모델 이름 고르기.
# 이 시점: T5 직후 T6 선정.
print("Selected:", winner, "AUC=", round(scores[winner], 4))

# T6 — 선정 이유 (주석으로 남김; 숫자 나오면 위 Selected와 맞춰 읽기)
# 1) 세 모델 모두 같은 split·전처리·ROC-AUC로 비교했다.
# 2) 불균형(~37% cancel)이라 accuracy보다 AUC를 우선했다.
# 3) 우승 모델은 위 Selected 한 줄이다 이 데이터에서 val AUC가 가장 높다.
# 4) 누수 열(reservation_status*)은 쓰지 않았다.
# 5) 다음 게이트(4/9)에서 이 승자를 train.py로 수출한다.

print("Phase 2 script OK - three models trained, no API/Docker")
