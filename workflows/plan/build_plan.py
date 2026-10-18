#!/usr/bin/env python3
"""
Hellbender 100 training plan — single source of truth.

Emits three artifacts from one plan definition, so they cannot drift:

  advisory/analysis/plan/plan.md              human-readable 29-week plan
  advisory/analysis/plan/hellbender-2027.ics  Google Calendar import
  advisory/analysis/plan/garmin_workouts.json structured workouts for push_garmin.py

WHY A GENERATOR AND NOT A WRITTEN PLAN. A 29-week plan is ~190 sessions. Hand-written,
the calendar and the document disagree within a fortnight of the first change, and the
athlete trains off whichever one they opened. Generated, a change to the phase table
rewrites all three outputs together.

THE DESIGN CONSTRAINT THIS PLAN IS BUILT AROUND. The athlete has 6-7 days a week
available and is currently running under 20 miles a week. Available time is therefore
NOT the binding constraint — connective-tissue adaptation rate is. Cardiovascular
fitness will arrive months before tendon, bone and fascia can absorb the volume it
invites, and the gap between those two clocks is where the injury happens. Nearly every
conservative choice below (the 8-week base phase, down weeks every 4th week, hiking
counted as training, vert deferred to week 9) exists to defend that gap against an
athlete who has the hours to go faster and will want to.

Usage:  python3 workflows/plan/build_plan.py
        python3 workflows/plan/build_plan.py --check   # validate, write nothing
"""

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "advisory", "analysis", "plan")

# ── Race and athlete parameters ──────────────────────────────────────────────
RACE_NAME = "Hellbender 100"
RACE_DATE = date(2027, 5, 7)          # Friday. CONFIRM — see hellbender-100.md
RACE_START_TIME = "04:00"             # assumed; confirm against the race site
WEEK1_MONDAY = date(2026, 10, 19)
TIMEZONE = "America/New_York"
RACE_MILES = 102.3
RACE_VERT_FT = 21500                  # listings disagree, 20,000-21,540; see race page
RACE_CUTOFF_H = 40

DEFAULT_TIMES = {                     # local start time per session kind
    "run": "06:00", "long": "06:00", "vert": "06:00",
    "strength": "17:30", "mobility": "21:00", "race": RACE_START_TIME,
}

# ── Phases ───────────────────────────────────────────────────────────────────
PHASES = [
    ("Base 1 — tissue tolerance", 1, 8),
    ("Base 2 — aerobic volume + vert", 9, 16),
    ("Specific — mountain, dark, fuelled", 17, 25),
    ("Taper", 26, 28),
    ("Race week", 29, 29),
]

def phase_for(week):
    for name, lo, hi in PHASES:
        if lo <= week <= hi:
            return name
    raise ValueError(week)

# Weekly training hours (running + vert + strength; daily mobility excluded).
# Down weeks every 4th. The ramp averages well under 10%/week across the build.
WEEK_HOURS = {
    1: 3.0,  2: 3.5,  3: 4.0,  4: 3.0,
    5: 4.5,  6: 5.0,  7: 5.5,  8: 4.5,
    9: 6.5, 10: 7.5, 11: 8.0, 12: 5.5,
    13: 8.5, 14: 9.0, 15: 9.5, 16: 6.5,
    17: 10.0, 18: 13.0, 19: 12.0, 20: 8.0,
    21: 12.0, 22: 16.5, 23: 7.0, 24: 12.0,
    25: 14.0, 26: 10.0, 27: 7.5, 28: 5.0, 29: 2.5,
}

# Weekly vertical gain target, FEET. The race is ~21,500 ft; peak weeks reach
# roughly a third of that, which is as close as a working amateur gets.
WEEK_VERT_FT = {
    1: 0, 2: 0, 3: 400, 4: 300, 5: 600, 6: 2500, 7: 800, 8: 600,
    9: 1200, 10: 3500, 11: 1600, 12: 1000, 13: 2000, 14: 4500, 15: 2500, 16: 1500,
    17: 3000, 18: 11000, 19: 4000, 20: 2500, 21: 6500, 22: 14000, 23: 1500, 24: 5000,
    25: 8000, 26: 3500, 27: 2000, 28: 1000, 29: RACE_VERT_FT,
}

DOWN_WEEKS = {4, 8, 12, 16, 20, 23, 27, 28}

