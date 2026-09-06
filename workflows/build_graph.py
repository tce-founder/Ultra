#!/usr/bin/env python3
"""
Edge extractor and impact query over the corpus, the registers and the analysis.

THE QUESTION THIS EXISTS TO ANSWER: *if this claim turns out to be wrong, what
depends on it?* Without it that is answered by grepping and hoping.

In this domain the question is not academic. Ultrarunning circulates a small
number of load-bearing numbers — 90 g/h, "salt prevents cramp", "80/20" — that
are quoted far more often than they are sourced, and each of them, if it moves,
moves a training plan and a race-day plan at the same time. The declared claims
below are exactly those: assertions that live in prose across many documents
rather than in one file, so they have no natural node until one is made for them.

TWO EDGE CLASSES, AND THEY ARE NOT EQUALLY TRUSTWORTHY. Keeping them apart is
the whole point; blending them produces a confident graph built partly on string
matching.

  STRUCTURAL (exact) — an ID or a wikilink literally appears in a row or a page:
    cites        register row -> kb page
    references   register row -> another register row
    relates_to   kb page <-> kb page

  CLAIM (lexical, approximate) — a declared claim's patterns appear in a doc:
    asserts      document -> claim

Structural edges are facts. Claim edges are candidates: a lexical hit means the
document *mentions* the claim, not necessarily that it *depends* on it. The
impact report labels which is which and never merges the two counts.

Usage:
  python3 workflows/build_graph.py                 # build advisory/graph/edges.json
  python3 workflows/build_graph.py --impact CLAIM  # what depends on this
"""

import json
import os
import re
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADVISORY = os.path.join(ROOT, "advisory")
KB = os.path.join(ADVISORY, "kb")
OUT_DIR = os.path.join(ADVISORY, "graph")
OUT = os.path.join(OUT_DIR, "edges.json")

WIKI_RE = re.compile(r"\[\[([^\]|#]+)")
ROW_RE = re.compile(r"^\|\s*((?:OBJ|ACT|DEC)-\d+)\s*\|")


def wikilinks(text):
    """Wikilink targets, stripped, with the empty ones dropped.

    `WIKI_RE` matches `[[ ]]`, which pages about the schema write as prose
    notation rather than as a link. Left in, that produces a real node with a
    blank label and no path, sitting in the graph as a permanent artefact of one
    sentence in one page.
    """
    for raw in WIKI_RE.findall(text):
        name = raw.strip()
        if name:
            yield name


