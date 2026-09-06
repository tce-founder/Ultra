---
title: Athlete card — current position
type: register
status: template
updated: 2026-09-06
---

# Athlete card

> **Derived, not asked.** This card is filled once, from what already exists — a training log, a race
> history, a calendar — and thereafter later runs report **drift** against it rather than
> re-interviewing the athlete. An advisory system that asks the same twelve questions every session
> is a form that has learned to talk.
>
> **Confidentiality.** Nothing here enters `advisory/kb/`. The corpus is the general layer read by
> every lens on every run; this is the specific layer and it stays out of it. Health data — blood
> work, menstrual-cycle data, clinical history — does not belong here either: it belongs with the
> athlete and their clinician, and this card records only that a referral exists, never its content.

## Empty by design

No athlete data has been entered. Seeding this with a plausible example would put invented content
in the one place in this repository reserved for things that are actually true, and every downstream
lens would read it as fact.

## The card

| Field | Value | Derived from | Last checked |
| ----- | ----- | ------------ | ------------ |
| Target race, date, distance, vertical | | | |
| Cutoffs, and the segment where they bind | | | |
| Weeks remaining | | | |
| Phase (base / strength / specific / taper) | | | |
| **Observed** weekly hours, rolling 12 wk | | | |
| **Planned** weekly hours | | | |
| Session completion rate, rolling 12 wk | | | |
| Weekly vertical, metres, with derivation | | | |
| Longest recent session | | | |
| Current tolerated fuelling rate, g/h | | | |
| Target fuelling rate, g/h | | | |
| Heat exposure available | | | |
| Injury status, and current restriction | | | |
| Energy-availability gate — pass / referred | | | |
| Sleep, habitual hours | | | |
| Competing life load, next 8 weeks | | | |
| Named crew / pacer | | | |

## Drift log

One line per review. What changed since the last card, and whether the change was planned.

| Date | Field | From | To | Planned? |
| ---- | ----- | ---- | -- | -------- |

## Rules

1. **The gate first.** If the energy-availability row is not a clear pass, no training
   recommendation is produced. See `advisory/kb/frameworks/energy-availability-floor.md`.
2. **Observed, not intended.** Every hours figure is taken from what happened, not from the plan.
   Athletes overestimate available hours by a large and consistent margin, and a card built from
   intentions produces a plan that fails in week three.
3. **State the derivation for vertical.** Indoor and outdoor vertical are measured differently and
   must never be summed into one number without saying how each was derived.
4. **A blank cell is honest; a guessed cell is not.** Downstream, they look identical.
