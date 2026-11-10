# Phase 8 paste — cloud (9/9)

Runbook: [`phase_8_final_guide.md`](phase_8_final_guide.md)  
Deploy note: [`../../deploy/README.md`](../../deploy/README.md)

## Table of contents

- [Facts](#facts)

---

## Facts

Repo code already had `PORT`, `debug=False`, tracked `model.bin`, the Dockerfile, `render.yaml`, and the deploy note.

Learner steps that closed the gate: Render login, Blueprint, green Live URL, smoke, README evidence.

- Repo: https://github.com/zakard114/hotel-booking-cancellation (`main`)
- Render: https://render.com and https://dashboard.render.com
- Blueprint: **New +** → **Blueprint** → `zakard114/hotel-booking-cancellation` → `main` → **Apply**
- Success: green **Live** and a `.onrender.com` host
- **Done** 2026-11-10. Live https://hotel-cancel-api.onrender.com
- Certificate: **Heeju Yang**

A push to `main` rebuilds that service.

[↑ Contents](#table-of-contents)
