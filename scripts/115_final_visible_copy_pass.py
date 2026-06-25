#!/usr/bin/env python3
"""
B115 - Final visible copy pass and no-overclaim audit

Purpose
-------
Perform a conservative final copy pass on the public page.

B115 is intentionally narrow:
- no map changes
- no data changes
- no layout/CSS changes
- no LGL reactivation
- only targeted wording replacements when risky public-copy phrases are present
- plus a visible-copy audit for overclaiming and missing caveats

Changed files
-------------
- index.html, only if targeted risky phrases are found
- docs/B115_final_visible_copy_pass.md
- docs/B115_visible_copy_audit.txt
- docs/B115_visible_copy_findings.csv
- tasks/done.md

Not changed
-----------
- src/styles.css
- public/maps/*
- data/*
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import html
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B115_final_visible_copy_pass.md"
AUDIT = DOCS / "B115_visible_copy_audit.txt"
FINDINGS = DOCS / "B115_visible_copy_findings.csv"

TODAY = date.today().isoformat()

# Replacements are deliberately conservative and avoid changing the required caveat:
# "keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse".
REPLACEMENTS = [
    ("Wiedervernässungspotenzialkarte", "Schnittmengenkarte"),
    ("Wiedervernässungspotenzial", "Wiedervernässungsfrage"),
    ("geeignete Flächen", "zu prüfende Räume"),
    ("geeignete Standorte", "zu prüfende Standorte"),
    ("Prioritätsflächen", "Prüfräume"),
    ("Maßnahmenkarte", "Orientierungskarte"),
    ("betroffene Betriebe", "betriebliche Kontexte"),
    ("hydrologisch machbar", "hydrologisch zu prüfen"),
    ("rechtlich förderfähige Flächen", "förderrechtlich zu prüfende Flächen"),
    ("fertige Empfehlungen", "Prüf- und Abstimmungsbedarf"),
]

RISK_PATTERNS = [
    "Wiedervernässungspotenzial",
    "Wiedervernässungspotenzialkarte",
    "geeignete Flächen",
    "geeignete Standorte",
    "Prioritätsflächen",
    "Maßnahmenkarte",
    "betroffene Betriebe",
    "hydrologisch machbar",
    "rechtlich förderfähige Flächen",
    "fertige Empfehlungen",
    "oberschwaben_lgl",
    "Datenquelle in Umstellung",
    "B98c",
    "Flächen-QA",
]

REQUIRED_SAFE_PATTERNS = [
    "räumliche Orientierung",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
    "FIONA 2024",
    "BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "eigene Auswahl, Klassifikation und Verschneidung",
    "~19.900 ha",
]

WATCH_TERMS = [
    "Potenzial",
    "geeignet",
    "Priorität",
    "Maßnahme",
    "Empfehlung",
    "Betroffenheit",
    "Machbarkeit",
    "Förderfähigkeit",
    "sollte",
    "muss",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_to_visible_text(raw: str) -> str:
    """Approximate visible text for copy QA."""
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def replacement_pass(index_text: str) -> tuple[str, list[dict[str, str]]]:
    changed = index_text
    rows: list[dict[str, str]] = []

    for old, new in REPLACEMENTS:
        n = changed.count(old)
        if n:
            changed = changed.replace(old, new)
        rows.append({
            "type": "replacement",
            "pattern": old,
            "replacement": new,
            "count_before": str(n),
            "count_after": str(changed.count(old)),
            "status": "changed" if n else "not_found",
        })

    return changed, rows


def add_audit_rows(index_text: str, visible_text: str, rows: list[dict[str, str]]) -> None:
    for p in RISK_PATTERNS:
        c = visible_text.count(p)
        rows.append({
            "type": "risk_pattern_visible",
            "pattern": p,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "OK" if c == 0 else "REVIEW",
        })

    for p in REQUIRED_SAFE_PATTERNS:
        c = visible_text.count(p)
        rows.append({
            "type": "required_safe_pattern_visible",
            "pattern": p,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "OK" if c > 0 else "MISSING",
        })

    for p in WATCH_TERMS:
        c = visible_text.count(p)
        rows.append({
            "type": "watch_term_visible",
            "pattern": p,
            "replacement": "",
            "count_before": str(c),
            "count_after": str(c),
            "status": "WATCH" if c > 0 else "OK",
        })


def write_findings(rows: list[dict[str, str]]) -> None:
    fieldnames = ["type", "pattern", "replacement", "count_before", "count_after", "status"]
    with FINDINGS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        "replacements_changed": sum(1 for r in rows if r["type"] == "replacement" and r["status"] == "changed"),
        "risk_reviews": sum(1 for r in rows if r["type"] == "risk_pattern_visible" and r["status"] == "REVIEW"),
        "missing_required": sum(1 for r in rows if r["type"] == "required_safe_pattern_visible" and r["status"] == "MISSING"),
        "watch_terms": sum(1 for r in rows if r["type"] == "watch_term_visible" and r["status"] == "WATCH"),
    }


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B115 - Final visible copy pass and no-overclaim audit"
    if marker in current:
        return
    entry = f"""
