#!/usr/bin/env python3
"""
B120 - Final public readiness cleanup

Small final text cleanup after B116-B119:
- remove/translate remaining public English structure labels;
- finalize Oberschwaben area-balance labels;
- ensure method note for Ackerland / Stilllegung / unclear FIONA assignment;
- harmonize older "Moore verstehen" wording with the B119 water-table/GHG mechanism;
- audit visible text for old prototype, English and overclaiming risks.

Changed:
- index.html
- docs/B120_final_public_readiness_cleanup.md
- docs/B120_final_public_readiness_audit.txt
- tasks/done.md

Not changed:
- src/styles.css
- public/maps/*
- data/*
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import html as html_lib
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b120_final_public_readiness_cleanup"

REPORT = DOCS / "B120_final_public_readiness_cleanup.md"
AUDIT = DOCS / "B120_final_public_readiness_audit.txt"

TODAY = date.today().isoformat()

METHOD_NOTE = "Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen. Werte gerundet."

REPLACEMENTS = [
    ("Scrollytelling structure", "Kartenfolge"),
    ("Six-part story", "Sechsteilige Kartenstory"),
    ("Six part story", "Sechsteilige Kartenstory"),
    ("six-part story", "sechsteilige Kartenstory"),

    ("~16 % Ackerland ohne Stilllegung und unklare Zuordnung", "~16 % Ackerland"),
    ("~2 % Stilllegung oder unklare Zuordnung separat geführt", "~2 % Stilllegung / unklare FIONA-Zuweisung"),
    ("Stilllegung oder unklare Zuordnung separat geführt", "Stilllegung / unklare FIONA-Zuweisung"),
    ("Ackerland ohne Stilllegung und unklare Zuordnung", "Ackerland"),

    (
        "Solange Torf nass bleibt, speichert er Kohlenstoff; wird er entwässert, wird er zur dauerhaften Emissionsquelle.",
        "Solange Torf nass bleibt, kann Kohlenstoff im Torf erhalten bleiben. Wird der Boden entwässert, gelangt Sauerstoff in den Torfkörper; Torf wird abgebaut und es entstehen Treibhausgasemissionen.",
    ),
    (
        "Torf mineralisiert und setzt Treibhausgase frei.",
        "Torf mineralisiert; dabei entstehen vor allem CO₂ sowie weitere klimawirksame Gase.",
    ),

    ("Welche Betriebe sind betroffen", "Welche Nutzungskontexte sind berührt"),
]

RISK_PATTERNS = [
    "This guided view",
    "Evidence explorer",
    "Prototype appendix",
    "Current prototype datasets",
    "Loading country hotspot map",
    "Click an evidence node",
    "Suitability would require",
    "Layer logic",
    "The map below is the core narrative",
    "The rest of the page is an evidence explorer",
    "Scrollytelling structure",
    "Six-part story",
    "Six part story",
    "GLOBAL_FRAME_V1",
    "source swap",
    "oberschwaben_lgl",
    "B98c",
    "Flächen-QA",
    "Klassifikations-QA",
    "Datenquelle in Umstellung",
    "berechnetes Treibhausgasminderungspotenzial",
    "THG-Minderungspotenzial der gezeigten Flächen",
    "Eignung für Wiedervernässung",
    "priorisierte Flächen",
    "müssen wiedervernässt werden",
    "Diese Flächen sollen wiedervernässt werden",
    "Welche Betriebe sind betroffen",
    "Ã",
    "�",
]

REQUIRED_PATTERNS = [
    "Moorschutz braucht räumliche Orientierung",
    "Warum Wasserstand über Klimawirkung entscheidet",
    "Diese Seite berechnet deshalb keine Treibhausgasminderung",
    "Warum Oberschwaben?",
    "Oberschwaben ist für Baden-Württemberg ein zentraler Fokusraum",
    "~19.900 ha",
    "~82 % Grünland",
    "~16 % Ackerland",
    "~2 % Stilllegung / unklare FIONA-Zuweisung",
    METHOD_NOTE,
    "FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024",
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine betriebliche Betroffenheitsanalyse",
    "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def apply_replacements(raw: str) -> tuple[str, list[tuple[str, int]]]:
    out = raw
    applied: list[tuple[str, int]] = []
    for old, new in REPLACEMENTS:
        n = out.count(old)
        if n:
            out = out.replace(old, new)
        applied.append((old, n))
    return out, applied


def ensure_method_note(raw: str) -> tuple[str, str]:
    if METHOD_NOTE in visible_text(raw):
        return raw, "already_present"

    pattern = re.compile(
        r"(?P<prefix>\s*)(?P<source><p[^>]*>\s*Datenbasis:\s*FIONA 2024,\s*BK50 Moor-/Feuchtbodenkontext\s*und\s*GISCO NUTS 2024;)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    m = pattern.search(raw)
    if not m:
        return raw, "source_line_not_found"

    note = f'\n{m.group("prefix")}<p class="moore-ob-method-note">{METHOD_NOTE}</p>\n'
    return raw[:m.start("source")] + note + raw[m.start("source"):], "inserted_before_fiona_source"


def audit(raw: str) -> dict[str, object]:
    vis = visible_text(raw)
    risk_counts = {p: vis.count(p) for p in RISK_PATTERNS}
    required_counts = {p: vis.count(p) for p in REQUIRED_PATTERNS}
    english_watch_patterns = ["structure", "story", "Loading", "Click", "prototype", "explorer", "layer:", "frame:"]
    english_watch_counts = {p: vis.count(p) for p in english_watch_patterns}
    return {
        "risk_counts": risk_counts,
        "required_counts": required_counts,
        "english_watch_counts": english_watch_counts,
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "english_watch": sum(english_watch_counts.values()),
    }


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B120 - Final public readiness cleanup"
    if marker in current:
        return
    entry = f"""
