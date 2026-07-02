from pathlib import Path
import re
from datetime import date
from html import escape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "152_oberschwaben_felt_integration_consolidation.py"
DOC = ROOT / "docs" / "B152_oberschwaben_felt_integration_consolidation.md"
AUDIT = ROOT / "docs" / "B152_oberschwaben_felt_integration_consolidation_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B149_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
B149_END = "<!-- /B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END -->"

B151_START = "<!-- B151_FELT_EXTERNAL_SERVICE_NOTICE_START -->"
B151_END = "<!-- /B151_FELT_EXTERNAL_SERVICE_NOTICE_END -->"

CSS_START = "/* B152_OBERSCHWABEN_FELT_INTEGRATION_CONSOLIDATION_START */"
CSS_END = "/* B152_OBERSCHWABEN_FELT_INTEGRATION_CONSOLIDATION_END */"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def find_block(text: str, start: str, end: str) -> tuple[int, int, str] | None:
    m = re.search(re.escape(start) + r".*?" + re.escape(end), text, re.S)
    if not m:
        return None
    return m.start(), m.end(), m.group(0)


def extract_iframe(block: str) -> str:
    m = re.search(r"<iframe\b.*?</iframe>", block, re.S | re.I)
    return m.group(0).strip() if m else ""


def extract_share_url(block: str, iframe: str) -> str:
    # Prefer the mobile fallback button href.
    for pattern in [
        r'href="(https://felt\.com/[^"]+)"',
        r"href='(https://felt\.com/[^']+)'",
        r'\ssrc="([^"]*felt\.com[^"]*)"',
        r"\ssrc='([^']*felt\.com[^']*)'",
    ]:
        m = re.search(pattern, block if "href" in pattern else iframe, re.I)
        if m:
            return m.group(1)
    return ""


def extract_or_default_notice(block: str) -> str:
    m = re.search(re.escape(B151_START) + r".*?" + re.escape(B151_END), block, re.S)
    if m:
        return m.group(0).strip()

    return f"""{B151_START}
<p class="b151-felt-external-notice">
  Drittanbieter-Hinweis: Die interaktive Karte wird über Felt geladen und nutzt
  Hintergrunddaten von OpenStreetMap. Beim Öffnen oder Laden der Karte können
  Verbindungsdaten an externe Kartendienste übertragen werden. Die statische
  Kartenfassung im Abschnitt bleibt als Fallback erhalten.
</p>
{B151_END}"""


