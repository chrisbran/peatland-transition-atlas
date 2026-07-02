from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
JS = ROOT / "src" / "b169_live_sticky_zoom.js"

SCRIPT = ROOT / "scripts" / "169b_live_sticky_zoom_annotation_and_spacing_fix.py"
DOC = ROOT / "docs" / "B169b_live_sticky_zoom_annotation_and_spacing_fix.md"
AUDIT = ROOT / "docs" / "B169b_live_sticky_zoom_annotation_and_spacing_fix_audit.txt"
CSV_OUT = ROOT / "docs" / "B169b_live_sticky_zoom_annotation_matrix.csv"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
HTML_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"
CSS_START = "/* B169B_LIVE_STICKY_ZOOM_ANNOTATION_FIX_START */"
CSS_END = "/* B169B_LIVE_STICKY_ZOOM_ANNOTATION_FIX_END */"

NOTES = {
    "global-peat": "Die Karte zeigt die räumliche Konzentration von Mooren — nicht ihre lokale Nutzbarkeit.",
    "global-pressure-total": "Gesamtwerte zeigen große Beiträge — oft dort, wo Fläche, Entwässerung und Nutzung zusammenkommen.",
    "global-pressure-density": "Die Intensitätskarte zeigt den Druck pro Fläche. Sie ergänzt die Gesamtwerte, erzählt aber eine andere Geschichte.",
    "europe-bridge": "Der regionale Blick wird erst verständlich, wenn der größere Bezugsraum steht.",
    "germany-extent": "Die nationale Kulisse zeigt, wo genauer hingesehen werden muss — noch ohne regionale Nutzungsentscheidung.",
    "germany-types": "Typen, Nutzung und Wasserstand unterscheiden sich. Deshalb reicht eine Flächenkarte allein nicht aus.",
    "baden-wuerttemberg": "Der BW-Layer ist die Brücke: nicht mehr Deutschland, noch nicht der Oberschwaben-Zoom.",
    "oberschwaben-handoff": "Hier beginnt die regionale Story: Moor-/Feuchtbodenkontext und heutige landwirtschaftliche Nutzung überlagern sich.",
}

