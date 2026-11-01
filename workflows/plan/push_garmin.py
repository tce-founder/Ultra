#!/usr/bin/env python3
"""
Push the generated workouts to Garmin Connect, which syncs them to the Fenix 7 Pro.

RUN THIS ON YOUR OWN MACHINE, NOT HERE. It needs your Garmin Connect login, and
credentials should never be pasted into a chat or committed to a repository. It
reads them from the environment, never from a file and never from an argument
(arguments show up in shell history and in `ps`).

    pip install "garminconnect[workout]"
    python3 push_garmin.py --email you@example.com --dry-run

The password is PROMPTED, never passed as an argument and never read from a file
by default. An exported GARMIN_PASSWORD survives in shell history, is visible in
`ps` while the process runs, and tends to end up committed in a dotfile; $GARMIN_
PASSWORD is still honoured for CI or a password-manager pipe, but it is not the
recommended path and the script warns when it uses one.

    python3 push_garmin.py --dry-run                      # see what WOULD be sent
    python3 push_garmin.py --only run      --limit 1      # one of each sport first
    python3 push_garmin.py --only strength --limit 1      # <- the uncertain one
    python3 push_garmin.py --only mobility --limit 1
    python3 push_garmin.py --from-week 1 --to-week 8      # then a block at a time

WHY --dry-run IS THE DEFAULT POSTURE. Garmin publishes no consumer API for
structured workouts. `python-garminconnect` works against the same private
endpoints the web app uses:

    POST /workout-service/workout              -> creates, returns workoutId
    POST /workout-service/schedule/{workoutId} -> body {"date": "YYYY-MM-DD"}

The step-type and condition-type IDs in build_plan.py come from community
reverse-engineering, not documentation. Where they could be corroborated they have
been: sportTypeId 5 / "strength_training" and stepTypeId 3 / "interval" appear in
several independent community projects and in a Garmin forum payload. warmup (1)
and cooldown (2) are the widely-used convention but were NOT corroborated, so they
are the likeliest things to be wrong. They are the most likely thing in this
toolchain to be wrong or to have drifted, and a bad bulk run leaves 150 broken
workouts to delete by hand. So: dry-run, then ONE, then look at the watch, then
the rest. The ten minutes this costs is cheaper than the cleanup.

If the API has moved on and this stops working, the .ics file still carries the
whole plan and nothing is lost but convenience.
"""

import argparse
import getpass
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# Every created workout id is appended here as it uploads, so --undo can remove
# exactly what this script made without guessing from names. Gitignored.
MANIFEST = os.path.join(HERE, ".garmin_uploaded.jsonl")
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
    ap.add_argument("--email", default="", help="Garmin account email. Falls back to $GARMIN_EMAIL.")
    ap.add_argument("--from-week", type=int, default=1)
    ap.add_argument("--to-week", type=int, default=29)
    ap.add_argument("--limit", type=int, default=0, help="stop after N workouts (0 = no limit)")
    ap.add_argument("--only", default="", metavar="KIND",
                    help="restrict to one session kind: run|long|vert|strength|mobility|race. "
                         "Use this to smoke-test each sport separately — the strength sport ID is "
                         "the least certain value in the toolchain.")
    ap.add_argument("--dry-run", action="store_true", help="print the plan of record and exit")
    ap.add_argument("--no-schedule", action="store_true", help="create workouts but do not put them on dates")
    ap.add_argument("--sleep", type=float, default=1.0, help="seconds between calls; be polite to the endpoint")
    ap.add_argument("--undo", action="store_true",
                    help="DELETE every workout this script created, newest first, from the local "
                         "manifest. The recovery path for a bulk run that went wrong.")
    args = ap.parse_args()

    if args.undo:
        return undo(args)

    workouts = load(args.json, args.from_week, args.to_week)
    if args.only:
        workouts = [w for w in workouts if w.get("_kind") == args.only]
    if args.limit:
        workouts = workouts[:args.limit]

    if not workouts:
        print("nothing selected — check --from-week/--to-week")
        return 1

    import collections
    kinds = collections.Counter(w.get("_kind", "?") for w in workouts)
    print(f"{len(workouts)} workouts, weeks {args.from_week}-{args.to_week}, "
          f"{workouts[0]['_scheduleDate']} .. {workouts[-1]['_scheduleDate']}")
    print(f"  kinds: {dict(kinds)}")
    print(f"  sports: {dict(collections.Counter(w['sportType']['sportTypeKey'] for w in workouts))}")

    if args.dry_run:
        for w in workouts:
            steps = w["workoutSegments"][0]["workoutSteps"]
            mins = sum(s.get("endConditionValue", 0) for s in steps) / 60
            tag = "lap" if mins == 0 else f"{mins:.0f}m"
            print(f"  {w['_scheduleDate']}  W{w['_week']:02d}  {tag:>6}  "
                  f"{len(steps)} steps  {w['sportType']['sportTypeKey'][:8]:8}  {w['workoutName']}")
        print("\nDRY RUN — nothing sent. Re-run with --limit 1 to send a single workout.")
        return 0

    email = args.email or os.environ.get("GARMIN_EMAIL")
    if not email:
        print("ERROR: pass --email or set $GARMIN_EMAIL.", file=sys.stderr)
        return 2

    # PROMPT, don't read from the environment by preference. An exported
    # GARMIN_PASSWORD lands in shell history, in `ps` while the process runs, and
    # in any shell dotfile it gets pasted into. getpass echoes nothing and keeps the
    # password in this process only. The env var is still honoured for CI or for a
    # password manager piping it in, but it is no longer what the docs recommend.
    password = os.environ.get("GARMIN_PASSWORD")
    if password:
        print("using $GARMIN_PASSWORD (note: exported secrets persist in shell history)")
    else:
        try:
            password = getpass.getpass(f"Garmin password for {email} (not echoed): ")
        except (EOFError, KeyboardInterrupt):
            print("\naborted — no password entered.", file=sys.stderr)
            return 2
    if not password:
        print("ERROR: empty password.", file=sys.stderr)
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
            with open(MANIFEST, "a") as fh:
                fh.write(json.dumps({"workoutId": wid, "date": when, "name": name}) + "\n")
            print(f"  OK   {when}  {name}  (id {wid})")
            ok += 1
        except Exception as exc:                      # noqa: BLE001 — report and continue
            print(f"  FAIL {when}  {name}: {type(exc).__name__}: {exc}")
            # The HTTP body is where Garmin says WHICH field it rejected, and the
            # exception string usually drops it. Without this a wrong sport or
            # step-type id produces an unactionable "400 Bad Request".
            body = getattr(getattr(exc, "response", None), "text", None)
            if body:
                print(f"       response: {body[:400]}")
            fail += 1
            if fail >= 3 and ok == 0:
                print("\nThree failures and no successes — stopping rather than grinding through 150.")
                print("The step/condition type IDs in build_plan.py are the first thing to check.")
                return 1
        time.sleep(args.sleep)

    print(f"\n{ok} uploaded, {fail} failed")
    if ok:
        print(f"Recorded in {os.path.relpath(MANIFEST, HERE)} — `--undo` removes exactly these.")
        print("Sync the watch (Garmin Connect app, or plug in) and check Training > Workouts.")
    return 0 if not fail else 1


