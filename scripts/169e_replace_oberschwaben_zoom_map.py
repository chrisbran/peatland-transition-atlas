from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
JS = ROOT / "src" / "b169_live_sticky_zoom.js"

SCRIPT = ROOT / "scripts" / "169e_replace_oberschwaben_zoom_map.py"
DOC = ROOT / "docs" / "B169e_replace_oberschwaben_zoom_map.md"
CSV_OUT = ROOT / "docs" / "B169e_live_sticky_zoom_state_matrix.csv"
AUDIT = ROOT / "docs" / "B169e_replace_oberschwaben_zoom_map_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
HTML_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"
CSS_START = "/* B169_LIVE_STICKY_ZOOM_START */"
CSS_END = "/* B169_LIVE_STICKY_ZOOM_END */"
CSS_B169D_START = "/* B169D_OBERSCHWABEN_SUBTLE_BOUNDARY_OVERLAY_START */"
CSS_B169D_END = "/* B169D_OBERSCHWABEN_SUBTLE_BOUNDARY_OVERLAY_END */"

NEW_OBERSCHWABEN_ASSET = "public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png"

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
    },
    {
        "order": 8,
        "state": "oberschwaben-handoff",
        "kicker": "08 / Oberschwaben",
        "title": "Die Region wird lesbar, die Nutzungsfrage folgt",
        "body": "Oberschwaben zeigt, wo Moor- und Feuchtbodenkontexte regional gebündelt auftreten. Im nächsten Schritt wird sichtbar, wo diese Räume auf heutige landwirtschaftliche Nutzung treffen.",
        "base": NEW_OBERSCHWABEN_ASSET,
        "overlay": "",
        "label": "Oberschwaben: Moor-/Feuchtbodenkontext",
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


def js_escape(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


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

        if s["overlay"]:
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
    start = html.find(HTML_START)
    end = html.find(HTML_END)
    if start < 0 or end < 0:
        raise SystemExit("B169 marked block not found. Run B169/B169c first.")

    end += len(HTML_END)
    old_block = html[start:end]

    audit.append(f"Old B169 block length: {len(old_block)}")
    audit.append(f"Old used intersection asset: {'oberschwaben_agriculture_moor_intersection.png' in old_block}")
    audit.append(f"Old used new no-label asset: {NEW_OBERSCHWABEN_ASSET in old_block}")
    audit.append(f"Old oberschwaben overlay present: {'data-b169-overlay=\"oberschwaben-handoff\"' in old_block}")

    new_block = build_section()
    return html[:start] + new_block + "\n" + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    css = strip_block(css, CSS_B169D_START, CSS_B169D_END)

    block = f"""
{CSS_START}
/* B169e live sticky zoom: stable numbered text rail and clean Oberschwaben handoff map. */
.b169-live-sticky-zoom {{
  --b169-bg: #f4eee2;
  --b169-dark: #07120d;
  --b169-ink: #1c2a22;
  --b169-muted: #66746a;
  --b169-accent: #087f7a;
  background:
    radial-gradient(circle at 72% 22%, rgba(8, 127, 122, 0.09), transparent 34rem),
    linear-gradient(180deg, rgba(244, 238, 226, 1), rgba(231, 226, 215, 0.9) 56%, rgba(244, 238, 226, 1));
  color: var(--b169-ink);
  padding: clamp(4rem, 7vw, 6.4rem) 0;
  scroll-margin-top: 7rem;
}}

.b169-intro,
.b169-mobile-note,
.b169-source-line {{
  width: min(100% - 2rem, 76rem);
  margin-inline: auto;
}}

.b169-intro {{
  padding-top: clamp(1.25rem, 2.5vw, 2.25rem);
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
  padding: 12vh 0 24vh;
}}

.b169-step {{
  min-height: 38vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0.34;
  transition: opacity 180ms ease;
  transform: none;
}}

.b169-step.is-active {{
  opacity: 1;
  transform: none;
}}

.b169-step-kicker {{
  margin: 0 0 0.55rem;
  color: #79a64f;
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
    scroll-margin-top: 5rem;
  }}

  .b169-intro {{
    padding-top: 0.75rem;
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
    labels = ",\n      ".join([f"'{js_escape(s['state'])}': '{js_escape(s['label'])}'" for s in STATES])
    return f"""(function () {{
  function ready(fn) {{
    if (document.readyState === 'loading') {{
      document.addEventListener('DOMContentLoaded', fn);
    }} else {{
      fn();
    }}
  }}

  ready(function () {{
    var sections = Array.prototype.slice.call(document.querySelectorAll('[data-b169-live-sticky-zoom]'));
    if (!sections.length) return;

    var labelFallback = {{
      {labels}
    }};

    function setState(section, state) {{
      if (!state) return;

      section.querySelectorAll('[data-b169-step]').forEach(function (step) {{
        var isActive = step.getAttribute('data-state') === state;
        step.classList.toggle('is-active', isActive);
        if (isActive) {{
          step.setAttribute('aria-current', 'step');
        }} else {{
          step.removeAttribute('aria-current');
        }}
      }});

      section.querySelectorAll('[data-b169-base]').forEach(function (img) {{
        img.classList.toggle('is-active', img.getAttribute('data-b169-base') === state);
      }});

      section.querySelectorAll('[data-b169-overlay]').forEach(function (img) {{
        img.classList.toggle('is-active', img.getAttribute('data-b169-overlay') === state);
      }});

      var label = section.querySelector('.b169-stage-label');
      if (label) {{
        var activeImg = section.querySelector('[data-b169-base="' + state + '"]');
        label.textContent = activeImg ? activeImg.getAttribute('alt') : (labelFallback[state] || state);
      }}
    }}

    sections.forEach(function (section) {{
      var steps = Array.prototype.slice.call(section.querySelectorAll('[data-b169-step]'));
      if (!steps.length) return;

      steps.forEach(function (step) {{
        var state = step.getAttribute('data-state');
        step.addEventListener('mouseenter', function () {{ setState(section, state); }});
        step.addEventListener('focusin', function () {{ setState(section, state); }});
      }});

      setState(section, steps[0].getAttribute('data-state'));

      if (!('IntersectionObserver' in window)) return;

      var observer = new IntersectionObserver(function (entries) {{
        entries.forEach(function (entry) {{
          if (entry.isIntersecting) {{
            setState(section, entry.target.getAttribute('data-state'));
          }}
        }});
      }}, {{
        root: null,
        rootMargin: '-36% 0px -46% 0px',
        threshold: 0.01
      }});

      steps.forEach(function (step) {{
        observer.observe(step);
      }});
    }});
  }});
}})();
"""


def update_done(done_text: str, today: str) -> str:
    line = f"- B169e replace Oberschwaben zoom map: replaced the live sticky zoom Oberschwaben handoff map with the new no-label Landkreis + Moor-/Feuchtbodenkontext asset and removed overlay hacks ({today})."
    if "B169e replace Oberschwaben zoom map" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")
    if not JS.exists():
        raise SystemExit("src/b169_live_sticky_zoom.js not found")
    if not (ROOT / NEW_OBERSCHWABEN_ASSET).exists():
        raise SystemExit(f"New Oberschwaben asset not found: {NEW_OBERSCHWABEN_ASSET}")

    html = read(INDEX)
    css = read(CSS)

    audit = []
    html = patch_html(html, audit)
    css = patch_css(css)
    js = build_js()

    write(INDEX, html)
    write(CSS, css)
    write(JS, js)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["order", "state", "title", "base", "overlay", "label"])
        writer.writeheader()
        for s in STATES:
            writer.writerow({
                "order": s["order"],
                "state": s["state"],
                "title": s["title"],
                "base": s["base"],
                "overlay": s["overlay"] or "none",
                "label": s["label"],
            })

    doc = f"""# B169e - Replace Oberschwaben Zoom Map

Date: {today}

## Ziel

B169e ersetzt im Live-Sticky-Zoom direkt die Oberschwaben-Handoff-Karte.

Neue Karte:

```text
{NEW_OBERSCHWABEN_ASSET}
```

Diese Karte zeigt bewusst:

- Landkreisgrenzen
- Moor-/Feuchtbodenkontext
- keine Labels
- keine Überlagerung mit landwirtschaftlicher Nutzung

## Warum

Die Überlagerung von Moor-/Feuchtbodenkontext und Landwirtschaft soll später in der regionalen Story ihre Rolle spielen.
Im Sticky-Zoom geht es nur um die Maßstabsbrücke:

```text
Deutschland → Baden-Württemberg → Oberschwaben als regionaler Bodenkontext
```

## Änderungen

- Oberschwaben-State nutzt jetzt `oberschwaben_landkreise_moor_nolabel.png`.
- Oberschwaben-Overlay-Hack aus B169d wird entfernt.
- Oberschwaben-Text wird angepasst:
  - nicht mehr „Moorschutz trifft Landwirtschaft“
  - sondern „Region wird lesbar, Nutzungsfrage folgt“
- JS bleibt schlank: keine Annotationen, nur Step/Image/Label-State.

## Nicht geändert

- keine neue Statefolge
- keine neue Datenquelle
- keine Änderung an Felt
- keine Änderung an der späteren Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Visuelle QA

Prüfen:

- Oberschwaben-Step zeigt Landkreisgrenzen ohne Namen.
- Moor-/Feuchtbodenkontext ist sichtbar.
- Die landwirtschaftliche Überschneidung wird noch nicht vorweggenommen.
- Keine extra Overlay-Artefakte.
- Übergang zur nachfolgenden Oberschwaben-Story bleibt logisch.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    new_css = read(CSS)
    new_js = read(JS)

    audit_text = "# B169e replace Oberschwaben zoom map audit\n\n"
    audit_text += f"Date: {today}\n\n"
    for line in audit:
        audit_text += f"- {line}\n"

    audit_text += "\nPost-patch checks:\n"
    audit_text += f"- new Oberschwaben no-label asset in index: {NEW_OBERSCHWABEN_ASSET in new_html}\n"
    audit_text += f"- old Oberschwaben intersection asset absent from B169 block: {'oberschwaben_agriculture_moor_intersection.png' not in new_html[new_html.find(HTML_START):new_html.find(HTML_END)]}\n"
    audit_text += f"- oberschwaben overlay absent from B169 block: {'data-b169-overlay=\"oberschwaben-handoff\"' not in new_html[new_html.find(HTML_START):new_html.find(HTML_END)]}\n"
    audit_text += f"- B169d CSS removed: {CSS_B169D_START not in new_css and CSS_B169D_END not in new_css}\n"
    audit_text += f"- JS label updated: {'Oberschwaben: Moor-/Feuchtbodenkontext' in new_js}\n"
    audit_text += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B169e replace Oberschwaben zoom map complete.")
    print("Changed: index.html, src/styles.css, src/b169_live_sticky_zoom.js")
    print("Created/updated:")
    print("  docs/B169e_replace_oberschwaben_zoom_map.md")
    print("  docs/B169e_live_sticky_zoom_state_matrix.csv")
    print("  docs/B169e_replace_oberschwaben_zoom_map_audit.txt")
    print("  tasks/done.md")
    print("Next: hard-refresh browser and visually check the Oberschwaben step.")


if __name__ == "__main__":
    main()
