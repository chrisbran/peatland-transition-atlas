#!/usr/bin/env python3
"""
B101 - Add Oberschwaben key-figures capsule from B98c

Purpose
-------
Add a compact quantitative capsule after the Oberschwaben scrolly map and before
the Transformationspfade section.

The capsule uses B98c only in rounded, public-safe form:

- ~19,900 ha Schnittmenge
- ~82 % Grünland
- ~16 % Ackerland
- ~2 % Stilllegung / unklare FIONA-Zuweisung getrennt geprüft

It explicitly preserves the method boundary:
The numbers describe a spatial search/context layer, not suitability,
prioritization, or farm-level affectedness.

Placement
---------
Preferred insertion point:
  after <!-- B96_OBERSCHWABEN_SCROLLY_END -->
  before <!-- B99_TRANSFORMATION_PATHWAYS_START -->

Fallback:
  after <!-- B96_OBERSCHWABEN_SCROLLY_END -->

Changed files
-------------
- index.html
- src/styles.css
- docs/B101_add_oberschwaben_key_figures_capsule.md
- docs/B101_oberschwaben_key_figures_audit.txt
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

REPORT = DOCS / "B101_add_oberschwaben_key_figures_capsule.md"
AUDIT = DOCS / "B101_oberschwaben_key_figures_audit.txt"

B96_END = "<!-- B96_OBERSCHWABEN_SCROLLY_END -->"
B99_START = "<!-- B99_TRANSFORMATION_PATHWAYS_START -->"

HTML_START = "<!-- B101_OBERSCHWABEN_KEY_FIGURES_START -->"
HTML_END = "<!-- B101_OBERSCHWABEN_KEY_FIGURES_END -->"
CSS_START = "/* B101_OBERSCHWABEN_KEY_FIGURES_START */"
CSS_END = "/* B101_OBERSCHWABEN_KEY_FIGURES_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    missing = [p for p in [INDEX, CSS] if not p.exists()]
    if missing:
        print("B101 cannot run. Missing files:")
        for p in missing:
            print(f"  - {rel(p)}")
        sys.exit(1)

    html = read_text(INDEX)
    if B96_END not in html:
        print("B101 cannot run. Oberschwaben scrolly end marker not found.")
        print(f"Expected: {B96_END}")
        sys.exit(1)


def remove_existing_html_block(html: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(HTML_START) + r".*?" + re.escape(HTML_END), re.DOTALL)
    updated, count = pattern.subn("", html)
    return updated, count > 0


def build_html_block() -> str:
    return f"""{HTML_START}
<section id="oberschwaben-key-figures" class="section moore-ob-keyfigures" aria-labelledby="oberschwaben-keyfigures-title">
  <div class="moore-ob-keyfigures-inner">
    <div class="moore-ob-keyfigures-copy">
      <p class="eyebrow">Interne Verschneidung</p>
      <h2 id="oberschwaben-keyfigures-title">Was die Schnittmenge in Oberschwaben zeigt</h2>
      <p>
        Die Karte bleibt eine räumliche Einordnung. Die interne Flächen-QA zeigt aber,
        dass die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext
        nicht nur visuell plausibel ist, sondern auch quantitativ trägt.
      </p>
    </div>

    <div class="moore-ob-keyfigures-grid" aria-label="Gerundete Kennzahlen zur Oberschwaben-Schnittmenge">
      <article class="moore-ob-keyfigure moore-ob-keyfigure--primary">
        <span class="moore-ob-keyfigure-value">~19.900 ha</span>
        <span class="moore-ob-keyfigure-label">landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext</span>
      </article>

      <article class="moore-ob-keyfigure">
        <span class="moore-ob-keyfigure-value">~82 %</span>
        <span class="moore-ob-keyfigure-label">Grünland</span>
      </article>

      <article class="moore-ob-keyfigure">
        <span class="moore-ob-keyfigure-value">~16 %</span>
        <span class="moore-ob-keyfigure-label">Ackerland, bereinigt um Sonderfälle</span>
      </article>

      <article class="moore-ob-keyfigure">
        <span class="moore-ob-keyfigure-value">~2 %</span>
        <span class="moore-ob-keyfigure-label">Stilllegung oder unklare FIONA-Zuweisung getrennt geprüft</span>
      </article>
    </div>

    <div class="moore-ob-keyfigures-boundary">
      <strong>Lesart:</strong>
      Diese Werte beschreiben eine Such- und Gesprächskulisse. Sie sind keine
      Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
    </div>

    <p class="moore-source-line moore-ob-keyfigures-source">
      Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext, GISCO NUTS 2024;
      eigene Verschneidung und B98c-Klassifikations-QA. Werte gerundet.
    </p>
  </div>
