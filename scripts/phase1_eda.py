"""Phase 1 EDA (2/9) — terminal mirror of the notebook.

Same steps as the notebook. This file is the fast edit path. The submission narrative is notebooks/notebook.ipynb.

Run from the project root:
  . E:\\IT_SPACES\\AI\\scripts\\use_e_drive.ps1
  cd E:\\IT_SPACES\\AI\\Projects\\ml\\hotel-booking-cancellation
  .\\.venv\\Scripts\\python.exe scripts\\phase1_eda.py
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "hotel_bookings.csv"

# --- Load ---
df = pd.read_csv(CSV)
print("Shape:", df.shape)
print(df.dtypes)
print(df.head())

# --- Missing ---
missing = df.isnull().sum()
print("\nMissing (nonzero):\n", missing[missing > 0])

# --- Target ---
print("\nis_canceled counts:\n", df["is_canceled"].value_counts())
print("\nis_canceled %:\n", df["is_canceled"].value_counts(normalize=True) * 100)

# nunique. The leakage and feature memo is in the notebook markdown.
print("\nnunique:\n", df.nunique())

# --- Split (no fit) ---
df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)
print("\nTrain:", df_train.shape, "Val:", df_val.shape)
print("Phase 1 script OK - no model.fit")
