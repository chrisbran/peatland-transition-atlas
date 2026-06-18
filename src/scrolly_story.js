/*
B12 sticky-scroll scaffold.

This is intentionally a light, dependency-free scaffold. It creates active
story states while the existing explorer sections remain unchanged below.
*/

(function () {
  const steps = Array.from(document.querySelectorAll(".story-step"));
  const visual = document.querySelector("#storyVisual");
  const titleEl = document.querySelector("#storyVisualTitle");
  const textEl = document.querySelector("#storyVisualText");
  const stageEl = document.querySelector("#storyStage");
  const layerEls = Array.from(document.querySelectorAll("[data-story-layer]"));

  if (!steps.length || !visual || !titleEl || !textEl || !stageEl) return;

  function setActive(step) {
    const state = step.dataset.state || "world-emissions";
    const title = step.dataset.visualTitle || step.querySelector("h3")?.textContent || "";
    const text = step.dataset.visualText || step.querySelector("p")?.textContent || "";

    steps.forEach(el => el.classList.toggle("active", el === step));

    visual.dataset.state = state;
    stageEl.dataset.state = state;
    titleEl.textContent = title;
    textEl.textContent = text;

    layerEls.forEach(el => {
      const activeStates = (el.dataset.storyLayer || "").split(/\s+/);
      el.classList.toggle("active", activeStates.includes(state));
    });
  }

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (visible) setActive(visible.target);
  }, {
    root: null,
    threshold: [0.25, 0.45, 0.65, 0.85],
    rootMargin: "-18% 0px -35% 0px"
  });

  steps.forEach(step => observer.observe(step));
  setActive(steps[0]);
})();
