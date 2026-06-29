#!/usr/bin/env python3
# B127b - Remove BW boundary-only step
#
# Purpose:
# Make the BW transition consistent with Europe and Germany after B127:
# remove the boundary-only Baden-Württemberg step and use the thematic
# BW Moor-/Feuchtboden context map directly for the regional transition.
#
# Changed:
# - index.html
# - src/central_global_map_story.js
# - docs/B127b_remove_bw_boundary_only_step.md
# - docs/B127b_remove_bw_boundary_only_step_audit.txt
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
CENTRAL_JS = ROOT / "src" / "central_global_map_story.js"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b127b_remove_bw_boundary_only_step"

REPORT = DOCS / "B127b_remove_bw_boundary_only_step.md"
AUDIT = DOCS / "B127b_remove_bw_boundary_only_step_audit.txt"
TODAY = date.today().isoformat()

REMOVE_STATE = "bw-context"
RETAIN_STATE = "bw-bk50-extent"

NEW_TITLE = "Baden-Württemberg macht die Frage regional konkret."
NEW_BODY = "Hier wird sichtbar, wo Moor- und Feuchtbodenkontexte auf Nutzung, Zuständigkeiten und regionale Planung treffen."

REQUIRED = [
    f'data-global-state="{RETAIN_STATE}"',
    NEW_TITLE,
    NEW_BODY,
    "Datenbasis:",
    "Moorbodenschutz",
]

RISK = [
    f'data-global-state="{REMOVE_STATE}"',
    "Baden-Württemberg macht die Frage räumlich konkret.",
    "Auf regionaler Ebene zeigt sich",
    "Der Bodenkontext zeigt, wo Prüfung beginnt.",
    "Moor- und Feuchtbodenbereiche markieren Räume, in denen Wasserstand, Nutzung und Standortbedingungen gemeinsam bewertet werden müssen.",
    "BW frame:",
    "GLOBAL_FRAME_V1",
    "Thuenen",
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


def remove_article_step(html: str, state: str) -> tuple[str, int]:
    pattern = rf'\s*<article\b[^>]*\bdata-global-state="{re.escape(state)}"[^>]*>.*?</article>\s*'
    return re.subn(pattern, "\n", html, count=1, flags=re.DOTALL)


def replace_first_tag(block: str, tag: str, new_inner: str) -> tuple[str, int]:
    pattern = rf"<{tag}>(.*?)</{tag}>"
    repl = f"<{tag}>{new_inner}</{tag}>"
    return re.subn(pattern, repl, block, count=1, flags=re.DOTALL)


def retitle_article_step(html: str, state: str, title: str, body: str) -> tuple[str, int]:
    pattern = rf'(<article\b[^>]*\bdata-global-state="{re.escape(state)}"[^>]*>.*?</article>)'
    m = re.search(pattern, html, flags=re.DOTALL)
    if not m:
        return html, 0

    block = m.group(1)
    new_block, h3_hits = replace_first_tag(block, "h3", title)
    new_block, p_hits = replace_first_tag(new_block, "p", body)

    return html[:m.start()] + new_block + html[m.end():], h3_hits + p_hits


def retitle_js_state(js: str, state: str, title: str) -> tuple[str, int]:
    pattern = rf'("{re.escape(state)}":\s*\{{.*?title:\s*")[^"]*(")'
    return re.subn(pattern, rf'\1{title}\2', js, flags=re.DOTALL)


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B127b - Remove BW boundary-only step"
    if marker in current:
        return

    entry = f"""
## B127b - Remove BW boundary-only step ({TODAY})

- Removed the boundary-only Baden-Württemberg step from the central map sequence.
- Reused the thematic BW Moor-/Feuchtbodenkontext step as the regional transition.
- Kept the BW map image, layer mechanics and data unchanged.
- Made the BW sequence consistent with the tightened Europe and Germany transitions from B127.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(counters: dict[str, int]) -> dict[str, object]:
    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)
    visible = visible_text(html)
    raw = html + "\n" + js

    required_counts = {p: raw.count(p) for p in REQUIRED}
    visible_risk_counts = {p: visible.count(p) for p in RISK}
    raw_risk_counts = {p: raw.count(p) for p in RISK}

    return {
        "required_counts": required_counts,
        "visible_risk_counts": visible_risk_counts,
        "raw_risk_counts": raw_risk_counts,
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "visible_risk_findings": sum(1 for v in visible_risk_counts.values() if v > 0),
        "raw_risk_findings": sum(1 for v in raw_risk_counts.values() if v > 0),
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = result["missing_required"] == 0 and result["visible_risk_findings"] == 0
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B127b – Remove BW Boundary-only Step",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B127b entfernt auch den reinen Baden-Württemberg-Grenzschritt aus der zentralen Kartenfolge.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B127b_remove_bw_boundary_only_step_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\central_global_map_story.js -Pattern \"Baden-Württemberg macht die Frage regional konkret\",\"Hier wird sichtbar, wo Moor- und Feuchtbodenkontexte\",\"data-global-state=`\"bw-context`\"\",\"data-global-state=`\"bw-bk50-extent`\"\",\"Der Bodenkontext zeigt\",\"GLOBAL_FRAME_V1\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B127b remove BW boundary-only step audit",
        "",
        f"- Status: {status}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
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

    audit_lines.extend(["", "## Visible risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["visible_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Raw risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["raw_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    for path in [INDEX, CENTRAL_JS]:
        if not path.exists():
            print(f"Missing {rel(path)}")
            sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    backup(INDEX)
    backup(CENTRAL_JS)

    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)

    counters = {
        "removed_bw_boundary_step": 0,
        "retitled_html_step": 0,
        "retitled_js_state": 0,
    }

    html, n = remove_article_step(html, REMOVE_STATE)
    counters["removed_bw_boundary_step"] += n

    html, n = retitle_article_step(html, RETAIN_STATE, NEW_TITLE, NEW_BODY)
    counters["retitled_html_step"] += n

    js, n = retitle_js_state(js, RETAIN_STATE, NEW_TITLE)
    counters["retitled_js_state"] += n

    write_text(INDEX, html)
    write_text(CENTRAL_JS, js)
    update_done()

    result = audit(counters)
    write_docs(result)

    ok = result["missing_required"] == 0 and result["visible_risk_findings"] == 0

    print("B127b remove BW boundary-only step complete.")
    print("Changed/created:")
    for p in [INDEX, CENTRAL_JS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['visible_risk_findings']}")
    print(f"Raw risk findings: {result['raw_risk_findings']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B127b_remove_bw_boundary_only_step_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
