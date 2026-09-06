---
title: Ultra — advisory graph system for ultrarunning
type: guide
status: active
author: '@benelliott'
created: 2026-09-06
updated: 2026-09-06
purpose: Operator's map for this repository — what each subsystem holds, which files are generated and which are authored, what to run after changing something, and the rules that are load-bearing rather than stylistic.
---

# Ultra — advisory graph system for ultrarunning

A knowledge corpus, a set of stateful registers and a small analytic path, built so that advice about
training, fuelling, mindset, time and racing can be **grounded and refused** rather than merely
generated.

Sibling of [`tce-founder/Anton`](https://github.com/tce-founder/Anton), which does the same thing for
a startup. Same structure, same builders, own domain, own taxonomy, own content. Read that
repository's README if you want the lineage; you do not need it to use this one.

**Start here, then read [`advisory/kb/purpose.md`](advisory/kb/purpose.md)** — the charter, which
says whether a page should exist. `SCHEMA.md` says what it must contain.

## The problem this is built around

Ultrarunning does not have an information shortage. It has abundant, free, mostly-correct advice —
and almost none of it carries **who it is correct about**.

Endurance research runs on small samples of well-trained young men, frequently in a laboratory,
frequently on a bicycle because a cycle ergometer is easier to instrument than a mountain, in efforts
far shorter than any race in this sport. Coaching knowledge is deep, genuinely valuable, and
systematically stated with more confidence than its evidence supports. Both travel through podcasts
and blog posts that drop the population in exactly one hop.

So the recurring failure is not *finding nothing*. It is **finding confident advice measured on
somebody else**, and nothing downstream can detect that. Two schema fields exist to make it
detectable — `population` and `authority` — and one register exists to check whether they are earning
their cost.

## What this repository deliberately does not hold

Read this before adding a file. [`.gitignore`](.gitignore) states each reason inline so a later edit
does not quietly remove a guardrail.

| Excluded | Where it lives | Why |
| -------- | -------------- | --- |
| **Health data** — blood work, clinical correspondence, cycle tracking, body composition | `advisory/private/` — gitignored | Not in a git repository at any level. The registers may record *that* a referral exists; never what it found |
| **Third-party material held for personal use** — books, purchased plans, paid courses | `advisory/sources/` — gitignored | `ip_class: licensed`. May shape a training decision, may never reach anything outward-facing. *Distillations of it are tracked; the source is not* |
| **Raw training exports** — GPX, FIT, TCX, platform dumps | `advisory/exports/` — gitignored | Binary, enormous, do not diff. The platform is the system of record; derived figures are tracked |
| **Run output** | `advisory/.run-notes/` — gitignored | Working artifacts. Read them, act on them, let them regenerate |

The repository is private, so **assessment and opinion are welcome here** — that is not what the
exclusions are about.

## The map

```
advisory/
  kb/          ← the corpus     — general knowledge, reusable, read by every lens on every run
    purpose.md ← the charter    — whether a page should EXIST. SCHEMA.md says what it must contain
  graph/       ← the index      — GENERATED. Do not hand-edit
  analysis/    ← the registers  — athlete-specific state, stateful across runs
  model/       ← the analytics  — fuelling arithmetic over graded inputs
  private/     ← health data    — gitignored
docs/          ← backlog
workflows/     ← the builders and the declared vocabularies
```

### 1. The corpus — `advisory/kb/`

28 pages of general, reusable knowledge. **It is the general layer** — every lens on every run reads
it, which is exactly why nothing about a specific athlete may land here.

- [`purpose.md`](advisory/kb/purpose.md) — the **charter**. Carries a dated working thesis **with two
  stated falsifiers**, so the corpus can be argued out of rather than only added to.
- [`SCHEMA.md`](advisory/kb/SCHEMA.md) — the page contract. **Read it before authoring a page.** Two
  rules bite most often: minimum two outbound wikilinks, and `related` is **bidirectional** — adding
  a link means editing the other page too, and this is now *checked*.
- [`INDEX.md`](advisory/kb/INDEX.md) — the human index, including what is missing and how missing.
- [`log.md`](advisory/kb/log.md) — append-only operation log. Never rewritten, including when an
  entry turns out to be wrong; the retraction goes *below* it.
- `frameworks/` · `benchmarks/` · `subject/` — layers 1, 2 and 3.

Four frontmatter fields carry real consequence rather than being metadata hygiene:

- **`population`** — required wherever the page carries a figure, and the most load-bearing field in
  the vault. Who the figure was measured on, in enough detail to **refuse** it. Write it long: a
  `population` that reads "trained runners" has told a downstream node nothing.
- **`authority`** (`measured` | `established` | `experienced` | `asserted`) — where a claim gets its
  *standing*, as a second axis from how well it is *checked*. **These are never laundered into one
  another.** This is the field that keeps the sport's excellent coaching experience from being read
  as research, which is the substitution a downstream node cannot detect: it reads a corpus page, not
  the source, so the grammar of the sentence *is* the evidence as far as it can tell.
- **`ip_class`** (`public` | `licensed`) — required on every page. A `licensed` page may inform a
  personal training decision and **may not be paraphrased into anything outward-facing**. Enforced at
  the output boundary, not the input one, which is why the marker has to be on the page.
- **`disposition`** (`sharpened` | `counterpoint` | `gap`, each naming a target) — what a source did
  *to the corpus*. It makes charter job 3 countable: at first build, **19 sharpened, 8 counterpoint,
  21 gap.** A year of ingests that adds two hundred pages and records no sharpening is a reading list
  with a schema on it.

### 2. The index and dependency graph — `advisory/kb/INDEX.json`, `advisory/graph/edges.json`

**Both are generated. Do not hand-edit either.** Produced by
[`build_index.py`](workflows/build_index.py) and [`build_graph.py`](workflows/build_graph.py), which
are deterministic and assert their own totals reconcile before writing.

Indexing is mechanical, so it is code. Judgment — which gaps the corpus has — stays with the agent
and is preserved across rebuilds. The rule the upstream repository learned the hard way and this one
inherits: **an absent key and an empty list are different failures, and only one of them is
visible.** Every taxonomy key is emitted whether or not it has members.

The graph answers the question that matters when a claim turns out to be wrong: **what depends on
it?** Six claims are declared — the carbohydrate ceiling, sodium-prevents-cramp, GI-as-leading-DNF,
polarised superiority, indoor-vert equivalence, and the minimum effective dose. They are the
sport's load-bearing numbers: quoted far more often than sourced, and each one moves a training plan
and a race plan simultaneously.

```
python3 workflows/build_graph.py --impact claim:sodium
```

Structural edges (exact) are kept separate from claim edges (lexical) and are never merged in a
count.

### 3. The registers — `advisory/analysis/`

Athlete-specific and **stateful across runs** — a run updates them rather than replacing them.

| File | Holds |
| ---- | ----- |
| `athlete-card.md` | Current position. **Derived, not asked.** Later runs report *drift* rather than re-interviewing |
| `source-queue.md` | **The ingest schedule** — what to read next, in what order, and what each one closes. The one register that ships populated |
| `action-register.md` | Every advised action, with an owner and what blocks it. Seeded from the plan the athlete already has |
| `objection-register.md` | Objections, theme-grouped, convergence-marked. Objections attach to **decisions, never to the athlete** |
| `predictions.md` | Prediction log. A wrong prediction stays visible, or the confidence on the next one means nothing |
| `cadence-log.md` | **Append-only.** Carries the no-action streak — the only cross-run state the loop has, so a rewritten line silently resets it |
| `master-list.md` | What must be measured, and the calls no amount of building resolves |

Every register except the source queue ships **empty**. Seeding them with plausible example rows
would put invented content in the one place reserved for things that actually happened.

### 4. The analytic path — `advisory/model/`

Python, not prose. `Input` binds **value + unit + population + source + grade**, so a figure cannot be
quoted while its caveat is left behind, and derived figures inherit the weakest grade.

**[`README.md`](advisory/model/README.md) has a "Known weaknesses — read before citing anything"
section. Read it before citing anything.** It includes one thing the module deliberately does *not*
do: there is no fluid model, because a millilitres-per-hour number generated by a program is exactly
the scheduled-drinking behaviour identified as the mechanism of exercise-associated hyponatremia.

### 5. The workflows — `workflows/`

| File | Does |
| ---- | ---- |
| `build_index.py` | Rebuilds `INDEX.json`. `--check` also asserts routing, `related` reciprocity, the golden set and the floors |
| `build_graph.py` | Rebuilds `edges.json`. `--impact CLAIM` walks dependencies backwards |
| `lenses.json` | **Authored.** The fifteen lenses. The lens vocabulary's single owner |
| `golden_queries.json` | **Authored.** The lens→tag map plus 14 grounding questions resolved deterministically against `INDEX.json` |
| `acceptance_floors.json` | **Authored.** The ratchet the builder checks against |

## What to run after you change something

| You changed | Run | Why |
| ----------- | --- | --- |
| Any page under `advisory/kb/` | `python3 workflows/build_index.py --today $(date +%F)` then `python3 workflows/build_graph.py` | Both indexes are generated. Editing a page without rebuilding leaves retrieval stale, and nothing warns you |
| Added a page | The above, **plus** a row in `INDEX.md`, **plus** a line in `log.md`, **plus** reciprocal `related` entries on every page you linked | The reciprocity is checked and floored at zero, so a one-way link now fails the build rather than orphaning a page silently |
| Anything, before committing | `python3 workflows/build_index.py --check` | Exits non-zero on inconsistency. Reports orphans, empty tags and unclassified pages as **errors**, not warnings |
| A lens in `lenses.json`, or a tag in `SCHEMA.md` | The same `--check` — expect it to fail until you edit [`golden_queries.json`](workflows/golden_queries.json) | Lens names and tag names are **two different vocabularies**. The map is declared and checked in both directions: a new lens with no mapping is an error, and so is a mapped lens that no longer exists |
| A register | Nothing mechanical — check whether `docs/build-backlog.md` or `master-list.md` now disagrees with disk | Reconciliation is manual until G2 exists |

A healthy `--check` reports: **28 pages · orphans none · 0 one-way related · 9 empty tags, all
declared · no starved lenses · 14/14 golden questions grounded · totals reconcile, routing declared,
floors held.**

Two authored files make that line mean something:

- [`golden_queries.json`](workflows/golden_queries.json) — the **lens→tag map** plus 14 grounding
  questions. It measures *reachability*, never answer quality.
- [`acceptance_floors.json`](workflows/acceptance_floors.json) — the **ratchet**. Worse than a floor
  fails; better is reported as *"floor can drop"* for a human to commit, because auto-tightening lets
  one lucky run lock in a number nobody chose.

**The nine empty tags are listed, with a reason each, in the floors file** — not counted here. An
empty tag not on that list is an error.

The distinction that matters is not an empty tag but a **starved lens** — one whose *every* mapped
tag is empty, so it has no reachable page at all. Unlike an empty tag this never surfaces at runtime:
the lens does not fail, it improvises, and its note reads exactly like a grounded one. **At first
build there are none**, which was a deliberate constraint on which pages got written first.

## Rules that are load-bearing

Not style.

1. **Nothing athlete-specific enters `advisory/kb/`.** The corpus is the general layer read by every
   lens. Health data does not enter the registers either.
2. **Grade everything** — VERIFIED (traced to a primary that was opened) / REPORTED (stated, not
   checked) / UNVERIFIED (assumed or modelled). Something said confidently on a podcast is not
   thereby verified.
3. **`authority` and grade are different axes and are never laundered into one another.** Coaching
   experience is valuable *as* coaching experience.
4. **Never invent to fill a shape.** A routed lens with an empty corpus bucket is **worse than an
   absent one** — it does not fail loudly, it improvises.
5. **Medical, and this is the rule that most distinguishes this repository from its sibling: this
   system produces questions for a clinician, never positions.** Injury, RED-S and low energy
   availability, hyponatremia, anything with a differential diagnosis. A hedged self-diagnosis
   carries the same risk as a precise question and none of the value. The energy-availability gate
   runs *before* every training recommendation, not alongside them.
6. **This system advises. It does nothing.** No entry made, no plan started, no supplement bought, no
   session performed. Every step is emitted for a human to execute on their own body, which is the
   reason the bar here is higher than in the sibling repository: a wrong recommendation there costs
   money and reverses next quarter.

## The honest state of this repository

Worth stating plainly, because everything above describes machinery and machinery is easy to mistake
for knowledge.

**Not one primary source has been read in full.** Every corpus page is `citation_status: acquired` or
weaker — built from open-access abstracts and from secondary reporting, some of it published by
organisations with a commercial interest in the conclusion. The book canon is entirely
`recommended`: a dozen-plus titles, none opened.

**The advisory graph does not exist yet** (`docs/build-backlog.md`, G1). The corpus, the index, the
routing map and the floors all serve a graph that has not been written, which means this is currently
a well-checked library rather than an advisory system.

Both are recorded in [`advisory/kb/log.md`](advisory/kb/log.md) rather than smoothed over. The whole
schema rests on the difference between `acquired` and `summarized`, and a vault that blurred it on
day one would never recover the distinction.

[`advisory/analysis/source-queue.md`](advisory/analysis/source-queue.md) is the plan for fixing the
first of those. Tier 0 is three documents, two of them free.

## History

| Date | Author | Change |
| ---- | ------ | ------ |
| 2026-09-06 | @benelliott | First build. Structure, schema and both builders ported from `tce-founder/Anton`; `archetype` replaced by `population`, lens names moved into an authored `lenses.json`, `related` reciprocity added to the checker, and a medical boundary added to the schema |
