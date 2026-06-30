from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "138_soil_context_precision_note.py"
DOC = ROOT / "docs" / "B138_soil_context_precision_note.md"
AUDIT = ROOT / "docs" / "B138_soil_context_precision_note_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B138_SOIL_CONTEXT_PRECISION_START -->"
HTML_END = "<!-- /B138_SOIL_CONTEXT_PRECISION_END -->"
CSS_START = "/* B138_SOIL_CONTEXT_PRECISION_START */"
CSS_END = "/* B138_SOIL_CONTEXT_PRECISION_END */"

INSERT_AFTER_ANCHORS = [
    "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft",
    "Die Schnittmenge macht den Prüfbedarf sichtbar, nicht die Lösung",
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


def build_note_html() -> str:
    return f"""{HTML_START}
<div class="b138-soil-context-note" role="note" aria-label="Begriffliche Einordnung der regionalen Bodenkulisse">
  <p class="b138-soil-context-note__label">Begriffliche Einordnung</p>
  <p>
    Die regionale Karte zeigt keinen parzellenscharfen Nachweis aktueller Moorböden.
    Sie nutzt den BK50-Moor- und Feuchtbodenkontext als Orientierungskulisse:
    organische Böden, Feuchtbodenlagen und bodenkundlich verwandte Hinweise werden
    bewusst als Prüfkontext gelesen, nicht als Flächeneignung.
  </p>
</div>
{HTML_END}"""


def insert_after_intro_paragraph(html: str, audit: list[str]) -> str:
    for anchor in INSERT_AFTER_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        section_start = html.rfind("<section", 0, pos)
        if section_start < 0:
            audit.append(f"WARN anchor found but no section before it: {anchor}")
            continue

        section_end = html.find("</section>", pos)
        if section_end < 0:
            audit.append(f"WARN anchor found but no section end after it: {anchor}")
            continue

        section = html[section_start:section_end]

        # Insert after the first paragraph following the anchor, preferably after the section lead.
        first_p_start_rel = section.find("<p", pos - section_start)
        if first_p_start_rel < 0:
            audit.append(f"WARN no paragraph found after anchor: {anchor}")
            continue

        first_p_end_rel = section.find("</p>", first_p_start_rel)
        if first_p_end_rel < 0:
            audit.append(f"WARN no paragraph end found after anchor: {anchor}")
            continue

        first_p_end_rel += len("</p>")
        insert_pos = section_start + first_p_end_rel

        audit.append(f"OK inserted B138 soil-context note after first paragraph in section containing anchor: {anchor}")
        return html[:insert_pos] + "\n" + build_note_html() + html[insert_pos:]

    audit.append("ERROR no insertion anchor found for B138")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b138-soil-context-note {{
  max-width: 46rem;
  margin: 1rem 0 1.25rem;
  padding: 0.85rem 0.95rem;
  border-left: 3px solid rgba(89, 123, 82, 0.72);
  background: rgba(255, 255, 255, 0.45);
  border-radius: 0.75rem;
}}

.b138-soil-context-note__label {{
  margin: 0 0 0.25rem;
  color: #5f735e;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 800;
}}

.b138-soil-context-note p:last-child {{
  margin-bottom: 0;
}}

.b138-soil-context-note p:not(.b138-soil-context-note__label) {{
  color: var(--muted, #637266);
  font-size: 0.95rem;
  line-height: 1.55;
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B138 soil-context precision note: clarified that the regional BK50 layer is a Moor-/Feuchtbodenkontext, not a parcel-level peat-soil proof or suitability map ({date.today().isoformat()})."
    if "B138 soil-context precision note" in done_text:
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
    audit.append(f"Old B138 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B138 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    html = insert_after_intro_paragraph(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B138 - Soil Context Precision Note

Date: {today}

## Ziel

B138 schärft die fachliche Begrifflichkeit im Oberschwaben-Abschnitt.
Die regionale Karte soll nicht als parzellenscharfer Moorbodennachweis oder Eignungskarte
verstanden werden, sondern als BK50-basierte Moor-/Feuchtbodenkulisse für Prüfbedarf.

## Umsetzung

- kurze Note im Oberschwaben-Abschnitt
- Begriffsklärung: BK50-Moor- und Feuchtbodenkontext
- klare Abgrenzung: Orientierungskulisse, keine Flächeneignung
- zurückhaltendes Layout als kleine redaktionelle Notiz
- keine Änderung an Kartenlogik, Daten, Navigation, Scorecard oder Quellenblock

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/138_soil_context_precision_note.py`
- `docs/B138_soil_context_precision_note.md`
- `docs/B138_soil_context_precision_note_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Note erscheint im Oberschwaben-Abschnitt.
- Sie ist sichtbar, aber nicht dominant.
- Sie klärt den BK50-Moor-/Feuchtbodenkontext.
- Karten, Navigation, Scorecard und Quellenblock bleiben unverändert.
"""
    write(DOC, doc_text)

    audit_text = "# B138 soil-context precision note audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B138 soil-context precision note patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B138_soil_context_precision_note.md")
    print("  docs/B138_soil_context_precision_note_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
