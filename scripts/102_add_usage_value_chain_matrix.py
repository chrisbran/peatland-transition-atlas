#!/usr/bin/env python3
"""
B102 - Add usage-path / value-chain matrix from literature and primer

Purpose
-------
Add a compact public-facing matrix that translates the abstract transformation
pathways into concrete use and value-chain logics:

- Nassgrünland / Pflegenutzung
- Nassweide / robuste Tierarten
- Schilf / Rohrkolben / Seggen
- Sphagnum / Substratpfade
- Moor-PV
- Kooperation / Flurneuordnung / Abnahme

This section is based on the earlier moor primer and SOLAMO-BW logic, but
adapted to the current editorial design. It should not become a catalogue of
recommendations. It is a "Welche Wertschöpfungslogik wäre überhaupt denkbar?"
matrix.

Placement
---------
Preferred insertion point:
  after <!-- B99_TRANSFORMATION_PATHWAYS_END -->

Fallback:
  after the closing </section> of section id="pathways"

Changed files
-------------
- index.html
- src/styles.css
- docs/B102_add_usage_value_chain_matrix.md
- docs/B102_usage_value_chain_matrix_audit.txt
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

REPORT = DOCS / "B102_add_usage_value_chain_matrix.md"
AUDIT = DOCS / "B102_usage_value_chain_matrix_audit.txt"

B99_END = "<!-- B99_TRANSFORMATION_PATHWAYS_END -->"

HTML_START = "<!-- B102_USAGE_VALUE_CHAIN_MATRIX_START -->"
HTML_END = "<!-- B102_USAGE_VALUE_CHAIN_MATRIX_END -->"
CSS_START = "/* B102_USAGE_VALUE_CHAIN_MATRIX_START */"
CSS_END = "/* B102_USAGE_VALUE_CHAIN_MATRIX_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    missing = [p for p in [INDEX, CSS] if not p.exists()]
    if missing:
        print("B102 cannot run. Missing files:")
        for p in missing:
            print(f"  - {rel(p)}")
        sys.exit(1)


def remove_existing_block(html: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(HTML_START) + r".*?" + re.escape(HTML_END), re.DOTALL)
    updated, count = pattern.subn("", html)
    return updated, count > 0


def find_section_by_id(html: str, section_id: str) -> tuple[int, int, str] | None:
    pattern = re.compile(
        r"<section\b(?=[^>]*\bid=[\"']" + re.escape(section_id) + r"[\"'])[^>]*>",
        re.IGNORECASE,
    )
    m = pattern.search(html)
    if not m:
        return None

    start = m.start()
    pos = m.end()
    depth = 1
    tag_pattern = re.compile(r"</?section\b[^>]*>", re.IGNORECASE)

    for tag in tag_pattern.finditer(html, pos):
        token = tag.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return start, tag.end(), html[start:tag.end()]
        else:
            depth += 1

    return None


def insertion_pos(html: str) -> tuple[int, str]:
    pos = html.find(B99_END)
    if pos != -1:
        return pos + len(B99_END), "after B99 Transformationspfade marker"

    found = find_section_by_id(html, "pathways")
    if found:
        return found[1], "after #pathways section fallback"

    # Last fallback: before method if present.
    method_pos = html.find('id="method')
    if method_pos != -1:
        return method_pos, "before method section fallback"

    return len(html), "end-of-file fallback"


def build_html_block() -> str:
    return f"""{HTML_START}
