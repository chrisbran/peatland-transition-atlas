from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "139_water_governance_block.py"
DOC = ROOT / "docs" / "B139_water_governance_block.md"
AUDIT = ROOT / "docs" / "B139_water_governance_block_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B139_WATER_GOVERNANCE_START -->"
HTML_END = "<!-- /B139_WATER_GOVERNANCE_END -->"
CSS_START = "/* B139_WATER_GOVERNANCE_START */"
CSS_END = "/* B139_WATER_GOVERNANCE_END */"

INSERT_BEFORE_ANCHORS = [
    "Der Hebel verschiebt sich von der Fläche zur Kette",
    "Konsequenz",
    "Quellen, Methodik und Nutzungsrechte",
    "Methode in Kürze",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def build_block_html() -> str:
    return f"""{HTML_START}
<section class="b139-water-governance" aria-labelledby="b139-water-governance-title">
  <div class="section-inner">
    <div class="b139-water-governance__inner">
      <p class="eyebrow">Wasser und Governance</p>
      <h2 id="b139-water-governance-title">Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen</h2>
      <p class="b139-water-governance__lead">
        Wiedervernässung wird nicht allein auf der einzelnen Fläche entschieden. Der Wasserstand
        verbindet Parzellen, Betriebe, Gräben, Vorfluter und Nachbarschaften. Deshalb beginnt
        Umsetzung oft dort, wo Zuständigkeiten nicht deckungsgleich sind.
      </p>

      <div class="b139-water-governance__diagram" aria-label="Parzelle, Betrieb und hydrologische Einheit als unterschiedliche Planungsebenen">
        <article>
          <span class="b139-water-governance__level">01</span>
          <h3>Parzelle</h3>
          <p>zeigt Nutzung, Eigentum und Bewirtschaftung – aber nur einen Ausschnitt des Wasserhaushalts.</p>
        </article>
        <article>
          <span class="b139-water-governance__level">02</span>
          <h3>Betrieb</h3>
          <p>entscheidet über Arbeitsabläufe, Futter, Technik und Risiko – liegt aber oft über mehrere Wasserlagen verteilt.</p>
        </article>
        <article>
          <span class="b139-water-governance__level">03</span>
          <h3>Hydrologische Einheit</h3>
          <p>bestimmt, welche Wasserstände gemeinsam steuerbar sind – und wer dafür zusammen planen muss.</p>
        </article>
      </div>

      <p class="b139-water-governance__note">
        Konsequenz: Karten können Prüfbedarf sichtbar machen. Umsetzung braucht zusätzlich lokale
        Wasserkenntnis, Abstimmung zwischen Eigentümern und Betrieben sowie tragfähige
        Bewirtschaftungs- und Verwertungspfade.
      </p>
    </div>
  </div>
</section>
{HTML_END}"""


def insert_before_anchor_section(html: str, block: str, audit: list[str]) -> str:
    for anchor in INSERT_BEFORE_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        # Avoid nav/header hits for generic anchors.
        if pos < 1200 and anchor in {"Konsequenz"}:
            continue

        section_start = html.rfind("<section", 0, pos)
        if section_start >= 0:
            audit.append(f"OK inserted B139 before section containing anchor: {anchor}")
            return html[:section_start] + block + "\n\n" + html[section_start:]

        footer_start = html.rfind("<footer", 0, pos)
        if footer_start >= 0:
            audit.append(f"OK inserted B139 before footer containing anchor: {anchor}")
            return html[:footer_start] + block + "\n\n" + html[footer_start:]

        audit.append(f"WARN anchor found but no section/footer before it: {anchor}")

    audit.append("ERROR no insertion anchor found for B139")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b139-water-governance {{
  padding-block: clamp(2rem, 5vw, 4rem);
}}

.b139-water-governance .section-inner {{
  width: min(100% - 2rem, 74rem);
  margin-inline: auto;
}}

.b139-water-governance__inner {{
  max-width: 68rem;
  margin-inline: auto;
  border-top: 1px solid rgba(26, 48, 38, 0.14);
  padding-top: clamp(1.25rem, 3vw, 2rem);
}}

.b139-water-governance h2 {{
  max-width: 15ch;
  margin-bottom: 0.65rem;
}}

.b139-water-governance__lead {{
  max-width: 48rem;
  color: var(--muted, #637266);
  font-size: clamp(1rem, 1.7vw, 1.14rem);
  line-height: 1.55;
}}

.b139-water-governance__diagram {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  margin-top: 1.3rem;
  position: relative;
}}

.b139-water-governance__diagram article {{
  position: relative;
  border-radius: 1rem;
  border: 1px solid rgba(26, 48, 38, 0.12);
  background: rgba(255, 255, 255, 0.5);
  padding: 1rem;
  min-height: 11.5rem;
}}

.b139-water-governance__level {{
  display: inline-block;
  margin-bottom: 0.55rem;
  color: #6f8c42;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}}

.b139-water-governance__diagram h3 {{
  margin: 0 0 0.35rem;
  font-size: 1.05rem;
  line-height: 1.25;
}}

.b139-water-governance__diagram p {{
  margin: 0;
  color: var(--muted, #637266);
  font-size: 0.94rem;
  line-height: 1.5;
}}

.b139-water-governance__note {{
  max-width: 52rem;
  margin: 1.1rem 0 0;
  padding: 0.85rem 0.95rem;
  border-left: 3px solid rgba(89, 123, 82, 0.72);
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.42);
  color: var(--muted, #637266);
  font-size: 0.96rem;
  line-height: 1.55;
}}

@media (max-width: 820px) {{
  .b139-water-governance .section-inner {{
    width: min(100% - 1.25rem, 74rem);
  }}

  .b139-water-governance h2 {{
    max-width: none;
  }}

  .b139-water-governance__diagram {{
    grid-template-columns: 1fr;
  }}

  .b139-water-governance__diagram article {{
    min-height: 0;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B139 water governance block: added a planning-level section on parcels, farms and hydrological units ({date.today().isoformat()})."
    if "B139 water governance block" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    html = read(INDEX)
    css = read(CSS)

    old_html_present = HTML_START in html and HTML_END in html
    old_css_present = CSS_START in css and CSS_END in css
    audit.append(f"Old B139 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B139 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    html = insert_before_anchor_section(html, build_block_html(), audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B139 - Water Governance Block

Date: {today}

## Ziel

B139 ergänzt den V2-Abschnitt `Wasser und Governance`.
Er macht sichtbar, dass Moorbodenschutz nicht nur auf Parzellenebene funktioniert:
Parzelle, Betrieb und hydrologische Einheit sind unterschiedliche Planungsebenen.

## Umsetzung

- neue Section vor dem Konsequenz-Kicker bzw. vor Quellen/Methodik
- Titel: `Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen`
- drei Planungsebenen:
  - Parzelle
  - Betrieb
  - Hydrologische Einheit
- kurze Schlussnotiz zur Abstimmung zwischen Wasserkenntnis, Eigentümern, Betrieben und Wertschöpfung
- keine Änderung an Kartenlogik, Daten, Navigation, Scorecard oder Quellenblock

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/139_water_governance_block.py`
- `docs/B139_water_governance_block.md`
- `docs/B139_water_governance_block_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Block steht vor dem Konsequenz-Kicker oder vor Quellen/Methodik.
- Er wirkt wie eine fachliche Brücke zwischen Wertschöpfung und Schlussfolgerung.
- Desktop: drei Karten nebeneinander.
- Mobil: Karten sauber gestapelt.
- Keine Änderung an Scorecard, Navigation und Karten.
"""
    write(DOC, doc_text)

    audit_text = "# B139 water governance block audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B139 water governance block patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B139_water_governance_block.md")
    print("  docs/B139_water_governance_block_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
