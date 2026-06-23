#!/usr/bin/env python3
"""
B85 - Restore persistent dark central map stage

Purpose:
- Red error is fixed after B84.
- Remaining issue: the dark map/stage background is visible only around step 01
  instead of staying present throughout the 01-11 central map sequence.
- Restore the central map stage as a persistent sticky dark visual field while
  the central story steps scroll.
- Keep all step cards consistently dark.
- Do not change map state names, JS logic, data, or map assets.

Outputs:
- docs/B85_restore_persistent_dark_central_map_stage.md
- modifies src/styles.css
- updates tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOC = DOCS / "B85_restore_persistent_dark_central_map_stage.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    css = read(CSS)

    b85_css = r"""
/* B85 restore persistent dark central map stage */

/*
  B84 fixed text panels, but the overall central map stage could visually collapse
  into a grey scroll field between steps. B85 restores the dark map stage as the
  persistent visual anchor throughout the centralGlobalMapStory section.
*/

#centralGlobalMapStory {
  position: relative !important;
  background:
    linear-gradient(
      180deg,
      rgba(245, 239, 230, 0.0) 0%,
      rgba(9, 18, 15, 0.38) 8%,
      rgba(9, 18, 15, 0.46) 50%,
      rgba(9, 18, 15, 0.38) 92%,
      rgba(245, 239, 230, 0.0) 100%
    ) !important;
  overflow: clip !important;
}

/* The actual map visual must stay as the dominant sticky object, not disappear
   into the background after the first step. */
#centralGlobalMapStory .central-map-visual,
#centralGlobalMapStory .central-map-stage,
#centralGlobalMapStory .central-map-frame,
#centralGlobalMapStory .central-map-stack,
#centralGlobalMapStory .map-frame {
  position: sticky !important;
  top: clamp(74px, 9vh, 116px) !important;
  z-index: 1 !important;
  background: #07120F !important;
  border: 1px solid rgba(245, 240, 231, 0.14) !important;
  border-radius: clamp(14px, 2vw, 28px) !important;
  box-shadow: 0 26px 90px rgba(0, 0, 0, 0.30) !important;
  overflow: hidden !important;
}

/* If the map images/layers are absolutely stacked, keep them inside the dark stage. */
#centralGlobalMapStory .central-map-visual img,
#centralGlobalMapStory .central-map-stage img,
#centralGlobalMapStory .central-map-frame img,
#centralGlobalMapStory .central-map-stack img,
#centralGlobalMapStory .map-frame img,
#centralGlobalMapStory img[class*="layer-"] {
  background: transparent !important;
}

/* All central step cards should float above the persistent map/stage. */
#centralGlobalMapStory article,
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory .central-story-step,
#centralGlobalMapStory .map-step,
#centralGlobalMapStory .step,
#centralGlobalMapStory [data-global-state] {
  position: relative;
  z-index: 5 !important;
  background: rgba(9, 18, 15, 0.88) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.16) !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.28) !important;
}

/* Prevent the broad article rule from turning non-step explanatory blocks into dark cards
   outside the step stream, where possible. */
#centralGlobalMapStory .section-heading,
#centralGlobalMapStory .section-heading *,
#centralGlobalMapStory .central-story-read-note {
  background: transparent !important;
  color: var(--b79-muted, #776A5D) !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Keep headings in intro area dark on warm paper, while step-card headings stay light. */
#centralGlobalMapStory .section-heading h2 {
  color: var(--b79-ink, #221D18) !important;
}

/* If the story uses a scroll column plus a sticky visual, force a sane two-column relation. */
#centralGlobalMapStory .central-map-layout,
#centralGlobalMapStory .central-map-grid,
#centralGlobalMapStory .central-story-grid,
#centralGlobalMapStory .central-map-scroll-layout {
  align-items: start !important;
}

/* If some steps are siblings after the map, keep enough vertical rhythm but not empty dead space. */
#centralGlobalMapStory article[data-global-state],
#centralGlobalMapStory .central-map-step {
  margin-bottom: clamp(46px, 10vh, 92px) !important;
}

/* Mobile: map does not need to be sticky on narrow screens. */
@media (max-width: 900px) {
  #centralGlobalMapStory {
    overflow: visible !important;
    background: rgba(9, 18, 15, 0.30) !important;
  }

  #centralGlobalMapStory .central-map-visual,
  #centralGlobalMapStory .central-map-stage,
  #centralGlobalMapStory .central-map-frame,
  #centralGlobalMapStory .central-map-stack,
  #centralGlobalMapStory .map-frame {
    position: relative !important;
    top: auto !important;
  }
}
/* End B85 restore persistent dark central map stage */
"""

    if "/* B85 restore persistent dark central map stage */" not in css:
        css = css.rstrip() + "\n\n" + b85_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B85 - Restore Persistent Dark Central Map Stage

Date: {today}

## 1. Issue

After B84:

- the red `textContent` error was fixed,
- but the dark map/stage background still appeared mainly around step 01,
- the middle of the central story could collapse visually into a grey scroll field with small floating cards.

## 2. Interpretation

The issue is visual/CSS-based, not data-based.

The central map visual needs to remain the persistent anchor throughout the 01-11 story sequence. B85 restores a sticky dark map stage and keeps all step cards above it.

## 3. Changes

B85 appends CSS only.

It:

- gives `#centralGlobalMapStory` a persistent dark gradient field,
- makes likely central map containers sticky again,
- gives map containers a dark stage background,
- keeps central step cards dark and above the map stage,
- avoids changing central map state names or JavaScript logic.

## 4. Files changed

- `src/styles.css`
- `docs/B85_restore_persistent_dark_central_map_stage.md`
- `tasks/done.md`

## 5. Manual QA

Check:

1. The red error bar remains gone.
2. The central map/story section no longer becomes a plain grey field between steps.
3. Steps 01-11 all have dark readable cards.
4. The map frame remains visible as the visual anchor through the central story.
5. Global, Europe, Germany and BW states still switch correctly.
"""
    write(DOC, doc)

    done_entry = f"""
## B85 - Restore persistent dark central map stage ({today})

- Restored a persistent dark central map stage via CSS.
- Kept all central step cards on a consistent dark readable panel treatment.
- Did not alter map state names, JavaScript logic, map assets or raw data.
- Created `docs/B85_restore_persistent_dark_central_map_stage.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B85 - Restore persistent dark central map stage" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B85 restore persistent dark central map stage complete.")
    print("Changed:")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
