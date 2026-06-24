#!/usr/bin/env python3
"""
B96 - Bind Oberschwaben scrolly layer stack into the German presentation page.

Purpose
-------
Adds a scrollable, sticky layer-stack module for Oberschwaben based on the four
B95h-validated PNG assets:

- public/maps/oberschwaben/oberschwaben_admin_context.png
- public/maps/oberschwaben/oberschwaben_agriculture.png
- public/maps/oberschwaben/oberschwaben_moor_context.png
- public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png

Design decision
---------------
This replaces the earlier idea of a single scientific-style composite map.
The web module follows the existing story-map logic:
Region -> agriculture -> moor/wetland soil context -> intersection -> method boundary.

This script is idempotent:
- Re-running it replaces the B96 HTML/CSS/JS blocks instead of duplicating them.
- It does not touch raw GIS data.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

INDEX = ROOT / "index.html"
CSS_PRIMARY = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
REPORT = DOCS / "B96_bind_oberschwaben_scrolly_layer_stack.md"

REQUIRED_ASSETS = [
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_admin_context.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_agriculture.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_moor_context.png",
    ROOT / "public" / "maps" / "oberschwaben" / "oberschwaben_agriculture_moor_intersection.png",
]

HTML_START = "<!-- B96_OBERSCHWABEN_SCROLLY_START -->"
HTML_END = "<!-- B96_OBERSCHWABEN_SCROLLY_END -->"
CSS_START = "/* B96_OBERSCHWABEN_SCROLLY_START */"
CSS_END = "/* B96_OBERSCHWABEN_SCROLLY_END */"
JS_START = "<!-- B96_OBERSCHWABEN_SCROLLY_JS_START -->"
JS_END = "<!-- B96_OBERSCHWABEN_SCROLLY_JS_END -->"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_block(text: str, start: str, end: str, block: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text), True
    return text, False


def choose_css_file() -> Path:
    if CSS_PRIMARY.exists():
        return CSS_PRIMARY
    css_files = sorted((ROOT / "src").glob("*.css")) if (ROOT / "src").exists() else []
    if css_files:
        return css_files[0]
    return CSS_PRIMARY


def assert_required_files() -> None:
    missing = [p for p in REQUIRED_ASSETS if not p.exists()]
    if missing:
        print("B96 cannot run. Required layer assets are missing:")
        for p in missing:
            print(f"  - {rel(p)}")
        print("\nRun B95h again after exporting/copying the missing PNGs.")
        sys.exit(1)

    if not INDEX.exists():
        print(f"B96 cannot run. Missing {rel(INDEX)}")
        sys.exit(1)


def build_html_block() -> str:
    return f"""{HTML_START}
