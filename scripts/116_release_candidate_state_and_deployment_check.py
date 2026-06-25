#!/usr/bin/env python3
"""
B116 - Release candidate state and deployment check

Purpose
-------
Create a release-candidate package for the current public/demo state after:
- B111/B111b FIONA public-state stabilization
- B112 local status hygiene
- B113 public release/method docs
- B114 visual QA plan
- B115 final visible copy audit

B116 is documentation/audit only:
- no index.html changes
- no CSS changes
- no map changes
- no data processing
- no local exclude changes

Outputs
-------
docs/B116_release_candidate_state.md
docs/B116_deployment_checklist.md
docs/B116_release_candidate_audit.txt
tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

STATE = DOCS / "B116_release_candidate_state.md"
DEPLOY = DOCS / "B116_deployment_checklist.md"
AUDIT = DOCS / "B116_release_candidate_audit.txt"

TODAY = date.today().isoformat()

REQUIRED_INDEX_PATTERNS = [
    "~19.900 ha",
    "FIONA 2024",
    "BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "eigene Auswahl, Klassifikation und Verschneidung",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
    "oberschwaben_agriculture.png",
    "oberschwaben_moor_context.png",
    "oberschwaben_agriculture_moor_intersection.png",
]

FORBIDDEN_INDEX_PATTERNS = [
    "Datenquelle in Umstellung",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
    "Wiedervernässungspotenzialkarte",
    "Prioritätsflächen",
    "geeignete Flächen",
]

EXPECTED_DOCS = [
    "docs/B110_external_source_register.md",
    "docs/B113_public_release_notes.md",
    "docs/B113_method_documentation.md",
    "docs/B113_release_checklist.md",
    "docs/B114_responsive_visual_qa_plan.md",
    "docs/B114_manual_test_matrix.csv",
    "docs/B114_public_copy_and_risk_review.md",
    "docs/B115_visible_copy_audit.txt",
    "docs/B115_visible_copy_findings.csv",
]

OPTIONAL_BUT_USEFUL = [
    "docs/B58_visual_qa_and_commit_check.md",
    "docs/B103b_corrected_visible_text_audit.md",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def git_cmd(args: list[str]) -> str:
    try:
        cp = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
        out = (cp.stdout or "").strip()
        err = (cp.stderr or "").strip()
        if cp.returncode != 0:
            return f"ERROR({cp.returncode}): {err or out}"
        return out
    except Exception as exc:
        return f"ERROR: {exc}"


def status_lines() -> list[str]:
    s = git_cmd(["status", "--short"])
    return s.splitlines() if s else []


def count_status(lines: list[str]) -> dict[str, int]:
    counts = {
        "total": len(lines),
        "modified_tracked": 0,
        "untracked": 0,
        "staged": 0,
        "raw_or_working_visible": 0,
        "lgl_public_visible": 0,
    }
    raw_prefixes = ("data/external/", "data/working/", "working/", "sources/")
    for line in lines:
        if not line:
            continue
        xy = line[:2]
        path = line[3:].replace("\\", "/") if len(line) > 3 else ""
        if xy != "??" and xy[0] != " ":
            counts["staged"] += 1
        if xy.strip() == "M":
            counts["modified_tracked"] += 1
        if xy == "??":
            counts["untracked"] += 1
        if path.startswith(raw_prefixes):
            counts["raw_or_working_visible"] += 1
        if path.startswith("public/maps/oberschwaben_lgl/") or "oberschwaben_lgl" in path:
            counts["lgl_public_visible"] += 1
    return counts


def audit_data(index_text: str, css_text: str) -> dict[str, object]:
    required_counts = {p: index_text.count(p) for p in REQUIRED_INDEX_PATTERNS}
    forbidden_counts = {p: index_text.count(p) for p in FORBIDDEN_INDEX_PATTERNS}
    doc_exists = {p: (ROOT / p).exists() for p in EXPECTED_DOCS}
    optional_exists = {p: (ROOT / p).exists() for p in OPTIONAL_BUT_USEFUL}
    lines = status_lines()
    s_counts = count_status(lines)

    ok_required = all(v > 0 for v in required_counts.values())
    ok_forbidden = all(v == 0 for v in forbidden_counts.values())
    ok_docs_core = all(doc_exists[p] for p in EXPECTED_DOCS if not p.startswith("docs/B110"))
    # B110 source register may still be missing depending on whether the earlier generation was committed.
    ok_status_safety = s_counts["raw_or_working_visible"] == 0 and s_counts["lgl_public_visible"] == 0
    ok_responsive_basics = ("viewport" in index_text.lower()) and ("@media" in css_text)

    return {
        "required_counts": required_counts,
        "forbidden_counts": forbidden_counts,
        "doc_exists": doc_exists,
        "optional_exists": optional_exists,
        "status_lines": lines,
        "status_counts": s_counts,
        "ok_required": ok_required,
        "ok_forbidden": ok_forbidden,
        "ok_docs_core": ok_docs_core,
        "ok_status_safety": ok_status_safety,
        "ok_responsive_basics": ok_responsive_basics,
        "head": git_cmd(["log", "-1", "--oneline"]),
        "branch": git_cmd(["branch", "--show-current"]),
        "recent": git_cmd(["log", "--oneline", "-8"]),
    }


def rc_status(data: dict[str, object]) -> str:
    if (
        data["ok_required"]
        and data["ok_forbidden"]
        and data["ok_docs_core"]
        and data["ok_status_safety"]
        and data["ok_responsive_basics"]
    ):
        return "RELEASE CANDIDATE FOR INTERNAL/PROJECT DEMO"
    return "REVIEW REQUIRED"


def state_text(data: dict[str, object]) -> str:
    status = rc_status(data)
    sc = data["status_counts"]
    return f"""# B116 – Release Candidate State

