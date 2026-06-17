#!/usr/bin/env python3
r"""
B6b — Toggle total emissions vs emissions density on the hotspot choropleth.

Run from repository root:

  python scripts\08_add_hotspot_metric_toggle.py

Purpose:
- add a map metric toggle:
  [Total emissions] [Emissions density]
- recolor the SVG choropleth based on selected metric,
- update the legend and hover/click details,
- keep everything static and dependency-free.

Inputs expected:
  index.html
  src/hotspots.js
  src/styles.css
  public/data/hotspot_countries_110m.geojson
"""

from pathlib import Path
import datetime


TODAY = datetime.date.today().isoformat()


TOGGLE_HTML = r"""
          <div id="hotspotMapToggle" class="hotspot-toggle" role="group" aria-label="Map metric">
            <button type="button" class="hotspot-toggle-btn active" data-map-metric="emissions_total_kt_co2e">
              Total emissions
            </button>
            <button type="button" class="hotspot-toggle-btn" data-map-metric="emissions_density_t_co2e_per_ha">
              Emissions density
            </button>
          </div>
"""


B6B_JS = r"""
/*
B6b choropleth metric toggle.
Dependency-free SVG renderer for public/data/hotspot_countries_110m.geojson.
Allows switching between total emissions and emissions density.
*/

(function () {
  const GEOJSON_URL = "public/data/hotspot_countries_110m.geojson";
  const WIDTH = 960;
  const HEIGHT = 500;

  const METRICS = {
    emissions_total_kt_co2e: {
      label: "Total emissions",
      legendLabel: "Total emissions",
      formatter: fmtKt,
      classPrefix: "total"
    },
    emissions_density_t_co2e_per_ha: {
      label: "Emissions density",
      legendLabel: "Emissions density",
      formatter: fmtDensity,
      classPrefix: "density"
    }
  };

  let geoFeatures = [];
  let activeMetric = "emissions_total_kt_co2e";

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

  function legendHTML(metricConfig, breaks) {
    if (!breaks.length) return "";

    const f = metricConfig.formatter;
    const labels = [
      `≤ ${f(breaks[0])}`,
      `${f(breaks[0])}–${f(breaks[1])}`,
      `${f(breaks[1])}–${f(breaks[2])}`,
      `${f(breaks[2])}–${f(breaks[3])}`,
      `> ${f(breaks[3])}`
    ];

    return `
      <div class="legend-title">${metricConfig.legendLabel}</div>
      ${labels.map((label, idx) => `
        <span class="legend-item"><i class="map-fill-${idx + 1}"></i>${label}</span>
      `).join("")}
    `;
  }

  function detailHTML(props, metricKey) {
    const metricConfig = METRICS[metricKey] || METRICS.emissions_total_kt_co2e;
    const metricValue = metricConfig.formatter(props[metricKey]);

    return `
      <strong>${props.country}</strong>
      · ${metricConfig.label}: ${metricValue}
      · total ${fmtKt(props.emissions_total_kt_co2e)}
      · density ${fmtDensity(props.emissions_density_t_co2e_per_ha)}
      · area ${fmtHa(props.drained_organic_soils_area_ha)}
    `;
  }

  function renderMap(metricKey) {
    const map = document.querySelector("#hotspotMap");
    if (!map) return;

    const details = document.querySelector("#hotspotMapDetails");
    const legend = document.querySelector("#hotspotMapLegend");
    const metricConfig = METRICS[metricKey] || METRICS.emissions_total_kt_co2e;

    const values = geoFeatures
      .map(f => num(f.properties?.[metricKey]))
      .filter(v => v !== null);

    const breaks = quantileBreaks(values);

    if (legend) legend.innerHTML = legendHTML(metricConfig, breaks);

    const paths = geoFeatures.map((feature, idx) => {
      const props = feature.properties || {};
      const d = geometryToPath(feature.geometry);
      const fillClass = classForValue(props[metricKey], breaks);
      const label = `${props.country}: ${metricConfig.formatter(props[metricKey])}`;

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
      const feature = geoFeatures[Number(path.dataset.idx)];
      const props = feature.properties || {};

      const show = () => {
        map.querySelectorAll(".hotspot-country.active").forEach(el => el.classList.remove("active"));
        path.classList.add("active");
        if (details) details.innerHTML = detailHTML(props, metricKey);
      };

      path.addEventListener("mouseenter", show);
      path.addEventListener("focus", show);
      path.addEventListener("click", show);
    });
  }

  function updateToggleState(metricKey) {
    document.querySelectorAll("[data-map-metric]").forEach(button => {
      const isActive = button.dataset.mapMetric === metricKey;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  async function initMap() {
    const map = document.querySelector("#hotspotMap");
    if (!map) return;

    try {
      const res = await fetch(GEOJSON_URL);
      if (!res.ok) throw new Error(`Failed to load ${GEOJSON_URL}`);
      const geo = await res.json();
      geoFeatures = (geo.features || []).filter(f => f.geometry);

      document.querySelectorAll("[data-map-metric]").forEach(button => {
        button.addEventListener("click", () => {
          activeMetric = button.dataset.mapMetric || "emissions_total_kt_co2e";
          updateToggleState(activeMetric);
          renderMap(activeMetric);
        });
      });

      updateToggleState(activeMetric);
      renderMap(activeMetric);
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
    document.addEventListener("DOMContentLoaded", initMap);
  } else {
    initMap();
  }
})();
"""


