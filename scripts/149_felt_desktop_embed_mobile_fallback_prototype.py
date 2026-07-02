from pathlib import Path
import re
from datetime import date
from html import escape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
CANDIDATE = ROOT / "docs" / "B146_felt_embed_candidate.md"

SCRIPT = ROOT / "scripts" / "149_felt_desktop_embed_mobile_fallback_prototype.py"
DOC = ROOT / "docs" / "B149_felt_desktop_embed_mobile_fallback_prototype.md"
AUDIT = ROOT / "docs" / "B149_felt_desktop_embed_mobile_fallback_prototype_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
HTML_END = "<!-- /B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END -->"
CSS_START = "/* B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START */"
CSS_END = "/* B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END */"

INSERT_AFTER_ANCHORS = [
    "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft",
    "Die regionale Karte zerlegt den Zusammenhang",
    "Oberschwaben",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def extract_iframe(text: str) -> str:
    m = re.search(r"<iframe\b.*?</iframe>", text, re.S | re.I)
    if not m:
        return ""

    iframe = m.group(0).strip()

    # Let our CSS control size.
    iframe = re.sub(r'\swidth\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\swidth\s*=\s*'[^']*'", "", iframe, flags=re.I)
    iframe = re.sub(r'\sheight\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\sheight\s*=\s*'[^']*'", "", iframe, flags=re.I)
    iframe = re.sub(r'\sstyle\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\sstyle\s*=\s*'[^']*'", "", iframe, flags=re.I)

    if "class=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe class="b149-felt-iframe"', 1)

    if "title=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe title="Interaktive Oberschwaben-Karte als Felt-Pilot"', 1)

    if "loading=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe loading="lazy"', 1)

    if "allowfullscreen" not in iframe.lower():
        iframe = iframe.replace("<iframe", "<iframe allowfullscreen", 1)

    return iframe


def extract_share_url(text: str, iframe: str) -> str:
    urls = re.findall(r"https://felt\.com/map/[^\s)`\"<>]+", text)
    if urls:
        return urls[0]

    if iframe:
        m = re.search(r'\ssrc\s*=\s*"([^"]+)"', iframe, re.I)
        if not m:
            m = re.search(r"\ssrc\s*=\s*'([^']+)'", iframe, re.I)
        if m and "felt.com" in m.group(1):
            return m.group(1)

    urls = re.findall(r"https://felt\.com/[^\s)`\"<>]+", text)
    if urls:
        return urls[0]

    return ""


def build_html(iframe: str, share_url: str) -> str:
    safe_link = escape(share_url) if share_url else "#"
    return f"""{HTML_START}
<section class="b149-felt-pilot" id="oberschwaben-felt-pilot" aria-labelledby="b149-felt-title" data-publication-state="prototype">
  <div class="section-inner">
    <div class="b149-felt-pilot__inner">
      <p class="eyebrow">Interaktiver Kartenpilot</p>
      <h2 id="b149-felt-title">Die Schnittmenge wird als interaktive Karte lesbar</h2>
      <p class="b149-felt-pilot__lead">
        Der Felt-Pilot zeigt die Überlagerung aus landwirtschaftlicher Nutzung und
        Moor-/Feuchtbodenkontext als scharfe Vektorkarte. Er ist ein Integrationskandidat
        für größere Bildschirme; die bestehende Kartenfassung bleibt als Fallback erhalten.
      </p>

      <div class="b149-felt-pilot__desktop" aria-label="Interaktive Felt-Karte für Oberschwaben">
        <div class="b149-felt-pilot__frame">
          {iframe}
        </div>
      </div>

      <div class="b149-felt-pilot__mobile" role="note" aria-label="Mobile Alternative zur interaktiven Karte">
        <p class="b149-felt-pilot__mobile-title">Mobile Ansicht: interaktive Karte separat öffnen</p>
        <p>
          Auf kleinen Bildschirmen verdeckt die externe Kartenoberfläche viel Fläche.
          Deshalb bleibt die Seite mobil ruhig; die interaktive Felt-Karte öffnet in einem neuen Tab.
        </p>
        <a class="b149-felt-pilot__button" href="{safe_link}" target="_blank" rel="noopener noreferrer">
          Interaktive Karte öffnen
        </a>
      </div>

      <p class="b149-felt-pilot__source">
        Kartenpilot mit Felt auf Basis einer lokal vereinfachten GeoJSON-Schnittmenge aus
        landwirtschaftlicher Nutzung und BK50-Moor-/Feuchtbodenkontext. Schematische Orientierung,
        keine parzellenscharfe Eignungs- oder Priorisierungskarte.
        <a href="#methode-in-kuerze">Methode in Kürze</a>.
      </p>
    </div>
  </div>
</section>
{HTML_END}"""


def find_insert_position(html: str, audit: list[str]) -> int | None:
    for anchor in INSERT_AFTER_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        # Skip early header/nav occurrences of broad fallback.
        if anchor == "Oberschwaben" and pos < 1200:
            continue

        section_start = html.rfind("<section", 0, pos)
        section_end = html.find("</section>", pos)
        if section_start < 0 or section_end < 0:
            audit.append(f"WARN anchor found but section bounds missing: {anchor}")
            continue

        section_end += len("</section>")
        audit.append(f"OK insertion after section containing anchor: {anchor}")
        return section_end

    audit.append("ERROR no insertion anchor found")
    return None


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b149-felt-pilot {{
  padding-block: clamp(2.25rem, 5vw, 4.25rem);
  background:
    radial-gradient(circle at 50% 0%, rgba(8, 127, 122, 0.07), transparent 38%),
    linear-gradient(180deg, rgba(248, 245, 236, 0.84), rgba(248, 245, 236, 0.96));
}}

.b149-felt-pilot .section-inner {{
  width: min(100% - 2rem, 74rem);
  margin-inline: auto;
}}

.b149-felt-pilot__inner {{
  max-width: 68rem;
  margin-inline: auto;
}}

.b149-felt-pilot h2 {{
  max-width: 15ch;
  margin-bottom: 0.65rem;
}}

.b149-felt-pilot__lead {{
  max-width: 51rem;
  color: var(--muted, #637266);
  font-size: clamp(1rem, 1.7vw, 1.14rem);
  line-height: 1.55;
}}

.b149-felt-pilot__desktop {{
  display: block;
  margin-top: 1.2rem;
}}

.b149-felt-pilot__frame {{
  position: relative;
  width: 100%;
  min-height: 36rem;
  height: min(76vh, 52rem);
  overflow: hidden;
  border-radius: 1.1rem;
  border: 1px solid rgba(26, 48, 38, 0.16);
  background: #101510;
  box-shadow: 0 22px 64px rgba(26, 48, 38, 0.18);
}}

.b149-felt-pilot__frame iframe,
.b149-felt-iframe {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}}

.b149-felt-pilot__mobile {{
  display: none;
  margin-top: 1.2rem;
  border-radius: 1rem;
  border: 1px solid rgba(26, 48, 38, 0.13);
  background: rgba(255, 255, 255, 0.52);
  padding: 1rem;
}}

.b149-felt-pilot__mobile-title {{
  margin: 0 0 0.35rem;
  font-weight: 800;
  color: #1e2d25;
}}

.b149-felt-pilot__mobile p:not(.b149-felt-pilot__mobile-title) {{
  margin: 0 0 0.85rem;
  color: var(--muted, #637266);
  font-size: 0.95rem;
  line-height: 1.5;
}}

.b149-felt-pilot__button {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.55rem;
  padding: 0.62rem 0.9rem;
  border-radius: 999px;
  background: #087f7a;
  color: #ffffff;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 10px 24px rgba(8, 127, 122, 0.22);
}}

.b149-felt-pilot__button:hover {{
  text-decoration: underline;
  text-underline-offset: 0.18em;
}}

.b149-felt-pilot__source {{
  max-width: 56rem;
  margin: 0.85rem 0 0;
  color: var(--muted, #637266);
  font-size: 0.84rem;
  line-height: 1.45;
}}

.b149-felt-pilot__source a {{
  color: inherit;
  font-weight: 700;
  text-underline-offset: 0.16em;
}}

@media (max-width: 760px) {{
  .b149-felt-pilot {{
    padding-block: 1.6rem 2.4rem;
  }}

  .b149-felt-pilot .section-inner {{
    width: min(100% - 1.25rem, 74rem);
  }}

  .b149-felt-pilot h2 {{
    max-width: none;
  }}

  .b149-felt-pilot__desktop {{
    display: none;
  }}

  .b149-felt-pilot__mobile {{
    display: block;
  }}

  .b149-felt-pilot__source {{
    font-size: 0.8rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B149 Felt desktop embed/mobile fallback prototype: added a reversible page-level prototype with desktop iframe and mobile external-link fallback ({date.today().isoformat()})."
    if "B149 Felt desktop embed/mobile fallback prototype" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")
    if not CANDIDATE.exists():
        raise SystemExit("docs/B146_felt_embed_candidate.md not found. Add Felt iframe/share URL there first.")

    candidate_text = read(CANDIDATE)
    iframe = extract_iframe(candidate_text)
    share_url = extract_share_url(candidate_text, iframe)

    audit.append(f"Felt iframe detected in B146 candidate: {bool(iframe)}")
    audit.append(f"Felt share URL detected in B146 candidate: {bool(share_url)}")
    if share_url:
        audit.append(f"Felt share URL: {share_url}")

    if not iframe:
        raise SystemExit("No Felt iframe found in docs/B146_felt_embed_candidate.md. Paste the iframe code there before running B149.")

    html = read(INDEX)
    css = read(CSS)

    old_html_present = HTML_START in html and HTML_END in html
    old_css_present = CSS_START in css and CSS_END in css
    audit.append(f"Old B149 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B149 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    insert_pos = find_insert_position(html, audit)
    if insert_pos is None:
        raise SystemExit("No suitable insertion point found for B149.")

    html = html[:insert_pos] + "\n\n" + build_html(iframe, share_url) + "\n" + html[insert_pos:]
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B149 - Felt Desktop Embed / Mobile Fallback Prototype

Date: {today}

## Ziel

B149 setzt die in B148 dokumentierte Responsive-Strategie als kontrollierten Seiten-Prototyp um.

- Desktop/Tablet: Felt iframe wird angezeigt.
- Mobile unter 760 px: kein iframe, sondern kurzer Fallback-Block mit externem Felt-Link.
- Bestehende Kartenlogik und bestehende Assets bleiben erhalten.
- Keine lokalen GeoJSON/Shapefile-Daten werden ins Repo aufgenommen.

## Umsetzung

Der neue Abschnitt wird nach dem Oberschwaben-Kartenabschnitt eingefügt.

Titel:

```text
Die Schnittmenge wird als interaktive Karte lesbar
```

Mobile-Fallback:

```text
Interaktive Karte öffnen
```

## Technische Entscheidung

Der Felt-iframe wird aus `docs/B146_felt_embed_candidate.md` gelesen.
Breite/Höhe des iframe-Codes werden entfernt und über CSS gesteuert.

Breakpoint:

```css
@media (max-width: 760px)
```

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/149_felt_desktop_embed_mobile_fallback_prototype.py`
- `docs/B149_felt_desktop_embed_mobile_fallback_prototype.md`
- `docs/B149_felt_desktop_embed_mobile_fallback_prototype_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Desktop: Felt-Karte lädt und steht nach dem Oberschwaben-Abschnitt.
- Desktop: Annotation, Legende und Popup funktionieren.
- Mobile 390 px: iframe ist nicht sichtbar.
- Mobile: Fallback-Box mit Button ist sichtbar.
- Button öffnet die Felt-Karte in neuem Tab.
- Bestehende Oberschwaben-Karte ist nicht gelöscht.
"""
    write(DOC, doc_text)

    audit_text = "# B149 Felt desktop embed/mobile fallback prototype audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B149 Felt desktop embed/mobile fallback prototype complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B149_felt_desktop_embed_mobile_fallback_prototype.md")
    print("  docs/B149_felt_desktop_embed_mobile_fallback_prototype_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
