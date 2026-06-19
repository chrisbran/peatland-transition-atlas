#!/usr/bin/env python3
r"""
B18b6 — Simplify compare state in central global map story.

Run from repository root:

  python scripts\44_simplify_central_map_compare_state.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
CSS = '\n/* B18b6 simplify compare state: no extra mixed hotspot layer */\n.central-map-story[data-state="compare"] .layer-gpm {\n  opacity: .68;\n}\n\n.central-map-story[data-state="compare"] .layer-total {\n  opacity: 0;\n}\n\n.central-map-story[data-state="compare"] .layer-density {\n  opacity: .86;\n}\n\n.central-map-story[data-state="compare"] .layer-borders {\n  opacity: .96;\n}\n'
DOC = '# B18b6 — Simplify Compare State\n\nDate: 2026-06-18\n\n## Problem\n\nThe central global map appeared to show an additional map layer after the total-emissions and emission-density states. This was not an export error. It came from the compare state, where total and density overlays were intentionally shown together.\n\n## Decision\n\nThe mixed overlay is visually confusing. The compare state should not introduce a fourth visual map state.\n\n## Fix\n\nThe compare state now keeps the density view visible and uses the text to explain the metric comparison:\n\n- total emissions = absolute national climate relevance;\n- emission density = intensity relative to mapped drained organic-soil area.\n\n## Acceptance check\n\nDuring scroll, the sequence should read as:\n\n1. peatland extent;\n2. total emissions;\n3. emission density;\n4. interpretation text without a new mixed map layer.\n\nThere should be no apparent extra hotspot layer after density.\n'
TASK = '# Task B18c — Clean Central Global Story Stage\n\n## Goal\n\nReduce redundancy and improve readability in the central global map story.\n\n## Work items\n\n1. Reduce the in-map titlebar so it does not repeat the large scroll card.\n2. Keep the scroll card as the main narrative text.\n3. Improve text-card positioning so it does not cover the legend or map title.\n4. Add sparse callouts only after the stage is visually stable.\n5. Keep one central map; do not add extra map panels.\n\n## Acceptance criteria\n\n- The map is the visual focus.\n- The text does not repeat itself.\n- The compare step no longer feels like a hidden extra map layer.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_js(text: str) -> str:
    text = text.replace('mode: "Metric comparison",', 'mode: "Metric interpretation",')

    old_legend = """legend: `
        <span><i class="legend-risk"></i>Total emissions</span>
        <span><i class="legend-density"></i>Emission density</span>
        <span><i class="legend-border"></i>Country frame</span>
      `,"""

    new_legend = """legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-density"></i>Emission density view</span>
        <span><i class="legend-border"></i>Country frame</span>
      `,"""

    text = text.replace(old_legend, new_legend)
    text = text.replace(
        'source: "The same global frame keeps the spatial comparison stable while the metric changes."',
        'source: "Interpretation state: density view remains visible; text explains why total emissions and density must be read together."'
    )
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
        print("Updated compare state metadata in src/central_global_map_story.js")
    else:
        print("No JS metadata replacement was needed or exact strings were not found.")

    css_text = read(styles)
    if "B18b6 simplify compare state: no extra mixed hotspot layer" not in css_text:
        write(styles, css_text.rstrip() + "\n" + CSS + "\n")

    write(root / "docs" / "B18b6_simplify_compare_state.md", DOC)
    write(root / "tasks" / "B18c_clean_central_global_story_stage.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B18b6 completed" not in done_text:
        done_text += f"- {TODAY}: Task B18b6 completed — simplified compare state to avoid mixed hotspot overlay.\n"
        write(done, done_text)

    print("B18b6 applied: compare state no longer overlays total and density together.")
    print("Changed/created:")
    print("  src/central_global_map_story.js")
    print("  src/styles.css")
    print("  docs/B18b6_simplify_compare_state.md")
    print("  tasks/B18c_clean_central_global_story_stage.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