CSS_APPEND = r"""
/* B6b hotspot metric toggle */
.hotspot-toggle {
  display: inline-flex;
  flex-wrap: wrap;
  gap: .5rem;
  padding: .35rem;
  margin: .35rem 0 .85rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255,255,255,.035);
}

.hotspot-toggle-btn {
  border: 1px solid transparent;
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  padding: .48rem .78rem;
  cursor: pointer;
  font: inherit;
  font-size: .82rem;
  font-weight: 700;
  transition: background .15s ease, color .15s ease, border-color .15s ease;
}

.hotspot-toggle-btn:hover,
.hotspot-toggle-btn:focus {
  color: var(--text);
  border-color: var(--line);
  outline: none;
}

.hotspot-toggle-btn.active {
  color: var(--bg);
  background: var(--accent);
  border-color: var(--accent);
}

@media (max-width: 520px) {
  .hotspot-toggle {
    border-radius: 1rem;
    width: 100%;
  }

  .hotspot-toggle-btn {
    flex: 1 1 100%;
  }
}
"""


METHOD = f"""# B6b — Toggle Total Emissions vs Emissions Density

Date: {TODAY}

## Status

Adds a metric toggle to the hotspot choropleth map.

## Available map modes

1. `Total emissions`
   - field: `emissions_total_kt_co2e`
   - shows national-scale hotspot magnitude

2. `Emissions density`
   - field: `emissions_density_t_co2e_per_ha`
   - shows intensity per hectare of drained organic soils

## Why this matters

Total emissions highlight large national hotspots.  
Emissions density highlights where drained organic soils are especially emission-intensive per unit area.

Together, the two views prevent the map from implying that the largest national emitters are always the most intensive land-use systems.

## Technical approach

- no external map library,
- no build system,
- reuses `public/data/hotspot_countries_110m.geojson`,
- recolors the SVG choropleth by quantiles for the selected metric,
- updates legend and hover/click details.

## Caveat

Both modes remain national-level summaries. Neither mode shows local hydrological feasibility, farm-scale land-use transition potential or rewetting suitability.
"""


TASK = """# Task B6c — Link Rankings and Map Interaction

## Agent

Visualization Engineer Agent + QA Critic Agent

## Goal

Make the hotspot map and rankings feel connected.

## Candidate interactions

- hovering a ranking row highlights the same country on the map,
- clicking a country scrolls/marks its ranking position where available,
- add a small details panel with rank, total emissions, density and area,
- clarify that unmatched territories are excluded from the map.

## Acceptance criteria

- no build system,
- no heavy map library,
- current static GitHub Pages deployment remains functional,
- country-level caveat remains visible.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    root = Path.cwd()
    index = root / "index.html"
    js_path = root / "src" / "hotspots.js"
    css_path = root / "src" / "styles.css"

    if not index.exists():
        raise SystemExit("Run from repository root. index.html not found.")
    if not js_path.exists():
        raise SystemExit("src/hotspots.js not found.")
    if not css_path.exists():
        raise SystemExit("src/styles.css not found.")
    if not (root / "public" / "data" / "hotspot_countries_110m.geojson").exists():
        raise SystemExit("public/data/hotspot_countries_110m.geojson not found. Run/commit B4 first.")

    html = read(index)
    if 'id="hotspotMapToggle"' not in html:
        marker = '          <div id="hotspotMap" class="hotspot-map" aria-label="Country-level hotspot choropleth map">'
        if marker not in html:
            raise SystemExit("Could not find hotspot map marker in index.html.")
        html = html.replace(marker, TOGGLE_HTML + "\n" + marker)
        write(index, html)

    js = read(js_path)
    b5_marker = "/*\nB5 choropleth map layer."
    b6_marker = "/*\nB6b choropleth metric toggle."
    if b6_marker not in js:
        if b5_marker in js:
            js = js[:js.index(b5_marker)].rstrip() + "\n\n" + B6B_JS
        else:
            js = js.rstrip() + "\n\n" + B6B_JS
        write(js_path, js)

    css = read(css_path)
    if "B6b hotspot metric toggle" not in css:
        write(css_path, css + "\n" + CSS_APPEND)

    write(root / "docs" / "B6b_hotspot_metric_toggle.md", METHOD)
    write(root / "tasks" / "B6c_link_rankings_and_map.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B6b completed" not in done_text:
        done_text += f"- {TODAY}: Task B6b completed — added total emissions vs emissions density toggle to hotspot map.\n"
        write(done, done_text)

    print("B6b metric toggle applied.")
    print("Changed/created:")
    print("  index.html")
    print("  src/hotspots.js")
    print("  src/styles.css")
    print("  docs/B6b_hotspot_metric_toggle.md")
    print("  tasks/B6c_link_rankings_and_map.md")
    print("  tasks/done.md")
    print()
    print("Local test:")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000")
    print("  hard reload with Ctrl+F5")


if __name__ == "__main__":
    main()
