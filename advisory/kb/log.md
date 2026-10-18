# Corpus operation log

**Append-only.** Every ingest, fix and correction gets a line. Entries are never rewritten,
including when one turns out to be wrong — the retraction goes *below* it, with its own date. A log
that can be edited is a log that records what somebody currently believes, which is what the corpus
pages are for.

Format: `## YYYY-MM-DD — what` followed by what changed and what it cost.

---

## 2026-09-06 — vault created, 28 pages, first build

**What.** First corpus for the ultrarunning advisory system, created alongside the schema rather
than after it. Ported the structure, the schema and both deterministic builders from
`tce-founder/Anton`.

**Pages written (28).** 14 concept, 12 source, 2 entity. Coverage chosen so that **every one of the
fifteen lenses in `workflows/lenses.json` has at least one reachable page** — that constraint, not
subject interest, decided which pages got written first. It is job 1 of the charter and it is the
only thing that cannot be fixed later without the intervening runs being quietly wrong.

**What was changed from the upstream structure, and why:**

1. **`archetype` → `population`.** Same job — the field that lets a figure be refused — but the
   refusal criterion here is *who the figure was measured on* rather than *what company shape it
   came from*. Endurance research runs on small samples of well-trained young men, often on cycle
   ergometers, in efforts far shorter than an ultra, and none of that travels in the number.
2. **Lens names read from `workflows/lenses.json`, not from a graph.** Upstream parses them out of
   the JavaScript that routes them, because there the graph is their owner. No graph is written here
   yet, and a stub JS file that looked runnable would let the routing check pass against a fiction.
3. **`related` reciprocity is now checked.** Upstream declares it bidirectional in the schema and
   trusts it. `build_index.py` here reports `nonreciprocal_related` and `dangling_related`, both
   floored at zero. A one-way entry is invisible from the side that was never edited, which is
   exactly the class of failure a declared convention does not catch.
4. **A medical boundary added to the schema.** This corpus produces questions for a clinician and
   never positions — on injury, RED-S, hyponatremia, anything with a differential. Three pages carry
   an explicit boundary note. The upstream equivalent covers legal, tax and insurance; the reasoning
   is identical and the stakes here are not reversible next quarter.

**First build result.** 28 pages · orphans none · one-way `related` none · dangling none ·
unclassified IP none · untyped none · `authority` and `disposition` present on every page in scope ·
no starved lenses · 14/14 golden questions grounded · totals reconcile.

Floors committed in `workflows/acceptance_floors.json` at those measured values. Note that the
`missing_authority` and `missing_disposition` floors start at **zero** rather than at the full
corpus size as they did upstream. That is a consequence of the schema existing before the pages did,
not of greater discipline, and it means there is no backfill credit to spend: those floors can only
be defended.

**Nine empty tags**, each declared with a reason. Ranked by consequence in `INDEX.md`;
`return-to-run` is the one that matters most, because the `injury-health` lens grounds via four
other tags and will therefore improvise rather than fail.

**Honest state of the citations.** Every page in this corpus is `citation_status: acquired` or
weaker. **Not one primary source has been read in full.** The evidence pages are built from
open-access abstracts and from secondary reporting, several pieces of it published by organisations
with a commercial interest in the conclusion. The book canon is entirely `recommended` — twelve-plus
titles, none opened. This is recorded here rather than smoothed over because the whole schema is
built on the difference between `acquired` and `summarized`, and a vault that blurred that on its
first day would never recover the distinction.

**Disposition tally at first build:** 19 `sharpened`, 8 `counterpoint`, 21 `gap`. The gap count
exceeding the sharpened count is the expected shape for a first build and is the number to watch:
per the charter, a corpus that keeps recording gaps and never records sharpening is a reading list
with a schema on it.

**Cost.** One research pass (fourteen web searches), one authoring pass, one build. No source
purchased, no paper downloaded, no book opened.

---

## 2026-09-06 — registers seeded, empty by design

**What.** `advisory/analysis/` created with the five registers and the source queue, all seeded
with structure and **no athlete data**.

**Why empty.** The registers are stateful across runs and their value is entirely in the state they
accumulate. Seeding them with plausible-looking example rows would put invented content in the one
place in this repository that is supposed to hold only things that actually happened. The first real
row goes in when there is a first real answer.

`source-queue.md` is the exception and is populated, because it is a queue of things to read rather
than a record of things that happened.

---

## 2026-10-18 — Hellbender race page; corpus 28 -> 29; three empty tags closed

**What.** Added `subject/hellbender-100.md` — the target race as an entity page: course figures,
cutoffs, the four demands in the order they bite, and the course-specific failure chain.

**Why it earns a corpus page rather than a register entry.** It passes the SCHEMA naming test:
everything on it is public, and it tells a reader nothing they could not get from the official
site. The athlete's relationship to the race is in `advisory/analysis/`; the race itself is
general reference.

**Three empty tags closed** — `race-selection`, `aid-station-crew`, `gear-kit` — and the rows
removed from `allowed_empty_lenses`. Worth recording *how*: not by writing three general pages,
but by writing one page about a specific race, which forced concrete answers where the general
versions had been deferring them. Possibly a pattern; one instance is not evidence.

**Floors raised.** `pages_min` 28 -> 29, committed by hand after `--check` reported the slack. The
ratchet behaved exactly as designed: it reported the improvement and declined to tighten itself.

**`disposition` is absent on this page and that is correct** — `entity` pages are exempt under
SCHEMA.md, because a Layer-3 entity page absorbs nothing.

**Citation honesty.** Every figure on the page is `acquired`, and the page says so prominently,
because published sources genuinely disagree: official distance 102.3 mi against listings saying
100; gain between 20,000 and 21,540 ft; a high point given as both 5,408 and 6,684 ft, which
cannot both be right. The official cutoff page may also be stale. The page carries the
disagreement rather than resolving it by picking a number, and names re-derivation before the
taper as the action.

---

## 2026-10-18 — training plan toolchain (registers, not corpus)

**What.** `workflows/plan/build_plan.py` generates a 29-week plan to Hellbender from one
definition, emitting the document, a Google Calendar `.ics`, and structured Garmin workouts
together so they cannot drift. `push_garmin.py` uploads them.

**Nothing here touched the corpus**, which is the point of the split: the plan is this athlete's
and lives in `advisory/analysis/plan/`; what it is built *from* is general and stays in `kb/`.

**The validator earned its place on the first run.** It rejected the first draft for leaving no
full rest day in any week from 9 onward — the weights gave Monday a small recovery run in two
phases. For an athlete with 6-7 available days coming off under 20 mi/week, that is precisely the
defect that matters, and it was invisible in the generated document. A second check (the ramp
ceiling) produced six false failures by comparing build weeks against down weeks; fixed to compare
against the previous build week, which is the trend line it was always meant to police.