<section id="value-chain-matrix" class="section moore-value-section" aria-labelledby="value-chain-title">
  <div class="section-header moore-value-header">
    <p class="eyebrow">Nutzung und Wertschöpfung</p>
    <h2 id="value-chain-title">Welche Pfade aus nassen Flächen Wertschöpfung machen könnten</h2>
    <p>
      Die Transformationspfade werden erst tragfähig, wenn aus Biomasse, Pflege,
      Energie oder Flächenorganisation reale Abnahme- und Erlöslogiken entstehen.
      Die Matrix zeigt keine Empfehlung pro Standort, sondern typische Kombinationen
      aus Nutzung, Produktlogik und Engpass.
    </p>
  </div>

  <div class="moore-value-matrix" role="table" aria-label="Nutzungspfad- und Wertschöpfungsmatrix">
    <div class="moore-value-row moore-value-row--head" role="row">
      <div role="columnheader">Pfad</div>
      <div role="columnheader">Produktlogik</div>
      <div role="columnheader">Reifegrad</div>
      <div role="columnheader">Hauptengpass</div>
    </div>

    <article class="moore-value-row" role="row">
      <div class="moore-value-path" role="cell">
        <span>niedrigschwellig</span>
        <strong>Nassgrünland / Pflegenutzung</strong>
      </div>
      <div role="cell">Mahdgut, Einstreu, Pflegebiomasse, Nährstoffentzug</div>
      <div role="cell">anschlussfähig, aber oft geringe Erlöse</div>
      <div role="cell">Erntefenster, Logistik, Qualität, dauerhafte Finanzierung</div>
    </article>

    <article class="moore-value-row" role="row">
      <div class="moore-value-path" role="cell">
        <span>betriebsspezifisch</span>
        <strong>Nassweide / robuste Tierarten</strong>
      </div>
      <div role="cell">Landschaftspflege, Fleisch/Milch in Spezial- oder Direktvermarktung</div>
      <div role="cell">punktuell erprobt, nicht Standard-Milchviehlogik</div>
      <div role="cell">Tragfähigkeit, Tiergesundheit, Zaun-/Wasserführung, Arbeitswirtschaft</div>
    </article>

    <article class="moore-value-row" role="row">
      <div class="moore-value-path" role="cell">
        <span>im Aufbau</span>
        <strong>Schilf / Rohrkolben / Seggen</strong>
      </div>
      <div role="cell">Fasern, Platten, Dämmstoffe, Bau- und Materialpfade</div>
      <div role="cell">fachlich plausibel, regional noch marktabhängig</div>
      <div role="cell">Verarbeitung, Normierung, Abnahmegarantie, Rohstoffmenge</div>
    </article>

    <article class="moore-value-row" role="row">
      <div class="moore-value-path" role="cell">
        <span>spezialisiert</span>
        <strong>Sphagnum / Substratpfade</strong>
      </div>
      <div role="cell">Torfmoos-Biomasse als Substrat- oder Torfersatz-Baustein</div>
      <div role="cell">spezialisiertes Know-how, nicht flächendeckend übertragbar</div>
      <div role="cell">Standortansprüche, Etablierung, Qualität, Clusterbildung</div>
    </article>

    <article class="moore-value-row" role="row">
      <div class="moore-value-path" role="cell">
        <span>kontroverser Baustein</span>
        <strong>Moor-PV</strong>
      </div>
      <div role="cell">Energieerlös bei hohem Wasserstand und extensiver Pflege</div>
      <div role="cell">potenziell planbare Cashflows, aber hohe Qualitätsanforderungen</div>
      <div role="cell">Wasserstandsnachweis, Bodeneingriffe, Biodiversität, Landschaftsbild</div>
    </article>
  </div>

  <div class="moore-value-reality">
    <h3>Die eigentliche Engstelle liegt selten im Anbau allein</h3>
    <p>
      Verarbeitung lohnt sich erst bei ausreichender Menge. Anbau lohnt sich erst
      bei sicherer Abnahme. Nachfrage entsteht erst bei verlässlicher Qualität,
      Standards und wettbewerbsfähigen Produkten. Deshalb ist Moorschutz auf
      Landwirtschaftsflächen immer auch Wertschöpfungs- und Koordinationsarbeit.
    </p>
  </div>

  <p class="moore-source-line moore-value-source">
    Grundlage: kuratierte Literatur- und Projektauswertung zu Paludikultur,
    Nassgrünland, Nassweide, Sphagnum, Moor-PV und SOLAMO-BW-Wertschöpfungsketten;
    diese Matrix ist eine Orientierung, keine Standortempfehlung.
  </p>
</section>
{HTML_END}"""


def insert_html_block(html: str, block: str) -> tuple[str, str]:
    html, replaced = remove_existing_block(html)
    pos, where = insertion_pos(html)
    updated = html[:pos].rstrip() + "\n\n" + block + "\n\n" + html[pos:].lstrip()
    action = f"replaced existing B102 block and inserted {where}" if replaced else f"inserted {where}"
    return updated, action


def build_css_block() -> str:
    return f"""{CSS_START}
