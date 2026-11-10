"""Phase 2 model training (3/9).

Run from a terminal:
  . E:\\IT_SPACES\\AI\\scripts\\use_e_drive.ps1
  cd E:\\IT_SPACES\\AI\\Projects\\ml\\hotel-booking-cancellation
  .\\.venv\\Scripts\\python.exe scripts\\phase2_models.py

About 37% of rows are cancels, so the comparison metric is ROC-AUC.
Leakage columns are dropped. seed=42.
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
# read_csv: load the CSV into memory. Same path as Phase 1.
# When: start of Phase 2.

df = df.drop(columns=LEAKAGE_COLS, errors="ignore")
# drop: remove post-booking columns so they cannot leak into training.
# When: right after load, before the split.

df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
# train_test_split: 80/20 with the Phase 1 seed so the split is the same.
# When: after leakage columns are removed, before X/y split.

y_train = df_train["is_canceled"].values
# values: Series to a NumPy array, the label shape the models expect.
# When: the target is taken off the train frame.
y_val = df_val["is_canceled"].values


def prepare_xy(frame: pd.DataFrame):
    X = frame.drop(columns=["is_canceled"]).copy()
    # Drop is_canceled so the answer is not a feature.
    # When: building the preprocessing input.
    for col in X.columns:
        if pd.api.types.is_numeric_dtype(X[col]):
            X[col] = X[col].fillna(0)
            # fillna(0): numeric gaps become 0 so NaN does not break the vectorizer.
            # When: just before DictVectorizer (children, agent, and similar columns).
        else:
            X[col] = X[col].fillna("missing").astype(str)
            # fillna("missing"): one category for blank strings such as country.
            # When: just before category encoding.
    return X


X_train_df = prepare_xy(df_train)
X_val_df = prepare_xy(df_val)

train_dicts = X_train_df.to_dict(orient="records")
# to_dict(orient="records"): list of {column: value} dicts for DictVectorizer.
# When: after missing-value fills, before vectorizing.
val_dicts = X_val_df.to_dict(orient="records")

dv = DictVectorizer(sparse=True)
# DictVectorizer: dict rows to a numeric matrix. sparse=True keeps memory down.
# When: preprocessing. This table has many category levels.

X_train = dv.fit_transform(train_dicts)
# fit_transform: learn category levels on train only and transform those rows.
# When: encoding is fixed to the train vocabulary.
X_val = dv.transform(val_dicts)
# transform: validation uses the train vocabulary only, even if a new level appears.
# When: after fit, before any model fit.

# --- T2 Logistic Regression ---
model_lr = LogisticRegression(max_iter=1000, random_state=42)
# LogisticRegression: linear baseline. Easy to read, first of the three models.
# When: first model.
model_lr.fit(X_train, y_train)
# fit: learn the linear weights for cancel probability.
# When: X_train and y_train are ready.
y_pred_lr = model_lr.predict_proba(X_val)[:, 1]
# predict_proba: class probabilities. Column 1 is P(cancel=1), the ROC-AUC score.
# When: validation, right after the logistic fit.
auc_lr = roc_auc_score(y_val, y_pred_lr)
# roc_auc_score: rank-based AUC. Comparable across models when about 37% of rows cancel.
# When: the shared metric for all three models.
print("LR ROC-AUC:", round(auc_lr, 4))

# --- T3 Random Forest ---
model_rf = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
)
# RandomForestClassifier: many trees vote. A nonlinear baseline.
# When: second model. max_depth is the small tune knob.
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict_proba(X_val)[:, 1]
auc_rf = roc_auc_score(y_val, y_pred_rf)
print("RF ROC-AUC:", round(auc_rf, 4))

# --- T3 small tune: try a couple of depths ---
best_rf_auc = auc_rf
best_rf = model_rf
for depth in (8, 12):
    # Small grid: a few max_depth values only. Not a large search.
    # When: after the default forest score is printed.
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
# DMatrix: XGBoost input, built from the same matrix the sklearn models used.
# When: third model.
dval = xgb.DMatrix(X_val, label=y_val)

xgb_params = {
    "eta": 0.1,
    "max_depth": 6,
    "min_child_weight": 1,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "seed": 42,
}
# params: learning rate, depth, and objective. Binary classification with AUC.
# When: just before xgb.train.

model_xgb = xgb.train(xgb_params, dtrain, num_boost_round=100)
# train: add trees for the given number of rounds. The stronger nonlinear candidate.
# When: the main XGBoost fit.
y_pred_xgb = model_xgb.predict(dval)
# predict: cancel probability per validation row, used for AUC.
# When: right after the XGBoost fit.
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
# max(..., key=): the name with the highest validation AUC.
# When: after the comparison table.
print("Selected:", winner, "AUC=", round(scores[winner], 4))

# Why this winner (read it next to the Selected line above):
# 1) All three models share the split, the preprocessing, and ROC-AUC.
# 2) About 37% cancel, so AUC is the comparison metric rather than accuracy.
# 3) The Selected line is the highest validation AUC on this table.
# 4) reservation_status columns were not used.
# 5) Gate 4/9 exports this winner from train.py.

print("Phase 2 script OK - three models trained, no API/Docker")
