---
title: Training log — self-reported
type: register
status: active
updated: 2026-10-31
---

# Training log

> **Self-reported.** The athlete logs what actually happened; the plan says what was asked for.
> The gap between the two columns is the only honest measure of this build, and it is the number
> the next review reads.
>
> **Observed, not intended.** Per the athlete card's rules: hours come from what happened. A
> session not logged is treated as not done, which is harsh and is the only version that works.

## What to report, and the one field that matters most

Four things, and the fourth is the one that catches problems early:

1. **Time** — minutes actually moving.
2. **How it felt** — easy / steady / hard. Not pace.
3. **Vert**, with its derivation if indoors (machine readout vs treadmill arithmetic).
4. **ANY posterior-heel sensation, toe discomfort, or change in how you were moving.** Even
   "nothing". A blank here is a missing observation, not a clean one.

Point 4 exists because of the recorded injury cascade: a stubbed toe became a lost nail became an
altered gait became seven months off. The compensation does the damage, and the only early warning
is noticing that something changed. See `advisory/kb/frameworks/foot-care-and-shoe-fit.md`.

## Log

| Date | Wk | Planned | Actual | Feel | Vert | Heel / toe / gait | Note |
| ---- | -- | ------- | ------ | ---- | ---- | ----------------- | ---- |
| 2026-10-31 | 2 | Long run 50m | | | | | *not reported* |
| 2026-11-01 | 2 | Recovery run 25m | **not done** | — | — | — | Athlete reported 2026-11-02. One missed 25-min recovery run; no action |
| 2026-11-02 | 3 | Rest | rest | — | — | — | Scheduled rest day |
| 2026-11-03 | 3 | Aerobic 25m + Strength A | | | | | *not reported* |
| 2026-11-04 | 3 | Easy 20m | | | | | *not reported* |
| 2026-11-05 | 3 | Aerobic 25m + Strength B | | | | | *not reported* |
| 2026-11-14 | 4 | Long run 35m | **not done** | — | — | — | Flew to Scottsdale AZ. Moved to Sunday rather than written off — in a down week the long run is the session worth keeping and the recovery run is the droppable one |
| 2026-11-15 | 4 | Recovery 20m | **35m long run instead** (swap) | | | | Scottsdale. Travel day before |
| 2026-11-07 | 3 | 55m long run — **cut** | short easy jog | — | flat | quads clean; hamstring tight, eased | Cut from 55m on the morning report: hamstring niggle after Friday's drive, plus Friday already 58% over. Correct call |
| 2026-11-08 | 3 | Off (swapped to Fri) | off | — | — | — | As planned |
| 2026-11-06 | 3 | 30m (swap from Sun) | **47:33** total / 44:30 moving, ~4.7 km | avg HR 134, max 162 | Company Mill, technical | **Quads: no soreness. Heel/toe: nothing. HAMSTRING tight next morning — athlete suspects the ~2.5 h drive home** | **58% over prescription.** Walk 12:50 = 27% — the technical ground was walked, as asked. Avg pace 10:08/km, moving 9:29. First descent exposure in ~7 months |

## Finding 2026-11-07 — the drive home is part of the session

Quads were **clean** the morning after a 47-minute first descent exposure. That is a better
eccentric tolerance than the plan assumed and mildly relaxes the descent-progression caution.

What was NOT clean was a hamstring, and the athlete's own read — the ~2.5 h drive home — is the
likeliest cause and matters far beyond one niggle. **The geography makes this structural:** every
mountain weekend in this plan ends with **5–5.5 hours in a car seat** immediately after the
biggest session of the block, seven times before May. Prolonged hip flexion on a loaded,
un-cooled-down posterior chain is a known way to turn a good session into a week of tightness.

So the drive is now treated as part of the session rather than as what happens afterwards:

1. **Walk 10 minutes before getting in the car.** Non-negotiable after a mountain day.
2. **Eat and drink before driving**, not at the first services an hour in.
3. **Stop every hour**, get out, walk 3–5 minutes, and do one set of standing hamstring and hip
   flexor openers.
4. **Seat upright**, not reclined — a reclined seat holds more hip flexion, not less.
5. **Treat the next day as part of the trip.** It is already a rest or easy day in every mountain
   week; keep it that way rather than backfilling a missed session into it.

This belongs in the plan's mountain-week notes, not only here.

## The pattern to watch — first instance, 2026-11-06

