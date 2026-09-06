---
title: Action register
type: register
status: template
updated: 2026-09-06
---

# Action register

> Every committed or advised action, with an owner and what blocks it. **Seeded from the plan the
> athlete already has**, never generated beside it — a second plan produced alongside an existing one
> is how both get abandoned.
>
> IDs are `ACT-n` and are permanent. A superseded action is marked superseded, with the ID that
> replaced it; the row is not deleted, because the register's whole value is that it remembers what
> was advised and did not happen.

## Empty by design

No actions recorded. The first row goes in after the first review.

| ID | Action | Owner | Blocked by | Source | Opened | Status |
| -- | ------ | ----- | ---------- | ------ | ------ | ------ |

## Conventions

- **Owner is a person**, not "the plan". An action nobody owns did not get advised, it got mentioned.
- **Blocked by names the actual blocker** — a date, a piece of kit, a clinician's appointment, a
  decision not yet made. "Time" is not a blocker; it is the absence of a decision about priority.
- **Source** cites the corpus page or the review that produced it, so a retracted claim can be
  traced to the actions resting on it. That is what `workflows/build_graph.py --impact` walks.
- **Status** is one of: open · done · superseded by ACT-n · dropped (with a reason).
- An action still open after three reviews is either blocked by something unrecorded or was never
  going to happen. Both are worth saying out loud rather than rolling forward.
