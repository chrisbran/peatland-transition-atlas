#!/usr/bin/env python3
"""
B80 - Polish German presentation layout

Purpose:
- Refine B79 visual presentation after video review.
- Keep B79's German content and editorial-nature direction.
- Fix presentation issues without changing map state logic:
  - navigation should not behave like a bottom overlay,
  - hero claim cards should breathe better,
  - central map text panels should be more readable and less ghosted,
  - map stage should feel intentional and source-aware.
- Do not modify data, maps, or central JS state logic.

Outputs:
- docs/B80_polish_german_presentation_layout.md
- modifies src/styles.css
- updates tasks/done.md

Does NOT:
- modify index.html
- modify JavaScript
- change map state names
- alter map PNGs or raw data
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOC = DOCS / "B80_polish_german_presentation_layout.md"


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

    b80_css = r"""
/* B80 German presentation layout polish */

/* Keep the navigation calm and top-oriented; avoid bottom overlay behaviour from earlier prototypes. */
.site-header,
.header,
.navbar,
header[role="banner"] {
  position: sticky !important;
  top: 0 !important;
  bottom: auto !important;
  left: 0;
  right: 0;
  z-index: 1000 !important;
  min-height: 52px;
  box-shadow: none !important;
}

.site-header nav,
.header nav,
.navbar nav {
  margin-left: auto;
  align-items: center;
}

/* B79 presentation rhythm: stronger centred content column without feeling boxed. */
#problem.hero,
section.hero#problem,
.hero#problem {
  max-width: 1180px !important;
  padding-left: clamp(24px, 7vw, 96px) !important;
  padding-right: clamp(24px, 7vw, 96px) !important;
}

#problem .b79-claim-grid {
  max-width: 980px;
}

#problem .b79-claim-grid article {
  min-height: 150px;
}

/* Keep the warm editorial feeling, but reduce card heaviness. */
.b79-claim-grid article,
.b79-card-grid article {
  background: rgba(255, 252, 247, 0.76) !important;
  border-color: rgba(222, 212, 199, 0.92) !important;
  box-shadow: none !important;
}

/* Central map story: make text cards legible over the sticky map without grey ghost columns. */
#centralGlobalMapStory {
  isolation: isolate;
}

#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state] {
  background: rgba(255, 252, 247, 0.92) !important;
  border: 1px solid rgba(222, 212, 199, 0.96) !important;
  box-shadow: 0 12px 42px rgba(70, 50, 30, 0.10) !important;
  color: var(--b79-ink) !important;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* Remove old overlay artefacts if previous step styling used pseudo-elements. */
#centralGlobalMapStory .central-map-step::before,
#centralGlobalMapStory .central-map-step::after,
#centralGlobalMapStory article[data-global-state]::before,
#centralGlobalMapStory article[data-global-state]::after {
  background: transparent !important;
  box-shadow: none !important;
  border: 0 !important;
}

/* Step readability: no cramped paragraphs, no low-contrast grey on grey. */
#centralGlobalMapStory .central-map-step h3,
#centralGlobalMapStory article[data-global-state] h3 {
  color: #221D18 !important;
  line-height: 1.15;
  letter-spacing: -0.018em;
}

#centralGlobalMapStory .central-map-step p,
#centralGlobalMapStory article[data-global-state] p {
  color: #5F554B !important;
  line-height: 1.45;
}

/* Map stage: retain the dark PNG maps but place them deliberately on a warm page. */
#centralGlobalMapStory .central-map-visual,
#centralGlobalMapStory .central-map-stage,
#centralGlobalMapStory .central-map-frame,
#centralGlobalMapStory .map-frame,
#centralGlobalMapStory figure {
  border-color: rgba(222, 212, 199, 0.95) !important;
  box-shadow: 0 22px 84px rgba(70, 50, 30, 0.13) !important;
}

/* Captions and source text should be present but quiet. */
#centralGlobalMapStory figcaption,
#centralGlobalMapStory .source,
#centralGlobalMapStory .source-line,
#centralGlobalMapStory .map-source {
  color: #776A5D !important;
  font-size: 0.76rem !important;
  letter-spacing: 0.01em;
}

/* Section transition after the sticky map: make the new German lower path feel attached, not appended. */
#b79RegionalImplementation {
  border-top: 1px solid rgba(222, 212, 199, 0.85);
}

#b79MethodBoundary {
  max-width: 1180px;
}

/* Mobile safeguard. */
@media (max-width: 860px) {
  .site-header,
  .header,
  .navbar,
  header[role="banner"] {
    position: sticky !important;
    top: 0 !important;
    bottom: auto !important;
  }

  #problem .b79-claim-grid article {
    min-height: auto;
  }

  #centralGlobalMapStory .central-map-step,
  #centralGlobalMapStory article[data-global-state] {
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
/* End B80 German presentation layout polish */
"""

    if "/* B80 German presentation layout polish */" not in css:
        css = css.rstrip() + "\n\n" + b80_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B80 - Polish German Presentation Layout

Date: {today}

## 1. Purpose

B80 refines the B79 German presentation version after video review.

The B79 direction works: the page now reads as a German, editorial-nature presentation rather than a technical prototype. B80 keeps that direction and only polishes layout behaviour.

## 2. Observed issues

The video review showed:

1. The German content direction works.
2. The warm editorial design works better than the earlier dark prototype.
3. The navigation/brand behaviour can appear like a bottom overlay in the scroll recording.
4. Central map text panels are readable but still show some ghosted/grey overlay behaviour from older sticky-story styling.
5. The map section needs stronger source-aware polish without changing map logic.

## 3. B80 changes

B80 only appends CSS overrides.

It:

- keeps navigation top-oriented and calm,
- improves hero claim-card spacing,
- makes central map step panels more opaque and readable,
- suppresses old pseudo-element overlay artefacts,
- keeps dark map PNGs but frames them deliberately on the warm page,
- quiets source/caption typography,
- improves transition into the German lower sections.

## 4. Files changed

- `src/styles.css`
- `docs/B80_polish_german_presentation_layout.md`
- `tasks/done.md`

## 5. Files not changed

- `index.html`
- JavaScript
- map PNGs
- data
- central map state names

## 6. QA

After B80, check visually:

1. Header/navigation stays at top and no longer distracts at bottom.
2. Hero still resembles the preferred B76_B direction.
3. Central map story still scrolls correctly.
4. Step panels are readable and not washed out.
5. Map remains dominant.
6. German lower sections still appear after the map.
"""
    write(DOC, doc)

    done_entry = f"""
## B80 - Polish German presentation layout ({today})

- Polished B79 German presentation layout via CSS only.
- Kept B79 editorial-nature direction.
- Improved header behaviour, hero cards, central map step readability and map framing.
- Created `docs/B80_polish_german_presentation_layout.md`.
- Did not modify HTML, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B80 - Polish German presentation layout" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B80 German presentation layout polish complete.")
    print("Changed:")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
