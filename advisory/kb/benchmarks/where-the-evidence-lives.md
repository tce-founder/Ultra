---
title: Where the evidence lives — the journals, the access routes, and the eight holes this corpus cannot fill
created: 2026-09-06
updated: 2026-09-06
type: source
tags:
  - bibliography
  - evidence-base
  - physiology
sources:
  - https://pmc.ncbi.nlm.nih.gov/
  - https://link.springer.com/journal/40279
  - https://www.frontiersin.org/journals/physiology
related:
  - ultrarunning-podcasts-blogs-and-newsletters
  - gi-distress-and-dnf-figures
  - carbohydrate-120g-mountain-marathon-trial
  - polarized-training-review-evidence
  - heat-acclimation-figures
  - sleep-in-mountain-ultramarathon-finishers
  - strength-training-running-economy-meta-analyses
  - sodium-does-not-prevent-cramping
  - reds-and-low-energy-availability-evidence
  - time-crunched-volume-claims
importance: 5
source_kind: bibliography
citation_status: recommended
reference_role: method
quality_signal: unknown
authority: asserted
disposition:
  - "gap: this page IS the gap register for the evidence layer. Its second half lists eight questions this corpus routes to and cannot ground from any literature found, which is the honest state of the sport's evidence base rather than a defect in this vault"
population: >-
  Not applicable — a map of sources. The recurring caution about the populations in this literature
  is the reason the corpus has a `population` field at all: endurance research is built on small
  samples of well-trained young men, frequently on cycle ergometers because they are easier to
  instrument than mountains, in efforts far shorter than an ultra. Assume that shape unless a paper
  says otherwise, and check whether it says otherwise.
unit: >-
  Not applicable. The standing unit warning: this literature reports oxygen cost, power, time to
  exhaustion and blood markers. It very rarely reports FINISHING AN ULTRAMARATHON. Every translation
  from the first set to the second is an inference and should be labelled as one.
ip_class: public
---

# Where the evidence lives

## The journals

| Journal | What appears there | Access |
| ------- | ------------------ | ------ |
| **Sports Medicine** (Springer) | The systematic reviews and meta-analyses. Where the intensity-distribution and strength-training evidence in this corpus comes from | Mostly paywalled; many reviews mirrored on PMC |
| **Sports Medicine – Open** | Open-access sibling. The 1,154-finisher sleep survey is here | Open |
| **British Journal of Sports Medicine** | IOC consensus statements, including REDs | Mixed |
| **International Journal of Sport Nutrition and Exercise Metabolism** | The fuelling and hydration literature's home | Paywalled |
| **Medicine & Science in Sports & Exercise** | ACSM's journal; position stands | Paywalled |
| **European Journal of Applied Physiology** | Heat, altitude, thermoregulation | Paywalled |
| **The Journal of Physiology** | Mechanistic work — heat acclimation haematology, cardiac adaptation | Mixed |
| **Frontiers in Physiology / Frontiers in Medicine** | Heat acclimation, EAH updates. Fully open | Open |
| **Nutrients** (MDPI) | High volume, open, **variable quality**. Read the methods, not the abstract | Open |

## Access routes that actually work

1. **PubMed Central (PMC).** The single most useful route. Most of this corpus's citations resolve
   to a `pmc.ncbi.nlm.nih.gov` identifier, and PMC copies are full text and free.
2. **PubMed** for the search, PMC for the text.
3. **The consensus statements**, which are the best value per hour in this whole literature: they
   are written to be read by practitioners, they state their evidence grades, and they cover the
   questions that matter here (hyponatremia, REDs, sports nutrition).
4. **The reference list of a good review**, which is faster than any search.

## The eight holes

These are questions the lenses in `workflows/lenses.json` route to and which **no literature found
in this research pass can ground**. They are listed here rather than in a private note because a
gap somebody wrote down is usable and the same gap left unstated is what a lens walks into.

1. **Amateur training volume versus ultramarathon outcome.** No measurement of finishing
   probability, finish time, injury or dropout against training volume. The question every amateur
   asks first. See [[time-crunched-volume-claims]] — the data exists on commercial platforms and the
   analysis has not been published.
2. **Intensity distribution at ultra distance.** Every study in the polarised literature is of
   events under about three hours. See [[polarized-training-review-evidence]].
3. **Fuelling rate at 100-mile duration.** The high-rate evidence is from a mountain marathon in
   elite men. See [[carbohydrate-120g-mountain-marathon-trial]].
4. **DNF reasons with starters as the denominator.** Only non-finisher denominators exist, so no
   race's DNF profile is comparable to another's. See [[gi-distress-and-dnf-figures]].
5. **Amateur heat-acclimation methods.** Sauna, hot bath, extra layers — how everyone actually does
   it, and none of it evaluated. See [[heat-acclimation-figures]].
6. **Runners who did not finish.** The sleep and pacing literature surveys finishers, which excludes
   by construction the population a night strategy is for. See
   [[sleep-in-mountain-ultramarathon-finishers]].
7. **Strength training measured at ultra pace, on a gradient, in a fatigued athlete.** All three
   conditions absent from the economy literature. See
   [[strength-training-running-economy-meta-analyses]].
8. **Ultrarunning-specific REDs prevalence**, and a dose-response sodium trial in high sweat-sodium
   athletes. See [[reds-and-low-energy-availability-evidence]] and
   [[sodium-does-not-prevent-cramping]].

## What this list is for

Two things.

**It bounds the corpus's claims.** A lens grounding on any of these eight is grounding on
extrapolation, and should say so in its output rather than producing a note indistinguishable from a
well-evidenced one.

**It is the research agenda.** Holes 1 and 4 are closable by someone with access to platform data and
no laboratory at all. That is worth knowing.

The practitioner layer that fills these holes in practice — coaching experience, which is
`authority: experienced` and is genuinely valuable at that grade — is mapped in
[[ultrarunning-podcasts-blogs-and-newsletters]].
