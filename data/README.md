# Data — hotel booking demand

**Do not commit the full CSV** by default (see root `.gitignore`). Peer reviewers need clear download steps.

## Source

- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand  
- Paper / original: Antonio, Almeida, Nunes — hotel booking demand datasets  
- Target column: `is_canceled` (0/1)

## Download (Windows, E: only)

1. Create a free Kaggle account and accept the dataset terms on the dataset page.
2. If using the Kaggle API: place `kaggle.json` where the CLI expects it (or use env vars from `.env.example`). Keep credentials off git.
3. In PowerShell:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation

# Option A — browser: download ZIP, extract hotel_bookings.csv into this data/ folder on E:

# Option B — CLI (only if kaggle is already set up; abort if >5 min / auth missing)
# kaggle datasets download -d jessemostipak/hotel-booking-demand -p data --unzip

# Option C — public GitHub mirror (same Kaggle CSV; no Kaggle login)
# https://raw.githubusercontent.com/aaqibqadeer/Hotel-booking-demand/master/hotel_bookings.csv
```

Expected file (name may vary slightly): `data/hotel_bookings.csv`  
(현재 워크스페이스에는 Option C로 `data/hotel_bookings.csv` ~16.6MB 확보됨.)

## Notes

- If download needs credentials or hangs: stop and use browser download to `E:\…\data\` only.
- Do not put the CSV under `C:\Users\...`.
