from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "137_consequence_kicker.py"
DOC = ROOT / "docs" / "B137_consequence_kicker.md"
AUDIT = ROOT / "docs" / "B137_consequence_kicker_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B137_CONSEQUENCE_KICKER_START -->"
HTML_END = "<!-- /B137_CONSEQUENCE_KICKER_END -->"
CSS_START = "/* B137_CONSEQUENCE_KICKER_START */"
CSS_END = "/* B137_CONSEQUENCE_KICKER_END */"

INSERT_BEFORE_ANCHORS = [
    "Quellen, Methodik und Nutzungsrechte",
    "Methode in Kürze",
    "Datengrundlagen, Rechte und Quellenvermerke",
    "Quellen",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def build_kicker_html() -> str:
    return f"""{HTML_START}
<section class="b137-consequence-kicker" aria-labelledby="b137-consequence-title">
  <div class="section-inner">
    <div class="b137-consequence-kicker__inner">
      <p class="eyebrow">Konsequenz</p>
      <h2 id="b137-consequence-title">Der Hebel verschiebt sich von der Fläche zur Kette</h2>
      <p class="b137-consequence-kicker__lead">
        Wiedervernässung bleibt der ökologische Kern. Für Umsetzung reicht die Flächenperspektive
        aber nicht aus: Entscheidend wird, ob Wasser, Nutzung, Verarbeitung und Nachfrage als
        zusammenhängendes System funktionieren.
      </p>

      <div class="b137-consequence-kicker__grid" aria-label="Drei Konsequenzen aus der räumlichen Einordnung">
        <article>
          <span>01</span>
          <h3>Mehr Wiedervernässung ist notwendig, aber nicht ausreichend</h3>
          <p>Ohne passende Nutzung und Abnahme entstehen aus nassen Flächen noch keine tragfähigen Pfade.</p>
        </article>
        <article>
          <span>02</span>
          <h3>Planung muss hydrologische Einheiten ernst nehmen</h3>
          <p>Parzellen, Betriebe und Wasserhaushalt passen selten deckungsgleich zusammen.</p>
        </article>
        <article>
          <span>03</span>
          <h3>Wertschöpfung muss vor der Skalierung mitgedacht werden</h3>
          <p>Verarbeitung, Standards, Mengen und Nachfrage entscheiden, welche Optionen regional anschlussfähig werden.</p>
        </article>
      </div>
    </div>
  </div>
</section>
{HTML_END}"""


def insert_before_sources(html: str, block: str, audit: list[str]) -> str:
    for anchor in INSERT_BEFORE_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        # Avoid the header nav link if the generic "Quellen" fallback is found early.
        if anchor == "Quellen" and pos < 1200:
            continue

        section_start = html.rfind("<section", 0, pos)
        if section_start >= 0:
            audit.append(f"OK inserted B137 before section containing anchor: {anchor}")
            return html[:section_start] + block + "\n\n" + html[section_start:]

        # If the sources area is not a section, use nearest footer/main block fallback.
        footer_start = html.rfind("<footer", 0, pos)
        if footer_start >= 0:
            audit.append(f"OK inserted B137 before footer containing anchor: {anchor}")
            return html[:footer_start] + block + "\n\n" + html[footer_start:]

        audit.append(f"WARN anchor found but no section/footer start before it: {anchor}")

    audit.append("ERROR no insertion anchor found for B137")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b137-consequence-kicker {{
  padding-block: clamp(2.2rem, 5vw, 4.2rem);
}}

.b137-consequence-kicker .section-inner {{
  width: min(100% - 2rem, 74rem);
  margin-inline: auto;
}}

.b137-consequence-kicker__inner {{
  border-radius: 1.35rem;
  border: 1px solid rgba(26, 48, 38, 0.13);
  background: rgba(255, 255, 255, 0.52);
  box-shadow: 0 18px 52px rgba(26, 48, 38, 0.07);
  padding: clamp(1rem, 3vw, 1.65rem);
}}

.b137-consequence-kicker h2 {{
  max-width: 16ch;
  margin-bottom: 0.65rem;
}}

.b137-consequence-kicker__lead {{
  max-width: 48rem;
  color: var(--muted, #637266);
  font-size: clamp(1rem, 1.7vw, 1.14rem);
  line-height: 1.55;
}}

.b137-consequence-kicker__grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 1.25rem;
}}

.b137-consequence-kicker__grid article {{
  border-radius: 1rem;
  border: 1px solid rgba(26, 48, 38, 0.11);
  background: rgba(248, 246, 238, 0.72);
  padding: 0.95rem;
}}

.b137-consequence-kicker__grid span {{
  display: inline-block;
  margin-bottom: 0.55rem;
  color: #6f8c42;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}}

.b137-consequence-kicker__grid h3 {{
  margin: 0 0 0.35rem;
  font-size: 1.02rem;
  line-height: 1.28;
}}

.b137-consequence-kicker__grid p {{
  margin: 0;
  color: var(--muted, #637266);
  font-size: 0.94rem;
  line-height: 1.48;
}}

@media (max-width: 820px) {{
  .b137-consequence-kicker .section-inner {{
    width: min(100% - 1.25rem, 74rem);
  }}

  .b137-consequence-kicker h2 {{
    max-width: none;
  }}

  .b137-consequence-kicker__grid {{
    grid-template-columns: 1fr;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B137 consequence kicker: added a concise end-of-story consequence block before sources ({date.today().isoformat()})."
    if "B137 consequence kicker" in done_text:
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
    audit.append(f"Old B137 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B137 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    html = insert_before_sources(html, build_kicker_html(), audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B137 - Consequence Kicker

Date: {today}

## Ziel

B137 ergänzt vor dem Quellen-/Methodikbereich einen knappen Schluss- bzw. Kickerblock.
Er verdichtet die V2-Erzählung: Moorbodenschutz ist nicht nur eine Frage der Fläche,
sondern der funktionierenden Kette aus Wasser, Nutzung, Verarbeitung und Nachfrage.

## Umsetzung

- neue Section `Konsequenz`
- Aussage-Titel: `Der Hebel verschiebt sich von der Fläche zur Kette`
- drei kurze Konsequenzen:
  - Wiedervernässung ist notwendig, aber nicht ausreichend
  - Planung muss hydrologische Einheiten ernst nehmen
  - Wertschöpfung muss vor der Skalierung mitgedacht werden
- Position vor dem Quellen-/Methodikbereich
- keine Änderung an Kartenlogik, Daten, Navigation oder Scorecard

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/137_consequence_kicker.py`
- `docs/B137_consequence_kicker.md`
- `docs/B137_consequence_kicker_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Kicker steht vor Quellen/Methodik.
- Er wirkt wie eine Schlussfolgerung, nicht wie ein weiterer Datenblock.
- Desktop: drei Karten nebeneinander.
- Mobil: Karten sauber gestapelt.
- Quellenblock und Methode-in-Kürze bleiben erhalten.
"""
    write(DOC, doc_text)

    audit_text = "# B137 consequence kicker audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B137 consequence kicker patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B137_consequence_kicker.md")
    print("  docs/B137_consequence_kicker_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
