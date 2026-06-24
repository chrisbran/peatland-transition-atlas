#!/usr/bin/env python3
"""
B97g - Clean remaining visible public-copy red flags after B97f.

Context
-------
B97f fixed several public-readiness issues, but its scan still reported a mix of:
- genuinely visible English/prototype copy,
- hidden/retired prototype appendix content,
- and a JavaScript false positive (`Array.prototype`).

B97g performs a conservative second pass:
1. Clean only high-confidence visible copy red flags.
2. Do not touch hidden retired appendix sections.
3. Do not touch JavaScript (`Array.prototype`).
4. Generate a classified residual scan:
   - visible-review
   - hidden-retired
   - script-false-positive

Changed files
-------------
- index.html
- docs/B97g_clean_remaining_public_copy_red_flags.md
- docs/B97g_public_readiness_red_flag_scan_classified.txt
- tasks/done.md

Not changed
-----------
- src/styles.css
- JS logic
- PNG/GIS assets
- hidden retired prototype appendix content
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
REPORT = DOCS / "B97g_clean_remaining_public_copy_red_flags.md"
SCAN = DOCS / "B97g_public_readiness_red_flag_scan_classified.txt"

RED_FLAG_PATTERNS = [
    r"prototype",
    r"guided scrollytelling prototype",
    r"visual state",
    r"next implementation",
    r"planned for Phase B",
    r"Phase B",
    r"placeholder",
    r"TODO",
    r"FIXME",
    r"stub",
    r"Methodeische",
    r"Methodeneische",
    r"rewetting suitability map",
    r"From national emission hotspots",
    r"implementation will bind",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    if not INDEX.exists():
        print(f"B97g cannot run. Missing `{rel(INDEX)}`.")
        sys.exit(1)


def replace_literal(text: str, old: str, new: str) -> tuple[str, int]:
    count = text.count(old)
    return text.replace(old, new), count


def replace_regex(text: str, pattern: str, replacement: str, flags: int = re.IGNORECASE) -> tuple[str, int]:
    updated, count = re.subn(pattern, replacement, text, flags=flags)
    return updated, count


def apply_replacements(html: str) -> tuple[str, list[tuple[str, int]]]:
    text = html
    changes: list[tuple[str, int]] = []

    literal_replacements = [
        (
            "From national emission hotspots to real peatland landscapes",
            "Von Emissions-Hotspots zu realen Moorlandschaften",
        ),
        (
            "A peat/organic-soils map is not a rewetting suitability map",
            "Eine Moor-/organische-Böden-Karte ist keine Wiedervernässungs-Eignungskarte",
        ),
        (
            "Use the following modules as interpretation and prototype support for the main",
            "Die folgenden Module ordnen die Hauptkarte ein und ergänzen die Argumentation der Seite",
        ),
        (
            "to evidence-informed transition pathways. The matrix is not a prescription; it is a prototype logic for",
            "zu evidenzgestützten Transformationspfaden. Die Matrix ist keine Vorgabe; sie ist eine Arbeitslogik für",
        ),
        (
            "<strong>Prototype rule:</strong>",
            "<strong>Arbeitsregel:</strong>",
        ),
        (
            '<p class="eyebrow">Phase B hotspot layer</p>',
            '<p class="eyebrow">Optionale Hotspot-Vertiefung</p>',
        ),
        (
            "Prototype based on curated literature coding. Scores are qualitative and evidence-map points are approximate visual anchors.",
            "Arbeitsstand auf Basis kuratierter Literaturcodierung. Die Bewertungen sind qualitativ; Evidenzpunkte sind ungefähre visuelle Anker.",
        ),
    ]

    for old, new in literal_replacements:
        text, count = replace_literal(text, old, new)
        if count:
            changes.append((f"`{old}` -> `{new}`", count))

    # Safer partial regex for sentence continuations not fully captured by literal replacements.
    regex_replacements = [
        (
            r"\bUse the following modules as interpretation and prototype support\b",
            "Die folgenden Module ordnen die Hauptkarte ein und ergänzen die Argumentation",
            "cleaned visible prototype-support wording",
        ),
        (
            r"\bThe matrix is not a prescription; it is a prototype logic for\b",
            "Die Matrix ist keine Vorgabe; sie ist eine Arbeitslogik für",
            "cleaned visible prototype-logic wording",
        ),
    ]

    for pattern, repl, label in regex_replacements:
        text, count = replace_regex(text, pattern, repl)
        if count:
            changes.append((label, count))

    return text, changes


def classify_hit(line: str) -> str:
    low = line.lower()

    if "array.prototype" in low:
        return "script-false-positive"

    if (
        "hidden" in low
        or "aria-hidden" in low
        or "is-retired" in low
        or "data-retired" in low
        or "prototypeappendixintro" in low
        or "prototype appendix" in low
        or "current prototype datasets" in low
        or "how to read this prototype" in low
        or "literature-driven prototype" in low
        or "b71 prototype appendix" in low
    ):
        return "hidden-retired"

    return "visible-review"


def red_flag_scan(html: str) -> list[tuple[str, int, str, str, str]]:
    lines = html.splitlines()
    hits: list[tuple[str, int, str, str, str]] = []

    for i, line in enumerate(lines, start=1):
        for pattern in RED_FLAG_PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE):
                snippet = line.strip()
                if len(snippet) > 220:
                    snippet = snippet[:217] + "..."
                category = classify_hit(line)
                hits.append((category, i, pattern, snippet, line))
                break

    return hits


def write_scan(hits: list[tuple[str, int, str, str, str]]) -> None:
    DOCS.mkdir(exist_ok=True)

    counts = {
        "visible-review": 0,
        "hidden-retired": 0,
        "script-false-positive": 0,
    }
    for category, *_rest in hits:
        counts[category] = counts.get(category, 0) + 1

    parts = [
        "# B97g Public-Readiness Red-Flag Scan Classified",
        "",
        "Scope: `index.html`",
        "",
        "Hits are classified so public-facing issues can be separated from hidden retired appendix content and JavaScript false positives.",
        "",
        "## Counts",
        "",
        f"- visible-review: {counts.get('visible-review', 0)}",
        f"- hidden-retired: {counts.get('hidden-retired', 0)}",
        f"- script-false-positive: {counts.get('script-false-positive', 0)}",
        f"- total: {len(hits)}",
        "",
    ]

    for category in ["visible-review", "hidden-retired", "script-false-positive"]:
        parts.append(f"## {category}")
        parts.append("")
        subset = [h for h in hits if h[0] == category]
        if subset:
            for _category, line_no, pattern, snippet, _line in subset:
                parts.append(f"- L{line_no}: pattern `{pattern}` :: {snippet}")
        else:
            parts.append("- none")
        parts.append("")

    write_text(SCAN, "\n".join(parts))


def write_report(today: str, changes: list[tuple[str, int]], hits: list[tuple[str, int, str, str, str]]) -> None:
    DOCS.mkdir(exist_ok=True)

    if changes:
        change_lines = "\n".join(f"- {label}: {count}" for label, count in changes)
    else:
        change_lines = "- No targeted replacements were needed."

    visible_count = sum(1 for h in hits if h[0] == "visible-review")
    hidden_count = sum(1 for h in hits if h[0] == "hidden-retired")
    script_count = sum(1 for h in hits if h[0] == "script-false-positive")

    md = f"""# B97g - Clean Remaining Public Copy Red Flags

