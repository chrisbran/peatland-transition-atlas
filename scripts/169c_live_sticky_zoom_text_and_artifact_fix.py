from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
JS = ROOT / "src" / "b169_live_sticky_zoom.js"

SCRIPT = ROOT / "scripts" / "169c_live_sticky_zoom_text_and_artifact_fix.py"
DOC = ROOT / "docs" / "B169c_live_sticky_zoom_text_and_artifact_fix.md"
CSV_OUT = ROOT / "docs" / "B169c_live_sticky_zoom_state_matrix.csv"
AUDIT = ROOT / "docs" / "B169c_live_sticky_zoom_text_and_artifact_fix_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
HTML_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"
CSS_START = "/* B169_LIVE_STICKY_ZOOM_START */"
CSS_END = "/* B169_LIVE_STICKY_ZOOM_END */"
CSS_B169B_START = "/* B169B_LIVE_STICKY_ZOOM_ANNOTATION_FIX_START */"
CSS_B169B_END = "/* B169B_LIVE_STICKY_ZOOM_ANNOTATION_FIX_END */"

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
        "title": "Hier trifft Moorschutz auf Landwirtschaft",
        "body": "In Oberschwaben überlagern sich Moor-/Feuchtbodenkontext und heutige Nutzung. Aus Klima wird eine regionale Nutzungsfrage.",
        "base": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
        # Important: no admin overlay here. The county labels looked like artifacts in the live zoom.
        "overlay": "",
        "label": "Oberschwaben: Nutzung × Bodenkontext",
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


def replace_b169_block(html: str) -> tuple[str, list[str]]:
    audit = []
    start = html.find(HTML_START)
    end = html.find(HTML_END)
    if start < 0 or end < 0:
        raise SystemExit("B169 marked block not found. Run B169 before B169c.")
    end += len(HTML_END)
    old_block = html[start:end]
    audit.append(f"Old B169 block length: {len(old_block)}")
    audit.append(f"Old annotation figcaption present: {'b169-annotation' in old_block}")
    audit.append(f"Old oberschwaben overlay present: {'data-b169-overlay=\"oberschwaben-handoff\"' in old_block}")

    new_block = build_section()
    html = html[:start] + new_block + "\n" + html[end:]
    audit.append(f"New B169 block length: {len(new_block)}")
    return html, audit


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


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    css = strip_block(css, CSS_B169B_START, CSS_B169B_END)

    block = f"""
{CSS_START}
/* B169c live sticky zoom: one numbered text rail, no separate map annotation, no lateral jump. */
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
    labels = ",\n      ".join([f"'{s['state']}': '{s['label'].replace(chr(39), '\\\\' + chr(39))}'" for s in STATES])
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
    line = f"- B169c live sticky zoom text and artifact fix: removed the separate map annotation rail, eliminated lateral step jumps, and disabled the Oberschwaben admin overlay that made county labels look like artifacts ({today})."
    if "B169c live sticky zoom text and artifact fix" in done_text:
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

    html = read(INDEX)
    css = read(CSS)

    before_global_annotation_count = html.count("Die Karte zeigt die räumliche Konzentration von Mooren")
    before_annotation_class_count = html.count("b169-annotation")
    before_oberschwaben_overlay = 'data-b169-overlay="oberschwaben-handoff"' in html

    html, block_audit = replace_b169_block(html)
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

    doc = f"""# B169c - Live Sticky Zoom Text and Artifact Fix

Date: {today}

## Ziel

Die B169/B169b-Ansicht hatte drei sichtbare Probleme:

1. Links erschien vor `02 / Gesamt` ein unnummerierter Textblock im anderen Design.
2. Die Textsteps wirkten beim Aktivwerden so, als würden sie leicht nach links springen.
3. Im Oberschwaben-Step wirkten Landkreisnamen wie Artefakte.

B169c korrigiert diese Punkte, ohne die Statefolge zu ändern.

## Änderungen

### 1. Keine separate Kartenannotation mehr

Die schwebende Annotation unten rechts und mögliche unnummerierte Annotationstexte werden entfernt.
Die linke Textspur besteht jetzt nur noch aus nummerierten Steps:

```text
01 / Welt
02 / Gesamt
03 / Intensität
...
```

### 2. Kein seitlicher Step-Sprung

Der aktive Step wird nicht mehr per `translateX()` verschoben.
Es ändert sich nur noch die Opazität.

### 3. Oberschwaben-Overlay deaktiviert

Für `oberschwaben-handoff` wird kein separates Admin-Overlay mehr eingeblendet.
Die Landkreisnamen wirkten im Live-Zoom wie Artefakte und sind für den Übergabeschritt nicht nötig.
Die Detailorientierung kommt später in der regionalen Oberschwaben-Section und im Felt-Block.

## Nicht geändert

- keine neue Karte
- keine neue Statefolge
- keine neue Datenquelle
- keine Änderung an Felt
- keine Änderung an Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Prüfen

- `01 / Welt` erscheint als erster normaler Textstep.
- Kein unnummerierter Vorabtext vor `02 / Gesamt`.
- Beim Scrollen kein seitliches Springen der Textblöcke.
- Oberschwaben-Step wirkt sauberer, ohne störende Landkreisnamen.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    new_css = read(CSS)
    new_js = read(JS)
    audit = "# B169c live sticky zoom text and artifact fix audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"Global annotation text count before: {before_global_annotation_count}\n"
    audit += f"b169-annotation class count before: {before_annotation_class_count}\n"
    audit += f"Oberschwaben overlay before: {before_oberschwaben_overlay}\n\n"
    audit += "Block replacement audit:\n"
    for line in block_audit:
        audit += f"- {line}\n"

    audit += "\nPost-patch checks:\n"
    audit += f"- B169 block present: {HTML_START in new_html and HTML_END in new_html}\n"
    audit += f"- b169-annotation removed from index: {'b169-annotation' not in new_html}\n"
    audit += f"- oberschwaben overlay removed from index: {'data-b169-overlay=\"oberschwaben-handoff\"' not in new_html}\n"
    audit += f"- CSS translateX removed for active step: {'translateX' not in new_css[new_css.find(CSS_START):new_css.find(CSS_END)] if CSS_START in new_css and CSS_END in new_css else 'UNKNOWN'}\n"
    audit += f"- JS annotation handling removed: {'b169-annotation' not in new_js and 'annotationFallback' not in new_js}\n"
    audit += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B169c live sticky zoom text and artifact fix complete.")
    print("Changed: index.html, src/styles.css, src/b169_live_sticky_zoom.js")
    print("Created/updated:")
    print("  docs/B169c_live_sticky_zoom_text_and_artifact_fix.md")
    print("  docs/B169c_live_sticky_zoom_state_matrix.csv")
    print("  docs/B169c_live_sticky_zoom_text_and_artifact_fix_audit.txt")
    print("  tasks/done.md")
    print("Next: hard-refresh browser, then visual QA.")


if __name__ == "__main__":
    main()