def normalize_iframe(iframe: str) -> str:
    # Keep all Felt-specific attributes/src, but ensure class/title/loading/fullscreen are present.
    if not iframe:
        return ""

    if "class=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe class="b149-felt-iframe"', 1)
    elif "b149-felt-iframe" not in iframe:
        iframe = re.sub(r'class="([^"]*)"', r'class="\1 b149-felt-iframe"', iframe, count=1)

    if "title=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe title="Interaktive Oberschwaben-Karte: Schnittmenge aus Nutzung und Moor-/Feuchtbodenkontext"', 1)

    if "loading=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe loading="lazy"', 1)

    if "allowfullscreen" not in iframe.lower():
        iframe = iframe.replace("<iframe", "<iframe allowfullscreen", 1)

    # Layout is controlled by CSS.
    iframe = re.sub(r'\swidth\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\swidth\s*=\s*'[^']*'", "", iframe, flags=re.I)
    iframe = re.sub(r'\sheight\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\sheight\s*=\s*'[^']*'", "", iframe, flags=re.I)
    iframe = re.sub(r'\sstyle\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\sstyle\s*=\s*'[^']*'", "", iframe, flags=re.I)

    return iframe


def build_consolidated_block(iframe: str, share_url: str, notice: str) -> str:
    safe_link = escape(share_url) if share_url else "#"

    return f"""{B149_START}
<section class="b149-felt-pilot b152-felt-integration" id="oberschwaben-felt-pilot" aria-labelledby="b149-felt-title" data-publication-state="candidate">
  <div class="section-inner">
    <div class="b149-felt-pilot__inner">
      <p class="eyebrow">Interaktive Vertiefung</p>
      <h2 id="b149-felt-title">Die statische Karte zeigt die Lage – die interaktive Karte zeigt die Details</h2>
      <p class="b149-felt-pilot__lead">
        Der vorherige Kartenabschnitt ordnet die Schnittmenge im Seitenfluss ein.
        Diese interaktive Version ist die Vertiefung: Sie zeigt dieselbe Kernaussage
        als scharfe Vektorkarte, mit Landkreisorientierung und Klick-Information zur
        Gesamtfläche der Schnittmenge.
      </p>

      <div class="b152-felt-bridge" role="note" aria-label="Einordnung der interaktiven Karte">
        <strong>Lesart:</strong>
        Die türkis markierten Bereiche zeigen Prüfbedarf, nicht automatisch Eignung.
        Für konkrete Maßnahmen bleiben Wasserstand, Betriebssituation, Eigentum,
        Förderung und Wertschöpfung entscheidend.
      </div>

      <div class="b149-felt-pilot__desktop" aria-label="Interaktive Felt-Karte für Oberschwaben">
        <div class="b149-felt-pilot__frame">
          {iframe}
        </div>
      </div>

      <div class="b149-felt-pilot__mobile" role="note" aria-label="Mobile Alternative zur interaktiven Karte">
        <p class="b149-felt-pilot__mobile-title">Interaktive Vertiefung separat öffnen</p>
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
      {notice}
    </div>
  </div>
</section>
{B149_END}"""


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b152-felt-integration {{
  margin-top: clamp(0.75rem, 2vw, 1.5rem);
  padding-block: clamp(2.4rem, 5vw, 4.6rem);
}}

.b152-felt-integration .eyebrow {{
  color: #76964e;
}}

.b152-felt-integration h2 {{
  max-width: 22ch;
}}

.b152-felt-bridge {{
  max-width: 54rem;
  margin: 0.95rem 0 1.15rem;
  padding: 0.78rem 0.95rem;
  border-left: 3px solid rgba(8, 127, 122, 0.64);
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.55);
  color: var(--muted, #637266);
  font-size: 0.94rem;
  line-height: 1.52;
}}

.b152-felt-bridge strong {{
  color: #24352c;
}}

.b152-felt-integration .b149-felt-pilot__frame {{
  height: min(70vh, 48rem);
  min-height: 32rem;
}}

.b152-felt-integration .b149-felt-pilot__source {{
  margin-top: 0.75rem;
}}

.b152-felt-integration .b151-felt-external-notice {{
  margin-top: 0.55rem;
}}

@media (max-width: 760px) {{
  .b152-felt-integration {{
    padding-block: 1.5rem 2.1rem;
  }}

  .b152-felt-integration h2 {{
    max-width: none;
  }}

  .b152-felt-bridge {{
    margin-block: 0.8rem 0.95rem;
    padding: 0.72rem 0.82rem;
    font-size: 0.88rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B152 Oberschwaben/Felt integration consolidation: reframed the Felt block as an interactive deepening of the static Oberschwaben map and reduced redundancy ({date.today().isoformat()})."
    if "B152 Oberschwaben/Felt integration consolidation" in done_text:
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

    block_info = find_block(html, B149_START, B149_END)
    if not block_info:
        raise SystemExit("B149 Felt block not found in index.html. Run B149/B150/B151 before B152.")

    start, end, old_block = block_info
    iframe = normalize_iframe(extract_iframe(old_block))
    share_url = extract_share_url(old_block, iframe)
    notice = extract_or_default_notice(old_block)

    audit.append("B149 block found: True")
    audit.append(f"iframe preserved: {bool(iframe)}")
    audit.append(f"share URL preserved: {bool(share_url)}")
    audit.append(f"B151 notice preserved or defaulted: {bool(notice)}")

    if not iframe:
        raise SystemExit("No iframe found in B149 block; refusing to rewrite.")

    new_block = build_consolidated_block(iframe, share_url, notice)
    html = html[:start] + new_block + html[end:]
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B152 - Oberschwaben/Felt Integration Consolidation

Date: {today}

## Ziel

B152 reduziert die Redundanz zwischen der bestehenden Oberschwaben-Karte und dem neuen
Felt-Block. Die Felt-Karte wird nicht mehr als weiterer Kartenabschnitt neben der alten Karte
gerahmt, sondern als interaktive Vertiefung der vorherigen statischen Story-Karte.

## Umsetzung

- Eyebrow: `Interaktive Vertiefung`
- neuer Titel:
  - `Die statische Karte zeigt die Lage – die interaktive Karte zeigt die Details`
- Text erklärt die Rollen:
  - vorherige Karte = Einordnung im Seitenfluss
  - Felt-Karte = interaktive Vertiefung
- zusätzliche Lesart-Box:
  - Schnittmenge = Prüfbedarf, nicht automatisch Eignung
  - konkrete Maßnahmen brauchen Wasserstand, Betrieb, Eigentum, Förderung und Wertschöpfung
- Desktop iframe bleibt erhalten
- Mobile Fallback bleibt erhalten
- Drittanbieter-Hinweis bleibt erhalten
- Quellen-/Methodenzeile bleibt erhalten
- lokale GeoJSON-/Shapefile-Dateien bleiben außerhalb des Repo

## Nicht geändert

- kein Entfernen der bestehenden Oberschwaben-Karte
- kein Entfernen des PNG-/Sticky-Fallbacks
- keine Änderung am Felt-iframe-Link
- keine Änderung an Kartenlogik oder Rohdaten

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/152_oberschwaben_felt_integration_consolidation.py`
- `docs/B152_oberschwaben_felt_integration_consolidation.md`
- `docs/B152_oberschwaben_felt_integration_consolidation_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Felt-Block wirkt als Vertiefung, nicht als Dopplung.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt sichtbar unter 760 px.
- Drittanbieter-Hinweis bleibt erhalten.
- Bestehende Oberschwaben-Karte bleibt unverändert vorhanden.
"""
    write(DOC, doc_text)

    audit_text = "# B152 Oberschwaben/Felt integration consolidation audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B152 Oberschwaben/Felt integration consolidation complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B152_oberschwaben_felt_integration_consolidation.md")
    print("  docs/B152_oberschwaben_felt_integration_consolidation_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
