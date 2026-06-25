#!/usr/bin/env python3
"""
B111b - Targeted Oberschwaben source-note fix

B111 stabilized the public release state, but the intended source-note wording
did not hit the current HTML because the exact whitespace/text differed.
B111b performs a narrow targeted replacement in the Oberschwaben key-figure
source note.

Scope:
- index.html
- docs/B111b_oberschwaben_source_note_fix.md
- docs/B111b_oberschwaben_source_note_fix_audit.txt
- tasks/done.md

No map/data/layout changes.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B111b_oberschwaben_source_note_fix.md"
AUDIT = DOCS / "B111b_oberschwaben_source_note_fix_audit.txt"

OLD = "Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext, GISCO NUTS 2024;"
NEW = "Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;"

OLD2 = "eigene Verschneidung und Prüfung der Nutzungsklassen. Werte gerundet."
NEW2 = "eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet."

REQUIRED_AFTER = [
    NEW,
    NEW2,
    "~19.900 ha",
    "oberschwaben_agriculture.png",
    "oberschwaben_agriculture_moor_intersection.png",
]

FORBIDDEN_AFTER = [
    "Datenquelle in Umstellung",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B111b - Oberschwaben source-note fix"
    if marker in current:
        return
    entry = f"""
## B111b - Oberschwaben source-note fix ({date.today().isoformat()})

- Applied targeted source-note wording correction in the Oberschwaben key-figure capsule.
- Kept FIONA/BK50/GISCO public story state.
- Did not modify map paths, map images, CSS or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read_text(INDEX)
    before_counts = {p: html.count(p) for p in [OLD, OLD2] + REQUIRED_AFTER + FORBIDDEN_AFTER}

    n1 = html.count(OLD)
    n2 = html.count(OLD2)
    html2 = html.replace(OLD, NEW)
    html2 = html2.replace(OLD2, NEW2)

    after_counts = {p: html2.count(p) for p in [OLD, OLD2] + REQUIRED_AFTER + FORBIDDEN_AFTER}

    write_text(INDEX, html2)

    ok = (
        after_counts[OLD] == 0
        and after_counts[OLD2] == 0
        and all(after_counts[p] > 0 for p in REQUIRED_AFTER)
        and all(after_counts[p] == 0 for p in FORBIDDEN_AFTER)
    )

    report = [
        "# B111b - Oberschwaben Source Note Fix",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        f"Status: **{'OK' if ok else 'REVIEW REQUIRED'}**",
        "",
        "## Changes",
        "",
        f"- Replaced old source lead: `{n1}` occurrence(s)",
        f"- Replaced old method phrase: `{n2}` occurrence(s)",
        "",
        "## New visible source note",
        "",
        "```text",
        f"{NEW}",
        f"{NEW2}",
        "```",
        "",
        "## Scope",
        "",
        "- No CSS changes.",
        "- No map-path changes.",
        "- No map/data processing.",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit = [
        "# B111b audit",
        "",
        f"- Status: {'OK' if ok else 'REVIEW REQUIRED'}",
        "",
        "## Counts after patch",
        "",
        f"- Old source lead: {after_counts[OLD]}",
        f"- Old method phrase: {after_counts[OLD2]}",
        f"- New source lead: {after_counts[NEW]}",
        f"- New method phrase: {after_counts[NEW2]}",
        "",
        "## Forbidden/parked patterns",
    ]
    for p in FORBIDDEN_AFTER:
        audit.append(f"- {p}: {after_counts[p]}")
    audit.extend([
        "",
        "## Recommended checks",
        "",
        "```powershell",
        "Select-String -Path index.html -Pattern \"FIONA 2024\",\"eigene Auswahl\",\"Datenquelle in Umstellung\",\"oberschwaben_lgl\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(AUDIT, "\n".join(audit))

    update_done()

    print("B111b Oberschwaben source-note fix complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B111b_oberschwaben_source_note_fix_audit.txt")
    print("  Select-String -Path index.html -Pattern \"FIONA 2024\",\"eigene Auswahl\",\"Datenquelle in Umstellung\",\"oberschwaben_lgl\"")


if __name__ == "__main__":
    main()