## B120 - Final public readiness cleanup ({TODAY})

- Removed/translated remaining public English structure labels.
- Finalized Oberschwaben area-balance labels and method note.
- Harmonized older "Moore verstehen" wording with the B119 water-table/GHG mechanism.
- Audited visible public text for prototype remnants, overclaims and encoding artefacts.
- Did not modify maps, CSS, map colours or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(applied: list[tuple[str, int]], method_status: str, result: dict[str, object]) -> None:
    risk_counts = result["risk_counts"]
    required_counts = result["required_counts"]
    english_watch_counts = result["english_watch_counts"]
    status = "OK" if result["risk_findings"] == 0 and result["missing_required"] == 0 else "REVIEW REQUIRED"

    lines = [
        "# B120 – Final Public Readiness Cleanup",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Zweck",
        "",
        "B120 ist ein kleiner finaler Text-Cleanup nach B116–B119. Es werden keine Karten, Farben oder Daten verändert.",
        "",
        "## Änderungen",
        "",
        "- verbliebene öffentliche englische Strukturbegriffe entfernt/übersetzt",
        "- Oberschwaben-Flächenbilanz final geglättet",
        "- methodische Notiz zu Ackerland/Stilllegung/unklarer FIONA-Zuweisung sichergestellt",
        "- älteren Moore-verstehen-Text an die B119-Logik angepasst",
        "",
        "## Replacement counts",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    any_applied = False
    for old, n in applied:
        if n:
            any_applied = True
            lines.append(f"| `{old.replace('|', '\\|')}` | {n} |")
    if not any_applied:
        lines.append("| none | 0 |")

    lines.extend([
        "",
        "## Method note",
        "",
        f"- Status: `{method_status}`",
        "",
        "## Audit summary",
        "",
        f"- Risk findings: {result['risk_findings']}",
        f"- Missing required findings: {result['missing_required']}",
        f"- English watch hits: {result['english_watch']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B120_final_public_readiness_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Scrollytelling structure\",\"Six-part story\",\"Evidence explorer\",\"Prototype appendix\",\"Warum Wasserstand\",\"Warum Oberschwaben\",\"~16 % Ackerland\",\"~2 % Stilllegung\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(lines))

    audit_lines = [
        "# B120 final public readiness audit",
        "",
        f"- Status: {status}",
        f"- Risk findings: {result['risk_findings']}",
        f"- Missing required findings: {result['missing_required']}",
        f"- English watch hits: {result['english_watch']}",
        "",
        "## Risk patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    for p, c in risk_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in required_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## English watch patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in english_watch_counts.items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend([
        "",
        "## Acceptable English/source terms",
        "",
        "- `Global Peatland Map`",
        "- `IPCC Wetlands Supplement`",
        "- `FAOSTAT`",
        "- `Sphagnum`",
        "",
    ])
    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    backup = BACKUP_DIR / "index_before_b120.html"
    if not backup.exists():
        shutil.copy2(INDEX, backup)

    html = read_text(INDEX)
    html, applied = apply_replacements(html)
    html, method_status = ensure_method_note(html)
    write_text(INDEX, html)

    update_done()
    result = audit(html)
    write_report(applied, method_status, result)

    print("B120 final public readiness cleanup complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(backup)}")
    print("")
    print(f"Status: {'OK' if result['risk_findings'] == 0 and result['missing_required'] == 0 else 'REVIEW REQUIRED'}")
    print(f"Risk findings: {result['risk_findings']}")
    print(f"Missing required findings: {result['missing_required']}")
    print(f"English watch hits: {result['english_watch']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B120_final_public_readiness_audit.txt -Encoding UTF8")
    print("  Select-String -Encoding UTF8 -Path index.html -Pattern \"Scrollytelling structure\",\"Six-part story\",\"Evidence explorer\",\"Prototype appendix\",\"Warum Wasserstand\",\"Warum Oberschwaben\",\"~16 % Ackerland\",\"~2 % Stilllegung\",\"Ã\",\"�\"")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
