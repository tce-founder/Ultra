# Wiki schema — ultrarunning advisory corpus

## Domain

This vault covers the decisions an ultrarunner actually faces: how to structure training, how to build
climbing and descending capacity (including on a treadmill and a stair machine when the mountain is not
available), what to eat on a normal Tuesday and what to eat at hour nineteen, how to drink, how to
sleep, how to recover, how to stay motivated across a training block longer than most people's
attention, how to fit any of it around a job, how to prepare for a specific race, how to pace it, and
when to stop.

It exists so advisory workflows can reason from a local, graded, population-tagged corpus instead of
fetching at runtime. It follows the same house schema as `tce-founder/Anton`, with two domain-specific
extensions (`population`, `unit`) that replace that vault's `archetype` and serve the same purpose.

It is a **separate vault**. Same structure, own domain, own taxonomy, own content.

## Conventions

- Filenames lowercase kebab-case, `.md`
- YAML frontmatter on every page
- Double-bracket wikilinks for all internal references — **minimum two outbound per page**
- `related` must be **bidirectional**: adding a link means editing the other page too. This is
  **checked**, not trusted — `build_index.py` reports every one-way entry, because a one-way `related`
  is invisible from the side that was never edited
- Source pages are factual only; interpretation belongs on concept pages
- Bump `updated` on every edit
- Add every new page to `INDEX.md`
- Append every operation to `log.md` — append-only, never rewritten
- A page with fewer than two outbound links, or none inbound, is an **orphan** and is reported by the
  indexer. An orphan is a page nobody will find

## Page types

| Type | Holds | Directory |
| ---- | ----- | --------- |
| `concept` | A reusable method a node can *apply* — inputs, steps, outputs, and how to tell it is being applied wrongly | `frameworks/` |
| `source` | Factual extract from one source: figures, populations, provenance | `benchmarks/` |
| `entity` | A coach, publication, podcast, product or organisation, indexed by reference | `subject/` |
| `comparison` | Two or more methods set against each other, with where they disagree | anywhere |
| `query` | A settled answer to a recurring question, with its sources | `queries/` |

## Frontmatter

**Required on every page**

- `title`
- `created` — YYYY-MM-DD
- `updated` — YYYY-MM-DD
- `type` — source | entity | concept | comparison | query
- `tags` — array; values must come from the taxonomy below
- `sources` — array of paths or URLs the page draws from
- `related` — array of slugs; bidirectional

**Additional on `source` pages**

- `importance` — 1–5. Gates how many concept pages one source may spawn; a 2 does not justify six
- `source_kind` — article | paper | book | report | transcript | podcast | website | bibliography | notes
- `citation_status` — recommended | queued | acquired | read | summarized | rejected
- `reference_role` — foundation | comparison | ancestor | counterpoint | evidence | method | example | skeptic
- `quality_signal` — canonical | peer-reviewed | practitioner | consulting | empirical | anecdotal | skeptical | unknown

**Domain extensions**

- `population` — **required where the page carries a figure.** Who the figure was measured on, in
  enough detail to refuse it. Sex, training status, event, environment, and sample size where stated.

  This is the single most load-bearing field in the vault, and it is worth being explicit about why.
  Endurance science runs on small samples of well-trained young men, frequently in a laboratory,
  frequently on a bicycle because a cycle ergometer is easier to instrument than a mountain. The
  headline numbers of this sport — 120 g/h of carbohydrate, a heat-acclimation timeline, a plasma
  volume percentage — are almost all of that shape. A correctly sourced, correctly transcribed figure
  applied to a different body in a different event is the failure this layer was built to prevent, and
  it passes every other check we run because nothing about it is wrong except who it is about.

  Write it long. A `population` that reads "trained runners" has told a downstream node nothing it did
  not already assume.

- `unit` — **required where the page carries a count.** What is actually being counted. Grams of
  carbohydrate or grams of *glucose*; percent of starters or percent of non-finishers; vertical metres
  climbed or vertical metres of the route; hours of training or hours of *running*. A figure in the
  wrong unit passes every other check on this list.

- `ip_class` — **required on every page.** How the page's content may be used downstream:
  - `public` — distilled from publicly published material: journal articles, open web pages, public
    podcasts, government data. Attribution is sufficient.
  - `licensed` — distilled from copyrighted material held for personal use only: books, purchased
    training plans, paid courses, gated coaching material. May shape reasoning and personal training
    decisions; must **never** reach anything outward-facing — a published post, a coaching product, a
    plan sold or given to another athlete — in any form, including paraphrase.

  **A page's `ip_class` is the most restrictive class of anything in it.** A concept page citing one
  book alongside three open-access reviews is `licensed`.

  The field exists because the internal-only rule is enforced at the **output** boundary, not the input
  one. A node three hops downstream is reading a corpus page, not a book — it cannot tell which page is
  safe to paraphrase from unless the page says so.

