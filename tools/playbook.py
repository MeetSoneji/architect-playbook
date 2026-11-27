#!/usr/bin/env python3
"""playbook.py — the deterministic half of the orchestrator.

The LLM decides *what to write*. This script decides *what is true*: which concepts
exist, which stage each one has really reached, what should run next, and whether
the labs actually prove their failure modes. Zero dependencies (Python 3.11+).

Commands
  validate          Check registry, folder layout and stage gates. Exit 1 on any error.
  labs [ID ...]     Run lab tests (all labs, or the given concept ids).
  next [--json]     Print the next work items for the scheduler, honouring the WIP limit.
  status            Regenerate STATUS.md and the schedule block in ROADMAP.md.
  scaffold ID       Create a concept folder from templates/ (used by DEEP_DIVE).
  feeds [--days N]  Pull new posts from sources/feeds.toml into inbox/drops.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import tomllib
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "curriculum.toml"
CONCEPTS = ROOT / "concepts"
TEMPLATES = ROOT / "templates"
INBOX = ROOT / "inbox" / "drops.md"
FEEDS = ROOT / "sources" / "feeds.toml"
FEEDS_SEEN = ROOT / "inbox" / ".feeds_seen.json"

STAGES = ["queued", "drafted", "proven", "mastered", "published"]

# One learner-first structure for every concept page (see EXPLAINING.md). post.md uses it too.
NOTES_HEADINGS = [
    "## 1. A moment you've lived",
    "## 2. The big idea",
    "## 3. Invent it yourself",
    "## 4. You've already used it",
    "## 5. How it really works",
    "## 6. When it goes wrong",
    "## 7. The price you pay",
    "## 8. The AI connection",
    "## 9. Remember and check",
    "## Prove it yourself",
    "## Going deeper",
    "## Sources",
]
INCIDENTS = "## 6. When it goes wrong"
LAB_HEADINGS = ["## Invariant", "## Failure injected", "## How to run", "## What you should observe"]
REVIEW_HEADINGS = ["## Teach-back", "## Attacks", "## Gaps found"]
PLACEHOLDER = re.compile(r"<!--\s*FILL", re.I)
MIN_SECTION_WORDS = {"## 3. Invent it yourself": 250, "## 4. You've already used it": 100,
                     "## 5. How it really works": 300, "## 6. When it goes wrong": 150,
                     "## 7. The price you pay": 120, "## 8. The AI connection": 150, "## 9. Remember and check": 80}
MIN_PREDICTIONS = 2  # predict-then-reveal moments: <details> blocks outside part 9
MIN_INCIDENT_LINKS = 2  # public postmortems / incident write-ups, linked
MIN_SOURCES = 3


# ----------------------------------------------------------------------------- registry
def load() -> dict:
    with REGISTRY.open("rb") as f:
        reg = tomllib.load(f)
    mods = {m["id"]: m for m in reg["modules"]}
    for c in reg["concepts"]:
        c["dir"] = CONCEPTS / mods[c["module"]]["slug"] / f'{c["id"]}-{c["slug"]}'
    reg["by_id"] = {c["id"]: c for c in reg["concepts"]}
    reg["mods"] = mods
    return reg


def week_date(reg: dict, week: int) -> dt.date:
    return reg["schedule"]["start"] + dt.timedelta(weeks=week - 1)


def current_week(reg: dict, today: dt.date | None = None) -> int:
    today = today or dt.date.today()
    return (today - reg["schedule"]["start"]).days // 7 + 1


def stage_ix(c: dict) -> int:
    return STAGES.index(c["stage"])


# ----------------------------------------------------------------------------- markdown helpers
def sections(text: str) -> dict[str, str]:
    """Map each '## ' heading line to the body below it (until the next '## ')."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = line.strip(), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def words(s: str) -> int:
    s = re.sub(r"```.*?```", "", s, flags=re.S)  # code blocks don't count as explanation
    return len(re.findall(r"[A-Za-z0-9']+", s))