# Weeks where the athlete is still adding RUNNING DAYS rather than minutes. Going
# from 1-2 runs a week to five in one step is a frequency jump, and frequency jumps
# are the cheap kind only if each session stays short — so these weeks run four days
# and Wednesday is a mobility-and-shoe-check day instead of a fifth run.
RETURN_TO_RUN_WEEKS = {1, 2}

# ── Special weeks ────────────────────────────────────────────────────────────
# Mountain trips are weekend-only: the athlete is 3-5 hours from sustained climbs.
# Fridays in these weeks become travel/rest rather than training.
MOUNTAIN_WEEKS = {
    6:  "Thanksgiving weekend — first mountain block. Hike-heavy, no pace targets.",
    10: "Holiday mountain block. Long hike/run Sat, shorter Sun.",
    14: "Mountain block — first real back-to-back.",
    18: "ART LOEB TRAVERSE — Presidents' Day weekend. Take the Monday if you can; this is the biggest day of the build before the Heartbreaker and the drive home afterwards is long.",
    21: "COURSE RECON 1 — Old Fort / Curtis Creek. Keep it moderate: the Heartbreaker is six days later and this is a look, not a test.",
    25: "COURSE RECON 2 — peak back-to-back on Hellbender's own course. Night section on the Saturday: start late and finish after dark.",
    27: "Final light course look. Legs stay fresh; this is reconnaissance, not training.",
}

# Big objective days. Each dominates its week, so the rest of the week is sized around
# it rather than the other way round. `kind` distinguishes an entered race from a big
# unsupported training day — the validator excludes races from the weekly-hours
# reconciliation, because a 13-hour race is not a training-hours figure.
TUNE_UPS = {
    15: {"name": "50K tune-up race — NOT YET CHOSEN", "minutes": 390, "kind": "race", "vert_ft": 3500,
         "note": "First ultra of the build. Rehearse fuelling at 60 g/h. No time goal. "
                 "Race still to be picked — see plan/tune-up-races.md."},
    18: {"name": "Art Loeb Trail traverse", "minutes": 540, "kind": "long", "vert_ft": 9200,
         "note": "30.1 mi point-to-point, ~9,200 ft, Davidson River to Camp Daniel Boone. "
                 "NOT a race — a big unsupported day, and the largest single effort before the "
                 "Heartbreaker. Budget 9 h; it may take 11-12 and that is fine. "
                 "BAIL POINT: FS 816 at Black Balsam, roughly two-thirds in and road-accessible — "
                 "if you are more than 2 h over budget by Gloucester Gap (mile 12.3), stop there "
                 "instead. Needs a car shuttle at both ends. February on the balds is genuinely "
                 "exposed: this is the cold-kit test for Hellbender's 6,684 ft summit."},
    22: {"name": "Mount Mitchell Heartbreaker 50M", "minutes": 810, "kind": "race", "vert_ft": 12000,
         "note": "THE DRESS REHEARSAL. Starts at Camp Grier — the same start line as Hellbender. "
                 "~12,000 ft, 5:30 am start, 16.5 h cutoff. Climbs Mt Mitchell via the Black "
                 "Mountain Crest and finishes over Heartbreak Ridge, so it is Hellbender terrain "
                 "at race effort. Full kit, full race fuelling, nothing untested."},
}

# ── Session model ────────────────────────────────────────────────────────────
@dataclass
class Session:
    day_offset: int          # 0 = Monday
    kind: str                # run|long|vert|strength|mobility|rest|race
    title: str
    minutes: int
    vert_ft: int = 0
    notes: str = ""
    garmin: bool = False     # push this one to the watch

    @property
    def dayname(self):
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][self.day_offset]


# Fraction of weekly RUNNING minutes per day, by phase.
#
# MONDAY (0) CARRIES NO WEIGHT IN ANY PHASE, deliberately. The first draft gave it a
# small recovery run in the two middle phases and the validator rejected the result:
# it left an athlete with 6-7 available days and no full rest day in any week from
# week 9 onward. Having the time to train seven days is exactly why the schedule has
# to refuse the seventh — the constraint being defended here is tissue adaptation,
# and it is defended on the days off, not the days on.
WEIGHTS = {
    "Base 1 — tissue tolerance":          {1: .16, 2: .11, 3: .16, 5: .37, 6: .20},
    "Base 2 — aerobic volume + vert":     {1: .14, 2: .17, 3: .14, 4: .07, 5: .33, 6: .15},
    "Specific — mountain, dark, fuelled": {1: .13, 2: .16, 3: .13, 4: .06, 5: .33, 6: .19},
    "Taper":                              {1: .15, 2: .15, 3: .14, 4: .06, 5: .31, 6: .19},
}

