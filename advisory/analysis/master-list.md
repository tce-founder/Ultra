---
title: Master list — open questions and human decisions
type: register
status: active
updated: 2026-09-06
---

# Master list

> The backlog of things **no amount of corpus-building resolves.** Split from
> `docs/build-backlog.md` deliberately: that one is about building the system, this one is about
> what has to be measured and what has to be decided by a person.

## Workstream A — what must be measured

Things the system cannot advise well without, none of which are in the corpus's power to supply.

| # | What | Why it blocks | Status |
| - | ---- | ------------- | ------ |
| A1 | Observed weekly hours over a real 12 weeks | Every plan in `minimum-effective-dose-and-time` is built on observed rather than intended hours, and nothing here has the athlete's data | Open |
| A2 | Session completion rate | The one number that page can be judged by | Open |
| A3 | Current tolerated fuelling rate, measured at race intensity | `gut-training-protocol` starts from a baseline nobody has taken | Open |
| A4 | Weekly vertical with its derivation stated | Indoor and outdoor vertical are not the same measurement | Open |
| A5 | Energy-availability gate — a clear pass or a referral | Runs before every training recommendation | Open |

## Workstream C — decisions no research settles

| # | Decision | Why it is a judgement | Status |
| - | -------- | --------------------- | ------ |
| C1 | Which race, and therefore which demands the whole plan is shaped by | `race-selection` is an empty tag and this is the decision it would serve. Currently unsupported by the corpus | Open |
| C2 | How much of life the block gets | Not a training question. The corpus can say what a given number of hours buys; it cannot say what the hours are worth | Open |
| C3 | Whether to be coached, and by which school | The four lineages disagree substantively — see `advisory/kb/subject/coaching-schools-and-where-they-disagree.md`. Blending them is worse than picking one | Open |
| C4 | The DNF non-negotiable list, and who holds it | Has to be decided rested, and by the athlete rather than by this system | Open |
| C5 | Whether the corpus's calibration machinery is earning its cost | The charter's working thesis, with its falsifier. Counted in the objection register's `evidence-quality` theme against `corpus_gaps` | Open |

## Rules

- A row leaves this list by being **done** or by being **explicitly dropped with a reason**. Rows do
  not expire.
- If this list and `docs/build-backlog.md` disagree about what is outstanding, reconcile them by
  hand and note it here. They have drifted in the upstream repository and there is no mechanism yet
  that prevents it.
