from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "151_felt_external_service_notice.py"
DOC = ROOT / "docs" / "B151_felt_external_service_notice.md"
AUDIT = ROOT / "docs" / "B151_felt_external_service_notice_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B149_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
B149_END = "<!-- /B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END -->"

HTML_NOTICE_START = "<!-- B151_FELT_EXTERNAL_SERVICE_NOTICE_START -->"
HTML_NOTICE_END = "<!-- /B151_FELT_EXTERNAL_SERVICE_NOTICE_END -->"
CSS_START = "/* B151_FELT_EXTERNAL_SERVICE_NOTICE_START */"
CSS_END = "/* B151_FELT_EXTERNAL_SERVICE_NOTICE_END */"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def get_block_bounds(text: str, start: str, end: str) -> tuple[int, int] | None:
    m = re.search(re.escape(start) + r".*?" + re.escape(end), text, re.S)
    if not m:
        return None
    return m.start(), m.end()


def build_notice() -> str:
    return f"""{HTML_NOTICE_START}
<p class="b151-felt-external-notice">
  Drittanbieter-Hinweis: Die interaktive Karte wird über Felt geladen und nutzt
  Hintergrunddaten von OpenStreetMap. Beim Öffnen oder Laden der Karte können
  Verbindungsdaten an externe Kartendienste übertragen werden. Die statische
  Kartenfassung im Abschnitt bleibt als Fallback erhalten.
</p>
{HTML_NOTICE_END}"""


def insert_notice_into_b149(html: str, audit: list[str]) -> str:
    html = strip_block(html, HTML_NOTICE_START, HTML_NOTICE_END)

    bounds = get_block_bounds(html, B149_START, B149_END)
    if not bounds:
        audit.append("ERROR B149 block not found")
        return html

    start, end = bounds
    block = html[start:end]

    source_pos = block.find('class="b149-felt-pilot__source"')
    if source_pos >= 0:
        p_end = block.find("</p>", source_pos)
        if p_end >= 0:
            insert_pos = start + p_end + len("</p>")
            audit.append("OK inserted B151 notice after b149 source line")
            return html[:insert_pos] + "\n" + build_notice() + html[insert_pos:]

    # fallback before section close
    close_pos = html.rfind("</section>", start, end)
    if close_pos >= 0:
        audit.append("WARN source line not found; inserted B151 notice before B149 section close")
        return html[:close_pos] + build_notice() + "\n" + html[close_pos:]

    audit.append("ERROR could not insert B151 notice into B149 block")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b151-felt-external-notice {{
  max-width: 56rem;
  margin: 0.65rem 0 0;
  padding: 0.72rem 0.85rem;
  border-left: 3px solid rgba(8, 127, 122, 0.46);
  border-radius: 0.72rem;
  background: rgba(255, 255, 255, 0.42);
  color: var(--muted, #637266);
  font-size: 0.82rem;
  line-height: 1.45;
}}

@media (max-width: 760px) {{
  .b151-felt-external-notice {{
    font-size: 0.79rem;
    padding: 0.68rem 0.78rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B151 Felt external-service notice: added a compact third-party map-service notice below the Felt map block ({date.today().isoformat()})."
    if "B151 Felt external-service notice" in done_text:
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

    audit.append(f"B149 block present before patch: {B149_START in html and B149_END in html}")
    audit.append(f"Old B151 notice present before patch: {HTML_NOTICE_START in html and HTML_NOTICE_END in html}")
    audit.append(f"Old B151 CSS present before patch: {CSS_START in css and CSS_END in css}")

    html = insert_notice_into_b149(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B151 - Felt External-Service Notice

Date: {today}

## Ziel

B151 ergänzt den neuen Felt-Kartenblock um einen kompakten Drittanbieter-Hinweis.
Der Felt-iframe ist ein externer Kartenservice; das soll im Seitenfluss transparent sein,
ohne den Kartenblock zu dominieren.

## Umsetzung

Unterhalb der Quellen-/Methodenzeile des Felt-Blocks wird ein kurzer Hinweis eingefügt:

- Felt wird als externer Kartendienst geladen
- OpenStreetMap-Hintergrunddaten werden genutzt
- beim Laden/Öffnen können Verbindungsdaten an externe Kartendienste übertragen werden
- die statische Kartenfassung bleibt als Fallback erhalten

## Nicht geändert

- keine Änderung am iframe-Code
- keine Änderung an Felt-Link oder Share-URL
- keine Änderung an Kartenlogik
- keine Änderung an lokalen GeoJSON-/Shapefile-Dateien
- kein Datenschutz-/Impressum-Ersatz

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/151_felt_external_service_notice.py`
- `docs/B151_felt_external_service_notice.md`
- `docs/B151_felt_external_service_notice_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hinweis steht direkt unter dem Felt-Kartenblock.
- Hinweis ist lesbar, aber nicht dominant.
- Desktop-iframe lädt weiterhin.
- Mobile-Fallback bleibt unverändert.
"""
    write(DOC, doc_text)

    audit_text = "# B151 Felt external-service notice audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B151 Felt external-service notice complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B151_felt_external_service_notice.md")
    print("  docs/B151_felt_external_service_notice_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
