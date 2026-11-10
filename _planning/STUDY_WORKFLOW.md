# Study workflow — build while learning

Each phase is understood and run before the next one starts.

## Table of contents

- [Roles](#roles)
- [Loop](#loop)
- [Done gate](#done-gate)
- [Checkpoints](#checkpoints)
- [Where to run](#where-to-run)
- [Where we are](#where-we-are)

---

## Roles

| Role | Work |
|------|------|
| Learner | Paste a packet, run the steps, bring the guide back, approve the diff |
| Guide | Beginner Why → What → How → check, from that packet only |
| Editor | Draft the packet, validity check, apply only what was allowed |

[↑ Contents](#table-of-contents)

---

## Loop

```text
Packet → beginner guide
→ if stuck, revise the guide
→ validity check
→ run only the clean guide
→ update PHASE_LOG → next phase only after it is allowed
```

Roadmap: [`ML_ROADMAP_PROTOCOL.md`](ML_ROADMAP_PROTOCOL.md)

[↑ Contents](#table-of-contents)

---

## Done gate

All three must be yes:

1. The learner ran the command or notebook cell and saw the result.
2. The learner can say what the phase does in one minute.
3. `PHASE_LOG.md` has the result and the learner read it.

[↑ Contents](#table-of-contents)

---

## Checkpoints

Gate and rubric tables: [`CHECKPOINTS.md`](CHECKPOINTS.md)  
Raise the README evaluation score when new evidence exists.

[↑ Contents](#table-of-contents)

---

## Where to run

- Default: `scripts/*.py` in the editor.
- Notebook: when the submission story needs cell-by-cell notes.
- Each step names the checklist item it closes.

[↑ Contents](#table-of-contents)

---

## Where we are

Gates **1–9 are done**, including the live Render URL. Next is the course submission (repo URL and commit ID) and peer reviews.

[↑ Contents](#table-of-contents)
