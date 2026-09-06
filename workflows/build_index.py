#!/usr/bin/env python3
"""
Deterministic rebuild of advisory/kb/INDEX.json.

WHY THIS IS CODE AND NOT AN AGENT. Building the index is mechanical: parse
frontmatter, group by field, count links. An agent doing it is expensive and
unreliable in a way that is invisible downstream. The upstream system this was
ported from (tce-founder/Anton) recorded three such bugs, and the first is the
one worth restating because it is a general law rather than a slip:

  `by_lens` omitted keys entirely for tags with no pages, so a lens querying
  `by_lens['heat-adaptation']` got a missing key rather than an empty list. A
  caller testing `len(v) == 0` never sees it. AN ABSENT KEY AND AN EMPTY LIST
  ARE DIFFERENT FAILURES AND ONLY ONE OF THEM IS VISIBLE.

Every key in the taxonomy is emitted whether or not it has members, and the
script asserts its own totals reconcile before writing.

Judgment still belongs to the agent: `corpus_gaps` is preserved from the
existing index rather than computed here, because "what does this corpus fail
to cover" is not derivable from frontmatter.

WHAT --check ASSERTS, beyond the index reconciling with itself:

  ROUTING   every lens in workflows/lenses.json has a tag mapping in
            golden_queries.json, and every taxonomy tag is either routed or
            explicitly declared unrouted. Lens names and tag names are two
            different vocabularies and nothing else connects them.
  STARVED   a lens whose every mapped tag is empty has no reachable page at
            all. Unlike an empty tag that never surfaces at runtime — the lens
            improvises and its note reads like a grounded one.
  RECIPROCITY  `related` is declared bidirectional in SCHEMA.md. A one-way
            entry is invisible from the orphaned side, so it is checked rather
            than trusted. This check is local to this repository and has no
            upstream equivalent.
  GOLDEN    each recorded question resolves to at least its min_pages.
            Measures REACHABILITY, not answer quality.
  FLOORS    acceptance_floors.json is a ratchet. Worse than a floor fails;
            better than a floor is reported for a human to commit, because
            lowering a floor is a decision with a reason and a date.

Usage:  python3 workflows/build_index.py [--check] [--today YYYY-MM-DD]
        --check exits non-zero on any inconsistency and writes nothing.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.join(ROOT, "advisory", "kb")
INDEX = os.path.join(KB, "INDEX.json")
SCHEMA = os.path.join(KB, "SCHEMA.md")
LENSES = os.path.join(ROOT, "workflows", "lenses.json")
GOLDEN = os.path.join(ROOT, "workflows", "golden_queries.json")
FLOORS = os.path.join(ROOT, "workflows", "acceptance_floors.json")

# purpose.md is the corpus CHARTER, not a corpus page. It carries no frontmatter
# by design — it is prose an ingest node reads to decide whether a page should
# exist at all, which is a different question from what INDEX.json answers.
SKIP_NAMES = {"SCHEMA.md", "INDEX.md", "log.md", "purpose.md"}

CITATION_STATUSES = ["recommended", "queued", "acquired", "read", "summarized", "rejected"]
WIKI_TYPES = ["concept", "source", "entity", "comparison", "query"]
IP_CLASSES = ["public", "licensed"]
AUTHORITIES = ["measured", "established", "experienced", "asserted"]
DISPOSITIONS = ["sharpened", "counterpoint", "gap"]
# disposition is required on pages built from OUTSIDE material. "Outside" is not
# derivable from frontmatter, so the mechanical proxy is the page type: source
# and concept pages absorb something, entity and query pages do not. The proxy
# over-counts slightly and that is the safe direction — it surfaces as a ratchet
# number, never as a hard failure.
DISPOSITION_REQUIRED_TYPES = {"source", "concept"}


def taxonomy():
    """Tag vocabulary, read from SCHEMA.md so the two cannot drift apart."""
    text = open(SCHEMA).read()
    m = re.search(r"## Tag taxonomy\n(.*?)\n## ", text, re.S)
    if not m:
        return []
    tags = re.findall(r"^- ([a-z][a-z0-9-]*)$", m.group(1), re.M)
    return sorted(set(tags))


def lens_names():
    """Lens vocabulary, read from workflows/lenses.json — its owner.

    Same pattern as taxonomy() reading SCHEMA.md: a vocabulary is read from the
    file that defines it, never copied. A lens added there without a
    golden_queries.json mapping is then an error rather than a silent
    fallthrough to an empty bucket.
    """
    doc = load_json(LENSES)
    if not doc:
        return []
    return sorted(k for k in doc.get("lenses", {}) if not k.startswith("_"))


def load_json(path):
    return json.load(open(path)) if os.path.exists(path) else None


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not m:
        return None, text
    fm, body = m.group(1), text[m.end():]
    out = {}
    key = None
    for line in fm.split("\n"):
        if not line.strip():
            continue
        li = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if li:
            key = li.group(1)
            val = li.group(2).strip()
            if val in ("", ">-", "|", ">"):
                out[key] = [] if val == "" else ""
            else:
                out[key] = val.strip("'\"")
        elif line.startswith("  - ") and key:
            if not isinstance(out.get(key), list):
                out[key] = []
            out[key].append(line[4:].strip().strip("'\""))
        elif line.startswith("  ") and isinstance(out.get(key), str):
            # continuation of a folded block scalar (`>-`)
            out[key] = (out[key] + " " + line.strip()).strip()
    return out, body


def collect():
    pages = {}
    for dirpath, dirnames, filenames in os.walk(KB):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn in SKIP_NAMES:
                continue
            path = os.path.join(dirpath, fn)
            fm, body = parse_frontmatter(open(path).read())
            if fm is None:
                print(f"  WARN no frontmatter: {os.path.relpath(path, ROOT)}")
                continue
            slug = fn[:-3]
            pages[slug] = {
                "slug": slug,
                "path": path,
                "rel": os.path.relpath(path, ROOT),
                "fm": fm,
                "outbound": sorted(set(x.strip() for x in re.findall(r"\[\[([^\]|]+)", body) if x.strip())),
            }
    return pages


def build(pages, previous):
    tags = taxonomy()
    # Every taxonomy key is emitted, empty or not.
    by_lens = {t: [] for t in tags}
    by_status = {s: [] for s in CITATION_STATUSES}
    by_type = {t: [] for t in WIKI_TYPES}
    by_ip = {c: [] for c in IP_CLASSES}
    by_layer = {"1": [], "2": [], "3": []}
    by_authority = {a: [] for a in AUTHORITIES}
    by_disposition = {d: [] for d in DISPOSITIONS}
    unclassified_ip, untyped, entries = [], [], []
    # Remainder lists, NOT reconcile groups. Neither sums to entry_count, so both
    # are ratcheted in acceptance_floors.json instead of reconciled here.
    missing_authority, bad_authority = [], []
    missing_disposition, bad_disposition = [], []

    # Inbound counts BOTH body [[wikilinks]] AND frontmatter `related`. Counting
    # body links alone reports false orphans: pages correctly cross-referenced in
    # `related` on both sides but not linked in prose. The question an orphan
    # check actually asks is "can anyone find this page", and a reciprocal
    # `related` entry answers yes.
    inbound = {s: set() for s in pages}
    for slug, p in pages.items():
        refs = set(p["outbound"]) | set(p["fm"].get("related", []) or [])
        for target in refs:
            if target in inbound and target != slug:
                inbound[target].add(slug)

    # SCHEMA.md declares `related` bidirectional. Trusting that is how a one-way
    # entry survives: it is invisible from the side that was never edited.
    nonreciprocal = []
    dangling_related = []
    for slug in sorted(pages):
        for target in pages[slug]["fm"].get("related", []) or []:
            if target not in pages:
                dangling_related.append(f"{slug} -> {target}")
            elif slug not in (pages[target]["fm"].get("related", []) or []):
                nonreciprocal.append(f"{slug} -> {target} (not returned)")

    for slug in sorted(pages):
        p = pages[slug]
        fm = p["fm"]
        wt = fm.get("type", "")
        ip = fm.get("ip_class", "")
        cs = fm.get("citation_status", "")
        tg = fm.get("tags", []) or []

        for t in tg:
            if t in by_lens:
                by_lens[t].append(slug)
        if wt in by_type:
            by_type[wt].append(slug)
        else:
            untyped.append(slug)
        if cs in by_status:
            by_status[cs].append(slug)
        if ip in by_ip:
            by_ip[ip].append(slug)
        else:
            unclassified_ip.append(slug)

        auth = fm.get("authority", "")
        if auth in by_authority:
            by_authority[auth].append(slug)
        elif auth:
            bad_authority.append(f"{slug}: {auth}")
        else:
            missing_authority.append(slug)

        # Each disposition entry reads "<value>: <target> — what it did". The
        # value is the prefix; a naked value with no target says nothing and is
        # counted as malformed rather than silently accepted.
        disp = fm.get("disposition", []) or []
        if isinstance(disp, str):
            disp = [disp]
        seen_disp = False
        for d in disp:
            value = d.split(":", 1)[0].strip()
            if value not in by_disposition:
                bad_disposition.append(f"{slug}: {d[:60]}")
                continue
            if ":" not in d or not d.split(":", 1)[1].strip():
                bad_disposition.append(f"{slug}: '{value}' names no target")
                continue
            by_disposition[value].append(slug)
            seen_disp = True
        if not seen_disp and wt in DISPOSITION_REQUIRED_TYPES:
            missing_disposition.append(slug)

        layer = "1" if "/frameworks/" in p["path"] else "2" if "/benchmarks/" in p["path"] else "3"
        by_layer[layer].append(slug)

        entries.append({
            "slug": slug, "path": p["rel"], "wiki_type": wt, "layer": int(layer),
            "title": fm.get("title", ""), "tags": tg,
            "citation_status": cs, "quality_signal": fm.get("quality_signal", ""),
            "reference_role": fm.get("reference_role", ""),
            "population": fm.get("population", ""), "unit": fm.get("unit", ""),
            "authority": fm.get("authority", ""),
            "disposition": fm.get("disposition", []) or [],
            "ip_class": ip, "related": fm.get("related", []) or [],
            "summary": (fm.get("summary", "") or fm.get("purpose", ""))[:400],
            "sources": fm.get("sources", []) or [],
            "outbound": p["outbound"],
            "inbound_count": len(inbound[slug]),
        })

    orphans = sorted(s for s in pages
                     if len(pages[s]["outbound"]) < 2 or len(inbound[s]) == 0)

    today = previous.get("updated", "")
    if "--today" in sys.argv:
        today = sys.argv[sys.argv.index("--today") + 1]

    idx = {
        "updated": today,
        "generated_by": "workflows/build_index.py — deterministic; do not hand-edit",
        "entry_count": len(entries),
        "entries": entries,
        "by_layer": by_layer,
        "by_lens": by_lens,
        "by_status": by_status,
        "by_type": by_type,
        "by_ip_class": by_ip,
        "by_authority": by_authority,
        "by_disposition": by_disposition,
        "orphans": orphans,
        "nonreciprocal_related": nonreciprocal,
        "dangling_related": dangling_related,
        "unclassified_ip": unclassified_ip,
        "missing_authority": missing_authority,
        "bad_authority": bad_authority,
        "missing_disposition": missing_disposition,
        "bad_disposition": bad_disposition,
        "untyped": untyped,
        "corpus_gaps": previous.get("corpus_gaps", []),
    }
    return idx


def check_routing(idx):
    """The lens vocabulary and the tag vocabulary are DIFFERENT vocabularies.

    lenses.json names lenses; INDEX.json groups by tag. golden_queries.json
    declares the map between them, and it is checked in BOTH directions — a
    stale entry for a deleted lens is as wrong as a missing one.
    """
    golden = load_json(GOLDEN)
    if golden is None:
        return ["golden_queries.json missing — routing is unchecked"]

    problems = []
    mapping = {k: v for k, v in golden.get("lens_tag_map", {}).items() if not k.startswith("_")}
    unrouted = {k for k in golden.get("unrouted_tags", {}) if not k.startswith("_")}
    declared_lenses, graph_lenses = set(mapping), set(lens_names())

    if graph_lenses:
        for lens in sorted(graph_lenses - declared_lenses):
            problems.append(f"lens '{lens}' is declared in lenses.json but has no tag mapping")
        for lens in sorted(declared_lenses - graph_lenses):
            problems.append(f"lens '{lens}' is mapped but no longer exists in lenses.json")

    tags = set(taxonomy())
    mapped = {tag for v in mapping.values() for tag in v}
    for tag in sorted(mapped - tags):
        problems.append(f"lens_tag_map names '{tag}', which is not in the SCHEMA.md taxonomy")
    for tag in sorted(unrouted - tags):
        problems.append(f"unrouted_tags names '{tag}', which is not in the SCHEMA.md taxonomy")
    for tag in sorted(tags - mapped - unrouted):
        problems.append(f"tag '{tag}' is in the taxonomy but neither routed nor declared unrouted")
    for tag in sorted(mapped & unrouted):
        problems.append(f"tag '{tag}' is both routed and declared unrouted")
    return problems


def starved_lenses(idx):
    """Lenses whose every tag resolves to zero pages.

    NOT the same as an empty tag. A lens with four tags, three of them empty, is
    still grounded. A lens with no reachable page anywhere does not fail loudly —
    it improvises, and its note reads exactly like a grounded one.
    """
    golden = load_json(GOLDEN) or {}
    mapping = {k: v for k, v in golden.get("lens_tag_map", {}).items() if not k.startswith("_")}
    by_lens = idx.get("by_lens", {})
    out = {}
    for lens, tags in mapping.items():
        reachable = {s for tag in tags for s in by_lens.get(tag, [])}
        if not reachable:
            out[lens] = tags
    return out


def check_golden(idx, excused=frozenset()):
    """Can each recorded question actually be grounded from the corpus?

    Deterministic: resolves each question's lenses to tags to pages and counts
    the distinct pages. It measures REACHABILITY, never answer quality — depth
    is not tested here and the golden file says so.

    A question whose shortfall is fully explained by lenses already recorded as
    starved in acceptance_floors.json is REPORTED, not failed. Over-flagging a
    known gap on every run is how a check earns being ignored.
    """
    golden = load_json(GOLDEN)
    if golden is None:
        return [], []
    mapping = {k: v for k, v in golden.get("lens_tag_map", {}).items() if not k.startswith("_")}
    by_lens = idx.get("by_lens", {})
    problems, results = [], []
    for q in golden.get("questions", []):
        pages = set()
        for lens in q.get("lenses", []):
            if lens not in mapping:
                problems.append(f"golden question routes to unmapped lens '{lens}'")
                continue
            for tag in mapping[lens]:
                pages.update(by_lens.get(tag, []))
        need = q.get("min_pages", 1)
        lenses = set(q.get("lenses", []))
        is_excused = bool(lenses) and lenses <= excused
        ok = len(pages) >= need
        results.append({"q": q["q"], "pages": len(pages), "min": need,
                        "ok": ok, "excused": is_excused and not ok})
        if not ok and not is_excused:
            problems.append(f"golden: {len(pages)}/{need} pages for \"{q['q'][:60]}\"")
    return problems, results


def check_floors(idx):
    """Acceptance floors — the ratchet.

    Floors are AUTHORED and committed; INDEX.json is generated, so a floor kept
    there would reset itself on every build. A run that is worse than a floor
    fails. A run that is BETTER reports the improvement and stops there: lowering
    a floor is a decision with a reason and a date, so a human commits it. Auto-
    tightening would let one lucky run lock in a number nobody chose.
    """
    floors_doc = load_json(FLOORS)
    if floors_doc is None:
        return ["acceptance_floors.json missing — nothing is ratcheted"], []
    f = floors_doc.get("floors", {})
    problems, slack = [], []

    def cmp_max(key, actual, label):
        if key not in f:
            return
        limit = f[key]["value"]
        if actual > limit:
            problems.append(f"{label}: {actual} exceeds floor {limit}")
        elif actual < limit:
            slack.append(f"{label}: {actual} is better than floor {limit} — floor can drop")

    def cmp_min(key, actual, label):
        if key not in f:
            return
        limit = f[key]["value"]
        if actual < limit:
            problems.append(f"{label}: {actual} is below floor {limit}")
        elif actual > limit:
            slack.append(f"{label}: {actual} is above floor {limit} — floor can rise")

    cmp_min("pages_min", idx["entry_count"], "pages")
    cmp_max("orphans_max", len(idx["orphans"]), "orphans")
    cmp_max("nonreciprocal_related_max", len(idx["nonreciprocal_related"]), "one-way related")
    cmp_max("dangling_related_max", len(idx["dangling_related"]), "related to a page that does not exist")
    cmp_max("unclassified_ip_max", len(idx["unclassified_ip"]), "unclassified ip")
    cmp_max("untyped_max", len(idx["untyped"]), "untyped")
    cmp_max("missing_authority_max", len(idx["missing_authority"]), "pages missing authority")
    cmp_max("missing_disposition_max", len(idx["missing_disposition"]), "pages missing disposition")

    # Malformed values are never ratcheted — a bad enum is a defect at any count.
    for key, label in (("bad_authority", "malformed authority"), ("bad_disposition", "malformed disposition")):
        for row in idx.get(key, []):
            problems.append(f"{label}: {row}")

    allowed_empty = {k for k in floors_doc.get("allowed_empty_lenses", {}) if not k.startswith("_")}
    empty = {k for k, v in idx["by_lens"].items() if not v}
    for tag in sorted(empty - allowed_empty):
        problems.append(f"tag '{tag}' has zero pages and is not on the allowed-empty list")
    for tag in sorted(allowed_empty - empty):
        slack.append(f"tag '{tag}' is no longer empty — remove it from allowed_empty_lenses")

    allowed_starved = {k for k in floors_doc.get("allowed_starved_lenses", {}) if not k.startswith("_")}
    starved = set(starved_lenses(idx))
    for lens in sorted(starved - allowed_starved):
        problems.append(f"LENS '{lens}' has zero reachable pages and is not a recorded gap — it will improvise")
    for lens in sorted(allowed_starved - starved):
        slack.append(f"lens '{lens}' is no longer starved — remove it from allowed_starved_lenses")

    return problems, slack


def check(idx):
    """Every grouping must account for every entry."""
    n = idx["entry_count"]
    problems = []
    for name in ("by_type", "by_ip_class", "by_layer"):
        total = sum(len(v) for v in idx[name].values())
        extra = len(idx["unclassified_ip"]) if name == "by_ip_class" else \
                len(idx["untyped"]) if name == "by_type" else 0
        if total + extra != n:
            problems.append(f"{name} covers {total}+{extra} of {n} entries")
    return problems


def main():
    check_only = "--check" in sys.argv
    previous = json.load(open(INDEX)) if os.path.exists(INDEX) else {}
    pages = collect()
    idx = build(pages, previous)
    problems = check(idx)

    print(f"{idx['entry_count']} pages")
    print(f"  by_type      {[(k, len(v)) for k, v in idx['by_type'].items()]}")
    print(f"  by_ip_class  {[(k, len(v)) for k, v in idx['by_ip_class'].items()]}")
    empty = [k for k, v in idx["by_lens"].items() if not v]
    print(f"  by_lens      {len(idx['by_lens'])} keys, {len(empty)} EMPTY: {', '.join(empty) or 'none'}")
    print(f"  orphans      {idx['orphans'] or 'none'}")
    print(f"  related      {len(idx['nonreciprocal_related'])} one-way, "
          f"{len(idx['dangling_related'])} dangling")
    print(f"  unclassified {idx['unclassified_ip'] or 'none'}")
    print(f"  by_authority {[(k, len(v)) for k, v in idx['by_authority'].items()]}"
          f"  missing {len(idx['missing_authority'])}")
    print(f"  by_disposit. {[(k, len(v)) for k, v in idx['by_disposition'].items()]}"
          f"  missing {len(idx['missing_disposition'])}")

    starved = starved_lenses(idx)
    print(f"  starved      {', '.join(sorted(starved)) or 'none'}"
          f"{'  (lenses with ZERO reachable pages)' if starved else ''}")

    routing = check_routing(idx)
    floors_doc = load_json(FLOORS) or {}
    excused = frozenset(k for k in floors_doc.get("allowed_starved_lenses", {}) if not k.startswith("_"))
    golden_problems, golden_results = check_golden(idx, excused)
    passed = sum(1 for r in golden_results if r["ok"])
    n_excused = sum(1 for r in golden_results if r["excused"])
    print(f"  golden       {passed}/{len(golden_results)} questions grounded"
          f"{f', {n_excused} short on a RECORDED GAP' if n_excused else ''}")
    for r in golden_results:
        if not r["ok"]:
            print(f"    {'~' if r['excused'] else '-'} {r['pages']}/{r['min']}  {r['q'][:66]}")

    floor_problems, slack = check_floors(idx)
    problems = problems + routing + golden_problems + floor_problems

    if slack:
        print("  FLOORS CAN TIGHTEN (authored file — a human commits the new value):")
        for s in slack:
            print(f"    + {s}")
    if problems:
        print("  FAILURES:")
        for pr in problems:
            print(f"    - {pr}")
        return 1
    print("  totals reconcile, routing declared, related reciprocal, floors held")
    if not check_only:
        json.dump(idx, open(INDEX, "w"), indent=2)
        print(f"wrote {os.path.relpath(INDEX, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
