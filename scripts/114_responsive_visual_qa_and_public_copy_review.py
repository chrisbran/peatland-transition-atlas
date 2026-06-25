#!/usr/bin/env python3
"""
B114 - Responsive visual QA and public copy release review

Purpose
-------
Create a manual QA package for the restored FIONA-based public version.

B114 does not modify the site. It creates a structured review protocol for:
- desktop/tablet/mobile scroll behaviour;
- Oberschwaben scrolly sequence;
- public copy and caveats;
- source-note visibility;
- release blockers;
- final screenshot/video review.

Scope
-----
Documentation/audit only:
- no index.html changes
- no CSS changes
- no map changes
- no data processing

Outputs
-------
docs/B114_responsive_visual_qa_plan.md
docs/B114_manual_test_matrix.csv
docs/B114_public_copy_and_risk_review.md
docs/B114_release_readiness_audit.txt
tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

QA_PLAN = DOCS / "B114_responsive_visual_qa_plan.md"
TEST_MATRIX = DOCS / "B114_manual_test_matrix.csv"
COPY_REVIEW = DOCS / "B114_public_copy_and_risk_review.md"
AUDIT = DOCS / "B114_release_readiness_audit.txt"

TODAY = date.today().isoformat()

REQUIRED_INDEX_PATTERNS = [
    "~19.900 ha",
    "FIONA 2024",
    "BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "eigene Auswahl, Klassifikation und Verschneidung",
    "oberschwaben_agriculture.png",
    "oberschwaben_moor_context.png",
    "oberschwaben_agriculture_moor_intersection.png",
]

FORBIDDEN_INDEX_PATTERNS = [
    "Datenquelle in Umstellung",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
    "Eignungspotenzial",
    "Wiedervernässungspotenzialkarte",
]

DESIRED_DOCS = [
    "docs/B110_external_source_register.md",
    "docs/B113_public_release_notes.md",
    "docs/B113_method_documentation.md",
    "docs/B113_release_checklist.md",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def count_occurrences(text: str, patterns: list[str]) -> dict[str, int]:
    return {p: text.count(p) for p in patterns}


def write_test_matrix() -> None:
    rows = [
        {
            "test_id": "VQA-001",
            "viewport": "1440x900 desktop",
            "section": "Full page",
            "test": "Scroll from top to bottom at normal reading speed",
            "expected": "No clipped headings; map stage transitions are stable; Oberschwaben section remains readable.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-002",
            "viewport": "1280x800 laptop",
            "section": "Central sticky story",
            "test": "Check global/europe/germany map stages",
            "expected": "Sticky map does not flicker; text cards remain within viewport; source notes do not dominate.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-003",
            "viewport": "1280x800 laptop",
            "section": "Oberschwaben",
            "test": "Check sequence: admin → agriculture → BK50 → intersection",
            "expected": "Each step has one clear visual change; no LGL test map appears; final intersection supports key figures.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-004",
            "viewport": "1024x768 tablet-ish",
            "section": "Oberschwaben",
            "test": "Check sticky stage height and step-card overlap",
            "expected": "No card blocks essential map area; headings and cards are readable.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-005",
            "viewport": "390x844 mobile",
            "section": "Full page",
            "test": "Check mobile fallback",
            "expected": "No horizontal overflow; maps scale down; text remains readable; sticky behaviour degrades gracefully.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-006",
            "viewport": "1440x900 desktop",
            "section": "Key figures",
            "test": "Check Oberschwaben key figures and source note",
            "expected": "~19.900 ha, FIONA 2024/BK50/GISCO source line and caveat visible but not visually dominant.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-007",
            "viewport": "1440x900 desktop",
            "section": "Pathways/value chain",
            "test": "Check that pathway cards read as Prüfpfade, not recommendations",
            "expected": "No wording implies direct site-level suitability or priority.",
            "result": "",
            "notes": "",
        },
        {
            "test_id": "VQA-008",
            "viewport": "Any",
            "section": "Sources/caveats",
            "test": "Search visible page for forbidden terms",
            "expected": "No active LGL/source-swap remnants; no internal QA labels like B98c or Flächen-QA.",
            "result": "",
            "notes": "",
        },
    ]
    with TEST_MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def qa_plan_text() -> str:
    return f"""# B114 – Responsive Visual QA Plan

