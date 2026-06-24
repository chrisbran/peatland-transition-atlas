#!/usr/bin/env python3
"""
B100b - Recast moor primer as a compact flow-preserving bridge

Why
---
The B100 primer was scientifically useful but too textbook-like at its current
position. It interrupts the visual/narrative flow before Oberschwaben.

B100b replaces the full primer with a much shorter editorial bridge:

- one title
- one concise explanation
- three compact mechanism chips
- one optional method/detail disclosure

The full technical primer logic is not lost; it is compressed into a small
"Details" element that readers can open if needed.

Changed files
-------------
- index.html
- src/styles.css
- docs/B100b_recast_moor_primer_as_compact_bridge.md
- docs/B100b_moor_primer_bridge_audit.txt
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

REPORT = DOCS / "B100b_recast_moor_primer_as_compact_bridge.md"
AUDIT = DOCS / "B100b_moor_primer_bridge_audit.txt"

HTML_START = "<!-- B100_MOOR_PRIMER_START -->"
HTML_END = "<!-- B100_MOOR_PRIMER_END -->"
CSS_START = "/* B100_MOOR_PRIMER_START */"
CSS_END = "/* B100_MOOR_PRIMER_END */"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def require_inputs() -> None:
    missing = [p for p in [INDEX, CSS] if not p.exists()]
    if missing:
        print("B100b cannot run. Missing files:")
        for p in missing:
            print(f"  - {rel(p)}")
        sys.exit(1)

    html = read_text(INDEX)
    if HTML_START not in html or HTML_END not in html:
        print("B100b cannot run. B100 moor primer block not found in index.html.")
        print("Run B100 first.")
        sys.exit(1)


def build_html_block() -> str:
    return f"""{HTML_START}
<section id="moor-primer" class="section moore-primer-section moore-primer-bridge" aria-labelledby="moor-primer-title">
  <div class="moore-primer-bridge-inner">
    <div class="moore-primer-bridge-copy">
      <p class="eyebrow">Moore verstehen</p>
      <h2 id="moor-primer-title">Warum die Karte beim Wasser beginnt</h2>
      <p>
        Ein Moor ist kein gewöhnlicher Boden. Solange Torf nass bleibt, speichert er
        Kohlenstoff; wird er entwässert, wird er zur dauerhaften Emissionsquelle.
        Darum führt die Oberschwaben-Story von Boden und Nutzung direkt zur Frage:
        Wie lässt sich Wasserstand verändern, ohne Betriebe und Landschaften zu überfordern?
      </p>
    </div>

    <div class="moore-primer-bridge-mechanism" aria-label="Moor-Kernmechanismus">
      <div class="moore-primer-chip">
        <span>Nass</span>
        <strong>Speicher</strong>
      </div>
      <div class="moore-primer-chip">
        <span>Entwässert</span>
        <strong>Quelle</strong>
      </div>
      <div class="moore-primer-chip">
        <span>Wiedervernässt</span>
        <strong>Verhandlung</strong>
      </div>
    </div>
  </div>

  <details class="moore-primer-details">
    <summary>Fachlicher Hintergrund in 30 Sekunden</summary>
    <div class="moore-primer-details-grid">
      <p>
        Torf entsteht, wenn Pflanzenreste unter nassen, sauerstoffarmen Bedingungen
        langsamer abgebaut als aufgebaut werden. Sinkt der Wasserstand, gelangt Sauerstoff
        in den Torfkörper; Torf mineralisiert und setzt Treibhausgase frei.
      </p>
      <p>
        Für landwirtschaftliche Transformationsfragen sind häufig Niedermoore und
        Feuchtbodenkomplexe relevant. Ob Nassgrünland, Paludikultur, Renaturierung oder
        Moor-PV realistisch sind, hängt von Wasserstand, Degradierung, Nährstoffen,
        Technik und regionaler Koordination ab.
      </p>
    </div>
  </details>
</section>
{HTML_END}"""


def replace_html(html: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(HTML_START) + r".*?" + re.escape(HTML_END), re.DOTALL)
    updated, count = pattern.subn(block, html)
    if count != 1:
        raise RuntimeError(f"Expected to replace exactly one B100 block, replaced {count}.")
    return updated, "replaced B100 textbook primer with compact bridge"


def build_css_block() -> str:
    return f"""{CSS_START}
.moore-primer-section {{
  position: relative;
}}

.moore-primer-bridge {{
  padding-top: clamp(2.6rem, 5vw, 4.6rem);
  padding-bottom: clamp(2.6rem, 5vw, 4.6rem);
}}

.moore-primer-bridge-inner {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
  gap: clamp(1.4rem, 4vw, 4rem);
  align-items: center;
}}

.moore-primer-bridge-copy h2 {{
  max-width: 760px;
  margin-bottom: 0.85rem;
  letter-spacing: -0.04em;
}}

.moore-primer-bridge-copy p:not(.eyebrow) {{
  max-width: 830px;
  margin: 0;
  font-size: clamp(1.02rem, 1.35vw, 1.18rem);
  line-height: 1.58;
  color: rgba(38, 47, 41, 0.78);
}}

.moore-primer-bridge-mechanism {{
  display: grid;
  gap: 0.7rem;
}}

.moore-primer-chip {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(53, 76, 61, 0.16);
  border-radius: 999px;
  background: rgba(255, 252, 244, 0.72);
  box-shadow: 0 0.65rem 1.8rem rgba(34, 43, 37, 0.065);
}}

