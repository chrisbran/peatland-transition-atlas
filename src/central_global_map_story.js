/*
 * B124 - Central map story single-source controller.
 * Owns step selection, labels, source text and PNG layer opacity for
 * #centralGlobalMapStory. Historic helper scripts are retired as no-ops.
 */
(function () {
  "use strict";

  const STORY_SELECTOR = "#centralGlobalMapStory";
  const STEP_SELECTOR = ".central-map-step[data-global-state], article[data-global-state]";

  const LAYERS = [
    "layer-gpm",
    "layer-total",
    "layer-density",
    "layer-borders",
    "layer-europe-borders",
    "layer-europe-peat",
    "layer-germany-admin",
    "layer-germany-thuenen-extent",
    "layer-germany-thuenen-types",
    "layer-bw-admin",
    "layer-bw-bk50-extent"
  ];

  const STATES = {
    "extent": {
      mode: "Globale Moorverbreitung",
      title: "Moore sind räumlich stark konzentriert.",
      legend: '<span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Datenbasis: Global Peatland Map 2.0; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.96, "layer-borders": 0.62 }
    },
    "total": {
      mode: "Emissionsdruck",
      title: "Gesamtemissionen zeigen, wo die größten bilanziellen Hotspots liegen.",
      legend: '<span><i class="legend-total"></i>höhere Gesamtemissionen</span><span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Datenbasis: FAOSTAT, Gesamtemissionen aus drainierten organischen Böden; Global Peatland Map 2.0 als Kontext; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.48, "layer-total": 0.92, "layer-borders": 0.84 }
    },
    "density": {
      mode: "Emissionsdichte",
      title: "Emissionsdichte zeigt, wo der Druck relativ zur Fläche besonders hoch ist.",
      legend: '<span><i class="legend-density"></i>höhere Emissionsdichte</span><span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Datenbasis: FAOSTAT, flächenbezogene Emissionsdichte aus drainierten organischen Böden; Global Peatland Map 2.0 als Kontext; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.48, "layer-density": 0.92, "layer-borders": 0.86 }
    },
    "compare": {
      mode: "Einordnung",
      title: "Größe und Intensität müssen getrennt gelesen werden.",
      legend: '<span><i class="legend-density"></i>Emissionsdichte</span><span><i class="legend-border"></i>Ländergrenzen</span>',
      source: "Hinweis: Gesamtmenge und Emissionsdichte beantworten unterschiedliche Fragen und dürfen nicht vermischt werden.",
      layers: { "layer-gpm": 0.56, "layer-density": 0.88, "layer-borders": 0.90 }
    },
    "europe-peat": {
      mode: "Europäischer Moorkontext",
      title: "Europa zeigt den größeren Bezugsraum.",
      legend: '<span><i class="legend-peat"></i>Moorkontext</span><span><i class="legend-border"></i>Europäische Ländergrenzen</span>',
      source: "Datenbasis: Global Peatland Map 2.0; Darstellung im europäischen Kartenrahmen.",
      layers: { "layer-europe-peat": 0.98, "layer-europe-borders": 0.88 }
    },
    "germany-thuenen-extent": {
      mode: "Organische Böden",
      title: "Deutschland grenzt den Prüfbedarf ein.",
      legend: '<span><i class="legend-peat"></i>Thünen-Kulisse organischer Böden</span><span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Datenbasis: Thünen-Kulisse organischer Böden; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-thuenen-extent": 0.98, "layer-germany-admin": 0.86 }
    },
    "germany-thuenen-types": {
      mode: "Einordnung der nationalen Kulisse",
      title: "Die nationale Kulisse ersetzt keine Standortprüfung.",
      legend: '<span><i class="legend-peat"></i>Thünen-Kulisse organischer Böden</span><span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Datenbasis: Thünen-Kulisse organischer Böden; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-thuenen-extent": 0.98, "layer-germany-admin": 0.86 }
    },
    "bw-bk50-extent": {
      mode: "BK50",
      title: "Baden-Württemberg macht die Frage regional konkret.",
      legend: '<span><i class="legend-peat"></i>BK50 Moor-/Feuchtbodenkontext</span><span><i class="legend-border"></i>Regionaler Kartenrahmen</span>',
      source: "Datenbasis: BK50 Moor-/Feuchtbodenkontext; eigene Auswahl und kartografische Aufbereitung.",
      layers: { "layer-bw-bk50-extent": 0.98, "layer-bw-admin": 0.86 }
    }
  };

  let story = null;
  let steps = [];
  let activeState = null;
  let ticking = false;

  function setText(id, value, html) {
    const el = document.getElementById(id);
    if (!el) return;
    if (html) el.innerHTML = value || "";
    else el.textContent = value || "";
  }

  function applyLayers(meta) {
    LAYERS.forEach((className, index) => {
      const opacity = meta.layers && Object.prototype.hasOwnProperty.call(meta.layers, className)
        ? meta.layers[className]
        : 0;
      document.querySelectorAll(STORY_SELECTOR + " ." + className).forEach((el) => {
        el.style.setProperty("opacity", String(opacity), "important");
        el.style.setProperty("visibility", opacity > 0 ? "visible" : "hidden", "important");
        el.style.setProperty("pointer-events", "none", "important");
        el.style.setProperty("z-index", String(10 + index), "important");
      });
    });
  }

  function applyState(state, reason) {
    if (!story || !STATES[state]) return;
    if (activeState === state && reason !== "force") return;

    activeState = state;
    const meta = STATES[state];

    story.setAttribute("data-state", state);
    story.setAttribute("data-b124-active-state", state);

    steps.forEach((step) => {
      const isActive = step.getAttribute("data-global-state") === state;
      step.classList.toggle("is-active", isActive);
      step.classList.toggle("is-current", isActive);
      if (isActive) step.setAttribute("aria-current", "step");
      else step.removeAttribute("aria-current");
    });

    setText("centralMapMode", meta.mode, false);
    setText("centralMapTitle", meta.title, false);
    setText("centralMapLegend", meta.legend, true);
    setText("centralMapSource", meta.source, false);
    applyLayers(meta);
  }

  function storyInRange() {
    if (!story) return false;
    const r = story.getBoundingClientRect();
    return r.bottom > 0 && r.top < window.innerHeight;
  }

  function pickStateFromViewport() {
    if (!steps.length) return null;
    const targetY = window.innerHeight * 0.46;
    let best = null;
    let bestScore = Infinity;

    steps.forEach((step) => {
      const rect = step.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const visible = rect.bottom >= 0 && rect.top <= window.innerHeight;
      const distance = Math.abs(center - targetY);
      const penalty = visible ? 0 : window.innerHeight;
      const score = distance + penalty;
      if (score < bestScore) {
        bestScore = score;
        best = step;
      }
    });

    return best ? best.getAttribute("data-global-state") : null;
  }

  function updateFromScroll() {
    ticking = false;
    if (!storyInRange()) return;
    const state = pickStateFromViewport();
    if (state) applyState(state, "scroll");
  }

  function scheduleUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateFromScroll);
  }

  function bindStepInteractions() {
    steps.forEach((step) => {
      const state = step.getAttribute("data-global-state");
      if (!state || !STATES[state]) return;
      step.addEventListener("mouseenter", () => applyState(state, "hover"));
      step.addEventListener("focusin", () => applyState(state, "focus"));
      step.addEventListener("click", () => applyState(state, "click"));
    });
  }

  function init() {
    story = document.querySelector(STORY_SELECTOR);
    if (!story) return;

    steps = Array.from(story.querySelectorAll(STEP_SELECTOR))
      .filter((step) => STATES[step.getAttribute("data-global-state")]);

    if (!steps.length) return;

    bindStepInteractions();

    const initial = story.getAttribute("data-state") || steps[0].getAttribute("data-global-state") || "extent";
    applyState(STATES[initial] ? initial : "extent", "force");
    scheduleUpdate();

    window.addEventListener("scroll", scheduleUpdate, { passive: true });
    window.addEventListener("resize", scheduleUpdate, { passive: true });

    window.__centralMapStoryB124 = {
      states: Object.keys(STATES),
      applyState,
      get activeState() { return activeState; }
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
