#!/usr/bin/env python3
"""
B100 - Add compact moor primer before the Oberschwaben implementation story

Purpose
-------
Add a short public-facing "Moore verstehen" section that explains the core
mechanism behind the atlas before the story moves into Oberschwaben:

  water level -> peat decomposition -> emissions -> implementation challenge

This section is deliberately compact. It reuses the earlier Moore_Primer logic,
but adapts it to the current editorial design and method boundary.

Placement
---------
B100 inserts the primer immediately before the first Oberschwaben regional block,
preferably before the section containing:

  "Oberschwaben: regionale Ausgangslage"

Fallbacks:
- before the B96 Oberschwaben scrolly marker
- before the first occurrence of "Oberschwaben"

Changed files
-------------
- index.html
- src/styles.css
- docs/B100_add_moor_primer_section.md
- docs/B100_moor_primer_public_readiness_audit.txt
- tasks/done.md

Not changed
-----------
- GIS data
- map PNGs
- JS logic
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B100_add_moor_primer_section.md"
AUDIT = DOCS / "B100_moor_primer_public_readiness_audit.txt"

HTML_START = "<!-- B100_MOOR_PRIMER_START -->"
HTML_END = "<!-- B100_MOOR_PRIMER_END -->"
CSS_START = "/* B100_MOOR_PRIMER_START */"
CSS_END = "/* B100_MOOR_PRIMER_END */"

OBERSCHWABEN_ANCHORS = [
    "Oberschwaben: regionale Ausgangslage",
    "<!-- B96_OBERSCHWABEN_SCROLLY_START -->",
    "Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird",
    "Oberschwaben",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    missing = [p for p in [INDEX, CSS] if not p.exists()]
    if missing:
        print("B100 cannot run. Missing files:")
        for p in missing:
            print(f"  - {rel(p)}")
        sys.exit(1)


def find_section_start_before(html: str, pos: int) -> int:
    """Return the opening <section> start that contains/starts near pos, if found."""
    # Look backwards for the nearest section opening. If it is reasonably close, use it.
    before = html[:pos]
    matches = list(re.finditer(r"<section\b[^>]*>", before, flags=re.IGNORECASE))
    if not matches:
        return pos
    last = matches[-1]
    # Use section start if there is no closing section after it before the anchor.
    tail = before[last.end():]
    if "</section>" not in tail.lower():
        return last.start()
    return pos


def remove_existing_block(html: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(HTML_START) + r".*?" + re.escape(HTML_END), re.DOTALL)
    updated, count = pattern.subn("", html)
    return updated, bool(count)


def insertion_position(html: str) -> tuple[int, str]:
    for anchor in OBERSCHWABEN_ANCHORS:
        pos = html.find(anchor)
        if pos != -1:
            if anchor == "Oberschwaben: regionale Ausgangslage":
                sec_pos = find_section_start_before(html, pos)
                return sec_pos, f"before section containing `{anchor}`"
            if anchor.startswith("<!--"):
                return pos, f"before marker `{anchor}`"
            # For generic text anchors, try to insert before containing section.
            sec_pos = find_section_start_before(html, pos)
            return sec_pos, f"before anchor `{anchor}`"

    # Fallback: after opening main tag or near top of body.
    main_match = re.search(r"<main\b[^>]*>", html, flags=re.IGNORECASE)
    if main_match:
        return main_match.end(), "after opening <main> fallback"

    body_match = re.search(r"<body\b[^>]*>", html, flags=re.IGNORECASE)
    if body_match:
        return body_match.end(), "after opening <body> fallback"

    return 0, "top-of-file fallback"


def build_html_block() -> str:
    return f"""{HTML_START}