# ── Declared claims ──────────────────────────────────────────────────────────
# Patterns are deliberately narrow. `carbohydrate` alone appears on most pages in
# this corpus; what is tracked is the QUANTIFIED claim, not the concept.
CLAIMS = {
    "claim:carb-ceiling": {
        "label": "The absorbable carbohydrate ceiling is ~90 g/h, and ~120 g/h with gut training",
        "why_it_matters": "It sets the race fuelling plan, the gut-training block that precedes it, "
                          "and how much of a bad patch is read as a fuelling failure. The 120 g/h "
                          "evidence is one small trial in elite men on a mountain marathon; the "
                          "number travels far better than its population does.",
        "patterns": [r"120\s*g\s*/?\s*h", r"90\s*g\s*/?\s*h", r"60\s*[-–]\s*90\s*g",
                     r"grams? (?:of )?carb(?:ohydrate)?s? per hour", r"multiple transportable"],
    },
    "claim:sodium-prevents-cramp": {
        "label": "Sodium supplementation prevents cramping, dehydration and hyponatremia",
        "why_it_matters": "Widely believed and directly contradicted by the trial recorded in "
                          "[[sodium-does-not-prevent-cramping]]. It is load-bearing in the opposite "
                          "direction from most claims here: acting on it causes over-drinking, which "
                          "is the actual mechanism of exercise-associated hyponatremia.",
        "patterns": [r"salt (?:tab|pill|cap)", r"sodium (?:prevent|stop|fix)",
                     r"electrolyte(?:s)? (?:prevent|stop|fix)", r"prevent(?:s|ing)? cramp"],
    },
    "claim:gi-leading-dnf": {
        "label": "GI distress is the leading cause of ultramarathon DNF",
        "why_it_matters": "If true it ranks gut training above most of the training plan. The "
                          "underlying figures are from two named US 100-mile races and are about "
                          "the stated PRIMARY reason for withdrawal, which is not the same as cause.",
        "patterns": [r"leading cause of (?:a )?DNF", r"most common reason for (?:withdrawal|dropping)",
                     r"23\s*(?:%|percent)", r"35\.6\s*(?:%|percent)", r"nausea and vomiting"],
    },
    "claim:polarized-superiority": {
        "label": "A polarised ~80/20 intensity distribution beats other distributions",
        "why_it_matters": "It decides how every week is built. The systematic-review evidence "
                          "supports low-intensity dominance far more strongly than it supports "
                          "POLARISED specifically over pyramidal or threshold models.",
        "patterns": [r"80\s*/\s*20", r"polari[sz]ed", r"intensity distribution",
                     r"75\s*[-–]\s*80\s*%\s*(?:low|LIT)"],
    },
    "claim:vert-machine-equivalence": {
        "label": "An indoor climbing machine substitutes for real vertical gain",
        "why_it_matters": "It is the claim a treadmill-and-stair-machine winter rests on, and it is "
                          "asymmetric: the machines reproduce the climbing demand reasonably and the "
                          "DESCENDING demand not at all, which is where the race damage comes from.",
        "patterns": [r"stair\s*master", r"stepmill", r"versaclimber", r"incline treadmill",
                     r"vertical gain", r"vert(?:ical)? (?:substitute|equivalent)"],
    },
    "claim:minimum-effective-dose": {
        "label": "Roughly 6-10 h/week, held consistently, is enough to finish a long ultra",
        "why_it_matters": "It is the premise the whole time-management lens rests on, and the one "
                          "with the weakest evidence base in this corpus — coaching assertion "
                          "repeated across sources, not a measured finding.",
        "patterns": [r"6\s*[-–]\s*10\s*hours", r"8\s*[-–]\s*10\s*hours", r"minimum effective dose",
                     r"time[- ]crunched"],
    },
}

SKIP_DIRS = {".ingest-notes", ".run-notes", ".venv", "__pycache__", "graph", "private"}


def scan_files():
    # WALK ORDER IS PINNED, because `add_node` and `add_edge` are first-write-wins.
    # os.walk yields directory entries in filesystem order, which shifts when a
    # page is rewritten. Whichever file mentions `kb:X` first decides whether that
    # node carries the page's real label and path or a bare wikilink stub, so an
    # unsorted walk lets the disk pick. Sorting does not make either winner more
    # correct — it makes the winner a property of the corpus.
    for dirpath, dirnames, filenames in os.walk(ADVISORY):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if fn.endswith((".md", ".py")):
                yield os.path.join(dirpath, fn)


# Which files under kb/ are NOT corpus pages. Imported rather than restated:
# upstream, the two lists drifted the moment one of them gained an entry, and the
# corpus charter became a node in its own dependency graph. Same class as the
# taxonomy being read from SCHEMA.md and the lens names from lenses.json — a
# vocabulary is read from its owner, never copied.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import SKIP_NAMES as NON_PAGE_FILES


def node_for_file(path):
    rel = os.path.relpath(path, ROOT)
    if os.sep + "kb" + os.sep in path and path.endswith(".md"):
        if os.path.basename(path) not in NON_PAGE_FILES:
            return f"kb:{os.path.basename(path)[:-3]}", rel
    return f"doc:{os.path.basename(path)}", rel