# Tuesday and Thursday: paired with the easy aerobic days, and kept clear of the
# Wednesday vert session and the weekend long runs.
STRENGTH_DAYS = {"Base 1 — tissue tolerance": [1, 3],
                 "Base 2 — aerobic volume + vert": [1, 3],
                 "Specific — mountain, dark, fuelled": [1, 3],
                 "Taper": [1]}
STRENGTH_MIN = 45


def r5(x):
    """Round to 5 minutes. A plan with 47-minute sessions is a plan nobody follows."""
    return max(20, int(round(x / 5.0) * 5))


def build_week(w):
    """One week of sessions."""
    ph = phase_for(w)
    hours = WEEK_HOURS[w]
    vert = WEEK_VERT_FT[w]
    sessions = []

    if w == 29:
        return race_week(), ph

    strength_days = STRENGTH_DAYS[ph]
    run_min = hours * 60 - STRENGTH_MIN * len(strength_days)
    weights = dict(WEIGHTS[ph])
    if w in RETURN_TO_RUN_WEEKS:
        weights.pop(2, None)        # Wednesday becomes the shoe-and-mobility check
    mountain = w in MOUNTAIN_WEEKS
    tune_up = TUNE_UPS.get(w)

    if tune_up:
        # The big day IS the long run. Everything else shrinks around it, and SUNDAY IS
        # DROPPED ENTIRELY — after 9-13 hours on Saturday the next day is rest, not a
        # token jog. The first version left a 20-minute run the day after a 50-mile race.
        weights = {1: .35, 2: .30, 3: .35}
        run_min = max(0, run_min - tune_up["minutes"])
        # The big day carries its own vert; only the remainder is spread across the week.
        vert = max(0, vert - tune_up["vert_ft"])

    if mountain:
        # Friday is travel. Saturday and Sunday carry the block.
        weights.pop(4, None)
        for d, bump in ((5, 1.25), (6, 1.35)):
            if d in weights:
                weights[d] *= bump

    total_w = sum(weights.values()) or 1.0

    for d in range(7):
        frac = weights.get(d, 0)
        mins = r5(run_min * frac / total_w) if frac else 0

        if d in strength_days:
            sessions.append(Session(d, "strength", strength_label(ph, d), STRENGTH_MIN,
                                    notes=strength_notes(ph, d)))

        if tune_up and d == 5:
            sessions.append(Session(d, tune_up["kind"], tune_up["name"], tune_up["minutes"],
                                    tune_up["vert_ft"], tune_up["note"],
                                    garmin=tune_up["kind"] != "race"))
            continue

        if not frac:
            if d == 0:
                sessions.append(Session(d, "rest", "Rest", 0,
                                        notes="Full rest. This is the session that makes the others work."))
            elif tune_up and d == 6:
                sessions.append(Session(d, "rest", "Rest — walk only if you want to", 0,
                                        notes="Day after a big effort. Eat, sleep, drive home gently. "
                                              "Nothing you do today improves May; plenty of things could cost it."))
            elif w in RETURN_TO_RUN_WEEKS and d == 2:
                sessions.append(Session(d, "mobility", "Shoe audit + mobility", 25, 0,
                    "NOT a run day — the gap is deliberate while running frequency climbs. "
                    "Week 1: lay out every pair you own and press a thumb into the back of each "
                    "heel counter. Anything stiff, high, or with a seam over the Achilles goes in "
                    "the bin, not the rotation — that shoe is what caused the 2026 bursitis. "
                    "Then the usual 15 min of ankle, calf and hip work, plus heel-lock lacing "
                    "practice.")) 
            elif mountain and d == 4:
                sessions.append(Session(d, "rest", "Travel to the mountains", 0,
                                        notes="Drive. Eat properly on the road; arriving under-fuelled wastes the weekend."))
            continue

        kind, title, note, vshare = classify(ph, d, w, mountain)
        sessions.append(Session(d, kind, title, mins, int(vert * vshare), note,
                                garmin=kind in ("run", "long", "vert")))

    return sessions, ph


