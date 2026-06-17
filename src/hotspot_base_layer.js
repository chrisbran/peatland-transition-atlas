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
