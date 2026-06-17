
/*
B3 hotspot ranking layer.

This file is independent from app.js on purpose.
It reads public/data/country_hotspots.csv and renders a compact ranking layer.
*/

(function () {
  const HOTSPOT_DATA_URL = "public/data/country_hotspots.csv";

  function parseCSV(text) {
    const rows = [];
    const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(line => line.trim() !== "");
    if (!lines.length) return rows;

    const delimiter = lines[0].includes(";") && !lines[0].includes(",") ? ";" : ",";
    const header = splitLine(lines[0], delimiter).map(h => h.trim());

    for (let i = 1; i < lines.length; i++) {
      const values = splitLine(lines[i], delimiter);
      const row = {};
      header.forEach((h, idx) => row[h] = (values[idx] || "").trim());
      rows.push(row);
    }
    return rows;
  }

  function splitLine(line, delimiter) {
    const out = [];
    let cur = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const ch = line[i];

      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === delimiter && !inQuotes) {
        out.push(cur);
        cur = "";
      } else {
        cur += ch;
      }
    }
    out.push(cur);
    return out;
  }

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

  function completeRows(rows) {
    return rows.filter(r => num(r.emissions_total_kt_co2e) !== null);
  }

  function topBy(rows, field, n = 10) {
    return [...rows]
      .filter(r => num(r[field]) !== null)
      .sort((a, b) => num(b[field]) - num(a[field]))
      .slice(0, n);
  }

  function barWidth(value, max) {
    const n = num(value);
    if (n === null || !max) return 0;
    return Math.max(2, Math.min(100, (n / max) * 100));
  }

  function renderRanking(container, rows, field, label, formatter) {
    const top = topBy(rows, field, 10);
    const max = top.length ? num(top[0][field]) : 0;

    container.innerHTML = top.map((r, idx) => `
      <article class="hotspot-row">
        <div class="hotspot-rank">${idx + 1}</div>
        <div class="hotspot-main">
          <div class="hotspot-row-head">
            <strong>${r.country}</strong>
            <span>${formatter(r[field])}</span>
          </div>
          <div class="hotspot-bar-wrap" aria-label="${label}">
            <div class="hotspot-bar" style="width:${barWidth(r[field], max)}%"></div>
          </div>
          <p>
            Area: ${fmtHa(r.drained_organic_soils_area_ha)}
            · CO₂: ${fmtKt(r.co2_kt_co2)}
            · N₂O: ${fmtKt(r.n2o_ar5_kt_co2e)}
          </p>
        </div>
      </article>
    `).join("");
  }

  async function renderHotspots() {
    const root = document.querySelector("#hotspotLayer");
    if (!root) return;

    try {
      const res = await fetch(HOTSPOT_DATA_URL);
      if (!res.ok) throw new Error(`Failed to load ${HOTSPOT_DATA_URL}`);
      const rows = parseCSV(await res.text());
      const complete = completeRows(rows);

      const total = document.querySelector("#hotspotMetricCountries");
      const year = document.querySelector("#hotspotMetricYear");
      const emissions = document.querySelector("#hotspotMetricEmissions");

      if (total) total.textContent = complete.length;
      if (year) year.textContent = complete[0]?.year || "—";
      if (emissions) {
        const sum = complete.reduce((acc, r) => acc + (num(r.emissions_total_kt_co2e) || 0), 0);
        emissions.textContent = `${(sum / 1000).toFixed(1)} Mt CO₂e`;
      }

      const totalEl = document.querySelector("#hotspotRankingTotal");
      const densityEl = document.querySelector("#hotspotRankingDensity");

      if (totalEl) renderRanking(totalEl, complete, "emissions_total_kt_co2e", "Total emissions", fmtKt);
      if (densityEl) renderRanking(densityEl, complete, "emissions_density_t_co2e_per_ha", "Emissions density", fmtDensity);

      root.classList.remove("loading");
    } catch (err) {
      root.innerHTML = `
        <div class="detail-card">
          <p class="eyebrow">Hotspot layer</p>
          <h3>Could not load hotspot data</h3>
          <p>${err.message}</p>
        </div>
      `;
      console.error(err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderHotspots);
  } else {
    renderHotspots();
  }
})();



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
