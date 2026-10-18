# The plan toolchain

One plan definition, three outputs, so they cannot drift apart.

```
build_plan.py   ->  advisory/analysis/plan/plan.md              read this
                    advisory/analysis/plan/hellbender-2027.ics  import to Google Calendar
                    advisory/analysis/plan/garmin_workouts.json  feed to push_garmin.py
push_garmin.py  ->  Garmin Connect -> Fenix 7 Pro
```

## Rebuild after any change

```bash
python3 workflows/plan/build_plan.py --check   # validate, write nothing
python3 workflows/plan/build_plan.py           # write all three
```

**Never hand-edit the three outputs.** Change `build_plan.py` and rebuild, or the document, the
calendar and the watch will disagree within a fortnight and you will train off whichever one you
happened to open.

## What `--check` enforces

| Check | Why |
| ----- | --- |
| Build-week ramp ≤ 22% | Compares each build week to the previous **build** week, not the calendar week before it — comparing against a down week reports a 50% jump every time volume resumes, which is the shape a down week is supposed to have |
| Every week has a rest day | Caught a real defect: the first draft gave Monday a recovery run in two phases, leaving an athlete with 6–7 available days and no full rest day from week 9 on |
| Session minutes reconcile with the weekly hour target (±0.75 h) | Weights that do not sum produce a plan whose header and body disagree |
| Every week has hours and vert defined | A missing week fails loudly rather than generating an empty one |

## Google Calendar

Import once: **Google Calendar → Settings → Import & export → Import**, choose
`hellbender-2027.ics`, and **import into a new calendar** called something like "Hellbender".
A separate calendar can be toggled off and, more importantly, deleted wholesale when the plan
changes — re-importing into your main calendar leaves 219 orphaned events to delete by hand.

Re-importing after a rebuild **adds duplicates**; it does not update in place. The workflow is:
delete the calendar, re-import. The UIDs are stable, so a client that honours them will update
rather than duplicate, but Google's importer does not reliably do this.

Daily mobility is one recurring event rather than ~200 copies.

## Garmin

Read the header of `push_garmin.py` before running it. Three things matter:

1. **Run it on your own machine.** It needs your Garmin login, read from the environment. Never
   paste credentials into a chat, an argument, or this repository.
2. **Dry-run, then one, then the rest.** Garmin publishes no consumer API for structured
   workouts; this works against the private endpoints the web app uses, and the step-type IDs
   come from community reverse-engineering rather than documentation. A bad bulk run leaves 150
   broken workouts to delete by hand.
3. **Only runs and vert sessions are pushed** — 150 of the 246 sessions. Strength and mobility
   stay in the calendar, because Garmin's strength-exercise IDs are a separate and much larger
   reverse-engineering problem and getting them wrong produces a workout that looks right and
   prescribes the wrong movement.

```bash
pip install "garminconnect[workout]"
export GARMIN_EMAIL='...' GARMIN_PASSWORD='...'

python3 push_garmin.py --dry-run                  # what would be sent
python3 push_garmin.py --limit 1                  # send ONE, then look at the watch
python3 push_garmin.py --from-week 1 --to-week 8  # then a block at a time
```

**Workouts ship with no pace or heart-rate target**, deliberately. The athlete's zones are
unknown, and inventing them would put targets on the watch that look authoritative and are
guesses. Effort guidance is in each step's description instead, where it reads as guidance. Once
there is a tested threshold or a set of HR zones, add targets in `garmin_workout()` — that is the
right time, not before.

If Garmin breaks the endpoint, the `.ics` still carries the entire plan and nothing is lost but
convenience.

## Changing the plan

Most edits are to one of four tables at the top of `build_plan.py`:

| Table | Controls |
| ----- | -------- |
| `WEEK_HOURS` | Weekly training hours. The ramp check polices this |
| `WEEK_VERT_FT` | Weekly vertical gain target, feet |
| `MOUNTAIN_WEEKS` | Which weekends are mountain trips, and the note that goes with each |
| `TUNE_UPS` | Tune-up races: week, name, minutes, note |

Session structure lives in `WEIGHTS` (fraction of weekly running minutes per weekday, per phase)
and `classify()` (what each day is for). `STRENGTH_DAYS` drives both the schedule and the A/B
labelling — they were decoupled once, and every session in the plan silently rendered as
"Strength B" until the validator's output made it obvious.
