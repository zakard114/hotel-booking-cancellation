# Phase 6 final guide — containerization (7/9)

**Done** (2026-11-09).

## Table of contents

- [Why](#why)
- [What](#what)
- [How](#how)
- [Check](#check)

---

## Why

Pinned packages are not enough for a reviewer who does not have the same OS libraries (XGBoost needs OpenMP). The image carries the runtime.

[↑ Contents](#table-of-contents)

---

## What

- Root `Dockerfile`
- Tag `hotel-cancel`
- Host port 9696 mapped to the container
- One `POST /predict` from the host

[↑ Contents](#table-of-contents)

---

## How

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation
docker build -t hotel-cancel .
docker run --rm -d -p 9696:9696 --name hotel-cancel-api hotel-cancel
```

`docker build` packs dependencies, code, and `models/model.bin` into one image. `docker run -p 9696:9696` publishes the Flask port. Stop the container after the smoke call: `docker stop hotel-cancel-api`.

Recorded smoke: `cancel_probability≈0.679`, `is_canceled=true`.

[↑ Contents](#table-of-contents)

---

## Check

- [x] Build succeeded
- [x] Logs showed the model loaded and the server running
- [x] Host POST returned JSON
- [x] Cloud was not part of this gate

[↑ Contents](#table-of-contents)