.moore-value-section {{
  padding-top: clamp(3.5rem, 6vw, 5.8rem);
  padding-bottom: clamp(3.8rem, 6.5vw, 6.2rem);
  background:
    radial-gradient(circle at 12% 16%, rgba(95, 128, 94, 0.10), transparent 28rem),
    radial-gradient(circle at 88% 24%, rgba(63, 103, 95, 0.08), transparent 30rem);
}}

.moore-value-header {{
  max-width: 980px;
}}

.moore-value-header h2 {{
  max-width: 900px;
}}

.moore-value-header p {{
  max-width: 850px;
}}

.moore-value-matrix {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  border: 1px solid rgba(45, 63, 52, 0.14);
  border-radius: 1.25rem;
  overflow: hidden;
  background: rgba(255, 252, 244, 0.72);
  box-shadow: 0 1rem 2.6rem rgba(34, 43, 37, 0.08);
}}

.moore-value-row {{
  display: grid;
  grid-template-columns: 1.25fr 1.15fr 1fr 1.25fr;
  gap: 0;
  border-top: 1px solid rgba(45, 63, 52, 0.11);
}}

.moore-value-row:first-child {{
  border-top: 0;
}}

.moore-value-row > div {{
  padding: clamp(0.85rem, 1.6vw, 1.15rem);
  border-left: 1px solid rgba(45, 63, 52, 0.10);
  color: rgba(46, 58, 51, 0.76);
  line-height: 1.45;
}}

.moore-value-row > div:first-child {{
  border-left: 0;
}}

.moore-value-row--head {{
  background: rgba(235, 244, 235, 0.78);
}}

.moore-value-row--head > div {{
  font-size: 0.74rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: rgba(70, 91, 76, 0.62);
}}

.moore-value-path span {{
  display: block;
  margin-bottom: 0.35rem;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(71, 98, 80, 0.58);
}}

.moore-value-path strong {{
  display: block;
  color: rgba(28, 38, 31, 0.94);
  font-size: clamp(1rem, 1.25vw, 1.13rem);
  line-height: 1.18;
}}

.moore-value-reality {{
  width: min(1120px, calc(100% - 2rem));
  margin: clamp(1rem, 2vw, 1.4rem) auto 0;
  padding: clamp(1rem, 2vw, 1.35rem);
  border-left: 0.3rem solid rgba(72, 118, 89, 0.64);
  border-radius: 0.95rem;
  background: rgba(241, 248, 244, 0.76);
}}

.moore-value-reality h3 {{
  margin: 0 0 0.5rem;
  font-size: clamp(1.08rem, 1.5vw, 1.28rem);
  color: rgba(29, 38, 32, 0.94);
}}

.moore-value-reality p {{
  max-width: 860px;
  margin: 0;
  color: rgba(45, 57, 50, 0.76);
  line-height: 1.55;
}}

.moore-value-source {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0.85rem auto 0;
  color: rgba(65, 78, 70, 0.62) !important;
}}

@media (max-width: 960px) {{
  .moore-value-matrix {{
    border-radius: 1rem;
    overflow: visible;
    background: transparent;
    border: 0;
    box-shadow: none;
  }}

  .moore-value-row--head {{
    display: none;
  }}

  .moore-value-row {{
    grid-template-columns: 1fr;
    margin-bottom: 0.9rem;
    border: 1px solid rgba(45, 63, 52, 0.14);
    border-radius: 1rem;
    overflow: hidden;
    background: rgba(255, 252, 244, 0.76);
    box-shadow: 0 0.7rem 1.8rem rgba(34, 43, 37, 0.07);
  }}

  .moore-value-row > div {{
    border-left: 0;
    border-top: 1px solid rgba(45, 63, 52, 0.09);
  }}

  .moore-value-row > div:first-child {{
    border-top: 0;
  }}

  .moore-value-row > div:nth-child(2)::before {{
    content: "Produktlogik";
  }}

  .moore-value-row > div:nth-child(3)::before {{
    content: "Reifegrad";
  }}

  .moore-value-row > div:nth-child(4)::before {{
    content: "Hauptengpass";
  }}

  .moore-value-row > div:nth-child(n+2)::before {{
    display: block;
    margin-bottom: 0.25rem;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(70, 91, 76, 0.55);
  }}
}}
{CSS_END}"""


def insert_css_block(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B102 CSS block"
    return css.rstrip() + "\n\n" + block + "\n", "appended B102 CSS block"


def write_report(today: str, html_action: str, css_action: str) -> None:
    md = f"""# B102 - Add Usage-Path / Value-Chain Matrix