- `authority` — **required on every page.** Where the page's main claims get their standing:

  | value | meaning |
  | ----- | ------- |
  | `measured` | computed from this athlete's own training and race data, or from `advisory/model/` |
  | `established` | a finding in the literature or a published dataset |
  | `experienced` | drawn from coaching or racing experience — the athlete's, or a named coach's |
  | `asserted` | our judgement, offered as judgement |

  **These must never be laundered into one another.** A coach's habit written in the voice of a finding
  is the specific failure this field exists to prevent, and it is rife in this domain: a great deal of
  ultrarunning advice is `experienced`, is worth having as `experienced`, and is repeated until it
  sounds `established`. A downstream node cannot detect the substitution, because it reads a corpus
  page rather than the source, so the grammar of the sentence *is* the evidence as far as it can tell.

  This is a **second axis**, not a rename of the VERIFIED / REPORTED / UNVERIFIED grade in the repo
  README. That grade asks *how well is this checked*; `authority` asks *what kind of claim is it*. A
  coaching judgement can be perfectly well attested as a judgement, and a measured figure can be
  unverified. Both are needed and neither substitutes.

  A page's `authority` is the **weakest** standing of anything it asserts, the same rule that governs
  `citation_status` and `ip_class`. Where a page genuinely mixes them, say so per claim in the body —
  the frontmatter field is the floor, not a summary.

- `disposition` — **required on `source` and `concept` pages built from outside material.** A list;
  one or more entries, each naming its target. What this source did *to this corpus*:

  | value | what it must name |
  | ----- | ----------------- |
  | `sharpened` | the page it improved, and what it added or corrected |
  | `counterpoint` | the page it disagrees with — both positions recorded with their evidence |
  | `gap` | what no page covers; becomes a research lead in `corpus_gaps` and the master list |

  Written as `- "sharpened: <slug> — what it added"`. **Drop the target and the field says nothing**,
  so a naked value is counted as malformed rather than accepted.

  **Exempt:** `entity` and `query` pages, and any page distilled from our own training data.

- `ip_restriction` — optional free-text companion to `ip_class: licensed`. `ip_class` says *which*
  class a page is; `ip_restriction` says *what follows from it on this specific page* — where the
  material came from, what it may not reach, and which local hazard a reader is most likely to
  rationalise past. The commonest one in this domain: a training method's *name* may be in wide public
  circulation while the book's actual protocol is not, and the first fact does not license the second.

  **Classifying edge cases.** The dividing line is *how the material was obtained*, not whether it is
  copyrighted. Everything here is somebody's copyright — that is what the distillation-not-reproduction
  rule below already governs, on every page regardless of class. `ip_class: licensed` adds a **second,
  stricter** restriction for material held for personal use. Worked examples:

  | Material | Class | Why |
  | -------- | ----- | --- |
  | Books — Koop, House/Johnston/Jornet, Fitzgerald, Magness, Hutchinson | `licensed` | Bought for personal use. May shape a training decision; may never reach anything published |
  | Open-access journal articles and systematic reviews (PMC, Frontiers, Sports Medicine) | `public` | Published openly |
  | Coaching-company blog posts (CTS, Uphill Athlete, Precision Fuel & Hydration) | `public` | Openly published marketing-adjacent content. Attribute it and note the commercial interest |
  | Public podcast episodes | `public` | Freely broadcast. Reproducing a transcript is barred by the distillation rule, not by this field |
  | A purchased training plan or a paid coaching relationship's material | `licensed` | Bought, and frequently licensed to one athlete by its terms |

## Citation lifecycle

```
recommended → queued → acquired → read → summarized
                                      ↘ rejected
```

`summarized` requires the primary source to have been opened and the figure read directly. **A figure
taken from a secondary while the primary was reachable but unopened is `acquired` at best, and cites
the secondary.** In this domain that rule bites constantly, because the sport's numbers reach the
athlete through blog posts and podcasts that are themselves reporting a study nobody in the chain has
opened. `rejected` is never published as fact — it is recorded as a known gap with its reason.

**A page's `citation_status` is the weakest status of anything in it.** One `acquired` figure among ten
`summarized` ones makes the page `acquired`.

## Tag taxonomy

Values must come from this list. If a needed tag is genuinely absent, record the shortfall rather than
inventing one silently — the taxonomy is extended deliberately, not by drift.

