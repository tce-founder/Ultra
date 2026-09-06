---
title: GI distress and DNF — the withdrawal figures, and what unit each of them is actually in
created: 2026-09-06
updated: 2026-09-06
type: source
tags:
  - gi-distress
  - dnf-decision
  - failure-modes
  - evidence-base
sources:
  - https://trainright.com/gi-distress-ultrarunning-dnf/
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8665950/
  - https://trailhead.ultrasignup.com/training-nutrition/utmb-dnf-data/
related:
  - carbohydrate-fueling-ladder
  - gut-training-protocol
  - pacing-by-effort
  - the-dnf-decision
  - where-the-evidence-lives
importance: 5
source_kind: article
citation_status: acquired
reference_role: evidence
quality_signal: practitioner
authority: established
disposition:
  - "sharpened: carbohydrate-fueling-ladder — supplies the counterweight to maximal fuelling rates, which that page needed and did not have on its own"
  - "gap: no source found reports DNF reasons for the whole field of any race as a fraction of STARTERS, only of non-finishers. The denominator that would make these numbers comparable across races does not exist in anything consulted"
population: >-
  Two named US 100-mile races (Western States and Vermont) for the 23% figure, and a separate study
  of 100-mile runners for the 35.6% figure. Field is predominantly North American, predominantly
  male, at hot summer 100-milers — Western States is specifically a hot race and heat is a direct
  driver of GI symptoms, so this is close to a worst case rather than a representative one. The
  30-90% symptom-prevalence range spans endurance athletes across sports and event lengths. The
  anxiety correlation is from a 56 km race and is a correlation.
unit: >-
  READ THIS BEFORE QUOTING ANY NUMBER HERE. The 23% is the share of WITHDRAWING RUNNERS whose stated
  PRIMARY reason was nausea and vomiting — not the share of starters, and not a cause established by
  anything other than self-report. The 35.6% is the share of NON-FINISHERS who said GI symptoms
  CONTRIBUTED to withdrawal, which is a broader question with a lower bar and a different
  denominator; the two are not comparable and must never be presented as a range. The 30-90% is
  symptom PREVALENCE among competitors, most of whom finish — having symptoms and stopping because
  of them are different events.
ip_class: public
---

# GI distress and DNF

## The figures

| Figure | What it counts | Where from |
| ------ | -------------- | ---------- |
| **23%** | Share of *withdrawing* runners whose stated **primary** reason was nausea and vomiting | Western States and Vermont 100-mile study, as reported by CTS |
| **35.6%** | Share of *non-finishers* who said GI symptoms **contributed** to withdrawal | Separate 100-mile study, as reported |
| **30–90%** | Prevalence of GI symptoms among endurance athletes during competition, rising with event duration | Range reported across the endurance literature |

## The claim built on them

That **GI distress is the leading cause of ultramarathon DNF** — more than injury, more than lack of
fitness. This is the claim tracked as `claim:gi-leading-dnf` in `advisory/graph/edges.json`, and it
is load-bearing: if true, gut training ranks above most of the training plan.

## What the figures support, and what they do not

**Supported.** Among people who stop in a 100-miler, GI symptoms are the most commonly *stated*
primary reason, and a larger share again name them as contributing. That is a robust and repeatedly
observed pattern.

**Not supported.** That GI distress *causes* those withdrawals in any deeper sense. Self-reported
primary reason is what the runner noticed last. The causal chain in most accounts runs: went out too
hard → gut blood flow fell → nausea → intake stopped → energy deficit → stopped. The runner reports
the nausea because that is where it hurt. On that reading the primary cause is pacing, and the
proximate one is GI — see [[pacing-by-effort]], which traces the chain, and [[the-dnf-decision]],
which is where it terminates.

**Also not supported.** Any comparison between the 23% and 35.6% figures. Different questions,
different denominators, different studies. Quoting them as "23–36%" would be wrong in a way nobody
downstream could detect, which is why the `unit` field on this page is longer than the table.

## Provenance — read before citing

Both headline figures reached this page through **secondary reporting** by a coaching company
(CTS/TrainRight), which has a commercial interest in the conclusion that fuelling and gut training
are decisive. The underlying studies were reachable and were **not opened**. That fixes
`citation_status: acquired` and means:

- These figures may inform an internal training decision.
- They may **not** be quoted outward with a study attribution, because the study was not read and the
  reporting may have compressed the population or the question.
- Anyone promoting this page to `summarized` must open the primary studies, confirm the
  denominators, and rewrite the `unit` field from the papers rather than from the reporting.

The remaining source, the anxiety/GI correlation from a 56 km race, is open-access and was read at
abstract level only. It supports the pre-race-routine recommendation in
[[gut-training-protocol]] weakly and is not evidence of a causal path.

## What would change the conclusion

A field-wide DNF reason breakdown with starters as the denominator, or any prospective study in
which fuelling rate was manipulated and DNF rate observed. Neither exists in anything consulted, and
that absence is recorded in [[where-the-evidence-lives]] as one of the sport's larger evidential
holes.
