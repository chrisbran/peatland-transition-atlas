from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
JS = ROOT / "src" / "b169_live_sticky_zoom.js"

SCRIPT = ROOT / "scripts" / "169_live_sticky_zoom_integration_prototype.py"
DOC = ROOT / "docs" / "B169_live_sticky_zoom_integration_prototype.md"
STATE_CSV = ROOT / "docs" / "B169_live_sticky_zoom_state_matrix.csv"
AUDIT = ROOT / "docs" / "B169_live_sticky_zoom_integration_prototype_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
HTML_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"
CSS_START = "/* B169_LIVE_STICKY_ZOOM_START */"
CSS_END = "/* B169_LIVE_STICKY_ZOOM_END */"

JS_REF = '<script src="src/b169_live_sticky_zoom.js" defer></script>'

ASSETS = [
    "public/maps/global/global_gpm2_peat_extent.png",
    "public/maps/global/global_hotspots_total.png",
    "public/maps/global/global_hotspots_density.png",
    "public/maps/global/global_country_borders.png",
    "public/maps/europe/europe_gpm2_peat_extent.png",
    "public/maps/europe/europe_country_borders.png",
    "public/maps/germany/germany_thuenen_moor_extent.png",
    "public/maps/germany/germany_thuenen_moor_types.png",
    "public/maps/germany/germany_admin_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
    "public/maps/bw/bw_admin_context.png",
    "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
    "public/maps/oberschwaben/oberschwaben_admin_context.png",
]

