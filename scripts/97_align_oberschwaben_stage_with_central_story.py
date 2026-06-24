#!/usr/bin/env python3
"""
B97 - Align Oberschwaben scrolly stage with the central story-map design.

Purpose
-------
B96 correctly bound the Oberschwaben PNG layer stack into the page, but the
first visual pass made the map feel like a smaller scientific publication figure.
B97 keeps the B96 HTML/JS and replaces only the B96 CSS block with a larger,
darker, central-story-aligned stage.

Changes
-------
- Replaces the CSS block between:
  /* B96_OBERSCHWABEN_SCROLLY_START */
  /* B96_OBERSCHWABEN_SCROLLY_END */
- Enlarges the sticky map stage.
- Gives the Oberschwaben section a darker editorial story-map background.
- Moves the legend into a compact overlay style.
- Makes step cards visually closer to the main Global/Europe/Germany/BW story.
- Adds B97 documentation and updates tasks/done.md.

Does not modify
---------------
- GIS data
- PNG layer assets
- index.html structure
- B96 JS layer-state logic
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
REPORT = DOCS / "B97_align_oberschwaben_stage_with_central_story.md"

CSS_START = "/* B96_OBERSCHWABEN_SCROLLY_START */"
CSS_END = "/* B96_OBERSCHWABEN_SCROLLY_END */"

REQUIRED_ASSETS = [
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_admin_context.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_agriculture.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_moor_context.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_agriculture_moor_intersection.png",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    if not CSS.exists():
        print(f"B97 cannot run. Missing `{rel(CSS)}`.")
        sys.exit(1)

    css = read_text(CSS)
    if CSS_START not in css or CSS_END not in css:
        print("B97 cannot run. The B96 Oberschwaben CSS block was not found in src/styles.css.")
        print("Run B96 first, then rerun B97.")
        sys.exit(1)

    missing = [p for p in REQUIRED_ASSETS if not p.exists()]
    if missing:
        print("B97 cannot run. Required B95h/B96 Oberschwaben layer assets are missing:")
        for path in missing:
            print(f"  - {rel(path)}")
        sys.exit(1)


def build_css_block() -> str:
    return f"""{CSS_START}
/*
  B97 visual alignment pass:
  The Oberschwaben module uses the B96 layer logic, but is styled as a large
  editorial story-map stage rather than as a small publication-style map figure.
*/

.moore-ob-section {{
  position: relative;
  margin: 0;
  padding: clamp(4.5rem, 8vw, 8rem) 0 clamp(5rem, 9vw, 9rem);
  color: #edf1eb;
  background:
    radial-gradient(circle at 18% 8%, rgba(116, 145, 117, 0.22), transparent 34rem),
    radial-gradient(circle at 78% 28%, rgba(46, 90, 93, 0.26), transparent 34rem),
    linear-gradient(180deg, #111713 0%, #18211b 46%, #111713 100%);
  overflow: clip;
}}

.moore-ob-section::before {{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(255,255,255,0.026) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: radial-gradient(circle at 50% 35%, black 0%, transparent 72%);
  opacity: 0.55;
}}

.moore-ob-heading {{
  position: relative;
  z-index: 1;
  width: min(1420px, calc(100% - clamp(1.25rem, 4vw, 4rem)));
  margin: 0 auto clamp(2.2rem, 4.5vw, 4.6rem);
}}

.moore-ob-kicker {{
  margin: 0 0 0.65rem;
  font-size: 0.76rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(237, 241, 235, 0.62);
}}

.moore-ob-heading h2 {{
  max-width: 1040px;
  margin: 0;
  font-size: clamp(2.35rem, 5.8vw, 6.2rem);
  line-height: 0.9;
  letter-spacing: -0.064em;
  color: #f4f2e8;
}}

.moore-ob-lead {{
  max-width: 820px;
  margin: 1.25rem 0 0;
  font-size: clamp(1.02rem, 1.45vw, 1.32rem);
  line-height: 1.55;
  color: rgba(237, 241, 235, 0.72);
}}

.moore-ob-grid {{
  position: relative;
  z-index: 1;
  width: min(1500px, calc(100% - clamp(1rem, 3vw, 3.2rem)));
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(680px, 1.95fr) minmax(300px, 0.62fr);
  gap: clamp(1.2rem, 3vw, 3.2rem);
  align-items: start;
}}

.moore-ob-stage-column {{
  position: sticky;
  top: clamp(0.75rem, 7vh, 4.5rem);
  align-self: start;
  z-index: 1;
}}

.moore-ob-stage {{
  position: relative;
  aspect-ratio: 16 / 9;
  margin: 0;
  overflow: hidden;
  border-radius: clamp(1.05rem, 2vw, 1.65rem);
  background:
    radial-gradient(circle at 48% 44%, rgba(240, 237, 218, 0.08), transparent 34%),
    radial-gradient(circle at 20% 16%, rgba(98, 128, 93, 0.19), transparent 38%),
    linear-gradient(135deg, #1b241f 0%, #111713 100%);
  border: 1px solid rgba(225, 226, 205, 0.17);
  box-shadow:
    0 2.2rem 5.5rem rgba(0, 0, 0, 0.36),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}}

.moore-ob-stage::after {{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.07), transparent 20%),
    radial-gradient(circle at 52% 45%, transparent 46%, rgba(0,0,0,0.20) 100%);
  mix-blend-mode: screen;
  opacity: 0.55;
}}

