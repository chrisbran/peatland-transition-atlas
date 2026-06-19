#!/usr/bin/env python3
r"""
B18b4 — Keep GPM2 visible beneath emissions overlays.

Run from repository root:

  python scripts\42_keep_gpm_context_under_emissions.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
CSS = '\n/* B18b4 keep GPM2 context visible beneath emissions overlays */\n.central-map-layer {\n  filter: none !important;\n  mix-blend-mode: normal !important;\n}\n\n.central-map-story[data-state="extent"] .layer-gpm {\n  opacity: 1;\n}\n\n.central-map-story[data-state="extent"] .layer-total,\n.central-map-story[data-state="extent"] .layer-density {\n  opacity: 0;\n}\n\n.central-map-story[data-state="extent"] .layer-borders {\n  opacity: .82;\n}\n\n.central-map-story[data-state="total"] .layer-gpm {\n  opacity: .58;\n}\n\n.central-map-story[data-state="total"] .layer-total {\n  opacity: .86;\n}\n\n.central-map-story[data-state="total"] .layer-density {\n  opacity: 0;\n}\n\n.central-map-story[data-state="total"] .layer-borders {\n  opacity: .96;\n}\n\n.central-map-story[data-state="density"] .layer-gpm {\n  opacity: .58;\n}\n\n.central-map-story[data-state="density"] .layer-total {\n  opacity: 0;\n}\n\n.central-map-story[data-state="density"] .layer-density {\n  opacity: .86;\n}\n\n.central-map-story[data-state="density"] .layer-borders {\n  opacity: .96;\n}\n\n.central-map-story[data-state="compare"] .layer-gpm {\n  opacity: .42;\n}\n\n.central-map-story[data-state="compare"] .layer-total {\n  opacity: .62;\n}\n\n.central-map-story[data-state="compare"] .layer-density {\n  opacity: .58;\n}\n\n.central-map-story[data-state="compare"] .layer-borders {\n  opacity: 1;\n}\n\n/* Keep the map visually calm after the alpha re-export. */\n.central-map-shell {\n  background: rgba(5, 13, 11, .96);\n}\n'
DOC = '# B18b4 — Keep GPM2 Context Visible Beneath Emissions Overlays\n\nDate: 2026-06-18\n\n## Purpose\n\nThe central global map now uses transparent ArcGIS PNG overlays. With true alpha transparency, the GPM2 peatland context can remain visible underneath the emissions layers without creating the previous milky haze.\n\n## Change\n\nThe CSS state logic is refined so that:\n\n- `global_gpm2_peat_extent.png` remains visible in total-emissions and density states;\n- emissions overlays remain dominant but semi-transparent enough to reveal peatland context;\n- country borders remain visible for orientation;\n- CSS filters are explicitly disabled, because the visual quality should now come from the ArcGIS-rendered PNGs, not browser post-processing.\n\n## State opacity logic\n\n| State | GPM2 | Total | Density | Borders |\n|---|---:|---:|---:|---:|\n| Extent | 1.00 | 0.00 | 0.00 | 0.82 |\n| Total emissions | 0.58 | 0.86 | 0.00 | 0.96 |\n| Emission density | 0.58 | 0.00 | 0.86 | 0.96 |\n| Compare | 0.42 | 0.62 | 0.58 | 1.00 |\n\n## Acceptance check\n\nThe map should now show:\n\n1. peatland extent as a persistent geographic context;\n2. emissions as the dominant analytical layer;\n3. country borders clearly enough for orientation;\n4. no milky overlay or browser filter artefacts.\n'
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
    if "B18b4 keep GPM2 context visible beneath emissions overlays" not in css_text:
        write(styles, css_text.rstrip() + "\n" + CSS + "\n")

    write(root / "docs" / "B18b4_keep_gpm_context_under_emissions.md", DOC)
    write(root / "tasks" / "B18c_global_callouts_and_metric_interpretation.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B18b4 completed" not in done_text:
        done_text += f"- {TODAY}: Task B18b4 completed — kept GPM2 context visible under total-emissions and density overlays.\n"
        write(done, done_text)

    print("B18b4 applied: GPM2 context remains visible beneath emissions overlays.")
    print("Changed/created:")
    print("  src/styles.css")
    print("  docs/B18b4_keep_gpm_context_under_emissions.md")
    print("  tasks/B18c_global_callouts_and_metric_interpretation.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")
    print()
    print("Check:")
    print("  In total/density states, GPM2 should remain visible but subordinate.")
    print("  There should be no milky haze and no CSS filter artefacts.")

if __name__ == "__main__":
    main()
