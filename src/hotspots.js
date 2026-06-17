/*
Hotspot module: rankings, choropleth map, metric toggle and ranking-map linking.
Static GitHub Pages compatible. No external dependencies.
*/

(function () {
  const HOTSPOT_DATA_URL = "public/data/country_hotspots.csv";
  const GEOJSON_URL = "public/data/hotspot_countries_110m.geojson";
  const WIDTH = 960;
  const HEIGHT = 500;

  const METRICS = {
    emissions_total_kt_co2e: {
      label: "Total emissions",
      legendLabel: "Total emissions",
      formatter: fmtKt
    },
    emissions_density_t_co2e_per_ha: {
      label: "Emissions density",
      legendLabel: "Emissions density",
      formatter: fmtDensity
    }
  };

  let activeMetric = "emissions_total_kt_co2e";
  let geoFeatures = [];
  let activeCountryKey = "";

  function countryKey(value) {
    return String(value || "")
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/&/g, "and")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function escapeAttr(value) {
    return String(value || "").replace(/"/g, "&quot;");
  }

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

    container.innerHTML = top.map((r, idx) => {
      const key = countryKey(r.country);
      return `
        <article class="hotspot-row" data-country-key="${escapeAttr(key)}" tabindex="0">
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
      `;
    }).join("");
  }

  function project(coord) {
    /*
    Robinson-style pseudo-projection using the standard 5-degree coefficient table.
    This is not a GIS-grade reprojection step; it is a lightweight visual projection
    for the static SVG prototype.
    */
    const lon = Math.max(-180, Math.min(180, Number(coord[0]) || 0));
    const lat = Math.max(-90, Math.min(90, Number(coord[1]) || 0));
    const absLat = Math.abs(lat);

    const X = [
      1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730, 0.9600,
      0.9427, 0.9216, 0.8962, 0.8679, 0.8350, 0.7986, 0.7597,
      0.7186, 0.6732, 0.6213, 0.5722, 0.5322
    ];

    const Y = [
      0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100, 0.3720,
      0.4340, 0.4958, 0.5571, 0.6176, 0.6769, 0.7346, 0.7903,
      0.8435, 0.8936, 0.9394, 0.9761, 1.0000
    ];

    const i = Math.min(17, Math.floor(absLat / 5));
    const t = (absLat - i * 5) / 5;

    const xCoef = X[i] + (X[i + 1] - X[i]) * t;
    const yCoef = Y[i] + (Y[i + 1] - Y[i]) * t;

    const lonRad = lon * Math.PI / 180;
    const sign = lat < 0 ? -1 : 1;

    const rawX = 0.8487 * xCoef * lonRad;
    const rawY = 1.3523 * yCoef * sign;

    const maxX = 0.8487 * Math.PI;
    const maxY = 1.3523;

    const x = (0.5 + rawX / (2 * maxX)) * WIDTH;
    const y = (0.5 - rawY / (2 * maxY)) * HEIGHT;

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


  function geometryCentroid(geometry) {
    const points = [];

    function collectRing(ring) {
      if (!ring) return;
      ring.forEach(coord => {
        const projected = project(coord);
        points.push(projected);
      });
    }

    if (!geometry) return null;

    if (geometry.type === "Polygon") {
      geometry.coordinates.forEach(collectRing);
    } else if (geometry.type === "MultiPolygon") {
      geometry.coordinates.forEach(poly => poly.forEach(collectRing));
    }

    if (!points.length) return null;

    const x = points.reduce((sum, p) => sum + p[0], 0) / points.length;
    const y = points.reduce((sum, p) => sum + p[1], 0) / points.length;

    return [x, y];
  }

  function addActiveMarker(feature) {
    const svg = document.querySelector("#hotspotMap svg");
    if (!svg || !feature || !feature.geometry) return;

    svg.querySelectorAll(".hotspot-active-marker, .hotspot-active-marker-ring, .hotspot-active-label").forEach(el => el.remove());

    const centroid = geometryCentroid(feature.geometry);
    if (!centroid) return;

    const props = feature.properties || {};
    const [x, y] = centroid;
    const label = props.country || "Selected";

    const ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    ring.setAttribute("class", "hotspot-active-marker-ring");
    ring.setAttribute("cx", x);
    ring.setAttribute("cy", y);
    ring.setAttribute("r", "13");
    svg.appendChild(ring);

    const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    dot.setAttribute("class", "hotspot-active-marker");
    dot.setAttribute("cx", x);
    dot.setAttribute("cy", y);
    dot.setAttribute("r", "5.5");
    svg.appendChild(dot);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("class", "hotspot-active-label");
    text.setAttribute("x", Math.min(WIDTH - 140, x + 16));
    text.setAttribute("y", Math.max(16, y - 10));
    text.textContent = label;
    svg.appendChild(text);
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

  function applyLinkedHighlight(countryKeyValue, options = {}) {
    if (!countryKeyValue) return;
    activeCountryKey = countryKeyValue;

    document.querySelectorAll(".hotspot-row.link-active, .hotspot-country.link-active").forEach(el => {
      el.classList.remove("link-active");
    });

    document.querySelectorAll(".hotspot-row[data-country-key], .hotspot-country[data-country-key]").forEach(el => {
      if (el.dataset.countryKey === countryKeyValue) {
        el.classList.add("link-active");
      }
    });

    const feature = geoFeatures.find(f => countryKey(f.properties?.country) === countryKeyValue);
    if (feature) {
      addActiveMarker(feature);
    }

    const details = document.querySelector("#hotspotMapDetails");
    if (details && options.detailsHTML) {
      details.innerHTML = options.detailsHTML;
    }
  }

  function updateToggleState(metricKey) {
    document.querySelectorAll("[data-map-metric]").forEach(button => {
      const isActive = button.dataset.mapMetric === metricKey;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
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
      const key = countryKey(props.country);
      const d = geometryToPath(feature.geometry);
      const fillClass = classForValue(props[metricKey], breaks);
      const label = `${props.country}: ${metricConfig.formatter(props[metricKey])}`;

      return `<path
        d="${d}"
        class="hotspot-country ${fillClass}"
        data-idx="${idx}"
        data-country-key="${escapeAttr(key)}"
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
      const key = countryKey(props.country);

      const show = () => {
        applyLinkedHighlight(key, { detailsHTML: detailHTML(props, metricKey) });
      };

      path.addEventListener("mouseenter", show);
      path.addEventListener("focus", show);
      path.addEventListener("click", show);
    });

    if (activeCountryKey) {
      const feature = geoFeatures.find(f => countryKey(f.properties?.country) === activeCountryKey);
      if (feature) {
        applyLinkedHighlight(activeCountryKey, { detailsHTML: detailHTML(feature.properties || {}, metricKey) });
      }
    }
  }

  function bindRankingEvents() {
    const section = document.querySelector("#hotspots");
    if (!section || section.dataset.rankingBound === "true") return;

    section.dataset.rankingBound = "true";

    function handleRankingEvent(event) {
      const row = event.target.closest?.(".hotspot-row[data-country-key]");
      if (!row) return;

      const key = row.dataset.countryKey;
      const feature = geoFeatures.find(f => countryKey(f.properties?.country) === key);
      const html = feature
        ? detailHTML(feature.properties || {}, activeMetric)
        : `<strong>${row.querySelector("strong")?.textContent || "Country"}</strong> · ranking row highlighted.`;

      applyLinkedHighlight(key, { detailsHTML: html });
    }

    section.addEventListener("mouseover", handleRankingEvent);
    section.addEventListener("focusin", handleRankingEvent);
    section.addEventListener("click", handleRankingEvent);
  }

  async function renderHotspotRankings() {
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

      bindRankingEvents();
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

  async function renderHotspotMap() {
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
      bindRankingEvents();
    } catch (err) {
      map.innerHTML = `
        <div class="map-loading">
          Could not load choropleth data: ${err.message}
        </div>
      `;
      console.error(err);
    }
  }

  function initHotspots() {
    renderHotspotRankings();
    renderHotspotMap();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHotspots);
  } else {
    initHotspots();
  }
})();
