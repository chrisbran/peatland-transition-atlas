#!/usr/bin/env python3
"""
B97e - Restore stable semi-transparent Oberschwaben text cards.

Context
-------
B97d correctly stopped the scroll-state fade, but it made all text cards too
opaque. The intended behavior is:

- text cards remain semi-transparent,
- transparency is stable while scrolling,
- the map can be seen through/around the cards,
- text remains readable,
- active/inactive state does not change card transparency.

B97e therefore overrides B97d with stable translucent card backgrounds.

Changed files:
- src/styles.css
- docs/B97e_restore_oberschwaben_translucent_step_cards.md
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
REPORT = DOCS / "B97e_restore_oberschwaben_translucent_step_cards.md"

B96_CSS_START = "/* B96_OBERSCHWABEN_SCROLLY_START */"
B96_CSS_END = "/* B96_OBERSCHWABEN_SCROLLY_END */"

B97D_END = "/* B97D_OBERSCHWABEN_STABLE_STEP_OPACITY_END */"

OVERRIDE_START = "/* B97E_OBERSCHWABEN_TRANSLUCENT_STEP_CARDS_START */"
OVERRIDE_END = "/* B97E_OBERSCHWABEN_TRANSLUCENT_STEP_CARDS_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    if not CSS.exists():
        print(f"B97e cannot run. Missing `{rel(CSS)}`.")
        sys.exit(1)

    css = read_text(CSS)
    if B96_CSS_START not in css or B96_CSS_END not in css:
        print("B97e cannot run. The Oberschwaben B96/B97 CSS block is missing from src/styles.css.")
        print("Run B96/B97b/B97c/B97d first.")
        sys.exit(1)


def build_override_block() -> str:
    return f"""{OVERRIDE_START}
/*
  B97e translucent card correction:
  B97d stabilized step-card opacity but made cards too opaque. This override
  keeps card transparency stable while restoring translucent backgrounds.
  Important: use background alpha, not element opacity, so text stays readable.
*/

.moore-ob-step,
.moore-ob-step.is-active {{
  opacity: 1 !important;
  transform: none !important;
  background: rgba(255, 252, 244, 0.72) !important;
  border-color: rgba(48, 58, 51, 0.18) !important;
  backdrop-filter: blur(5px) saturate(1.02) !important;
  -webkit-backdrop-filter: blur(5px) saturate(1.02) !important;
}}

.moore-ob-step--boundary,
.moore-ob-step--boundary.is-active {{
  opacity: 1 !important;
  transform: none !important;
  background: rgba(241, 248, 244, 0.72) !important;
  border-color: rgba(43, 103, 93, 0.28) !important;
}}

.moore-ob-step.is-active {{
  box-shadow: 0 1.1rem 2.6rem rgba(36, 45, 39, 0.11) !important;
}}

.moore-ob-step:not(.is-active) {{
  box-shadow: 0 0.7rem 1.8rem rgba(36, 45, 39, 0.08) !important;
}}

.moore-ob-step {{
  transition: border-color 220ms ease, box-shadow 220ms ease !important;
}}

.moore-ob-step h3,
.moore-ob-step.is-active h3 {{
  color: rgba(29, 36, 31, 0.94) !important;
}}

.moore-ob-step p:not(.moore-ob-step-label),
.moore-ob-step.is-active p:not(.moore-ob-step-label) {{
  color: rgba(44, 55, 49, 0.78) !important;
}}

.moore-ob-step-label,
.moore-ob-step.is-active .moore-ob-step-label {{
  color: rgba(56, 70, 61, 0.62) !important;
}}

@media (min-width: 1101px) {{
  .moore-ob-step,
  .moore-ob-step.is-active {{
    background: rgba(255, 252, 244, 0.68) !important;
  }}

  .moore-ob-step--boundary,
  .moore-ob-step--boundary.is-active {{
    background: rgba(241, 248, 244, 0.70) !important;
  }}
}}

@media (max-width: 760px) {{
  .moore-ob-step,
  .moore-ob-step.is-active {{
    background: rgba(255, 252, 244, 0.84) !important;
  }}

  .moore-ob-step--boundary,
  .moore-ob-step--boundary.is-active {{
    background: rgba(241, 248, 244, 0.86) !important;
  }}
}}
{OVERRIDE_END}"""


def replace_or_append_override(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(OVERRIDE_START) + r".*?" + re.escape(OVERRIDE_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B97e override block"

    # Prefer inserting after B97d, because this intentionally overrides B97d.
    pos = css.find(B97D_END)
    if pos != -1:
        pos += len(B97D_END)
        return css[:pos].rstrip() + "\n\n" + block + "\n" + css[pos:].lstrip(), "inserted B97e override after B97d block"

    # Fallback: directly after the main Oberschwaben CSS block.
    pos = css.find(B96_CSS_END)
    if pos != -1:
        pos += len(B96_CSS_END)
        return css[:pos].rstrip() + "\n\n" + block + "\n" + css[pos:].lstrip(), "inserted B97e override after Oberschwaben CSS block"

    return css.rstrip() + "\n\n" + block + "\n", "appended B97e override block"


def write_report(today: str, action: str) -> None:
    DOCS.mkdir(exist_ok=True)
    md = f"""# B97e - Restore Oberschwaben Translucent Step Cards

Date: {today}

## Result

B97e restored stable semi-transparent Oberschwaben text cards.

## Changed files

- `src/styles.css`
- `docs/B97e_restore_oberschwaben_translucent_step_cards.md`
- `tasks/done.md`

## Action

- {action}

## Visual fix

B97d made card backgrounds too opaque. B97e keeps active/inactive card states
visually stable while using translucent background colors so the map remains
partly visible behind/around the cards.

## Technical note

The override uses `background: rgba(...)` rather than element-level `opacity`,
because element opacity would also fade the card text. Text readability is
therefore retained while the card surface remains translucent.

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
    marker = "## B97e - Restore Oberschwaben translucent step cards"
    if marker in current:
        return

    entry = f"""
## B97e - Restore Oberschwaben translucent step cards ({today})

- Added a CSS override block that restores stable semi-transparent Oberschwaben text-card backgrounds.
- Preserved stable active/inactive behavior from B97d while making the map visible through/around the cards again.
- Added `docs/B97e_restore_oberschwaben_translucent_step_cards.md`.
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

    print("B97e Oberschwaben translucent step-card correction complete.")
    print("Changed/created:")
    for path in [CSS, REPORT, DONE]:
        print(f"  {rel(path)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  inspect locally in browser")


if __name__ == "__main__":
    main()