def classify(ph, d, w, mountain):
    """What a given day is for, and its share of the week's vert."""
    base1 = ph.startswith("Base 1")
    if d == 5:
        if mountain:
            return ("long", "Mountain long run / hike", MOUNTAIN_WEEKS[w], .55)
        return ("long", "Long run", "Conversational throughout. Walk the steep bits on purpose — "
                "you will walk them in the race.", .30 if not base1 else .40)
    if d == 6:
        if mountain:
            return ("long", "Back-to-back day 2", "On tired legs by design. This is the session that most "
                    "resembles hour 20 of the race.", .35)
        if base1:
            return ("run", "Recovery run", "Slow enough to feel pointless. That is the point.", .05)
        return ("long", "Medium-long run", "Back-to-back with Saturday. Slower than yesterday.", .20)
    if d == 2 and not base1:
        return ("vert", "Vert session — stair machine or treadmill incline", VERT_NOTE, .35)
    if d == 1:
        return ("run", "Aerobic run" + ("" if base1 else " + strides"),
                "Easy. Add 6 x 20 s strides at the end once base is in." if not base1
                else "Easy, conversational. No strides yet.", .05)
    if d == 3:
        return ("run", "Aerobic run",
                "Easy, conversational." if base1 else
                "Easy. If yesterday's vert left you sore, make this shorter — never faster.", .05)
    if d == 4:
        return ("run", "Easy run", "Short and genuinely easy. Drop it without guilt on a bad week.", 0)
    return ("run", "Easy run", "Easy.", 0)


HEEL_WARNING = (
    " ** HEEL WATCH: steep climbing holds the ankle in dorsiflexion, which drives the shoe's "
    "heel counter into the back of the calcaneus — the exact mechanism that caused the 2026 "
    "bursitis. Use a shoe with a soft, low heel collar; lock the heel with the top eyelet so it "
    "does not piston; stop at the FIRST sign of posterior heel soreness, not the second. "
    "Substitute if it niggles: uphill treadmill WALKING in a higher-drop shoe, or a weighted "
    "pack hike, or the bike for the aerobic half. **")

VERT_NOTE = ("Stair machine (StepMill) preferred — far steeper than a treadmill's 15% ceiling. "
             "DO NOT hold the handrail; it removes a large and unrecorded share of the work. "
             "Treadmill at max incline is the alternative. Neither trains DESCENDING, which is "
             "what actually breaks down at Hellbender — that is what the mountain weekends and "
             "the eccentric strength work are for." + HEEL_WARNING)


# Keyed on the FIRST strength day in STRENGTH_DAYS, not a hardcoded weekday. The
# two were the same number until the rest-day fix moved strength from Wed/Fri to
# Tue/Thu, after which every session in the plan rendered as "Strength B".
def strength_label(ph, d):
    return "Strength A — heavy lower" if d == STRENGTH_DAYS[ph][0] else "Strength B — unilateral + eccentric"


def strength_notes(ph, d):
    if d == STRENGTH_DAYS[ph][0]:
        return ("Back squat or trap-bar deadlift 4x5 @ heavy. Romanian deadlift 3x6. "
                "Standing calf raise 3x8 heavy, FLAT GROUND until week 9. Weighted step-up 3x6/leg. "
                "HIGH LOAD, low reps, long rests — the meta-analyses found high-load and combined "
                "formats improved running economy and submaximal/isometric circuits did not.")
    return ("Bulgarian split squat 3x8/leg. Single-leg RDL 3x8/leg. "
            "ECCENTRIC step-down 3x10/leg, 4 s lowering — this is the Hellbender-specific one; "
            "the race's damage is quadriceps braking on descents. "
            "Calf raise, bent-knee 3x12 — FLAT GROUND, not hanging off a step, until week 9: "
            "loaded end-range dorsiflexion is what irritates a posterior heel bursa. "
            "Side plank 3x40 s.")


