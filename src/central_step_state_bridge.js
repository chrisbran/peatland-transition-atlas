/*
 * B52 central map step-state bridge.
 *
 * Purpose:
 * Ensure every .central-map-step[data-global-state] actively drives
 * .central-map-story[data-state]. This is needed for newly inserted
 * Europe/Germany steps when the original controller does not recognize them.
 */
(function () {
  const story = document.querySelector(".central-map-story");
  const steps = Array.from(document.querySelectorAll(".central-map-step[data-global-state]"));

  if (!story || !steps.length) return;

  const META = {
    "europe-borders": {
      mode: "Europe frame",
      title: "Europe needs its own regional map frame.",
      legend: `
        <span><i class="legend-border"></i>European country borders</span>
      `,
      source: "Europe frame: GISCO country boundaries · exported from EUROPE_FRAME_V1."
    },
    "europe-peat": {
      mode: "European peat context",
      title: "European peatlands are spatially concentrated.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-mosaic"></i>Peat in soil mosaic</span>
        <span><i class="legend-border"></i>Country frame</span>
      `,
      source: "GPM2 peatland context rendered in Europe frame · ETRS89 / LAEA Europe."
    },
    "germany-context": {
      mode: "Germany frame",
      title: "Germany is where peatland transition becomes an implementation problem.",
      legend: `
        <span><i class="legend-border"></i>Federal-state context</span>
      `,
      source: "Germany frame: national implementation scale with NUTS 1 / federal-state context."
    },
    "germany-thuenen-extent": {
      mode: "Thuenen Kulisse",
      title: "The Thuenen Kulisse identifies the national peat and organic-soils target area.",
      legend: `
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-extent" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#2F6B4F;background-color:#2F6B4F;"></span>Thuenen peat / organic-soils Kulisse</span>
        <span><i class="legend-border"></i>Federal-state context</span>
      `,
      source: "Thuenen Kulisse: national peat and organic-soils target area rendered as a one-colour extent layer."
    },
    "germany-thuenen-types": {
      mode: "Moor and soil types",
      title: "The type distinction is not cosmetic — it changes the transition logic.",
      legend: `
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-hh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#6E4B78;background-color:#6E4B78;"></span>Hochmoorboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-nh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#2F6B4F;background-color:#2F6B4F;"></span>Niedermoorboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-mf" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#8E7A4D;background-color:#8E7A4D;"></span>Moorfolgeboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-tief-hh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#8A5A63;background-color:#8A5A63;"></span>Tiefumbruchboden aus Hochmoor</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-tief-nh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#1F7A5C;background-color:#1F7A5C;"></span>Tiefumbruchboden aus Niedermoor</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-flach-hh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#9B7F8D;background-color:#9B7F8D;"></span>flach ueberdeckter Hochmoorboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-flach-nh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#6F9A78;background-color:#6F9A78;"></span>flach ueberdeckter Niedermoorboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-maechtig-hh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#B08B6C;background-color:#B08B6C;"></span>maechtig ueberdeckter Hochmoorboden</span>
        <span class="legend-entry"><span class="legend-swatch legend-thuenen-maechtig-nh" style="display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;border:1px solid rgba(255,255,255,.25);background:#B7A15A;background-color:#B7A15A;"></span>maechtig ueberdeckter Niedermoorboden</span>
      `,
      source: "Thuenen Kulisse symbolized by KAT_LANG to distinguish moor and soil types relevant for transition pathways."
    },
    "bw-context": {
      mode: "Baden-Württemberg frame",
      title: "Baden-Württemberg narrows the national frame to a regional planning scale.",
      legend: `
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BW frame: regional context exported from the same 16:9 ArcGIS map frame."
    },
    "bw-bk50-extent": {
      mode: "BK50 peat and wetland soils",
      title: "BK50 shows the regional peat and wetland soil context.",
      legend: `
        <span><i class="legend-peat"></i>BK50 peat / wetland soil context</span>
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BK50 BW layer: peat and wetland soil context shown as a single extent layer; no land-use or suitability classification is implied."
    }
  };

  function first(selectors) {
    for (const selector of selectors) {
      const el = story.querySelector(selector) || document.querySelector(selector);
      if (el) return el;
    }
    return null;
  }

  function setText(selectors, value) {
    const el = first(selectors);
    if (el && value) el.textContent = value;
  }

  function setHTML(selectors, value) {
    const el = first(selectors);
    if (el && value) el.innerHTML = value;
  }

  function updateMeta(state) {
    const meta = META[state];
    if (!meta) return;

    setText([
      "[data-central-map-mode]",
      "[data-map-mode]",
      ".central-map-mode",
      ".central-map-kicker",
      ".central-stage-mode",
      ".map-mode",
      ".map-chip"
    ], meta.mode);

    setText([
      "[data-central-map-title]",
      "[data-map-title]",
      ".central-map-title",
      ".central-stage-title",
      ".map-title"
    ], meta.title);

    setHTML([
      "[data-central-map-legend]",
      "[data-map-legend]",
      ".central-map-legend",
      ".central-stage-legend",
      ".map-legend"
    ], meta.legend);

    setText([
      "[data-central-map-source]",
      "[data-map-source]",
      ".central-map-source",
      ".central-stage-source",
      ".map-source"
    ], meta.source);
  }

  function applyState(state) {
    if (!state) return;

    if (story.getAttribute("data-state") !== state) {
      story.setAttribute("data-state", state);
    }

    updateMeta(state);

    if (typeof window.__applyCentralMapState === "function") {
      window.__applyCentralMapState(state);
    }
  }

  function activeStepByPosition() {
    const anchor = window.innerHeight * 0.48;
    let best = null;
    let bestDistance = Infinity;

    for (const step of steps) {
      const rect = step.getBoundingClientRect();
      const center = rect.top + rect.height * 0.5;
      const distance = Math.abs(center - anchor);

      if (rect.bottom >= 0 && rect.top <= window.innerHeight && distance < bestDistance) {
        best = step;
        bestDistance = distance;
      }
    }

    return best;
  }

  let ticking = false;
  function refresh() {
    ticking = false;
    const active = activeStepByPosition();
    if (!active) return;
    applyState(active.dataset.globalState);
  }

  function requestRefresh() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(refresh);
  }

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

    if (visible.length) {
      applyState(visible[0].target.dataset.globalState);
    } else {
      requestRefresh();
    }
  }, {
    root: null,
    rootMargin: "-30% 0px -45% 0px",
    threshold: [0, 0.15, 0.35, 0.6, 0.85]
  });

  steps.forEach((step) => observer.observe(step));
  window.addEventListener("scroll", requestRefresh, { passive: true });
  window.addEventListener("resize", requestRefresh);

  document.addEventListener("DOMContentLoaded", requestRefresh);
  window.addEventListener("load", requestRefresh);
  setTimeout(requestRefresh, 50);
  setTimeout(requestRefresh, 250);

  window.__centralStepStateBridgeRefresh = refresh;
})();
