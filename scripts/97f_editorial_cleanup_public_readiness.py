#!/usr/bin/env python3
"""
B97f - Editorial Cleanup / Public-Readiness Pass

Purpose
-------
Prepare the current German presentation page for external viewing by removing
or softening visible prototype/build language, fixing a prominent typo, and
making the Oberschwaben section labels more distinct.

This is intentionally conservative:
- It only performs targeted text replacements in index.html.
- It does not restructure the whole page.
- It does not move the Transformationspfade section yet. That belongs to B99,
  after B98 has checked the Oberschwaben intersection statistics.
- It creates a public-readiness report and a residual red-flag scan.

Main cleanup targets
--------------------
1. Fix "Methodeische Grenze" -> "Methodische Grenze".
2. Reduce German/English mixing in prominent visible labels.
3. Remove or neutralize visible prototype/build notes.
4. Distinguish the two Oberschwaben-related sections:
   - existing explanatory section: "Oberschwaben: regionale Ausgangslage"
   - scrolly layer section: "Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird"
5. Scan remaining visible-ish red flags for manual review.

Changed files
-------------
- index.html
- docs/B97f_editorial_cleanup_public_readiness.md
- docs/B97f_public_readiness_red_flag_scan.txt
- tasks/done.md

Not changed
-----------
- src/styles.css
- PNG/GIS assets
- JS logic
- raw data
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
REPORT = DOCS / "B97f_editorial_cleanup_public_readiness.md"
SCAN = DOCS / "B97f_public_readiness_red_flag_scan.txt"

# High-signal strings that should generally not appear in public-facing copy.
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
        print(f"B97f cannot run. Missing `{rel(INDEX)}`.")
        sys.exit(1)


def count_occurrences(text: str, pattern: str, flags: int = re.IGNORECASE) -> int:
    return len(re.findall(pattern, text, flags=flags))


def replace_literal(text: str, old: str, new: str) -> tuple[str, int]:
    count = text.count(old)
    return text.replace(old, new), count


def replace_regex(text: str, pattern: str, replacement: str, flags: int = re.IGNORECASE) -> tuple[str, int]:
    updated, count = re.subn(pattern, replacement, text, flags=flags)
    return updated, count


def apply_editorial_replacements(html: str) -> tuple[str, list[tuple[str, int]]]:
    changes: list[tuple[str, int]] = []
    text = html

    # 1. Hard typo fixes.
    literal_replacements = [
        ("Methodeische Grenze", "Methodische Grenze"),
        ("methodeische Grenze", "methodische Grenze"),
        ("Methodeneische Grenze", "Methodische Grenze"),

        # Prominent English/prototype labels. Keep meaning, remove prototype wording.
        ("Guided scrollytelling prototype", "Geführte Kartenstory"),
        ("Guided Scrollytelling Prototype", "Geführte Kartenstory"),
        ("Guided scrollytelling", "Geführte Kartenstory"),
        ("guided scrollytelling", "geführte Kartenstory"),

        ("From national emission hotspots to regional peatland transitions",
         "Von nationalen Emissions-Hotspots zu regionalen Moor-Transformationspfaden"),
        ("From national emission hotspots to regional peatland transitions.",
         "Von nationalen Emissions-Hotspots zu regionalen Moor-Transformationspfaden."),

        ("A peat map is not a rewetting suitability map",
         "Eine Moorkarte ist keine Wiedervernässungs-Eignungskarte"),
        ("A peat map is not a rewetting suitability map.",
         "Eine Moorkarte ist keine Wiedervernässungs-Eignungskarte."),

        # Prototype/build-note language -> public method/status language.
        ("Prototype visual state", "Methodischer Hinweis"),
        ("Prototype Visual State", "Methodischer Hinweis"),
        ("The next implementation will bind these states to real map layers.",
         "Diese Ansicht dient der räumlichen Einordnung und ersetzt keine Eignungs- oder Prioritätskarte."),
        ("The next implementation will bind these states to real map layers",
         "Diese Ansicht dient der räumlichen Einordnung und ersetzt keine Eignungs- oder Prioritätskarte"),
        ("Hotspot layers are planned for Phase B.",
         "Weitere räumliche Auswertungen werden nur nach gesonderter Datenprüfung ergänzt."),
        ("Hotspot layers are planned for Phase B",
         "Weitere räumliche Auswertungen werden nur nach gesonderter Datenprüfung ergänzt"),
    ]

    for old, new in literal_replacements:
        text, count = replace_literal(text, old, new)
        if count:
            changes.append((f"`{old}` -> `{new}`", count))

    # 2. Slightly safer regex cleanup for phase/build notes that occur with small wording variation.
    regex_replacements = [
        (
            r"\bThe next implementation will bind\b[^<.\n]*(?:\.|)",
            "Diese Ansicht dient der räumlichen Einordnung und ersetzt keine Eignungs- oder Prioritätskarte.",
            "neutralized next-implementation note",
        ),
        (
            r"\bHotspot layers\b[^<\n]*\bPhase B\b[^<.\n]*(?:\.|)",
            "Weitere räumliche Auswertungen werden nur nach gesonderter Datenprüfung ergänzt.",
            "neutralized Phase-B hotspot note",
        ),
        (
            r"\bplanned for Phase B\b",
            "für eine spätere geprüfte Ausbaustufe vorgesehen",
            "neutralized remaining Phase-B wording",
        ),
    ]

    for pattern, repl, label in regex_replacements:
        text, count = replace_regex(text, pattern, repl)
        if count:
            changes.append((label, count))

    # 3. Distinguish the pre-scrolly Oberschwaben explanatory heading from the scrolly title.
    # Do not change the B96 scrolly H2; change only the older explanatory title if present.
    heading_replacements = [
        (
            "Oberschwaben zeigt die praktische Herausforderung",
            "Oberschwaben: regionale Ausgangslage"
        ),
        (
            "Oberschwaben zeigt die praktische Herausforderung.",
            "Oberschwaben: regionale Ausgangslage."
        ),
    ]
    for old, new in heading_replacements:
        text, count = replace_literal(text, old, new)
        if count:
            changes.append((f"disambiguated Oberschwaben heading `{old}` -> `{new}`", count))

    # 4. Slight public-facing wording upgrade around implementation sections.
    text, count = replace_literal(
        text,
        "Regionale Umsetzung</p>\n    <h2 id=\"oberschwaben-layer-title\">Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird</h2>",
        "Regionale Umsetzung</p>\n    <h2 id=\"oberschwaben-layer-title\">Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird</h2>",
    )
    # This is intentionally a no-op placeholder for idempotent clarity; no report entry.

    return text, changes


def red_flag_scan(html: str) -> list[str]:
    lines = html.splitlines()
    hits: list[str] = []

    for i, line in enumerate(lines, start=1):
        low = line.lower()
        for pattern in RED_FLAG_PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE):
                # Avoid listing script filenames/docs references too aggressively? This scan is for manual review,
                # so keep line snippets.
                snippet = line.strip()
                if len(snippet) > 220:
                    snippet = snippet[:217] + "..."
                hits.append(f"L{i}: pattern `{pattern}` :: {snippet}")
                break

    return hits


def write_scan(hits: list[str]) -> None:
    DOCS.mkdir(exist_ok=True)
    if hits:
        body = "\n".join(f"- {h}" for h in hits)
    else:
        body = "- No red-flag strings found in index.html after B97f replacements."

    write_text(
        SCAN,
        "# B97f Public-Readiness Red-Flag Scan\n\n"
        "Scope: `index.html`\n\n"
        "This scan is intentionally conservative. Hits are not automatically failures; they are prompts for manual review.\n\n"
        "## Hits\n\n"
        f"{body}\n",
    )


def write_report(today: str, changes: list[tuple[str, int]], hits: list[str]) -> None:
    DOCS.mkdir(exist_ok=True)

    if changes:
        change_lines = "\n".join(f"- {label}: {count}" for label, count in changes)
    else:
        change_lines = "- No text replacements were needed."

    md = f"""# B97f - Editorial Cleanup / Public-Readiness