- aerobic-base
- aid-station-crew
- altitude
- best-practices
- bibliography
- body-composition
- caffeine-supplements
- carbohydrate-fueling
- coaching-practice
- cold-weather
- cross-training
- daily-diet
- dnf-decision
- downhill-eccentric
- energy-availability
- evidence-base
- failure-modes
- foot-care
- framework-comparison
- gear-kit
- gi-distress
- goal-setting
- gut-training
- habit-adherence
- heat-adaptation
- hydration
- indoor-climbing-machines
- injury-prevention
- intensity-distribution
- life-load
- long-run
- mindset
- motivation
- night-and-sleep-deprivation
- nutrition
- overtraining
- pacing
- pain-perception
- periodization
- physiology
- plyometrics-durability
- race-prep
- race-selection
- race-strategy
- recovery
- return-to-run
- self-talk
- sleep
- sodium-electrolytes
- speed-economy
- strength-training
- tapering
- threshold
- time-management
- training-load-monitoring
- training-methodology
- treadmill-training
- vertical-gain
- vo2max

### Why the taxonomy is this shape

Three groups of tags exist for reasons that are not obvious from their names, and are recorded here so
a later edit does not quietly merge them.

`treadmill-training` and `indoor-climbing-machines` are separate from `vertical-gain` on purpose. Vert
is the training *demand*; the other two are *substitutes* for it, and the substitution is asymmetric in
a way that matters — a stair machine reproduces the climbing demand tolerably and the descending demand
not at all. Collapsing the three would hide exactly the fact a node needs.

`hydration` and `sodium-electrolytes` are separate because the sport's dominant folk belief joins them,
and the evidence pulls them apart: the trial recorded in [[sodium-does-not-prevent-cramping]] found
sodium intake unrelated to cramping, dehydration and hyponatremia, while over-drinking is the mechanism
of hyponatremia. A single `hydration-and-electrolytes` tag would route a question about drinking to
pages about salt.

`motivation`, `habit-adherence` and `goal-setting` are separate from `mindset`. Mindset is what happens
at hour twenty when it hurts; the other three are what happens at 6 a.m. in February when it does not.
They fail differently, they are fixed differently, and they are the ones that actually decide whether a
training block happens at all.

## Facets

Two dimensions are orthogonal to subject and belong in their own fields rather than in `tags`, where
they would multiply against every subject value:

- `distance` — 50k | 50mi | 100k | 100mi | multiday | backyard | distance-agnostic
- `terrain` — flat | rolling | mountain | technical | road | track | indoor | terrain-agnostic

Both optional; set them where the source has a clear answer. `distance` matters because the advice
inverts somewhere between a 50k and a 100 miler — a 50k is a long race run mostly aerobically, a 100
miler is a fuelling, sleep and decision-making problem with running attached. `terrain` matters because
mountain and flat ultras share a name and very little else.

## Content rules

**Distillation, not reproduction.** Structure, facts, figures and method skeletons in our own words,
with attribution and a link back. Never transcripts, reproduced training plans, or verbatim third-party
prose. At most one short attributed quotation (under 15 words) per page, where the exact wording
genuinely is the fact.

**Licensed material is personal-use only.** A book bought for personal use may inform a training
decision and must never reach anything published, in any form including paraphrase. Enforced at the
output boundary, not the input one.

**Nothing medical is decided here.** This corpus produces *questions for a clinician*, never
positions — on injury, on RED-S and low energy availability, on hyponatremia, on medication, on
anything with a differential diagnosis. A hedged self-diagnosis carries the same risk as a precise
question and none of the value. Pages that touch these areas say what to ask and whom to ask.

**No personal health data in the corpus.** Weight, body composition, blood work, menstrual-cycle data,
injury history and the athlete's own training file do not enter `advisory/kb/`. This is the general
reference layer read by every lens on every run; the athlete's own state lives in
`advisory/analysis/athlete-card.md` and in the private workspace.

**Naming an entity — the test.** An entity page may name a coach, a publication, a podcast or a
product and describe it from public sources. The test is:

> Does this page tell a reader anything they could not learn either from public sources, or by opening
> the pointer it cites?

If no, the page belongs here. If yes, it belongs in the analysis workspace. In practice an entity page
may say what a coaching school teaches and where it disagrees with another; it may **never** carry the
terms of a coaching relationship, an unpublished conversation, or anything a named individual said in
confidence.

**Honest gaps.** Where a source's substance is not extractable — video-only, paywalled, a podcast with
no transcript — record it as a known gap with a pointer to where the substance lives. Never fill it
with plausible invention. This matters more here than in most domains: ultrarunning knowledge is
disproportionately held in podcasts, and a podcast claim nobody has heard is a gap, not a citation.