</section>
{HTML_END}"""


def insert_html_block(html: str, block: str) -> tuple[str, str]:
    html, replaced = remove_existing_html_block(html)

    b96_pos = html.find(B96_END)
    if b96_pos == -1:
        raise RuntimeError("B96 end marker missing after cleanup.")
    b96_insert_after = b96_pos + len(B96_END)

    b99_pos = html.find(B99_START, b96_insert_after)
    if b99_pos != -1:
        updated = html[:b99_pos].rstrip() + "\n\n" + block + "\n\n" + html[b99_pos:].lstrip()
        action = "inserted between Oberschwaben scrolly and B99 Transformationspfade"
    else:
        updated = html[:b96_insert_after].rstrip() + "\n\n" + block + "\n\n" + html[b96_insert_after:].lstrip()
        action = "inserted after Oberschwaben scrolly end marker; B99 marker not found"

    if replaced:
        action = "replaced existing B101 block and " + action

    return updated, action


def build_css_block() -> str:
    return f"""{CSS_START}
.moore-ob-keyfigures {{
  padding-top: clamp(3rem, 5.5vw, 5rem);
  padding-bottom: clamp(2.6rem, 5vw, 4.4rem);
}}

.moore-ob-keyfigures-inner {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
}}

.moore-ob-keyfigures-copy {{
  max-width: 850px;
  margin-bottom: clamp(1.2rem, 2.4vw, 1.8rem);
}}

.moore-ob-keyfigures-copy h2 {{
  max-width: 780px;
  margin-bottom: 0.75rem;
  letter-spacing: -0.04em;
}}

.moore-ob-keyfigures-copy p:not(.eyebrow) {{
  max-width: 780px;
  margin: 0;
  color: rgba(42, 53, 47, 0.76);
  line-height: 1.58;
}}

.moore-ob-keyfigures-grid {{
  display: grid;
  grid-template-columns: 1.4fr repeat(3, minmax(0, 1fr));
  gap: clamp(0.8rem, 1.6vw, 1.1rem);
  align-items: stretch;
}}

