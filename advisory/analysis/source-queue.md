---
title: Source queue — what to read next, in what order, and what each one closes
type: register
status: active
updated: 2026-09-06
---

# Source queue

> The **ingest queue**, ordered by what each source would close in the corpus — not by quality and
> not by interest. A source that closes nothing named here is a source to enjoy, not to ingest.
> That ordering is job 3 of `advisory/kb/purpose.md` and it is the only defence this repository has
> against becoming a well-tagged reading list.
>
> The catalogue lives in the corpus: [[ultrarunning-book-canon]],
> [[ultrarunning-podcasts-blogs-and-newsletters]] and [[where-the-evidence-lives]]. **This page is
> the schedule.** When a source is ingested, its row moves to Done with a date and the page it
> produced.

## Status of every citation in this corpus, stated plainly

**Nothing has been read in full.** Every corpus page is `acquired` or weaker. Everything below is
therefore a real queue rather than a formality, and the top three rows are the difference between a
corpus that reports what other people say and one that has checked.

## Tier 0 — read these before the corpus is used for anything consequential

| # | Source | Kind | Closes | Why it is tier 0 |
| - | ------ | ---- | ------ | ---------------- |
| S-01 | **IOC consensus statement on REDs (2023)**, *Br J Sports Med* | Consensus | `reds-and-low-energy-availability-evidence` | The corpus's health **gate** currently knows only that this document exists. The screening and referral guidance is *in* it. Free, findable, and the single highest-value hour available |
| S-02 | **3rd International EAH Consensus (2015)** + the 2017 *Frontiers in Medicine* update | Consensus | `sodium-does-not-prevent-cramping`, `drink-to-thirst` | The one topic here where acting on the popular belief creates the harm. Both open access |
| S-03 | **Training Essentials for Ultrarunning, 2nd ed.** — Koop, Rutberg, Malcolm | Book (licensed) | `periodization-for-ultras` and most of layer 1 | Periodisation is currently assembled from coaching web pages with no primary text behind it. This is the sport's reference training text and its absence is the corpus's largest structural weakness |

## Tier 1 — the primary papers behind figures already quoted

Each of these is already cited by a corpus page at `acquired`. Reading it moves that page to
`summarized` and lets its `unit` and `population` fields be rewritten from the source instead of
from the reporting. **Ordered by how badly the reporting could have distorted the figure.**

| # | Source | Moves to `summarized` | The specific thing to check |
| - | ------ | --------------------- | --------------------------- |
| S-04 | Hoffman & Stuempfle, sodium intake in a hot ultramarathon (PMC4688305) | `sodium-does-not-prevent-cramping` | Whether high sweat-sodium individuals were identified separately. This is the whole commercial counter-argument and the null result may simply not address it |
| S-05 | Viribay et al., 120 g/h during a mountain marathon (PMC7284742) | `carbohydrate-120g-mountain-marathon-trial` | The exact damage markers, the race duration, and what "previously gut-trained" meant in the protocol. The number is quoted as a performance result and the outcome was a 24 h recovery marker |
| S-06 | The Western States / Vermont DNF study behind the 23% figure | `gi-distress-and-dnf-figures` | The denominator, and whether "primary reason" was self-reported. Currently reached only through a coaching company's reporting |
| S-07 | Sleep and ultramarathon, 1,154 finishers (*Sports Med Open*, PMC11001838) | `sleep-in-mountain-ultramarathon-finishers` | Whether "recovered wakefulness within two days" is self-reported subjective wakefulness. This corpus assumes it is; if wrong, a recommendation changes |
| S-08 | Polarised TID meta-analysis (*Sports Medicine*, s40279-024-02034-z) | `polarized-training-review-evidence` | Whether the included studies report distribution by **time** or by **session**. Decides whether the corpus's "80%" and the sport's "80%" are the same quantity |
| S-09 | Strength training and running economy meta-analysis (s40279-023-01978-y) | `strength-training-running-economy-meta-analyses` | The test speeds. The speed-dependence finding is what decides whether any of it transfers to ultra pace |
| S-10 | Heat acclimation: the five-day and nine-day protocols (PMC6843002, PMC6532023) | `heat-acclimation-figures` | That the 7.3% is a percentage of **plasma** volume, and the exact female protocol |

## Tier 2 — books that close a named gap

