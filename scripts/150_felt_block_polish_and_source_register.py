from pathlib import Path
import re
from datetime import date
from html import escape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "150_felt_block_polish_and_source_register.py"
DOC = ROOT / "docs" / "B150_felt_block_polish_and_source_register.md"
AUDIT = ROOT / "docs" / "B150_felt_block_polish_and_source_register_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B149_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
B149_END = "<!-- /B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END -->"

SRC_START = "<!-- B150_FELT_SOURCE_REGISTER_START -->"
SRC_END = "<!-- /B150_FELT_SOURCE_REGISTER_END -->"
CSS_START = "/* B150_FELT_BLOCK_POLISH_AND_SOURCE_REGISTER_START */"
CSS_END = "/* B150_FELT_BLOCK_POLISH_AND_SOURCE_REGISTER_END */"

SOURCE_SECTION_ANCHORS = [
    "Quellen, Methodik und Nutzungsrechte",
    "Methode in Kürze",
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


def get_block(text: str, start: str, end: str) -> str:
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.S)
    return m.group(1).strip() if m else ""


def extract_iframe(block: str) -> str:
    m = re.search(r"<iframe\b.*?</iframe>", block, re.S | re.I)
    return m.group(0).strip() if m else ""


def extract_share_url(block: str, iframe: str) -> str:
    m = re.search(r'href="(https://felt\.com/[^"]+)"', block, re.I)
    if m:
        return m.group(1)

    m = re.search(r"href='(https://felt\.com/[^']+)'", block, re.I)
    if m:
        return m.group(1)

    m = re.search(r'\ssrc="([^"]*felt\.com[^"]*)"', iframe, re.I)
    if m:
        return m.group(1)

    m = re.search(r"\ssrc='([^']*felt\.com[^']*)'", iframe, re.I)
    if m:
        return m.group(1)

    return ""


def build_polished_b149(iframe: str, share_url: str) -> str:
    safe_link = escape(share_url) if share_url else "#"
    return f"""{B149_START}
<section class="b149-felt-pilot" id="oberschwaben-felt-pilot" aria-labelledby="b149-felt-title" data-publication-state="candidate">
  <div class="section-inner">
    <div class="b149-felt-pilot__inner">
      <p class="eyebrow">Interaktive Karte</p>
      <h2 id="b149-felt-title">Die Schnittmenge wird als interaktive Karte lesbar</h2>
      <p class="b149-felt-pilot__lead">
        Die Karte zeigt die Überlagerung aus landwirtschaftlicher Nutzung und
        Moor-/Feuchtbodenkontext als scharfe Vektorkarte. Auf größeren Bildschirmen
        lassen sich Details per Klick prüfen; auf kleinen Bildschirmen öffnet die
        Karte in einem eigenen Tab.
      </p>

      <div class="b149-felt-pilot__desktop" aria-label="Interaktive Felt-Karte für Oberschwaben">
        <div class="b149-felt-pilot__frame">
          {iframe}
        </div>
      </div>

      <div class="b149-felt-pilot__mobile" role="note" aria-label="Mobile Alternative zur interaktiven Karte">
        <p class="b149-felt-pilot__mobile-title">Interaktive Karte separat öffnen</p>
        <p>
          Auf kleinen Bildschirmen ist die externe Kartenansicht in einem eigenen Tab
          besser lesbar. Die Kernaussage bleibt: Die Schnittmenge markiert Prüfbedarf,
          nicht automatisch Eignung.
        </p>
        <a class="b149-felt-pilot__button" href="{safe_link}" target="_blank" rel="noopener noreferrer">
          Interaktive Karte öffnen
        </a>
      </div>

      <p class="b149-felt-pilot__source">
        Interaktive Karte: Felt; Basiskarte/Daten: OpenStreetMap. Eigene GIS-Aufbereitung
        aus landwirtschaftlicher Nutzung und BK50-Moor-/Feuchtbodenkontext, via mapshaper
        für den Webeinsatz vereinfacht. Orientierung, keine parzellenscharfe Eignungs-
        oder Priorisierungskarte. <a href="#methode-in-kuerze">Methode in Kürze</a>.
      </p>
    </div>
  </div>
</section>
{B149_END}"""


def build_source_register() -> str:
    return f"""{SRC_START}
<div class="b150-felt-source-register" role="note" aria-label="Quellenhinweis zur interaktiven Oberschwaben-Karte">
  <h3>Interaktive Oberschwaben-Karte</h3>
  <p>
    Felt-Embed mit Basiskarte und Hintergrunddaten von OpenStreetMap. Eigene GIS-Aufbereitung
    aus FIONA 2024, BK50-Moor-/Feuchtbodenkontext und GISCO/NUTS-Landkreisgrenzen;
    vereinfachter GeoJSON-Export via mapshaper. Die Darstellung ist eine Orientierungskarte
    für Prüfbedarf, keine hydrologische Modellierung und keine parzellenscharfe Eignungs-
    oder Priorisierungskarte.
  </p>
</div>
{SRC_END}"""