The athlete card names the standing risk as **added sessions, not missed ones**. First instance
recorded: a 30-minute prescription run as 47:33, on the one session where overshooting carried the
most cost — a first eccentric descent exposure after ~7 months off, on root-and-rock terrain, with
a toe-strike injury history on exactly that ground.

This is not a reprimand and the session was not reckless: it was easy (avg HR 134), a quarter of it
was walked, and the terrain was the right stimulus. It is recorded because **the consequence lands
on the NEXT session**, not this one — unaccustomed descent peaks at 24–48 h, so Saturday's long run
was cut rather than Friday's being undone. That is the whole argument for logging prescription
against actual.

Watch for: a second instance. One is a good day out. Two is a pattern, and the pattern is the one
thing this build cannot absorb.

## Garmin integration — first successful upload 2026-11-16

Workout id **1762562381** ("W1 Aerobic run") created and scheduled on the athlete's Garmin
account. That validates the whole payload shape against the live, undocumented endpoint: the
`running` sport id, the `interval` step type, the time-based end condition, and the schedule call.

**Second upload 2026-11-16:** workout **1762566316** ("W1 Strength A — heavy lower", 6 steps) —
`strength_training` sport id 5 **verified against the live API**. That was the least certain
constant in the toolchain and it covers 53 of the 202 workouts. Token caching also succeeded, via
`api.client`, so remaining batches need neither password nor MFA.

**Still unproven:** the `other` sport used for mobility (2 workouts) and the lap-button end
condition on the three all-day objectives. One of each before the bulk push.

Four failures preceded it, all mine, all on this athlete's laptop rather than in a test:
dependency import after the password prompt; a silently-unmatched refactor leaving `run_uploads`
undefined; no MFA callback; and a token-cache attribute that does not exist on this library
release. The first two are now covered by `test_push_garmin.py`.

## Correction 2026-11-16 (second, same day) — it was a CUTOFF DNF, and that is good news

Athlete: *"I could have finished the 50 miles at heartbreaker if I could have met the cut offs. I
was physically running still. The bursa had zero pain the loss of toenails was not stopping the
run. It was poor execution on the descents and wasted pace on flats."*

**This supersedes the correction below, which was recorded hours earlier.** The sequence of
diagnoses in this file now runs: injury cascade → eccentric durability failure → **execution**.
Only the last one is the athlete's own account of why the clock beat them.

### Why this is the best news in the file

| Heartbreaker-equivalent | Hellbender projection | Finishes |
| ----------------------- | --------------------- | -------- |
| **16h51** — extrapolated from 45 mi / 15h00 | 36h13 – 43h38 | **51%** |
| 16h00 (−5%) | 34h30 – 41h41 | 77% |
| 15h27 (−8%) | 33h23 – 40h26 | 94% |
| **15h00 (−11%)** | 32h28 – 39h24 | **100% — inside on every assumption** |
| 14h00 (−17%) | 30h26 – 37h06 | 100%, 2h54 spare |

**The gap is 11%, and it is attributed to two skills rather than to physiology.** On a course with
12,000 ft of descent, descending execution alone can plausibly account for that much. A durability
or aerobic-ceiling deficit of 11% in 25 weeks off a seven-month layoff would be a far harder ask.

### The cutoff structure, which shapes the whole pacing problem

From the official intermediate cutoffs (**`acquired`, possibly stale — re-read before entry**):

| Segment | Miles | Hours | Required |
| ------- | ----- | ----- | -------- |
| Start → 50.1 | 50.1 | 20.75 | 24.85 min/mi |
| 50.1 → 65.8 | 15.7 | 5.75 | **21.97 min/mi** |
| 65.8 → 83.4 | 17.6 | 6.50 | **22.16 min/mi** |
| 83.4 → 102.3 | 18.9 | 7.00 | **22.22 min/mi** |

**This is the opposite shape from most hundreds.** The first fifty is the MOST generous segment and
the back half tightens to ~22 min/mi. Two consequences: there is little point banking time early
against cutoffs, and the binding constraint is holding ~22 min/mi from mile 50 to 102 through a
night. The athlete ran 20.0 min/mi for 45 miles fresh at the Heartbreaker — so the demand is a
slightly slower pace, but held three times as far and into a second day.

### What changed in the plan

1. **The descent block is now TECHNIQUE PRACTICE first**, conditioning second, carrying five cues
   one per rep. The earlier framing — "control the lowering", conditioning-led — was built on the
   durability diagnosis.
