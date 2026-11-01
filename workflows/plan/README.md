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
3. **Everything trainable is pushed — 202 of 246 sessions.** The other 44 are rest and travel
   days, which are on the calendar but are not workouts. Breakdown: 81 run, 45 long, 53 strength,
   20 vert, 2 mobility, 1 tune-up race.

   **Strength goes up as one step per exercise**, under the `strength_training` sport, with no
   exercise IDs — Garmin's exercise catalogue is a separate reverse-engineering problem and a
   wrong ID prescribes the wrong movement convincingly. You get the prescription as step text
   instead of animations, which is the right trade.

   **`SPORT_STRENGTH` is the least certain value in the toolchain.** If strength uploads are
   rejected, set it to `SPORT_OTHER` in `build_plan.py` and re-run: the workout still lands with
   its prescription intact, just filed under the wrong sport. Test it first:
   `push_garmin.py --only strength --limit 1`.

   **All-day objectives** (Art Loeb, the self-supported 50, the week-15 50K) go up with a
   **lap-button** end condition rather than a duration. A 14-hour countdown step is worse than no
   timer. Press lap when the day is done.

   **Daily mobility is deliberately NOT pushed.** It is one recurring calendar event; 190 copies
   of a 15-minute workout on the watch is clutter. The two week-1/2 shoe-audit days do go up,
   because they are scheduled sessions with content.

```bash
pip install "garminconnect[workout]"

python3 push_garmin.py --email you@example.com --dry-run              # nothing sent
python3 push_garmin.py --email you@example.com --only run      --limit 1
python3 push_garmin.py --email you@example.com --only strength --limit 1   # <- the uncertain one
python3 push_garmin.py --email you@example.com --only mobility --limit 1
python3 push_garmin.py --email you@example.com --from-week 1 --to-week 8
```

**The password is prompted, not exported.** Earlier versions of this file said to
`export GARMIN_PASSWORD=...`, which was poor advice: an exported secret persists in shell
history, is visible in `ps` while the process runs, and tends to end up committed in a dotfile.
`getpass` echoes nothing and keeps it in the one process. `$GARMIN_PASSWORD` is still honoured
for CI or a password-manager pipe, and the script warns when it uses one.

**Nothing in this repository should ever contain the password**, and the email is passed as an
argument rather than committed for the same reason — one less personal detail living in git.

### If it goes wrong: `--undo`

Every created workout id is appended to a local, gitignored manifest as it uploads.

```bash
python3 push_garmin.py --undo --dry-run                        # list what would go
python3 push_garmin.py --email you@example.com --undo          # type DELETE to confirm
```

It deletes newest-first and rewrites the manifest with only what it failed to remove, so a second
`--undo` retries the stragglers rather than re-deleting ids that are already gone.

**This is the reason it is safe to attempt a 202-workout push at all.** The ids in
`build_plan.py` are reverse-engineered; without a one-command rollback the alternative to a bad
bulk run is deleting 202 workouts by hand in the Garmin web UI, which nobody does — so they get
left there instead, and a calendar full of subtly wrong workouts is worse than an empty one.

### ID provenance — what is corroborated and what is not

| Value | Status |
| ----- | ------ |
| `sportTypeId 1` / `running` | Corroborated across community projects |
| `sportTypeId 5` / `strength_training` | **Corroborated** — several independent projects plus a Garmin forum payload |
| `sportTypeId 3` / `other` | Convention, uncorroborated |
| `stepTypeId 3` / `interval` | **Corroborated** |
| `stepTypeId 1` / `warmup`, `2` / `cooldown` | Widely-used convention, **not corroborated** — likeliest to be wrong |
| `conditionTypeId 2` / `time`, `1` / `lap.button` | Convention, uncorroborated |

On a failure the script now prints the **HTTP response body**, which is where Garmin names the
field it rejected. Paste that back and the fix is usually one constant.

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