.moore-ob-keyfigure {{
  min-height: 8.2rem;
  padding: clamp(1rem, 2vw, 1.35rem);
  border: 1px solid rgba(47, 67, 55, 0.15);
  border-radius: 1.15rem;
  background: rgba(255, 252, 244, 0.78);
  box-shadow: 0 0.8rem 2.1rem rgba(34, 43, 37, 0.07);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.moore-ob-keyfigure--primary {{
  background:
    linear-gradient(135deg, rgba(235, 244, 235, 0.88), rgba(255, 252, 244, 0.78));
  border-color: rgba(68, 115, 86, 0.24);
}}

.moore-ob-keyfigure-value {{
  display: block;
  font-size: clamp(1.65rem, 3vw, 2.35rem);
  line-height: 0.98;
  letter-spacing: -0.055em;
  color: rgba(27, 37, 31, 0.94);
}}

.moore-ob-keyfigure-label {{
  display: block;
  margin-top: 0.8rem;
  font-size: 0.9rem;
  line-height: 1.35;
  color: rgba(53, 65, 58, 0.72);
}}

.moore-ob-keyfigures-boundary {{
  margin-top: clamp(1rem, 2vw, 1.35rem);
  padding: 1rem 1.15rem;
  border-left: 0.3rem solid rgba(68, 115, 86, 0.62);
  border-radius: 0.9rem;
  background: rgba(241, 248, 244, 0.72);
  color: rgba(40, 52, 45, 0.78);
  line-height: 1.5;
}}

.moore-ob-keyfigures-source {{
  margin: 0.85rem 0 0;
  color: rgba(65, 78, 70, 0.62) !important;
}}

@media (max-width: 980px) {{
  .moore-ob-keyfigures-grid {{
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }}
}}

@media (max-width: 620px) {{
  .moore-ob-keyfigures-grid {{
    grid-template-columns: 1fr;
  }}

  .moore-ob-keyfigure {{
    min-height: auto;
    border-radius: 0.95rem;
  }}
}}
{CSS_END}"""


def insert_css_block(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    if pattern.search(css):
        return pattern.sub(block, css), "replaced existing B101 CSS block"
    return css.rstrip() + "\n\n" + block + "\n", "appended B101 CSS block"


def write_report(today: str, html_action: str, css_action: str) -> None:
    md = f"""# B101 - Add Oberschwaben Key-Figures Capsule

Date: {today}

## Result

B101 added a compact rounded key-figures capsule after the Oberschwaben scrolly
map and before the Transformationspfade section.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B101_add_oberschwaben_key_figures_capsule.md`
- `docs/B101_oberschwaben_key_figures_audit.txt`
- `tasks/done.md`

## Actions

- HTML: {html_action}
- CSS: {css_action}

## Public numbers used

Rounded from B98c:

- `~19.900 ha` Schnittmenge
- `~82 %` Grünland
- `~16 %` Ackerland
- `~2 %` Stilllegung / unklare FIONA-Zuweisung getrennt geprüft

## Editorial decision

The capsule avoids exact hectare claims and keeps the method boundary explicit.
It quantifies the visual Oberschwaben intersection without turning the site into
a GIS dashboard or implying suitability, priority or farm-level affectedness.

## Next step

Visual review. If accepted, continue with B102:
Paludikultur-/Produktpfad-Matrix from the literature and primer material.
"""
    write_text(REPORT, md)


def audit(html: str) -> str:
    b96_pos = html.find(B96_END)
    b101_pos = html.find(HTML_START)
    b99_pos = html.find(B99_START)

    checks = {
        "B101 marker start": HTML_START in html,
        "B101 marker end": HTML_END in html,
        "placed after Oberschwaben": b101_pos > b96_pos if b96_pos != -1 and b101_pos != -1 else False,
        "placed before B99 pathways": b101_pos < b99_pos if b99_pos != -1 and b101_pos != -1 else True,
        "contains ~19.900 ha": "~19.900 ha" in html,
        "contains ~82 %": "~82 %" in html,
        "contains ~16 %": "~16 %" in html,
        "contains ~2 %": "~2 %" in html,
        "method boundary: keine Eignungskarte": "keine Eignungskarte" in html,
        "method boundary: keine Priorisierung": "keine Priorisierung" in html,
        "method boundary: keine betriebliche Betroffenheitsanalyse": "keine betriebliche Betroffenheitsanalyse" in html,
        "source line present": "B98c-Klassifikations-QA" in html,
    }

    lines = [
        "# B101 Oberschwaben key-figures audit",
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
        "- Capsule should sit between Oberschwaben scrolly and Transformationspfade.",
        "- Numbers should feel like orientation, not a planning result.",
        "- The boundary note must remain visible but not alarmist.",
        "- Mobile layout should stack cleanly.",
        "- Avoid adding exact CSV-like numbers to public copy.",
        "",
    ])
    return "\n".join(lines)


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B101 - Add Oberschwaben key-figures capsule"
    if marker in current:
        return

    entry = f"""
## B101 - Add Oberschwaben key-figures capsule ({today})

- Added a compact rounded key-figures capsule after the Oberschwaben scrolly map.
- Used B98c qualitatively and with rounded values: ~19,900 ha, ~82% Grünland, ~16% Ackerland, ~2% separated/reviewed categories.
- Kept the method boundary explicit: no suitability, no prioritization, no farm-level affectedness.
- Added `docs/B101_add_oberschwaben_key_figures_capsule.md`.
- Added `docs/B101_oberschwaben_key_figures_audit.txt`.
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

    print("B101 Oberschwaben key-figures capsule complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Actions:")
    print(f"  HTML: {html_action}")
    print(f"  CSS: {css_action}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B101_oberschwaben_key_figures_audit.txt")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
