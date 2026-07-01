(function () {
  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  ready(function () {
    var sections = Array.prototype.slice.call(document.querySelectorAll('[data-b169-live-sticky-zoom]'));
    if (!sections.length) return;

    var labelFallback = {
      'global-peat': 'Globale Moorverbreitung',
      'global-pressure-total': 'Gesamt-Emissionsdruck',
      'global-pressure-density': 'Emissionsintensität pro Fläche',
      'europe-bridge': 'Europäischer Bezugsraum',
      'germany-extent': 'Organische Böden in Deutschland',
      'germany-types': 'Typen organischer Böden',
      'baden-wuerttemberg': 'Baden-Württemberg: Moor-/Feuchtbodenkontext',
      'oberschwaben-handoff': 'Oberschwaben: Moor-/Feuchtbodenkontext'
    };

    function setState(section, state) {
      if (!state) return;

      section.querySelectorAll('[data-b169-step]').forEach(function (step) {
        var isActive = step.getAttribute('data-state') === state;
        step.classList.toggle('is-active', isActive);
        if (isActive) {
          step.setAttribute('aria-current', 'step');
        } else {
          step.removeAttribute('aria-current');
        }
      });

      section.querySelectorAll('[data-b169-base]').forEach(function (img) {
        img.classList.toggle('is-active', img.getAttribute('data-b169-base') === state);
      });

      section.querySelectorAll('[data-b169-overlay]').forEach(function (img) {
        img.classList.toggle('is-active', img.getAttribute('data-b169-overlay') === state);
      });

      var label = section.querySelector('.b169-stage-label');
      if (label) {
        var activeImg = section.querySelector('[data-b169-base="' + state + '"]');
        label.textContent = activeImg ? activeImg.getAttribute('alt') : (labelFallback[state] || state);
      }
    }

    sections.forEach(function (section) {
      var steps = Array.prototype.slice.call(section.querySelectorAll('[data-b169-step]'));
      if (!steps.length) return;

      steps.forEach(function (step) {
        var state = step.getAttribute('data-state');
        step.addEventListener('mouseenter', function () { setState(section, state); });
        step.addEventListener('focusin', function () { setState(section, state); });
      });

      setState(section, steps[0].getAttribute('data-state'));

      if (!('IntersectionObserver' in window)) return;

      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            setState(section, entry.target.getAttribute('data-state'));
          }
        });
      }, {
        root: null,
        rootMargin: '-36% 0px -46% 0px',
        threshold: 0.01
      });

      steps.forEach(function (step) {
        observer.observe(step);
      });
    });
  });
})();