# ----------------------------------------------------------------------------- gates
def check_notes(c: dict) -> list[str]:
    p = c["dir"] / "notes.md"
    if not p.exists():
        return [f"{c['id']}: stage '{c['stage']}' needs notes.md"]
    text, errs = p.read_text(), []
    sec = sections(text)
    for h in NOTES_HEADINGS:
        if h not in sec:
            errs.append(f"{c['id']}: notes.md missing heading '{h}'")
        elif not sec[h]:
            errs.append(f"{c['id']}: notes.md section '{h}' is empty")
    for h, n in MIN_SECTION_WORDS.items():
        if h in sec and words(sec[h]) < n:
            errs.append(f"{c['id']}: '{h}' has {words(sec[h])} words, gate is {n} (no surface summaries)")
    links = re.findall(r"\]\(https?://", sec.get(INCIDENTS, ""))
    if len(links) < MIN_INCIDENT_LINKS:
        errs.append(f"{c['id']}: 'Real incidents' links {len(links)} public write-ups, gate is {MIN_INCIDENT_LINKS}")
    if "```mermaid" not in sec.get("## 2. The big idea", "") + sec.get("## 5. How it really works", ""):
        errs.append(f"{c['id']}: part 2 or 5 needs a mermaid diagram")
    preds = sum(sec.get(h, "").count("<details>") for h in NOTES_HEADINGS[:8])
    if preds < MIN_PREDICTIONS:
        errs.append(f"{c['id']}: {preds} predict-then-reveal moments in parts 1-8, gate is {MIN_PREDICTIONS} (EXPLAINING.md)")
    if PLACEHOLDER.search(text):
        errs.append(f"{c['id']}: notes.md still has <!-- FILL --> placeholders")
    srcs = [l for l in sec.get("## Sources", "").splitlines() if l.lstrip().startswith(("-", "*", "1", "["))]
    if len(srcs) < MIN_SOURCES:
        errs.append(f"{c['id']}: notes.md cites {len(srcs)} sources, gate is {MIN_SOURCES}")
    return errs


def lab_tests(c: dict) -> list[Path]:
    lab = c["dir"] / "lab"
    return sorted(lab.glob("test_*.py")) if lab.exists() else []


def check_lab(c: dict) -> list[str]:
    lab, errs = c["dir"] / "lab", []
    readme = lab / "README.md"
    if not readme.exists():
        return [f"{c['id']}: stage '{c['stage']}' needs lab/README.md"]
    sec = sections(readme.read_text())
    errs += [f"{c['id']}: lab/README.md missing '{h}'" for h in LAB_HEADINGS if not sec.get(h)]
    src = "\n".join(t.read_text() for t in lab_tests(c))
    if not re.search(r"def test_simulate_failure_\w+", src):
        errs.append(f"{c['id']}: lab needs a test_simulate_failure_* test (negative control: failure happens without the mechanism)")
    if not re.search(r"def test_recovery_\w+", src):
        errs.append(f"{c['id']}: lab needs a test_recovery_* test (same fault, mechanism keeps the invariant)")
    if re.search(r"^\s*(import|from)\s+(requests|numpy|pytest)\b", src, re.M):
        errs.append(f"{c['id']}: lab tests must be zero-dependency (stdlib only)")
    return errs


def check_review(c: dict) -> list[str]:
    p = c["dir"] / "review.md"
    if not p.exists():
        return [f"{c['id']}: stage 'mastered' needs review.md from a /challenge session"]
    text = p.read_text()
    errs = []
    if frontmatter(text).get("verdict") != "pass":
        errs.append(f"{c['id']}: review.md verdict must be 'pass' to be mastered")
    sec = sections(text)
    errs += [f"{c['id']}: review.md section '{h}' is empty" for h in REVIEW_HEADINGS if not sec.get(h)]
    return errs