2. **Long runs carry a RUNNABLE-GROUND DISCIPLINE note**: run everything runnable at easy effort
   from mile one, and hike the climbs early enough that nothing gets walked later that could have
   been run. This addresses the second half of the deficit, which had nothing in the plan at all.
3. **New corpus page**: `kb/frameworks/descending-technique-and-eccentric-conditioning.md`. The
   tag `downhill-eccentric` previously appeared on exactly one page — about indoor climbing
   machines, where descent is mentioned only as what they cannot train. It is the corpus's only
   `measured`-authority page, and it grades the technique half honestly as ASSERTED: a targeted
   search found no controlled study linking cadence, stride or lean to reduced quadriceps damage
   or faster descending in trail runners.
4. **`projection.py` no longer claims an injured pace.** It printed "this is an INJURED pace …
   a FLOOR on capability". That is now false and said so in the one place downstream code quotes.

### Defect 2026-11-16 (third) — the plan withheld its most important exercise for 8 weeks

Found by the athlete: *"FLAT GROUND until week 9 → we're doing vert this week."*

Correct, and it is worse than a stale label. **Week 5 prescribes 600 ft of vert and week 6
prescribes 2,500 ft on a mountain trip, both inside Base 1.** Steep climbing holds the ankle in
dorsiflexion — the plan's own `HEEL_WARNING` says exactly that — so the plan was withholding a
15 cm step in the gym while prescribing hundreds of feet of climbing that loads the same tissue
far harder. **The precaution protected against a small dose of precisely what it prescribed in a
large one.**

**And "ECCENTRIC step-down on FLAT GROUND" is not an exercise.** A step-down without a step
removes the eccentric range that makes the movement worth doing. So the single most important
exercise in the plan, given a race lost on descents, was gutted for 8 of 29 weeks.

The restriction also rested on a causal model corrected twice since: the 2026 bursitis gave ZERO
pain during the race, did not stop the run, is ~8 months resolved, and arose from a gait change
following toe trauma — not from calf loading. Loaded end-range dorsiflexion is a plausible
irritant for an ACTIVE bursa, not a cause in a settled one.

**Fixed.** Base 1 eccentric step-downs now use a LOW (~15 cm) step with step height as the
progression; calf work is full range off a step from week 1, bodyweight before load. The heel
watch is retained as a **stopping rule** rather than a prohibition — which is what it should
always have been.

### Answered 2026-11-16 — missed cutoff, confirmed

*"Missed cut off. I was still running."* Closes the open question. The constraint was the clock,
not the athlete's judgement, which means the 40 h Hellbender cutoff and its intermediate splits
are the thing to model — and the pacing work above is the intervention, not a caveat to it.

### Answered 2026-11-16 — the mechanism was SOCIAL PACING

*"Shuffling out walking with a group that could execute downhill run."*

Neither of the two readings offered. The root cause was **adopting another group's terrain
allocation.** That group's race model — cruise the runnable ground, make the time back on the
descents — is perfectly solvent for runners who can descend. The athlete borrowed the comfortable
half of it without owning the descending half, and so **lost time on both terrains from a single
decision**: slow where speed was cheapest, and slow again where the group was fast.

This explains a large time loss economically, and it feels correct while it is happening, which is
why it is recorded as a mechanism rather than a cue. It also means the deficit is more recoverable
than two independent errors would be — one decision, not two habits.

**The corollary is uncomfortable and is now in the plan:** a weak descender's model has to be the
INVERSE. Make time on the runnable ground *because* you will give some back on the descents. You
cannot afford to walk what a good descender can afford to walk.

Added to the long-run note as a terrain-plan instruction plus a one-question test — *can I run
this?* — and to
`kb/frameworks/descending-technique-and-eccentric-conditioning.md` as "the social-pacing trap".

### Consequence — I was wrong about Badwater Cape Fear

Recorded 2026-11-16 that a flat beach 50 "tests none of this". **That was wrong once the mechanism
was known.** 38 of its 51.4 miles are runnable beach, which makes it close to a pure test of
runnable-ground discipline — exactly half the deficit, and the half that is purely disciplinary
rather than skill-limited. Its value goes up materially.

The two races now cover both halves cleanly:

| Objective | Date | Tests |
| --------- | ---- | ----- |
| Badwater Cape Fear 51.4 mi | Sat 20 Mar 2027 | **Runnable-ground discipline**, plus a first 50-mile finish |
| Hellbender course rehearsal (week 25) | Sat 10 Apr 2027 | **Descending**, on the actual terrain, 27 days out |

