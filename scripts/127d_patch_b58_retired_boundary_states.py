#!/usr/bin/env python3
# B127d - Patch B58 for retired boundary states
#
# Context:
# B127/B127b intentionally removed boundary-only story states from index.html:
# - europe-borders
# - germany-context
# - bw-context
#
# B58 still treats these old story states as required/possible state keys and
# therefore reports "State not fully wired". This patch updates B58 so retired
# states are ignored in the state-wiring check. It does not change public page
# content, maps, scrolly logic or data.

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
B58 = ROOT / "scripts" / "58_visual_qa_and_commit_check.py"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b127d_patch_b58_retired_states"

REPORT = DOCS / "B127d_patch_b58_retired_boundary_states.md"
AUDIT = DOCS / "B127d_patch_b58_retired_boundary_states_audit.txt"
TODAY = date.today().isoformat()

RETIRED_STATES = ["europe-borders", "germany-context", "bw-context"]
CONSTANT_NAME = "B127_RETIRED_CENTRAL_STATES"
CONSTANT_BLOCK = """
# B127d: boundary-only story states removed from the public central map sequence.
B127_RETIRED_CENTRAL_STATES = {"europe-borders", "germany-context", "bw-context"}

"""


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


def insert_constant(text: str) -> tuple[str, int]:
    if CONSTANT_NAME in text:
        return text, 0

    import_matches = list(re.finditer(r"(?m)^(?:from\s+\S+\s+import\s+.*|import\s+.*)$", text))
    if import_matches:
        insert_at = import_matches[-1].end()
        return text[:insert_at] + "\n\n" + CONSTANT_BLOCK.strip() + "\n" + text[insert_at:], 1

    return CONSTANT_BLOCK + text, 1


def patch_state_loop(text: str) -> tuple[str, int, str]:
    if f"- {CONSTANT_NAME}" in text:
        return text, 0, "already_patched"

    needle = "State not fully wired"
    pos = text.find(needle)
    if pos < 0:
        return text, 0, "state_message_not_found"

    prefix = text[:pos]
    matches = list(re.finditer(r"(?m)^(\s*)for\s+state\s+in\s+sorted\((.*?)\):\s*$", prefix))
    if not matches:
        return text, 0, "for_state_loop_not_found"

    m = matches[-1]
    indent, expr = m.group(1), m.group(2).strip()

    if CONSTANT_NAME in expr:
        return text, 0, "loop_already_mentions_retired_states"

    new_line = f"{indent}for state in sorted(set({expr}) - {CONSTANT_NAME}):"
    text = text[:m.start()] + new_line + text[m.end():]
    return text, 1, "patched_state_wiring_loop"


def patch_known_expected_lists(text: str) -> tuple[str, int]:
    total = 0
    for state in RETIRED_STATES:
        patterns = [
            rf'(?m)^\s*"{re.escape(state)}",\s*\n',
            rf"(?m)^\s*'{re.escape(state)}',\s*\n",
        ]
        for pattern in patterns:
            text, n = re.subn(pattern, "", text)
            total += n
    return text, total


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B127d - Patch B58 retired boundary states"
    if marker in current:
        return

    entry = f"""
## B127d - Patch B58 retired boundary states ({TODAY})

- Updated B58 visual QA to ignore retired boundary-only central map states.
- Retired states: `europe-borders`, `germany-context`, `bw-context`.
- Keeps thematic states and layer names intact.
- Fixes expected `State not fully wired` failures after B127/B127b sequence tightening.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(text: str, counters: dict[str, object]) -> dict[str, object]:
    return {
        "constant_count": text.count(CONSTANT_NAME),
        "state_message_count": text.count("State not fully wired"),
        "loop_filter_count": text.count(f"- {CONSTANT_NAME}"),
        "retired_literal_counts": {state: text.count(state) for state in RETIRED_STATES},
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = result["constant_count"] >= 1 and result["loop_filter_count"] >= 1
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B127d – Patch B58 Retired Boundary States",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B127d aktualisiert die B58-QA nach der Straffung der zentralen Kartenfolge.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Constant count: {result['constant_count']}",
        f"- Loop filter count: {result['loop_filter_count']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B127d_patch_b58_retired_boundary_states_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path scripts\\58_visual_qa_and_commit_check.py -Pattern \"B127_RETIRED_CENTRAL_STATES\",\"State not fully wired\",\"europe-borders\",\"germany-context\",\"bw-context\"",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B127d patch B58 retired boundary states audit",
        "",
        f"- Status: {status}",
        f"- Constant count: {result['constant_count']}",
        f"- State message count: {result['state_message_count']}",
        f"- Loop filter count: {result['loop_filter_count']}",
        "",
        "## Counters",
        "",
        "| Counter | Value |",
        "|---|---:|",
    ]
    for k, v in result["counters"].items():
        audit_lines.append(f"| `{k}` | `{v}` |")

    audit_lines.extend(["", "## Retired literal counts in B58", "", "| State | Count |", "|---|---:|"])
    for state, count in result["retired_literal_counts"].items():
        audit_lines.append(f"| `{state}` | {count} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not B58.exists():
        print(f"Missing {rel(B58)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    backup(B58)

    text = read_text(B58)

    counters: dict[str, object] = {
        "inserted_constant": 0,
        "patched_loop": 0,
        "loop_status": "",
        "removed_expected_list_lines": 0,
    }

    text, n = insert_constant(text)
    counters["inserted_constant"] = n

    text, n, loop_status = patch_state_loop(text)
    counters["patched_loop"] = n
    counters["loop_status"] = loop_status

    text, n = patch_known_expected_lists(text)
    counters["removed_expected_list_lines"] = n

    write_text(B58, text)
    update_done()

    result = audit(text, counters)
    write_docs(result)

    ok = result["constant_count"] >= 1 and result["loop_filter_count"] >= 1

    print("B127d patched B58 retired boundary states.")
    print("Changed/created:")
    for p in [B58, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Loop status: {loop_status}")
    print(f"Constant count: {result['constant_count']}")
    print(f"Loop filter count: {result['loop_filter_count']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B127d_patch_b58_retired_boundary_states_audit.txt -Encoding UTF8")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
