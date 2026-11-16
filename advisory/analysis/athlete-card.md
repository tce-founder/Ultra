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
| Home | **Hampstead, NC** — coastal plain, Pender County, effectively sea level | Athlete, 2026-11-05 | 2026-11-05 |
| Terrain access | **~330–340 mi / 5–5.5 h each way to Old Fort** (my estimate, not verified — check a mapping service). The intake band of "3–5 h" understated it. **Zero usable local vert and zero local descent** | Athlete + estimate, 2026-11-05 | 2026-11-05 |
| Mountain trips planned | 7 (weeks 6, 10, 14, 18, 21, 25, 27) — **now a 10–11 h round trip each, so each is a 2-night stay, not a day trip. ~75 h of driving in total. Needs consolidating — see below** | Plan | 2026-11-05 |
| Races entered | **None.** Heartbreaker declined 2026-10-31 in favour of a self-supported 50; week-15 50K still unchosen | Athlete, 2026-10-31 | 2026-10-31 |
| Course knowledge | **Has raced Hellbender's first-half terrain**: Camp Grier start, Snooks Nose, Green Knob, Mt Mitchell via Black Mountain Crest, Heartbreak Ridge | Athlete, 2026-10-31 | 2026-10-31 |
| Heartbreaker result | **DNF, 45 mi / 15h00. CAUSE CORRECTED 2026-11-16: quadriceps failure on the descents — could not maintain speed.** NOT the toe-to-bursitis cascade, which happened and cost 7 months but was not what stopped the race. 14:22 was offered 2026-11-02 and retracted 2026-11-03 | Athlete, 2026-11-16 | 2026-11-16 |
| Hellbender projection | **36h13 – 43h38 against a 40 h cutoff — MARGINAL, ~51% of assumptions finish.** From a 16h51 full-distance equivalent, itself extrapolated from the DNF. **The caveat that cut the other way is now WEAKER** (2026-11-16): the 15h00 was not primarily an injury artifact but eccentric durability running out, so it is closer to a real estimate than to a floor. Read ~51% as less optimistic, not more | `projection.py --dnf 45 15:00` | 2026-11-05 |
| Injury status | **Resolved posterior-Achilles bursitis**, ~March 2026, ~7 months off. CAUSAL CHAIN (corrected 2026-10-31): stubbed toe mid-race → lost toenail → altered gait → heel driven into the counter → bursitis. **Not primarily a shoe fault — a compensation injury.** Fully settled | Athlete, 2026-10-18 (**corrects** the intake answer of 'clean history') | 2026-10-18 |
| Energy-availability gate | **Not yet run** — see `plan/nutrition.md` §0 | — | — |
| Longest run, last 2 months | **~5k** | Athlete, 2026-10-18 | 2026-10-18 |
| Ultra history / longest ever | **Mount Mitchell Heartbreaker 50M, March 2026** — confirmed 2026-10-31. 50 mi, ~12,000 ft, from Camp Grier. Finish time UNKNOWN and now the top open item | Athlete, 2026-10-31 | 2026-10-31 |
| Bodyweight (kg) | **84 kg / 185 lb** | Athlete, 2026-11-15 | 2026-11-15 |
| Goal weight | **190 lb (86 kg) by ~week 16**, as lean mass, for descent durability. Athlete asked for 190–195; 195 is not available inside the window without fat gain. Explicitly NOT a cut — Ironman history of cutting and feeling weak | Athlete + `plan/nutrition.md` §1a | 2026-11-15 |
| Current tolerated fuelling rate | *unknown — measure in week 1* | — | — |
| HR zones / threshold | *still unknown — Garmin workouts ship with no target.* **First anchor 2026-11-06:** avg HR 134 / max 162 on technical trail, reported as easy. Working easy ceiling ~140 bpm until a real test | Athlete, 2026-11-06 | 2026-11-15 |
| Easy pace anchor | **~8:30–9:00 /km running on technical trail** at HR 134 (derived, one session). Flat/smooth: ~8:00–9:00 /km. REPORTED grade — one data point, walk pace assumed | Derived from 2026-11-06 | 2026-11-15 |
| Ferritin / vitamin D | *not tested* | — | — |
| Shoe rotation audited | **No — scheduled week 1 Wednesday** | Plan | — |
| Named crew / pacer | *none yet* | — | — |

## The four unknowns that matter, ranked

1. **Longest run in the last two months, and any ultra finished.** The plan assumes a first
   hundred off a low base. If there is a 50-miler in recent history the early phases are too
   conservative; if the longest run is 6 miles, week 1 is already too much. **Highest-value
   missing fact in this file.**
2. ~~**Bodyweight.**~~ **ANSWERED 2026-11-15: 185 lb / 84 kg.** All nutrition figures now computed.
3. **Current tolerated fuelling rate**, measured on a real long run rather than estimated. The
   gut-training progression starts from it.
