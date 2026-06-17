#!/usr/bin/env python3
r"""
B5 — Add a simple dependency-free choropleth map to the hotspot section.

Run from repository root:

  python scripts\06_add_hotspot_choropleth_map.py

Inputs expected:
  public/data/hotspot_countries_110m.geojson
  src/hotspots.js
  index.html
  src/styles.css

Outputs/changes:
  index.html
  src/hotspots.js
  src/styles.css
  docs/B5_choropleth_map_method.md
  tasks/B6_interaction_and_layout_refinement.md

No external JavaScript libraries; static GitHub Pages compatible.
"""

from __future__ import annotations

from pathlib import Path
import datetime


TODAY = datetime.date.today().isoformat()


MAP_PANEL = r"""
        <article class="detail-card hotspot-map-card">
          <p class="eyebrow">Map layer</p>
          <h3>Country-level hotspot map</h3>
          <div id="hotspotMap" class="hotspot-map" aria-label="Country-level hotspot choropleth map">
            <div class="map-loading">Loading country hotspot map…</div>
          </div>
          <div id="hotspotMapLegend" class="hotspot-map-legend"></div>
          <p id="hotspotMapDetails" class="hotspot-map-details">
            Hover or click a country to inspect total emissions, emissions density and drained organic soils area.
          </p>
        </article>
"""


