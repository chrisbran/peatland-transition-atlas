#!/usr/bin/env python3
r"""
B11c — Add Baden-Württemberg BK50-Moor preview map to the public atlas.

Run from repository root:

  python scripts\19_add_bw_bk50_moor_preview_map.py

Precondition:
  public/data/bw_bk50_moor_simplified.geojson exists.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()
BW_JS = '/*\nB11c Baden-Württemberg BK50-Moor preview map.\nStatic SVG rendering of the simplified BK50-Moor web layer.\n*/\n\n(function () {\n  const DATA_URL = "public/data/bw_bk50_moor_simplified.geojson";\n  const WIDTH = 960;\n  const HEIGHT = 620;\n  const PADDING = 24;\n\n  function num(value) {\n    if (value === undefined || value === null || value === "") return null;\n    const n = Number(String(value).replace(",", "."));\n    return Number.isFinite(n) ? n : null;\n  }\n\n  function fmtArea(value) {\n    const n = num(value);\n    if (n === null) return "area not available";\n    const ha = n / 10000;\n    if (ha >= 1000) return `${(ha / 1000).toFixed(1)} kha`;\n    return `${ha.toFixed(1)} ha`;\n  }\n\n  function collectCoords(coords, out) {\n    if (!Array.isArray(coords)) return;\n    if (coords.length >= 2 && typeof coords[0] === "number" && typeof coords[1] === "number") {\n      out.push(coords);\n      return;\n    }\n    coords.forEach(item => collectCoords(item, out));\n  }\n\n  function bbox(features) {\n    const pts = [];\n    features.forEach(f => collectCoords(f.geometry?.coordinates, pts));\n    if (!pts.length) return null;\n    const xs = pts.map(p => p[0]);\n    const ys = pts.map(p => p[1]);\n    return { minX: Math.min(...xs), minY: Math.min(...ys), maxX: Math.max(...xs), maxY: Math.max(...ys) };\n  }\n\n  function makeProject(bounds) {\n    const dx = bounds.maxX - bounds.minX;\n    const dy = bounds.maxY - bounds.minY;\n    const sx = (WIDTH - PADDING * 2) / dx;\n    const sy = (HEIGHT - PADDING * 2) / dy;\n    const s = Math.min(sx, sy);\n    const usedW = dx * s;\n    const usedH = dy * s;\n    const ox = (WIDTH - usedW) / 2;\n    const oy = (HEIGHT - usedH) / 2;\n\n    return function project(coord) {\n      const x = ox + (coord[0] - bounds.minX) * s;\n      const y = HEIGHT - (oy + (coord[1] - bounds.minY) * s);\n      return [x, y];\n    };\n  }\n\n  function ringToPath(ring, project) {\n    if (!ring || !ring.length) return "";\n    return ring.map((coord, idx) => {\n      const [x, y] = project(coord);\n      return `${idx === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;\n    }).join(" ") + " Z";\n  }\n\n  function geometryToPath(geometry, project) {\n    if (!geometry) return "";\n    if (geometry.type === "Polygon") {\n      return geometry.coordinates.map(ring => ringToPath(ring, project)).join(" ");\n    }\n    if (geometry.type === "MultiPolygon") {\n      return geometry.coordinates.flatMap(poly => poly.map(ring => ringToPath(ring, project))).join(" ");\n    }\n    return "";\n  }\n\n  function classKey(value) {\n    return String(value || "Unclassified").trim() || "Unclassified";\n  }\n\n  function summarize(features) {\n    const counts = new Map();\n    let totalArea = 0;\n    features.forEach(f => {\n      const klass = classKey(f.properties?.class);\n      counts.set(klass, (counts.get(klass) || 0) + 1);\n      const area = num(f.properties?.source_area_m2);\n      if (area !== null) totalArea += area;\n    });\n    return { counts: [...counts.entries()].sort((a, b) => b[1] - a[1]), totalArea };\n  }\n\n  function typeIndexMap(counts) {\n    const map = new Map();\n    counts.forEach(([klass], idx) => map.set(klass, idx % 7));\n    return map;\n  }\n\n  function detailHTML(props) {\n    return `<strong>${props.class || "Unclassified"}</strong>\n      · ${props.soil || "soil class not available"}\n      · ${props.material || "material not available"}\n      · ${fmtArea(props.source_area_m2)}`;\n  }\n\n  function renderLegend(counts) {\n    const legend = document.querySelector("#bwMoorLegend");\n    if (!legend) return;\n    const top = counts.slice(0, 7);\n    legend.innerHTML = `\n      <div class="legend-title">BK50-Moor classes</div>\n      ${top.map(([klass, count], idx) => `\n        <span class="legend-item"><i class="bw-moor-type-${idx}"></i>${klass} <small>${count}</small></span>\n      `).join("")}\n    `;\n  }\n\n  function renderMetrics(features, summary) {\n    const countEl = document.querySelector("#bwMoorFeatureCount");\n    const classEl = document.querySelector("#bwMoorClassCount");\n    const areaEl = document.querySelector("#bwMoorArea");\n    if (countEl) countEl.textContent = features.length.toLocaleString("en-US");\n    if (classEl) classEl.textContent = summary.counts.length.toLocaleString("en-US");\n    if (areaEl) areaEl.textContent = fmtArea(summary.totalArea);\n  }\n\n  async function init() {\n    const container = document.querySelector("#bwMoorMap");\n    if (!container) return;\n    try {\n      const res = await fetch(DATA_URL);\n      if (!res.ok) throw new Error(`Failed to load ${DATA_URL}`);\n      const geo = await res.json();\n      const features = (geo.features || []).filter(f => f.geometry);\n      const bounds = bbox(features);\n      if (!features.length || !bounds) throw new Error("No displayable BK50-Moor features found.");\n\n      const project = makeProject(bounds);\n      const summary = summarize(features);\n      const idxMap = typeIndexMap(summary.counts);\n      renderMetrics(features, summary);\n      renderLegend(summary.counts);\n\n      const paths = features.map((feature, idx) => {\n        const props = feature.properties || {};\n        const klass = classKey(props.class);\n        const typeIdx = idxMap.get(klass) || 0;\n        const d = geometryToPath(feature.geometry, project);\n        return `<path d="${d}" class="bw-moor-feature bw-moor-type-${typeIdx}" data-idx="${idx}" tabindex="0" aria-label="${String(klass).replace(/"/g, "&quot;")}"></path>`;\n      }).join("");\n\n      container.innerHTML = `\n        <svg class="bw-moor-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">\n          <rect class="bw-moor-bg" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>\n          ${paths}\n        </svg>`;\n\n      const details = document.querySelector("#bwMoorDetails");\n      container.querySelectorAll(".bw-moor-feature").forEach(path => {\n        const feature = features[Number(path.dataset.idx)];\n        const props = feature.properties || {};\n        const show = () => {\n          container.querySelectorAll(".bw-moor-feature.active").forEach(el => el.classList.remove("active"));\n          path.classList.add("active");\n          if (details) details.innerHTML = detailHTML(props);\n        };\n        path.addEventListener("mouseenter", show);\n        path.addEventListener("focus", show);\n        path.addEventListener("click", show);\n      });\n      if (details) details.innerHTML = "Hover over a BK50-Moor polygon to inspect class, soil description and source area.";\n    } catch (err) {\n      container.innerHTML = `<div class="map-loading">Could not load BK50-Moor layer: ${err.message}</div>`;\n      console.error(err);\n    }\n  }\n\n  if (document.readyState === "loading") {\n    document.addEventListener("DOMContentLoaded", init);\n  } else {\n    init();\n  }\n})();\n'
CSS_APPEND = '\n/* B11c Baden-Württemberg BK50-Moor regional layer */\n.bw-moor-section { margin-top: 4rem; }\n.bw-moor-grid {\n  display: grid;\n  grid-template-columns: minmax(0, 1.15fr) minmax(280px, .85fr);\n  gap: 1.25rem;\n  align-items: start;\n}\n.bw-moor-map-card {\n  background: rgba(255,255,255,.035);\n  border: 1px solid rgba(255,255,255,.075);\n  border-radius: 1.15rem;\n  overflow: hidden;\n}\n.bw-moor-map { min-height: 420px; }\n.bw-moor-svg { display: block; width: 100%; height: auto; }\n.bw-moor-bg { fill: rgba(18, 27, 24, .95); }\n.bw-moor-feature {\n  stroke: rgba(18,27,24,.88);\n  stroke-width: .28;\n  opacity: .82;\n  cursor: pointer;\n  transition: opacity .12s ease, filter .12s ease, stroke-width .12s ease;\n}\n.bw-moor-feature:hover,\n.bw-moor-feature:focus,\n.bw-moor-feature.active {\n  opacity: 1;\n  stroke: rgba(238,225,170,.95);\n  stroke-width: 1.2;\n  filter: drop-shadow(0 0 5px rgba(212,196,118,.36));\n  outline: none;\n}\n.bw-moor-type-0 { fill: rgba(75, 120, 96, .68); }\n.bw-moor-type-1 { fill: rgba(108, 141, 101, .68); }\n.bw-moor-type-2 { fill: rgba(139, 124, 87, .72); }\n.bw-moor-type-3 { fill: rgba(92, 111, 132, .68); }\n.bw-moor-type-4 { fill: rgba(159, 128, 96, .72); }\n.bw-moor-type-5 { fill: rgba(119, 103, 139, .68); }\n.bw-moor-type-6 { fill: rgba(149, 158, 111, .68); }\n.legend-item i.bw-moor-type-0 { background: rgba(75, 120, 96, .68); }\n.legend-item i.bw-moor-type-1 { background: rgba(108, 141, 101, .68); }\n.legend-item i.bw-moor-type-2 { background: rgba(139, 124, 87, .72); }\n.legend-item i.bw-moor-type-3 { background: rgba(92, 111, 132, .68); }\n.legend-item i.bw-moor-type-4 { background: rgba(159, 128, 96, .72); }\n.legend-item i.bw-moor-type-5 { background: rgba(119, 103, 139, .68); }\n.legend-item i.bw-moor-type-6 { background: rgba(149, 158, 111, .68); }\n.bw-moor-side { display: grid; gap: 1rem; }\n.bw-moor-detail {\n  border: 1px solid rgba(212,196,118,.20);\n  border-radius: .9rem;\n  padding: .85rem;\n  background: rgba(212,196,118,.045);\n  color: var(--text);\n}\n@media (max-width: 900px) {\n  .bw-moor-grid { grid-template-columns: 1fr; }\n  .bw-moor-map { min-height: 320px; }\n}\n'
SECTION_HTML = '\n<section id="bwPeatLayer" class="section bw-moor-section">\n  <div class="section-kicker">Regional peat/organic-soils layer</div>\n  <h2>Baden-Württemberg: where the peat and organic-soil context becomes spatial</h2>\n  <p class="section-lead">\n    The country hotspot map shows national emissions. The regional layer below shifts the question:\n    where are moor, moor-like and humus-rich groundwater soils actually located within Baden-Württemberg?\n  </p>\n\n  <div class="metric-row">\n    <div class="metric-card">\n      <span class="metric-label">BK50-Moor features</span>\n      <strong id="bwMoorFeatureCount">—</strong>\n    </div>\n    <div class="metric-card">\n      <span class="metric-label">Classes</span>\n      <strong id="bwMoorClassCount">—</strong>\n    </div>\n    <div class="metric-card">\n      <span class="metric-label">Source area sum</span>\n      <strong id="bwMoorArea">—</strong>\n    </div>\n  </div>\n\n  <div class="bw-moor-grid">\n    <div class="bw-moor-map-card">\n      <div id="bwMoorMap" class="bw-moor-map">\n        <div class="map-loading">Loading Baden-Württemberg BK50-Moor layer…</div>\n      </div>\n    </div>\n\n    <aside class="bw-moor-side">\n      <div class="detail-card">\n        <p class="eyebrow">Why this layer matters</p>\n        <h3>From national hotspots to real landscapes</h3>\n        <p>\n          This regional layer is a first spatial bridge from national drained-organic-soils emissions\n          to the actual distribution of moor and organic-soil contexts in Baden-Württemberg.\n        </p>\n        <p class="caveat">\n          Interpretation boundary: this is a medium-scale soil-context layer, not a local rewetting\n          suitability map or parcel-level planning instrument.\n        </p>\n      </div>\n\n      <div id="bwMoorLegend" class="map-legend"></div>\n      <div id="bwMoorDetails" class="bw-moor-detail"></div>\n    </aside>\n  </div>\n</section>\n'
METHOD = '# B11c — Baden-Württemberg BK50-Moor Preview Map\n\nDate: 2026-06-18\n\n## Purpose\n\nAdd the first regional peat/organic-soils spatial layer to the public atlas.\n\n## Input\n\n`public/data/bw_bk50_moor_simplified.geojson`\n\n## Added interface\n\nThe new section `#bwPeatLayer` shows:\n\n- a simplified BK50-Moor SVG map,\n- feature count,\n- class count,\n- source area sum,\n- class legend,\n- hover/click detail display,\n- interpretation caveat.\n\n## Interpretation boundary\n\nThe map shows a regional medium-scale soil-context layer for Baden-Württemberg. It is not a local rewetting suitability map and should not be interpreted as parcel-level planning guidance.\n\n## Technical approach\n\n- no external mapping library,\n- no build system,\n- automatic bounding-box fitting,\n- SVG polygon rendering,\n- class-based color assignment from `properties.class`.\n\n## Next step\n\nUse this regional layer as the final zoom target in the planned sticky-scroll story.\n'
TASK = '# Task B12 — Sticky Scroll Scaffold\n\n## Agent\n\nVisualization Engineer Agent + Story Editor Agent + QA Critic Agent\n\n## Goal\n\nCreate the first guided sticky-scroll scaffold without removing the existing explorer sections.\n\n## Proposed structure\n\n1. World country emissions\n2. Global peat/organic-soils context\n3. Europe wetland/peat context\n4. Germany organic-soils bridge\n5. Baden-Württemberg BK50-Moor zoom\n6. Interpretation boundary\n\n## First technical step\n\nAdd a new `#guidedStory` section before the explorer layers:\n\n- left or right sticky visual container,\n- 5–6 text steps,\n- IntersectionObserver to set active step,\n- no complex animations yet.\n\n## Acceptance criteria\n\n- existing explorer sections remain available,\n- sticky section is readable on desktop,\n- mobile fallback is simple and non-sticky,\n- no heavy dependency is introduced.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    root = Path.cwd()
    index = root / "index.html"
    data = root / "public" / "data" / "bw_bk50_moor_simplified.geojson"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not data.exists():
        raise SystemExit("public/data/bw_bk50_moor_simplified.geojson not found. Run B11b first.")

    write(root / "src" / "bw_peat_layer.js", BW_JS)

    html = read(index)
    if 'id="bwPeatLayer"' not in html:
        if "</main>" in html:
            html = html.replace("</main>", SECTION_HTML + "\n</main>")
        else:
            raise SystemExit("Could not find </main> insertion point in index.html.")

    if 'src="src/bw_peat_layer.js"' not in html:
        marker = '<script src="src/hotspot_base_layer.js"></script>'
        if marker in html:
            html = html.replace(marker, marker + '\n  <script src="src/bw_peat_layer.js"></script>')
        elif "</body>" in html:
            html = html.replace("</body>", '  <script src="src/bw_peat_layer.js"></script>\n</body>')
        else:
            raise SystemExit("Could not insert bw_peat_layer.js script tag.")
    write(index, html)

    styles = root / "src" / "styles.css"
    css = read(styles)
    if "B11c Baden-Württemberg BK50-Moor regional layer" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B11c_bw_bk50_moor_preview_map.md", METHOD)
    write(root / "tasks" / "B12_sticky_scroll_scaffold.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B11c completed" not in done_text:
        done_text += f"- {TODAY}: Task B11c completed — added Baden-Württemberg BK50-Moor preview map to the public atlas.\n"
        write(done, done_text)

    print("B11c BW BK50-Moor preview map added.")
    print("Changed/created:")
    print("  index.html")
    print("  src/bw_peat_layer.js")
    print("  src/styles.css")
    print("  docs/B11c_bw_bk50_moor_preview_map.md")
    print("  tasks/B12_sticky_scroll_scaffold.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")

if __name__ == "__main__":
    main()