def check_post(c: dict) -> list[str]:
    p = c["dir"] / "post.md"
    if not p.exists():
        return [f"{c['id']}: stage 'published' needs post.md"]
    fm = frontmatter(p.read_text())
    errs = []
    if fm.get("status") != "ready":
        errs.append(f"{c['id']}: post.md frontmatter status must be 'ready'")
    if not fm.get("two_audience_check"):
        errs.append(f"{c['id']}: post.md frontmatter needs two_audience_check")
    for f in ("video.md", "video/script.json", "video/scenes.js"):
        if not (c["dir"] / f).exists():
            errs.append(f"{c['id']}: stage 'published' needs {f} (see EXPLAINING.md, From page to video)")
    return errs


GATES = {"drafted": [check_notes], "proven": [check_lab], "mastered": [check_review], "published": [check_post]}


def validate(reg: dict) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    ids = [c["id"] for c in reg["concepts"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate concept ids in curriculum.toml")
    for c in reg["concepts"]:
        if c["module"] not in reg["mods"]:
            errs.append(f"{c['id']}: unknown module {c['module']}")
        if c["stage"] not in STAGES:
            errs.append(f"{c['id']}: unknown stage {c['stage']}")
            continue
        for r in c.get("requires", []):
            if r not in reg["by_id"]:
                errs.append(f"{c['id']}: requires unknown concept {r}")
            elif stage_ix(c) >= 1 and reg["by_id"][r]["stage"] == "queued":
                warns.append(f"{c['id']}: started before prerequisite {r} (fine, but link it as a forward reference)")
        for stage in STAGES[1:stage_ix(c) + 1]:
            for gate in GATES[stage]:
                errs += gate(c)
    known = {c["dir"].resolve() for c in reg["concepts"]}
    if CONCEPTS.exists():
        for d in CONCEPTS.glob("*/c*-*"):
            if d.is_dir() and d.resolve() not in known:
                errs.append(f"orphan concept folder not in curriculum.toml: {d.relative_to(ROOT)}")
    return errs, warns


# ----------------------------------------------------------------------------- labs
def run_labs(reg: dict, only: list[str]) -> int:
    failed = 0
    for c in reg["concepts"]:
        if only and c["id"] not in only:
            continue
        if not lab_tests(c):
            continue
        lab = c["dir"] / "lab"
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(lab), "-p", "test_*.py", "-v"],
                           cwd=lab, capture_output=True, text=True)
        ok = r.returncode == 0
        print(f"{'PASS' if ok else 'FAIL'}  {c['id']}  {lab.relative_to(ROOT)}")
        if not ok:
            print(r.stdout[-3000:], r.stderr[-3000:], sep="\n")
            failed += 1
    return failed


# ----------------------------------------------------------------------------- scheduler
def next_items(reg: dict, today: dt.date | None = None) -> list[dict]:
    """Decide the next workflow runs. Pure function of the registry + date, so it is testable.

    Order of preference (finish work before starting work):
      1. PUBLISH every mastered concept.
      2. BUILD_LAB every drafted concept.
      3. Proven concepts wait on Meet (CHALLENGE is interactive, never automated).
      4. DEEP_DIVE the earliest queued concept whose week has arrived, if under the WIP limit.
    """
    wk = current_week(reg, today)
    items = []
    for c in sorted(reg["concepts"], key=lambda c: c["week"]):
        if c["stage"] == "mastered":
            items.append({"workflow": "PUBLISH", "concept": c["id"], "title": c["title"]})
    for c in sorted(reg["concepts"], key=lambda c: c["week"]):
        if c["stage"] == "drafted":
            items.append({"workflow": "BUILD_LAB", "concept": c["id"], "title": c["title"]})
    for c in sorted(reg["concepts"], key=lambda c: c["week"]):
        if c["stage"] == "proven":
            items.append({"workflow": "WAITING_ON_MEET", "concept": c["id"], "title": c["title"],
                          "note": "run /challenge " + c["id"]})
    active = sum(c["stage"] in ("drafted", "proven") for c in reg["concepts"])
    queued = sorted((c for c in reg["concepts"] if c["stage"] == "queued"), key=lambda c: c["week"])
    if queued and active < reg["schedule"]["wip_limit"] and queued[0]["week"] <= wk:
        c = queued[0]
        items.append({"workflow": "DEEP_DIVE", "concept": c["id"], "title": c["title"]})
    elif queued and active >= reg["schedule"]["wip_limit"]:
        items.append({"workflow": "BLOCKED_BY_WIP", "concept": queued[0]["id"], "title": queued[0]["title"],
                      "note": f"{active} concepts in flight (limit {reg['schedule']['wip_limit']}); master one first"})
    if INBOX.exists() and pending_drops():
        items.append({"workflow": "INGEST", "concept": None, "title": f"{len(pending_drops())} inbox drops"})
    return items