Date: {today}

## Result

B97f applied a conservative editorial cleanup to `index.html`.

## Changed files

- `index.html`
- `docs/B97f_editorial_cleanup_public_readiness.md`
- `docs/B97f_public_readiness_red_flag_scan.txt`
- `tasks/done.md`

## Replacements applied

{change_lines}

## Remaining red-flag scan

- Scan file: `docs/B97f_public_readiness_red_flag_scan.txt`
- Remaining hit count: {len(hits)}

Hits are not automatically failures. They indicate places worth checking manually before external sharing.

## Editorial decisions

- Fixed the prominent typo `Methodeische Grenze` where present.
- Reduced visible prototype/build language.
- Reduced prominent English/German mixing where exact known phrases were present.
- Distinguished the older Oberschwaben explanatory heading from the newer Oberschwaben scrolly map heading.
- Did not move Transformationspfade. That should be handled in B99 after B98 quantitative QA.

## Next recommended steps

1. Run visual QA.
2. Manually inspect remaining red-flag scan.
3. Continue with B98: Oberschwaben intersection area and classification QA.
"""
    write_text(REPORT, md)


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B97f - Editorial cleanup / public-readiness"
    if marker in current:
        return

    entry = f"""
## B97f - Editorial cleanup / public-readiness ({today})

- Applied targeted editorial cleanup to `index.html`.
- Fixed visible typo variants for `Methodische Grenze` if present.
- Neutralized visible prototype/build notes where exact patterns were found.
- Reduced selected German/English mixing in prominent page copy.
- Added `docs/B97f_editorial_cleanup_public_readiness.md`.
- Added `docs/B97f_public_readiness_red_flag_scan.txt`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    original = read_text(INDEX)
    updated, changes = apply_editorial_replacements(original)
    write_text(INDEX, updated)

    hits = red_flag_scan(updated)
    write_scan(hits)
    write_report(today, changes, hits)
    update_done(today)

    print("B97f editorial cleanup / public-readiness pass complete.")
    print("Changed/created:")
    for path in [INDEX, REPORT, SCAN, DONE]:
        print(f"  {rel(path)}")

    print("\nReplacements applied:")
    if changes:
        for label, count in changes:
            print(f"  - {label}: {count}")
    else:
        print("  - none")

    print(f"\nRemaining red-flag hits: {len(hits)}")
    print("Review:")
    print(f"  Get-Content {rel(SCAN).replace('/', '\\\\')}")
    print("\nNext:")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