Date: {today}

## Result

B97g applied a conservative second editorial cleanup pass to `index.html`.

## Changed files

- `index.html`
- `docs/B97g_clean_remaining_public_copy_red_flags.md`
- `docs/B97g_public_readiness_red_flag_scan_classified.txt`
- `tasks/done.md`

## Replacements applied

{change_lines}

## Residual scan summary

- visible-review: {visible_count}
- hidden-retired: {hidden_count}
- script-false-positive: {script_count}
- scan file: `docs/B97g_public_readiness_red_flag_scan_classified.txt`

## Editorial decisions

- Removed remaining high-confidence visible English/prototype wording.
- Did not touch hidden retired prototype appendix sections.
- Did not touch JavaScript false positives such as `Array.prototype`.
- Did not move Transformationspfade. That remains planned for B99 after B98 quantitative QA.

## Next recommended steps

1. Inspect the classified scan.
2. If visible-review count is zero or acceptable, commit B97f/B97g.
3. Continue with B98: Oberschwaben intersection area and classification QA.
"""
    write_text(REPORT, md)


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B97g - Clean remaining public copy red flags"
    if marker in current:
        return

    entry = f"""
## B97g - Clean remaining public copy red flags ({today})

- Applied a second conservative editorial cleanup to visible public copy in `index.html`.
- Generated a classified residual red-flag scan distinguishing visible-review, hidden-retired and script false-positive hits.
- Left hidden retired prototype appendix sections untouched.
- Added `docs/B97g_clean_remaining_public_copy_red_flags.md`.
- Added `docs/B97g_public_readiness_red_flag_scan_classified.txt`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    original = read_text(INDEX)
    updated, changes = apply_replacements(original)
    write_text(INDEX, updated)

    hits = red_flag_scan(updated)
    write_scan(hits)
    write_report(today, changes, hits)
    update_done(today)

    print("B97g remaining public-copy red-flag cleanup complete.")
    print("Changed/created:")
    for path in [INDEX, REPORT, SCAN, DONE]:
        print(f"  {rel(path)}")

    print("\nReplacements applied:")
    if changes:
        for label, count in changes:
            print(f"  - {label}: {count}")
    else:
        print("  - none")

    visible_count = sum(1 for h in hits if h[0] == "visible-review")
    hidden_count = sum(1 for h in hits if h[0] == "hidden-retired")
    script_count = sum(1 for h in hits if h[0] == "script-false-positive")

    print("\nResidual scan:")
    print(f"  visible-review: {visible_count}")
    print(f"  hidden-retired: {hidden_count}")
    print(f"  script-false-positive: {script_count}")
    print("\nReview:")
    print(f"  Get-Content {rel(SCAN).replace('/', '\\\\')}")
    print("\nNext:")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
