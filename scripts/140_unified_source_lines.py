from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "140_unified_source_lines.py"
DOC = ROOT / "docs" / "B140_unified_source_lines.md"
AUDIT = ROOT / "docs" / "B140_unified_source_lines_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CSS_START = "/* B140_UNIFIED_SOURCE_LINES_START */"
CSS_END = "/* B140_UNIFIED_SOURCE_LINES_END */"

METHOD_ID = "methode-in-kuerze"

NOTE_SPECS = [
    {
        "key": "FRAME_BRIDGE",
        "anchors": [
            "Moorbodenschutz beginnt als Klimathema",
            "Frame-Mismatch",
        ],
        "text": 'Schematische redaktionelle Einordnung; keine eigenständige Datenauswertung. <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "class": "",
    },
    {
        "key": "GLOBAL_CONTEXT",
        "anchors": [
            "Moore sind räumlich konzentriert und klimatisch wirksam",
            "Globale Moorverbreitung",
        ],
        "text": 'Kartografische Orientierung auf Basis der im zentralen Quellenverzeichnis genannten globalen Moor- und Referenzdaten; generalisierte Darstellung. <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "class": "",
    },
    {
        "key": "REGIONAL_CONTEXT",
        "anchors": [
            "Die Schnittmenge macht den Prüfbedarf sichtbar, nicht die Lösung",
            "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft",
            "Oberschwaben als Ausgangspunkt",
        ],
        "text": 'Eigene Verschneidung und kartografische Generalisierung aus FIONA 2024, BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024; Orientierung, keine Flächeneignung. <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "class": "",
    },
    {
        "key": "WATER_GOVERNANCE",
        "anchors": [
            "Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen",
            "Wasser und Governance",
        ],
        "text": 'Schematische Planungseinordnung; keine hydrologische Modellierung und keine Betroffenheitsanalyse. <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "class": "",
    },
    {
        "key": "CONSEQUENCE_KICKER",
        "anchors": [
            "Der Hebel verschiebt sich von der Fläche zur Kette",
        ],
        "text": 'Redaktionelle Schlussfolgerung aus Kartenstory, Wertschöpfungs-Scorecard und Methodikhinweisen; keine Priorisierung einzelner Flächen. <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "class": "",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_css_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def strip_existing_b140_notes(html: str) -> str:
    pattern = re.compile(r"<!-- B140_SOURCE_NOTE_[A-Z0-9_]+_START -->.*?<!-- /B140_SOURCE_NOTE_[A-Z0-9_]+_END -->\s*", re.S)
    return pattern.sub("", html)


def build_note(key: str, text: str, extra_class: str = "") -> str:
    classes = "b140-source-line"
    if extra_class:
        classes += " " + extra_class
    return f"""<!-- B140_SOURCE_NOTE_{key}_START -->
<p class="{classes}">{text}</p>
<!-- /B140_SOURCE_NOTE_{key}_END -->"""


def find_section_for_anchors(html: str, anchors: list[str], audit: list[str], key: str) -> tuple[int, int, str] | None:
    for anchor in anchors:
        pos = html.find(anchor)
        if pos < 0:
            continue

        section_start = html.rfind("<section", 0, pos)
        section_end = html.find("</section>", pos)

        if section_start < 0 or section_end < 0:
            audit.append(f"WARN {key}: anchor found but section bounds missing: {anchor}")
            continue

        section_end += len("</section>")
        return section_start, section_end, anchor

    return None


def insert_note_before_section_end(html: str, spec: dict, audit: list[str]) -> str:
    found = find_section_for_anchors(html, spec["anchors"], audit, spec["key"])
    if not found:
        audit.append(f"MISS {spec['key']}: no anchor found")
        return html

    section_start, section_end, anchor = found
    close_start = html.rfind("</section>", section_start, section_end)

    if close_start < 0:
        audit.append(f"WARN {spec['key']}: closing section tag not found")
        return html

    note = build_note(spec["key"], spec["text"], spec.get("class", ""))
    audit.append(f"OK {spec['key']}: inserted source/method line before section end; anchor={anchor}")
    return html[:close_start] + note + "\n" + html[close_start:]


def patch_b130_sourcebox_method_link(html: str, audit: list[str]) -> str:
    old = "Die konkrete Darstellung ist eine redaktionelle Synthese aus diesen Quellen und dient der Orientierung."
    new = 'Die konkrete Darstellung ist eine redaktionelle Synthese aus diesen Quellen und dient der Orientierung. <a href="#methode-in-kuerze">Methode in Kürze</a>.'

    if new in html:
        audit.append("OK B130 sourcebox already contains method link")
        return html

    if old in html:
        html = html.replace(old, new, 1)
        audit.append("OK B130 sourcebox: added method link")
        return html

    audit.append("MISS B130 sourcebox: expected sentence not found")
    return html


def patch_css(css: str) -> str:
    css = strip_css_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b140-source-line {{
  max-width: 54rem;
  margin: 0.9rem 0 0;
  color: var(--muted, #637266);
  font-size: 0.88rem;
  line-height: 1.45;
}}

.b140-source-line a,
.b130-source-box a {{
  color: inherit;
  font-weight: 700;
  text-underline-offset: 0.16em;
  text-decoration-thickness: 0.08em;
}}

.section-dark .b140-source-line,
.b130-engpass-climax .b140-source-line {{
  color: rgba(246, 242, 232, 0.68);
}}

.section-dark .b140-source-line a,
.b130-engpass-climax .b140-source-line a,
.b130-source-box a {{
  color: rgba(246, 242, 232, 0.9);
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B140 unified source lines: added compact source/method lines and method links for key V2 narrative and map blocks ({date.today().isoformat()})."
    if "B140 unified source lines" in done_text:
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

    method_present = f'id="{METHOD_ID}"' in html
    audit.append(f"Method anchor present before patch: {method_present}")
    audit.append(f"Existing B140 note blocks before patch: {len(re.findall(r'B140_SOURCE_NOTE_[A-Z0-9_]+_START', html))}")
    audit.append(f"Existing B140 CSS block before patch: {CSS_START in css and CSS_END in css}")

    html = strip_existing_b140_notes(html)
    html = patch_b130_sourcebox_method_link(html, audit)

    for spec in NOTE_SPECS:
        html = insert_note_before_section_end(html, spec, audit)

    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B140 - Unified Source Lines

Date: {today}

## Ziel

B140 vereinheitlicht kompakte Quellen-/Methodikzeilen unter zentralen Karten-, Grafik-
und Erzählblöcken. Damit wird der V2-Standard `Quellzeile + Methode-Link unter jeder Grafik`
schrittweise umgesetzt, ohne Kartenlogik oder Daten anzufassen.

## Umsetzung

- B130b-Quellenbox erhält einen Link auf `Methode in Kürze`
- kompakte Quellen-/Methodikzeilen für:
  - Frame-Mismatch-Bridge
  - globalen Karten-/Kontextblock
  - regionalen Oberschwaben-/Schnittmengenblock
  - Wasser-und-Governance-Block
  - Konsequenz-Kicker
- CSS für ein einheitliches, zurückhaltendes Erscheinungsbild
- keine Änderung an Kartenlogik, Daten, Navigation oder Scorecard-Struktur

## Hinweise

Die Zeilen sind bewusst kurz und verweisen auf den zentralen Methodenanker `#methode-in-kuerze`.
Sie ersetzen nicht den zentralen Quellen- und Rechtenachweis, sondern machen die Herkunft und
Einordnung direkt im Lesefluss sichtbar.

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/140_unified_source_lines.py`
- `docs/B140_unified_source_lines.md`
- `docs/B140_unified_source_lines_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- kompakte Quell-/Methodenzeilen erscheinen unter den relevanten Blöcken
- Methode-Links springen zu `Methode in Kürze`
- Zeilen wirken zurückhaltend und nicht wie zusätzliche Absätze
- keine doppelten B140-Quellzeilen nach erneutem Ausführen
- Karten, Scorecard, Navigation und Quellenblock bleiben unverändert
"""
    write(DOC, doc_text)

    audit_text = "# B140 unified source lines audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B140 unified source lines patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B140_unified_source_lines.md")
    print("  docs/B140_unified_source_lines_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
