/*
B15e — Exact-state GPM 2.0 sticky-story overlay.

This replaces the heuristic/text-based B15c/B15d overlay.

Problem fixed:
- The previous script inferred the active GPM layer from visible text.
- During sticky scrolling, old/adjacent cards can remain partially visible.
- That caused the Europe/GPM image to appear repeatedly as a pseudo-placeholder.

Fix:
- Use only explicit data attributes on the active story step.
- Do not infer from text content.
- Hide the overlay for every non-GPM state.
*/

(function () {
  const IMAGE_URLS = {
    globalPeat: "public/images/gpm2_global_context.png",
    europePeat: "public/images/gpm2_europe_context.png",
  };

  const STAGE_SELECTORS = [
    "#storyRealLayerMap",
    "#storyStage",
    ".story-real-layer-map",
    ".story-visual",
    ".scrolly-visual"
  ];

  const STEP_SELECTORS = [
    "[data-story-state]",
    "[data-state]",
    "[data-key]",
    "[data-layer]"
  ];

  let overlay = null;
  let currentKey = null;
  let lastStage = null;

  function findStage() {
    for (const selector of STAGE_SELECTORS) {
      const el = document.querySelector(selector);
      if (el) return el;
    }
    return null;
  }

  function findStoryRoot(stage) {
    return document.querySelector("#guidedStory") || stage?.closest("section") || document.body;
  }

  function visibleScore(el) {
    const rect = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const visible = Math.max(0, Math.min(rect.bottom, vh) - Math.max(rect.top, 0));
    return visible / Math.max(1, rect.height);
  }

  function getStateString(el) {
    return [
      el.getAttribute("data-story-state"),
      el.getAttribute("data-state"),
      el.getAttribute("data-key"),
      el.getAttribute("data-layer")
    ].filter(Boolean).join(" ").toLowerCase().trim();
  }

  function keyFromStateString(raw) {
    if (!raw) return null;

    // Prevent false positives on country/emissions/hotspot states.
    const emissionsLike =
      raw.includes("emission") ||
      raw.includes("hotspot") ||
      raw.includes("country") ||
      raw.includes("faostat") ||
      raw.includes("drained");

    if (!emissionsLike && (
      raw === "global" ||
      raw === "global-peat" ||
      raw === "global_peat" ||
      raw === "globalpeat" ||
      raw === "peat" ||
      raw === "peat-context" ||
      raw === "peat_context" ||
      raw === "gpm" ||
      raw === "gpm2"
    )) {
      return "globalPeat";
    }

    if (
      raw === "europe" ||
      raw === "europa" ||
      raw === "europe-peat" ||
      raw === "europe_peat" ||
      raw === "europepeat" ||
      raw === "europe-context" ||
      raw === "europe_context"
    ) {
      return "europePeat";
    }

    return null;
  }

  function getActiveKey(stage) {
    const root = findStoryRoot(stage);
    const steps = Array.from(root.querySelectorAll(STEP_SELECTORS.join(",")));

    let best = null;
    let bestScore = 0;

    steps.forEach((step) => {
      const score = visibleScore(step);
      if (score > bestScore) {
        best = step;
        bestScore = score;
      }
    });

    if (!best || bestScore < 0.10) return null;

    return keyFromStateString(getStateString(best));
  }

  function ensureOverlay(stage) {
    const container = stage.parentElement || stage;

    if (lastStage !== stage || !overlay || !document.body.contains(overlay)) {
      lastStage = stage;

      const existing = container.querySelector(":scope > .story-gpm2-stable-overlay");
      overlay = existing || document.createElement("div");
      overlay.className = "story-gpm2-stable-overlay";
      overlay.setAttribute("aria-live", "polite");

      if (!existing) {
        container.appendChild(overlay);
      }

      const computedPosition = window.getComputedStyle(container).position;
      if (computedPosition === "static") {
        container.style.position = "relative";
      }
    }

    return overlay;
  }

  function hideOverlay(stage) {
    const layer = ensureOverlay(stage);
    currentKey = null;
    layer.classList.remove("is-visible");
    layer.setAttribute("aria-hidden", "true");
  }

  function showOverlay(stage, key) {
    const layer = ensureOverlay(stage);

    if (!key || !IMAGE_URLS[key]) {
      hideOverlay(stage);
      return;
    }

    if (currentKey !== key) {
      currentKey = key;

      const meta = key === "globalPeat"
        ? {
            title: "Global peatland context",
            caption: "Global Peatland Map 2.0 · peat dominated and peat in soil mosaic · 1 km context layer",
            src: IMAGE_URLS.globalPeat,
            alt: "Global Peatland Map 2.0 context image showing peat dominated and peat in soil mosaic areas worldwide."
          }
        : {
            title: "Europe peatland context",
            caption: "Global Peatland Map 2.0 visual Europe context · peat dominated and peat in soil mosaic",
            src: IMAGE_URLS.europePeat,
            alt: "Europe context image from Global Peatland Map 2.0 showing peat dominated and peat in soil mosaic areas."
          };

      layer.innerHTML = `
        <figure class="story-gpm2-context-card">
          <img class="story-gpm2-context-image" src="${meta.src}" alt="${meta.alt}" loading="eager">
          <figcaption class="story-real-caption story-gpm2-caption">
            <strong>Real layer:</strong> ${meta.title} · <span>${meta.caption}</span>
          </figcaption>
        </figure>
      `;
    }

    layer.classList.add("is-visible");
    layer.setAttribute("aria-hidden", "false");
  }

  function update() {
    const stage = findStage();
    if (!stage) return;

    const key = getActiveKey(stage);
    if (key) showOverlay(stage, key);
    else hideOverlay(stage);
  }

  let ticking = false;
  function scheduleUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(() => {
      ticking = false;
      update();
    });
  }

  window.addEventListener("load", scheduleUpdate);
  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate);

  window.addEventListener("DOMContentLoaded", () => {
    const root = document.querySelector("#guidedStory") || document.body;
    const observer = new MutationObserver(scheduleUpdate);
    observer.observe(root, { childList: true, subtree: true, attributes: true });
    scheduleUpdate();
  });
})();
