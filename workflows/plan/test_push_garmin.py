#!/usr/bin/env python3
"""
Offline test for push_garmin.py, against a FAKE Garmin client.

WHY THIS EXISTS. Two bugs reached the athlete's laptop in two days, and both were
in code paths that only run after a successful login — so neither `ast.parse` nor
`--dry-run` touched them:

  1. The dependency import sat after the password prompt, so a missing library
     made him type his Garmin password for nothing.
  2. A refactor's string replacement silently did not match, leaving the whole
     upload loop inside `get_password()` and `run_uploads` undefined. It failed
     with NameError the moment he entered his password.

Both are trivially catchable without a Garmin account. The only thing standing
between them and the user was that nothing ever exercised the post-login path.
This does, with a stub injected into sys.modules.

Run:  python3 workflows/plan/test_push_garmin.py
"""

import json
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FAILURES = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{'  ' + detail if detail and not cond else ''}")
    if not cond:
        FAILURES.append(name)


class FakeGarmin:
    """Stands in for garminconnect.Garmin. Records what it was asked to do."""

    instances = []

    def __init__(self, email=None, password=None, prompt_mfa=None):
        self.email, self.password, self.prompt_mfa = email, password, prompt_mfa
        self.uploaded, self.scheduled, self.deleted = [], [], []
        self.logged_in = False
        self.resume_should_fail = True
        self.garth = types.SimpleNamespace(dump=lambda path: None)
        FakeGarmin.instances.append(self)

    def login(self, tokenstore=None):
        # resume() calls login(TOKENSTORE) on a no-arg Garmin(); make that fail so
        # the test drives the full-login path.
        if tokenstore is not None:
            raise RuntimeError("no cached session")
        self.logged_in = True
        return True

    def upload_workout(self, payload):
        assert "_week" not in payload, "private keys must be stripped before sending"
        self.uploaded.append(payload)
        return {"workoutId": 1000 + len(self.uploaded)}

    def schedule_workout(self, wid, date):
        self.scheduled.append((wid, date))

    def delete_workout(self, wid):
        self.deleted.append(wid)


def install_stub():
    mod = types.ModuleType("garminconnect")
    mod.Garmin = FakeGarmin
    sys.modules["garminconnect"] = mod


def main():
    install_stub()
    import push_garmin as P

    print("push_garmin offline tests\n")

    # Keep the real manifest and tokenstore untouched.
    tmp = tempfile.mkdtemp()
    P.MANIFEST = os.path.join(tmp, "uploaded.jsonl")
    P.TOKENSTORE = os.path.join(tmp, "tokens")
    os.environ["GARMIN_PASSWORD"] = "test-password"

    # --- the regression that shipped: run_uploads must exist and be callable ---
    check("run_uploads is a module-level function", callable(getattr(P, "run_uploads", None)))
    check("get_password is a module-level function", callable(getattr(P, "get_password", None)))

    # --- get_password returns a VALUE, never an exit code ---
    pw = P.get_password("someone@example.com")
    check("get_password returns the password string", pw == "test-password", repr(pw))

    # --- the full upload path ---
    FakeGarmin.instances.clear()
    sys.argv = ["push_garmin.py", "--email", "someone@example.com",
                "--only", "run", "--limit", "2", "--sleep", "0"]
    rc = P.main()
    check("main() exits 0 on a clean run", rc == 0, f"got {rc}")

    api = next((i for i in FakeGarmin.instances if i.uploaded), None)
    check("a workout was uploaded", api is not None and len(api.uploaded) == 2,
          f"{len(api.uploaded) if api else 0} uploaded")
    check("each upload was scheduled", api is not None and len(api.scheduled) == 2)
    check("prompt_mfa was supplied to the client",
          any(i.prompt_mfa is not None for i in FakeGarmin.instances))

    # --- the manifest, which --undo depends on ---
    rows = [json.loads(l) for l in open(P.MANIFEST)] if os.path.exists(P.MANIFEST) else []
    check("manifest recorded every upload", len(rows) == 2, f"{len(rows)} rows")
    check("manifest rows carry a workoutId", all(r.get("workoutId") for r in rows))

    # --- --only filters by kind ---
    FakeGarmin.instances.clear()
    sys.argv = ["push_garmin.py", "--email", "x@y.z", "--only", "strength",
                "--limit", "1", "--sleep", "0"]
    P.main()
    api = next((i for i in FakeGarmin.instances if i.uploaded), None)
    check("--only strength sends a strength workout",
          api is not None and api.uploaded[0]["sportType"]["sportTypeKey"] == "strength_training")

    # --- --undo deletes exactly what was recorded ---
    FakeGarmin.instances.clear()
    sys.argv = ["push_garmin.py", "--email", "x@y.z", "--undo", "--dry-run"]
    rc = P.main()
    check("--undo --dry-run exits 0 and deletes nothing", rc == 0 and
          not any(i.deleted for i in FakeGarmin.instances))

    # --- a missing library must not reach the password prompt ---
    saved = sys.modules.pop("garminconnect")
    sys.argv = ["push_garmin.py", "--email", "x@y.z", "--only", "run", "--limit", "1"]
    rc = P.main()
    check("missing library exits 2 before prompting", rc == 2, f"got {rc}")
    sys.modules["garminconnect"] = saved

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