## B115 - Final visible copy pass and no-overclaim audit ({TODAY})

- Ran a conservative final copy pass for risky public-copy phrases.
- Created visible-copy audit for overclaiming, required caveats and watch terms.
- Kept FIONA/BK50/GISCO Oberschwaben public state active.
- Did not modify maps, CSS, data or LGL parked material.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def report_text(summary: dict[str, int], changed_files: list[str]) -> str:
    status = "OK" if summary["risk_reviews"] == 0 and summary["missing_required"] == 0 else "REVIEW REQUIRED"

    return f"""# B115 – Final Visible Copy Pass

Stand: {TODAY}

Status: **{status}**

## Scope

B115 performs a conservative final copy pass and no-overclaim audit for the restored FIONA-based public page.

It does not change:

- map paths;
- map images;
- CSS/layout;
- data processing;
- the parked LGL branch.

## Changed files

{chr(10).join(f"- `{p}`" for p in changed_files)}

## Summary

| Check | Count |
|---|---:|
| Targeted replacements applied | {summary["replacements_changed"]} |
| Risk patterns remaining in visible text | {summary["risk_reviews"]} |
| Required safe/caveat patterns missing | {summary["missing_required"]} |
| Watch terms present | {summary["watch_terms"]} |

## Interpretation

A `WATCH` term is not automatically a problem. For example, `Maßnahme` or `Potenzial` can appear in a negated caveat or a general explanatory context. Remaining `WATCH` terms should be reviewed in `docs/B115_visible_copy_findings.csv`.

A `REVIEW` risk pattern should be inspected before release.

## Core public-copy rule

The page may say:

```text
Die Karten zeigen räumliche Orientierung, Schnittmengen und Planungskontexte.
```

The page should not say:

```text
Die Karten zeigen geeignete Flächen, Prioritätsflächen oder Wiedervernässungspotenzial.
```

## Next step

If the audit status is OK, proceed to browser-responsive QA and final release review.

If `REVIEW REQUIRED`, inspect:

```powershell
Import-Csv docs\\B115_visible_copy_findings.csv -Delimiter ';' | Format-Table -Auto
```
"""


def audit_text(summary: dict[str, int], rows: list[dict[str, str]]) -> str:
    status = "OK" if summary["risk_reviews"] == 0 and summary["missing_required"] == 0 else "REVIEW REQUIRED"

    lines = [
        "# B115 visible copy audit",
        "",
        f"- Status: {status}",
        f"- Targeted replacements applied: {summary['replacements_changed']}",
        f"- Risk patterns remaining in visible text: {summary['risk_reviews']}",
        f"- Required safe/caveat patterns missing: {summary['missing_required']}",
        f"- Watch terms present: {summary['watch_terms']}",
        "",
        "## Risk or missing findings",
        "",
    ]

    flagged = [r for r in rows if r["status"] in {"REVIEW", "MISSING"}]
    if flagged:
        lines.append("| Type | Pattern | Count |")
        lines.append("|---|---|---:|")
        for r in flagged:
            lines.append(f"| {r['type']} | `{r['pattern']}` | {r['count_after']} |")
    else:
        lines.append("No risk or missing findings.")

    lines.extend([
        "",
        "## Watch terms",
        "",
        "Watch terms are not automatically errors. They indicate terms to inspect in context.",
        "",
        "```powershell",
        "Import-Csv docs\\B115_visible_copy_findings.csv -Delimiter ';' | Where-Object {$_.status -ne 'OK'} | Format-Table -Auto",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    original = read_text(INDEX)
    changed, rows = replacement_pass(original)

    # Write index only if needed.
    changed_files = []
    if changed != original:
        write_text(INDEX, changed)
        changed_files.append(rel(INDEX))

    visible = strip_to_visible_text(changed)
    add_audit_rows(changed, visible, rows)
    write_findings(rows)

    summary = summarize(rows)

    changed_files.extend([rel(REPORT), rel(AUDIT), rel(FINDINGS), rel(DONE)])
    write_text(REPORT, report_text(summary, changed_files))
    write_text(AUDIT, audit_text(summary, rows))
    update_done()

    print("B115 final visible copy pass complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, FINDINGS, DONE]:
        if p.exists():
            print(f"  {rel(p)}")
    print("")
    print(f"Risk patterns remaining: {summary['risk_reviews']}")
    print(f"Required safe patterns missing: {summary['missing_required']}")
    print(f"Watch terms present: {summary['watch_terms']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B115_visible_copy_audit.txt")
    print("  Import-Csv docs\\B115_visible_copy_findings.csv -Delimiter ';' | Where-Object {$_.status -ne 'OK'} | Format-Table -Auto")


if __name__ == "__main__":
    main()