4. **Whether the race has a qualifying standard.** If it does, the week-22 50-miler stops being
   a tune-up and becomes a requirement with its own entry deadline.

## The primary limiter — corrected 2026-11-16

**Eccentric quadriceps durability on descent.** The athlete corrected the DNF cause: the 2026
race ended because the quads were shot on the descents and speed could not be maintained. The
toe-to-nail-to-gait-to-bursitis cascade is real, cost seven months, and still governs foot and
heel prevention — but it is not what stopped the race.

This moves descending from risk 4 to **risk 1**, and it is the worst possible pairing with this
athlete's geography: Hampstead is sea level, the nearest real descent is 5–5.5 h away, and the
plan originally contained seven mountain weekends and one never-progressing 3x10 step-down for
the exact system that failed.

**The arithmetic is unkind.** The Heartbreaker is ~12,000 ft over 50 miles (~240 ft/mi);
Hellbender is ~21,500 ft over 102 miles (~210 ft/mi). Similar density, but **roughly double the
absolute descent load**, asked of the system that gave out at mile 45 of the shorter race.

Addressed by three threads added 2026-11-16: a progressive `ECCENTRIC` block (load, step height
and tempo now advance by phase, where before the prescription was identical in week 3 and week
25), a `DESCENT_REPS` block appended to the END of non-mountain long runs (tired legs, because
the quads failed at mile 45 and not at mile 5), and the mountain weekends.

**What this does NOT fix:** a flat 50 tests none of it. See the Badwater note in the drift log.

## The other standing risk

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
| 2026-10-31 | Week 22 | Mount Mitchell Heartbreaker 50M | Self-supported 50 on the Hellbender course | Yes — athlete's call |
| 2026-10-31 | Injury mechanism | "heel-cup rubbing" | Toe trauma → nail loss → gait change → heel rub | No — correction. Shifts prevention to toe box, nail care and reacting to gait change |
| 2026-10-31 | Ultra history | "a 50 in March last year" | **Mount Mitchell Heartbreaker, March 2026** | No — confirmation. Resolves the 2025/2026 ambiguity and establishes course knowledge |
| 2026-11-02 | Heartbreaker time | unknown | 14:22 | No — athlete self-report |
| 2026-11-03 | Heartbreaker time | 14:22 | RETRACTED — unknown | No — athlete did not know what that figure was |
| 2026-11-05 | Home / terrain | "3–5 h from climbs" | **Hampstead NC, sea level, 5–5.5 h each way** | No — correction. Makes every mountain weekend a 2-night trip and makes descending the acute gap |
| 2026-11-16 | **DNF cause** | Toe → nail → gait → heel → bursitis ended the race | **Quadriceps failure on descents; could not maintain speed.** The cascade happened and cost 7 months, but did not stop the race | No — **the most consequential correction in this file.** Moves descending from risk 4 to risk 1, weakens the charitable reading of the 51% projection, and made the never-progressing eccentric block the plan's central defect |
| 2026-11-16 | Badwater Cape Fear | Looked like a straight substitute for the week-22 50 | **38 of its 51.4 mi are flat beach — it tests ZERO descent.** Still worth doing for a first 50-mile finish, but it cannot be read as evidence the failure mode is fixed. Makes the week-25 Hellbender course rehearsal essential rather than optional | — follows from the correction |
| 2026-11-15 | Bodyweight | unknown | **84 kg / 185 lb**, goal 190 lb as lean mass | — new information. Unblocks the whole nutrition page |
| 2026-11-15 | Week 22 | Self-supported 50 on the Hellbender course | **Heartbreaker declined again** (too close to May); **Badwater Cape Fear 51.4 mi, Bald Head Island, Sat 20 Mar 2027** proposed — same date, ~2 h away. Not yet decided | Yes — athlete's call |
| 2026-11-15 | Intensity distribution | Assumed adequate | **DEFECT: zero hard sessions in 29 weeks.** Raised by the athlete from last year's plateau. Fix proposed on the Tuesday vert session, pending decision | No — design defect |
| 2026-11-05 | Heartbreaker result | "50-miler **finished**" | **DNF at 45 mi in 15h00** | No — the most consequential correction in this file. No 50-mile race has ever been completed, and the feasibility verdict moves from comfortable to marginal |

## Rules

1. **The gate first.** If the energy-availability row is not a clear pass, no training
   recommendation is produced.
2. **Observed, not intended.** Hours come from what happened, not from the plan.
3. **State the derivation for vert.** Indoor and outdoor vertical are measured differently and
   must never be summed without saying how each was derived.
4. **A blank cell is honest; a guessed cell is not.** Downstream they look identical.