def build():
    nodes, edges = {}, []
    seen = set()

    def add_node(nid, kind, label, path=None):
        # A REFERENCE CREATES A STUB; THE DEFINITION UPGRADES IT. A node is
        # reached two ways — a document cites an `OBJ-4` or a bare wikilink,
        # which knows only the identifier, or the row/page itself is read, which
        # knows the real label and the path. Whichever arrives first winning
        # outright leaves pages that exist on disk carrying `path: null`, because
        # references almost always arrive first: `advisory/analysis/` sorts before
        # `advisory/kb/`. So a path-bearing add overwrites a stub.
        #
        # What survives as a stub is then SIGNAL rather than an artefact of walk
        # order: `path: null` means nothing on disk defines this target — a
        # dangling wikilink, or an ID cited but never recorded.
        prev = nodes.get(nid)
        if prev is None or (prev["path"] is None and path is not None):
            nodes[nid] = {"id": nid, "kind": kind, "label": label[:180], "path": path}

    def add_edge(src, rel, dst, evidence):
        key = (src, rel, dst)
        if key in seen or src == dst:
            return
        seen.add(key)
        edges.append({"from": src, "rel": rel, "to": dst, "evidence": evidence[:160]})

    for cid, c in CLAIMS.items():
        add_node(cid, "claim", c["label"])

    for path in scan_files():
        text = open(path, errors="ignore").read()
        fnode, rel = node_for_file(path)
        add_node(fnode, fnode.split(":")[0], os.path.basename(path), rel)

        # Register rows become their own nodes; everything they mention hangs off them.
        row_nodes = []
        for line in text.split("\n"):
            m = ROW_RE.match(line)
            if not m:
                continue
            rid = m.group(1)
            nid = f"{rid.split('-')[0].lower()}:{rid}"
            cells = [c.strip() for c in line.strip("|").split("|")]
            add_node(nid, "register", cells[1] if len(cells) > 1 else rid, rel)
            add_edge(nid, "recorded_in", fnode, os.path.basename(path))
            row_nodes.append((nid, line))
            for tok in re.findall(r"\b(?:OBJ|ACT|DEC)-\d+\b", line):
                tgt = f"{tok.split('-')[0].lower()}:{tok}"
                if tgt != nid:
                    add_node(tgt, "register", tok)
                    add_edge(nid, "references", tgt, line[:140])
            for wl in wikilinks(line):
                add_node(f"kb:{wl}", "kb", wl)
                add_edge(nid, "cites", f"kb:{wl}", line[:140])

        # KB page relationships
        if fnode.startswith("kb:"):
            for wl in sorted(set(wikilinks(text))):
                add_node(f"kb:{wl}", "kb", wl)
                add_edge(fnode, "relates_to", f"kb:{wl}", "wikilink")

        # Claim assertions — lexical, therefore candidates not facts.
        for cid, c in CLAIMS.items():
            hits = []
            for p in c["patterns"]:
                for m in re.finditer(p, text, re.I):
                    ln = text[:m.start()].count("\n") + 1
                    hits.append(f"L{ln}:{m.group(0)[:40]}")
                    break
            if hits:
                # Attribute to the most specific node available: a register row
                # if the match is inside one, otherwise the file.
                attributed = False
                for nid, line in row_nodes:
                    if any(re.search(p, line, re.I) for p in c["patterns"]):
                        add_edge(nid, "asserts", cid, line[:140])
                        attributed = True
                if not attributed:
                    add_edge(fnode, "asserts", cid, "; ".join(hits[:3]))

    return {"nodes": list(nodes.values()), "edges": edges,
            "claims": {k: {kk: vv for kk, vv in v.items() if kk != "patterns"}
                       for k, v in CLAIMS.items()}}