**Both should be run SELF-PACED**, and the rehearsal ideally solo — the failure mode being trained
out is pacing to other people.

## Correction 2026-11-16 — the DNF was quads on the descents (SUPERSEDED, see above)

Athlete, unprompted: *"The dnf was due to poor performance on descents I could not maintain speed
my quads were shot."*

This supersedes the causal model that has driven this repo since 2026-10-31. Both things happened
— the toe trauma, the lost nail, the gait change, the bursitis that cost seven months — but **the
race ended because eccentric quadriceps capacity ran out**, not because of the heel.

### What it invalidates

1. **The risk ranking.** Descending was risk 4. It is risk 1, and it is paired with the worst
   possible geography: sea level at home, 5–5.5 h to the nearest real descent.
2. **The eccentric block, which was the plan's central defect.** A fixed
   `ECCENTRIC step-down 3x10/leg, 4 s lowering`, identical in week 3 and week 25. The one quality
   that most needed progressive overload was the only thing in the plan that never changed. Now
   progresses by phase in load, step height and tempo.
3. **The descent thread, which did not exist.** Seven mountain weekends in 29 weeks, for the
   system that ended the last race. A `DESCENT FINISH` block now closes every non-mountain long
   run — car park ramps, overpasses, bridges, since Hampstead supplies nothing and treadmills
   almost never decline. Deliberately at the END, on tired legs: the quads failed at mile 45, not
   mile 5.
4. **Yesterday's argument for uphill intervals.** I justified the Wednesday session partly on
   "climbing has no eccentric loading." Under the corrected model that describes what it does NOT
   train. The session stays on a narrower claim — the safest way to deliver aerobic intensity,
   and specific to 21,500 ft of ascent — but it was never the answer to the failure mode, and the
   comment in `build_plan.py` now says so.
5. **The charitable reading of the 51% projection.** The athlete card recorded "that was an
   INJURED pace, so it is a floor on capability." If the limiter was eccentric durability rather
   than a toe, the 15h00 is closer to a real estimate than to a floor. **Read ~51% as less
   optimistic, not more.**
6. **A stale prescription found while fixing the above:** both calf-raise lines carried
   "FLAT GROUND until week 9" as literal text and never progressed — an instruction still reading
   "until week 9" in week 19. Now phase-keyed.

### The arithmetic that matters

Heartbreaker: ~12,000 ft over 50 mi. Hellbender: ~21,500 ft over 102 mi. Similar vert density,
but **roughly double the absolute descent load**, asked of the system that gave out at mile 45 of
the shorter race. This is the central problem of the build, and nineteen weeks is enough time to
address it only if it starts now.

### Open question worth answering

Was the DNF a missed cutoff or a voluntary withdrawal? It decides whether the constraint is pace
against the clock or the athlete's own judgement that continuing was unwise — and those imply
different things about the 40 h Hellbender cutoff.

## Week rollup

Filled at each review. Completion rate over a rolling twelve weeks is the number the plan is
judged by — not volume.

| Wk | Planned h | Actual h | Sessions planned | Done | Completion |
| -- | --------- | -------- | ---------------- | ---- | ---------- |
| 1 | 3.0 | *unreported* | 6 | | |
| 2 | 3.5 | *partial* | 6 | 5 of 6 | Sunday 1 Nov missed |
| 3 | 4.0 | ~4.0 | 6 | 6 | Friday +18 min over, Saturday cut to compensate. **Net on target** |
| 4 | 3.0 (down) | | 6 | | Sat long run moved to Sun (travel to Scottsdale) |

## Terrain exposures — tracked separately, because Hampstead supplies none

Descending is the structural gap in this build (athlete card, risk 4): sea level at home, and the
only eccentric descent load available comes from travel. So every exposure gets logged, with its
terrain, because the progression here matters more than the weekly hours do.

| Date | Where | Gain | Technical? | Toe / heel after | Note |
| ---- | ----- | ---- | ---------- | ---------------- | ---- |
| 2026-11-06 | Company Mill, Umstead SP (Reedy Creek / Harrison Ave) | ~100 ft/mi | **Yes — roots, rocks, uneven** | **Quads clean, heel/toe clean, hamstring tight (likely the drive)** | **Done at 47:33, not the prescribed 30.** 27% walked. Eccentric dose ~58% larger than intended on a first exposure — the reason Saturday was cut |