<section id="oberschwaben-layer-story" class="moore-ob-section" data-oberschwaben-state="region" aria-labelledby="oberschwaben-layer-title">
  <div class="moore-ob-heading">
    <p class="moore-ob-kicker">Regionale Umsetzung</p>
    <h2 id="oberschwaben-layer-title">Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird</h2>
    <p class="moore-ob-lead">
      Die regionale Karte zerlegt den Zusammenhang in einzelne Ebenen: Verwaltungsraum,
      landwirtschaftliche Nutzung, Moor-/Feuchtbodenkontext und ihre räumliche Überschneidung.
    </p>
  </div>

  <div class="moore-ob-grid">
    <div class="moore-ob-stage-column" aria-label="Oberschwaben Layerkarte">
      <figure class="moore-ob-stage">
        <img class="moore-ob-layer moore-ob-layer--agriculture" data-ob-layer="agriculture" src="public/maps/oberschwaben/oberschwaben_agriculture.png" alt="Landwirtschaftliche Nutzung in Oberschwaben mit Ackerland, Grünland und Dauerkultur">
        <img class="moore-ob-layer moore-ob-layer--moor" data-ob-layer="moor" src="public/maps/oberschwaben/oberschwaben_moor_context.png" alt="BK50 Moor- und Feuchtbodenkontext in Oberschwaben">
        <img class="moore-ob-layer moore-ob-layer--intersection" data-ob-layer="intersection" src="public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png" alt="Schnittmenge aus landwirtschaftlicher Nutzung und Moor- beziehungsweise Feuchtbodenkontext">
        <img class="moore-ob-layer moore-ob-layer--admin" data-ob-layer="admin" src="public/maps/oberschwaben/oberschwaben_admin_context.png" alt="Landkreisgrenzen und Landkreisnamen: Biberach, Ravensburg, Sigmaringen und Bodenseekreis">
      </figure>

      <div class="moore-ob-legend" aria-label="Legende Oberschwaben">
        <span class="moore-ob-legend-item"><i class="moore-ob-swatch moore-ob-swatch--acker"></i>Ackerland</span>
        <span class="moore-ob-legend-item"><i class="moore-ob-swatch moore-ob-swatch--gruenland"></i>Grünland</span>
        <span class="moore-ob-legend-item"><i class="moore-ob-swatch moore-ob-swatch--dauerkultur"></i>Dauerkultur</span>
        <span class="moore-ob-legend-item"><i class="moore-ob-swatch moore-ob-swatch--moor"></i>Moor-/Feuchtbodenkontext</span>
        <span class="moore-ob-legend-item"><i class="moore-ob-swatch moore-ob-swatch--intersection"></i>Schnittmenge</span>
      </div>
    </div>

    <div class="moore-ob-steps" aria-label="Scrollschritte Oberschwaben">
      <article class="moore-ob-step is-active" data-ob-step data-state="region">
        <p class="moore-ob-step-label">1 / Region</p>
        <h3>Ein regionaler Umsetzungsraum</h3>
        <p>
          Der Blick richtet sich auf vier Landkreise in Oberschwaben: Biberach, Ravensburg,
          Sigmaringen und den Bodenseekreis. Die Karte beginnt bewusst mit Orientierung,
          nicht mit Bewertung.
        </p>
      </article>

      <article class="moore-ob-step" data-ob-step data-state="agriculture">
        <p class="moore-ob-step-label">2 / Nutzung</p>
        <h3>Landwirtschaftliche Nutzung ist räumlich differenziert</h3>
        <p>
          Ackerland, Grünland und Dauerkulturen bilden unterschiedliche Produktionsräume.
          Für regionale Moorschutzstrategien ist diese Nutzungskulisse ein Ausgangspunkt,
          aber noch keine Aussage über Eignung oder Priorität.
        </p>
      </article>

      <article class="moore-ob-step" data-ob-step data-state="moor-context">
        <p class="moore-ob-step-label">3 / Bodenkontext</p>
        <h3>Der Moor-/Feuchtbodenkontext liegt quer zur Nutzung</h3>
        <p>
          Die BK50-basierte Ebene ordnet Moor- und Feuchtbodenkontexte räumlich ein.
          Sie zeigt, wo bodenkundliche Ausgangsbedingungen mit bestehenden Nutzungsräumen
          zusammenfallen können.
        </p>
      </article>

      <article class="moore-ob-step" data-ob-step data-state="intersection">
        <p class="moore-ob-step-label">4 / Schnittmenge</p>
        <h3>Hier wird Moorschutz zur Umsetzungsfrage</h3>
        <p>
          Die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext
          markiert Räume, in denen Transformationsfragen konkret werden: Bewirtschaftung,
          Wasserstand, Betriebslogik, Förderung und regionale Abstimmung.
        </p>
      </article>

      <article class="moore-ob-step moore-ob-step--boundary" data-ob-step data-state="method-boundary">
        <p class="moore-ob-step-label">5 / Grenze der Aussage</p>
        <h3>Einordnung, nicht Priorisierung</h3>
        <p>
          Die Karte zeigt eine räumliche Einordnung der Überschneidung von landwirtschaftlicher
          Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzt keine Flächeneignungsprüfung,
          keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
        </p>
      </article>
    </div>
  </div>
</section>
{HTML_END}"""


def build_css_block() -> str:
    return f"""{CSS_START}
