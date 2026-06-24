#!/usr/bin/env python3
"""
B97c - Fix Oberschwaben step-card layering and legend overlay.

Observed after B97b
-------------------
The Oberschwaben stage size and light treatment are now much better, but:
1. The scroll text cards can visually slip behind the large sticky map card.
2. The light legend background sits on top of the map and obscures map details.

B97c keeps:
- B96 HTML and JS
- B97/B97b large stage size
- B97b lighter editorial treatment
- B95h PNG assets

B97c changes:
- Adds a small CSS override block, instead of replacing the whole B96/B97/B97b block.
- Raises the scroll step cards above the map stage with explicit z-index.
- Gives the text column more breathing room on desktop.
- Moves the legend out of the map overlay flow by making it static below the map.
- Removes the legend background, border, blur and shadow.

Changed files:
- src/styles.css
- docs/B97c_oberschwaben_readability_and_legend_fix.md
- tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
REPORT = DOCS / "B97c_oberschwaben_readability_and_legend_fix.md"

B96_CSS_START = "/* B96_OBERSCHWABEN_SCROLLY_START */"
B96_CSS_END = "/* B96_OBERSCHWABEN_SCROLLY_END */"

OVERRIDE_START = "/* B97C_OBERSCHWABEN_READABILITY_FIX_START */"
OVERRIDE_END = "/* B97C_OBERSCHWABEN_READABILITY_FIX_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    if not CSS.exists():
        print(f"B97c cannot run. Missing `{rel(CSS)}`.")
        sys.exit(1)

    css = read_text(CSS)
    if B96_CSS_START not in css or B96_CSS_END not in css:
        print("B97c cannot run. The Oberschwaben B96/B97 CSS block is missing from src/styles.css.")
        print("Run B96/B97b first.")
        sys.exit(1)


def build_override_block() -> str:
    return f"""{OVERRIDE_START}
/*
  B97c readability fix:
  - Step cards must sit above the large sticky map stage.
  - The legend should not cover map detail; it is moved below the stage and
    rendered without a white overlay background.
*/

.moore-ob-stage-column {{
  z-index: 1;
}}

.moore-ob-steps {{
  position: relative;
  z-index: 8;
}}

.moore-ob-step {{
  position: relative;
  z-index: 8;
}}

.moore-ob-step.is-active {{
  z-index: 9;
}}

.moore-ob-legend {{
  position: static !important;
  left: auto !important;
  right: auto !important;
  bottom: auto !important;
  margin: 0.78rem 0 0 !important;
  padding: 0 !important;
  width: auto !important;
  background: transparent !important;
  border: 0 !important;
  backdrop-filter: none !important;
  box-shadow: none !important;
  color: rgba(35, 43, 38, 0.72) !important;
}}

.moore-ob-legend-item {{
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.62);
}}

.moore-ob-swatch {{
  width: 0.66rem;
  height: 0.66rem;
  border-color: rgba(35, 43, 38, 0.22);
  box-shadow: none;
}}

@media (min-width: 1101px) {{
  .moore-ob-grid {{
    grid-template-columns: minmax(700px, 1.78fr) minmax(360px, 0.78fr);
    gap: clamp(2rem, 4vw, 4.75rem);
  }}

  .moore-ob-steps {{
    padding-top: clamp(3.5rem, 7vh, 6.5rem);
  }}

  .moore-ob-step {{
    margin-left: 0;
    background: rgba(255, 252, 244, 0.94);
  }}

  .moore-ob-step.is-active {{
    background: rgba(255, 252, 244, 0.98);
  }}
}}

@media (max-width: 1100px) {{
  .moore-ob-steps {{
    z-index: 4;
  }}
}}
{OVERRIDE_END}"""


def replace_or_append_override(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(OVERRIDE_START) + r".*?" + re.escape(OVERRIDE_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B97c override block"

    # Prefer inserting directly after the B96/B97 block, so future review is easy.
    pos = css.find(B96_CSS_END)
    if pos != -1:
        pos += len(B96_CSS_END)
        return css[:pos].rstrip() + "\n\n" + block + "\n" + css[pos:].lstrip(), "inserted B97c override after Oberschwaben CSS block"

    return css.rstrip() + "\n\n" + block + "\n", "appended B97c override block"


def write_report(today: str, action: str) -> None:
    DOCS.mkdir(exist_ok=True)
    md = f"""# B97c - Oberschwaben Readability and Legend Fix

Date: {today}

## Result

B97c added a small CSS override block to improve the B97b Oberschwaben section.

## Changed files

- `src/styles.css`
- `docs/B97c_oberschwaben_readability_and_legend_fix.md`
- `tasks/done.md`

## Action

- {action}

## Visual fixes

- Scroll text cards receive explicit z-index so they do not disappear behind the large sticky map stage.
- Desktop grid spacing is widened slightly to give the text column more breathing room.
- Legend is moved below the map stage rather than overlaid on top of map details.
- Legend background, border, blur and shadow are removed.
- B96 layer-state logic remains unchanged.

## QA recommendation

Run:

```powershell
python scripts\\95h_validate_oberschwaben_layer_stack.py
python scripts\\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section locally.
"""
    write_text(REPORT, md)


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B97c - Oberschwaben readability and legend fix"
    if marker in current:
        return

    entry = f"""
## B97c - Oberschwaben readability and legend fix ({today})

- Added a CSS override block so Oberschwaben scroll text cards render above the large sticky map stage.
- Removed the legend's white overlay background and placed the legend below the map.
- Preserved B96 HTML/JS and B97b light-stage treatment.
- Added `docs/B97c_oberschwaben_readability_and_legend_fix.md`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    css = read_text(CSS)
    updated, action = replace_or_append_override(css, build_override_block())
    write_text(CSS, updated)

    write_report(today, action)
    update_done(today)

    print("B97c Oberschwaben readability and legend fix complete.")
    print("Changed/created:")
    for path in [CSS, REPORT, DONE]:
        print(f"  {rel(path)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  inspect locally in browser")


if __name__ == "__main__":
    main()
