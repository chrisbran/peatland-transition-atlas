/*
B11c Baden-Württemberg BK50-Moor preview map.
Static SVG rendering of the simplified BK50-Moor web layer.
*/

(function () {
  const DATA_URL = "public/data/bw_bk50_moor_simplified.geojson";
  const WIDTH = 960;
  const HEIGHT = 620;
  const PADDING = 24;

  function num(value) {
    if (value === undefined || value === null || value === "") return null;
    const n = Number(String(value).replace(",", "."));
    return Number.isFinite(n) ? n : null;
  }

  function fmtArea(value) {
    const n = num(value);
    if (n === null) return "area not available";
    const ha = n / 10000;
    if (ha >= 1000) return `${(ha / 1000).toFixed(1)} kha`;
    return `${ha.toFixed(1)} ha`;
  }

  function collectCoords(coords, out) {
    if (!Array.isArray(coords)) return;
    if (coords.length >= 2 && typeof coords[0] === "number" && typeof coords[1] === "number") {
      out.push(coords);
      return;
    }
    coords.forEach(item => collectCoords(item, out));
  }

  function bbox(features) {
    const pts = [];
    features.forEach(f => collectCoords(f.geometry?.coordinates, pts));
    if (!pts.length) return null;
    const xs = pts.map(p => p[0]);
    const ys = pts.map(p => p[1]);
    return { minX: Math.min(...xs), minY: Math.min(...ys), maxX: Math.max(...xs), maxY: Math.max(...ys) };
  }

  function makeProject(bounds) {
    const dx = bounds.maxX - bounds.minX;
    const dy = bounds.maxY - bounds.minY;
    const sx = (WIDTH - PADDING * 2) / dx;
    const sy = (HEIGHT - PADDING * 2) / dy;
    const s = Math.min(sx, sy);
    const usedW = dx * s;
    const usedH = dy * s;
    const ox = (WIDTH - usedW) / 2;
    const oy = (HEIGHT - usedH) / 2;

    return function project(coord) {
      const x = ox + (coord[0] - bounds.minX) * s;
      const y = HEIGHT - (oy + (coord[1] - bounds.minY) * s);
      return [x, y];
    };
  }

  function ringToPath(ring, project) {
    if (!ring || !ring.length) return "";
    return ring.map((coord, idx) => {
      const [x, y] = project(coord);
      return `${idx === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;
    }).join(" ") + " Z";
  }

  function geometryToPath(geometry, project) {
    if (!geometry) return "";
    if (geometry.type === "Polygon") {
      return geometry.coordinates.map(ring => ringToPath(ring, project)).join(" ");
    }
    if (geometry.type === "MultiPolygon") {
      return geometry.coordinates.flatMap(poly => poly.map(ring => ringToPath(ring, project))).join(" ");
    }
    return "";
  }

  function classKey(value) {
    return String(value || "Unclassified").trim() || "Unclassified";
  }

  function summarize(features) {
    const counts = new Map();
    let totalArea = 0;
    features.forEach(f => {
      const klass = classKey(f.properties?.class);
      counts.set(klass, (counts.get(klass) || 0) + 1);
      const area = num(f.properties?.source_area_m2);
      if (area !== null) totalArea += area;
    });
    return { counts: [...counts.entries()].sort((a, b) => b[1] - a[1]), totalArea };
  }

  function typeIndexMap(counts) {
    const map = new Map();
    counts.forEach(([klass], idx) => map.set(klass, idx % 7));
    return map;
  }

  function detailHTML(props) {
    return `<strong>${props.class || "Unclassified"}</strong>
      · ${props.soil || "soil class not available"}
      · ${props.material || "material not available"}
      · ${fmtArea(props.source_area_m2)}`;
  }

  function renderLegend(counts) {
    const legend = document.querySelector("#bwMoorLegend");
    if (!legend) return;
    const top = counts.slice(0, 7);
    legend.innerHTML = `
      <div class="legend-title">BK50-Moor classes</div>
      ${top.map(([klass, count], idx) => `
        <span class="legend-item"><i class="bw-moor-type-${idx}"></i>${klass} <small>${count}</small></span>
      `).join("")}
    `;
  }

  function renderMetrics(features, summary) {
    const countEl = document.querySelector("#bwMoorFeatureCount");
    const classEl = document.querySelector("#bwMoorClassCount");
    const areaEl = document.querySelector("#bwMoorArea");
    if (countEl) countEl.textContent = features.length.toLocaleString("en-US");
    if (classEl) classEl.textContent = summary.counts.length.toLocaleString("en-US");
    if (areaEl) areaEl.textContent = fmtArea(summary.totalArea);
  }

  async function init() {
    const container = document.querySelector("#bwMoorMap");
    if (!container) return;
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`Failed to load ${DATA_URL}`);
      const geo = await res.json();
      const features = (geo.features || []).filter(f => f.geometry);
      const bounds = bbox(features);
      if (!features.length || !bounds) throw new Error("No displayable BK50-Moor features found.");

      const project = makeProject(bounds);
      const summary = summarize(features);
      const idxMap = typeIndexMap(summary.counts);
      renderMetrics(features, summary);
      renderLegend(summary.counts);

      const paths = features.map((feature, idx) => {
        const props = feature.properties || {};
        const klass = classKey(props.class);
        const typeIdx = idxMap.get(klass) || 0;
        const d = geometryToPath(feature.geometry, project);
        return `<path d="${d}" class="bw-moor-feature bw-moor-type-${typeIdx}" data-idx="${idx}" tabindex="0" aria-label="${String(klass).replace(/"/g, "&quot;")}"></path>`;
      }).join("");

      container.innerHTML = `
        <svg class="bw-moor-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
          <rect class="bw-moor-bg" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
          ${paths}
        </svg>`;

      const details = document.querySelector("#bwMoorDetails");
      container.querySelectorAll(".bw-moor-feature").forEach(path => {
        const feature = features[Number(path.dataset.idx)];
        const props = feature.properties || {};
        const show = () => {
          container.querySelectorAll(".bw-moor-feature.active").forEach(el => el.classList.remove("active"));
          path.classList.add("active");
          if (details) details.innerHTML = detailHTML(props);
        };
        path.addEventListener("mouseenter", show);
        path.addEventListener("focus", show);
        path.addEventListener("click", show);
      });
      if (details) details.innerHTML = "Hover over a BK50-Moor polygon to inspect class, soil description and source area.";
    } catch (err) {
      container.innerHTML = `<div class="map-loading">Could not load BK50-Moor layer: ${err.message}</div>`;
      console.error(err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
