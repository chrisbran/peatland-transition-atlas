/*
B8a base land layer for hotspot choropleth.

This script inserts a non-interactive Natural Earth country base layer behind
the hotspot countries. It is intentionally independent from hotspots.js.
*/

(function () {
  const BASE_GEOJSON_URL = "public/data/world_countries_110m_base.geojson";
  const WIDTH = 960;
  const HEIGHT = 500;
  let baseFeatures = null;
  let renderScheduled = false;

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

  function insertBaseLayer() {
    const svg = document.querySelector("#hotspotMap svg");
    if (!svg || !baseFeatures || !baseFeatures.length) return;

    svg.querySelectorAll(".base-country").forEach(el => el.remove());

    const ocean = svg.querySelector(".map-ocean");
    const firstHotspot = svg.querySelector(".hotspot-country");

    const fragment = document.createDocumentFragment();

    baseFeatures.forEach(feature => {
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("class", "base-country");
      path.setAttribute("d", geometryToPath(feature.geometry));
      path.setAttribute("aria-hidden", "true");
      fragment.appendChild(path);
    });

    if (firstHotspot) {
      svg.insertBefore(fragment, firstHotspot);
    } else if (ocean && ocean.nextSibling) {
      svg.insertBefore(fragment, ocean.nextSibling);
    } else {
      svg.appendChild(fragment);
    }
  }

  function scheduleRender() {
    if (renderScheduled) return;
    renderScheduled = true;

    window.requestAnimationFrame(() => {
      renderScheduled = false;
      insertBaseLayer();
    });
  }

  async function initBaseLayer() {
    try {
      const res = await fetch(BASE_GEOJSON_URL);
      if (!res.ok) throw new Error(`Failed to load ${BASE_GEOJSON_URL}`);
      const geo = await res.json();
      baseFeatures = (geo.features || []).filter(f => f.geometry);

      scheduleRender();

      const map = document.querySelector("#hotspotMap");
      if (map) {
        const observer = new MutationObserver(scheduleRender);
        observer.observe(map, { childList: true, subtree: true });
      }
    } catch (err) {
      console.warn("Base land layer not loaded:", err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBaseLayer);
  } else {
    initBaseLayer();
  }
})();
