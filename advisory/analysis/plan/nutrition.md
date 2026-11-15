---
title: Nutrition plan — daily diet, training fuelling, and the race-day ladder
type: register
status: active
updated: 2026-10-18
---

# Nutrition plan — Hellbender 100

> **Not medical advice, and not a diet.** This is a fuelling plan for a specific training
> load. Anything clinical — bloods, GI disease, disordered eating, medication, supplements
> beyond the ordinary — goes to a physician or a sports dietitian. See the gate below, which
> runs before everything else on this page.

## 0. The gate — read before anything else

Per `advisory/kb/frameworks/energy-availability-floor.md`, this runs **before** any training
recommendation, not alongside it. You are about to roughly quadruple your training load over
seven months. The single most likely nutritional failure is not a bad macro split — it is
**inadvertent under-fuelling**: hard sessions stacked on top of a normal day's food, repeated
for weeks.

Stop and get professional input if any of these appear:

- A bone stress injury. One is a signal; two is a pattern.
- Persistent fatigue that down weeks do not touch, with performance falling at unchanged load.
- Recurrent illness, poor wound healing, feeling cold constantly.
- Unintended weight loss during a build, or deliberate weight loss while training.
- Low mood, poor sleep, lost libido alongside any of the above.

**Do not attempt weight LOSS during this build.** Under-fuelled training is worse than absent
training, and that is the one hard constraint on this page.

**Deliberate lean-mass GAIN is a different proposition and is not prohibited.** The original
version of this section banned "body-composition change" in both directions, which conflated two
opposite risks. A modest energy surplus alongside heavy strength work does not cause relative
energy deficiency — it is the opposite failure mode. The athlete's stated goal (2026-11-15) is
190–195 lb from 185 lb, explicitly for leg strength rather than for a number, after an Ironman
history of cutting weight and feeling weak. That goal is compatible with this gate. See §1a.

## 1. Daily diet — fuel the work, not the day

**You weigh 185 lb = 84 kg** (athlete, 2026-11-15). Everything below is computed from it.
`advisory/model/fueling.py` does the race-day arithmetic.

| Nutrient | Per kg | **At 84 kg** |
| -------- | ------ | ------------ |
| Protein | 1.8–2.2 g/kg | **150–185 g/day — target 170 g** |
| Carbohydrate, easy days | 3–5 g/kg | **250–420 g** |
| Carbohydrate, moderate days | 5–7 g/kg | **420–590 g** |
| Carbohydrate, big days | 7–10 g/kg | **590–840 g** |
| Fat, floor | ≥0.8 g/kg | **≥67 g** |

Protein is set at the UPPER end of the usual endurance range, not the middle, for two reasons
that both apply here: a heavy strength block runs twice a week for the whole build, and the
athlete is pursuing lean-mass gain. 170 g/day across 3–4 meals is ~45 g per meal — which in
practice is the single biggest change most endurance athletes have to make, because 45 g of
protein is more food than it looks like.

| Nutrient | Target | Notes |
| -------- | ------ | ----- |
| **Protein** | 1.6–2.0 g/kg/day | The upper end while the strength block is running. Spread across 3–4 meals, ~0.3 g/kg each, rather than loaded at dinner |
| **Carbohydrate — easy days** | 3–5 g/kg | Base 1 weekdays, down weeks, rest days |
| **Carbohydrate — moderate days** | 5–7 g/kg | Vert sessions, aerobic runs over an hour |
| **Carbohydrate — big days** | 7–10 g/kg | Mountain weekends, long runs over 3 h, tune-up races |
| **Fat** | Whatever is left, ≥0.8 g/kg | Do not drive it low; it carries fat-soluble vitamins and satiety |
| **Fluid** | To thirst | Not a schedule. See §4 |

**Carbohydrate is periodised to the session, not held constant.** The commonest amateur error
is eating the same way on a rest day and a five-hour mountain day. The second commonest is
eating like it is a five-hour mountain day on a rest day.

## 1a. The weight goal — 185 → 190–195 lb, as muscle

Stated 2026-11-15: goal 190–195 lb, "so that my legs are stronger and not just cutting weight
similar to ironman days."

**The reasoning is sound, and the arithmetic supports it more strongly than expected.** The
intuitive objection to carrying mass up a mountain race is that it costs climbing work. For
Hellbender's 21,500 ft (6,553 m), five extra pounds (2.27 kg) costs:

```
W = m·g·h = 2.27 × 9.81 × 6553 = 146 kJ = 35 kcal of mechanical work
at ~25% efficiency ≈ 140 kcal metabolic, across the ENTIRE course
```