<section id="moor-primer" class="section moore-primer-section" aria-labelledby="moor-primer-title">
  <div class="section-header moore-primer-header">
    <p class="eyebrow">Moore verstehen</p>
    <h2 id="moor-primer-title">Warum der Wasserstand der Hebel ist</h2>
    <p>
      Moore sind in der Fläche oft klein, aber im Klimasystem überproportional wichtig.
      Der Grund liegt im Torf: Er speichert Kohlenstoff nur dann dauerhaft, wenn er nass
      und sauerstoffarm bleibt.
    </p>
  </div>

  <div class="moore-primer-mechanism" aria-label="Kernmechanismus Moor und Emissionen">
    <div class="moore-primer-step">
      <span class="moore-primer-number">01</span>
      <h3>Nass bleibt Speicher</h3>
      <p>
        Unter nassen, sauerstoffarmen Bedingungen werden Pflanzenreste nur langsam
        abgebaut. Über lange Zeit entsteht Torf – ein organischer Kohlenstoffspeicher.
      </p>
    </div>
    <div class="moore-primer-arrow" aria-hidden="true">→</div>
    <div class="moore-primer-step">
      <span class="moore-primer-number">02</span>
      <h3>Drainage macht Quelle</h3>
      <p>
        Wird der Wasserstand abgesenkt, gelangt Sauerstoff in den Torfkörper. Der Torf
        mineralisiert; aus einem Speicher wird eine dauerhafte Treibhausgasquelle.
      </p>
    </div>
    <div class="moore-primer-arrow" aria-hidden="true">→</div>
    <div class="moore-primer-step">
      <span class="moore-primer-number">03</span>
      <h3>Umsetzung wird Verhandlung</h3>
      <p>
        Wasserstände lassen sich selten schlagweise denken. Nutzung, Nachbarschaft,
        Gräben, Technik, Förderung und Wertschöpfung müssen zusammen geplant werden.
      </p>
    </div>
  </div>

  <div class="moore-primer-grid">
    <article class="moore-primer-card">
      <h3>Niedermoor oder Hochmoor?</h3>
      <p>
        Für die landwirtschaftliche Transformationsfrage sind häufig Niedermoore und
        Feuchtbodenkomplexe zentral: grundwasserbeeinflusst, historisch entwässert und
        vielerorts in Nutzung. Hochmoore sind stärker niederschlagsgeprägt, nährstoffarm
        und ökologisch besonders empfindlich.
      </p>
    </article>

    <article class="moore-primer-card">
      <h3>Was entscheidet über Nutzung?</h3>
      <p>
        Drei Fragen sind entscheidend: Wie hoch steht das Wasser? Wie stark ist der
        Torfkörper degradiert? Welche Nährstoff- und Standortbedingungen liegen vor?
        Erst daraus ergeben sich realistische Pfade: Nassgrünland, Paludikultur,
        Renaturierung, Moor-PV oder Kombinationen.
      </p>
    </article>

    <article class="moore-primer-card moore-primer-card--rule">
      <h3>Merksatz</h3>
      <p>
        Wasserstand steuert Torfabbau. Torfabbau steuert Emissionen. Umsetzbarkeit
        entsteht durch Koordination, Akzeptanz und Wertschöpfung.
      </p>
    </article>
  </div>

  <p class="moore-source-line moore-primer-source">
    Fachlicher Hintergrund: kompakte Auswertung der Moor-, Paludikultur- und
    SOLAMO-BW-Arbeitsgrundlagen; diese Sektion erklärt den Mechanismus und ersetzt
    keine standortbezogene hydrologische oder betriebliche Prüfung.
  </p>
</section>
{HTML_END}"""


def insert_block(html: str, block: str) -> tuple[str, str]:
    html, replaced = remove_existing_block(html)
    pos, anchor_msg = insertion_position(html)
    updated = html[:pos].rstrip() + "\n\n" + block + "\n\n" + html[pos:].lstrip()
    action = f"replaced existing B100 block and inserted {anchor_msg}" if replaced else f"inserted {anchor_msg}"
    return updated, action


def build_css_block() -> str:
    return f"""{CSS_START}
.moore-primer-section {{
  position: relative;
  padding-top: clamp(4rem, 7vw, 7rem);
  padding-bottom: clamp(4rem, 7vw, 7rem);
  background:
    radial-gradient(circle at 14% 8%, rgba(113, 139, 104, 0.12), transparent 32rem),
    radial-gradient(circle at 86% 20%, rgba(65, 105, 96, 0.10), transparent 30rem);
}}

.moore-primer-header {{
  max-width: 960px;
}}

.moore-primer-header h2 {{
  max-width: 880px;
}}

.moore-primer-header p {{
  max-width: 820px;
}}

.moore-primer-mechanism {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto clamp(1.5rem, 3vw, 2.2rem);
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr) auto minmax(0, 1fr);
  gap: clamp(0.8rem, 1.8vw, 1.2rem);
  align-items: stretch;
}}

.moore-primer-step {{
  padding: clamp(1rem, 2vw, 1.45rem);
  border: 1px solid rgba(46, 68, 55, 0.14);
  border-radius: 1.15rem;
  background: rgba(255, 252, 244, 0.78);
  box-shadow: 0 0.9rem 2.4rem rgba(35, 45, 38, 0.08);
}}

.moore-primer-number {{
  display: inline-block;
  margin-bottom: 0.65rem;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  color: rgba(70, 103, 80, 0.62);
}}

.moore-primer-step h3 {{
  margin: 0 0 0.65rem;
  font-size: clamp(1.05rem, 1.5vw, 1.3rem);
  line-height: 1.15;
  color: rgba(29, 38, 32, 0.94);
}}

.moore-primer-step p {{
  margin: 0;
  color: rgba(45, 57, 50, 0.78);
  line-height: 1.55;
}}

.moore-primer-arrow {{
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(67, 100, 80, 0.42);
  font-size: clamp(1.4rem, 3vw, 2.1rem);
}}

.moore-primer-grid {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.1fr 1.1fr 0.9fr;
  gap: clamp(1rem, 2vw, 1.4rem);
}}

