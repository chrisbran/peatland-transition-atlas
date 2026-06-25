#!/usr/bin/env python3
"""
B111 - Public release stabilization after FIONA restore

Purpose
-------
Stabilize the restored FIONA-based Oberschwaben public story without changing
map logic, data sources or map images.

B111 is intentionally conservative:
- no LGL work
- no map path rebinding
- no data processing
- no layout rewrite
- only small public wording/source-note consolidation and audit documentation

Changed files
-------------
- index.html
- docs/B111_public_release_stabilization.md
- docs/B111_public_release_stabilization_audit.txt
- tasks/done.md

Not changed
-----------
- src/styles.css, unless you manually edit it later
- public/maps/*
- data/*
- scripts/B106-B109 LGL parked material
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

REPORT = DOCS / "B111_public_release_stabilization.md"
AUDIT = DOCS / "B111_public_release_stabilization_audit.txt"

FORBIDDEN_VISIBLE_PATTERNS = [
    "Datenquelle in Umstellung",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
]

REQUIRED_PATTERNS = [
    "~19.900 ha",
    "FIONA 2024",
    "BK50 Moor-/Feuchtbodenkontext",
    "GISCO NUTS 2024",
    "oberschwaben_agriculture.png",
    "oberschwaben_agriculture_moor_intersection.png",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, changes: list[tuple[str, int]]) -> str:
    n = text.count(old)
    if n:
        text = text.replace(old, new)
    changes.append((old[:90].replace("\n", " ") + ("..." if len(old) > 90 else ""), n))
    return text


def normalize_oberschwaben_keyfigure_notes(html: str, changes: list[tuple[str, int]]) -> str:
    """
    Keep the current restored content, but make the source and interpretation
    notes consistent and less awkward. This is deliberately narrow and only
    affects the Oberschwaben key-figure capsule.
    """

    # Standardize source note.
    old_source = """Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext, GISCO NUTS 2024;
            eigene Verschneidung und Prüfung der Nutzungsklassen. Werte gerundet."""
    new_source = """Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
            eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet."""

    html = replace_once(html, old_source, new_source, changes)

    old_source_flat = "Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext, GISCO NUTS 2024; eigene Verschneidung und Prüfung der Nutzungsklassen. Werte gerundet."
    new_source_flat = "Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024; eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet."
    html = replace_once(html, old_source_flat, new_source_flat, changes)

    # Standardize method-note phrasing.
    old_method = """Lesart: Diese Werte geben räumliche Orientierung. Sie sind keine
            Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse."""
    new_method = """Lesart: Die Werte geben räumliche Orientierung. Sie sind keine
            Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse."""

    html = replace_once(html, old_method, new_method, changes)

    old_method_flat = "Lesart: Diese Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse."
    new_method_flat = "Lesart: Die Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse."
    html = replace_once(html, old_method_flat, new_method_flat, changes)

    return html


def audit_counts(html: str) -> dict[str, int]:
    keys = FORBIDDEN_VISIBLE_PATTERNS + REQUIRED_PATTERNS + [
        "Eignungskarte",
        "Priorisierung",
        "betriebliche Betroffenheitsanalyse",
        "eigene Auswahl, Klassifikation und Verschneidung",
    ]
    return {k: html.count(k) for k in keys}


def write_reports(before: dict[str, int], after: dict[str, int], changes: list[tuple[str, int]]) -> None:
    forbidden_after = {k: after.get(k, 0) for k in FORBIDDEN_VISIBLE_PATTERNS}
    required_after = {k: after.get(k, 0) for k in REQUIRED_PATTERNS}

    ok_forbidden = all(v == 0 for v in forbidden_after.values())
    ok_required = all(v > 0 for v in required_after.values())

    status = "OK" if ok_forbidden and ok_required else "REVIEW REQUIRED"

    report = [
        "# B111 - Public Release Stabilization",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        f"Status: **{status}**",
        "",
        "## Scope",
        "",
        "B111 keeps the restored FIONA-based Oberschwaben story. It does not change map data, map paths or map images.",
        "",
        "## What changed",
        "",
        "- Consolidated the Oberschwaben source note.",
        "- Standardized the interpretation note for the key figures.",
        "- Added an audit for LGL/B105 leftovers and required FIONA/BK50 map references.",
        "",
        "## Replacement counts",
        "",
        "| Operation | Count |",
        "|---|---:|",
    ]

    for label, n in changes:
        if n:
            safe = label.replace("|", "\\|")
            report.append(f"| `{safe}` | {n} |")

    report.extend([
        "",
        "## Required public-state checks",
        "",
        "| Pattern | Before | After | Expected |",
        "|---|---:|---:|---|",
    ])

    for k in REQUIRED_PATTERNS:
        report.append(f"| `{k}` | {before.get(k, 0)} | {after.get(k, 0)} | > 0 |")

    report.extend([
        "",
        "## Forbidden/parked-state checks",
        "",
        "| Pattern | Before | After | Expected |",
        "|---|---:|---:|---|",
    ])

    for k in FORBIDDEN_VISIBLE_PATTERNS:
        report.append(f"| `{k}` | {before.get(k, 0)} | {after.get(k, 0)} | 0 |")

    report.extend([
        "",
        "## Internal note",
        "",
        "FIONA remains the active public-story data basis for Oberschwaben in this branch. The LGL replacement work from B106-B109 is parked and should not be mixed into the public page unless deliberately reactivated later.",
        "",
        "For project documentation, FIONA usage and publication rights should remain flagged as an item to clarify.",
        "",
    ])

    write_text(REPORT, "\n".join(report))

    audit = [
        "# B111 audit",
        "",
        f"- Status: {status}",
        "",
        "## Required patterns",
    ]
    for k, v in required_after.items():
        audit.append(f"- {k}: {v}")

    audit.extend(["", "## Forbidden/parked patterns"])
    for k, v in forbidden_after.items():
        audit.append(f"- {k}: {v}")

    audit.extend([
        "",
        "## Recommended next commands",
        "",
        "```powershell",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])

    write_text(AUDIT, "\n".join(audit))


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B111 - Public release stabilization"
    if marker in current:
        return
    entry = f"""
## B111 - Public release stabilization ({date.today().isoformat()})

- Stabilized restored FIONA-based Oberschwaben public story.
- Consolidated source and interpretation notes.
- Confirmed LGL/source-swap leftovers are not active in `index.html`.
- Did not modify map data, map PNGs or LGL parked material.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    html = read_text(INDEX)
    before = audit_counts(html)

    changes: list[tuple[str, int]] = []
    html2 = normalize_oberschwaben_keyfigure_notes(html, changes)

    after = audit_counts(html2)

    write_text(INDEX, html2)
    write_reports(before, after, changes)
    update_done()

    print("B111 public release stabilization complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")

    print("")
    print("Review:")
    print("  Get-Content docs\\B111_public_release_stabilization_audit.txt")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
