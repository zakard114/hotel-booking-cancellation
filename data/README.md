# Data — hotel booking demand

The full CSV stays out of git (see the root `.gitignore`). Reviewers need a clear download path.

## Table of contents

- [Source](#source)
- [Download](#download)
- [Notes](#notes)

---

## Source

- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
- Paper: Antonio, Almeida, Nunes — hotel booking demand datasets
- Target column: `is_canceled` (0/1)

[↑ Contents](#table-of-contents)

---

## Download

Windows, **E:** only.

1. Create a free Kaggle account and accept the dataset terms.
2. If you use the Kaggle API, keep `kaggle.json` off git.
3. In PowerShell:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation

# Option A — browser: download the ZIP and extract hotel_bookings.csv into data/ on E:

# Option B — CLI (only if kaggle is already set up; stop if it runs longer than 5 minutes)
# kaggle datasets download -d jessemostipak/hotel-booking-demand -p data --unzip

# Option C — public GitHub mirror of the same CSV (no Kaggle login)
# https://raw.githubusercontent.com/aaqibqadeer/Hotel-booking-demand/master/hotel_bookings.csv
```

Expected file: `data/hotel_bookings.csv`.  
This workspace already has that file from Option C (~16.6 MB). It is gitignored.

[↑ Contents](#table-of-contents)

---

## Notes

- If a download asks for credentials or hangs, stop and use the browser path onto `E:\…\data\` only.
- Do not put the CSV under `C:\Users\...`.

[↑ Contents](#table-of-contents)