def undo(args):
    """Delete every workout recorded in the manifest, newest first.

    This exists because the sport and step-type ids in build_plan.py are
    reverse-engineered. If a bulk run lands 202 subtly wrong workouts, the
    alternative to this command is deleting them one at a time in the Garmin web
    UI, which nobody will do — so they would be left there instead, and the
    calendar would be worse than empty.
    """
    if not os.path.exists(MANIFEST):
        print(f"no manifest at {MANIFEST} — nothing this script created is recorded.")
        return 1
    rows = [json.loads(l) for l in open(MANIFEST) if l.strip()]
    if not rows:
        print("manifest is empty.")
        return 0

    print(f"{len(rows)} workouts recorded, {rows[0]['date']} .. {rows[-1]['date']}")
    if args.dry_run:
        for r in rows:
            print(f"  would delete  {r['date']}  {r['workoutId']}  {r['name']}")
        print("\nDRY RUN — nothing deleted.")
        return 0

    confirm = input(f"Delete all {len(rows)} from Garmin Connect? Type DELETE to confirm: ")
    if confirm.strip() != "DELETE":
        print("aborted.")
        return 1

    email = args.email or os.environ.get("GARMIN_EMAIL")
    if not email:
        print("ERROR: pass --email or set $GARMIN_EMAIL.", file=sys.stderr)
        return 2
    password = os.environ.get("GARMIN_PASSWORD") or getpass.getpass(
        f"Garmin password for {email} (not echoed): ")
    try:
        from garminconnect import Garmin
    except ImportError:
        print('ERROR: pip install "garminconnect[workout]"', file=sys.stderr)
        return 2
    api = Garmin(email, password)
    api.login()

    kept, gone = [], 0
    for r in reversed(rows):
        try:
            api.delete_workout(r["workoutId"])
            print(f"  deleted  {r['date']}  {r['name']}")
            gone += 1
        except Exception as exc:                      # noqa: BLE001
            print(f"  FAILED   {r['date']}  {r['name']}: {type(exc).__name__}: {exc}")
            kept.append(r)
        time.sleep(args.sleep)

    # Rewrite the manifest with only what could not be deleted, so a second --undo
    # retries exactly the stragglers rather than re-deleting ids that are gone.
    with open(MANIFEST, "w") as fh:
        for r in reversed(kept):
            fh.write(json.dumps(r) + "\n")
    print(f"\n{gone} deleted, {len(kept)} left in the manifest"
          f"{' — re-run --undo to retry those' if kept else ''}")
    return 0 if not kept else 1


if __name__ == "__main__":
    sys.exit(main())
