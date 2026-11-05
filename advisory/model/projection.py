#!/usr/bin/env python3
"""
Project a target-race time from a known result on comparable terrain.

WHY THIS EXISTS. The athlete finished the Mount Mitchell Heartbreaker (50 mi,
~12,000 ft) in March 2026 — the same start line and much of the same terrain as
Hellbender. That is the single most informative data point available for the
question that actually decides this build:

    IS A 40-HOUR CUTOFF ACHIEVABLE, AND BY HOW MUCH?

Everything else in the plan assumes the answer is yes. If it is marginal, the plan
should be arguing about cutoff splits rather than about vert targets, and it would
be better to know that in October than at mile 50 in May.

WHAT THIS IS NOT. Not a prediction. Trail-time scaling is a rule of thumb with no
useful evidence base — there is no validated model for 50-to-100-mile scaling on
mountain terrain, and anyone who tells you otherwise is selling a calculator. So:

  - every output is a RANGE, never a number
  - the range comes from varying the two assumptions that matter most
  - the night penalty is ADDITIVE and separate, because a 14-hour race contains no
    night and a 100-miler contains most of one — folding that into an exponent
    hides the single biggest difference between the two events
  - the result is graded, and it inherits UNVERIFIED from the method regardless of
    how well-measured the input time is

Usage:
    python3 advisory/model/projection.py 14:30        # a known Heartbreaker time
    python3 advisory/model/projection.py 14:30 16:00  # sensitivity across times
    python3 advisory/model/projection.py              # the table, no known time
"""

import sys

from inputs import Input, derive

# ── The two races ────────────────────────────────────────────────────────────
KNOWN = {"name": "Mount Mitchell Heartbreaker 50M", "miles": 50.0, "vert_ft": 12000}
TARGET = {"name": "Hellbender 100", "miles": 102.3, "vert_ft": 21500, "cutoff_h": 40.0}

# ── The two assumptions, each given as a range rather than a value ───────────
# VERT EQUIVALENCE: how many flat miles a 1,000 ft climb is "worth". Trail
# convention spans roughly 1 to 2; nothing establishes either end.
VERT_FACTOR = (1.0, 2.0)

# FATIGUE EXPONENT: time scales as (equivalent distance ratio) ** k. Riegel's
# road exponent is about 1.06; ultra-trail practice suggests materially higher
# over a doubling of distance. 1.05 is optimistic, 1.20 is pessimistic.
EXPONENT = (1.05, 1.20)

# NIGHT AND SLEEP PENALTY, additive hours. The Heartbreaker is a daylight race.
# Hellbender puts most athletes out for a full night and into a second day, and
# the cost shows up as slower movement and longer stops rather than as a
# different pace curve. Practitioner estimate, wide on purpose.
NIGHT_PENALTY_H = (2.0, 5.0)


def equivalent_miles(miles, vert_ft, vert_factor):
    return miles + (vert_ft / 1000.0) * vert_factor


def parse_hm(s):
    if ":" in s:
        h, m = s.split(":", 1)
        return int(h) + int(m) / 60.0
    return float(s)


def fmt_h(h):
    return f"{int(h)}h{int(round((h - int(h)) * 60)):02d}"


def dnf_equivalent(miles_done, hours, vert_factor=1.5, exponent=1.1):
    """Scale an UNFINISHED effort up to a full-distance equivalent.

    The athlete covered `miles_done` of the Heartbreaker in `hours` and stopped.
    This extrapolates to what the full 50 would have taken AT THE SAME EFFORT,
    assuming vert accrued proportionally to distance.

    READ THE WARNING. If the stop was caused by an injury that developed DURING
    the race, the observed pace is an INJURED pace, and extrapolating it projects
    the injured athlete rather than the healthy one. The result is then a floor on
    capability, not an estimate of it, and how big the gap is depends entirely on
    how early the injury started — which the number cannot tell you.
    """
    vert_done = KNOWN["vert_ft"] * miles_done / KNOWN["miles"]
    eq_done = equivalent_miles(miles_done, vert_done, vert_factor)
    eq_full = equivalent_miles(KNOWN["miles"], KNOWN["vert_ft"], vert_factor)
    return hours * (eq_full / eq_done) ** exponent


def project(known_h):
    """Returns (low, high) projected hours across the assumption ranges."""
    out = []
    for vf in VERT_FACTOR:
        ek = equivalent_miles(KNOWN["miles"], KNOWN["vert_ft"], vf)
        et = equivalent_miles(TARGET["miles"], TARGET["vert_ft"], vf)
        for k in EXPONENT:
            for night in NIGHT_PENALTY_H:
                out.append(known_h * (et / ek) ** k + night)
    return min(out), max(out)


