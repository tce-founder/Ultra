---
title: Athlete card — current position
type: register
status: active
updated: 2026-10-18
---

# Athlete card

> **Derived, not asked.** Filled once from what exists; later reviews report **drift** against it
> rather than re-interviewing. An advisory system that asks the same twelve questions every
> session is a form that has learned to talk.
>
> **Confidentiality.** Nothing here enters `advisory/kb/`. Health data — bloods, clinical
> correspondence — does not belong here either: this card records only *that* a referral or test
> exists, never its findings.

## The card

| Field | Value | Derived from | Last checked |
| ----- | ----- | ------------ | ------------ |
| Target race | **Hellbender 100**, Old Fort NC | `advisory/kb/subject/hellbender-100.md` | 2026-10-18 |
| Race date | **Fri 7 May 2027** — *athlete said 8 May; unresolved* | Ultrarunning.com listing | 2026-10-18 |
| Distance / vert | 102.3 mi · ~21,500 ft · 40 h cutoff | Official course page (sources disagree) | 2026-10-18 |
| Weeks remaining | 29 (week 1 begins Mon 19 Oct 2026) | Computed | 2026-10-18 |
| Phase | **Base 1 — tissue tolerance** (weeks 1–8) | Plan | 2026-10-18 |
| **Observed** weekly volume | **1–2 short runs most weeks** — intake band of 3–4 h was an overstatement | Athlete, 2026-10-18 (corrected same day) | 2026-10-18 |
| **Planned** weekly volume, week 1 | 3.0 h — 4 run days, not 5 | Plan | 2026-10-18 |
| Peak planned volume | 14.5 h (week 22, 50-mile tune-up) | Plan | 2026-10-18 |
| Days available | **6–7, flexible hours** | Athlete, 2026-10-18 | 2026-10-18 |
| Days actually scheduled | **6** — Monday is a full rest day by design | Plan | 2026-10-18 |
| Terrain access | **3–5 h from sustained climbs; weekends only** | Athlete, 2026-10-18 | 2026-10-18 |
| Mountain trips planned | 7 (weeks 6, 10, 14, 18, 21, 25, 27) | Plan | 2026-10-18 |
| Injury status | **Resolved posterior-Achilles bursitis** — heel-counter friction, ~March 2026, cost ~7 months of running. Fully settled, no current symptoms | Athlete, 2026-10-18 (**corrects** the intake answer of 'clean history') | 2026-10-18 |
| Energy-availability gate | **Not yet run** — see `plan/nutrition.md` §0 | — | — |
| Longest run, last 2 months | **~5k** | Athlete, 2026-10-18 | 2026-10-18 |
| Ultra history / longest ever | **50-miler finished, ~March 2026.** Month/year to confirm | Athlete, 2026-10-18 | 2026-10-18 |
| Bodyweight (kg) | *unknown — blocks every nutrition figure* | — | — |
| Current tolerated fuelling rate | *unknown — measure in week 1* | — | — |
| HR zones / threshold | *unknown — all Garmin workouts ship with no target* | — | — |
| Ferritin / vitamin D | *not tested* | — | — |
| Shoe rotation audited | **No — scheduled week 1 Wednesday** | Plan | — |
| Named crew / pacer | *none yet* | — | — |

## The four unknowns that matter, ranked

1. **Longest run in the last two months, and any ultra finished.** The plan assumes a first
   hundred off a low base. If there is a 50-miler in recent history the early phases are too
   conservative; if the longest run is 6 miles, week 1 is already too much. **Highest-value
   missing fact in this file.**
2. **Bodyweight.** Every number in `plan/nutrition.md` is per-kilogram and uncomputed without it.
3. **Current tolerated fuelling rate**, measured on a real long run rather than estimated. The
   gut-training progression starts from it.
4. **Whether the race has a qualifying standard.** If it does, the week-22 50-miler stops being
   a tune-up and becomes a requirement with its own entry deadline.

## The standing risk on this build

**Ramp rate, not fitness.** Under 20 mi/week to a 102-mile mountain hundred in 29 weeks is
aggressive, and the limiting system is connective tissue rather than aerobic capacity. The
athlete has 6–7 days available, which makes it *easy* to do more than the plan asks and to
*feel* fine doing it for about ten weeks.

The plan defends this with an 8-week base phase, down weeks every fourth week, a mandatory
Monday rest day, and a 22% ceiling on the build-week ramp that `build_plan.py` enforces rather
than suggests. **The failure mode to watch for in reviews is not missed sessions — it is added
ones.**

## Drift log

| Date | Field | From | To | Planned? |
| ---- | ----- | ---- | -- | -------- |
| 2026-10-18 | Card created | — | Baseline recorded from a four-question intake | — |
| 2026-10-18 | Injury status | "clean history" | Resolved posterior-Achilles bursitis, ~7 months off | No — intake correction |
| 2026-10-18 | Weekly volume | 3–4 h | 1–2 short runs | No — intake correction |
| 2026-10-18 | Ultra history | unknown | 50-miler finished | No — new information |

## Rules

1. **The gate first.** If the energy-availability row is not a clear pass, no training
   recommendation is produced.
2. **Observed, not intended.** Hours come from what happened, not from the plan.
3. **State the derivation for vert.** Indoor and outdoor vertical are measured differently and
   must never be summed without saying how each was derived.
4. **A blank cell is honest; a guessed cell is not.** Downstream they look identical.
