/*
 * B56 stage-label fix.
 *
 * Purpose:
 * Make the small map-stage chip follow the active central-map story state.
 * This fixes cases where the map image changes to Germany/Thuenen states but
 * the chip still reads "European peat context".
 */
(function () {
  const story = document.querySelector(".central-map-story");
  if (!story) return;

  const LABELS = {
    extent: "GLOBAL PEAT CONTEXT",
    total: "GLOBAL EMISSIONS PRESSURE",
    density: "EMISSION DENSITY",
    compare: "GLOBAL HOTSPOT INTERPRETATION",
    "europe-borders": "EUROPA",
    "europe-peat": "EUROPEAN PEAT CONTEXT",
    "germany-context": "DEUTSCHLAND",
    "germany-thuenen-extent": "THUENEN KULISSE",
    "germany-thuenen-types": "MOOR AND SOIL TYPES",
    "bw-context": "BADEN-WÜRTTEMBERG",
    "bw-bk50-extent": "BK50 MOOR- UND FEUCHTBÖDEN"
  };

  const ALIASES = {
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

  const KNOWN_LABEL_PATTERN = /(GLOBAL|EUROPE|EUROPEAN|GERMANY|THUENEN|MOOR AND SOIL|EMISSION|BADEN|BK50)/i;

  function activeState() {
    const raw = story.getAttribute("data-state") || "extent";
    return ALIASES[raw] || raw;
  }

  function stageRoot() {
    return (
      story.querySelector(".central-map-stage") ||
      story.querySelector(".central-map-visual") ||
      story.querySelector(".central-map-card") ||
      story.querySelector(".central-map-layer-stack") ||
      story
    );
  }

  function candidateElements(root) {
    const selectors = [
      "[data-central-map-mode]",
      "[data-map-mode]",
      ".central-map-mode",
      ".central-map-kicker",
      ".central-stage-mode",
      ".map-mode",
      ".map-chip",
      ".map-kicker",
      ".stage-chip",
      ".map-pill",
      ".central-map-pill"
    ];

    const set = new Set();
    selectors.forEach((selector) => {
      root.querySelectorAll(selector).forEach((el) => set.add(el));
      story.querySelectorAll(selector).forEach((el) => set.add(el));
    });

    // Fallback: leaf elements in the map stage whose text looks like a stage chip.
    root.querySelectorAll("span, p, div").forEach((el) => {
      const text = (el.textContent || "").trim();
      if (!text) return;
      if (el.children.length > 0) return;
      if (text.length > 42) return;
      if (KNOWN_LABEL_PATTERN.test(text)) set.add(el);
    });

    return Array.from(set);
  }

  function applyLabel() {
    const state = activeState();
    const label = LABELS[state];
    if (!label) return;

    const root = stageRoot();
    const candidates = candidateElements(root);

    if (!candidates.length) return;

    // Prefer elements that currently contain a known stage/context label.
    const target =
      candidates.find((el) => KNOWN_LABEL_PATTERN.test((el.textContent || "").trim())) ||
      candidates[0];

    target.textContent = label;
  }

  const observer = new MutationObserver(applyLabel);
  observer.observe(story, { attributes: true, attributeFilter: ["data-state"] });

  window.addEventListener("load", applyLabel);
  document.addEventListener("DOMContentLoaded", applyLabel);
  window.addEventListener("scroll", () => window.requestAnimationFrame(applyLabel), { passive: true });

  setTimeout(applyLabel, 50);
  setTimeout(applyLabel, 300);

  window.__fixCentralStageLabel = applyLabel;
})();