**The rule for this table:** the first few entries are about tissue tolerance, not about vert
totals. Unaccustomed descent produces soreness at 24–48 h, so a second exposure inside three days
is how the first one becomes an injury.

## Defect 2026-11-15 — down weeks are not as down as the target says

Week 4's sessions total **3.4 h against a 3.0 h target**. Cause: `r5()` in `build_plan.py` floors
every session at 20 minutes, which is sensible on its own — a 12-minute run is not worth the kit —
but in a down week several sessions get floored UP, and the week lands 13% above its target.

The validator does not catch it because its tolerance is +/-0.75 h.

**The direction is wrong for this athlete**, whose recorded standing risk is doing more than the
plan asks. Down weeks are the specific thing defending a 29-week ramp off a 7-month layoff, and
they are quietly 13% less restful than designed. Fix is to drop a session from down weeks rather
than to shave minutes off the floor: four runs instead of five, which is also how the weeks
actually get executed.

**FIXED 2026-11-15**, bundled with the intensity fix so the calendar and watch regenerate once.

`build_week()` now drops the droppable run from a down week, capturing `total_w` BEFORE the drop
so the remaining sessions keep their minutes and the week genuinely falls — renormalising would
have redistributed the same total and made the long run longer, which is the opposite of the
intent. Base 1 down weeks drop Wednesday (Base 1 has no Friday run); Base 2 onward drop Friday,
the session already annotated "drop it without guilt".

Mountain weeks are excluded, which week 27 forced: it is both a down week and a mountain week,
the mountain block already drops Friday for travel, and the second drop undershot the target by
an hour. A mountain week's sessions are long enough that the 20-minute floor never binds, so the
defect does not apply there.

Week 4 now lands at 3.08 h against its 3.0 h target, from 3.4 h. The dropped day appears in the
plan as an explicit "Rest — down week" row rather than vanishing, so it reads as deliberate.

## Defect 2026-11-15 — the plan has no hard pole

Raised by the athlete, unprompted: last year's pace-based training "wasn't pushing my overall
fitness" and they never regained a previous level. Checking `classify()` in `build_plan.py`
confirms the complaint applies to THIS plan too, and that it is a design defect rather than a
metric problem.

**Every running day in all 29 weeks is prescribed easy.** (Stated once as "no hard work at\nall", which was wrong: `Back squat or trap-bar deadlift 4x5 @ heavy` is genuine high-intensity\nwork. The accurate claim is that there is no hard AEROBIC work.) "Easy, conversational", "genuinely
easy", "slow enough to feel pointless". The only intensity in the build is 6 x 20 s strides from
Base 2, plus whatever intensity the athlete chooses on the Wednesday vert session, which carries no
intensity prescription at all.

The repo declares `polarized-superiority` as a tracked CLAIM — roughly 80% easy and 20% **hard**.
The plan implements the 80 and omits the 20 entirely. That is monotonous, not polarized, and it
would reproduce precisely the plateau the athlete described.

**This is not an argument for HR over pace.** The metric question is separate and answered below.
A plan with no hard sessions produces no high-intensity adaptation whichever number is on the
watch face.

### Intensity control — different metric per session type

| Session | Control by | Reason |
| ------- | ---------- | ------ |
| Easy / recovery / long | **HR ceiling** | Coastal NC heat inflates HR at a given pace, so a pace target silently converts an easy run into a moderate one. Pace is meaningless on technical trail (2026-11-06: HR 134 at 10:08/km — easy effort, slow pace). And an HR cap cannot be accidentally beaten, which suits an athlete whose standing risk is doing more than prescribed |
| Threshold / hard flat | **Pace** | HR lags 30-60 s into an effort, drifts up with fatigue at identical output, and is SUPPRESSED when most fatigued — so it is wrong in all three directions precisely when it is being relied on |
| Climbing / vert | **Effort and breathing** | Neither pace nor HR is usable on sustained climbs |

### The under-appreciated argument for HR: it measures, not just targets

The athlete's report — "never getting to the level of fitness I've had" — describes a missing
INSTRUMENT as much as a missing stimulus. Pace alone confounds fitness with heat, terrain, wind
and sleep. Two cheap HR-derived measures close that loop:

1. **Pace at fixed easy HR**, same route, every few weeks. Rising pace at constant HR is aerobic
   fitness, observed directly.
2. **Cardiac drift across a long run** — the pace:HR ratio, first half vs second. Under ~5% means
   the aerobic base is real; over ~10% means long runs are being run too hard.