def pending_drops() -> list[str]:
    sec = sections(INBOX.read_text()).get("## Pending", "")
    return [l for l in sec.splitlines() if re.match(r"\s*-\s+\S", l) and "(drop" not in l]


# ----------------------------------------------------------------------------- status rendering
def render_status(reg: dict) -> None:
    wk = current_week(reg)
    lines = ["# Status", "", "> Generated by `python3 tools/playbook.py status`. Do not edit by hand.", "",
             f"Roadmap week **{wk}** (week 1 = {reg['schedule']['start']}). Stages: "
             + " → ".join(f"`{s}`" for s in STAGES) + ".", ""]
    counts = {s: sum(c["stage"] == s for c in reg["concepts"]) for s in STAGES}
    lines += ["| " + " | ".join(STAGES) + " |", "|" + "---|" * len(STAGES),
              "| " + " | ".join(str(counts[s]) for s in STAGES) + " |", ""]
    for m in reg["modules"]:
        lines += [f"## {m['id'].upper()}: {m['title']}", "", "| Id | Concept | Stage | Week | Notes | Lab | Review | Post |",
                  "|---|---|---|---|---|---|---|---|"]
        for c in (c for c in reg["concepts"] if c["module"] == m["id"]):
            rel = c["dir"].relative_to(ROOT)

            def link(name, path):
                return f"[{name}]({rel}/{path})" if (c["dir"] / path).exists() else "—"
            lines.append(f"| {c['id']} | {c['title']} | `{c['stage']}` | {c['week']} | {link('notes', 'notes.md')} | "
                         f"{link('lab', 'lab/README.md')} | {link('review', 'review.md')} | {link('post', 'post.md')} |")
        lines.append("")
    lines += ["## Next up", ""] + [f"- **{i['workflow']}** {i['concept'] or ''} {i['title']}"
                                  + (f" ({i['note']})" if i.get("note") else "") for i in next_items(reg)] + [""]
    (ROOT / "STATUS.md").write_text("\n".join(lines))

    roadmap = ROOT / "ROADMAP.md"
    if roadmap.exists():
        rows = ["| Week | Starts | Id | Concept | The AI-era question it answers | Stage |", "|---|---|---|---|---|---|"]
        for c in sorted(reg["concepts"], key=lambda c: c["week"]):
            rows.append(f"| {c['week']} | {week_date(reg, c['week']):%b %d %Y} | {c['id']} | {c['title']} | {c.get('ai_question', '')} | `{c['stage']}` |")
        text = roadmap.read_text()
        text = re.sub(r"(<!-- BEGIN:schedule -->\n).*?(<!-- END:schedule -->)",
                      lambda m: m.group(1) + "\n".join(rows) + "\n" + m.group(2), text, flags=re.S)
        roadmap.write_text(text)
    print("wrote STATUS.md" + (" and ROADMAP.md schedule" if roadmap.exists() else ""))


# ----------------------------------------------------------------------------- scaffold
def scaffold(reg: dict, cid: str) -> None:
    c = reg["by_id"][cid]
    (c["dir"] / "lab").mkdir(parents=True, exist_ok=True)
    notes = c["dir"] / "notes.md"
    if not notes.exists():
        t = (TEMPLATES / "notes.md").read_text()
        reqs = ", ".join(f"{r} ({reg['by_id'][r]['title']})" for r in c.get("requires", [])) or "none"
        t = (t.replace("{{id}}", c["id"]).replace("{{title}}", c["title"]).replace("{{module}}", reg["mods"][c["module"]]["title"])
              .replace("{{requires}}", reqs).replace("{{bedrock}}", "; ".join(c.get("bedrock", [])))
              .replace("{{ai_question}}", c.get("ai_question", "")))
        notes.write_text(t)
    lab_readme = c["dir"] / "lab" / "README.md"
    if not lab_readme.exists():
        lab_readme.write_text((TEMPLATES / "lab_README.md").read_text().replace("{{id}}", c["id"]).replace("{{title}}", c["title"]))
    print(c["dir"].relative_to(ROOT))