Date: {today}

## Result

B102 added a compact matrix translating the Transformationspfade into concrete
usage and value-chain logics.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B102_add_usage_value_chain_matrix.md`
- `docs/B102_usage_value_chain_matrix_audit.txt`
- `tasks/done.md`

## Actions

- HTML: {html_action}
- CSS: {css_action}

## Content logic

The matrix covers:

- Nassgrünland / Pflegenutzung
- Nassweide / robuste Tierarten
- Schilf / Rohrkolben / Seggen
- Sphagnum / Substratpfade
- Moor-PV

It also adds the value-chain bottleneck:

```text
Verarbeitung lohnt sich erst bei ausreichender Menge.
Anbau lohnt sich erst bei sicherer Abnahme.
Nachfrage entsteht erst bei verlässlicher Qualität und wettbewerbsfähigen Produkten.
```

## Editorial boundary

The section is explicitly framed as orientation, not as a site recommendation.
It does not imply suitability, priority or farm-level affectedness.

## Next step

Visual review. If accepted, continue with B103:
Realismus-Formel / closing synthesis or B104 emissions-method concept.
"""
    write_text(REPORT, md)


def audit(html: str) -> str:
    b99_pos = html.find(B99_END)
    b102_pos = html.find(HTML_START)

    checks = {
        "B102 marker start": HTML_START in html,
        "B102 marker end": HTML_END in html,
        "placed after B99": b102_pos > b99_pos if b99_pos != -1 and b102_pos != -1 else True,
        "section id value-chain-matrix": 'id="value-chain-matrix"' in html,
        "Nassgrünland": "Nassgrünland" in html,
        "Nassweide": "Nassweide" in html,
        "Schilf / Rohrkolben / Seggen": "Schilf / Rohrkolben / Seggen" in html,
        "Sphagnum": "Sphagnum" in html,
        "Moor-PV": "Moor-PV" in html,
        "Henne-Ei / Abnahme logic": "Anbau lohnt sich erst" in html and "sicherer Abnahme" in html,
        "boundary orientation": "keine Standortempfehlung" in html,
    }

    lines = [
        "# B102 usage/value-chain matrix audit",
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
        "- Matrix should not feel like a dense scientific table.",
        "- It should sit naturally after Transformationspfade.",
        "- It should make product/value-chain logic more concrete.",
        "- It must not imply site suitability or recommendations.",
        "- Mobile layout should collapse into readable cards.",
        "",
    ])
    return "\n".join(lines)


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B102 - Add usage-path / value-chain matrix"
    if marker in current:
        return

    entry = f"""
## B102 - Add usage-path / value-chain matrix ({today})

- Added a compact matrix for Nassgrünland, Nassweide, Schilf/Rohrkolben/Seggen, Sphagnum and Moor-PV.
- Translated transformation pathways into product logic, maturity and bottlenecks.
- Added the value-chain bottleneck: quantity, secure offtake, quality, standards and competitive products.
- Added `docs/B102_add_usage_value_chain_matrix.md`.
- Added `docs/B102_usage_value_chain_matrix_audit.txt`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    html = read_text(INDEX)
    css = read_text(CSS)

    new_html, html_action = insert_html_block(html, build_html_block())
    new_css, css_action = insert_css_block(css, build_css_block())

    write_text(INDEX, new_html)
    write_text(CSS, new_css)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    write_report(today, html_action, css_action)
    write_text(AUDIT, audit(new_html))
    update_done(today)

    print("B102 usage-path / value-chain matrix complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Actions:")
    print(f"  HTML: {html_action}")
    print(f"  CSS: {css_action}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B102_usage_value_chain_matrix_audit.txt")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