def race_week():
    return [
        Session(0, "run", "Shakeout", 30, 0, "Easy. Legs should feel under-used all week. That is correct."),
        Session(1, "run", "Shakeout + 4 strides", 30, 0, "Last chance to feel fast. Keep it short."),
        Session(2, "rest", "Rest — pack and check kit", 0, 0,
                "Lay out drop bags. Check the mandatory kit list against what you own, not what you remember owning."),
        Session(3, "run", "Travel + 20 min shakeout", 20, 0,
                "Drive to Old Fort. Easy jog on arrival to settle the legs after the car."),
        Session(4, "race", f"{RACE_NAME} — {RACE_MILES} mi, ~{RACE_VERT_FT:,} ft", RACE_CUTOFF_H * 60,
                RACE_VERT_FT,
                "Effort ceiling for the first third, non-negotiable. Hike the climbs on a rule, not a feeling. "
                "Pace the descents by damage, not speed. Fuel from hour one. Never make an irreversible "
                "decision in the dark — hand the DNF list to your crew."),
        Session(6, "rest", "Finish / recover", 0, 0, "Eat. Sleep. Do not plan anything."),
    ]


# ── Output: plan.md ──────────────────────────────────────────────────────────
def week_start(w):
    return WEEK1_MONDAY + timedelta(weeks=w - 1)


def render_markdown(weeks):
    L = []
    L.append("---")
    L.append("title: Hellbender 100 — 29-week training plan")
    L.append("type: register")
    L.append("status: active")
    L.append(f"updated: {date.today().isoformat()}")
    L.append("---\n")
    L.append("# Hellbender 100 — 29-week plan\n")
    L.append("> **GENERATED** by `workflows/plan/build_plan.py`. Do not hand-edit — edit the")
    L.append("> generator and rebuild, or the calendar and the watch will disagree with this file.\n")
    L.append(f"**Race** {RACE_NAME}, {RACE_DATE:%a %-d %B %Y}, Old Fort NC · "
             f"{RACE_MILES} mi · ~{RACE_VERT_FT:,} ft · {RACE_CUTOFF_H} h cutoff\n")
    L.append(f"**Plan** Week 1 begins {WEEK1_MONDAY:%-d %B %Y}. 29 weeks.\n")

    L.append("## The one thing this plan is designed against\n")
    L.append("You have 6-7 days a week available and are currently running under 20 miles a week.")
    L.append("**Your constraint is not time. It is how fast tendon, bone and fascia adapt** — which is")
    L.append("far slower than your heart and lungs will. By February you will feel capable of much more")
    L.append("than your legs can structurally absorb, and that gap is where this build either survives")
    L.append("or ends. Every conservative choice here exists to defend it.\n")
    L.append("**If you take one rule from this document:** on a week where you feel great and have a free")
    L.append("afternoon, do not add the session. Bank it. The plan has down weeks for a reason and the")
    L.append("athlete who deletes them is the athlete who does not start in May.\n")

    L.append("## Phases\n")
    L.append("| Phase | Weeks | Dates | Purpose |")
    L.append("| ----- | ----- | ----- | ------- |")
    purposes = {
        "Base 1 — tissue tolerance": "Volume at a recoverable intensity. Hiking counts. No vert work yet",
        "Base 2 — aerobic volume + vert": "Weekly vert session begins. Mountain weekends start. First ultra",
        "Specific — mountain, dark, fuelled": "Back-to-backs, descending load, night running, race fuelling rate",
        "Taper": "Arrive not-tired. Volume falls, a little intensity stays",
        "Race week": "Do nothing useful",
    }
    for name, lo, hi in PHASES:
        L.append(f"| {name} | {lo}–{hi} | {week_start(lo):%-d %b} – {week_start(hi)+timedelta(days=6):%-d %b} | {purposes[name]} |")
    L.append("")

    L.append("## Key dates\n")
    L.append("| Week | Date | What |")
    L.append("| ---- | ---- | ---- |")
    for w in sorted(set(list(MOUNTAIN_WEEKS) + list(TUNE_UPS))):
        sat = week_start(w) + timedelta(days=5)
        what = TUNE_UPS[w]["name"] if w in TUNE_UPS else MOUNTAIN_WEEKS[w].split(" — ")[0].split(".")[0]
        L.append(f"| {w} | {sat:%a %-d %b %Y} | {what} |")
    L.append(f"| 29 | {RACE_DATE:%a %-d %b %Y} | **{RACE_NAME}** |")
    L.append("")

    L.append("## Weekly load\n")
    L.append("| Wk | Starting | Phase | Hours | Vert (ft) | Notes |")
    L.append("| -- | -------- | ----- | ----- | --------- | ----- |")
    for w, (sessions, ph) in weeks.items():
        tag = []
        if w in DOWN_WEEKS: tag.append("**down week**")
        if w in MOUNTAIN_WEEKS: tag.append("mountains")
        if w in TUNE_UPS: tag.append(f"**{TUNE_UPS[w]['name']}**")
        if w == 29: tag.append("**RACE**")
        short = ph.split(" — ")[0]
        L.append(f"| {w} | {week_start(w):%-d %b} | {short} | {WEEK_HOURS[w]:.1f} | "
                 f"{WEEK_VERT_FT[w]:,} | {', '.join(tag)} |")
    L.append("")

    L.append("## The weeks\n")
    for w, (sessions, ph) in weeks.items():
        ws = week_start(w)
        hdr = f"### Week {w} — {ws:%-d %b} to {ws+timedelta(days=6):%-d %b} · {ph}"
        flags = []
        if w in DOWN_WEEKS: flags.append("DOWN WEEK")
        if w in MOUNTAIN_WEEKS: flags.append("MOUNTAIN TRIP")
        if w in TUNE_UPS: flags.append(TUNE_UPS[w]["name"].upper())
        if w == 29: flags.append("RACE WEEK")
        if flags:
            hdr += f"  ·  **{' · '.join(flags)}**"
        L.append(hdr + "\n")
        L.append(f"Target: {WEEK_HOURS[w]:.1f} h · {WEEK_VERT_FT[w]:,} ft vert\n")
        L.append("| Day | Date | Session | Time | Vert | Notes |")
        L.append("| --- | ---- | ------- | ---- | ---- | ----- |")
        for s in sorted(sessions, key=lambda x: (x.day_offset, x.kind != "run")):
            d = ws + timedelta(days=s.day_offset)
            dur = "—" if not s.minutes else (f"{s.minutes//60}h{s.minutes%60:02d}" if s.minutes >= 60 else f"{s.minutes}m")
            vf = f"{s.vert_ft:,}" if s.vert_ft else "—"
            L.append(f"| {s.dayname} | {d:%-d %b} | {s.title} | {dur} | {vf} | {s.notes} |")
        L.append("")
    return "\n".join(L)


