from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "158_reduce_notice_density.py"
DOC = ROOT / "docs" / "B158_reduce_notice_density.md"
AUDIT = ROOT / "docs" / "B158_reduce_notice_density_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B152_BRIDGE_RE = re.compile(
    r"\s*<div class=\"b152-felt-bridge\" role=\"note\" aria-label=\"Einordnung der interaktiven Karte\">\s*"
    r"<strong>Lesart:</strong>\s*"
    r"Die türkis markierten Bereiche zeigen Prüfbedarf, nicht automatisch Eignung\.\s*"
    r"Für konkrete Maßnahmen bleiben Wasserstand, Betriebssituation, Eigentum,\s*"
    r"Förderung und Wertschöpfung entscheidend\.\s*"
    r"</div>\s*",
    re.S,
)

B151_RE = re.compile(
    r"<!-- B151_FELT_EXTERNAL_SERVICE_NOTICE_START -->\s*"
    r"<p class=\"b151-felt-external-notice\">\s*"
    r".*?"
    r"</p>\s*"
    r"<!-- /B151_FELT_EXTERNAL_SERVICE_NOTICE_END -->",
    re.S,
)

B157_RE = re.compile(
    r"<!-- B157_AREA_BALANCE_METHOD_NOTE_START -->\s*"
    r"<p class=\"b157-area-method-note\">\s*"
    r".*?"
    r"</p>\s*"
    r"<!-- /B157_AREA_BALANCE_METHOD_NOTE_END -->",
    re.S,
)

CSS_START = "/* B158_REDUCE_NOTICE_DENSITY_START */"
CSS_END = "/* B158_REDUCE_NOTICE_DENSITY_END */"

B151_COMPACT = """<!-- B151_FELT_EXTERNAL_SERVICE_NOTICE_START -->
<p class="b151-felt-external-notice">
  Externer Kartendienst: Felt/OpenStreetMap. Details stehen im Quellen- und Methodenbereich.
</p>
<!-- /B151_FELT_EXTERNAL_SERVICE_NOTICE_END -->"""

B157_DETAILS = """<!-- B157_AREA_BALANCE_METHOD_NOTE_START -->
<details class="b157-area-method-note">
  <summary>Berechnungsgrundlage der Hektarbilanz</summary>
  <p>
    Die Hektarbilanz basiert auf der ursprünglichen GIS-Verschneidung von FIONA 2024,
    BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024. Die für Felt/mapshaper
    vereinfachte Web-Geometrie wurde nicht für die Flächenberechnung verwendet.
  </p>
</details>
<!-- /B157_AREA_BALANCE_METHOD_NOTE_END -->"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_css_block(css: str) -> str:
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r"\s*", re.S)
    return pattern.sub("", css)


def patch_css(css: str) -> str:
    css = strip_css_block(css)

    block = f"""
{CSS_START}
/* B158 notice-density reduction: keep caveats available, but remove repeated visual boxes. */
.b152-felt-integration .b152-felt-bridge {{
  display: none;
}}

.b151-felt-external-notice {{
  max-width: 56rem;
  margin: 0.42rem 0 0;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: var(--muted, #637266);
  font-size: 0.76rem;
  line-height: 1.42;
}}

.b157-area-method-note {{
  max-width: 58rem;
  margin: 0.58rem 0 0;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: var(--muted, #637266);
  font-size: 0.8rem;
  line-height: 1.45;
}}

.b157-area-method-note summary {{
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--muted, #637266);
  font-weight: 700;
  text-decoration: underline;
  text-decoration-thickness: 0.08em;
  text-underline-offset: 0.18em;
}}

.b157-area-method-note summary:hover {{
  color: #24352c;
}}

.b157-area-method-note p {{
  max-width: 54rem;
  margin: 0.45rem 0 0;
  padding: 0.65rem 0.78rem;
  border-left: 3px solid rgba(8, 127, 122, 0.42);
  border-radius: 0.65rem;
  background: rgba(255, 255, 255, 0.42);
}}

@media (max-width: 760px) {{
  .b151-felt-external-notice,
  .b157-area-method-note {{
    font-size: 0.75rem;
  }}

  .b157-area-method-note p {{
    padding: 0.62rem 0.72rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B158 reduce notice density: reduced visible warning/notice clutter by removing the Felt Lesart box, shortening the external-service notice and collapsing the area-balance method note ({today})."
    if "B158 reduce notice density" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    html = read(INDEX)
    css = read(CSS)

    today = date.today().isoformat()
    audit = []

    b152_matches = len(B152_BRIDGE_RE.findall(html))
    html, b152_n = B152_BRIDGE_RE.subn("\n", html)
    audit.append(f"Removed B152 Felt Lesart box matches: {b152_n} (found {b152_matches})")

    b151_matches = len(B151_RE.findall(html))
    html, b151_n = B151_RE.subn(B151_COMPACT, html)
    audit.append(f"Compacted B151 external-service notice matches: {b151_n} (found {b151_matches})")

    b157_matches = len(B157_RE.findall(html))
    html, b157_n = B157_RE.subn(B157_DETAILS, html)
    audit.append(f"Collapsed B157 area method note matches: {b157_n} (found {b157_matches})")

    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    doc_text = f"""# B158 - Reduce Notice Density

Date: {today}

## Ziel

Nach B157 war die Seite fachlich sehr abgesichert, aber visuell zu stark von Hinweisen,
Lesarten und Warnboxen geprägt. B158 reduziert diese Hinweisdichte, ohne die fachlichen
Grenzen zu entfernen.

## Prinzip

- wichtige Einschränkungen bleiben erhalten
- weniger sichtbare Boxen im Lesefluss
- Detailmethodik wird aufklappbar
- Drittanbieter-Hinweis wird kurz und ruhig
- keine Änderung an Karten, Zahlen, Quellen oder Daten

## Änderungen

1. **Felt-Lesart-Box entfernt**
   - Die Aussage `Schnittmenge = Prüfbedarf, nicht Eignung` bleibt bereits in Karte,
     Quellenzeile, Mobile-Fallback und Methodik erhalten.
   - Die zusätzliche Box war redundant.

2. **Drittanbieter-Hinweis gekürzt**
   - vorher: längerer Warnhinweis unter dem Felt-Block
   - jetzt: kurze Fußnotenzeile mit Verweis auf den Quellen-/Methodenbereich

3. **Methodennotiz zur Hektarbilanz eingeklappt**
   - die methodische Absicherung bleibt verfügbar
   - sie dominiert aber nicht mehr direkt den Flächenbilanz-Abschnitt

## Nicht geändert

- `~19.900 ha`
- Felt-iframe
- Mobile-Fallback
- Quellenregister
- zentrale Methode
- statische Oberschwaben-Karte
- Datenbasis

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Seite wirkt weniger von Warn-/Hinweisboxen überladen.
- Felt-Block bleibt verständlich.
- Hektarbilanz bleibt methodisch absicherbar.
- Keine Layoutverschiebung.
"""
    write(DOC, doc_text)

    audit_text = "# B158 reduce notice density audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    if b152_n == 0 or b151_n == 0 or b157_n == 0:
        audit_text += "WARN: At least one expected notice pattern was not replaced. Check page manually; prior patches may have changed wording.\n"
    else:
        audit_text += "OK: Expected notice-density reductions were applied.\n"
    audit_text += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B158 reduce notice density complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B158_reduce_notice_density.md")
    print("  docs/B158_reduce_notice_density_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
