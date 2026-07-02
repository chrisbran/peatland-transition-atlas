from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "133_method_in_brief.py"
DOC = ROOT / "docs" / "B133_method_in_brief.md"
AUDIT = ROOT / "docs" / "B133_method_in_brief_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B133_METHOD_IN_BRIEF_START -->"
HTML_END = "<!-- /B133_METHOD_IN_BRIEF_END -->"
CSS_START = "/* B133_METHOD_IN_BRIEF_START */"
CSS_END = "/* B133_METHOD_IN_BRIEF_END */"

METHOD_ANCHOR = "Methodische Hinweise"
FOOTER_OLD = "Erstellt im Kontext von SOLAMO-BW / Universität Hohenheim."
FOOTER_NEW = "Entstanden im Kontext von SOLAMO-BW / Universität Hohenheim; eigenständiger fachlicher Demonstrator, kein offizielles Produkt."


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def build_method_box() -> str:
    return f"""{HTML_START}
              <div class="b133-method-in-brief" id="methode-in-kuerze">
                <h3>Methode in Kürze</h3>
                <p>
                  Die Seite kombiniert öffentliche Datengrundlagen und eigene kartografische Auswertungen.
                  Die großräumigen Karten nutzen internationale und nationale Referenzdaten; die regionale
                  Oberschwaben-Auswertung verschneidet FIONA 2024, BK50 Moor-/Feuchtbodenkontext und
                  GISCO NUTS 2024.
                </p>
                <p>
                  Die Flächenbilanz beruht auf einer eigenen Auswahl, Klassifikation und Verschneidung der
                  Nutzungsklassen mit dem Boden- und Feuchtbodenkontext. Die BK50 ist eine generalisierte
                  Bodenkarte im Maßstab 1:50.000. Sie eignet sich für räumliche Orientierung, aber nicht für
                  parzellenscharfe Eignungsentscheidungen.
                </p>
                <p>
                  Die Darstellung zeigt Prüfbedarf und typische Zusammenhänge. Sie ist keine hydrologische
                  Modellierung, keine Priorisierung, keine Eignungskarte und keine betriebliche
                  Betroffenheitsanalyse.
                </p>
              </div>
{HTML_END}"""


def insert_method_box(html: str, audit: list[str]) -> str:
    pos = html.find(METHOD_ANCHOR)
    if pos < 0:
        audit.append(f"ERROR method anchor not found: {METHOD_ANCHOR}")
        return html

    # Prefer inserting before the h3/heading that contains "Methodische Hinweise".
    heading_start = html.rfind("<h", 0, pos)
    if heading_start < 0:
        audit.append(f"ERROR no heading start found before anchor: {METHOD_ANCHOR}")
        return html

    block = build_method_box()
    audit.append(f"OK inserted method-in-brief before heading containing: {METHOD_ANCHOR}")
    return html[:heading_start] + block + "\n" + html[heading_start:]


def patch_footer(html: str, audit: list[str]) -> str:
    old_count = html.count(FOOTER_OLD)
    new_count = html.count(FOOTER_NEW)

    if old_count:
        html = html.replace(FOOTER_OLD, FOOTER_NEW)
        audit.append(f"OK footer wording replaced {old_count}x")
    elif new_count:
        audit.append("OK footer wording already updated")
    else:
        audit.append("WARN footer old/new wording not found; footer unchanged")

    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b133-method-in-brief {{
  margin: 1.15rem 0 1.5rem;
  padding: clamp(0.9rem, 2vw, 1.15rem);
  border-radius: 1rem;
  border: 1px solid rgba(26, 48, 38, 0.14);
  background: rgba(255, 255, 255, 0.54);
}}

.b133-method-in-brief h3 {{
  margin-top: 0;
}}

.b133-method-in-brief p {{
  max-width: 62rem;
}}

.b133-method-in-brief p:last-child {{
  margin-bottom: 0;
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B133 method in brief: added a compact method transparency block and clarified footer positioning ({date.today().isoformat()})."
    if "B133 method in brief" in done_text:
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
    audit.append(f"Old B133 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B133 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    html = insert_method_box(html, audit)
    html = patch_footer(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B133 - Method in Brief

Date: {today}

## Ziel

B133 ergänzt eine kompakte Methode-in-Kürze-Box im bestehenden Quellen-/Methodikbereich
und präzisiert die Projektnennung im Footer.

## Umsetzung

- neue Box `Methode in Kürze` vor `Methodische Hinweise`
- Anker `id="methode-in-kuerze"`
- kurze Beschreibung von Quellen, Datenständen, Verschneidungslogik und BK50-Generalisierung
- klare Abgrenzung: Orientierung, keine Flächeneignung oder Einzelfallentscheidung
- Footer präzisiert: eigenständiger fachlicher Demonstrator, kein offizielles Produkt

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/133_method_in_brief.py`
- `docs/B133_method_in_brief.md`
- `docs/B133_method_in_brief_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Quellenblock öffnen.
- `Methode in Kürze` steht vor `Methodische Hinweise`.
- Text ist kompakt und nicht zu technisch.
- Footer-Projektnennung ist präzisiert.
- Keine Layout-Verschiebung im Quellenblock.
"""
    write(DOC, doc_text)

    audit_text = "# B133 method in brief audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B133 method in brief patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B133_method_in_brief.md")
    print("  docs/B133_method_in_brief_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
