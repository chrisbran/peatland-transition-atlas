#!/usr/bin/env python3
r"""
B18b5 — Increase GPM2 context opacity in emissions states.

Run from repository root:

  python scripts\43_increase_gpm_context_opacity.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
CSS = '\n/* B18b5 increase GPM2 context opacity in emissions states */\n.central-map-story[data-state="total"] .layer-gpm {\n  opacity: .68;\n}\n\n.central-map-story[data-state="density"] .layer-gpm {\n  opacity: .68;\n}\n\n.central-map-story[data-state="compare"] .layer-gpm {\n  opacity: .50;\n}\n'
DOC = '# B18b5 — Increase GPM2 Context Opacity in Emissions States\n\nDate: 2026-06-18\n\n## Purpose\n\nThe transparent ArcGIS layer stack now works well, but the GPM2 peatland context was still too subtle beneath the emissions layers.\n\n## Change\n\nThis small CSS override increases GPM2 opacity while preserving the emissions layer as the dominant analytical layer:\n\n| State | Previous GPM2 opacity | New GPM2 opacity |\n|---|---:|---:|\n| Total emissions | 0.58 | 0.68 |\n| Emission density | 0.58 | 0.68 |\n| Compare | 0.42 | 0.50 |\n\n## Acceptance check\n\n- GPM2 remains visible beneath total and density layers.\n- Emissions remain the dominant visual signal.\n- No milky haze returns.\n- The map remains stable and aligned.\n'
TASK = '# Task B18c — Global Callouts and Metric Interpretation\n\n## Goal\n\nAdd sparse, scroll-state-specific callouts to make the global metric shift easier to understand.\n\n## Work items\n\n1. Add 2–4 callouts for the total-emissions state.\n2. Add 2–4 callouts for the emission-density state.\n3. Avoid over-labeling the map.\n4. Keep callouts statement-driven, not decorative.\n5. Ensure callouts work on desktop and degrade gracefully on mobile.\n6. Use the existing central global map stage; do not add new map panels.\n\n## Acceptance criteria\n\n- A viewer understands why total emissions and density differ without reading a long explanation.\n- The map remains visually calm.\n- Peatland context, emissions, and callouts have a clear visual hierarchy.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    root = Path.cwd()
    styles = root / "src" / "styles.css"

    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")

    css_text = read(styles)
    if "B18b5 increase GPM2 context opacity in emissions states" not in css_text:
        write(styles, css_text.rstrip() + "\n" + CSS + "\n")

    write(root / "docs" / "B18b5_increase_gpm_context_opacity.md", DOC)
    write(root / "tasks" / "B18c_global_callouts_and_metric_interpretation.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B18b5 completed" not in done_text:
        done_text += f"- {TODAY}: Task B18b5 completed — increased GPM2 context opacity under emissions overlays.\n"
        write(done, done_text)

    print("B18b5 applied: GPM2 context opacity increased in emissions states.")
    print("Changed/created:")
    print("  src/styles.css")
    print("  docs/B18b5_increase_gpm_context_opacity.md")
    print("  tasks/B18c_global_callouts_and_metric_interpretation.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")
    print()
    print("Check:")
    print("  GPM2 should be more visible under total/density, without reducing emissions readability.")

if __name__ == "__main__":
    main()