LABELS = {
    "global-peat": "Globale Moorverbreitung",
    "global-pressure-total": "Gesamt-Emissionsdruck",
    "global-pressure-density": "Emissionsintensität pro Fläche",
    "europe-bridge": "Europäischer Bezugsraum",
    "germany-extent": "Organische Böden in Deutschland",
    "germany-types": "Typen organischer Böden",
    "baden-wuerttemberg": "Baden-Württemberg: Moor-/Feuchtbodenkontext",
    "oberschwaben-handoff": "Oberschwaben: Nutzung × Bodenkontext",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def html_escape(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def js_escape(s: str) -> str:
    return str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def get_b169_block(html: str) -> tuple[int, int, str]:
    start = html.find(HTML_START)
    end = html.find(HTML_END)
    if start < 0 or end < 0:
        raise SystemExit("B169 marked live sticky zoom block not found. Run B169 first.")
    end += len(HTML_END)
    return start, end, html[start:end]


def add_article_annotations(block: str, audit: list[str]) -> str:
    for state, note in NOTES.items():
        # Find opening article tag for state.
        pattern = re.compile(r'(<article\b[^>]*data-b169-step[^>]*data-state="' + re.escape(state) + r'"[^>]*)(>)', re.I | re.S)
        m = pattern.search(block)

        # Attribute order may be reversed, so try a broader article scan if direct pattern fails.
        if not m:
            article_re = re.compile(r"<article\b[^>]*data-b169-step[^>]*>", re.I | re.S)
            found = False
            for am in article_re.finditer(block):
                tag = am.group(0)
                if f'data-state="{state}"' in tag or f"data-state='{state}'" in tag:
                    found = True
                    if "data-b169-annotation=" in tag:
                        new_tag = re.sub(
                            r'data-b169-annotation="[^"]*"',
                            f'data-b169-annotation="{html_escape(note)}"',
                            tag,
                            count=1,
                        )
                    else:
                        new_tag = tag[:-1] + f' data-b169-annotation="{html_escape(note)}">'
                    block = block[:am.start()] + new_tag + block[am.end():]
                    audit.append(f"OK article annotation set via fallback: {state}")
                    break
            if not found:
                audit.append(f"WARN article not found for annotation: {state}")
            continue

        tag = m.group(1)
        closing = m.group(2)
        full = tag + closing
        if "data-b169-annotation=" in full:
            new_full = re.sub(
                r'data-b169-annotation="[^"]*"',
                f'data-b169-annotation="{html_escape(note)}"',
                full,
                count=1,
            )
        else:
            new_full = tag + f' data-b169-annotation="{html_escape(note)}"' + closing

        block = block[:m.start()] + new_full + block[m.end():]
        audit.append(f"OK article annotation set: {state}")

    return block


def patch_initial_annotation(block: str, audit: list[str]) -> str:
    initial = NOTES["global-peat"]
    pattern = re.compile(r'(<figcaption\b[^>]*data-b169-annotation[^>]*>)(.*?)(</figcaption>)', re.I | re.S)
    block, n = pattern.subn(r"\1" + html_escape(initial) + r"\3", block, count=1)
    audit.append(f"Initial figcaption annotation replacements: {n}")
    return block


def patch_html(html: str, audit: list[str]) -> str:
    start, end, block = get_b169_block(html)
    block = add_article_annotations(block, audit)
    block = patch_initial_annotation(block, audit)
    return html[:start] + block + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
/* B169b: give the live sticky zoom more nav clearance and make annotations feel intentional. */
.b169-live-sticky-zoom {{
  scroll-margin-top: 7rem;
}}

.b169-intro {{
  padding-top: clamp(1.25rem, 2.5vw, 2.25rem);
}}

.b169-annotation {{
  max-width: min(28rem, calc(100% - 2rem));
}}

.b169-step[aria-current="step"] {{
  opacity: 1;
}}

@media (max-width: 860px) {{
  .b169-live-sticky-zoom {{
    scroll-margin-top: 5rem;
  }}

  .b169-intro {{
    padding-top: 0.75rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def build_js() -> str:
    note_items = ",\n      ".join([f"'{js_escape(k)}': '{js_escape(v)}'" for k, v in NOTES.items()])
    label_items = ",\n      ".join([f"'{js_escape(k)}': '{js_escape(v)}'" for k, v in LABELS.items()])

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

    var annotationFallback = {{
      {note_items}
    }};

    var labelFallback = {{
      {label_items}
    }};

    function setState(section, state) {{
      if (!state) return;

      var activeStep = null;

      section.querySelectorAll('[data-b169-step]').forEach(function (step) {{
        var isActive = step.getAttribute('data-state') === state;
        step.classList.toggle('is-active', isActive);
        if (isActive) {{
          step.setAttribute('aria-current', 'step');
          activeStep = step;
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

      var annotation = section.querySelector('figcaption.b169-annotation');
      if (annotation) {{
        var text = activeStep ? activeStep.getAttribute('data-b169-annotation') : '';
        annotation.textContent = text || annotationFallback[state] || '';
      }}
    }}

    sections.forEach(function (section) {{
      var steps = Array.prototype.slice.call(section.querySelectorAll('[data-b169-step]'));
      if (!steps.length) return;

      steps.forEach(function (step) {{
        var state = step.getAttribute('data-state');
        if (!step.getAttribute('data-b169-annotation') && annotationFallback[state]) {{
          step.setAttribute('data-b169-annotation', annotationFallback[state]);
        }}

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
    line = f"- B169b live sticky zoom annotation and spacing fix: embedded per-state annotations in the live sticky zoom and replaced the JS controller so the caption updates with each map state ({today})."
    if "B169b live sticky zoom annotation and spacing fix" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")
    if not JS.exists():
        raise SystemExit("src/b169_live_sticky_zoom.js not found. Run B169 first.")

    html = read(INDEX)
    css = read(CSS)

    audit.append(f"B169 block present before patch: {HTML_START in html and HTML_END in html}")
    audit.append(f"Old repeated global annotation count before patch: {html.count('Die Karte zeigt die räumliche Konzentration von Mooren')}")
    audit.append(f"Old B169b CSS present before patch: {CSS_START in css and CSS_END in css}")

    html = patch_html(html, audit)
    css = patch_css(css)
    js = build_js()

    write(INDEX, html)
    write(CSS, css)
    write(JS, js)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["state", "label", "annotation"])
        writer.writeheader()
        for state, note in NOTES.items():
            writer.writerow({"state": state, "label": LABELS.get(state, ""), "annotation": note})

    doc = f"""# B169b - Live Sticky Zoom Annotation and Spacing Fix

Date: {today}

## Ziel

B169 integriert die neue Sticky-Zoom-Logik in die Hauptseite. Die visuelle Prüfung zeigte aber ein konkretes Problem:
Die Karten und Labels wechseln, aber die Annotation unten rechts blieb teilweise beim ersten Weltkarten-Hinweis stehen.

B169b behebt genau das.

## Änderungen

### 1. Per-State-Annotationen direkt in HTML

Jeder Scroll-Step erhält eine eigene `data-b169-annotation`.

Dadurch hängt die Annotation nicht mehr nur an einer JS-Fallback-Tabelle.

### 2. JS-Controller ersetzt

`src/b169_live_sticky_zoom.js` wird robuster:

- setzt `aria-current="step"` auf den aktiven Step
- toggelt Basis- und Overlay-Bilder wie bisher
- aktualisiert Label und Annotation über den aktiven Step
- nutzt Fallbacks nur, wenn HTML-Attribute fehlen
- läuft erst nach DOM-ready

### 3. Kleine Spacing-Politur

- mehr `scroll-margin-top` für die Navigation
- etwas mehr Top-Clearance im B169-Intro
- Annotation bleibt etwas kompakter

## Nicht geändert

- keine neue Karte
- keine neue Statefolge
- keine neue Datenquelle
- keine Änderung an Felt
- keine Änderung an Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Visuelle QA

Prüfen:

1. Gesamt-Emissionsdruck zeigt nicht mehr den Weltkarten-Hinweis.
2. Intensitätskarte zeigt eigene Intensitätsannotation.
3. Europa/Deutschland/BW/Oberschwaben zeigen jeweils passende Annotationen.
4. Stage-Label oben links bleibt korrekt.
5. Nav verdeckt den Abschnittstitel nicht unangenehm.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    new_js = read(JS)
    audit_text = "# B169b live sticky zoom annotation and spacing fix audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Post-patch checks:\n"
    for state in NOTES:
        audit_text += f"- article annotation for `{state}` in index: {state in new_html and NOTES[state] in new_html}\n"
    audit_text += f"- JS uses figcaption.b169-annotation selector: {'figcaption.b169-annotation' in new_js}\n"
    audit_text += f"- JS uses aria-current: {'aria-current' in new_js}\n"
    audit_text += f"- B169b CSS present: {CSS_START in read(CSS) and CSS_END in read(CSS)}\n"
    audit_text += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B169b live sticky zoom annotation and spacing fix complete.")
    print("Changed: index.html, src/styles.css, src/b169_live_sticky_zoom.js")
    print("Created/updated:")
    print("  docs/B169b_live_sticky_zoom_annotation_and_spacing_fix.md")
    print("  docs/B169b_live_sticky_zoom_annotation_matrix.csv")
    print("  docs/B169b_live_sticky_zoom_annotation_and_spacing_fix_audit.txt")
    print("  tasks/done.md")
    print("Next: hard-refresh browser, then visual QA.")


if __name__ == "__main__":
    main()
