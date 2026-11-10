# Phase 7 paste — reproducibility (8/9)

The runbook is [`phase_7_final_guide.md`](phase_7_final_guide.md). This file is the scope note.

## Table of contents

- [Rules](#rules)
- [Rubric](#rubric)
- [Already done](#already-done)
- [Tasks](#tasks)

---

## Rules

- Gate **(8/9)** only. Do not change paths, seeds, or file names.
- E: only. Before install or run: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.
- The CSV stays gitignored. Do not force it into git. `data/README.md` is the download path.
- No cloud, no new tuning, no caches on `C:`, no AI commit trailers.
- Stop with “next guide after permission”.

[↑ Contents](#table-of-contents)

---

## Rubric

Official maximum 1. The point is earned when the notebook and `train.py` rerun, and the data is present or the download steps are clear.

[↑ Contents](#table-of-contents)

---

## Already done

- `data/README.md`
- `requirements.txt` with five pins
- `src/train.py` (`random_state=42`, XGBoost `seed=42`)
- `notebooks/notebook.ipynb`
- Docker gate 7/9 done

[↑ Contents](#table-of-contents)

---

## Tasks

- T1: README order — data, venv, train, optional predict or docker
- T2: document the seeds
- T3: `python src/train.py` smoke
- T4: evaluation and checkpoint evidence

**Done** 2026-11-09. Score 1/1. `X_train` shape 95512×254.

[↑ Contents](#table-of-contents)