def impact(graph, target):
    """Everything that transitively depends on `target`, by walking edges backwards."""
    # CONTAINMENT IS NOT DEPENDENCY. `recorded_in` says a row lives in a file;
    # walking it backwards makes every row in that file a "dependent" of anything
    # the file mentions, which floods the answer with noise. Only
    # dependency-bearing relations are traversed.
    DEPENDENCY_RELS = {"asserts", "references", "cites"}
    rev = defaultdict(list)
    for e in graph["edges"]:
        if e["rel"] in DEPENDENCY_RELS:
            rev[e["to"]].append(e)
    nodes = {n["id"]: n for n in graph["nodes"]}

    matches = [n for n in nodes if target.lower() in n.lower()]
    if not matches:
        print(f"no node matching '{target}'. Known claims:")
        for c in graph["claims"]:
            print(f"  {c}")
        return 1

    for root in matches:
        print(f"\n{'=' * 74}\nIMPACT: {root}")
        meta = graph["claims"].get(root)
        if meta:
            print(f"  {meta['label']}")
            print(f"  Why it matters: {meta['why_it_matters']}")
        print("=" * 74)

        seen, direct, indirect = {root}, [], []
        q = deque([(root, 0)])
        while q:
            cur, depth = q.popleft()
            for e in rev.get(cur, []):
                if e["from"] in seen:
                    continue
                seen.add(e["from"])
                (direct if depth == 0 else indirect).append((e, depth))
                q.append((e["from"], depth + 1))

        by_rel = defaultdict(list)
        for e, d in direct:
            by_rel[e["rel"]].append(e)
        for rel, es in sorted(by_rel.items()):
            conf = "LEXICAL — mentions it, may not depend on it" if rel == "asserts" else "STRUCTURAL — exact"
            print(f"\n  DIRECT via '{rel}'  ({len(es)})   [{conf}]")
            for e in sorted(es, key=lambda x: x["from"]):
                n = nodes.get(e["from"], {})
                print(f"    {e['from']:<38} {(n.get('label') or '')[:66]}")

        if indirect:
            print(f"\n  TRANSITIVE ({len(indirect)}) — reachable, one or more hops further out")
            for e, d in sorted(indirect, key=lambda x: (x[1], x[0]["from"]))[:24]:
                print(f"    [{d+1}] {e['from']:<34} --{e['rel']}-->  {e['to']}")
            if len(indirect) > 24:
                print(f"    … {len(indirect) - 24} more")

        print(f"\n  TOTAL REACHED: {len(seen) - 1} nodes")
    return 0


def main():
    if "--impact" in sys.argv:
        g = json.load(open(OUT)) if os.path.exists(OUT) else build()
        i = sys.argv.index("--impact")
        return impact(g, sys.argv[i + 1] if len(sys.argv) > i + 1 else "")
    os.makedirs(OUT_DIR, exist_ok=True)
    g = build()
    # CANONICAL ORDER BEFORE WRITING. Both arrays come out in discovery order, and
    # discovery order is not stable: `set(...)` iterates under randomised string
    # hashing, so two consecutive builds of an UNCHANGED corpus emit thousands of
    # diff lines that are identical as sets. A rebuild is mandated after every
    # page edit, so that churn would be emitted constantly and a real graph change
    # would be invisible inside it. Both keys are already unique — nodes are
    # dict-keyed by `id`, edges deduplicated on (from, rel, to) — so the sort is
    # total.
    g["nodes"].sort(key=lambda n: n["id"])
    g["edges"].sort(key=lambda e: (e["from"], e["rel"], e["to"]))
    json.dump(g, open(OUT, "w"), indent=2)
    kinds = defaultdict(int)
    for n in g["nodes"]:
        kinds[n["kind"]] += 1
    rels = defaultdict(int)
    for e in g["edges"]:
        rels[e["rel"]] += 1
    print(f"{len(g['nodes'])} nodes, {len(g['edges'])} edges -> {os.path.relpath(OUT, ROOT)}")
    print(f"  nodes: {dict(kinds)}")
    print(f"  edges: {dict(rels)}")
    dangling = [n["id"] for n in g["nodes"] if n["kind"] == "kb" and n["path"] is None]
    if dangling:
        print(f"  DANGLING kb targets ({len(dangling)}): {', '.join(sorted(dangling)[:8])}"
              f"{' …' if len(dangling) > 8 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