# ----------------------------------------------------------------------------- feeds
def fetch_feeds(days: int) -> None:
    with FEEDS.open("rb") as f:
        feeds = tomllib.load(f)["feeds"]
    seen = set(json.loads(FEEDS_SEEN.read_text())) if FEEDS_SEEN.exists() else set()
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    new, failures = [], []
    for fd in feeds:
        try:
            req = urllib.request.Request(fd["url"], headers={"User-Agent": "architect-playbook-feeds/1.0"})
            root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
        except Exception as e:  # network policy, dead feed, bad XML: report, don't crash the run
            failures.append(f"{fd['name']}: {type(e).__name__}")
            continue
        for title, link, date in parse_feed(root):
            if link in seen or (date and date < cutoff):
                continue
            seen.add(link)
            new.append(f"- [{title}]({link}) — {fd['name']}{', ' + date.date().isoformat() if date else ''} `auto`")
    if new:
        text = INBOX.read_text()
        text = text.replace("## Pending\n", "## Pending\n" + "\n".join(new) + "\n", 1)
        INBOX.write_text(text)
    FEEDS_SEEN.write_text(json.dumps(sorted(seen), indent=0))
    print(f"{len(new)} new items added to inbox/drops.md")
    for f_ in failures:
        print(f"unreachable: {f_}")


def parse_feed(root: ET.Element):
    ns = {"a": "http://www.w3.org/2005/Atom"}
    from email.utils import parsedate_to_datetime
    for it in root.iter("item"):  # RSS 2.0
        d = it.findtext("pubDate")
        try:
            date = parsedate_to_datetime(d) if d else None
        except (TypeError, ValueError):
            date = None
        yield (it.findtext("title") or "").strip(), (it.findtext("link") or "").strip(), date
    for e in root.iter("{http://www.w3.org/2005/Atom}entry"):  # Atom
        link = e.find("a:link[@rel='alternate']", ns) or e.find("a:link", ns)
        d = e.findtext("a:published", namespaces=ns) or e.findtext("a:updated", namespaces=ns)
        try:
            date = dt.datetime.fromisoformat(d.replace("Z", "+00:00")) if d else None
        except ValueError:
            date = None
        yield (e.findtext("a:title", namespaces=ns) or "").strip(), (link.get("href") if link is not None else ""), date


# ----------------------------------------------------------------------------- cli
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    p = sub.add_parser("labs"); p.add_argument("ids", nargs="*")
    p = sub.add_parser("next"); p.add_argument("--json", action="store_true")
    sub.add_parser("status")
    p = sub.add_parser("scaffold"); p.add_argument("id")
    p = sub.add_parser("feeds"); p.add_argument("--days", type=int, default=8)
    a = ap.parse_args()
    reg = load()

    if a.cmd == "validate":
        errs, warns = validate(reg)
        for w in warns:
            print("warn ", w)
        for e in errs:
            print("ERROR", e)
        print(f"{len(errs)} errors, {len(warns)} warnings")
        return 1 if errs else 0
    if a.cmd == "labs":
        return 1 if run_labs(reg, a.ids) else 0
    if a.cmd == "next":
        items = next_items(reg)
        if a.json:
            print(json.dumps(items, indent=2))
        else:
            for i in items:
                print(f"{i['workflow']:<16} {i['concept'] or '-':<4} {i['title']}" + (f"  ({i['note']})" if i.get("note") else ""))
        return 0
    if a.cmd == "status":
        render_status(reg)
        return 0
    if a.cmd == "scaffold":
        scaffold(reg, a.id)
        return 0
    if a.cmd == "feeds":
        fetch_feeds(a.days)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
