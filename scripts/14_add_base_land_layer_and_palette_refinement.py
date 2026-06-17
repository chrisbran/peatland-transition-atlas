#!/usr/bin/env python3
r"""
B8a — Add base land layer and soften hotspot palette.

Run from repository root:

  python scripts\14_add_base_land_layer_and_palette_refinement.py

Purpose:
- add a non-interactive Natural Earth base-country layer behind the hotspot countries,
- distinguish ocean/background from non-hotspot/no-data land,
- soften the active-country highlight color,
- keep the hotspot map static, dependency-free and GitHub Pages compatible.
"""

from pathlib import Path
import datetime
import json
import urllib.request

TODAY = datetime.date.today().isoformat()

NATURAL_EARTH_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_admin_0_countries.geojson"
)

BASE_LAYER_JS = '/*\nB8a base land layer for hotspot choropleth.\n\nThis script inserts a non-interactive Natural Earth country base layer behind\nthe hotspot countries. It is intentionally independent from hotspots.js.\n*/\n\n(function () {\n  const BASE_GEOJSON_URL = "public/data/world_countries_110m_base.geojson";\n  const WIDTH = 960;\n  const HEIGHT = 500;\n  let baseFeatures = null;\n  let renderScheduled = false;\n\n  function project(coord) {\n    const lon = coord[0];\n    const lat = coord[1];\n    const x = ((lon + 180) / 360) * WIDTH;\n    const y = ((90 - lat) / 180) * HEIGHT;\n    return [x, y];\n  }\n\n  function ringToPath(ring) {\n    if (!ring || !ring.length) return "";\n    return ring.map((coord, idx) => {\n      const [x, y] = project(coord);\n      return `${idx === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;\n    }).join(" ") + " Z";\n  }\n\n  function geometryToPath(geometry) {\n    if (!geometry) return "";\n    if (geometry.type === "Polygon") {\n      return geometry.coordinates.map(ringToPath).join(" ");\n    }\n    if (geometry.type === "MultiPolygon") {\n      return geometry.coordinates.flatMap(poly => poly.map(ringToPath)).join(" ");\n    }\n    return "";\n  }\n\n  function insertBaseLayer() {\n    const svg = document.querySelector("#hotspotMap svg");\n    if (!svg || !baseFeatures || !baseFeatures.length) return;\n\n    svg.querySelectorAll(".base-country").forEach(el => el.remove());\n\n    const ocean = svg.querySelector(".map-ocean");\n    const firstHotspot = svg.querySelector(".hotspot-country");\n\n    const fragment = document.createDocumentFragment();\n\n    baseFeatures.forEach(feature => {\n      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");\n      path.setAttribute("class", "base-country");\n      path.setAttribute("d", geometryToPath(feature.geometry));\n      path.setAttribute("aria-hidden", "true");\n      fragment.appendChild(path);\n    });\n\n    if (firstHotspot) {\n      svg.insertBefore(fragment, firstHotspot);\n    } else if (ocean && ocean.nextSibling) {\n      svg.insertBefore(fragment, ocean.nextSibling);\n    } else {\n      svg.appendChild(fragment);\n    }\n  }\n\n  function scheduleRender() {\n    if (renderScheduled) return;\n    renderScheduled = true;\n\n    window.requestAnimationFrame(() => {\n      renderScheduled = false;\n      insertBaseLayer();\n    });\n  }\n\n  async function initBaseLayer() {\n    try {\n      const res = await fetch(BASE_GEOJSON_URL);\n      if (!res.ok) throw new Error(`Failed to load ${BASE_GEOJSON_URL}`);\n      const geo = await res.json();\n      baseFeatures = (geo.features || []).filter(f => f.geometry);\n\n      scheduleRender();\n\n      const map = document.querySelector("#hotspotMap");\n      if (map) {\n        const observer = new MutationObserver(scheduleRender);\n        observer.observe(map, { childList: true, subtree: true });\n      }\n    } catch (err) {\n      console.warn("Base land layer not loaded:", err);\n    }\n  }\n\n  if (document.readyState === "loading") {\n    document.addEventListener("DOMContentLoaded", initBaseLayer);\n  } else {\n    initBaseLayer();\n  }\n})();\n'
CSS_APPEND = '\n/* B8a visual/cartographic refinement: base land and softer palette */\n.map-ocean {\n  fill: rgba(16, 27, 24, .96) !important;\n}\n\n.base-country {\n  fill: rgba(91, 108, 93, .34);\n  stroke: rgba(8, 15, 13, .82);\n  stroke-width: .38;\n  pointer-events: none;\n  opacity: .82;\n}\n\n.hotspot-country {\n  stroke: rgba(10, 18, 16, .96);\n  stroke-width: .55;\n}\n\n/* Softer hotspot ramp; works for SVG paths. */\n.map-fill-no-data { fill: rgba(91,108,93,.30) !important; }\n.map-fill-1 { fill: rgba(88,125,117,.58) !important; }\n.map-fill-2 { fill: rgba(111,146,124,.66) !important; }\n.map-fill-3 { fill: rgba(165,172,105,.76) !important; }\n.map-fill-4 { fill: rgba(204,160,91,.80) !important; }\n.map-fill-5 { fill: rgba(202,112,82,.84) !important; }\n\n/* Same ramp for HTML legend swatches. */\n.legend-item i.map-fill-no-data { background: rgba(91,108,93,.30) !important; }\n.legend-item i.map-fill-1 { background: rgba(88,125,117,.58) !important; }\n.legend-item i.map-fill-2 { background: rgba(111,146,124,.66) !important; }\n.legend-item i.map-fill-3 { background: rgba(165,172,105,.76) !important; }\n.legend-item i.map-fill-4 { background: rgba(204,160,91,.80) !important; }\n.legend-item i.map-fill-5 { background: rgba(202,112,82,.84) !important; }\n\n/* Softer selected-country state. */\n.hotspot-country.link-active {\n  fill: rgba(212,196,118,.96) !important;\n  stroke: rgba(248,238,177,.95) !important;\n  stroke-width: 2.1 !important;\n  opacity: 1 !important;\n  filter: drop-shadow(0 0 5px rgba(212,196,118,.45)) !important;\n}\n\n.hotspot-active-marker {\n  fill: rgba(212,196,118,.96) !important;\n  stroke: rgba(12,20,17,.95) !important;\n  filter: drop-shadow(0 0 5px rgba(212,196,118,.48)) !important;\n}\n\n.hotspot-active-marker-ring {\n  stroke: rgba(212,196,118,.88) !important;\n  opacity: .62 !important;\n}\n\n.hotspot-active-label {\n  fill: rgba(232,222,159,.98) !important;\n  stroke: rgba(10,17,15,.96) !important;\n}\n\n.hotspot-row.link-active {\n  background: rgba(212,196,118,.105) !important;\n  box-shadow: inset 4px 0 0 rgba(212,196,118,.86), inset 0 0 0 1px rgba(212,196,118,.30) !important;\n}\n\n.hotspot-row.link-active strong,\n.hotspot-row.link-active .hotspot-row-head span {\n  color: rgba(232,222,159,.98) !important;\n}\n\n.hotspot-map-details {\n  border-color: rgba(212,196,118,.22) !important;\n  background: rgba(212,196,118,.045) !important;\n}\n'
METHOD = '# B8a — Base Land Layer and Softer Hotspot Palette\n\nDate: 2026-06-17\n\n## Problem\n\nThe first functional hotspot map worked, but several visual issues were visible:\n\n- ocean/background and non-hotspot land were hard to distinguish,\n- the selected-country highlight was too bright/neon,\n- countries without hotspot data did not appear as a neutral base layer,\n- the map looked more like a data overlay floating on a dark background than a geographic map.\n\n## Change\n\nThis patch adds a non-interactive Natural Earth 110m base-country layer behind the hotspot countries and softens the color palette.\n\n## Files\n\n- `public/data/world_countries_110m_base.geojson`\n- `src/hotspot_base_layer.js`\n- `src/styles.css`\n\n## Technical approach\n\n- no external JavaScript map library,\n- no build system,\n- dependency-free SVG enhancement,\n- base layer is inserted behind existing hotspot SVG paths,\n- MutationObserver re-inserts the base layer after metric-toggle map re-rendering.\n\n## Interpretation boundary\n\nThe map remains a country-level screening layer. It still does not show local rewetting suitability.\n\n## Remaining cartographic limitations\n\n- the map still uses a simple equirectangular projection,\n- high-latitude countries remain visually distorted,\n- small islands and territories remain difficult to interact with.\n'
B8B_TASK = '# Task B8b — Projection and Map Geometry Review\n\n## Agent\n\nVisualization Engineer Agent + QA Critic Agent\n\n## Goal\n\nReview whether the current equirectangular SVG projection is good enough for the portfolio version or whether a more appropriate world projection should be implemented.\n\n## Issues\n\n- High-latitude countries are visually exaggerated.\n- Country areas are not visually comparable in the current projection.\n- Small countries and archipelagos are difficult to select.\n- A more cartographically balanced projection may improve visual credibility.\n\n## Candidate options\n\n1. Keep current equirectangular projection and document limitation.\n2. Implement a simple Robinson/Natural Earth-style approximation without external dependencies.\n3. Use pre-projected simplified SVG/GeoJSON geometry.\n4. Move to a lightweight mapping library only if needed.\n\n## Acceptance criteria\n\n- no heavy framework unless clearly justified,\n- static GitHub Pages deployment remains functional,\n- map caveat remains visible,\n- visual credibility improves without overengineering.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def download_natural_earth():
    req = urllib.request.Request(NATURAL_EARTH_URL, headers={"User-Agent": "peatland-transition-atlas/0.2"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))

