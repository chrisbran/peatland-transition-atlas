#!/usr/bin/env python3
r"""
B18c — Clean central global story stage.

Run from repository root:

  python scripts\45_clean_central_global_story_stage.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
CSS = '\n/* B18c clean central global story stage */\n.central-map-titlebar {\n  width: auto;\n  max-width: none;\n  padding: .45rem .65rem;\n  border-radius: 999px;\n  background: rgba(5, 11, 10, .62);\n}\n\n.central-map-titlebar span {\n  margin: 0;\n  font-size: .68rem;\n  letter-spacing: .10em;\n}\n\n.central-map-titlebar strong {\n  display: none;\n}\n\n/* Let the scroll card carry the narrative; keep it compact and away from the map legend. */\n.central-map-steps {\n  width: min(395px, calc(100vw - 2rem));\n  margin-left: clamp(.8rem, 5vw, 5.25rem);\n  padding-top: 28vh;\n  padding-bottom: 52vh;\n}\n\n.central-map-step {\n  min-height: 76vh;\n}\n\n.central-map-step::before {\n  width: min(395px, calc(100vw - 2rem));\n  min-height: 9.75rem;\n  background: rgba(5, 11, 10, .78);\n  border-color: rgba(232, 222, 159, .16);\n}\n\n.central-map-step h3 {\n  font-size: clamp(1.12rem, 2.05vw, 1.72rem);\n  line-height: 1.06;\n  margin-top: .32rem;\n}\n\n.central-map-step p {\n  font-size: .92rem;\n  line-height: 1.46;\n}\n\n.central-map-step > span {\n  font-size: .68rem;\n}\n\n/* Source stays readable but does not compete with the map. */\n.central-map-source {\n  max-width: min(360px, 34%);\n  color: rgba(238, 236, 219, .58);\n}\n\n/* Keep legend readable but subordinate. */\n.central-map-legend {\n  padding: .42rem .58rem;\n  gap: .32rem .62rem;\n}\n\n.central-map-legend span {\n  font-size: .70rem;\n}\n\n/* Slightly reduce visual heaviness around the central map shell. */\n.central-map-shell {\n  box-shadow: 0 20px 70px rgba(0, 0, 0, .24);\n}\n\n@media (max-width: 980px) {\n  .central-map-titlebar strong {\n    display: none;\n  }\n\n  .central-map-steps {\n    padding-top: 0;\n    padding-bottom: 2rem;\n  }\n\n  .central-map-step::before {\n    width: min(720px, calc(100vw - 2rem));\n  }\n}\n'
DOC = '# B18c — Clean Central Global Story Stage\n\nDate: 2026-06-18\n\n## Purpose\n\nThe central global map story is now visually and technically stable. This cleanup pass reduces redundancy and makes the map itself the main visual object.\n\n## Changes\n\n- Reduces the in-map titlebar to a compact mode label.\n- Hides the repeated in-map title because the scroll card already carries the narrative statement.\n- Makes scroll text cards slightly more compact.\n- Keeps the scroll card as the main explanatory layer.\n- Keeps legend and source visible but subordinate.\n\n## Rationale\n\nThe previous state had two narrative text layers saying similar things:\n\n1. the large scroll card;\n2. the in-map titlebar.\n\nThis made the map feel more crowded than necessary. The new logic is:\n\n- scroll card = narrative argument;\n- in-map titlebar = current mode only;\n- map = primary visual evidence.\n\n## Acceptance check\n\n- The central map feels calmer.\n- There is less duplicate text.\n- The card does not visually compete with the map.\n- Total and density transitions remain unchanged.\n'
TASK = '# Task B18d — Global Callouts and Metric Interpretation\n\n## Goal\n\nAdd sparse, state-specific callouts to the central global map, but only after the central stage is visually stable.\n\n## Work items\n\n1. Add 2–3 callouts for total emissions.\n2. Add 2–3 callouts for emission density.\n3. Use short statement labels, not generic country labels.\n4. Avoid over-labeling.\n5. Make callouts degrade gracefully on mobile.\n6. Keep the central map as one map stage; do not add new panels.\n\n## Acceptance criteria\n\n- The user can understand why total emissions and density differ without long text.\n- Callouts clarify, but do not decorate.\n- The visual hierarchy remains: map → metric state → callout → text card.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_js(text: str) -> str:
    # Shorten mode labels slightly if exact strings are present.
    replacements = {
        'mode: "Global peatland context",': 'mode: "Peatland context",',
        'mode: "Metric interpretation",': 'mode: "Interpretation",',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def main():
    root = Path.cwd()
    styles = root / "src" / "styles.css"
    js = root / "src" / "central_global_map_story.js"

    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")
    if not js.exists():
        raise SystemExit("src/central_global_map_story.js not found. Run B18b-new first.")

    js_text = read(js)
    new_js = patch_js(js_text)
    if new_js != js_text:
        write(js, new_js)
        print("Shortened selected central map mode labels.")
    else:
        print("No JS label changes needed.")

    css_text = read(styles)
    if "B18c clean central global story stage" not in css_text:
        write(styles, css_text.rstrip() + "\n" + CSS + "\n")

    write(root / "docs" / "B18c_clean_central_global_story_stage.md", DOC)
    write(root / "tasks" / "B18d_global_callouts_and_metric_interpretation.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B18c completed" not in done_text:
        done_text += f"- {TODAY}: Task B18c completed — cleaned central global story stage and reduced repeated text.\n"
        write(done, done_text)

    print("B18c central global story cleanup applied.")
    print("Changed/created:")
    print("  src/central_global_map_story.js")
    print("  src/styles.css")
    print("  docs/B18c_clean_central_global_story_stage.md")
    print("  tasks/B18d_global_callouts_and_metric_interpretation.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