JS_APPEND = r"""
/*
B5 choropleth map layer.
Dependency-free SVG renderer for public/data/hotspot_countries_110m.geojson.
*/

(function () {
  const GEOJSON_URL = "public/data/hotspot_countries_110m.geojson";
  const WIDTH = 960;
  const HEIGHT = 500;

  function num(value) {
    if (value === undefined || value === null || value === "") return null;
    const n = Number(String(value).replace(",", "."));
    return Number.isFinite(n) ? n : null;
  }

  function fmtKt(value) {
    const n = num(value);
    if (n === null) return "no data";
    if (n >= 1000) return `${(n / 1000).toFixed(1)} Mt CO₂e`;
    return `${Math.round(n)} kt CO₂e`;
  }

  function fmtHa(value) {
    const n = num(value);
    if (n === null) return "no data";
    if (n >= 1000000) return `${(n / 1000000).toFixed(1)} Mha`;
    if (n >= 1000) return `${Math.round(n / 1000)} kha`;
    return `${Math.round(n)} ha`;
  }

  function fmtDensity(value) {
    const n = num(value);
    if (n === null) return "no data";
    return `${n.toFixed(1)} t CO₂e/ha`;
  }

  function project(coord) {
    const lon = coord[0];
    const lat = coord[1];
    const x = ((lon + 180) / 360) * WIDTH;
    const y = ((90 - lat) / 180) * HEIGHT;
    return [x, y];
  }

  function ringToPath(ring) {
    if (!ring || !ring.length) return "";
    return ring.map((coord, idx) => {
      const [x, y] = project(coord);
      return `${idx === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;
    }).join(" ") + " Z";
  }

  function geometryToPath(geometry) {
    if (!geometry) return "";
    if (geometry.type === "Polygon") {
      return geometry.coordinates.map(ringToPath).join(" ");
    }
    if (geometry.type === "MultiPolygon") {
      return geometry.coordinates.flatMap(poly => poly.map(ringToPath)).join(" ");
    }
    return "";
  }

  function quantileBreaks(values) {
    const sorted = [...values].filter(v => Number.isFinite(v)).sort((a, b) => a - b);
    if (!sorted.length) return [];
    function q(p) {
      const idx = Math.max(0, Math.min(sorted.length - 1, Math.round((sorted.length - 1) * p)));
      return sorted[idx];
    }
    return [q(0.2), q(0.4), q(0.6), q(0.8)];
  }

  function classForValue(value, breaks) {
    const v = num(value);
    if (v === null || !breaks.length) return "map-fill-no-data";
    if (v <= breaks[0]) return "map-fill-1";
    if (v <= breaks[1]) return "map-fill-2";
    if (v <= breaks[2]) return "map-fill-3";
    if (v <= breaks[3]) return "map-fill-4";
    return "map-fill-5";
  }

  function legendHTML(breaks) {
    if (!breaks.length) return "";
    const labels = [
      `≤ ${fmtKt(breaks[0])}`,
      `${fmtKt(breaks[0])}–${fmtKt(breaks[1])}`,
      `${fmtKt(breaks[1])}–${fmtKt(breaks[2])}`,
      `${fmtKt(breaks[2])}–${fmtKt(breaks[3])}`,
      `> ${fmtKt(breaks[3])}`
    ];
    return `
      <div class="legend-title">Total emissions</div>
      ${labels.map((label, idx) => `
        <span class="legend-item"><i class="map-fill-${idx + 1}"></i>${label}</span>
      `).join("")}
    `;
  }

  function detailHTML(props) {
    return `
      <strong>${props.country}</strong>
      · total ${fmtKt(props.emissions_total_kt_co2e)}
      · density ${fmtDensity(props.emissions_density_t_co2e_per_ha)}
      · area ${fmtHa(props.drained_organic_soils_area_ha)}
    `;
  }

  async function renderMap() {
    const map = document.querySelector("#hotspotMap");
    if (!map) return;

    const details = document.querySelector("#hotspotMapDetails");
    const legend = document.querySelector("#hotspotMapLegend");

    try {
      const res = await fetch(GEOJSON_URL);
      if (!res.ok) throw new Error(`Failed to load ${GEOJSON_URL}`);
      const geo = await res.json();

      const features = (geo.features || []).filter(f => f.geometry);
      const values = features.map(f => num(f.properties?.emissions_total_kt_co2e)).filter(v => v !== null);
      const breaks = quantileBreaks(values);

      if (legend) legend.innerHTML = legendHTML(breaks);

      const paths = features.map((feature, idx) => {
        const props = feature.properties || {};
        const d = geometryToPath(feature.geometry);
        const fillClass = classForValue(props.emissions_total_kt_co2e, breaks);
        const label = `${props.country}: ${fmtKt(props.emissions_total_kt_co2e)}`;
        return `<path
          d="${d}"
          class="hotspot-country ${fillClass}"
          data-idx="${idx}"
          tabindex="0"
          role="img"
          aria-label="${label.replace(/"/g, "&quot;")}"
        ></path>`;
      }).join("");

      map.innerHTML = `
        <svg class="hotspot-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
          <rect class="map-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
          ${paths}
        </svg>
      `;

      map.querySelectorAll(".hotspot-country").forEach(path => {
        const feature = features[Number(path.dataset.idx)];
        const props = feature.properties || {};

        const show = () => {
          map.querySelectorAll(".hotspot-country.active").forEach(el => el.classList.remove("active"));
          path.classList.add("active");
          if (details) details.innerHTML = detailHTML(props);
        };

        path.addEventListener("mouseenter", show);
        path.addEventListener("focus", show);
        path.addEventListener("click", show);
      });
    } catch (err) {
      map.innerHTML = `
        <div class="map-loading">
          Could not load choropleth data: ${err.message}
        </div>
      `;
      console.error(err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderMap);
  } else {
    renderMap();
  }
})();
"""


