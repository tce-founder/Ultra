# Corpus purpose — the charter

> Read this before deciding what to ingest, what deserves a page, what to promote and what to cut.
> `SCHEMA.md` says what a page must **contain**; this page says whether it should **exist**.
> A corpus question this page cannot settle is a **defect in this page.** Fix it here, rather than
> deciding it privately inside one run where the reasoning dies with the session.

## What this is

The **general reference layer** for an advisory system operating on one athlete's ultrarunning. It
holds methods a node can apply, figures calibrated to a stated population, and the failure record of
the sport — on disk, graded, and readable without a network call.

**This is not a shelf.** A source is here because it changed something, and what it changed is recorded
per source: the page it improved, the page it disputes, or the ground it exposed that nothing here
covers. An entry recording none of those has been read but not absorbed.

It is also **not the training log.** The athlete's own state, figures and judgements live in
`advisory/analysis/`. Nothing personal or medical enters here — this layer is read by every lens on
every run.

## Who it serves

**Graph nodes, not people.** Lenses and grounders read this corpus and quote it into advice an athlete
acts on with their body. Three consequences shape every page:

1. **Retrieval-safe beats complete.** A page that cannot be quoted without acquiring false precision is
   worse than a page that does not exist, because nothing downstream re-reads the source.
2. **A node cannot tell what it does not know.** It reads a corpus page, not a study. Whatever the page
   fails to state — the population, the unit, where the claim gets its standing — is simply not
   available to it, and it will reason on anyway.
3. **The output is executed on a body.** This is the difference from the business-advisory vault this
   schema came from. A wrong recommendation there costs money and can be reversed next quarter. A wrong
   recommendation here costs a season, and in the specific cases of hyponatremia, low energy
   availability and running on a stress fracture, considerably more than a season. The corpus is
   correspondingly more willing to say *ask a professional* and stop.

## The four jobs, in priority order

### 1. Ground the routed lenses so none of them has to improvise

`workflows/lenses.json` declares fifteen lenses and each one reads its bucket here. **A routed lens
with an empty bucket is worse than an absent one** — it does not fail loudly, it improvises, and every
other lens in that run is grounded, so its output looks the same as theirs. This is the corpus's first
duty and it ranks above breadth: coverage of a lens the system actually routes to beats a better page
in a lens it does not.

The lens→tag map in `workflows/golden_queries.json` is what makes this checkable rather than hoped-for.

### 2. Carry enough calibration that a figure can be **refused**

The corpus exists so a lens can decline a number, not only find one. `population` and `unit` are the
two fields that make refusal possible.

This is the job most specific to this domain. Endurance science is built on small samples of
well-trained young men, often in a laboratory, often on a bicycle, and the sport's headline numbers
inherit that shape without carrying it. The useful output of a grounding pass is frequently *"this is
correctly sourced and does not apply here"* — that is the corpus working, not the corpus falling short.

The second half of the same job: **separate what is established from what is merely repeated.**
Ultrarunning has an unusually large body of high-quality coaching experience and an unusually small
body of evidence, and the two are constantly conflated because the experienced claim is the more
confidently stated one. `authority` is the field that keeps them apart, and it is not optional.

### 3. Absorb rather than accumulate

Size is the wrong measure of this corpus. The number worth watching is how many pages an ingest
*improved* — and `disposition` is what makes that countable rather than felt. **Binding at ingest**,
one of three outcomes:

| outcome | what it means |
| ------- | ------------- |
| `sharpened` | it improved a page we hold — name that page and what it added or corrected |
| `counterpoint` | it disagrees with a page we hold — both positions recorded, with their evidence |
| `gap` | it addresses something no page covers — logged as a research lead |

**Countable, therefore falsifiable.** A year of ingests that adds two hundred pages and records not one
`sharpened` is a reading list with a schema on it, and the right response is to say so here rather than
to keep ingesting.