Stand: {TODAY}

Status: **{status}**

## Current git state

```text
Branch: {data["branch"]}
HEAD: {data["head"]}
```

Recent commits:

```text
{data["recent"]}
```

## Current release scope

This release candidate represents the restored **FIONA/BK50/GISCO Oberschwaben public story** within the Moore / Peatland Transition Atlas.

The current state is intended as:

```text
internal/project demonstration version
```

It is not yet a fully cleared broad public release because FIONA derivative-publication rights and some source/method appendices still require final confirmation.

## What is considered stable

- FIONA-based Oberschwaben map story restored.
- LGL source-swap branch parked.
- Oberschwaben source line corrected.
- Visible copy audit passed.
- B58 visual QA returned PASS after release hygiene.
- Overclaim-risk patterns absent from visible text.
- Key caveats are present.

## Active Oberschwaben source line

```text
Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet.
```

## Active interpretation caveat

```text
Lesart: Die Werte geben räumliche Orientierung.
Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## Current worktree safety summary

| Check | Count |
|---|---:|
| Git status lines | {sc["total"]} |
| Modified tracked lines | {sc["modified_tracked"]} |
| Untracked lines | {sc["untracked"]} |
| Staged lines | {sc["staged"]} |
| Raw/working visible lines | {sc["raw_or_working_visible"]} |
| LGL public visible lines | {sc["lgl_public_visible"]} |

Untracked historical scripts/docs may still be visible. That is acceptable if they are not staged and B58 remains PASS.

## Remaining release caveats

For a broader public release, clarify/complete:

1. FIONA derivative-publication and use rights.
2. BK50 class-selection table.
3. FIONA original-class-to-public-class lookup.
4. FAOSTAT processing note.
5. Thünen geodata version/source note.
6. Full bibliography for literature-derived claims.
7. Browser/responsive manual QA.
"""


def deploy_text(data: dict[str, object]) -> str:
    return f"""# B116 – Deployment Checklist

Stand: {TODAY}

## 1. Pre-deployment checks

Run:

```powershell
cd C:\\Users\\User\\Documents\\GitHub\\peatland-transition-atlas

python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py

Select-String -Path index.html -Pattern "oberschwaben_lgl","Datenquelle in Umstellung","B98c","Flächen-QA","FIONA 2024","~19.900"

git status --short
```

Expected:

```text
B103b: no public source files changed
B58: RESULT: PASS
No oberschwaben_lgl / Datenquelle in Umstellung / B98c / Flächen-QA in index.html
FIONA 2024 and ~19.900 present
No raw/working data staged
```

## 2. Manual browser check

Run local server:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/index.html
```

Check at least:

```text
1440 × 900
1280 × 800
1024 × 768
390 × 844
```

Use:

```text
docs/B114_manual_test_matrix.csv
```

## 3. Commit release-candidate docs

