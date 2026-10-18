#!/usr/bin/env python3
"""
Push the generated workouts to Garmin Connect, which syncs them to the Fenix 7 Pro.

RUN THIS ON YOUR OWN MACHINE, NOT HERE. It needs your Garmin Connect login, and
credentials should never be pasted into a chat or committed to a repository. It
reads them from the environment, never from a file and never from an argument
(arguments show up in shell history and in `ps`).

    pip install "garminconnect[workout]"
    export GARMIN_EMAIL='you@example.com'
    export GARMIN_PASSWORD='...'          # or use a .netrc / password manager export

    python3 push_garmin.py --dry-run                 # see what WOULD be sent
    python3 push_garmin.py --limit 1                 # send ONE, check the watch
    python3 push_garmin.py --from-week 1 --to-week 8 # then a block at a time

WHY --dry-run IS THE DEFAULT POSTURE. Garmin publishes no consumer API for
structured workouts. `python-garminconnect` works against the same private
endpoints the web app uses:

    POST /workout-service/workout              -> creates, returns workoutId
    POST /workout-service/schedule/{workoutId} -> body {"date": "YYYY-MM-DD"}

The step-type and condition-type IDs in build_plan.py come from community
reverse-engineering, not documentation. They are the most likely thing in this
toolchain to be wrong or to have drifted, and a bad bulk run leaves 150 broken
workouts to delete by hand. So: dry-run, then ONE, then look at the watch, then
the rest. The ten minutes this costs is cheaper than the cleanup.

If the API has moved on and this stops working, the .ics file still carries the
whole plan and nothing is lost but convenience.
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JSON = os.path.normpath(
    os.path.join(HERE, "..", "..", "advisory", "analysis", "plan", "garmin_workouts.json"))


def load(path, from_week, to_week):
    with open(path) as fh:
        workouts = json.load(fh)
    return [w for w in workouts if from_week <= w.get("_week", 0) <= to_week]


def strip_private(w):
    """Keys prefixed with _ are ours, not Garmin's. Sending them is how a payload
    gets rejected with a 400 that names nothing useful."""
    return {k: v for k, v in w.items() if not k.startswith("_")}


def main():
    ap = argparse.ArgumentParser(description="Upload and schedule the Hellbender plan on Garmin Connect.")
    ap.add_argument("--json", default=DEFAULT_JSON)
    ap.add_argument("--from-week", type=int, default=1)
    ap.add_argument("--to-week", type=int, default=29)
    ap.add_argument("--limit", type=int, default=0, help="stop after N workouts (0 = no limit)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan of record and exit")
    ap.add_argument("--no-schedule", action="store_true", help="create workouts but do not put them on dates")
    ap.add_argument("--sleep", type=float, default=1.0, help="seconds between calls; be polite to the endpoint")
    args = ap.parse_args()

    workouts = load(args.json, args.from_week, args.to_week)
    if args.limit:
        workouts = workouts[:args.limit]

    if not workouts:
        print("nothing selected — check --from-week/--to-week")
        return 1

    print(f"{len(workouts)} workouts, weeks {args.from_week}-{args.to_week}, "
          f"{workouts[0]['_scheduleDate']} .. {workouts[-1]['_scheduleDate']}")

    if args.dry_run:
        for w in workouts:
            steps = w["workoutSegments"][0]["workoutSteps"]
            mins = sum(s["endConditionValue"] for s in steps) / 60
            print(f"  {w['_scheduleDate']}  W{w['_week']:02d}  {mins:5.0f} min  "
                  f"{len(steps)} steps  {w['workoutName']}")
        print("\nDRY RUN — nothing sent. Re-run with --limit 1 to send a single workout.")
        return 0

    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    if not email or not password:
        print("ERROR: set GARMIN_EMAIL and GARMIN_PASSWORD in the environment.", file=sys.stderr)
        print("Never pass credentials as arguments — they land in shell history and ps.", file=sys.stderr)
        return 2

    try:
        from garminconnect import Garmin
    except ImportError:
        print('ERROR: pip install "garminconnect[workout]"', file=sys.stderr)
        return 2

    api = Garmin(email, password)
    api.login()
    print("logged in")

    ok = fail = 0
    for w in workouts:
        name, when = w["workoutName"], w["_scheduleDate"]
        try:
            created = api.upload_workout(strip_private(w))
            wid = created.get("workoutId") or created.get("workoutIdStr")
            if not wid:
                raise RuntimeError(f"no workoutId in response: {str(created)[:200]}")
            if not args.no_schedule:
                api.schedule_workout(wid, when)
            print(f"  OK   {when}  {name}  (id {wid})")
            ok += 1
        except Exception as exc:                      # noqa: BLE001 — report and continue
            print(f"  FAIL {when}  {name}: {type(exc).__name__}: {exc}")
            fail += 1
            if fail >= 3 and ok == 0:
                print("\nThree failures and no successes — stopping rather than grinding through 150.")
                print("The step/condition type IDs in build_plan.py are the first thing to check.")
                return 1
        time.sleep(args.sleep)

    print(f"\n{ok} uploaded, {fail} failed")
    if ok:
        print("Sync the watch (Garmin Connect app, or plug in) and check Training > Workouts.")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
