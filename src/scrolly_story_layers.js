/*
B13 — Bind sticky story to real map layers where available.

Available real layers:
- world country base layer
- country drained-organic-soils hotspot layer
- Baden-Württemberg BK50-Moor layer

Planned/future layers are explicitly labelled as placeholders.
No external dependencies.
*/

(function () {
  const URLS = {
    base: "public/data/world_countries_110m_base.geojson",
    hotspots: "public/data/hotspot_countries_110m.geojson",
    bw: "public/data/bw_bk50_moor_simplified.geojson"
  };

  const WIDTH = 960;
  const HEIGHT = 620;
  const PAD = 36;
  const cache = {};
  const htmlCache = {};

  const stage = document.querySelector("#storyStage");
  if (!stage) return;

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

  function fmtArea(value) {
    const n = num(value);
    if (n === null) return "area not available";
    const ha = n / 10000;
    if (ha >= 1000) return `${(ha / 1000).toFixed(1)} kha`;
    return `${ha.toFixed(1)} ha`;
  }

  async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load ${url}`);
    return res.json();
  }

  function robinsonProject(coord) {
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

  function makeBBoxProject(features) {
    const bounds = bbox(features);
    if (!bounds) return coord => [0, 0];

    const dx = bounds.maxX - bounds.minX;
    const dy = bounds.maxY - bounds.minY;
    const sx = (WIDTH - PAD * 2) / dx;
    const sy = (HEIGHT - PAD * 2) / dy;
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
      return geometry.coordinates
        .flatMap(poly => poly.map(ring => ringToPath(ring, project)))
        .join(" ");
    }
    return "";
  }

  function quantileBreaks(values) {
    const sorted = values.filter(v => Number.isFinite(v)).sort((a, b) => a - b);
    if (!sorted.length) return [];
    const q = p => sorted[Math.max(0, Math.min(sorted.length - 1, Math.round((sorted.length - 1) * p)))];
    return [q(0.2), q(0.4), q(0.6), q(0.8)];
  }

  function fillClass(value, breaks) {
    const v = num(value);
    if (v === null || !breaks.length) return "story-hotspot-no-data";
    if (v <= breaks[0]) return "story-hotspot-1";
    if (v <= breaks[1]) return "story-hotspot-2";
    if (v <= breaks[2]) return "story-hotspot-3";
    if (v <= breaks[3]) return "story-hotspot-4";
    return "story-hotspot-5";
  }

  function worldBasePaths() {
    const features = cache.base?.features || [];
    return features.map(f => `<path class="story-real-base-country" d="${geometryToPath(f.geometry, robinsonProject)}"></path>`).join("");
  }

  function renderWorldEmissions() {
    const hotspots = cache.hotspots?.features || [];
    const values = hotspots.map(f => num(f.properties?.emissions_total_kt_co2e)).filter(v => v !== null);
    const breaks = quantileBreaks(values);

    const hotspotPaths = hotspots.map(f => {
      const props = f.properties || {};
      const klass = fillClass(props.emissions_total_kt_co2e, breaks);
      const label = `${props.country || "Country"} · ${fmtKt(props.emissions_total_kt_co2e)}`;
      return `<path class="story-real-hotspot ${klass}" d="${geometryToPath(f.geometry, robinsonProject)}">
        <title>${label}</title>
      </path>`;
    }).join("");

    return `
      <svg class="story-real-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
        <rect class="story-real-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
        ${worldBasePaths()}
        ${hotspotPaths}
      </svg>
      <div class="story-real-caption">
        <strong>Real layer:</strong> country-level drained organic soils emissions · <span>public/data/hotspot_countries_110m.geojson</span>
      </div>
    `;
  }

  function renderPlannedGlobalPeat() {
    return `
      <svg class="story-real-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
        <rect class="story-real-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
        ${worldBasePaths()}
        <ellipse class="story-planned-peat" cx="440" cy="170" rx="60" ry="17"></ellipse>
        <ellipse class="story-planned-peat" cx="530" cy="185" rx="82" ry="22"></ellipse>
        <ellipse class="story-planned-peat" cx="385" cy="250" rx="52" ry="18"></ellipse>
        <ellipse class="story-planned-peat" cx="650" cy="285" rx="70" ry="20"></ellipse>
      </svg>
      <div class="story-real-caption planned">
        <strong>Planned layer:</strong> global peat/organic-soils extent · source inventory prepared, web layer not processed yet
      </div>
    `;
  }

  function renderEuropeOrGermany(state) {
    const isGermany = state === "germany";
    const box = isGermany
      ? { x: 500, y: 245, w: 32, h: 38, label: "Germany organic-soils bridge layer planned" }
      : { x: 445, y: 180, w: 205, h: 155, label: "Europe wetland/peat context planned" };

    return `
      <svg class="story-real-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
        <rect class="story-real-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
        ${worldBasePaths()}
        <rect class="story-focus-box" x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="14"></rect>
        <text class="story-focus-label" x="${box.x + box.w + 12}" y="${box.y + 24}">${isGermany ? "Germany" : "Europe"}</text>
      </svg>
      <div class="story-real-caption planned">
        <strong>Planned layer:</strong> ${box.label}
      </div>
    `;
  }

  function renderBW() {
    const features = (cache.bw?.features || []).filter(f => f.geometry);
    const project = makeBBoxProject(features);

    const paths = features.map((f, idx) => {
      const props = f.properties || {};
      const typeIdx = idx % 7;
      const title = `${props.class || "BK50-Moor"} · ${props.soil || ""} · ${fmtArea(props.source_area_m2)}`;
      return `<path class="story-bw-moor story-bw-type-${typeIdx}" d="${geometryToPath(f.geometry, project)}">
        <title>${title}</title>
      </path>`;
    }).join("");

    return `
      <svg class="story-real-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" preserveAspectRatio="xMidYMid meet">
        <rect class="story-real-ocean" x="0" y="0" width="${WIDTH}" height="${HEIGHT}"></rect>
        ${paths}
      </svg>
      <div class="story-real-caption">
        <strong>Real layer:</strong> Baden-Württemberg BK50-Moor simplified web layer · <span>${features.length.toLocaleString("en-US")} polygons</span>
      </div>
    `;
  }

  function renderBoundary() {
    return `
      <div class="story-boundary-panel">
        <p class="eyebrow">Interpretation boundary</p>
        <h3>Extent is not suitability</h3>
        <p>
          Peat/organic-soil extent is necessary spatial context. Rewetting suitability would also need hydrology,
          current land use, drainage, ownership, farm economics, policy instruments and local feasibility.
        </p>
      </div>
    `;
  }

  function ensureContainer() {
    let container = document.querySelector("#storyRealLayerMap");
    if (container) return container;

    container = document.createElement("div");
    container.id = "storyRealLayerMap";
    container.className = "story-real-map";

    const label = stage.querySelector(".story-state-label");
    if (label) {
      stage.insertBefore(container, label);
    } else {
      stage.appendChild(container);
    }

    stage.classList.add("real-story-bound");
    return container;
  }

  function renderState(state) {
    const container = ensureContainer();
    const key = state || "world-emissions";

    if (!htmlCache[key]) {
      if (key === "world-emissions") htmlCache[key] = renderWorldEmissions();
      else if (key === "global-peat") htmlCache[key] = renderPlannedGlobalPeat();
      else if (key === "europe" || key === "germany") htmlCache[key] = renderEuropeOrGermany(key);
      else if (key === "bw") htmlCache[key] = renderBW();
      else if (key === "boundary") htmlCache[key] = renderBoundary();
      else htmlCache[key] = renderWorldEmissions();
    }

    container.innerHTML = htmlCache[key];
  }

  async function init() {
    const container = ensureContainer();
    container.innerHTML = `<div class="map-loading">Loading real story layers…</div>`;

    const [base, hotspots, bw] = await Promise.allSettled([
      fetchJSON(URLS.base),
      fetchJSON(URLS.hotspots),
      fetchJSON(URLS.bw)
    ]);

    if (base.status === "fulfilled") cache.base = base.value;
    if (hotspots.status === "fulfilled") cache.hotspots = hotspots.value;
    if (bw.status === "fulfilled") cache.bw = bw.value;

    if (!cache.base || !cache.hotspots || !cache.bw) {
      container.innerHTML = `
        <div class="map-loading">
          Some real story layers could not be loaded. Check public/data files.
        </div>
      `;
      console.warn("Story layer loading status:", { base, hotspots, bw });
      return;
    }

    renderState(stage.dataset.state || "world-emissions");

    const observer = new MutationObserver(() => {
      renderState(stage.dataset.state || "world-emissions");
    });

    observer.observe(stage, { attributes: true, attributeFilter: ["data-state"] });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
