/*
 * B51 hard central map layer controller.
 *
 * Purpose:
 * Keep central story map layers mutually exclusive and deterministic.
 * This intentionally runs after central_global_map_story.js.
 */
(function () {
  const story = document.querySelector(".central-map-story");
  if (!story) return;

  const layerSelectors = {
    gpm: ".layer-gpm",
    total: ".layer-total",
    density: ".layer-density",
    borders: ".layer-borders",
    europePeat: ".layer-europe-peat",
    europeBorders: ".layer-europe-borders",
    germanyAdmin: ".layer-germany-admin",
    germanyExtent: ".layer-germany-thuenen-extent",
    germanyTypes: ".layer-germany-thuenen-types"
  };

  const aliases = {
    "global-peat": "extent",
    "global-extent": "extent",
    "peat": "extent",
    "gpm": "extent",
    "global-total": "total",
    "hotspots-total": "total",
    "global-density": "density",
    "hotspots-density": "density",
    "global-compare": "compare"
  };

  const stateLayers = {
    extent: {
      gpm: 0.96,
      borders: 0.72
    },
    total: {
      gpm: 0.38,
      total: 0.98,
      borders: 0.66
    },
    density: {
      gpm: 0.38,
      density: 0.98,
      borders: 0.66
    },
    compare: {
      gpm: 0.38,
      density: 0.98,
      borders: 0.66
    },
    "europe-borders": {
      europeBorders: 0.96
    },
    "europe-peat": {
      europePeat: 0.98,
      europeBorders: 0.96
    },
    "germany-context": {
      germanyAdmin: 0.96
    },
    "germany-thuenen-extent": {
      germanyExtent: 0.98,
      germanyAdmin: 0.88
    },
    "germany-thuenen-types": {
      germanyTypes: 0.98,
      germanyAdmin: 0.86
    }
  };

  function setOpacity(selector, value) {
    document.querySelectorAll(selector).forEach((el) => {
      el.style.setProperty("opacity", String(value), "important");
    });
  }

  function applyState(rawState) {
    const normalized = aliases[rawState] || rawState || "extent";
    const visible = stateLayers[normalized] || stateLayers.extent;

    Object.values(layerSelectors).forEach((selector) => {
      setOpacity(selector, 0);
    });

    Object.entries(visible).forEach(([key, opacity]) => {
      const selector = layerSelectors[key];
      if (selector) setOpacity(selector, opacity);
    });
  }

  function currentState() {
    return story.getAttribute("data-state") || "extent";
  }

  const observer = new MutationObserver(() => applyState(currentState()));
  observer.observe(story, { attributes: true, attributeFilter: ["data-state"] });

  window.addEventListener("load", () => applyState(currentState()));
  document.addEventListener("DOMContentLoaded", () => applyState(currentState()));

  setTimeout(() => applyState(currentState()), 50);
  setTimeout(() => applyState(currentState()), 300);

  window.__applyCentralMapState = applyState;
})();