def report(known_h, dnf_from=None):
    # A DNF-derived equivalent must not be labelled a finish. The source string ends
    # up in the Input, which is the thing downstream reads and quotes.
    if dnf_from:
        src = (f"EXTRAPOLATED from a DNF: {dnf_from[0]:g} mi of {KNOWN['miles']:g} in "
               f"{fmt_h(dnf_from[1])}, March 2026. NOT a finish time")
        pop = ("this athlete, this course, 19 months out, AND INJURED DURING THE EFFORT — "
               "the observed pace is an injured pace, so this is a floor on capability")
    else:
        src = f"athlete's {KNOWN['name']} finish, March 2026"
        pop = "this athlete, this course, 19 months before the target race"
    known = Input(known_h, "hours", src, "REPORTED", population=pop,
                  note="self-reported; not checked against official results")
    lo, hi = project(known_h)
    cutoff = TARGET["cutoff_h"]

    method = Input(1.0, "scaling factor", "trail-time rule of thumb; no validated model exists "
                   "for 50-to-100-mile scaling on mountain terrain", "UNVERIFIED",
                   population="none — this is a convention, not a measurement")
    mid = derive((lo + hi) / 2, "hours", known, method,
                 note="midpoint of the assumption ranges. NOT a prediction — see the spread. "
                      "Graded UNVERIFIED by the METHOD, however well the input time is known.")

    print(f"\n{'=' * 74}")
    print(f"  {KNOWN['name']}  {fmt_h(known_h)}   ->   {TARGET['name']}")
    print(f"{'=' * 74}")
    print(f"  input         {known}")
    print(f"  projected     {fmt_h(lo)} to {fmt_h(hi)}    (spread {hi - lo:.1f} h)")
    print(f"  midpoint      {fmt_h(mid.value)}  [{mid.grade}]")
    print(f"  cutoff        {fmt_h(cutoff)}")

    margin_lo, margin_hi = cutoff - hi, cutoff - lo
    if hi <= cutoff:
        verdict = f"INSIDE the cutoff across every assumption. Margin {fmt_h(margin_lo)} at worst."
    elif lo >= cutoff:
        verdict = ("OUTSIDE the cutoff across every assumption. On this evidence the 40-hour "
                   "limit is not achievable from this starting point.")
    else:
        pct = (cutoff - lo) / (hi - lo)
        verdict = (f"MARGINAL — inside on optimistic assumptions, outside on pessimistic ones. "
                   f"Roughly {pct:.0%} of the assumption space finishes.")
    print(f"  verdict       {verdict}")
    print(f"\n  To finish inside {fmt_h(cutoff)} you need the equivalent of a "
          f"{fmt_h(known_h * cutoff / hi)}-{fmt_h(known_h * cutoff / lo)} Heartbreaker.")
    return lo, hi


def table():
    print(f"\n  Sensitivity — what a given {KNOWN['name']} time implies\n")
    print(f"  {'Heartbreaker':>14}   {'Hellbender range':>22}   {'vs 40 h cutoff'}")
    print(f"  {'-' * 14}   {'-' * 22}   {'-' * 26}")
    for hm in (11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 16.5):
        lo, hi = project(hm)
        if hi <= 40:
            v = "inside, all assumptions"
        elif lo >= 40:
            v = "OUTSIDE, all assumptions"
        else:
            v = f"marginal ({(40 - lo) / (hi - lo):.0%} finishes)"
        print(f"  {fmt_h(hm):>14}   {fmt_h(lo) + ' – ' + fmt_h(hi):>22}   {v}")
    # Computed, not asserted. The first draft hardcoded "13-14 h" under a table that
    # showed inside-all-assumptions through 15h00.
    safe = marginal = None
    h = 8.0
    while h < 24.0:
        lo, hi = project(h)
        if hi <= TARGET["cutoff_h"]:
            safe = h
        elif marginal is None:
            marginal = h
        h += 0.25
    print(f"\n  Computed breakpoints:")
    print(f"    up to {fmt_h(safe)}   finishes on EVERY assumption")
    print(f"    from {fmt_h(marginal)}   the cutoff becomes the objective rather than a formality")


def main():
    args = sys.argv[1:]
    dnf = None
    if args and args[0] == "--dnf":
        if len(args) < 3:
            print("usage: projection.py --dnf <miles_completed> <time>  e.g. --dnf 45 15:00")
            return 2
        miles, dnf_t = float(args[1]), parse_hm(args[2])
        dnf = dnf_equivalent(miles, dnf_t)
        args = [f"{int(dnf)}:{int(round((dnf-int(dnf))*60)):02d}"]
        print(f"\n  DNF INPUT: {miles:g} mi of {KNOWN['miles']:g} in {fmt_h(dnf_t)}")
        print(f"  -> {fmt_h(dnf)} full-distance equivalent at the same effort")
        print(f"  -> that is {'PAST' if dnf > 16.5 else 'inside'} the race's own 16h30 cutoff")
        print(f"  WARNING: if the stop was caused by an injury that developed during the race,")
        print(f"  this is an INJURED pace. The projection below is then a FLOOR on capability,")
        print(f"  not an estimate of it, and the gap depends on how early the injury started.")
    print(f"\n  ASSUMPTIONS (both ranges, neither established)")
    print(f"    vert equivalence   {VERT_FACTOR[0]}–{VERT_FACTOR[1]} flat miles per 1,000 ft")
    print(f"    fatigue exponent   {EXPONENT[0]}–{EXPONENT[1]} on equivalent-distance ratio")
    print(f"    night penalty      +{NIGHT_PENALTY_H[0]}–{NIGHT_PENALTY_H[1]} h, additive")
    print(f"    {KNOWN['name']}: {KNOWN['miles']} mi, {KNOWN['vert_ft']:,} ft")
    print(f"    {TARGET['name']}: {TARGET['miles']} mi, {TARGET['vert_ft']:,} ft, "
          f"{TARGET['cutoff_h']:.0f} h cutoff")

    if not args:
        table()
        print("\n  Pass a known time to project from it:  python3 projection.py 14:30")
        return 0

    for a in args:
        report(parse_hm(a), dnf_from=(miles, dnf_t) if dnf else None)
    print(f"\n  GRADE NOTE: every projection above is UNVERIFIED regardless of how well the")
    print(f"  input time is known, because the METHOD is a rule of thumb. Use the spread to")
    print(f"  decide, never the midpoint.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