.moore-primer-card {{
  padding: clamp(1.05rem, 2vw, 1.45rem);
  border: 1px solid rgba(44, 62, 52, 0.14);
  border-radius: 1.15rem;
  background: rgba(246, 249, 241, 0.74);
  box-shadow: 0 0.75rem 2rem rgba(34, 43, 37, 0.07);
}}

.moore-primer-card h3 {{
  margin: 0 0 0.7rem;
  font-size: clamp(1.05rem, 1.45vw, 1.25rem);
  line-height: 1.18;
  letter-spacing: -0.02em;
  color: rgba(31, 42, 35, 0.94);
}}

.moore-primer-card p {{
  margin: 0;
  color: rgba(48, 60, 53, 0.78);
  line-height: 1.55;
}}

.moore-primer-card--rule {{
  background: rgba(237, 247, 241, 0.82);
  border-color: rgba(52, 106, 92, 0.22);
}}

.moore-primer-source {{
  width: min(1120px, calc(100% - 2rem));
  margin: clamp(1rem, 2vw, 1.5rem) auto 0;
  color: rgba(65, 78, 70, 0.62) !important;
}}

@media (max-width: 1000px) {{
  .moore-primer-mechanism {{
    grid-template-columns: 1fr;
  }}

  .moore-primer-arrow {{
    transform: rotate(90deg);
    min-height: 1.2rem;
  }}

  .moore-primer-grid {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 640px) {{
  .moore-primer-step,
  .moore-primer-card {{
    border-radius: 0.9rem;
  }}
}}
{CSS_END}"""


def insert_css(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B100 CSS block"
    return css.rstrip() + "\n\n" + block + "\n", "appended B100 CSS block"


def write_report(today: str, html_action: str, css_action: str) -> None:
    md = f"""# B100 - Add Moor Primer Section

Date: {today}

## Result

B100 added a compact public-facing `Moore verstehen` primer before the
Oberschwaben implementation story.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B100_add_moor_primer_section.md`
- `docs/B100_moor_primer_public_readiness_audit.txt`
- `tasks/done.md`

## Actions

- HTML: {html_action}
- CSS: {css_action}

## Editorial role

The section explains the core mechanism:

```text
Wasserstand -> Torfabbau -> Emissionen -> Umsetzungsfrage
```

It reuses the earlier moor primer logic but adapts it to the current public
story and design. It avoids turning the page into a textbook and keeps the
method boundary explicit.

## Content choices

- Defines peat/moor mechanism in functional terms.
- Explains why Niedermoor-/Feuchtbodenkontexte matter for agricultural transition.
- Links water level, degradation, nutrients and site conditions to realistic use paths.
- Keeps suitability and prioritization claims out of the public copy.

## Next step

B101 should add a compact Oberschwaben B98c key-figures capsule, using rounded
class proportions rather than exact public hectare claims.
"""
    write_text(REPORT, md)


def audit(html: str) -> str:
    checks = {
        "B100 marker start": HTML_START in html,
        "B100 marker end": HTML_END in html,
        "moor-primer id": 'id="moor-primer"' in html,
        "Wasserstand": "Wasserstand" in html,
        "Torfabbau": "Torfabbau" in html,
        "keine standortbezogene": "keine standortbezogene" in html,
        "Oberschwaben appears after primer": html.find("Oberschwaben") > html.find(HTML_START) if HTML_START in html and "Oberschwaben" in html else False,
    }
    lines = [
        "# B100 moor primer public-readiness audit",
        "",
        "## Checks",
        "",
    ]
    for k, v in checks.items():
        lines.append(f"- {k}: {'OK' if v else 'MISSING'}")

    lines.extend([
        "",
        "## Manual visual review",
        "",
        "- Primer should appear before the Oberschwaben regional implementation story.",
        "- Section should be compact and not interrupt the scale-sequence too heavily.",
        "- Mechanism cards should not feel like a technical textbook.",
        "- Mobile layout should stack cleanly.",
        "",
    ])
    return "\n".join(lines)


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B100 - Add moor primer section"
    if marker in current:
        return

    entry = f"""
## B100 - Add moor primer section ({today})

- Added a compact `Moore verstehen` primer before the Oberschwaben implementation story.
- Explained the water-level / peat-decomposition / emissions mechanism.
- Added functional Niedermoor/Hochmoor and use-path context without creating suitability claims.
- Added `docs/B100_add_moor_primer_section.md`.
- Added `docs/B100_moor_primer_public_readiness_audit.txt`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    html = read_text(INDEX)
    css = read_text(CSS)

    new_html, html_action = insert_block(html, build_html_block())
    new_css, css_action = insert_css(css, build_css_block())

    write_text(INDEX, new_html)
    write_text(CSS, new_css)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    write_report(today, html_action, css_action)
    write_text(AUDIT, audit(new_html))
    update_done(today)

    print("B100 moor primer section complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Actions:")
    print(f"  HTML: {html_action}")
    print(f"  CSS: {css_action}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B100_moor_primer_public_readiness_audit.txt")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