.moore-ob-section {{
  padding: clamp(4rem, 7vw, 7rem) 0;
  color: var(--text, #1f2622);
}}

.moore-ob-heading {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto clamp(2rem, 4vw, 3.5rem);
}}

.moore-ob-kicker {{
  margin: 0 0 0.5rem;
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted, #68736c);
}}

.moore-ob-heading h2 {{
  max-width: 820px;
  margin: 0;
  font-size: clamp(2rem, 4.5vw, 4.2rem);
  line-height: 0.98;
  letter-spacing: -0.045em;
}}

.moore-ob-lead {{
  max-width: 760px;
  margin: 1.25rem 0 0;
  font-size: clamp(1rem, 1.4vw, 1.22rem);
  line-height: 1.55;
  color: var(--muted, #5f6b63);
}}

.moore-ob-grid {{
  width: min(1180px, calc(100% - 2rem));
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(300px, 0.82fr);
  gap: clamp(1.5rem, 4vw, 4rem);
  align-items: start;
}}

.moore-ob-stage-column {{
  position: sticky;
  top: clamp(1rem, 9vh, 6rem);
}}

.moore-ob-stage {{
  position: relative;
  aspect-ratio: 16 / 9;
  margin: 0;
  overflow: hidden;
  border-radius: 1.2rem;
  background:
    radial-gradient(circle at 20% 18%, rgba(255,255,255,0.92), rgba(255,255,255,0) 38%),
    linear-gradient(135deg, #f3f0e7 0%, #e7e4d8 100%);
  box-shadow: 0 1.4rem 4rem rgba(34, 45, 38, 0.16);
  border: 1px solid rgba(54, 69, 60, 0.12);
}}

.moore-ob-layer {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0;
  transition: opacity 520ms ease, filter 520ms ease;
  will-change: opacity;
}}

.moore-ob-layer--admin {{
  opacity: 0.92;
  z-index: 40;
  pointer-events: none;
}}

.moore-ob-layer--agriculture {{ z-index: 10; }}
.moore-ob-layer--moor {{ z-index: 20; }}
.moore-ob-layer--intersection {{ z-index: 30; }}

.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="region"] [data-ob-layer="intersection"] {{
  opacity: 0;
}}