def minimal_base_geojson(ne):
    features = []
    for feat in ne.get("features", []):
        props = feat.get("properties", {})
        features.append({
            "type": "Feature",
            "properties": {
                "name": props.get("ADMIN") or props.get("NAME") or "",
                "iso_a3": props.get("ISO_A3") or props.get("ADM0_A3") or "",
                "m49": props.get("UN_A3") or props.get("ISO_N3") or "",
            },
            "geometry": feat.get("geometry"),
        })

    return {
        "type": "FeatureCollection",
        "name": "world_countries_110m_base",
        "metadata": {
            "source": "Natural Earth 110m Admin 0 Countries",
            "source_url": NATURAL_EARTH_URL,
            "purpose": "Neutral base land layer for hotspot atlas map",
            "created": TODAY,
        },
        "features": features,
    }

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    print("Downloading Natural Earth base layer...")
    ne = download_natural_earth()
    base = minimal_base_geojson(ne)

    base_path = root / "public" / "data" / "world_countries_110m_base.geojson"
    write(base_path, json.dumps(base, ensure_ascii=False, separators=(",", ":")))

    write(root / "src" / "hotspot_base_layer.js", BASE_LAYER_JS)

    index = root / "index.html"
    html = read(index)
    if 'src="src/hotspot_base_layer.js"' not in html:
        marker = '<script src="src/hotspots.js"></script>'
        if marker not in html:
            raise SystemExit("Could not find hotspots.js script tag in index.html.")
        html = html.replace(marker, marker + '\n  <script src="src/hotspot_base_layer.js"></script>')
        write(index, html)

    styles = root / "src" / "styles.css"
    css = read(styles)
    if "B8a visual/cartographic refinement" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B8a_visual_cartographic_refinement.md", METHOD)
    write(root / "tasks" / "B8b_projection_review.md", B8B_TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B8a completed" not in done_text:
        done_text += f"- {TODAY}: Task B8a completed — added base land layer and softened hotspot map palette.\n"
        write(done, done_text)

    print("B8a visual/cartographic refinement applied.")
    print("Changed/created:")
    print("  public/data/world_countries_110m_base.geojson")
    print("  src/hotspot_base_layer.js")
    print("  index.html")
    print("  src/styles.css")
    print("  docs/B8a_visual_cartographic_refinement.md")
    print("  tasks/B8b_projection_review.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
