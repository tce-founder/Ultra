---
title: Build backlog — what is built and what is not
type: guide
status: active
updated: 2026-09-06
---

# Build backlog

> About **building the system**. What has to be *measured* and what has to be *decided* is in
> `advisory/analysis/master-list.md`, and the two are deliberately separate: this file carries no
> athlete data, so it can be read and edited without opening the private half.

## Built (2026-09-06)

| # | Thing | State |
| - | ----- | ----- |
| B1 | Corpus schema, charter and taxonomy — `advisory/kb/SCHEMA.md`, `purpose.md` | Done. 59 tags, `population`/`unit`/`ip_class`/`authority`/`disposition` |
| B2 | Seed corpus, 28 pages | Done. Every one of the 15 lenses has at least one reachable page |
| B3 | Deterministic index builder with `--check` | Done. Adds a `related` reciprocity check the upstream version does not have |
| B4 | Dependency and claim graph, with `--impact` | Done. Six declared claims |
| B5 | Lens declaration — `workflows/lenses.json` | Done. 15 lenses |
| B6 | Routing ratchet — `golden_queries.json` | Done. 14 questions, all grounded |
| B7 | Acceptance floors | Done. Measured at first build; nothing starts with backfill credit |
| B8 | Registers | Structure only, empty by design |
| B9 | Source queue | Done and populated — `advisory/analysis/source-queue.md` |
| B10 | Fuelling model with graded inputs | Done, runnable |

## Not built — ranked by what it unblocks

### G1 — The advisory graph itself

**The largest missing piece.** `workflows/lenses.json` declares fifteen lenses and nothing reads
them. The corpus, the index, the routing map and the floors all exist to serve a graph that does not
exist yet, which means the whole system is currently a well-checked library.

Upstream (`tce-founder/Anton`) has one — `startup-advisor.js`, a state → route → ground → lenses →
check → options → panel → harden → memo pipeline. Porting its shape is the obvious path, and the two
things that must change are worth naming now:

- **The health gate runs first**, before routing. An athlete below the energy-availability floor gets
  a referral and no training advice at all. That is a hard precedence rule, not a lens.
- **The medical boundary is enforced at the output node**, not hoped for in the prompts.

### G2 — The review loop

The cadence-log register exists and nothing writes to it. Needs: read the registers, report what
moved, propose **one** action from the plan that already exists, and stop when the no-action streak
reaches three. Manual invocation only — automating it before it proves useful is how it becomes
wallpaper.

### G3 — Ingest pipeline

Currently a person writes pages by hand. Upstream has plan → extract → distill → verify → fan-out →
index, with the verify node failing a bundle whose `disposition` names no target. The corpus rules
that make ingest checkable are already in place here; the pipeline is not.

**Blocked on nothing.** This is the piece that would let tier 0 of the source queue actually get read.

### G4 — Training-load model

`advisory/model/` holds fuelling arithmetic only. A load model — weekly hours, vertical with its
derivation, session completion rate, and the drift the athlete card wants — is the other half.

Deliberately not started, for a reason worth recording: **load modelling is where this kind of system
most easily produces false precision.** A number computed from a heart-rate stream feels measured and
is frequently an artefact. Any model here has to output its grade, and if it cannot, it should not
exist.

### G5 — The nine empty tags

Tracked in `acceptance_floors.json` with a reason each, and scheduled in tier 3 of the source queue.
`return-to-run` first: it is the decision an injured athlete gets wrong at the highest cost, and its
lens grounds via four other tags, so nothing fails — it will improvise.

### G6 — Shareable-output check

Upstream has a script that scans a draft for anything derived from `ip_class: licensed` material
before it goes outward. Nothing here does that yet. Currently zero pages are `licensed`, so the risk
is zero — **and it becomes non-zero the moment the first book in the source queue is read**, which is
tier 0. Build it before S-03, not after.

## Two things deliberately not on this list

**A training-plan generator.** Tempting, and it would produce plausible plans immediately. It is
excluded because the corpus's own evidence says the plan is not the binding constraint — adherence,
fuelling and pacing are — and a generator would make the system feel complete while answering the
question the athlete was not failing at. See the second falsifier in `advisory/kb/purpose.md`.

**Wearable and platform integrations.** Not until G4 exists and can state a grade. Otherwise the
system acquires a large volume of data it cannot say anything honest about.

## History

| Date | Author | Change |
| ---- | ------ | ------ |
| 2026-09-06 | @benelliott | First backlog, written with the first build |
