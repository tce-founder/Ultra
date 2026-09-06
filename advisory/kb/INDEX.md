# Corpus index — human-readable

> `INDEX.json` is the machine index and is **generated** by `workflows/build_index.py`. This file is
> **authored** and exists for a person deciding what to read or what to write next. When they
> disagree, `INDEX.json` is right about what is on disk and this file is right about what it means.

**State at 2026-09-06:** 28 pages · 14 concept · 12 source · 2 entity · orphans none · one-way
`related` none · 9 empty tags, all declared · no starved lenses · 14/14 golden questions grounded.

## Layer 1 — frameworks (`frameworks/`)

Methods a node can apply. Inputs, steps, outputs, and how to tell they are being applied wrongly.

| Page | Answers | Standing |
| ---- | ------- | -------- |
| `polarized-intensity-distribution` | How much of my training should be easy? | `established` — but only the low-intensity-dominance half |
| `periodization-for-ultras` | In what order should the training happen? | `experienced` — coaching convention, no trial exists |
| `strength-training-for-ultrarunners` | Is gym time worth the hours? | `established` for economy, `asserted` for the ultra application |
| `vertical-gain-and-its-substitutes` | Treadmill, stair machine or climbing machine — and what do none of them cover? | `experienced` |
| `carbohydrate-fueling-ladder` | How many grams an hour? | `established` |
| `gut-training-protocol` | How do I raise what I can tolerate? | `established` mechanism, `experienced` schedule |
| `drink-to-thirst` | How much do I drink, and does salt do anything? | `established` |
| `energy-availability-floor` | Am I eating enough to be trained at all? | `established` — **runs as a gate before every training question** |
| `heat-acclimation-protocol` | What can I change about the heat, starting when? | `established` |
| `sleep-and-the-night` | Sleep in training, and the plan for the second night | `established` |
| `pacing-by-effort` | What am I holding constant for fourteen hours? | `experienced` |
| `the-dnf-decision` | Should I stop? | `experienced` |
| `mental-skills-toolkit` | Which of the mental side is trainable? | `established` mechanism, `asserted` at ultra duration |
| `minimum-effective-dose-and-time` | Eight hours a week — enough? | `experienced`, thinly. **Highest leverage, weakest evidence** |

## Layer 2 — benchmarks and bibliography (`benchmarks/`)

Factual extracts with their populations, and the reading queue.

**Evidence pages.** Each carries the figures, the population, the unit trap, and what the figure does
*not* establish.

`gi-distress-and-dnf-figures` · `carbohydrate-120g-mountain-marathon-trial` ·
`polarized-training-review-evidence` · `heat-acclimation-figures` ·
`sleep-in-mountain-ultramarathon-finishers` · `strength-training-running-economy-meta-analyses` ·
`sodium-does-not-prevent-cramping` · `reds-and-low-energy-availability-evidence` ·
`time-crunched-volume-claims`

**Bibliography pages.** The answer to "what should I read, listen to, and search".

| Page | Covers |
| ---- | ------ |
| `ultrarunning-book-canon` | The books, tiered by **which gap in this corpus they would close** rather than by quality. All unread — this is an ingest queue |
| `ultrarunning-podcasts-blogs-and-newsletters` | Podcasts, sites, magazines and coaching organisations, each with what it is reliable for and where its commercial interest lies |
| `where-the-evidence-lives` | The journals, the access routes, and **the eight questions this corpus routes to and cannot ground from any literature found** |

## Layer 3 — subject (`subject/`)

| Page | Covers |
| ---- | ------ |
| `coaching-schools-and-where-they-disagree` | Four lineages — CTS/Koop, Uphill Athlete/Evoke, Maffetone, SWAP/Roche — and the three questions they actually disagree about. Read this before treating two corpus pages' conflict as an error |
| `fueling-brands-and-their-interests` | Who publishes the fuelling content, what they sell, and the one place the commercial position contradicts the evidence |

## What is missing, and how missing it is

Nine tags have no page. All are declared in `workflows/acceptance_floors.json` with a reason, which
is what keeps them loud. Ranked by consequence rather than alphabetically:

1. **`return-to-run`** — the decision an injured athlete gets wrong at the highest cost. The
   `injury-health` lens grounds elsewhere, so nothing fails: it will improvise, and the output will
   read like advice.
2. **`cold-weather`** — hypothermia sits in the DNF page's non-negotiable stop list with no page
   behind it. A rule with no reasoning attached.
3. **`race-selection`** and **`goal-setting`** — the entry points to every other decision.
4. **`aid-station-crew`** — named as high-value inside `pacing-by-effort` and unwritten.
5. **`altitude`**, **`caffeine-supplements`**, **`foot-care`**, **`gear-kit`**.

Beyond the tags, the **eight evidential holes** in `where-the-evidence-lives` are a different kind of
gap: nobody can close those by writing a page, because the studies do not exist.

## Rules for editing this file

- Every new page gets a row here **and** a line in `log.md`.
- Do not restate a count here that `INDEX.json` generates. The state line at the top is the one
  exception and it is regenerated by hand from a `--check` run, which is why it carries its date.
- If this file and `INDEX.json` disagree about what exists, the JSON is right. If they disagree about
  what matters, this file is.
