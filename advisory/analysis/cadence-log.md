---
title: Cadence log
type: register
status: template
updated: 2026-09-06
---

# Cadence log

> **Append-only. One line per review.** Never rewritten.
>
> This file carries the only cross-run state the review loop has: the **no-action streak** — how many
> consecutive reviews have produced no completed action. A rewritten line silently resets it, which
> is why the append-only rule is load-bearing rather than tidy.
>
> **The kill condition.** Three consecutive reviews with no action completed means the loop is
> producing reading rather than change, and it stops until something outside it changes. An advisory
> system nobody acts on is not neutral — it consumes attention and manufactures the feeling of
> progress.

## Empty by design

| Date | Clock | Phase | What moved | Action proposed | Action completed since last | No-action streak |
| ---- | ----- | ----- | ---------- | --------------- | --------------------------- | ---------------- |

## Conventions

- `clock` is `weekly` or `monthly`. Daily is available and is almost always wrong for this sport:
  the signal in a single day of endurance training is nearly all noise.
- **One action proposed per review.** Not three. A review that proposes three proposes none.
- The action is taken **from the plan that already exists** wherever possible, rather than invented
  beside it.
- **Manual invocation only.** Automating a review before it has proved useful is how it becomes
  wallpaper — read once, then never.
