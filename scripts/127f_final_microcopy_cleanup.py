#!/usr/bin/env python3
# B127f - Final microcopy cleanup
#
# Purpose:
# Remove the last visible "Lesart" wording and one remaining redundant
# "Werte gerundet." line after the Oberschwaben data-basis note.
#
# Changed:
# - index.html
# - docs/B127f_final_microcopy_cleanup.md
# - docs/B127f_final_microcopy_cleanup_audit.txt
# - tasks/done.md

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
BACKUP_DIR = ROOT / "_backup_before_b127f_final_microcopy_cleanup"

REPORT = DOCS / "B127f_final_microcopy_cleanup.md"
AUDIT = DOCS / "B127f_final_microcopy_cleanup_audit.txt"
TODAY = date.today().isoformat()

REQUIRED = [
    "Methodische Hinweise",
    "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet.",
]

RISK = [
    "Methodische Lesart",
    "Lesart",
    "Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;\neigene Auswahl, Klassifikation und Verschneidung.\nWerte gerundet.",
    "Werte gerundet.\nTransformationspfade",
    "Werte gerundet. Werte gerundet.",
    "Ã",
    "�",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup(path: Path) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / rel(path).replace("/", "__").replace("\\", "__")
    if path.exists() and not dest.exists():
        shutil.copy2(path, dest)


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def patch_index(html: str) -> tuple[str, dict[str, int]]:
    counters = {
        "methodische_lesart_replaced": 0,
        "standalone_werte_gerundet_removed": 0,
    }

    html, n = re.subn(r"Methodische\s+Lesart", "Methodische Hinweise", html)
    counters["methodische_lesart_replaced"] += n

    # Remove the redundant standalone "Werte gerundet." immediately after the
    # Oberschwaben FIONA/BK50/GISCO data-basis line. The earlier Hinweis line
    # already contains "Werte gerundet".
    pattern = (
        r"(Datenbasis:\s*FIONA 2024,\s*BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;\s*"
        r"eigene Auswahl,\s*Klassifikation und Verschneidung\.)\s*"
        r"(?:<br\s*/?>\s*)?"
        r"(?:<span[^>]*>\s*)?"
        r"Werte gerundet\."
        r"(?:\s*</span>)?"
    )
    html, n = re.subn(pattern, r"\1", html, flags=re.IGNORECASE | re.DOTALL)
    counters["standalone_werte_gerundet_removed"] += n

    # Conservative fallback for plain text line breaks if the first pattern did
    # not match due to slightly different formatting.
    html, n = re.subn(
        r"(eigene Auswahl,\s*Klassifikation und Verschneidung\.)\s*\n\s*Werte gerundet\.",
        r"\1",
        html,
        flags=re.IGNORECASE,
    )
    counters["standalone_werte_gerundet_removed"] += n

    return html, counters


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B127f - Final microcopy cleanup"
    if marker in current:
        return

    entry = f"""
## B127f - Final microcopy cleanup ({TODAY})

- Replaced `Methodische Lesart` with `Methodische Hinweise`.
- Removed the redundant standalone `Werte gerundet.` line after the Oberschwaben FIONA/BK50/GISCO data-basis note.
- Kept the earlier explicit note: `Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet.`
- Did not modify maps, CSS, data or scrolly logic.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(html: str, counters: dict[str, int]) -> dict[str, object]:
    visible = visible_text(html)
    return {
        "required_counts": {p: visible.count(p) for p in REQUIRED},
        "risk_counts": {p: visible.count(p) for p in RISK},
        "missing_required": sum(1 for p in REQUIRED if visible.count(p) == 0),
        "risk_findings": sum(1 for p in RISK if visible.count(p) > 0),
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = result["missing_required"] == 0 and result["risk_findings"] == 0
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B127f – Final Microcopy Cleanup",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B127f entfernt zwei letzte sichtbare redaktionelle Kleinigkeiten vor dem Commit.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B127f_final_microcopy_cleanup_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html -Pattern \"Methodische Hinweise\",\"Methodische Lesart\",\"Lesart\",\"Werte gerundet. Werte gerundet\",\"Werte gerundet.\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B127f final microcopy cleanup audit",
        "",
        f"- Status: {status}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['risk_findings']}",
        "",
        "## Counters",
        "",
        "| Counter | Count |",
        "|---|---:|",
    ]
    for k, v in result["counters"].items():
        audit_lines.append(f"| `{k}` | {v} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["required_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    backup(INDEX)

    html = read_text(INDEX)
    html, counters = patch_index(html)
    write_text(INDEX, html)

    update_done()

    result = audit(html, counters)
    write_docs(result)

    ok = result["missing_required"] == 0 and result["risk_findings"] == 0

    print("B127f final microcopy cleanup complete.")
    print("Changed/created:")
    for p in [INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['risk_findings']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B127f_final_microcopy_cleanup_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
