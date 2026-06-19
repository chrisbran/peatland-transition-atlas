/*
B18b-new — Central global map story.

Uses four ArcGIS-rendered PNG layers exported from the same GLOBAL_FRAME_V1.
The scroll state controls layer opacity only. The map frame, projection, size and placement remain fixed.
*/

(function () {
  const STATE_META = {
    extent: {
      mode: "Peatland context",
      title: "Peatlands are spatially concentrated.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-mosaic"></i>Peat in soil mosaic</span>
      `,
      source: "Global Peatland Map 2.0 context · exported from GLOBAL_FRAME_V1."
    },
    total: {
      mode: "Total emissions",
      title: "Absolute emissions show national climate pressure.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-risk"></i>Higher total emissions</span>
      `,
      source: "Country hotspot layer: emissions_total_kt_co2e · GPM context underneath · same ArcGIS frame."
    },
    density: {
      mode: "Emission density",
      title: "Density reveals concentrated pressure.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-risk"></i>Higher emission density</span>
      `,
      source: "Country hotspot layer: emissions_density_t_co2e_per_ha · GPM context underneath · same ArcGIS frame."
    },
    compare: {
      mode: "Interpretation",
      title: "Both views are needed for prioritisation.",
      legend: `
        <span><i class="legend-peat"></i>Peatland context</span>
        <span><i class="legend-density"></i>Emission density view</span>
        <span><i class="legend-border"></i>Country frame</span>
      `,
      source: "Interpretation state: density view remains visible; text explains why total emissions and density must be read together."
    }
    ,
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
    }
  };

  function setState(state) {
    const section = document.querySelector("#centralGlobalMapStory");
    if (!section || !STATE_META[state]) return;

    section.setAttribute("data-state", state);

    document.querySelectorAll(".central-map-step").forEach(step => {
      step.classList.toggle("is-active", step.getAttribute("data-global-state") === state);
    });

    const meta = STATE_META[state];

    const mode = document.querySelector("#centralMapMode");
    const title = document.querySelector("#centralMapTitle");
    const legend = document.querySelector("#centralMapLegend");
    const source = document.querySelector("#centralMapSource");

    if (mode) mode.textContent = meta.mode;
    if (title) title.textContent = meta.title;
    if (legend) legend.innerHTML = meta.legend;
    if (source) source.textContent = meta.source;
  }

  function init() {
    const section = document.querySelector("#centralGlobalMapStory");
    if (!section) return;

    const steps = Array.from(document.querySelectorAll(".central-map-step"));
    if (!steps.length) return;

    const observer = new IntersectionObserver(entries => {
      const visible = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visible) return;

      const state = visible.target.getAttribute("data-global-state");
      setState(state);
    }, {
      threshold: [0.35, 0.5, 0.7],
      rootMargin: "-28% 0px -38% 0px"
    });

    steps.forEach(step => observer.observe(step));
    setState("extent");
  }

  window.addEventListener("DOMContentLoaded", init);
})();