All `ip_class: licensed` once distilled: personal use, never outward-facing, not even paraphrased.

| # | Source | Closes | Note |
| - | ------ | ------ | ---- |
| S-11 | **Training for the Uphill Athlete** — House, Johnston, Jornet | `vertical-gain-and-its-substitutes`; the aerobic-base side of `coaching-schools-and-where-they-disagree` | Read *after* S-03 so the two positions are read in the order the corpus argues them |
| S-12 | **The Happy Runner** — David and Megan Roche | `goal-setting` (empty), and the thin `motivation-adherence` lens | The lens with the highest leverage and the least corpus. Also the cheapest gap to close |
| S-13 | **Endure** — Alex Hutchinson | `mental-skills-toolkit`, `pain-perception` | Currently carried entirely at second hand |
| S-14 | **Do Hard Things** — Steve Magness | `mindset` | The argument against toughness-as-trait, which this corpus already leans on without a source |
| S-15 | **80/20 Running** — Matt Fitzgerald | `polarized-intensity-distribution` | Read to know what the popular claim actually says before continuing to argue with it |
| S-16 | **Lore of Running** — Tim Noakes | `physiology` depth | Reference rather than a read-through |
| S-17 | **Relentless Forward Progress** — Bryon Powell | `race-prep`, `aid-station-crew`, `gear-kit` | Practical rather than theoretical, and three empty tags is a good return. Bibliographic details unverified |

## Tier 3 — the empty tags, and where their material actually lives

These need writing more than they need reading. Ranked by consequence, matching `INDEX.md`.

| # | Tag | Where the material is | Note |
| - | --- | --------------------- | ---- |
| S-18 | `return-to-run` | Sports-medicine literature; physiotherapy return-to-run criteria | **Highest-consequence empty tag.** The page must be built around *criteria and referral*, not around a protocol — this is inside the medical boundary |
| S-19 | `cold-weather` | Wilderness medicine; hypothermia management | The DNF page's stop list currently cites a rule with no reasoning behind it |
| S-20 | `race-selection`, `goal-setting` | Practitioner and coaching material; S-12 | Entry points to every other decision |
| S-21 | `aid-station-crew` | Practitioner only — iRunFar, crew guides, S-17 | Named as high-value inside `pacing-by-effort` |
| S-22 | `altitude` | The same physiology journals as heat; well covered in the literature | Straightforward |
| S-23 | `caffeine-supplements` | IOC supplement consensus; the caffeine literature is unusually good | Purely an effort gap |
| S-24 | `foot-care` | Practitioner only; ultrarunning medical-tent write-ups | Little literature, high race impact |
| S-25 | `gear-kit` | Deliberately last. Any page must be about **selection method**, not products | Most commercially captured content in the sport |

## Tier 4 — the audio extraction project

| # | Source | Note |
| - | ------ | ---- |
| S-26 | **Science of Ultra** — ~150 episodes, researcher interviews, **host no longer posting** | A *bounded* corpus. The best audio ingest available precisely because it is finished: it can be completed rather than subscribed to |
| S-27 | **KoopCast** — training science, research guests | Ongoing. Ingest by topic against a named gap, never by episode |
| S-28 | **Some Work, All Play** — the Roches | Ongoing. Best source for the adherence lens |
| S-29 | **Freetrail** — athlete interviews | `reference_role: example`. Carries what racing is like, not method |

**The rule for all of tier 4:** a podcast claim nobody has heard is a gap, not a citation. An episode
listed and not listened to grounds nothing.

## Open leads

| # | Lead | Note |
| - | ---- | ---- |
| L-01 | **Newsletters and Substacks** | Not properly surveyed in the 2026-09-06 research pass. The sport's writing has partly migrated here and this corpus has no map of it |
| L-02 | **Platform training data** | Holes 1 and 4 in [[where-the-evidence-lives]] — volume versus outcome, and DNF reasons over starters — are closable by someone with access to a registration or training platform and no laboratory at all. Recorded because it is the only research agenda in this repository that is actually actionable |
| L-03 | **Sex differences across the corpus** | The one sex-specific heat study complicated the male finding rather than confirming it. Nothing here checks whether that pattern holds elsewhere, and the `population` field makes it checkable |

## Done

*Nothing yet. First entry goes here with its date and the page it produced.*