STATES = [
    {
        "order": 1,
        "state": "global-peat",
        "kicker": "01 / Welt",
        "title": "Kleine Fläche, große Wirkung",
        "body": "Moore nehmen global wenig Raum ein. Für Klima, Wasser und Biodiversität sind sie trotzdem entscheidend.",
        "base": "public/maps/global/global_gpm2_peat_extent.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "label": "Globale Moorverbreitung",
        "note": "Die Karte zeigt die räumliche Konzentration von Mooren — nicht ihre lokale Nutzbarkeit.",
    },
    {
        "order": 2,
        "state": "global-pressure-total",
        "kicker": "02 / Gesamt",
        "title": "Wo ist der gesamte Emissionsdruck hoch?",
        "body": "Die absolute Menge zeigt, wo drainierte organische Böden global besonders stark zur Emissionsbilanz beitragen.",
        "base": "public/maps/global/global_hotspots_total.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "label": "Gesamt-Emissionsdruck",
        "note": "Gesamtwerte zeigen große Beiträge — oft dort, wo Fläche, Entwässerung und Nutzung zusammenkommen.",
    },
    {
        "order": 3,
        "state": "global-pressure-density",
        "kicker": "03 / Intensität",
        "title": "Wo ist der Druck pro Fläche besonders hoch?",
        "body": "Die Intensitätskarte erzählt eine andere Geschichte: Nicht nur die Gesamtmenge zählt, sondern der Druck pro Fläche.",
        "base": "public/maps/global/global_hotspots_density.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "label": "Emissionsintensität pro Fläche",
        "note": "Intensität und Gesamtmenge sind unterschiedliche Aussagen. Für Planung müssen beide getrennt gelesen werden.",
    },
    {
        "order": 4,
        "state": "europe-bridge",
        "kicker": "04 / Europa",
        "title": "Aus Relevanz wird Planung",
        "body": "Der Maßstab wechselt: Klimafragen werden zu politischen und regionalen Planungskulissen.",
        "base": "public/maps/europe/europe_gpm2_peat_extent.png",
        "overlay": "public/maps/europe/europe_country_borders.png",
        "label": "Europäischer Bezugsraum",
        "note": "Der regionale Blick wird erst verständlich, wenn der größere Bezugsraum steht.",
    },
    {
        "order": 5,
        "state": "germany-extent",
        "kicker": "05 / Deutschland",
        "title": "Die nationale Karte zeigt, wo genauer hingesehen werden muss",
        "body": "Organische Böden bilden eine Planungskulisse. Welche Nutzung tragfähig ist, entscheidet sich aber erst darunter.",
        "base": "public/maps/germany/germany_thuenen_moor_extent.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "label": "Organische Böden in Deutschland",
        "note": "Die nationale Kulisse grenzt Prüfbedarf ein — sie ersetzt keine Standortprüfung.",
    },
    {
        "order": 6,
        "state": "germany-types",
        "kicker": "06 / Bodenkontext",
        "title": "Nicht jeder Moorboden stellt dieselbe Frage",
        "body": "Typen, Nutzung und Wasserstand unterscheiden sich. Deshalb braucht Moorbodenschutz mehr als eine Flächenkarte.",
        "base": "public/maps/germany/germany_thuenen_moor_types.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "label": "Typen organischer Böden",
        "note": "Die Karte bereitet die regionale Frage vor: Welche Nutzung trifft auf welchen Bodenkontext?",
    },
    {
        "order": 7,
        "state": "baden-wuerttemberg",
        "kicker": "07 / Baden-Württemberg",
        "title": "Jetzt wird die Frage regional",
        "body": "In Baden-Württemberg wird sichtbar, wo Moor- und Feuchtbodenkontexte auf Zuständigkeiten und regionale Planung treffen.",
        "base": "public/maps/bw/bw_bk50_moor_extent.png",
        "overlay": "public/maps/bw/bw_admin_context.png",
        "label": "Baden-Württemberg: Moor-/Feuchtbodenkontext",
        "note": "Der BW-Layer ist die Brücke: nicht mehr Deutschland, noch nicht der Oberschwaben-Zoom.",
    },
    {
        "order": 8,
        "state": "oberschwaben-handoff",
        "kicker": "08 / Oberschwaben",
        "title": "Hier trifft Moorschutz auf Landwirtschaft",
        "body": "In Oberschwaben überlagern sich Moor-/Feuchtbodenkontext und heutige Nutzung. Aus Klima wird eine regionale Nutzungsfrage.",
        "base": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
        "overlay": "public/maps/oberschwaben/oberschwaben_admin_context.png",
        "label": "Oberschwaben: Nutzung × Bodenkontext",
        "note": "Der Sticky-Zoom endet dort, wo die regionale Story beginnt: bei der Überschneidung von Nutzung und Bodenkontext.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def html_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def find_section_bounds(html: str, audit: list[str]) -> tuple[int, int] | None:
    # If already integrated, replace the marked block only.
    start = html.find(HTML_START)
    end = html.find(HTML_END)
    if start >= 0 and end >= 0:
        end += len(HTML_END)
        # include enclosing section if marker starts inside it? Here marker wraps whole section.
        audit.append("OK found existing B169 marked block")
        return start, end

    anchors = [
        "Moore sind räumlich konzentriert und klimatisch wirksam",
        "Moore sind räumlich konzentriert",
        "central_global_map_story",
        "global_gpm2_peat_extent",
        "Wo liegen die Moore?",
    ]

    for anchor in anchors:
        pos = html.find(anchor)
        if pos < 0:
            continue

        section_start = html.rfind("<section", 0, pos)
        section_end = html.find("</section>", pos)

        if section_start >= 0 and section_end >= 0:
            section_end += len("</section>")
            audit.append(f"OK found central map section by anchor: {anchor}")
            return section_start, section_end

        audit.append(f"WARN anchor found but section bounds missing: {anchor}")

    audit.append("ERROR central map section not found")
    return None


def build_section() -> str:
    step_cards = []
    base_imgs = []
    overlay_imgs = []

    for i, s in enumerate(STATES):
        active = " is-active" if i == 0 else ""
        step_cards.append(f"""
          <article class="b169-step{active}" data-b169-step data-state="{html_escape(s['state'])}" tabindex="0">
            <p class="b169-step-kicker">{html_escape(s['kicker'])}</p>
            <h3>{html_escape(s['title'])}</h3>
            <p>{html_escape(s['body'])}</p>
          </article>""")

        base_imgs.append(
            f'<img src="{html_escape(s["base"])}" alt="{html_escape(s["label"])}" '
            f'data-b169-base="{html_escape(s["state"])}" class="{"is-active" if i == 0 else ""}" loading="lazy">'
        )
        overlay_imgs.append(
            f'<img src="{html_escape(s["overlay"])}" alt="{html_escape("Grenzen / Orientierung für " + s["label"])}" '
            f'data-b169-overlay="{html_escape(s["state"])}" class="{"is-active" if i == 0 else ""}" loading="lazy">'
        )

    return f"""{HTML_START}
<section id="karten" class="b169-live-sticky-zoom" data-b169-live-sticky-zoom aria-label="Kartenfolge vom globalen Moorvorkommen bis Oberschwaben">
  <div class="b169-intro">
    <p class="b169-eyebrow">Kartenfolge</p>
    <h2>Der Maßstab entscheidet</h2>
    <p>Globale Karten zeigen, warum Moore relevant sind. Regional wird sichtbar, wo Planung beginnt.</p>
  </div>

  <div class="b169-mobile-note" role="note">
    Auf kleinen Bildschirmen wird die Kartenfolge als vertikale Sequenz gelesen. Die Aussage bleibt dieselbe: vom globalen Kontext zur regionalen Nutzungsfrage.
  </div>

  <div class="b169-layout">
    <div class="b169-steps" aria-label="Scroll-Schritte der Kartenfolge">
      {''.join(step_cards)}
    </div>

    <div class="b169-stage-wrap">
      <figure class="b169-stage" aria-label="Kartenbühne">
        <div class="b169-stage-label" data-b169-label>{html_escape(STATES[0]['label'])}</div>
        {"".join(base_imgs)}
        {"".join(overlay_imgs)}
        <figcaption class="b169-annotation" data-b169-annotation>{html_escape(STATES[0]['note'])}</figcaption>
      </figure>
    </div>
  </div>

  <p class="b169-source-line">
    Datenbasis: Global Peatland Map 2.0, FAOSTAT, Thünen-Kulisse organischer Böden, BK50 Baden-Württemberg und eigene kartografische Aufbereitung.
    <a href="#methode-in-kuerze">Methode in Kürze</a>.
  </p>
</section>
{HTML_END}"""


def patch_html(html: str, audit: list[str]) -> str:
    bounds = find_section_bounds(html, audit)
    if not bounds:
        raise SystemExit("Could not find central map section for B169 integration.")

    start, end = bounds
    section = build_section()
    html = html[:start] + section + "\n" + html[end:]

    if JS_REF not in html:
        body_close = html.rfind("</body>")
        if body_close >= 0:
            html = html[:body_close] + "  " + JS_REF + "\n" + html[body_close:]
            audit.append("OK inserted B169 script reference before </body>")
        else:
            html = html.rstrip() + "\n" + JS_REF + "\n"
            audit.append("WARN </body> not found; appended B169 script reference at EOF")
    else:
        audit.append("OK B169 script reference already present")

    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b169-live-sticky-zoom {{
  --b169-bg: #f4eee2;
  --b169-dark: #07120d;
  --b169-ink: #1c2a22;
  --b169-muted: #66746a;
  --b169-card: rgba(8, 18, 13, 0.88);
  --b169-accent: #087f7a;
  background:
    radial-gradient(circle at 72% 22%, rgba(8, 127, 122, 0.09), transparent 34rem),
    linear-gradient(180deg, rgba(244, 238, 226, 1), rgba(231, 226, 215, 0.9) 56%, rgba(244, 238, 226, 1));
  color: var(--b169-ink);
  padding: clamp(3.5rem, 7vw, 6rem) 0;
  scroll-margin-top: 5rem;
}}

.b169-intro,
.b169-mobile-note,
.b169-source-line {{
  width: min(100% - 2rem, 76rem);
  margin-inline: auto;
}}

.b169-eyebrow {{
  margin: 0 0 0.7rem;
  color: #6b7f51;
  font-size: 0.74rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.b169-intro h2 {{
  max-width: 13ch;
  margin: 0;
  color: var(--b169-ink);
  font-size: clamp(2.4rem, 5.4vw, 5.6rem);
  line-height: 0.94;
  letter-spacing: -0.06em;
  text-wrap: balance;
}}

.b169-intro p:not(.b169-eyebrow) {{
  max-width: 48rem;
  margin: 1.05rem 0 0;
  color: var(--b169-muted);
  font-size: clamp(1.05rem, 1.45vw, 1.28rem);
  line-height: 1.45;
}}

.b169-layout {{
  width: min(100% - 2rem, 86rem);
  margin: clamp(2.5rem, 5vw, 4rem) auto 0;
  display: grid;
  grid-template-columns: minmax(17rem, 23rem) minmax(0, 1fr);
  gap: clamp(1.5rem, 3.5vw, 3.5rem);
  align-items: start;
}}

.b169-steps {{
  padding: 14vh 0 26vh;
}}

.b169-step {{
  min-height: 40vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0.36;
  transition: opacity 180ms ease, transform 180ms ease;
}}

.b169-step.is-active {{
  opacity: 1;
  transform: translateX(0.35rem);
}}

.b169-step-kicker {{
  margin: 0 0 0.55rem;
  color: #8cb85f;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.b169-step h3 {{
  max-width: 13em;
  margin: 0;
  color: var(--b169-ink);
  font-size: clamp(1.55rem, 2.9vw, 2.45rem);
  line-height: 1.02;
  letter-spacing: -0.04em;
  text-wrap: balance;
}}

.b169-step p:last-child {{
  max-width: 24rem;
  margin: 0.85rem 0 0;
  color: var(--b169-muted);
  font-size: 1rem;
  line-height: 1.5;
  text-wrap: pretty;
}}

.b169-stage-wrap {{
  position: sticky;
  top: 2.25rem;
  height: calc(100vh - 4.5rem);
  min-height: 34rem;
  display: grid;
  place-items: center;
}}

.b169-stage {{
  position: relative;
  width: 100%;
  height: min(78vh, 46rem);
  min-height: 31rem;
  overflow: hidden;
  margin: 0;
  border-radius: 1.18rem;
  background: var(--b169-dark);
  border: 1px solid rgba(25, 39, 32, 0.16);
  box-shadow: 0 28px 86px rgba(25, 39, 32, 0.26);
}}

.b169-stage img {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transform: scale(1.018);
  transition: opacity 360ms ease, transform 560ms ease;
}}

.b169-stage img.is-active {{
  opacity: 1;
  transform: scale(1);
}}

.b169-stage img[data-b169-base] {{
  z-index: 1;
}}

.b169-stage img[data-b169-overlay] {{
  z-index: 2;
  mix-blend-mode: screen;
  filter: contrast(1.08) brightness(1.16);
  pointer-events: none;
}}

.b169-stage img[data-b169-overlay].is-active {{
  opacity: 0.62;
}}

.b169-stage-label {{
  position: absolute;
  z-index: 4;
  left: 1rem;
  top: 1rem;
  max-width: min(28rem, calc(100% - 2rem));
  padding: 0.72rem 0.86rem;
  border-radius: 0.75rem;
  background: rgba(8, 18, 13, 0.76);
  color: rgba(248, 245, 236, 0.94);
  font-weight: 850;
  letter-spacing: -0.02em;
  backdrop-filter: blur(10px);
}}

.b169-annotation {{
  position: absolute;
  z-index: 4;
  right: 1rem;
  bottom: 1rem;
  max-width: min(30rem, calc(100% - 2rem));
  margin: 0;
  padding: 0.8rem 0.9rem;
  border-left: 3px solid rgba(8, 127, 122, 0.85);
  border-radius: 0.75rem;
  background: rgba(248, 245, 236, 0.88);
  color: #24352c;
  font-size: 0.92rem;
  line-height: 1.42;
  box-shadow: 0 16px 42px rgba(0, 0, 0, 0.18);
}}

.b169-mobile-note {{
  display: none;
}}

.b169-source-line {{
  margin-top: 1rem;
  color: var(--b169-muted);
  font-size: 0.82rem;
  line-height: 1.45;
}}

.b169-source-line a {{
  color: inherit;
  text-underline-offset: 0.18em;
}}

@media (max-width: 860px) {{
  .b169-live-sticky-zoom {{
    padding: 3rem 0;
  }}

  .b169-layout {{
    display: block;
    width: min(100% - 1.25rem, 86rem);
    margin-top: 2rem;
  }}

  .b169-mobile-note {{
    display: block;
    margin-top: 1.25rem;
    padding: 0.85rem 0.95rem;
    border-radius: 0.85rem;
    background: rgba(255, 255, 255, 0.62);
    color: var(--b169-muted);
    font-size: 0.9rem;
    line-height: 1.45;
  }}

  .b169-steps {{
    padding: 0;
  }}

  .b169-step {{
    min-height: auto;
    padding: 1.5rem 0 0.75rem;
    opacity: 1;
    transform: none;
  }}

  .b169-stage-wrap {{
    position: static;
    height: auto;
    min-height: 0;
  }}

  .b169-stage {{
    height: auto;
    min-height: 0;
    aspect-ratio: 16 / 10;
  }}

  .b169-stage img[data-b169-overlay].is-active {{
    opacity: 0.72;
  }}

  .b169-annotation {{
    position: static;
    max-width: none;
    margin: 0.75rem 0 0;
  }}

  .b169-stage-label {{
    font-size: 0.86rem;
  }}
}}

@media (prefers-reduced-motion: reduce) {{
  .b169-stage img,
  .b169-step {{
    transition: none;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def build_js() -> str:
    return """(function () {
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-b169-live-sticky-zoom]'));
  if (!sections.length) return;

  function setState(section, state) {
    if (!state) return;

    var activeStep = section.querySelector('[data-b169-step][data-state="' + state + '"]');
    var label = section.querySelector('[data-b169-label]');
    var annotation = section.querySelector('[data-b169-annotation]');

    section.querySelectorAll('[data-b169-step]').forEach(function (step) {
      step.classList.toggle('is-active', step.getAttribute('data-state') === state);
    });

    section.querySelectorAll('[data-b169-base]').forEach(function (img) {
      img.classList.toggle('is-active', img.getAttribute('data-b169-base') === state);
    });

    section.querySelectorAll('[data-b169-overlay]').forEach(function (img) {
      img.classList.toggle('is-active', img.getAttribute('data-b169-overlay') === state);
    });

    if (label) {
      var activeImg = section.querySelector('[data-b169-base="' + state + '"]');
      label.textContent = activeImg ? activeImg.getAttribute('alt') : state;
    }

    if (annotation && activeStep) {
      var annotationText = activeStep.getAttribute('data-b169-annotation');
      if (annotationText) annotation.textContent = annotationText;
    }
  }

  sections.forEach(function (section) {
    var steps = Array.prototype.slice.call(section.querySelectorAll('[data-b169-step]'));
    if (!steps.length) return;

    // Store annotation text from the initial figcaption or fallback from hidden mapping.
    var annotationTextByState = {
      'global-peat': 'Die Karte zeigt die räumliche Konzentration von Mooren — nicht ihre lokale Nutzbarkeit.',
      'global-pressure-total': 'Gesamtwerte zeigen große Beiträge — oft dort, wo Fläche, Entwässerung und Nutzung zusammenkommen.',
      'global-pressure-density': 'Intensität und Gesamtmenge sind unterschiedliche Aussagen. Für Planung müssen beide getrennt gelesen werden.',
      'europe-bridge': 'Der regionale Blick wird erst verständlich, wenn der größere Bezugsraum steht.',
      'germany-extent': 'Die nationale Kulisse grenzt Prüfbedarf ein — sie ersetzt keine Standortprüfung.',
      'germany-types': 'Die Karte bereitet die regionale Frage vor: Welche Nutzung trifft auf welchen Bodenkontext?',
      'baden-wuerttemberg': 'Der BW-Layer ist die Brücke: nicht mehr Deutschland, noch nicht der Oberschwaben-Zoom.',
      'oberschwaben-handoff': 'Der Sticky-Zoom endet dort, wo die regionale Story beginnt: bei der Überschneidung von Nutzung und Bodenkontext.'
    };

    steps.forEach(function (step) {
      var state = step.getAttribute('data-state');
      if (annotationTextByState[state]) {
        step.setAttribute('data-b169-annotation', annotationTextByState[state]);
      }

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
})();
"""


def update_done(done_text: str, today: str) -> str:
    line = f"- B169 live sticky zoom integration prototype: integrated the repaired eight-step sticky-zoom state matrix into the live page using the existing dark map-story direction ({today})."
    if "B169 live sticky zoom integration prototype" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    missing_assets = [p for p in ASSETS if not (ROOT / p).exists()]
    if missing_assets:
        raise SystemExit("Missing required B169 assets:\n" + "\n".join(missing_assets))

    html = read(INDEX)
    css = read(CSS)

    audit.append(f"Existing B169 block before patch: {HTML_START in html and HTML_END in html}")
    audit.append(f"Existing B169 CSS before patch: {CSS_START in css and CSS_END in css}")
    audit.append(f"Existing B169 JS ref before patch: {JS_REF in html}")
    audit.append(f"Central-story script still referenced before patch: {'src/central_global_map_story.js' in html}")

    html = patch_html(html, audit)
    css = patch_css(css)
    js = build_js()

    write(INDEX, html)
    write(CSS, css)
    write(JS, js)

    with STATE_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["order", "state", "title", "base", "overlay", "label"],
        )
        writer.writeheader()
        for s in STATES:
            writer.writerow({
                "order": s["order"],
                "state": s["state"],
                "title": s["title"],
                "base": s["base"],
                "overlay": s["overlay"],
                "label": s["label"],
            })

    doc = f"""# B169 - Live Sticky Zoom Integration Prototype

Date: {today}

## Ziel

B169 integriert die reparierte B167b-State-Matrix als Live-Prototyp in die öffentliche Hauptseite.

Wichtig: Der Prototyp-HTML-Block aus `docs/prototypes` wurde nicht kopiert.
Stattdessen ersetzt B169 die bestehende zentrale Kartenfolge durch eine kompakte Live-Komponente,
die die dunkle Kartenbühnen-Richtung beibehält.

## Neue Live-Stepfolge

| Nr. | State | Aussage | Basis | Overlay |
|---:|---|---|---|---|
"""
    for s in STATES:
        doc += f"| {s['order']} | `{s['state']}` | {s['title']} | `{s['base']}` | `{s['overlay']}` |\n"

    doc += """
## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `src/b169_live_sticky_zoom.js`
- `scripts/169_live_sticky_zoom_integration_prototype.py`
- `docs/B169_live_sticky_zoom_integration_prototype.md`
- `docs/B169_live_sticky_zoom_state_matrix.csv`
- `docs/B169_live_sticky_zoom_integration_prototype_audit.txt`
- `tasks/done.md`

## Nicht geändert

- keine Änderung an Felt
- keine Änderung an der Oberschwaben-Detailkarte
- keine Änderung an Flächenbilanz
- keine Änderung an Wertschöpfungs-Scorecard
- keine neuen Datenquellen
- keine raw GIS-Dateien

## Visuelle QA

Prüfen:

1. Desktop: Sticky-Zoom scrollt sauber.
2. Global: Total- und Density-Step sind unterscheidbar.
3. Europa: politische Grenzen helfen, ohne dominant zu werden.
4. Deutschland: Extent und Types sind klar getrennt.
5. Baden-Württemberg: BW-Layer erscheint als eigene Brücke.
6. Oberschwaben: kein Deutschland-Overlay.
7. Danach funktioniert die bestehende Oberschwaben-Section ohne Dopplungsgefühl.
8. Mobile: vertikale Sequenz bleibt lesbar.

## Entscheidung nach visueller QA

Falls acht Steps zu lang wirken:

- Variante A: `global-pressure-total` streichen, Density behalten.
- Variante B: `germany-types` streichen, Germany extent behalten.

Für den ersten Live-Test bleiben alle acht Steps aktiv.
"""
    write(DOC, doc)

    audit_text = "# B169 live sticky zoom integration prototype audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Post-patch checks:\n"
    new_html = read(INDEX)
    audit_text += f"- B169 block present: {HTML_START in new_html and HTML_END in new_html}\n"
    audit_text += f"- B169 script ref present: {JS_REF in new_html}\n"
    audit_text += f"- B169 JS exists: {JS.exists()}\n"
    audit_text += f"- B169 CSS present: {CSS_START in read(CSS) and CSS_END in read(CSS)}\n"
    for s in STATES:
        audit_text += f"- state `{s['state']}` in index: {s['state'] in new_html}\n"
    audit_text += "\nResult: LIVE PROTOTYPE PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B169 live sticky zoom integration prototype complete.")
    print("Changed: index.html, src/styles.css, src/b169_live_sticky_zoom.js")
    print("Created/updated:")
    print("  docs/B169_live_sticky_zoom_integration_prototype.md")
    print("  docs/B169_live_sticky_zoom_state_matrix.csv")
    print("  docs/B169_live_sticky_zoom_integration_prototype_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA, then visual QA.")


if __name__ == "__main__":
    main()
