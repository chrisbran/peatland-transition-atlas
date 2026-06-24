#!/usr/bin/env python3
"""
B97b - Lighten Oberschwaben stage while keeping central-story scale.

Problem observed after B97
--------------------------
B97 fixed the size and central-stage feel, but the section became too dark for a
fine-grained regional map. The Oberschwaben layers contain many small polygons
and labels, so a dark/vignetted stage reduces readability.

B97b keeps:
- the large sticky 16:9 stage
- the B96 HTML structure
- the B96 IntersectionObserver logic
- the B95h validated PNG assets

B97b changes:
- replaces the dark section with a warm editorial/light stage
- keeps the map large, but removes heavy dark vignette
- uses light glass cards instead of dark cards
- keeps the legend compact, but makes it a light overlay
- increases thematic layer readability

Changed files:
- src/styles.css
- docs/B97b_lighten_oberschwaben_stage.md
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
REPORT = DOCS / "B97b_lighten_oberschwaben_stage.md"

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
        print(f"B97b cannot run. Missing `{rel(CSS)}`.")
        sys.exit(1)

    css = read_text(CSS)
    if CSS_START not in css or CSS_END not in css:
        print("B97b cannot run. The B96/B97 Oberschwaben CSS block was not found in src/styles.css.")
        print("Run B96 first, then B97 or B97b.")
        sys.exit(1)

    missing = [p for p in REQUIRED_ASSETS if not p.exists()]
    if missing:
        print("B97b cannot run. Required Oberschwaben layer assets are missing:")
        for path in missing:
            print(f"  - {rel(path)}")
        sys.exit(1)


def build_css_block() -> str:
    return f"""{CSS_START}
/*
  B97b visual alignment pass:
  Keep the large central-story stage introduced in B97, but use a lighter
  editorial treatment because the Oberschwaben regional layers are too detailed
  for a dark/vignetted map container.
*/

.moore-ob-section {{
  position: relative;
  margin: 0;
  padding: clamp(4.5rem, 8vw, 8rem) 0 clamp(5rem, 9vw, 9rem);
  color: #1d241f;
  background:
    radial-gradient(circle at 12% 8%, rgba(104, 142, 115, 0.14), transparent 32rem),
    radial-gradient(circle at 86% 26%, rgba(64, 112, 116, 0.12), transparent 36rem),
    linear-gradient(180deg, #f5f0e4 0%, #ebe6d9 48%, #f7f2e8 100%);
  overflow: clip;
}}

.moore-ob-section::before {{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(90deg, rgba(46, 58, 49, 0.045) 1px, transparent 1px),
    linear-gradient(180deg, rgba(46, 58, 49, 0.035) 1px, transparent 1px);
  background-size: 82px 82px;
  mask-image: radial-gradient(circle at 50% 34%, black 0%, transparent 74%);
  opacity: 0.42;
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
  color: rgba(50, 63, 55, 0.62);
}}

.moore-ob-heading h2 {{
  max-width: 1040px;
  margin: 0;
  font-size: clamp(2.35rem, 5.8vw, 6.2rem);
  line-height: 0.9;
  letter-spacing: -0.064em;
  color: #1d241f;
}}

.moore-ob-lead {{
  max-width: 820px;
  margin: 1.25rem 0 0;
  font-size: clamp(1.02rem, 1.45vw, 1.32rem);
  line-height: 1.55;
  color: rgba(44, 55, 49, 0.74);
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
    radial-gradient(circle at 46% 38%, rgba(255, 255, 255, 0.82), transparent 42%),
    linear-gradient(135deg, #fbf8ef 0%, #ebe7db 100%);
  border: 1px solid rgba(64, 74, 65, 0.18);
  box-shadow:
    0 2rem 5rem rgba(36, 45, 39, 0.20),
    inset 0 1px 0 rgba(255, 255, 255, 0.72);
}}

.moore-ob-stage::after {{
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: inherit;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.28), transparent 18%),
    radial-gradient(circle at 52% 45%, transparent 58%, rgba(70,75,64,0.045) 100%);
  opacity: 0.62;
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
  filter: drop-shadow(0 0 0.12rem rgba(255, 255, 255, 0.7));
}}

.moore-ob-layer--agriculture {{
  z-index: 10;
}}

.moore-ob-layer--moor {{
  z-index: 20;
}}

.moore-ob-layer--intersection {{
  z-index: 30;
}}

.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="intersection"] {{
  opacity: 0;
}}

