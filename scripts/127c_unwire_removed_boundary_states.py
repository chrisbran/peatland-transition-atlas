#!/usr/bin/env python3
# B127c - Unwire removed boundary states from scripts
#
# Purpose:
# B127/B127b removed boundary-only scrolly steps from index.html. B58 now fails
# because the retired states still exist in the central JS controller. This patch
# removes those retired state objects from the script side as well.
#
# Removed states:
# - europe-borders
# - germany-context
# - bw-context

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
BACKUP_DIR = ROOT / "_backup_before_b127c_unwire_removed_boundary_states"

REPORT = DOCS / "B127c_unwire_removed_boundary_states.md"
AUDIT = DOCS / "B127c_unwire_removed_boundary_states_audit.txt"
TODAY = date.today().isoformat()

REMOVED_STATES = ["europe-borders", "germany-context", "bw-context"]
RETAINED_STATES = ["europe-peat", "germany-thuenen-extent", "bw-bk50-extent"]

REQUIRED = [
    'data-global-state="europe-peat"',
    'data-global-state="germany-thuenen-extent"',
    'data-global-state="bw-bk50-extent"',
    '"europe-peat"',
    '"germany-thuenen-extent"',
    '"bw-bk50-extent"',
]

RISK = [
    'data-global-state="europe-borders"',
    'data-global-state="germany-context"',
    'data-global-state="bw-context"',
    '"europe-borders"',
    '"germany-context"',
    '"bw-context"',
    "GLOBAL_FRAME_V1",
    "EUROPE_FRAME_V1",
    "BW frame:",
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
    return re.subn(pattern, "\n", html, flags=re.DOTALL)


def find_matching_brace(text: str, open_pos: int) -> int:
    depth = 0
    quote = None
    escaped = False
    i = open_pos

    while i < len(text):
        ch = text[i]

        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue

        if ch in ("'", '"', "`"):
            quote = ch
            i += 1
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i

        i += 1

    return -1


def remove_js_state_object(js: str, state: str) -> tuple[str, int]:
    removed = 0

    while True:
        key = f'"{state}"'
        key_pos = js.find(key)
        if key_pos < 0:
            break

        colon = js.find(":", key_pos + len(key))
        if colon < 0:
            break

        open_brace = js.find("{", colon)
        if open_brace < 0:
            break

        close_brace = find_matching_brace(js, open_brace)
        if close_brace < 0:
            break

        # Remove from line start to after optional trailing comma and following newline.
        start = js.rfind("\n", 0, key_pos) + 1
        end = close_brace + 1

        # Include trailing comma and following whitespace/newline if present.
        j = end
        while j < len(js) and js[j] in " \t":
            j += 1
        if j < len(js) and js[j] == ",":
            j += 1
            if j < len(js) and js[j] == "\r":
                j += 1
            if j < len(js) and js[j] == "\n":
                j += 1
            end = j
        else:
            # If it was the last object entry, remove a preceding comma if possible.
            prev = start - 1
            while prev >= 0 and js[prev] in " \t\r\n":
                prev -= 1
            if prev >= 0 and js[prev] == ",":
                start = prev

        js = js[:start] + js[end:]
        removed += 1

    return js, removed


def remove_loose_state_mentions(js: str, state: str) -> tuple[str, int]:
    # Clean any orphan array/string mentions of the removed state.
    total = 0
    patterns = [
        rf'\s*"{re.escape(state)}",?\s*\n',
        rf',\s*"{re.escape(state)}"',
        rf'"{re.escape(state)}"\s*,',
        rf'"{re.escape(state)}"',
    ]
    for pattern in patterns:
        js, n = re.subn(pattern, "\n", js)
        total += n
    return js, total


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B127c - Unwire removed boundary states"
    if marker in current:
        return

    entry = f"""
## B127c - Unwire removed boundary states ({TODAY})

- Removed retired boundary-only states from the central map controller.
- Cleaned script-side state wiring for `europe-borders`, `germany-context` and `bw-context`.
- Kept thematic Europe, Germany and Baden-Württemberg states.
- Fixes B58 `State not fully wired` failures after sequence tightening.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(counters: dict[str, int]) -> dict[str, object]:
    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)
    raw = html + "\n" + js
    visible = visible_text(html)

    required_counts = {p: raw.count(p) for p in REQUIRED}
    risk_counts = {p: raw.count(p) for p in RISK}
    visible_risk_counts = {p: visible.count(p) for p in RISK}

    return {
        "required_counts": required_counts,
        "risk_counts": risk_counts,
        "visible_risk_counts": visible_risk_counts,
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "visible_risk_findings": sum(1 for v in visible_risk_counts.values() if v > 0),
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = result["missing_required"] == 0 and result["risk_findings"] == 0
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B127c – Unwire Removed Boundary States",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B127c entfernt nach der Straffung der Kartenfolge die nicht mehr sichtbaren Grenz-States auch aus dem zentralen JS-Controller.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Missing required entries: {result['missing_required']}",
        f"- Raw risk findings: {result['risk_findings']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B127c_unwire_removed_boundary_states_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\central_global_map_story.js -Pattern \"europe-borders\",\"germany-context\",\"bw-context\",\"europe-peat\",\"germany-thuenen-extent\",\"bw-bk50-extent\",\"GLOBAL_FRAME_V1\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B127c unwire removed boundary states audit",
        "",
        f"- Status: {status}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Raw risk findings: {result['risk_findings']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
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

    audit_lines.extend(["", "## Raw risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Visible risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["visible_risk_counts"].items():
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
        "removed_index_articles": 0,
        "removed_js_state_objects": 0,
        "removed_loose_js_mentions": 0,
    }

    for state in REMOVED_STATES:
        html, n = remove_article_step(html, state)
        counters["removed_index_articles"] += n

        js, n = remove_js_state_object(js, state)
        counters["removed_js_state_objects"] += n

        js, n = remove_loose_state_mentions(js, state)
        counters["removed_loose_js_mentions"] += n

    write_text(INDEX, html)
    write_text(CENTRAL_JS, js)
    update_done()

    result = audit(counters)
    write_docs(result)

    ok = result["missing_required"] == 0 and result["risk_findings"] == 0

    print("B127c unwire removed boundary states complete.")
    print("Changed/created:")
    for p in [INDEX, CENTRAL_JS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Raw risk findings: {result['risk_findings']}")
    print(f"Visible risk findings: {result['visible_risk_findings']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B127c_unwire_removed_boundary_states_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
