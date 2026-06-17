#!/usr/bin/env python3
r"""
B8b — Apply a Robinson-style world projection to the hotspot map.

Run from repository root:

  python scripts\15_apply_robinson_projection.py

Purpose:
- reduce high-latitude visual exaggeration compared with the previous equirectangular projection,
- keep the map static and dependency-free,
- apply the same projection to the hotspot layer and the base land layer.

No data changes.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
OLD_PROJECT = '  function project(coord) {\n    const lon = coord[0];\n    const lat = coord[1];\n    const x = ((lon + 180) / 360) * WIDTH;\n    const y = ((90 - lat) / 180) * HEIGHT;\n    return [x, y];\n  }'
ROBINSON_PROJECT = '  function project(coord) {\n    /*\n    Robinson-style pseudo-projection using the standard 5-degree coefficient table.\n    This is not a GIS-grade reprojection step; it is a lightweight visual projection\n    for the static SVG prototype.\n    */\n    const lon = Math.max(-180, Math.min(180, Number(coord[0]) || 0));\n    const lat = Math.max(-90, Math.min(90, Number(coord[1]) || 0));\n    const absLat = Math.abs(lat);\n\n    const X = [\n      1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730, 0.9600,\n      0.9427, 0.9216, 0.8962, 0.8679, 0.8350, 0.7986, 0.7597,\n      0.7186, 0.6732, 0.6213, 0.5722, 0.5322\n    ];\n\n    const Y = [\n      0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100, 0.3720,\n      0.4340, 0.4958, 0.5571, 0.6176, 0.6769, 0.7346, 0.7903,\n      0.8435, 0.8936, 0.9394, 0.9761, 1.0000\n    ];\n\n    const i = Math.min(17, Math.floor(absLat / 5));\n    const t = (absLat - i * 5) / 5;\n\n    const xCoef = X[i] + (X[i + 1] - X[i]) * t;\n    const yCoef = Y[i] + (Y[i + 1] - Y[i]) * t;\n\n    const lonRad = lon * Math.PI / 180;\n    const sign = lat < 0 ? -1 : 1;\n\n    const rawX = 0.8487 * xCoef * lonRad;\n    const rawY = 1.3523 * yCoef * sign;\n\n    const maxX = 0.8487 * Math.PI;\n    const maxY = 1.3523;\n\n    const x = (0.5 + rawX / (2 * maxX)) * WIDTH;\n    const y = (0.5 - rawY / (2 * maxY)) * HEIGHT;\n\n    return [x, y];\n  }'
CSS_APPEND = '\n/* B8b Robinson-style projection refinement */\n.hotspot-map::after {\n  content: "Projection: Robinson-style visual approximation · country-level screening layer";\n  display: block;\n  color: var(--muted);\n  font-size: .72rem;\n  padding: .35rem .55rem .55rem;\n  opacity: .78;\n}\n\n.hotspot-svg {\n  background: radial-gradient(circle at 50% 45%, rgba(255,255,255,.025), rgba(255,255,255,0) 62%);\n}\n'
METHOD = '# B8b — Projection Review and Robinson-Style Map Projection\n\nDate: 2026-06-17\n\n## Problem\n\nThe earlier hotspot map used a simple equirectangular projection. This was technically simple but visually exaggerated high-latitude countries and made the map look less cartographically credible.\n\n## Decision\n\nImplement a lightweight Robinson-style visual projection using the standard 5-degree coefficient table directly in JavaScript.\n\n## Why this option?\n\n- Keeps the atlas static and GitHub Pages compatible.\n- Avoids adding a build system or heavy mapping library.\n- Reduces high-latitude exaggeration compared with equirectangular display.\n- Applies consistently to the hotspot layer and the base land layer.\n\n## Implementation\n\nThe `project(coord)` function was replaced in:\n\n- `src/hotspots.js`\n- `src/hotspot_base_layer.js`\n\nThe projection is used only for SVG display. It is not a GIS-grade reprojection workflow.\n\n## Remaining caveats\n\n- The map remains country-level only.\n- Small islands and fragmented archipelagos remain difficult to select.\n- The projection is a visual approximation for an MVP atlas, not a scientific cartographic processing step.\n- Area comparisons should still be interpreted cautiously.\n\n## Next possible step\n\nB8c — refine tooltip/details panel and selected-country styling.\n'
TASK = '# Task B8c — Tooltip and Selected-Country Panel Refinement\n\n## Agent\n\nVisualization Engineer Agent + QA Critic Agent\n\n## Goal\n\nImprove how selected countries are explained after map/ranking interaction.\n\n## Candidate improvements\n\n- Replace hover-dependent details with a clearer selected-country panel.\n- Show rank, total emissions, density, area and metric mode.\n- Add small note if a clicked map country is not in the top-10 ranking.\n- Reduce reliance on map labels for small countries.\n\n## Acceptance criteria\n\n- static GitHub Pages deployment remains functional,\n- interaction is understandable without tutorial text,\n- country-level caveat remains visible.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def replace_project_function(path: Path):
    text = read(path)
    if "Robinson-style pseudo-projection" in text:
        return False
    if OLD_PROJECT not in text:
        raise SystemExit(f"Could not find old project() function in {path}")
    write(path, text.replace(OLD_PROJECT, ROBINSON_PROJECT))
    return True

def main():
    root = Path.cwd()
    hotspot_js = root / "src" / "hotspots.js"
    base_js = root / "src" / "hotspot_base_layer.js"
    styles = root / "src" / "styles.css"

    if not hotspot_js.exists():
        raise SystemExit("src/hotspots.js not found.")
    if not base_js.exists():
        raise SystemExit("src/hotspot_base_layer.js not found. Run B8a first.")
    if not styles.exists():
        raise SystemExit("src/styles.css not found.")

    changed_hotspots = replace_project_function(hotspot_js)
    changed_base = replace_project_function(base_js)

    css = read(styles)
    if "B8b Robinson-style projection refinement" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B8b_projection_review.md", METHOD)
    write(root / "tasks" / "B8c_tooltip_selected_country_panel.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B8b completed" not in done_text:
        done_text += f"- {TODAY}: Task B8b completed — replaced equirectangular map display with Robinson-style visual projection.\n"
        write(done, done_text)

    print("B8b projection refinement applied.")
    print("Changed/created:")
    print("  src/hotspots.js" + (" [updated]" if changed_hotspots else " [already updated]"))
    print("  src/hotspot_base_layer.js" + (" [updated]" if changed_base else " [already updated]"))
    print("  src/styles.css")
    print("  docs/B8b_projection_review.md")
    print("  tasks/B8c_tooltip_selected_country_panel.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
