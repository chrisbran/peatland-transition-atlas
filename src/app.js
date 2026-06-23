
const DATA = {
  papers: "public/data/papers.json",
  pathways: "public/data/transition_pathways.json",
  regions: "public/data/region_case_studies.geojson",
  sections: "public/data/atlas_story_sections.json"
};

const state = {
  papers: [],
  pathways: [],
  regions: [],
  sections: [],
  selectedPathway: null,
  selectedRegion: null
};

async function loadJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}`);
  return res.json();
}

function splitPipe(value) {
  return (value || "").split("|").filter(Boolean);
}

function scoreDots(score, max = 3) {
  const n = Number(score || 0);
  return `<div class="score-bars">${Array.from({length:max}, (_, i) =>
    `<span class="score-dot ${i < n ? "on" : ""}"></span>`).join("")}</div>`;
}

function project(lon, lat) {
  // Simple equirectangular projection for Europe-focused approximate visual anchors.
  // Bounds chosen to include Iceland/Atlantic conceptual nodes to Eastern Europe.
  const lonMin = -30, lonMax = 35, latMin = 45, latMax = 65;
  const x = ((lon - lonMin) / (lonMax - lonMin)) * 100;
  const y = (1 - ((lat - latMin) / (latMax - latMin))) * 100;
  return { x: Math.max(2, Math.min(98, x)), y: Math.max(3, Math.min(97, y)) };
}

function renderMetrics() {
  (function() { const __b83TextTarget = document.querySelector("#metricPapers"); if (__b83TextTarget) { __b83TextTarget.textContent = state.papers.length; } })();
  (function() { const __b83TextTarget = document.querySelector("#metricPathways"); if (__b83TextTarget) { __b83TextTarget.textContent = state.pathways.length; } })();
  (function() { const __b83TextTarget = document.querySelector("#metricRegions"); if (__b83TextTarget) { __b83TextTarget.textContent = state.regions.length; } })();
}

function renderStorySections() {
  const el = document.querySelector("#storySections");
  el.innerHTML = state.sections.map(s => `
    <article class="story-card">
      <p class="eyebrow">0${s.chapter_order} · ${s.visualisation_type.replaceAll("_", " ")}</p>
      <h3>${s.title}</h3>
      <p>${s.main_message}</p>
      <div class="tag-row">
        <span class="tag">${s.current_data_status}</span>
        <span class="tag">${s.mvp_priority}</span>
      </div>
    </article>
  `).join("");
}

function renderMap(filter = "all") {
  const el = document.querySelector("#evidenceMap");
  el.innerHTML = "";
  state.regions.forEach(region => {
    const { lon, lat } = region.geometry ? {
      lon: region.geometry.coordinates[0],
      lat: region.geometry.coordinates[1]
    } : { lon: 0, lat: 0 };
    const props = region.properties;
    const pt = project(lon, lat);
    const marker = document.createElement("button");
    marker.className = "map-node";
    marker.style.left = `${pt.x}%`;
    marker.style.top = `${pt.y}%`;
    marker.style.setProperty("--size", `${0.85 + Number(props.marker_size_hint || 1) * 0.18}rem`);
    marker.title = props.map_label;
    marker.setAttribute("aria-label", props.map_label);
    marker.dataset.category = props.marker_category;
    if (filter !== "all" && props.marker_category !== filter) marker.classList.add("hidden");
    marker.addEventListener("click", () => selectRegion(props.region_id));
    el.appendChild(marker);
  });
}

function selectRegion(regionId) {
  state.selectedRegion = state.regions.find(r => r.properties.region_id === regionId);
  const props = state.selectedRegion.properties;
  const card = document.querySelector("#regionCard");
  const evidenceType = (props.evidence_type || props.region_type || "evidence node").replaceAll("_", " ");
  card.innerHTML = `
    <p class="eyebrow">${props.country}</p>
    <h3>${props.region_name}</h3>

    <div class="evidence-meta">
      <span><strong>Evidence type:</strong> ${evidenceType}</span>
    </div>

    <p><strong>Key message:</strong> ${props.key_message}</p>
    <p><strong>Transfer hypothesis for South Germany:</strong> ${props.south_germany_transfer_note}</p>
    <p><strong>Main caveat:</strong> ${props.caveat}</p>
    <p><strong>Supporting papers:</strong> ${props.supporting_papers}</p>

    <p class="micro-note">Map points are approximate evidence anchors, not exact field-site coordinates.</p>

    <div class="tag-row">
      ${splitPipe(props.dominant_pathway_ids).map(t => `<span class="tag">${t}</span>`).join("")}
    </div>
  `;
}

function renderPathways() {
  const spectrum = document.querySelector("#pathwaySpectrum");
  spectrum.innerHTML = state.pathways
    .sort((a,b) => Number(a.transition_position) - Number(b.transition_position))
    .map(p => `
      <article class="pathway-card" data-pathway="${p.pathway_id}">
        <p class="eyebrow">${p.pathway_id} · ${p.wetness_gradient_position.replaceAll("_", " ")}</p>
        <h3>${p.short_label}</h3>
        <p>${p.atlas_card_text}</p>
      </article>
    `).join("");

  document.querySelectorAll(".pathway-card").forEach(card => {
    card.addEventListener("click", () => selectPathway(card.dataset.pathway));
  });

  selectPathway(state.pathways[0]?.pathway_id);
}

function selectPathway(pathwayId) {
  state.selectedPathway = state.pathways.find(p => p.pathway_id === pathwayId);
  document.querySelectorAll(".pathway-card").forEach(card => {
    card.classList.toggle("selected", card.dataset.pathway === pathwayId);
  });
  const p = state.selectedPathway;
  const matrix = document.querySelector("#pathwayMatrix");
  matrix.innerHTML = `
    <p class="eyebrow">${p.pathway_id} · ${p.visual_story_role}</p>
    <h3>${p.pathway_name}</h3>
    <p>${p.short_definition}</p>
    <div class="score-note">
      Score legend: 1 = low, 2 = medium, 3 = high. Scores are qualitative literature-informed codings, not statistical estimates.
    </div>

    <div class="score-row"><span>GHG mitigation</span>${scoreDots(p.ghg_score_1_low_3_high)}</div>
    <div class="score-row"><span>Trafficability constraint</span>${scoreDots(p.trafficability_score_1_low_3_high)}</div>
    <div class="score-row"><span>Farm compatibility</span>${scoreDots(p.farm_compatibility_score_1_low_3_high)}</div>
    <div class="score-row"><span>Market maturity</span>${scoreDots(p.market_maturity_score_1_low_3_high)}</div>
    <div class="score-row"><span>Adoption barrier</span>${scoreDots(p.adoption_barrier_score_1_low_3_high)}</div>
    <div class="score-row"><span>South Germany fit</span>${scoreDots(p.south_germany_fit_score_1_low_3_high)}</div>

    <p><strong>Main benefit:</strong> ${p.main_benefit}</p>
    <p><strong>Main trade-off:</strong> ${p.main_tradeoff}</p>
    <p><strong>Key uncertainty:</strong> ${p.key_uncertainty}</p>
    <p><strong>Supporting papers:</strong> ${p.supporting_papers}</p>
  `;
}

function renderFitChart() {
  const el = document.querySelector("#fitChart");
  el.innerHTML = `
    <span class="fit-axis-label" style="left:1rem; bottom:.8rem;">lower hydrological requirement</span>
    <span class="fit-axis-label" style="right:1rem; bottom:.8rem;">higher hydrological requirement</span>
    <span class="fit-axis-label" style="left:1rem; top:.8rem;">higher farm compatibility</span>
    <span class="fit-axis-label" style="left:1rem; bottom:2.3rem;">lower farm compatibility</span>
  `;

  state.pathways.forEach(p => {
    const hydro = Number(p.transition_position || 1);
    const farm = Number(p.farm_compatibility_score_1_low_3_high || 1);
    const ghg = Number(p.ghg_score_1_low_3_high || 1);
    const adoption = Number(p.adoption_barrier_score_1_low_3_high || 1);
    const x = 8 + ((hydro - 1) / 7) * 84;
    const y = 90 - ((farm - 1) / 2) * 72;
    const bubble = 2.0 + ghg * 0.9;
    const risk = adoption >= 3 ? "risk-high" : adoption === 2 ? "risk-medium" : "risk-low";
    const div = document.createElement("div");
    div.className = `fit-bubble ${risk}`;
    div.style.left = `${x}%`;
    div.style.top = `${y}%`;
    div.style.setProperty("--bubble", `${bubble}rem`);
    div.title = `${p.pathway_name}: ${p.main_tradeoff}`;
    div.textContent = p.short_label;
    div.addEventListener("click", () => {
      location.hash = "#pathways";
      setTimeout(() => selectPathway(p.pathway_id), 60);
    });
    el.appendChild(div);
  });
}

function setupFilters() {
  document.querySelectorAll(".map-toolbar button").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".map-toolbar button").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderMap(btn.dataset.filter);
    });
  });
}

async function init() {
  const [papers, pathways, regionsGeojson, sections] = await Promise.all([
    loadJson(DATA.papers),
    loadJson(DATA.pathways),
    loadJson(DATA.regions),
    loadJson(DATA.sections)
  ]);
  state.papers = papers;
  state.pathways = pathways;
  state.regions = regionsGeojson.features;
  state.sections = sections;

  renderMetrics();
  renderStorySections();
  renderMap();
  setupFilters();
  renderPathways();
  renderFitChart();
}

init().catch(err => {
  console.error(err);
  document.body.insertAdjacentHTML("afterbegin", `<pre style="padding:1rem;background:#4b1d1d;color:white">${err.message}</pre>`);
});