.moore-ob-section[data-oberschwaben-state="agriculture"] [data-ob-layer="agriculture"] {{
  opacity: 1;
  filter: saturate(1.0) contrast(1.02);
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="agriculture"] {{
  opacity: 0.58;
  filter: saturate(0.86) contrast(0.98);
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="moor"] {{
  opacity: 0.86;
  filter: saturate(1.08) contrast(1.04);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="agriculture"] {{
  opacity: 0.42;
  filter: saturate(0.78) contrast(0.96);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="moor"] {{
  opacity: 0.36;
  filter: saturate(0.88) contrast(0.94);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="intersection"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="intersection"] {{
  opacity: 0.96;
  filter: saturate(1.06) contrast(1.04) drop-shadow(0 0 0.10rem rgba(255, 255, 255, 0.35));
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
  padding: 0.72rem 0.84rem;
  border-radius: 999px;
  background: rgba(255, 252, 244, 0.78);
  border: 1px solid rgba(48, 58, 51, 0.14);
  backdrop-filter: blur(12px);
  box-shadow: 0 0.85rem 2.1rem rgba(45, 52, 45, 0.12);
  font-size: clamp(0.68rem, 0.76vw, 0.78rem);
  line-height: 1.22;
  color: rgba(35, 43, 38, 0.82);
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
  border: 1px solid rgba(35, 43, 38, 0.18);
  box-shadow: 0 0 0 1px rgba(255,255,255,0.32);
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
  background: rgba(255, 252, 244, 0.72);
  border: 1px solid rgba(48, 58, 51, 0.13);
  box-shadow: 0 1.1rem 2.6rem rgba(36, 45, 39, 0.10);
  color: rgba(29, 36, 31, 0.88);
  opacity: 0.58;
  transform: translateY(0.35rem);
  transition: opacity 260ms ease, transform 260ms ease, background 260ms ease, border-color 260ms ease;
  backdrop-filter: blur(8px);
}}

.moore-ob-step.is-active {{
  opacity: 1;
  transform: translateY(0);
  background: rgba(255, 252, 244, 0.92);
  border-color: rgba(48, 58, 51, 0.26);
}}

.moore-ob-step-label {{
  margin: 0 0 0.65rem;
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(56, 70, 61, 0.56);
}}

.moore-ob-step h3 {{
  margin: 0;
  font-size: clamp(1.22rem, 1.85vw, 1.75rem);
  line-height: 1.08;
  letter-spacing: -0.03em;
  color: #1d241f;
}}

.moore-ob-step p:not(.moore-ob-step-label) {{
  margin: 0.85rem 0 0;
  line-height: 1.56;
  color: rgba(44, 55, 49, 0.72);
}}

.moore-ob-step--boundary {{
  border-color: rgba(43, 103, 93, 0.24);
  background: rgba(241, 248, 244, 0.82);
}}

.moore-ob-step--boundary.is-active {{
  border-color: rgba(43, 103, 93, 0.42);
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
    background: rgba(255, 252, 244, 0.86);
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
    md = f"""# B97b - Lighten Oberschwaben Stage

Date: {today}

## Result

B97b replaced the dark B97 Oberschwaben visual treatment with a lighter editorial
stage while keeping the larger central-story scale.

## Changed files

- `src/styles.css`
- `docs/B97b_lighten_oberschwaben_stage.md`
- `tasks/done.md`

## Not changed

- `index.html`
- `public/maps/oberschwaben/*.png`
- GIS/raw data
- B96 scroll-state JavaScript

## Reason

The B97 stage size was correct, but the dark/vignetted treatment reduced
readability for the fine-grained Oberschwaben polygons and district labels.
A lighter warm stage is more suitable for this regional, high-detail map.

## Design changes

- Warm editorial section background instead of dark background.
- Light 16:9 map card, preserving the large central-story scale.
- Compact light legend overlay.
- Light glass story cards.
- Higher thematic layer readability and lower dark vignette.

## QA recommendation

Run:

```powershell
python scripts\\95h_validate_oberschwaben_layer_stack.py
python scripts\\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section locally in the browser/video.
"""
    write_text(REPORT, md)


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B97b - Lighten Oberschwaben stage"
    if marker in current:
        return

    entry = f"""
## B97b - Lighten Oberschwaben stage ({today})

- Replaced the dark B97 Oberschwaben CSS treatment with a lighter warm editorial stage.
- Kept the large central-story scale introduced by B97.
- Preserved B96 HTML/JS and the validated B95h layer assets.
- Added `docs/B97b_lighten_oberschwaben_stage.md`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    css = read_text(CSS)
    updated, replaced = replace_css_block(css, build_css_block())
    if not replaced:
        print("B97b did not modify styles.css because the Oberschwaben CSS block was not found.")
        sys.exit(1)

    write_text(CSS, updated)
    write_report(today)
    update_done(today)

    print("B97b Oberschwaben light-stage refinement complete.")
    print("Changed/created:")
    for path in [CSS, REPORT, DONE]:
        print(f"  {rel(path)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  inspect locally in browser")


if __name__ == "__main__":
    main()