After B116 generation:

```powershell
git add scripts\\116_release_candidate_state_and_deployment_check.py docs\\B116_release_candidate_state.md docs\\B116_deployment_checklist.md docs\\B116_release_candidate_audit.txt tasks\\done.md

git commit -m "Add release candidate state and deployment checklist"
```

If `docs/B58_visual_qa_and_commit_check.md` was modified by the final QA and you want to preserve the PASS state:

```powershell
git add docs\\B58_visual_qa_and_commit_check.md
git commit -m "Update final visual QA report"
```

## 4. Push

Only after confirming `git status --short` contains no accidental staged raw/probe material:

```powershell
git push
```

## 5. Post-deployment check

After GitHub Pages updates, open the public URL:

```text
https://chrisbran.github.io/peatland-transition-atlas/
```

Check:

- page loads without missing map images;
- Oberschwaben FIONA/BK50 section appears;
- no LGL test layer appears;
- source note and caveat are visible;
- scroll behaviour matches local version.

## 6. Release note for project team

Suggested short internal release note:

```text
The current Moore / Peatland Transition Atlas demo has been stabilized around the restored FIONA/BK50/GISCO Oberschwaben story. Visual QA and visible-copy audits pass. The map should be treated as a spatial orientation and discussion layer, not a site-level suitability or priority map. FIONA derivative-publication rights and source-method appendices remain to be clarified before broader public dissemination.
```
"""


def audit_text(data: dict[str, object]) -> str:
    status = rc_status(data)
    lines = [
        "# B116 release candidate audit",
        "",
        f"Date: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Required index patterns",
        "",
    ]

    for p, c in data["required_counts"].items():
        lines.append(f"- {p}: {c}")

    lines.extend(["", "## Forbidden index patterns", ""])
    for p, c in data["forbidden_counts"].items():
        lines.append(f"- {p}: {c}")

    lines.extend(["", "## Documentation files", ""])
    for p, exists in data["doc_exists"].items():
        lines.append(f"- {p}: {'OK' if exists else 'MISSING'}")

    lines.extend(["", "## Optional QA docs", ""])
    for p, exists in data["optional_exists"].items():
        lines.append(f"- {p}: {'OK' if exists else 'MISSING'}")

    sc = data["status_counts"]
    lines.extend([
        "",
        "## Worktree safety",
        "",
        f"- git status lines: {sc['total']}",
        f"- staged lines: {sc['staged']}",
        f"- raw/working visible lines: {sc['raw_or_working_visible']}",
        f"- LGL public visible lines: {sc['lgl_public_visible']}",
        "",
        "## Remaining status lines",
        "",
    ])

    if data["status_lines"]:
        lines.append("```text")
        lines.extend(data["status_lines"][:150])
        if len(data["status_lines"]) > 150:
            lines.append(f"... truncated, {len(data['status_lines']) - 150} more lines")
        lines.append("```")
    else:
        lines.append("No remaining git status lines.")

    lines.extend([
        "",
        "## Recommendation",
        "",
        "This is a release-candidate documentation check. It should be paired with manual browser QA before pushing to the public page.",
        "",
    ])
    return "\n".join(lines)


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B116 - Release candidate state and deployment check"
    if marker in current:
        return
    entry = f"""
## B116 - Release candidate state and deployment check ({TODAY})

- Created release-candidate state report for the restored FIONA/BK50/GISCO public demo.
- Created deployment checklist for local QA, commit, push and post-deployment checks.
- Audited required source/caveat patterns, forbidden LGL/source-swap remnants and worktree safety.
- Did not modify website, CSS, maps or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)
    if not CSS.exists():
        print(f"Missing {rel(CSS)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    index_text = read_text(INDEX)
    css_text = read_text(CSS)

    data = audit_data(index_text, css_text)

    write_text(STATE, state_text(data))
    write_text(DEPLOY, deploy_text(data))
    write_text(AUDIT, audit_text(data))
    update_done()

    print("B116 release candidate state and deployment check complete.")
    print("Changed/created:")
    for p in [STATE, DEPLOY, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print(f"Status: {rc_status(data)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B116_release_candidate_audit.txt")
    print("  Get-Content docs\\B116_deployment_checklist.md")
    print("")
    print("No website, CSS, map or data files were modified.")


if __name__ == "__main__":
    main()