Stand: {TODAY}

## Purpose

B114 defines the manual visual QA for the current restored FIONA-based public version of the Moore / Peatland Transition Atlas.

It should be used after B113 method documentation and before a broader public/demo release.

## Scope

This QA does not test scientific correctness of all source data. It checks whether the public page presents the current state clearly and without obvious layout, wording or source-state errors.

## Test setup

Run locally:

```powershell
cd C:\\Users\\User\\Documents\\GitHub\\peatland-transition-atlas
python -m http.server 8000
```

Open:

```text
http://localhost:8000/index.html
```

Recommended browser:

```text
Firefox or Chrome desktop, plus mobile viewport simulation in browser dev tools.
```

## Required viewports

| Viewport | Purpose |
|---|---|
| 1440 × 900 | main desktop reference |
| 1280 × 800 | typical laptop |
| 1024 × 768 | tablet-ish / constrained desktop |
| 390 × 844 | mobile fallback / phone portrait |

## Core visual questions

### A. Whole-page story

- Does the page move from global issue to regional implementation without abrupt jumps?
- Does the global hotspot sequence still feel necessary and not overly long?
- Does Germany/Baden-Württemberg prepare the Oberschwaben focus?
- Does the lower pathway/value-chain section follow logically from the map evidence?

### B. Oberschwaben section

Required order:

```text
admin context
→ agricultural use
→ BK50 Moor-/Feuchtbodenkontext
→ agriculture × BK50 intersection
→ key figures
→ pathways/value chains
```

Check:

- no active `oberschwaben_lgl` map appears;
- the old FIONA dark-map style remains active;
- the key figures follow from the intersection map;
- source note is visible but not visually dominant;
- method caveat remains close to the key figures.

### C. Sticky behaviour

Check:

- no heading is clipped by sticky offset;
- map stage is not too tall on laptop;
- step card does not obscure the key map signal;
- transitions are not flickering;
- mobile fallback is readable.

### D. Public copy

The text should not claim:

```text
Eignung
Priorisierung
Wiedervernässungspotenzial
betriebliche Betroffenheit
rechtliche Förderfähigkeit
hydrologische Machbarkeit
```

The text may claim:

```text
räumliche Orientierung
Schnittmenge
Planungskontext
Prüfpfade
Gesprächs-/Abstimmungsbedarf
```

## Manual test matrix

Use:

```text
docs/B114_manual_test_matrix.csv
```

Fill the `result` column with:

```text
PASS
WARN
FAIL
```

## Pass criteria

Minimum pass criteria:

- B58 returns `RESULT: PASS`;
- no active source-swap/LGL remnants in `index.html`;
- Oberschwaben sequence is visually stable at 1440 and 1280 px;
- no public copy implies site-level suitability or priority;
- source caveats are present in docs and compactly visible on page.

## Known non-blockers

The following are not release blockers for an MVP/demo:

- local untracked historical scripts/docs;
- parked LGL test outputs, as long as not active in public page;
- PowerShell 5.1 UTF-8 display artifacts in terminal output;
- source/method documentation still needing bibliographic completion, if release is explicitly internal/demo.

## Release blockers

For broader public dissemination:

- unresolved FIONA derivative-use/publication rights;
- missing BK50 class-selection table;
- incomplete FAOSTAT processing note;
- incomplete literature bibliography;
- untested mobile layout.
"""


def copy_review_text() -> str:
    return f"""# B114 – Public Copy and Risk Review

Stand: {TODAY}

## Current public copy position

The current page is suitable for a project/demo state if the caveats are kept visible in documentation and no stronger claims are added.

## Core wording rules

### Use

```text
räumliche Orientierung
Schnittmenge
Moor-/Feuchtbodenkontext
Nutzungskulisse
Planungskontext
Prüfpfad
Wertschöpfungspfad
regionale Abstimmung
```

### Avoid

```text
geeignete Flächen
Prioritätsflächen
Wiedervernässungspotenzial
Maßnahmenkarte
betriebliche Betroffenheit
rechtlich förderfähige Flächen
hydrologisch machbar
```

## Oberschwaben key figures

Keep the source note:

```text
Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet.
```

Keep the caveat:

```text
Lesart: Die Werte geben räumliche Orientierung. Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## FIONA risk language

For internal documentation:

```text
FIONA-based derived map products remain subject to final publication/derivative-use clarification.
```

For visible public copy, avoid overloading the story with legal caveats. The visible page should remain readable, while project documentation keeps the risk explicit.

## LGL branch language

Do not mention LGL in public story unless reactivated deliberately.

Internal language:

```text
The LGL Landnutzung source-swap branch was tested and parked because the resulting map was too fragmented for the current visual narrative without additional cartographic generalization.
```

## Value-chain/pathway section

The lower section should not read as a prescription. Preferred framing:

```text
Die Karte priorisiert keine Maßnahmen. Sie zeigt, welche Fragen regional zusammengeführt werden müssen.
```

Risky framing:

```text
Diese Flächen sollten wiedervernässt werden.
Diese Nutzung ist hier geeignet.
Dieser Pfad ist auf diesen Flächen empfohlen.
```

## Final copy-pass targets

For B115/B116, review:

- repeated uses of `zeigt`;
- overuse of `kann`;
- long sentences in step cards;
- source notes that interrupt reading flow;
- overly technical terms without immediate context.
"""


def audit_text(index_text: str, css_text: str) -> str:
    required_counts = {p: index_text.count(p) for p in REQUIRED_INDEX_PATTERNS}
    forbidden_counts = {p: index_text.count(p) for p in FORBIDDEN_INDEX_PATTERNS}
    desired_docs = {p: (ROOT / p).exists() for p in DESIRED_DOCS}

    ok_required = all(v > 0 for v in required_counts.values())
    ok_forbidden = all(v == 0 for v in forbidden_counts.values())
    has_viewport = "viewport" in index_text.lower()
    has_media_queries = "@media" in css_text

    status = "OK" if ok_required and ok_forbidden and has_viewport and has_media_queries else "REVIEW REQUIRED"

    lines = [
        "# B114 release readiness audit",
        "",
        f"Date: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Required index patterns",
        "",
    ]
    for p, c in required_counts.items():
        lines.append(f"- {p}: {c}")

    lines.extend(["", "## Forbidden / parked index patterns", ""])
    for p, c in forbidden_counts.items():
        lines.append(f"- {p}: {c}")

    lines.extend([
        "",
        "## Basic responsive infrastructure",
        "",
        f"- viewport meta present: {'YES' if has_viewport else 'NO'}",
        f"- CSS media queries present: {'YES' if has_media_queries else 'NO'}",
        "",
        "## Desired documentation files",
        "",
    ])
    for p, exists in desired_docs.items():
        lines.append(f"- {p}: {'OK' if exists else 'MISSING'}")

    lines.extend([
        "",
        "## B114 outputs",
        "",
        f"- {rel(QA_PLAN)}",
        f"- {rel(TEST_MATRIX)}",
        f"- {rel(COPY_REVIEW)}",
        "",
        "## Interpretation",
        "",
        "This audit checks structure and source-state patterns only. It does not replace manual browser scrolling and video review.",
        "",
    ])
    return "\n".join(lines)


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B114 - Responsive visual QA and public copy review"
    if marker in current:
        return
    entry = f"""
## B114 - Responsive visual QA and public copy review ({TODAY})

- Created responsive visual QA plan for desktop, laptop, tablet-like and mobile viewports.
- Created manual test matrix for Oberschwaben scrolly, key figures, source notes and pathway section.
- Created public copy/risk review for claims, caveats and parked LGL branch.
- Did not modify website, CSS, map images or data.
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

    write_text(QA_PLAN, qa_plan_text())
    write_test_matrix()
    write_text(COPY_REVIEW, copy_review_text())
    write_text(AUDIT, audit_text(index_text, css_text))
    update_done()

    print("B114 responsive visual QA and public copy review complete.")
    print("Changed/created:")
    for p in [QA_PLAN, TEST_MATRIX, COPY_REVIEW, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B114_release_readiness_audit.txt")
    print("  Import-Csv docs\\B114_manual_test_matrix.csv -Delimiter ';' | Format-Table -Auto")
    print("")
    print("No website, CSS, map or data files were modified.")


if __name__ == "__main__":
    main()