CSS_APPEND = r"""
/* B5 choropleth map */
.hotspot-map-card {
  grid-column: 1 / -1;
}

.hotspot-map {
  position: relative;
  width: 100%;
  min-height: 22rem;
  border: 1px solid var(--line);
  border-radius: 1rem;
  overflow: hidden;
  background: rgba(255,255,255,.025);
}

.hotspot-svg {
  display: block;
  width: 100%;
  height: auto;
}

.map-ocean {
  fill: rgba(255,255,255,.025);
}

.hotspot-country {
  stroke: rgba(13, 22, 20, .95);
  stroke-width: .55;
  cursor: pointer;
  transition: opacity .15s ease, stroke-width .15s ease;
}

.hotspot-country:hover,
.hotspot-country:focus,
.hotspot-country.active {
  opacity: 1;
  stroke: var(--accent);
  stroke-width: 1.2;
  outline: none;
}

.hotspot-country:not(:hover) {
  opacity: .9;
}

.map-fill-no-data { fill: rgba(255,255,255,.08); }
.map-fill-1 { fill: rgba(121,183,168,.22); }
.map-fill-2 { fill: rgba(121,183,168,.38); }
.map-fill-3 { fill: rgba(182,211,124,.50); }
.map-fill-4 { fill: rgba(233,186,102,.68); }
.map-fill-5 { fill: rgba(239,126,89,.82); }

.hotspot-map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: .65rem .9rem;
  align-items: center;
  color: var(--muted);
  font-size: .82rem;
  margin-top: .75rem;
}

.legend-title {
  color: var(--text);
  font-weight: 700;
  margin-right: .2rem;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
}

.legend-item i {
  display: inline-block;
  width: .9rem;
  height: .9rem;
  border: 1px solid rgba(255,255,255,.18);
  border-radius: .2rem;
}

.hotspot-map-details {
  color: var(--muted);
  font-size: .92rem;
  margin-top: .8rem;
}

.map-loading {
  color: var(--muted);
  padding: 1rem;
}
"""


METHOD = f"""# B5 — Choropleth Map Layer

Date: {TODAY}

## Status

Adds a first dependency-free country-level choropleth map to the hotspot section.

## Input

`public/data/hotspot_countries_110m.geojson`

## Rendering approach

- SVG map
- no external JavaScript map library
- equirectangular projection
- quantile color classes based on `emissions_total_kt_co2e`
- hover/click details for:
  - total emissions,
  - emissions density,
  - drained organic soils area.

## Why this simple map first?

This is a portfolio MVP. The aim is to make the hotspot layer visible on the public site without adding a build system or complex web-mapping dependency.

## Caveat

The layer is national-level only. It does not show local rewetting suitability, hydrological feasibility, land tenure or farm-scale transition constraints.

## Next step

B6 — interaction and layout refinement.
"""


TASK_B6 = """# Task B6 — Interaction and Layout Refinement

## Agent

Visualization Engineer Agent + QA Critic Agent

## Goal

Improve the hotspot section after the first choropleth map is visible.

## Candidate improvements

- map tooltip positioning,
- better mobile layout,
- ranking/map linking,
- option to switch total emissions vs emissions density,
- clearer no-data treatment,
- reduce visual clutter around the sticky navigation/header.

## Acceptance criteria

- keep the site static and lightweight,
- do not introduce a build framework,
- preserve caveats about country-level interpretation,
- live GitHub Pages version remains functional.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    root = Path.cwd()
    index = root / "index.html"
    styles = root / "src" / "styles.css"
    hotspots_js = root / "src" / "hotspots.js"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not hotspots_js.exists():
        raise SystemExit("src/hotspots.js not found. Run B3 first.")
    if not (root / "public" / "data" / "hotspot_countries_110m.geojson").exists():
        raise SystemExit("public/data/hotspot_countries_110m.geojson not found. Run B4 first.")

    html = read(index)
    if 'id="hotspotMap"' not in html:
        marker = '        <div class="hotspot-grid">'
        if marker not in html:
            raise SystemExit("Could not find hotspot-grid marker in index.html.")
        html = html.replace(marker, '        <div class="hotspot-grid">\n' + MAP_PANEL)
        write(index, html)

    js = read(hotspots_js)
    if "B5 choropleth map layer" not in js:
        write(hotspots_js, js + "\n\n" + JS_APPEND)

    css = read(styles)
    if "B5 choropleth map" not in css:
        write(styles, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B5_choropleth_map_method.md", METHOD)
    write(root / "tasks" / "B6_interaction_and_layout_refinement.md", TASK_B6)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B5 completed" not in done_text:
        done_text += f"- {TODAY}: Task B5 completed — dependency-free choropleth map added to hotspot section.\n"
        write(done, done_text)

    print("B5 choropleth map patch applied.")
    print("Changed/created:")
    print("  index.html")
    print("  src/hotspots.js")
    print("  src/styles.css")
    print("  docs/B5_choropleth_map_method.md")
    print("  tasks/B6_interaction_and_layout_refinement.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")


if __name__ == "__main__":
    main()