.moore-primer-chip span {{
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(70, 91, 76, 0.58);
}}

.moore-primer-chip strong {{
  font-size: clamp(1rem, 1.35vw, 1.14rem);
  color: rgba(27, 36, 30, 0.92);
}}

.moore-primer-details {{
  width: min(1120px, calc(100% - 2rem));
  margin: clamp(1rem, 2vw, 1.3rem) auto 0;
  border-top: 1px solid rgba(49, 62, 52, 0.12);
  color: rgba(48, 60, 53, 0.72);
}}

.moore-primer-details summary {{
  cursor: pointer;
  padding: 0.85rem 0 0;
  font-size: 0.88rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: rgba(69, 88, 74, 0.65);
}}

.moore-primer-details-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(1rem, 2vw, 2rem);
  padding-top: 0.8rem;
}}

.moore-primer-details-grid p {{
  margin: 0;
  max-width: 620px;
  font-size: 0.96rem;
  line-height: 1.55;
  color: rgba(48, 60, 53, 0.74);
}}

@media (max-width: 860px) {{
  .moore-primer-bridge-inner {{
    grid-template-columns: 1fr;
  }}

  .moore-primer-bridge-mechanism {{
    max-width: 520px;
  }}

  .moore-primer-details-grid {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 560px) {{
  .moore-primer-chip {{
    border-radius: 1rem;
    align-items: flex-start;
    flex-direction: column;
    gap: 0.25rem;
  }}
}}
{CSS_END}"""


def replace_css(css: str, block: str) -> tuple[str, str]:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.DOTALL)
    updated, count = pattern.subn(block, css)
    if count == 1:
        return updated, "replaced B100 CSS with compact bridge CSS"
    if count == 0:
        return css.rstrip() + "\n\n" + block + "\n", "appended compact bridge CSS because B100 CSS block was missing"
    raise RuntimeError(f"Expected to replace at most one B100 CSS block, replaced {count}.")


def write_report(today: str, html_action: str, css_action: str) -> None:
    md = f"""# B100b - Recast Moor Primer as Compact Bridge

Date: {today}

## Result

B100b replaced the textbook-like B100 primer with a compact flow-preserving
editorial bridge.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B100b_recast_moor_primer_as_compact_bridge.md`
- `docs/B100b_moor_primer_bridge_audit.txt`
- `tasks/done.md`

## Actions

- HTML: {html_action}
- CSS: {css_action}

## Editorial rationale

The previous B100 section explained the topic correctly but interrupted the
story flow. B100b keeps the necessary mechanism but reduces the reading burden:

```text
Nass -> Speicher
Entwässert -> Quelle
Wiedervernässt -> Verhandlung
```

Detailed moor background is now optional inside a collapsed disclosure element.

## Next step

Visual review. If accepted, continue with B101: add the rounded B98c
Oberschwaben key-figures capsule.
"""
    write_text(REPORT, md)


def audit(html: str) -> str:
    checks = {
        "B100 marker start": HTML_START in html,
        "compact bridge class": "moore-primer-bridge" in html,
        "details disclosure": "<details" in html and "Fachlicher Hintergrund in 30 Sekunden" in html,
        "old step-card class removed": "moore-primer-step" not in html,
        "old grid card class removed": "moore-primer-card" not in html,
        "chip mechanism": "moore-primer-chip" in html,
        "Nass -> Speicher": "Nass" in html and "Speicher" in html,
        "Entwässert -> Quelle": "Entwässert" in html and "Quelle" in html,
        "Wiedervernässt -> Verhandlung": "Wiedervernässt" in html and "Verhandlung" in html,
    }

    lines = [
        "# B100b moor primer bridge audit",
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
        "- Primer should read as a transition, not as a textbook section.",
        "- Main copy should be readable in one glance.",
        "- The three chips should carry the mechanism visually.",
        "- Details should remain optional and closed by default.",
        "- Section should not break the flow into Oberschwaben.",
        "",
    ])
    return "\n".join(lines)


def update_done(today: str) -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B100b - Recast moor primer as compact bridge"
    if marker in current:
        return

    entry = f"""
## B100b - Recast moor primer as compact bridge ({today})

- Replaced the textbook-like B100 primer with a compact editorial bridge.
- Reduced the visible mechanism to three chips: Nass/Speicher, Entwässert/Quelle, Wiedervernässt/Verhandlung.
- Moved detailed moor background into an optional disclosure element.
- Added `docs/B100b_recast_moor_primer_as_compact_bridge.md`.
- Added `docs/B100b_moor_primer_bridge_audit.txt`.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def main() -> None:
    require_inputs()
    today = date.today().isoformat()

    html = read_text(INDEX)
    css = read_text(CSS)

    new_html, html_action = replace_html(html, build_html_block())
    new_css, css_action = replace_css(css, build_css_block())

    write_text(INDEX, new_html)
    write_text(CSS, new_css)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    write_report(today, html_action, css_action)
    write_text(AUDIT, audit(new_html))
    update_done(today)

    print("B100b compact moor-primer bridge complete.")
    print("Changed/created:")
    for p in [INDEX, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print("")
    print("Actions:")
    print(f"  HTML: {html_action}")
    print(f"  CSS: {css_action}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B100b_moor_primer_bridge_audit.txt")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