# ── Output: ICS ──────────────────────────────────────────────────────────────
VTIMEZONE = """BEGIN:VTIMEZONE
TZID:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE"""


def esc(t):
    return (t.replace("\\", "\\\\").replace(";", r"\;")
             .replace(",", r"\,").replace("\n", r"\n"))


def fold(line):
    """RFC 5545 line folding at 75 octets. Unfolded long DESCRIPTIONs are the
    single commonest reason an .ics imports with mangled text."""
    out, b = [], line.encode("utf-8")
    if len(b) <= 75:
        return line
    out.append(b[:75].decode("utf-8", "ignore"))
    rest = b[len(out[0].encode("utf-8")):]
    while rest:
        chunk = rest[:74]
        s = chunk.decode("utf-8", "ignore")
        out.append(" " + s)
        rest = rest[len(s.encode("utf-8")):]
    return "\r\n".join(out)


def render_ics(weeks):
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    L = ["BEGIN:VCALENDAR", "VERSION:2.0",
         "PRODID:-//tce-founder//Ultra Hellbender Plan//EN",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         f"X-WR-CALNAME:{RACE_NAME} training",
         f"X-WR-TIMEZONE:{TIMEZONE}"]
    L += VTIMEZONE.split("\n")

    n = 0
    for w, (sessions, ph) in weeks.items():
        ws = week_start(w)
        for i, s in enumerate(sessions):
            if s.kind == "rest" and s.minutes == 0 and s.title == "Rest":
                continue  # a rest day does not need a calendar entry
            d = ws + timedelta(days=s.day_offset)
            t = DEFAULT_TIMES.get(s.kind, "06:00")
            hh, mm = int(t[:2]), int(t[3:])
            start = datetime(d.year, d.month, d.day, hh, mm)
            dur = s.minutes or 30
            end = start + timedelta(minutes=dur)
            n += 1
            vtxt = f" · {s.vert_ft:,} ft vert" if s.vert_ft else ""
            summary = f"W{w} · {s.title}"
            if s.minutes:
                summary += f" ({s.minutes//60}h{s.minutes%60:02d})" if s.minutes >= 60 else f" ({s.minutes}m)"
            desc = f"Week {w} · {ph}{vtxt}\\n\\n{s.notes}" if s.notes else f"Week {w} · {ph}{vtxt}"
            L.append("BEGIN:VEVENT")
            L.append(f"UID:hb100-w{w:02d}-{i}-{d.isoformat()}@tce-founder.ultra")
            L.append(f"DTSTAMP:{stamp}")
            L.append(f"DTSTART;TZID={TIMEZONE}:{start:%Y%m%dT%H%M%S}")
            L.append(f"DTEND;TZID={TIMEZONE}:{end:%Y%m%dT%H%M%S}")
            L.append(fold(f"SUMMARY:{esc(summary)}"))
            L.append(fold(f"DESCRIPTION:{esc(desc)}"))
            L.append(f"CATEGORIES:{s.kind.upper()}")
            if s.kind == "race":
                L.append("LOCATION:Camp Grier\\, Old Fort\\, NC")
            L.append("END:VEVENT")

    # Daily mobility as one recurring event rather than 200 copies.
    L += ["BEGIN:VEVENT",
          f"UID:hb100-mobility@tce-founder.ultra",
          f"DTSTAMP:{stamp}",
          f"DTSTART;TZID={TIMEZONE}:{WEEK1_MONDAY:%Y%m%d}T210000",
          f"DTEND;TZID={TIMEZONE}:{WEEK1_MONDAY:%Y%m%d}T211500",
          f"RRULE:FREQ=DAILY;UNTIL={RACE_DATE:%Y%m%d}T000000Z",
          "SUMMARY:Mobility — 15 min",
          fold("DESCRIPTION:" + esc(
              "Ankle dorsiflexion against a wall 10/side. Calf and soleus stretch 45 s each. "
              "Couch stretch 60 s/side. 90/90 hip rotations 10/side. Thoracic rotations 10/side.\n\n"
              "Honest framing: the evidence that stretching prevents running injury is weak. This is here "
              "for ankle and hip range you actually need on technical descents, and because a short daily "
              "anchor keeps the rest of the routine attached to something.")),
          "CATEGORIES:MOBILITY", "END:VEVENT"]
    n += 1

    L.append("END:VCALENDAR")
    return "\r\n".join(L) + "\r\n", n


