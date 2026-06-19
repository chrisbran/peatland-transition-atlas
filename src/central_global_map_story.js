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

  
  // B19d/B50 Germany / Thuenen states
  Object.assign(STATE_META, {
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
    }
  });

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