def insert_source_register(html: str, audit: list[str]) -> str:
    html = strip_block(html, SRC_START, SRC_END)

    source_block = build_source_register()

    for anchor in SOURCE_SECTION_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        # Avoid nav hits for generic "Quellen"
        if anchor == "Quellen" and pos < 1500:
            continue

        section_start = html.rfind("<section", 0, pos)
        section_end = html.find("</section>", pos)

        if section_start < 0 or section_end < 0:
            audit.append(f"WARN source anchor found but section bounds missing: {anchor}")
            continue

        close_pos = section_end
        audit.append(f"OK inserted B150 source register before end of section containing anchor: {anchor}")
        return html[:close_pos] + "\n" + source_block + "\n" + html[close_pos:]

    audit.append("WARN no central sources section found; B150 source register not inserted")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b150-felt-source-register {{
  max-width: 58rem;
  margin: 1.25rem 0 0;
  padding: 0.95rem 1rem;
  border-left: 3px solid rgba(8, 127, 122, 0.68);
  border-radius: 0.8rem;
  background: rgba(255, 255, 255, 0.5);
}}

.b150-felt-source-register h3 {{
  margin: 0 0 0.35rem;
  font-size: 1rem;
  line-height: 1.25;
  color: #1e2d25;
}}

.b150-felt-source-register p {{
  margin: 0;
  color: var(--muted, #637266);
  font-size: 0.9rem;
  line-height: 1.5;
}}

@media (max-width: 720px) {{
  .b150-felt-source-register {{
    padding: 0.85rem 0.9rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B150 Felt block polish and source register: polished public wording for the Felt map block and added a central source-register note ({date.today().isoformat()})."
    if "B150 Felt block polish and source register" in done_text:
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

    b149_block = get_block(html, B149_START, B149_END)
    if not b149_block:
        raise SystemExit("B149 block not found in index.html. Run B149 first.")

    iframe = extract_iframe(b149_block)
    share_url = extract_share_url(b149_block, iframe)

    audit.append(f"B149 block found: {bool(b149_block)}")
    audit.append(f"iframe preserved from B149 block: {bool(iframe)}")
    audit.append(f"share URL preserved from B149 block: {bool(share_url)}")

    if not iframe:
        raise SystemExit("No iframe found in B149 block; cannot polish Felt block safely.")

    html = strip_block(html, B149_START, B149_END)
    insert_pos = html.find("</section>", html.find("Oberschwaben, wo Moorschutz auf Landwirtschaft trifft"))
    if insert_pos < 0:
        # fallback: insert before the existing old B149 position by stripping did not preserve position,
        # so use source section anchor fallback.
        raise SystemExit("Could not locate Oberschwaben section after stripping B149 block.")

    insert_pos += len("</section>")
    html = html[:insert_pos] + "\n\n" + build_polished_b149(iframe, share_url) + "\n" + html[insert_pos:]
    audit.append("OK replaced B149 block with polished wording")

    html = insert_source_register(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B150 - Felt Block Polish and Source Register

Date: {today}

## Ziel

B150 macht den B149-Felt-Block sprachlich publikationstauglicher und ergänzt den zentralen
Quellennachweis um einen Eintrag zur interaktiven Oberschwaben-Karte.

## Umsetzung

- `Interaktiver Kartenpilot` wird zu `Interaktive Karte`
- öffentlicher Text entfernt interne Prototyp-Sprache
- Desktop-/Mobile-Logik bleibt unverändert
- iframe und Felt-Link bleiben aus B149 erhalten
- Quellen-/Methodenzeile im Kartenblock wird präzisiert
- zentraler Quellennachweis erhält einen Hinweis zu:
  - Felt
  - OpenStreetMap
  - FIONA 2024
  - BK50-Moor-/Feuchtbodenkontext
  - GISCO/NUTS-Landkreisgrenzen
  - mapshaper-Vereinfachung

## Nicht geändert

- kein Austausch der bestehenden Oberschwaben-Karte
- keine Änderung an Kartenlogik
- keine lokalen GeoJSON-/Shapefile-Dateien im Repo
- kein Entfernen des PNG-Fallbacks

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/150_felt_block_polish_and_source_register.py`
- `docs/B150_felt_block_polish_and_source_register.md`
- `docs/B150_felt_block_polish_and_source_register_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Felt-Block wirkt nicht mehr wie interner Prototyp.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt sichtbar unter 760 px.
- Zentraler Quellenblock enthält den Felt-/OSM-/mapshaper-Hinweis.
"""
    write(DOC, doc_text)

    audit_text = "# B150 Felt block polish and source register audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B150 Felt block polish and source register complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B150_felt_block_polish_and_source_register.md")
    print("  docs/B150_felt_block_polish_and_source_register_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