.moore-ob-layer {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0;
  transition: opacity 540ms ease, filter 540ms ease, transform 540ms ease;
  will-change: opacity, filter;
}}

.moore-ob-layer--admin {{
  opacity: 0.96;
  z-index: 40;
  pointer-events: none;
  filter: drop-shadow(0 0 0.18rem rgba(5, 9, 7, 0.42));
}}

.moore-ob-layer--agriculture {{
  z-index: 10;
}}

.moore-ob-layer--moor {{
  z-index: 20;
}}

.moore-ob-layer--intersection {{
  z-index: 30;
  filter: drop-shadow(0 0 0.18rem rgba(12, 30, 29, 0.42));
}}

.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="intersection"] {{
  opacity: 0;
}}

.moore-ob-section[data-oberschwaben-state="agriculture"] [data-ob-layer="agriculture"] {{
  opacity: 0.96;
  filter: saturate(0.94) contrast(1.02);
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="agriculture"] {{
  opacity: 0.48;
  filter: saturate(0.74) contrast(0.96);
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="moor"] {{
  opacity: 0.92;
  filter: saturate(1.05) contrast(1.04);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="agriculture"] {{
  opacity: 0.26;
  filter: saturate(0.62) contrast(0.9);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="moor"] {{
  opacity: 0.28;
  filter: saturate(0.8) contrast(0.88);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="intersection"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="intersection"] {{
  opacity: 0.98;
  filter: saturate(1.08) contrast(1.08) drop-shadow(0 0 0.22rem rgba(8, 32, 31, 0.56));
}}

.moore-ob-legend {{
  position: absolute;
  left: clamp(0.85rem, 1.4vw, 1.3rem);
  right: clamp(0.85rem, 1.4vw, 1.3rem);
  bottom: clamp(0.85rem, 1.4vw, 1.3rem);
  z-index: 60;
  display: flex;
  flex-wrap: wrap;
  gap: 0.42rem 0.78rem;
  width: auto;
  margin: 0;
  padding: 0.72rem 0.82rem;
  border-radius: 999px;
  background: rgba(12, 18, 15, 0.62);
  border: 1px solid rgba(239, 238, 222, 0.14);
  backdrop-filter: blur(12px);
  box-shadow: 0 0.8rem 2rem rgba(0, 0, 0, 0.2);
  font-size: clamp(0.68rem, 0.76vw, 0.78rem);
  line-height: 1.22;
  color: rgba(246, 246, 236, 0.82);
}}

.moore-ob-legend-item {{
  display: inline-flex;
  align-items: center;
  gap: 0.36rem;
  white-space: nowrap;
}}

.moore-ob-swatch {{
  width: 0.72rem;
  height: 0.72rem;
  border-radius: 999px;
  display: inline-block;
  border: 1px solid rgba(246, 246, 236, 0.24);
  box-shadow: 0 0 0 1px rgba(0,0,0,0.14);
}}

.moore-ob-swatch--acker {{ background: #c4a188; }}
.moore-ob-swatch--gruenland {{ background: #8bc2ad; }}
.moore-ob-swatch--dauerkultur {{ background: #d99ad2; }}
.moore-ob-swatch--moor {{ background: #7f9aa2; }}
.moore-ob-swatch--intersection {{ background: #214f53; }}

.moore-ob-steps {{
  display: grid;
  gap: clamp(1.25rem, 4vh, 3.2rem);
  padding: 4vh 0 22vh;
}}

.moore-ob-step {{
  min-height: clamp(300px, 48vh, 560px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(1.05rem, 2.2vw, 1.65rem);
  border-radius: clamp(0.9rem, 1.5vw, 1.25rem);
  background:
    linear-gradient(180deg, rgba(244, 242, 232, 0.105), rgba(244, 242, 232, 0.062));
  border: 1px solid rgba(239, 238, 222, 0.12);
  box-shadow: 0 1.1rem 2.6rem rgba(0, 0, 0, 0.18);
  color: rgba(246, 246, 236, 0.86);
  opacity: 0.5;
  transform: translateY(0.35rem);
  transition: opacity 260ms ease, transform 260ms ease, background 260ms ease, border-color 260ms ease;
  backdrop-filter: blur(8px);
}}

.moore-ob-step.is-active {{
  opacity: 1;
  transform: translateY(0);
  background:
    linear-gradient(180deg, rgba(244, 242, 232, 0.16), rgba(244, 242, 232, 0.082));
  border-color: rgba(239, 238, 222, 0.28);
}}

.moore-ob-step-label {{
  margin: 0 0 0.65rem;
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(237, 241, 235, 0.58);
}}

.moore-ob-step h3 {{
  margin: 0;
  font-size: clamp(1.22rem, 1.85vw, 1.75rem);
  line-height: 1.08;
  letter-spacing: -0.03em;
  color: #f4f2e8;
}}

.moore-ob-step p:not(.moore-ob-step-label) {{
  margin: 0.85rem 0 0;
  line-height: 1.56;
  color: rgba(237, 241, 235, 0.72);
}}

.moore-ob-step--boundary {{
  border-color: rgba(115, 169, 157, 0.36);
  background:
    linear-gradient(180deg, rgba(48, 93, 87, 0.22), rgba(244, 242, 232, 0.065));
}}

.moore-ob-step--boundary.is-active {{
  border-color: rgba(138, 203, 190, 0.58);
}}

@media (min-width: 1280px) {{
  .moore-ob-stage {{
    min-height: min(75vh, 820px);
  }}
}}

@media (max-width: 1100px) {{
  .moore-ob-grid {{
    grid-template-columns: 1fr;
    width: min(1060px, calc(100% - 1.5rem));
  }}

  .moore-ob-stage-column {{
    top: 0.75rem;
  }}

  .moore-ob-steps {{
    padding-top: 1rem;
  }}
}}

@media (max-width: 760px) {{
  .moore-ob-section {{
    padding-top: 3.5rem;
  }}

  .moore-ob-heading h2 {{
    font-size: clamp(2rem, 13vw, 3.7rem);
  }}

  .moore-ob-stage {{
    border-radius: 0.85rem;
  }}

  .moore-ob-legend {{
    position: static;
    margin-top: 0.65rem;
    border-radius: 0.8rem;
    background: rgba(12, 18, 15, 0.72);
  }}

  .moore-ob-step {{
    min-height: 42vh;
  }}
}}

@media (prefers-reduced-motion: reduce) {{
  .moore-ob-layer,
  .moore-ob-step {{
    transition: none;
  }}
}}
{CSS_END}"""


def replace_css_block(css_text: str, block: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    if not pattern.search(css_text):
        return css_text, False
    return pattern.sub(block, css_text), True


def write_report(today: str) -> None:
    DOCS.mkdir(exist_ok=True)
    md = f"""# B97 - Align Oberschwaben Stage With Central Story

Date: {today}

## Result

B97 replaced the B96 Oberschwaben CSS block with a larger and darker
central-story-aligned visual treatment.

## Changed files

- `src/styles.css`
- `docs/B97_align_oberschwaben_stage_with_central_story.md`
- `tasks/done.md`

## Not changed

- `index.html`
- `public/maps/oberschwaben/*.png`
- GIS/raw data
- B96 scroll-state JavaScript

## Design changes

- Enlarged sticky map stage.
- Changed section background from light figure-like treatment to dark editorial map-stage treatment.
- Moved legend into a compact overlay-style treatment.
- Adapted story cards to a glass/dark style closer to the Global/Europe/Germany/BW map narrative.
- Preserved B96 state sequence and method-boundary language.

## QA recommendation

Run:

```powershell
python scripts\\95h_validate_oberschwaben_layer_stack.py
python scripts\\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section in the browser/video.
"""
    write_text(REPORT, md)


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B97 - Align Oberschwaben stage with central story"
    if marker in current:
        return

    entry = f"""
## B97 - Align Oberschwaben stage with central story ({today})

- Replaced the B96 Oberschwaben CSS block with a larger, darker central-story-aligned map stage.
- Preserved the B96 HTML, JS and validated layer assets.
- Added `docs/B97_align_oberschwaben_stage_with_central_story.md`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    css = read_text(CSS)
    updated, replaced = replace_css_block(css, build_css_block())
    if not replaced:
        print("B97 did not modify styles.css because the B96 CSS block was not found.")
        sys.exit(1)

    write_text(CSS, updated)
    write_report(today)
    update_done(today)

    print("B97 Oberschwaben central-story visual alignment complete.")
    print("Changed/created:")
    for path in [CSS, REPORT, DONE]:
        print(f"  {rel(path)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  inspect locally in browser")


if __name__ == "__main__":
    main()
