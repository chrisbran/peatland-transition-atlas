#!/usr/bin/env python3
"""
B64 - Cleanup story flow phase 1

Purpose
-------
Reversibly simplify the Peatland Transition Atlas page flow after the BW/BK50
central story integration.

What this patch does:
1. Re-routes the top "Story" navigation link to the main central map story.
2. Reversibly retires the older duplicate guidedStory section.
3. Reframes lower sections as supporting evidence / pathway interpretation.
4. Adds a small CSS utility for retired sections.
5. Writes a B64 documentation note and updates tasks/done.md.

What this patch deliberately does NOT do:
- It does not delete HTML sections.
- It does not remove scripts.
- It does not delete assets or public/data files.
- It does not alter the central map layer controller.
"""

from pathlib import Path
import re
from datetime import date

ROOT = Path.cwd()
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOC = ROOT / "docs" / "B64_cleanup_story_flow_phase1.md"
DONE = ROOT / "tasks" / "done.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def patch_index() -> list[str]:
    if not INDEX.exists():
        raise FileNotFoundError(INDEX)

    txt = read_text(INDEX)
    old = txt
    changes = []

    # 1. Make the main nav "Story" jump to the actual central atlas story.
    if 'href="#story">Story</a>' in txt:
        txt = txt.replace('href="#story">Story</a>', 'href="#centralGlobalMapStory">Story</a>', 1)
        changes.append("Rerouted top Story navigation to #centralGlobalMapStory")

    # 2. Retire the older duplicate guidedStory section reversibly.
    guided_re = re.compile(r'(<section\s+id=["\']guidedStory["\'][^>]*>)', flags=re.I)

    def retire_guided(match: re.Match) -> str:
        tag = match.group(1)
        patched = tag

        if "is-retired" not in patched:
            if re.search(r'class=["\'][^"\']*["\']', patched):
                patched = re.sub(
                    r'class=(["\'])([^"\']*)(["\'])',
                    lambda m: f'class={m.group(1)}{m.group(2)} is-retired{m.group(3)}',
                    patched,
                    count=1,
                )
            else:
                patched = patched[:-1] + ' class="is-retired">'

        if "aria-hidden" not in patched:
            patched = patched[:-1] + ' aria-hidden="true">'

        return patched

    new_txt, n = guided_re.subn(retire_guided, txt, count=1)
    if n:
        txt = new_txt
        changes.append("Retired #guidedStory reversibly with is-retired + aria-hidden")

        comment = "<!-- B64: guidedStory retired because centralGlobalMapStory is now the main narrative spine. Kept in markup for reversible rollback. -->\n"
        if "B64: guidedStory retired" not in txt:
            txt = re.sub(
                r'(<section\s+id=["\']guidedStory["\'])',
                comment + r'\1',
                txt,
                count=1,
                flags=re.I,
            )
    else:
        changes.append("WARNING: #guidedStory section not found")

    # 3. Reframe lower sections so they read as supporting evidence rather than a second main story.
    replacements = {
        "<h2>Where are drained organic soil emissions concentrated?</h2>":
            "<h2>Evidence explorer: where are drained organic soil emissions concentrated?</h2>",
        "<h2>Evidence from elsewhere</h2>":
            "<h2>Evidence explorer: cases and transition evidence</h2>",
        "<h2>Between drained farming and full restoration</h2>":
            "<h2>Transition pathways between drained farming and full restoration</h2>",
        "<h2>What fits South Germany?</h2>":
            "<h2>South Germany fit: which pathways remain plausible?</h2>",
    }

    for src, dst in replacements.items():
        if src in txt:
            txt = txt.replace(src, dst, 1)
            changes.append(f"Updated heading: {src}")
        elif dst in txt:
            pass
        else:
            changes.append(f"NOTE: heading not found: {src}")

    if txt != old:
        write_text(INDEX, txt)

    return changes


def patch_css() -> list[str]:
    if not CSS.exists():
        raise FileNotFoundError(CSS)

    txt = read_text(CSS)
    changes = []

    block = """
/* B64 reversible story-flow cleanup.
   Retired sections remain in index.html for rollback but are not displayed. */
.is-retired {
  display: none !important;
}

#centralGlobalMapStory {
  scroll-margin-top: 5rem;
}
""".strip() + "\n"

    if "B64 reversible story-flow cleanup" not in txt:
        txt = txt.rstrip() + "\n\n" + block
        write_text(CSS, txt)
        changes.append("Added B64 is-retired CSS utility and scroll-margin for central story")
    else:
        changes.append("B64 CSS block already present")

    return changes


def write_doc(changes: list[str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    body = f"""# B64 - Cleanup story flow phase 1

Date: {today}

## Purpose

This patch performs the first reversible story-flow cleanup after the BW/BK50
central story integration.

The central PNG-based sticky-scroll story is now treated as the main narrative
spine of the atlas. Older story components are not deleted, but the duplicate
guided scroll story is retired from display.

## Changes

""" + "\n".join(f"- {c}" for c in changes) + """

## Deliberate non-changes

- No public data files were deleted.
- No assets were deleted.
- No scripts were removed from `index.html`.
- The central map layer controller was not refactored.
- The B62 BW/BK50 state bindings were not changed.

## Rationale

The page previously contained two separate scroll narratives:

1. `guidedStory`, an older state-based story using `world-emissions`,
   `global-peat`, `europe`, `germany`, `bw` and `boundary`.
2. `centralGlobalMapStory`, the newer PNG-based 11-step map story from global
   peatland extent and emission pressure to Europe, Germany / Thuenen and
   Baden-Wuerttemberg / BK50.

The second component is now stronger and should carry the main story. The first
component is therefore hidden with `is-retired` but left in the markup for easy
rollback.

## QA

Run:

```powershell
python scripts\\58_visual_qa_and_commit_check.py
python -m http.server 8000
```

Then inspect:

```text
http://localhost:8000/?v=b64
```

Expected visual result:

- The page should no longer show the old guided story block.
- The main central PNG sticky-scroll story should remain functional.
- Hotspot, evidence, pathway, fit, methodology and data sections should remain
  visible below the main story.
"""
    write_text(DOC, body)


def update_done(changes: list[str]) -> None:
    DONE.parent.mkdir(parents=True, exist_ok=True)
    if DONE.exists():
        txt = read_text(DONE)
    else:
        txt = ""

    marker = "B64 - Cleanup story flow phase 1"
    if marker in txt:
        return

    entry = f"""
## {date.today().isoformat()} - {marker}

- Retired duplicate `guidedStory` section via reversible `is-retired` class.
- Rerouted top Story navigation to `#centralGlobalMapStory`.
- Reframed lower evidence/pathway headings as supporting sections.
- Added `docs/B64_cleanup_story_flow_phase1.md`.
- No data, assets or scripts were deleted.
"""
    write_text(DONE, txt.rstrip() + "\n\n" + entry.strip() + "\n")


def main() -> None:
    changes = []
    changes.extend(patch_index())
    changes.extend(patch_css())
    write_doc(changes)
    update_done(changes)

    print("B64 story-flow cleanup phase 1 complete.")
    print("Changed/created:")
    print("  index.html")
    print("  src/styles.css")
    print("  docs/B64_cleanup_story_flow_phase1.md")
    print("  tasks/done.md")
    print("")
    print("Run next:")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")
    print("Then open:")
    print("  http://localhost:8000/?v=b64")


if __name__ == "__main__":
    main()