# ── Output: Garmin structured workouts ───────────────────────────────────────
# ID MAPPINGS ARE FROM UNOFFICIAL SOURCES. Garmin publishes no consumer API docs;
# these come from community reverse-engineering of /workout-service/workout. They
# are the most likely failure point in this whole toolchain, which is why
# push_garmin.py defaults to --dry-run and supports --limit.
SPORT_RUNNING = {"sportTypeId": 1, "sportTypeKey": "running"}
STEP_WARMUP = {"stepTypeId": 1, "stepTypeKey": "warmup"}
STEP_INTERVAL = {"stepTypeId": 3, "stepTypeKey": "interval"}
STEP_COOLDOWN = {"stepTypeId": 2, "stepTypeKey": "cooldown"}
END_TIME = {"conditionTypeId": 2, "conditionTypeKey": "time"}
NO_TARGET = {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target"}


def step(order, stype, seconds, desc):
    return {
        "type": "ExecutableStepDTO",
        "stepOrder": order,
        "stepType": stype,
        "endCondition": END_TIME,
        "endConditionValue": int(seconds),
        "targetType": NO_TARGET,
        "description": desc[:512],
    }


def garmin_workout(s, w, when):
    """One structured workout. Deliberately time-based with no pace/HR target.

    We do not know this athlete's zones, and inventing them would produce targets
    that look authoritative and are guesses. Effort guidance goes in the step
    description instead, where it reads as guidance.
    """
    secs = s.minutes * 60
    if s.kind in ("long",) or s.minutes >= 90:
        steps = [step(1, STEP_WARMUP, 900, "Easy. Walk breaks from the start if hilly."),
                 step(2, STEP_INTERVAL, max(300, secs - 1500), s.notes or "Conversational effort throughout."),
                 step(3, STEP_COOLDOWN, 600, "Easy walk/jog. Eat within 30 minutes.")]
    elif s.kind == "vert":
        steps = [step(1, STEP_WARMUP, 600, "Flat or low incline."),
                 step(2, STEP_INTERVAL, max(300, secs - 900), VERT_NOTE),
                 step(3, STEP_COOLDOWN, 300, "Flat, easy.")]
    else:
        steps = [step(1, STEP_INTERVAL, secs, s.notes or "Easy, conversational.")]
    return {
        "_scheduleDate": when.isoformat(),
        "_week": w,
        "sportType": SPORT_RUNNING,
        "workoutName": f"W{w} {s.title}"[:80],
        "description": (f"{RACE_NAME} plan · week {w}"
                        + (f" · target {s.vert_ft:,} ft vert" if s.vert_ft else ""))[:1024],
        "workoutSegments": [{
            "segmentOrder": 1,
            "sportType": SPORT_RUNNING,
            "workoutSteps": steps,
        }],
    }


def render_garmin(weeks):
    out = []
    for w, (sessions, ph) in weeks.items():
        ws = week_start(w)
        for s in sessions:
            if not s.garmin or not s.minutes:
                continue
            out.append(garmin_workout(s, w, ws + timedelta(days=s.day_offset)))
    return out


# ── Validation ───────────────────────────────────────────────────────────────
def validate(weeks):
    """Checks the plan against itself.

    The ramp check compares each build week to the PREVIOUS BUILD WEEK, not to the
    calendar week before it. Comparing against a down week reports a 50%+ jump every
    time volume resumes, which is the shape a down week is supposed to have — the
    first draft of this function did exactly that and produced six false failures.
    What it is actually policing is the trend line through the down weeks.
    """
    problems = []
    prev_build = None
    for w in sorted(weeks):
        h = WEEK_HOURS[w]
        is_build = w not in DOWN_WEEKS and w != 29 and w not in TUNE_UPS
        if is_build:
            if prev_build is not None:
                jump = (h - prev_build) / prev_build
                if jump > 0.22:
                    problems.append(f"week {w}: {jump:.0%} jump on the last build week — above the 22% ceiling")
            prev_build = h
        sessions, ph = weeks[w]
        got = sum(s.minutes for s in sessions if s.kind != "race") / 60.0
        if w not in TUNE_UPS and w != 29 and abs(got - h) > 0.75:
            problems.append(f"week {w}: sessions total {got:.1f} h against a {h:.1f} h target")
        if not any(s.kind == "rest" or s.minutes == 0 for s in sessions) and w != 29:
            problems.append(f"week {w}: no rest day")
    for w in range(1, 30):
        if w not in WEEK_HOURS or w not in WEEK_VERT_FT:
            problems.append(f"week {w}: missing hours or vert target")
    return problems


def main():
    weeks = {}
    for w in range(1, 30):
        weeks[w] = build_week(w)

    problems = validate(weeks)
    total_h = sum(WEEK_HOURS.values())
    total_v = sum(WEEK_VERT_FT.values()) - RACE_VERT_FT

    print(f"{len(weeks)} weeks · {total_h:.0f} training hours · {total_v:,} ft vert before race day")
    print(f"  peak week    {max(WEEK_HOURS, key=WEEK_HOURS.get)} at {max(WEEK_HOURS.values()):.1f} h")
    print(f"  down weeks   {sorted(DOWN_WEEKS)}")
    print(f"  mountain     weeks {sorted(MOUNTAIN_WEEKS)}")
    print(f"  tune-ups     weeks {sorted(TUNE_UPS)}")
    sess = sum(len(s) for s, _ in weeks.values())
    print(f"  sessions     {sess}")

    if problems:
        print("  FAILURES:")
        for p in problems:
            print(f"    - {p}")
        return 1
    print("  ramp within ceiling, every week has a rest day, totals reconcile")

    if "--check" in sys.argv:
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    md = render_markdown(weeks)
    open(os.path.join(OUT_DIR, "plan.md"), "w").write(md)
    ics, nev = render_ics(weeks)
    open(os.path.join(OUT_DIR, "hellbender-2027.ics"), "w", newline="").write(ics)
    gw = render_garmin(weeks)
    json.dump(gw, open(os.path.join(OUT_DIR, "garmin_workouts.json"), "w"), indent=2)

    rel = os.path.relpath(OUT_DIR, ROOT)
    print(f"wrote {rel}/plan.md ({len(md.splitlines())} lines)")
    print(f"wrote {rel}/hellbender-2027.ics ({nev} events)")
    print(f"wrote {rel}/garmin_workouts.json ({len(gw)} workouts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