Neither needs a lab. Both need the HR to be recorded, which starts now.

### Blocked on one number

Zones cannot be set. One data point exists (134 avg / 162 max, reported easy), which establishes
only that max HR is meaningfully above 162. **Age is deliberately not used:** 220-age carries a
standard deviation near 10 bpm, wide enough to place an easy ceiling inside a tempo zone. Per the
toolchain's standing rule, workouts ship with NO targets rather than invented ones.

**Resolution: a 30-minute threshold field test at the end of week 8** (Base 1 → Base 2 boundary,
~13 Dec 2026). Average HR over the final 20 minutes is LTHR, and every zone derives from it.
Chosen over a max-HR effort because it is submaximal, more useful as an anchor, and appropriate
for an athlete eight weeks back from a seven-month layoff.

### Fix APPLIED 2026-11-15

Add one quality session per week from week 9, **on the existing WEDNESDAY vert session** rather
than as an added day.

**Why not Tuesday and Thursday**, asked by the athlete 2026-11-15. Those are already the two
heaviest weekdays: 45 min of heavy lower-body strength stacked on a 40-min aerobic run, each.
Adding threshold running would be a third hard stimulus on the same day, and because the vert
session sits on Wednesday between them, the week would carry three consecutive hard days
(Tue/Wed/Thu). Wednesday is the only weekday with a single session. Friday is ruled out twice
over: it feeds Saturday's long run, and it is the travel day on all seven mountain weeks.

**One quality session, not two.** At week 9 the athlete is nine weeks off a seven-month layoff,
and the week already carries three significant stressors (Tuesday strength, Saturday long, Sunday
back-to-back). A second hard session is how a build arrives at May undertrained because February
was spent injured. If Wednesday is absorbing well by the Specific phase (week 17+), the second
hard dose should come from the mountain weekends, which are more race-specific than a second
threshold session.

The argument for that placement is injury-specific. Hard uphill work carries no eccentric
loading, no high ground-contact force, no speed and no descent — and this athlete's injury
cascade ran through a gait change under impact. Threshold work on a StepMill or treadmill incline
delivers the intensity stimulus with close to the lowest mechanical risk available, while being
directly specific to a race with 21,500 ft of climbing. It closes the fitness-plateau gap and the
vert gap with one session.

**Applied.** `QUALITY` and `quality_for()` in `build_plan.py`. Twelve quality sessions: six full
sets (weeks 9, 11, 13, 17, 19, 24), five shortened primers on mountain weeks (10, 14, 18, 21, 25)
where the weekend is the real work, and one taper sharpener (week 26). Nothing in Base 1, nothing
in a down week, nothing in a tune-up week.

Progression: 4x5 min → 5x5 → 4x8 → 5x8 → 3x12 → 4x10, with 2-4 min easy recoveries.

**No HR or pace target is written**, per the toolchain's standing rule. Effort description only
until the week-8 test. The athlete asked whether Tuesday AND Thursday should carry it; they
should not, and the reasoning is above.

## Open — unverified from the first two weeks

The plan began Mon 19 Oct 2026. Nothing has been logged, so none of this is known:

- **Did weeks 1 and 2 happen?** Partially answered 2026-11-02: the athlete reported *not* running
  Sunday 1 Nov, which implies they are tracking the plan and week 2 largely ran. Still unconfirmed
  session by session, and the Saturday 31 Oct long run is unreported.
- **Did the Wednesday shoe audit happen?** It is the cheapest injury-prevention action in the
  entire 29 weeks and it was scheduled twice.
- **Bodyweight**, which still blocks every figure in `plan/nutrition.md`. Now the top open item.
- **The Heartbreaker was a DNF** at 45 mi / 15h00 — established 2026-11-05, superseding both the
  14:22 figure and the assumption that it was a finish. Still worth pulling the Garmin activity
  for March 2026: the SPLITS would show how early the toe went, which is the one thing that says
  how much of that 15h00 was an injured pace rather than a real one.
- **When in the race did the toe injury start?** Decides whether the 51% feasibility estimate is
  roughly right or materially pessimistic. Nothing recorded answers it.
- **HR zones.** Unblocked by one 30-min test at the end of week 8. Until then every run logs
  avg HR, so the test has a baseline to be compared against.
- **Fuelling:** anything over 90 minutes should be carrying 30 g/h from week 1. Nothing yet is
  over 90 minutes, so this starts to bite around week 5.
