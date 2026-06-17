#!/usr/bin/env python3
r"""
B6c v3 — Make ranking-map linking unmistakably visible.

Run from repository root:

  python scripts\12_link_rankings_and_map_v3_visible.py

Adds:
- active-country marker/label on the map,
- stronger active row styling,
- stronger active country styling,
- clearer selected-country detail box.

No data changes.
"""

from pathlib import Path
import datetime

HELPER_JS = '\n  function geometryCentroid(geometry) {\n    const points = [];\n\n    function collectRing(ring) {\n      if (!ring) return;\n      ring.forEach(coord => {\n        const projected = project(coord);\n        points.push(projected);\n      });\n    }\n\n    if (!geometry) return null;\n\n    if (geometry.type === "Polygon") {\n      geometry.coordinates.forEach(collectRing);\n    } else if (geometry.type === "MultiPolygon") {\n      geometry.coordinates.forEach(poly => poly.forEach(collectRing));\n    }\n\n    if (!points.length) return null;\n\n    const x = points.reduce((sum, p) => sum + p[0], 0) / points.length;\n    const y = points.reduce((sum, p) => sum + p[1], 0) / points.length;\n\n    return [x, y];\n  }\n\n  function addActiveMarker(feature) {\n    const svg = document.querySelector("#hotspotMap svg");\n    if (!svg || !feature || !feature.geometry) return;\n\n    svg.querySelectorAll(".hotspot-active-marker, .hotspot-active-marker-ring, .hotspot-active-label").forEach(el => el.remove());\n\n    const centroid = geometryCentroid(feature.geometry);\n    if (!centroid) return;\n\n    const props = feature.properties || {};\n    const [x, y] = centroid;\n    const label = props.country || "Selected";\n\n    const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");\n    ring.setAttribute("class", "hotspot-active-marker-ring");\n    ring.setAttribute("cx", x);\n    ring.setAttribute("cy", y);\n    ring.setAttribute("r", "13");\n    svg.appendChild(ring);\n\n    const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");\n    dot.setAttribute("class", "hotspot-active-marker");\n    dot.setAttribute("cx", x);\n    dot.setAttribute("cy", y);\n    dot.setAttribute("r", "5.5");\n    svg.appendChild(dot);\n\n    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");\n    text.setAttribute("class", "hotspot-active-label");\n    text.setAttribute("x", Math.min(WIDTH - 140, x + 16));\n    text.setAttribute("y", Math.max(16, y - 10));\n    text.textContent = label;\n    svg.appendChild(text);\n  }\n'
CSS_APPEND = '\n/* B6c v3: unmistakable linked selection state */\n.hotspot-row.link-active {\n  background: rgba(236,255,176,.16) !important;\n  box-shadow: inset 4px 0 0 var(--accent), inset 0 0 0 1px rgba(236,255,176,.42) !important;\n}\n\n.hotspot-row.link-active strong,\n.hotspot-row.link-active .hotspot-row-head span {\n  color: #ecffb0 !important;\n}\n\n.hotspot-country.link-active {\n  fill: #ecffb0 !important;\n  stroke: #ffffff !important;\n  stroke-width: 2.8 !important;\n  opacity: 1 !important;\n  filter: drop-shadow(0 0 9px rgba(236,255,176,.75));\n}\n\n.hotspot-active-marker {\n  fill: #ecffb0;\n  stroke: #0b1411;\n  stroke-width: 2;\n  pointer-events: none;\n  filter: drop-shadow(0 0 8px rgba(236,255,176,.8));\n}\n\n.hotspot-active-marker-ring {\n  fill: none;\n  stroke: #ecffb0;\n  stroke-width: 2;\n  opacity: .72;\n  pointer-events: none;\n}\n\n.hotspot-active-label {\n  fill: #ecffb0;\n  font-size: 14px;\n  font-weight: 800;\n  paint-order: stroke;\n  stroke: #0b1411;\n  stroke-width: 4px;\n  stroke-linejoin: round;\n  pointer-events: none;\n}\n\n.hotspot-map-details {\n  border: 1px solid rgba(236,255,176,.22);\n  border-radius: .8rem;\n  padding: .75rem .85rem;\n  background: rgba(236,255,176,.045);\n}\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    root = Path.cwd()
    js_path = root / "src" / "hotspots.js"
    css_path = root / "src" / "styles.css"

    if not js_path.exists():
        raise SystemExit("src/hotspots.js not found.")
    if not css_path.exists():
        raise SystemExit("src/styles.css not found.")

    js = read(js_path)

    if "function geometryCentroid" not in js:
        marker = "  function quantileBreaks(values) {"
        if marker not in js:
            raise SystemExit("Could not find insertion point before quantileBreaks.")
        js = js.replace(marker, HELPER_JS + "\n" + marker)

    old = """    document.querySelectorAll(".hotspot-row[data-country-key], .hotspot-country[data-country-key]").forEach(el => {
      if (el.dataset.countryKey === countryKeyValue) {
        el.classList.add("link-active");
      }
    });

    const details = document.querySelector("#hotspotMapDetails");"""

    new = """    document.querySelectorAll(".hotspot-row[data-country-key], .hotspot-country[data-country-key]").forEach(el => {
      if (el.dataset.countryKey === countryKeyValue) {
        el.classList.add("link-active");
      }
    });

    const feature = geoFeatures.find(f => countryKey(f.properties?.country) === countryKeyValue);
    if (feature) {
      addActiveMarker(feature);
    }

    const details = document.querySelector("#hotspotMapDetails");"""

    if "addActiveMarker(feature);" not in js:
        if old not in js:
            raise SystemExit("Could not find applyLinkedHighlight insertion point.")
        js = js.replace(old, new)

    write(js_path, js)

    css = read(css_path)
    if "B6c v3: unmistakable linked selection state" not in css:
        write(css_path, css + "\n" + CSS_APPEND)

    today = datetime.date.today().isoformat()
    method = f"""# B6c v3 — Visible Ranking-Map Linking

Date: {today}

## Problem

The ranking-map linking was technically present but visually too weak.

## Change

This patch makes selected countries explicit by adding:

- stronger active country fill and outline,
- stronger active ranking-row styling,
- a centroid-based marker and label on the map,
- a clearer selected-country details box.

## Status

Visual/interaction refinement only. No data changes.

## Caveat

The marker is centroid-based and approximate. It is a visual selection aid, not a geographic measurement.
"""
    write(root / "docs" / "B6c_v3_visible_ranking_map_linking.md", method)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B6c v3 completed" not in done_text:
        done_text += f"- {today}: Task B6c v3 completed — made ranking-map linking visibly explicit with marker and stronger highlights.\n"
        write(done, done_text)

    print("B6c v3 visible linking applied.")
    print("Changed/created:")
    print("  src/hotspots.js")
    print("  src/styles.css")
    print("  docs/B6c_v3_visible_ranking_map_linking.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
