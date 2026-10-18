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

**Do not attempt body-composition change during this build.** If it matters to you, it belongs
in an off-season with professional support. Under-fuelled training is worse than absent
training, and that is the one hard constraint in this plan.

## 1. Daily diet — fuel the work, not the day

You weigh *(fill in)* kg. Every number below is per kilogram, so fill that in and compute once.
`advisory/model/fueling.py` will do the race-day arithmetic.

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