There is a domain-specific trap this job exists to catch. The material available in this sport is
overwhelmingly *introductory*: the same base-building, the same fuelling ladder, the same taper, told
again in a new voice. It is genuinely good and it is genuinely redundant after the third telling. A
source that restates what four pages already hold is not an ingest, whatever its quality.

### 4. Hold the failure record

Most of what a lens needs at a decision point is not what works, it is **what makes people stop** — and
that material is systematically under-published relative to training advice, because finishing is what
gets written about. GI distress, sleep collapse, the hour of hypothermia at 3 a.m., the entirely
correct DNF, low energy availability, the stress fracture that was a niggle in March. Sources carrying
it earn their place at a lower importance bar than the equivalent training framework.

## Scope

**In scope:** training design and periodisation; intensity distribution; strength, durability and
economy; vertical gain and its indoor substitutes; the physiology being trained and how it is measured;
heat, altitude and cold; race fuelling, gut training, hydration and sodium; the daily diet and energy
availability; recovery and sleep; injury, overtraining and return to running; mindset, pain and
attention; motivation, goal-setting and adherence; the athlete's time and competing load; race
selection, preparation, crew, kit, pacing, the night, and the DNF decision. Plus the failure modes that
recur across all of them.

**Out of scope:** anything about this athlete specifically (it belongs in `advisory/analysis/`); any
medical position (this corpus produces questions for a clinician, never answers); general fitness and
health material that neither sharpens a page here nor stands as a credible counterpoint to one; and
anything whose substance is not extractable, which is recorded as a known gap rather than approximated.

**Out of scope for a different reason:** material bought for personal use is marked `ip_class:
licensed` and never reaches anything published.

## What good looks like

A page earns its place if it passes all five:

- **Calibrated.** Every figure states the population it was measured on and the unit it counts.
- **Attributable.** Every figure traces to a source with a URL and a retrieval date; every claim carries
  its `authority` — measured, established, experienced or asserted — and those are **never laundered
  into one another.**
- **Applicable.** A node can act on it: inputs, steps, outputs, and how to tell it is being applied
  wrongly. Not a book report.
- **Connected.** It states what it sharpens, contradicts or depends on, and the other side says so too.
- **Honest about its limits.** Thin samples, population mismatches and unresolved tensions belong in the
  text of the page. A gap somebody wrote down is usable by the next node; the same gap left unstated is
  what a lens walks into without noticing.

## Working thesis (2026-09-06)

**In this sport the binding constraint on good advice is not access to information — it is calibration.
The material is abundant, free, and mostly correct about somebody. What is missing at the point of a
decision is a way to tell whether a given correct thing is correct about *this athlete, this race, this
week*, and nothing in the ordinary channels — a podcast, a blog post, a search result — carries the
population it came from.**

The corpus costs an ingest discipline, a schema, two builders and a verification pass. It is worth that
only if population mismatch is both common and invisible without the tagging.

**What would falsify it.** If grounding notes keep reporting gaps that a plain search would have
closed, while `population` refusals turn out to be rare, then the calibration machinery is ceremony and
the honest finding is that we should fetch at runtime and spend the effort elsewhere. That is a
countable question — `corpus_gaps` on one side, refusals in the grounding notes on the other — and this
charter should be rewritten by whichever way it counts.

**The second thing that would falsify it, and the likelier one.** If the advice that actually changes
outcomes turns out to be almost entirely in the three lenses that need no literature at all —
`time-management`, `motivation-adherence`, `mindset` — then the corpus is well built around the wrong
centre. The counter-check is in the registers, not here: if the action register fills with fuelling and
periodisation actions while the objection register keeps recording that the block did not happen, the
corpus is answering a question the athlete was not failing at.

## History

| Date | Author | Change |
| ---- | ------ | ------ |
| 2026-09-06 | @benelliott | First charter, written with the first corpus rather than after it. Ported from `tce-founder/Anton`, whose equivalent page was written two months into the vault's life and had to correct arguments already settled privately inside runs |