.moore-ob-section[data-oberschwaben-state="agriculture"] [data-ob-layer="agriculture"] {{
  opacity: 0.9;
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="agriculture"] {{
  opacity: 0.52;
  filter: saturate(0.88);
}}

.moore-ob-section[data-oberschwaben-state="moor-context"] [data-ob-layer="moor"] {{
  opacity: 0.84;
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="agriculture"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="agriculture"] {{
  opacity: 0.34;
  filter: saturate(0.72);
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="moor"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="moor"] {{
  opacity: 0.35;
}}

.moore-ob-section[data-oberschwaben-state="intersection"] [data-ob-layer="intersection"],
.moore-ob-section[data-oberschwaben-state="method-boundary"] [data-ob-layer="intersection"] {{
  opacity: 0.96;
}}

.moore-ob-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem 0.9rem;
  margin-top: 0.9rem;
  font-size: 0.78rem;
  line-height: 1.25;
  color: var(--muted, #5f6b63);
}}

.moore-ob-legend-item {{
  display: inline-flex;
  align-items: center;
  gap: 0.38rem;
  white-space: nowrap;
}}

.moore-ob-swatch {{
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 999px;
  display: inline-block;
  border: 1px solid rgba(31, 38, 34, 0.18);
}}

.moore-ob-swatch--acker {{ background: #b99057; }}
.moore-ob-swatch--gruenland {{ background: #7f9d62; }}
.moore-ob-swatch--dauerkultur {{ background: #8e6a91; }}
.moore-ob-swatch--moor {{ background: #69a8a5; }}
.moore-ob-swatch--intersection {{ background: #214f53; }}

.moore-ob-steps {{
  display: grid;
  gap: clamp(1.4rem, 4vh, 3rem);
  padding-bottom: 18vh;
}}

.moore-ob-step {{
  min-height: clamp(280px, 46vh, 520px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(1.15rem, 2.3vw, 1.8rem);
  border-radius: 1rem;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(48, 63, 55, 0.12);
  box-shadow: 0 0.7rem 2rem rgba(39, 52, 45, 0.06);
  opacity: 0.56;
  transform: translateY(0.35rem);
  transition: opacity 260ms ease, transform 260ms ease, background 260ms ease;
}}

.moore-ob-step.is-active {{
  opacity: 1;
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.9);
}}

.moore-ob-step-label {{
  margin: 0 0 0.55rem;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted, #68736c);
}}

.moore-ob-step h3 {{
  margin: 0;
  font-size: clamp(1.25rem, 2vw, 1.8rem);
  line-height: 1.08;
  letter-spacing: -0.025em;
}}

.moore-ob-step p:not(.moore-ob-step-label) {{
  margin: 0.85rem 0 0;
  line-height: 1.55;
  color: var(--muted, #5f6b63);
}}

.moore-ob-step--boundary {{
  border-color: rgba(33, 79, 83, 0.32);
  background: rgba(244, 248, 246, 0.92);
}}

@media (max-width: 900px) {{
  .moore-ob-grid {{
    grid-template-columns: 1fr;
  }}

  .moore-ob-stage-column {{
    position: sticky;
    top: 0.75rem;
    z-index: 2;
  }}

  .moore-ob-step {{
    min-height: 42vh;
  }}
}}

@media (prefers-reduced-motion: reduce) {{
  .moore-ob-layer,
  .moore-ob-step {{
    transition: none;
  }}
}}
{CSS_END}"""


def build_js_block() -> str:
    return f"""{JS_START}
<script>
(function () {{
  var sections = document.querySelectorAll('[data-oberschwaben-state]');
  if (!sections.length) return;

  function setState(section, state) {{
    if (!state) return;
    section.setAttribute('data-oberschwaben-state', state);
    section.querySelectorAll('[data-ob-step]').forEach(function (step) {{
      step.classList.toggle('is-active', step.getAttribute('data-state') === state);
    }});
  }}

  sections.forEach(function (section) {{
    var steps = Array.prototype.slice.call(section.querySelectorAll('[data-ob-step]'));
    if (!steps.length) return;

    setState(section, steps[0].getAttribute('data-state'));

    if (!('IntersectionObserver' in window)) {{
      steps.forEach(function (step) {{
        step.addEventListener('mouseenter', function () {{
          setState(section, step.getAttribute('data-state'));
        }});
        step.addEventListener('focusin', function () {{
          setState(section, step.getAttribute('data-state'));
        }});
      }});
      return;
    }}

    var observer = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{
        if (entry.isIntersecting) {{
          setState(section, entry.target.getAttribute('data-state'));
        }}
      }});
    }}, {{
      root: null,
      rootMargin: '-34% 0px -48% 0px',
      threshold: 0.01
    }});

    steps.forEach(function (step) {{
      observer.observe(step);
    }});
  }});
}})();
</script>
{JS_END}"""


def insert_html(index_text: str, html_block: str) -> tuple[str, str]:
    updated, replaced = replace_block(index_text, HTML_START, HTML_END, html_block)
    if replaced:
        return updated, "replaced existing B96 HTML block"

    # Prefer insertion before the closing main tag so the section remains part of main content.
    match = re.search(r"</main\s*>", index_text, flags=re.IGNORECASE)
    if match:
        pos = match.start()
        return index_text[:pos].rstrip() + "\n\n" + html_block + "\n\n" + index_text[pos:], "inserted B96 HTML before </main>"

    # Fallback: before body close.
    match = re.search(r"</body\s*>", index_text, flags=re.IGNORECASE)
    if match:
        pos = match.start()
        return index_text[:pos].rstrip() + "\n\n" + html_block + "\n\n" + index_text[pos:], "inserted B96 HTML before </body>"

    return index_text.rstrip() + "\n\n" + html_block + "\n", "appended B96 HTML at end of index.html"


def insert_css(css_text: str, css_block: str) -> tuple[str, str]:
    updated, replaced = replace_block(css_text, CSS_START, CSS_END, css_block)
    if replaced:
        return updated, "replaced existing B96 CSS block"
    return css_text.rstrip() + "\n\n" + css_block + "\n", "appended B96 CSS block"


def insert_js(index_text: str, js_block: str) -> tuple[str, str]:
    updated, replaced = replace_block(index_text, JS_START, JS_END, js_block)
    if replaced:
        return updated, "replaced existing B96 JS block"

    match = re.search(r"</body\s*>", index_text, flags=re.IGNORECASE)
    if match:
        pos = match.start()
        return index_text[:pos].rstrip() + "\n\n" + js_block + "\n\n" + index_text[pos:], "inserted B96 JS before </body>"

    return index_text.rstrip() + "\n\n" + js_block + "\n", "appended B96 JS at end of index.html"


def update_done(today: str) -> None:
    TASKS.mkdir(exist_ok=True)
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B96 - Bind Oberschwaben scrolly layer stack"
    if marker in current:
        return

    entry = f"""
## B96 - Bind Oberschwaben scrolly layer stack ({today})

- Added Oberschwaben scrollable layer-stack section to `index.html`.
- Added B96-specific CSS for sticky stage, PNG layer opacity states and story cards.
- Added a small self-contained IntersectionObserver script in `index.html`.
- Used B95h layer assets:
  - `public/maps/oberschwaben/oberschwaben_admin_context.png`
  - `public/maps/oberschwaben/oberschwaben_agriculture.png`
  - `public/maps/oberschwaben/oberschwaben_moor_context.png`
  - `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_report(today: str, css_file: Path, actions: list[str]) -> None:
    DOCS.mkdir(exist_ok=True)
    md = f"""# B96 - Bind Oberschwaben Scrolly Layer Stack

Date: {today}

## Result

B96 inserted a scrollable Oberschwaben layer-stack module into the German presentation page.

## Changed files

- `index.html`
- `{rel(css_file)}`
- `docs/B96_bind_oberschwaben_scrolly_layer_stack.md`
- `tasks/done.md`

## Assets used

- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

## Actions

{chr(10).join(f"- {a}" for a in actions)}

## Story states

1. `region` — Landkreisrahmen and labels only.
2. `agriculture` — agricultural use layer fades in.
3. `moor-context` — BK50 Moor-/Feuchtbodenkontext fades in.
4. `intersection` — intersection layer is emphasized while context layers are dimmed.
5. `method-boundary` — intersection remains visible and the method boundary is explicit.

## Method boundary

The section states that the map is a spatial contextualisation only and not a suitability map,
priority map or farm-level affectedness analysis.

## QA recommendation

Run:

```powershell
python scripts\\95h_validate_oberschwaben_layer_stack.py
python scripts\\58_visual_qa_and_commit_check.py
```

Then inspect the page locally and check the deployed GitHub Pages version after push.
"""
    write_text(REPORT, md)


def main() -> None:
    assert_required_files()

    today = date.today().isoformat()
    css_file = choose_css_file()
    css_file.parent.mkdir(exist_ok=True)

    actions: list[str] = []

    index_text = read_text(INDEX)
    index_text, action_html = insert_html(index_text, build_html_block())
    actions.append(action_html)
    index_text, action_js = insert_js(index_text, build_js_block())
    actions.append(action_js)
    write_text(INDEX, index_text)

    css_text = read_text(css_file) if css_file.exists() else ""
    css_text, action_css = insert_css(css_text, build_css_block())
    actions.append(f"{action_css} in `{rel(css_file)}`")
    write_text(css_file, css_text)

    write_report(today, css_file, actions)
    update_done(today)

    print("B96 Oberschwaben scrolly layer-stack binding complete.")
    print("Changed/created:")
    for p in [INDEX, css_file, REPORT, DONE]:
      print(f"  {rel(p)}")
    print("\nNext:")
    print("  python scripts\\95h_validate_oberschwaben_layer_stack.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
