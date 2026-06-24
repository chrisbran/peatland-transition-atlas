#!/usr/bin/env python3
"""
B97d - Keep Oberschwaben text-card transparency stable during scrolling.

Observed after B97c
-------------------
The Oberschwaben section layout now works, but the story text cards still change
their opacity/background transparency when the active scroll step changes. This
creates a distracting fade effect.

B97d keeps:
- B96 HTML and JS
- B97b light stage
- B97c legend placement and z-index fix
- B95h PNG assets

B97d changes:
- Adds a small CSS override block.
- Forces all Oberschwaben text cards to keep the same opacity and background.
- Removes opacity/transform/background transitions from the step cards.
- Keeps active state available for accessibility/logic, but not as a transparency fade.

Changed files:
- src/styles.css
- docs/B97d_stabilize_oberschwaben_step_card_opacity.md
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
REPORT = DOCS / "B97d_stabilize_oberschwaben_step_card_opacity.md"

B96_CSS_START = "/* B96_OBERSCHWABEN_SCROLLY_START */"
B96_CSS_END = "/* B96_OBERSCHWABEN_SCROLLY_END */"

OVERRIDE_START = "/* B97D_OBERSCHWABEN_STABLE_STEP_OPACITY_START */"
OVERRIDE_END = "/* B97D_OBERSCHWABEN_STABLE_STEP_OPACITY_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    if not CSS.exists():
        print(f"B97d cannot run. Missing `{rel(CSS)}`.")
        sys.exit(1)

    css = read_text(CSS)
    if B96_CSS_START not in css or B96_CSS_END not in css:
        print("B97d cannot run. The Oberschwaben B96/B97 CSS block is missing from src/styles.css.")
        print("Run B96/B97b/B97c first.")
        sys.exit(1)


def build_override_block() -> str:
    return f"""{OVERRIDE_START}
/*
  B97d stable card opacity:
  Keep all Oberschwaben story cards visually stable while scrolling.
  The active scroll state still controls the map layers, but no longer changes
  the transparency of the text cards.
*/

.moore-ob-step,
.moore-ob-step.is-active,
.moore-ob-step--boundary,
.moore-ob-step--boundary.is-active {{
  opacity: 1 !important;
  transform: none !important;
  background: rgba(255, 252, 244, 0.94) !important;
  border-color: rgba(48, 58, 51, 0.20) !important;
}}

.moore-ob-step {{
  transition: border-color 220ms ease, box-shadow 220ms ease !important;
}}

.moore-ob-step.is-active {{
  box-shadow: 0 1.1rem 2.6rem rgba(36, 45, 39, 0.12) !important;
}}

.moore-ob-step:not(.is-active) {{
  box-shadow: 0 0.65rem 1.6rem rgba(36, 45, 39, 0.08) !important;
}}

.moore-ob-step--boundary,
.moore-ob-step--boundary.is-active {{
  background: rgba(241, 248, 244, 0.94) !important;
  border-color: rgba(43, 103, 93, 0.28) !important;
}}

.moore-ob-step-label,
.moore-ob-step.is-active .moore-ob-step-label {{
  color: rgba(56, 70, 61, 0.56) !important;
}}

.moore-ob-step p:not(.moore-ob-step-label),
.moore-ob-step.is-active p:not(.moore-ob-step-label) {{
  color: rgba(44, 55, 49, 0.72) !important;
}}

.moore-ob-step h3,
.moore-ob-step.is-active h3 {{
  color: #1d241f !important;
}}
{OVERRIDE_END}"""


def replace_or_append_override(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(OVERRIDE_START) + r".*?" + re.escape(OVERRIDE_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B97d override block"

    # Prefer inserting after B97c if it exists; otherwise after Oberschwaben main block.
    b97c_end = "/* B97C_OBERSCHWABEN_READABILITY_FIX_END */"
    pos = css.find(b97c_end)
    if pos != -1:
        pos += len(b97c_end)
        return css[:pos].rstrip() + "\n\n" + block + "\n" + css[pos:].lstrip(), "inserted B97d override after B97c block"

    pos = css.find(B96_CSS_END)
    if pos != -1:
        pos += len(B96_CSS_END)
        return css[:pos].rstrip() + "\n\n" + block + "\n" + css[pos:].lstrip(), "inserted B97d override after Oberschwaben CSS block"

    return css.rstrip() + "\n\n" + block + "\n", "appended B97d override block"


def write_report(today: str, action: str) -> None:
    DOCS.mkdir(exist_ok=True)
    md = f"""# B97d - Stabilize Oberschwaben Step Card Opacity

Date: {today}

## Result

B97d added a small CSS override to keep Oberschwaben story-card transparency
stable during scrolling.

## Changed files

- `src/styles.css`
- `docs/B97d_stabilize_oberschwaben_step_card_opacity.md`
- `tasks/done.md`

## Action

- {action}

## Visual fix

The active scroll step still controls the visible Oberschwaben map layer state,
but it no longer changes the transparency/background of the text cards.

## Not changed

- `index.html`
- B96 JavaScript
- PNG layer assets
- GIS/raw data

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
    marker = "## B97d - Stabilize Oberschwaben step card opacity"
    if marker in current:
        return

    entry = f"""
## B97d - Stabilize Oberschwaben step card opacity ({today})

- Added a CSS override block to keep Oberschwaben text-card opacity/background stable while scrolling.
- Preserved B96 HTML/JS, B97b light-stage treatment and B97c legend/z-index fixes.
- Added `docs/B97d_stabilize_oberschwaben_step_card_opacity.md`.
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

    print("B97d Oberschwaben step-card opacity stabilization complete.")
    print("Changed/created:")
    for path in [CSS, REPORT, DONE]:
        print(f"  {rel(path)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  inspect locally in browser")


if __name__ == "__main__":
    main()
