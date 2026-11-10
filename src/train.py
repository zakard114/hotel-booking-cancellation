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
# parents[1]: repo root from this file (src/train.py). Finds data/ and models/ no matter the cwd.
# When: start of the script, paths are fixed.

data_path = ROOT_DIR / "data" / "hotel_bookings.csv"

df = pd.read_csv(data_path)
# read_csv: load the CSV into a DataFrame. This is the training table.
# When: immediately after the root path is set.

df = df.drop(
    columns=["reservation_status", "reservation_status_date"], errors="ignore"
)
# drop: remove leakage columns so post-booking fields never enter training.
# When: before the split.

df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
# train_test_split: 80/20, seed 42. Same split as Phase 1 and Phase 2.
# When: after leakage columns are gone.

y_train = df_train["is_canceled"].values
# values: target as an array, the label input for the model.
# When: X and y are being separated.
y_val = df_val["is_canceled"].values

X_train_df = df_train.drop(columns=["is_canceled"])
X_val_df = df_val.drop(columns=["is_canceled"])

num_cols = X_train_df.select_dtypes(include=["int64", "float64"]).columns
cat_cols = X_train_df.select_dtypes(include=["object", "category", "bool"]).columns

X_train_df[num_cols] = X_train_df[num_cols].fillna(0)
# fillna(0): fill numeric gaps so NaN does not break training.
# When: just before DictVectorizer.
X_train_df[cat_cols] = X_train_df[cat_cols].fillna("missing")
# fillna("missing"): turn category gaps into one string level (for example country).
# When: after the numeric fill.

X_val_df[num_cols] = X_val_df[num_cols].fillna(0)
X_val_df[cat_cols] = X_val_df[cat_cols].fillna("missing")

train_dicts = X_train_df.to_dict(orient="records")
# to_dict(orient="records"): each row becomes a dict. That is the DictVectorizer input.
# When: after missing values are filled.
val_dicts = X_val_df.to_dict(orient="records")

dv = DictVectorizer(sparse=True)
# DictVectorizer: dict rows to a sparse matrix of category and numeric features.
# When: preprocessing, before the booster.

X_train = dv.fit_transform(train_dicts)
# fit_transform: learn the vocabulary on train and transform those rows.
# When: DictVectorizer fit. Validation must not fit.
X_val = dv.transform(val_dicts)
# transform: apply the train vocabulary to validation. Check only; the saved file is the train fit.
# When: after fit.

print("X_train shape:", X_train.shape)

features = list(dv.get_feature_names_out())
# get_feature_names_out: column names for the DMatrix.
# When: just before XGBoost train.

dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=features)
# DMatrix: XGBoost table. label is y, feature_names keep column labels for later importance reads.
# When: immediately before train.

params = {
    "eta": 0.1,
    "max_depth": 6,
    "min_child_weight": 1,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "seed": 42,
}
# params: the Phase 2 winner settings, so this retrain follows the same rules.
# When: just before xgb.train.

model = xgb.train(params, dtrain, num_boost_round=150)
# train: 150 boosting rounds. Refit the chosen XGBoost for the artifact.
# When: the training call.

models_dir = ROOT_DIR / "models"
models_dir.mkdir(parents=True, exist_ok=True)
# mkdir: create models/ so the artifact has a place to land.
# When: just before save.

output_file = models_dir / "model.bin"
with open(output_file, "wb") as f_out:
    pickle.dump((dv, model), f_out)
    # pickle.dump((dv, model)): save the vectorizer and the booster together so predict can load both.
    # When: immediately after training.

print(f"Model successfully saved to {output_file}")


def main() -> None:
    print("train.py finished OK")


if __name__ == "__main__":
    main()