**About one and a half gels, over 102 miles.** The gravitational penalty for five pounds is
negligible. The broader carrying cost is larger — running economy scales roughly with mass, so
+2.7% body mass is about +2.7% energy for the same distance, perhaps 300–350 kcal over the race —
but that is still a few percent against a durability problem that ended the 2026 race outright.

**This athlete's limiter is tissue durability, not power-to-weight.** The Heartbreaker DNF was a
mechanical failure — toe trauma, gait change, bursitis — not an athlete who was too heavy to
climb. Eccentric braking capacity on 21,500 ft of descent is a strength quality. Trading a few
percent of climbing economy for descent durability is the right trade here, and it would not be
for a competitive runner chasing a podium.

### But 190 is realistic and 195 is not

| | |
| - | - |
| Rate lean mass can be added during an endurance build | **0.25–0.5 lb/week**, and the upper end only early |
| 185 → 190 lb (5 lb) | 10–20 weeks |
| 185 → 195 lb (10 lb) | 20–40 weeks |
| Weeks available in the usable window (now, week 4, to week 16) | **~12** |

**Target 190 lb by mid-February, then hold.** 195 is not available inside the window without the
surplus being large enough that most of the gain is fat, which costs the climbing economy without
buying the strength.

**The window is now, and it closes at week 16.** Two reasons it is open at all: the athlete is
eight months detrained, and re-gaining previously held muscle is far faster than building new
tissue. And weekly volume is still 3–9.5 h, where a surplus is manageable. From week 17 the
Specific phase runs 10–16.5 h/week, where the energy cost of training makes a deliberate surplus
impractical and the priority shifts to arriving at May intact.

### How to run it

| | |
| - | - |
| Energy surplus | **+250–350 kcal/day.** Not more. A bigger surplus in an endurance build goes to fat, because the hypertrophy signal is already capped by concurrent endurance volume |
| Protein | 170 g/day, ~45 g per meal (§1) |
| Strength | Already prescribed. **Progressive load is the whole stimulus** — Strength A must get heavier over the build, or the surplus has nothing to build with |
| Timing | Protein and carbohydrate within an hour of the Tuesday/Thursday strength sessions |

**Do not track this by scale weight.** Glycogen and fluid swing 3–4 lb inside a week on a
periodised carbohydrate intake, which is more than the entire 12-week signal. Track instead:

1. **Strength load.** Squat or trap-bar 4×5 and weighted step-up. If these are climbing, the
   surplus is working. This is the primary measure.
2. **Waist at the navel**, weekly, fasted. Flat while the bar goes up means the gain is lean.
3. **Bodyweight as a weekly average**, never a single morning.

If strength is flat and waist is rising, the surplus is too big — cut it to +150 kcal. If both
are flat, it is too small.

### Concurrent-training interference, stated honestly

Endurance volume and hypertrophy are partly opposed at the signalling level: the pathways that
endurance training activates suppress the ones that drive muscle growth. This is why the
realistic target is 5 lb over 12 weeks rather than the 15–20 lb a dedicated strength block might
produce. The goal is achievable but it is working against the training, not with it — which is
the argument for taking the low end of the range and taking it early.

### Micronutrients worth actually checking

Ask your physician about these before the build gets heavy, rather than supplementing blind:

- **Iron and ferritin.** Endurance running suppresses both. Low ferritin presents exactly like
  under-training — flat, heavy, no top end. It is a blood test, not a guess.
- **Vitamin D.** You will be training indoors through a Appalachian winter.
- **Calcium**, given the bone-loading this plan involves.

Do not self-supplement iron. Excess is harmful and the only way to know is a test.

## 2. Around sessions

| When | What | Why |
| ---- | ---- | --- |
| Before an easy run under 75 min | Nothing needed | Fasted easy running is fine if you tolerate it. Not a strategy, just permission |
| Before a vert session or long run | 1–1.5 g/kg carbohydrate, 2–3 h prior | Blood flow to the gut falls with intensity; a big meal too close is the usual nausea cause |
| **During anything over 90 min** | See §3 — start from week 1 | This is the one most people postpone, and gut capacity takes months |
| Within 30–60 min after a hard or long session | 0.3 g/kg protein + 1 g/kg carbohydrate | Matters most on back-to-back weekends, where Sunday depends on Saturday's refuel |
| Mountain weekends | Treat the drive home as part of the session | Arriving home under-fuelled is how Monday's fatigue becomes Wednesday's |

## 3. Race fuelling — the ladder, and the gut training that gets you there

Full reasoning in `advisory/kb/frameworks/carbohydrate-fueling-ladder.md` and
`gut-training-protocol.md`. The short version:

**Target for Hellbender: 60–90 g carbohydrate per hour.** Not 120. The 120 g/h figure comes
from a trial of twenty gut-trained elite men racing a *mountain marathon* — a quarter of your
race's duration — and its outcome was a muscle-damage marker, not performance. It does not
transfer to a 30-plus hour effort by a first-time hundred-miler.

**GI distress is the most commonly cited primary reason for withdrawal at 100-mile races.**
Your fuelling plan's job is not to maximise grams. It is to find the **highest rate that
survives the whole race**, which is almost always lower than the rate that works for four hours.

### The progression — start now, not in April

| Weeks | Target rate | What to practise |
| ----- | ----------- | ---------------- |
| 1–8 | 30–40 g/h on anything over 90 min | Habit, not capacity. Find two products you don't hate |
| 9–16 | +10 g/h every 2–3 weeks → 60 g/h | Long run only. Weekday easy runs teach the gut nothing |
| 17–25 | 70–90 g/h, race products only | Mountain weekends and both tune-ups at full race rate |
| Taper | Hold, don't raise | Nothing new after week 25 |

**Rules that matter more than the numbers:**

1. **Count grams of carbohydrate, not gels.** A 40 g gel is not 40 g of carbohydrate, and
   brands differ by a factor of two.
2. **Blend glucose:fructose above 60 g/h.** Below that it buys nothing; above it, single-pathway
   absorption saturates.
3. **Change one variable at a time.** Rate, product, form, concentration, temperature. Move two
   and a bad session teaches you nothing.
4. **Train the race products.** A gut trained on drink mix has not been trained on gels.
5. **Carry carbohydrate that does not need water.** If fuel only arrives in a drink mix, then in
   heat you must drink to fuel and in cold you must fuel to drink. Both go wrong.

### The fallback ladder — the part that gets used

Most plans have a target and no fallback. Write this on your race sheet:

| Rung | Rate | Action |
| ---- | ---- | ------ |
| 1 | 75 g/h | Plan products |
| 2 | ~55 g/h | Same rate band, different form — swap gel for chew, or chew for liquid |
| 3 | ~38 g/h | Half rate, simplest tolerated product only |
| 4 | ~22 g/h | Liquid carbohydrate only, sipped |
| 5 | 0 | Stop fuelling, walk, settle 20–30 min, restart at rung 4 |

Stepping **down** a rung and recovering beats pushing through and vomiting, which ends the
fuelling for hours.

## 4. Drinking and sodium — the part the sport gets backwards

Full reasoning in `advisory/kb/frameworks/drink-to-thirst.md` and
`benchmarks/sodium-does-not-prevent-cramping.md`.

**Drink to thirst. No more, no less.** The consensus position identifies **over-drinking of
hypotonic fluid** as the primary mechanism of exercise-associated hyponatremia, which can be
fatal and whose early symptoms — nausea, headache, confusion — are indistinguishable from
ordinary late-race misery.

**Do not set a millilitres-per-hour target.** That is the behaviour being avoided.

**On salt:** in a field study of hot-weather ultramarathons up to 30 hours, cramping,
dehydration, hyponatremia and nausea were **unrelated to total sodium intake**. Take salty food
at aid stations because it is palatable and keeps appetite going. Do not take it believing it
prevents cramp — the evidence does not support that, and the belief leads to drinking more,
which is the actual hazard.

**The one thing to measure:** weigh yourself before and after two or three long summer sessions.
Large weight *gain* over a long run is the clearest warning you will get that intake exceeds
losses. Training-block measurement, not a race-day one.

**Escalate, don't manage.** Nausea + headache + disorientation, especially with high fluid
intake and no weight loss, is a medical emergency, not a pacing problem.

## 5. Caffeine

Useful and over-used. Save it for the dark hours rather than spending it at hour four — it
borrows alertness rather than repaying it, and it masks the signal your nap decision depends on.
Practise your race-day dose at least twice in training. If you drink coffee daily, do not quit
beforehand to "sensitise"; the withdrawal costs more than the sensitivity gains.

## 6. What to do in the next two weeks

1. Fill in your bodyweight at the top and compute the four protein/carbohydrate numbers.
2. Book bloods: ferritin, iron studies, vitamin D.
3. Buy two fuelling products and start taking 30 g/h on any run over 90 minutes. Week 1.
4. Write the fallback ladder on a card and put it with your race kit.

## Open — fill these in

| Field | Value |
| ----- | ----- |
| Bodyweight (kg) | |
| Protein target (g/day) | |
| Easy-day carbohydrate (g) | |
| Big-day carbohydrate (g) | |
| Products tolerated so far | |
| Current tolerated rate (g/h, measured) | |
| Known intolerances | |
| Ferritin / vitamin D (date + result) | |
