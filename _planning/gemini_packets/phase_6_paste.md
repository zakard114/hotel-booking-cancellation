# Phase 6 paste — containerization (7/9)

Scope note. Build and run the image. Do not deploy to a cloud.

## Table of contents

- [Rules](#rules)
- [Comments](#comments)
- [Facts](#facts)
- [Order](#order)
- [Success](#success)

---

## Rules

- Gate **(7/9)**. Dependency gate 6/9 is already done.
- Do not open a full reproducibility rewrite (8/9) or cloud (9/9) in the same pass.
- Build context is the repo root on E:.
- Do not rewrite predict or train business logic if the server already binds `0.0.0.0`.
- No `Co-authored-by` or other AI commit trailers.

[↑ Contents](#table-of-contents)

---

## Comments

On a new or confusing Dockerfile instruction, put three short lines **under** that instruction: what it is, why it is there, and where it sits in the file. Do not collect a name list at the bottom of the file.

[↑ Contents](#table-of-contents)

---

## Facts

- `predict.py` loads `models/model.bin` from the project root, so the image needs `WORKDIR /app` plus `src/` and `models/` under it.
- Port 9696. Route `POST /predict`.
- Pins live in `requirements.txt`. Do not retype versions from memory.

[↑ Contents](#table-of-contents)

---

## Order

1. `use_e_drive`, `cd` to the root, Docker Desktop running.
2. Fill the Dockerfile: base image, `WORKDIR`, copy requirements, `pip install`, copy `src/` and `models/`, `EXPOSE 9696`, CMD `python src/predict.py`.
3. `docker build -t hotel-cancel .`
4. `docker run --rm -p 9696:9696 hotel-cancel`
5. One host `POST /predict`.

**Done** 2026-11-09. Probability about 0.679, `is_canceled=true`.

[↑ Contents](#table-of-contents)

---

## Success

- [x] Image builds
- [x] Container serves Flask on 9696
- [x] One JSON prediction from the host
- [x] No cloud URL required

[↑ Contents](#table-of-contents)
