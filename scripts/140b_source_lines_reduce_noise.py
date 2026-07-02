from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "140b_source_lines_reduce_noise.py"
DOC = ROOT / "docs" / "B140b_source_lines_reduce_noise.md"
AUDIT = ROOT / "docs" / "B140b_source_lines_reduce_noise_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CSS_START = "/* B140_UNIFIED_SOURCE_LINES_START */"
CSS_END = "/* B140_UNIFIED_SOURCE_LINES_END */"

REMOVE_KEYS = [
    "FRAME_BRIDGE",
    "WATER_GOVERNANCE",
    "CONSEQUENCE_KICKER",
]

KEEP_KEYS = [
    "GLOBAL_CONTEXT",
    "REGIONAL_CONTEXT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_keyed_note(html: str, key: str) -> tuple[str, int]:
    pattern = re.compile(
        r"<!-- B140_SOURCE_NOTE_" + re.escape(key) + r"_START -->.*?<!-- /B140_SOURCE_NOTE_" + re.escape(key) + r"_END -->\s*",
        re.S,
    )
    html_new, count = pattern.subn("", html)
    return html_new, count


def strip_css_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def patch_css(css: str) -> str:
    css = strip_css_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b140-source-line {{
  width: min(100%, 54rem);
  margin: 0.7rem auto 0;
  color: var(--muted, #637266);
  font-size: 0.82rem;
  line-height: 1.42;
  opacity: 0.82;
}}

.b140-source-line::before {{
  content: "Quelle/Methode: ";
  font-weight: 700;
}}

.b140-source-line a,
.b130-source-box a {{
  color: inherit;
  font-weight: 700;
  text-underline-offset: 0.16em;
  text-decoration-thickness: 0.08em;
}}

.b130-source-box a {{
  color: rgba(246, 242, 232, 0.9);
}}

@media (max-width: 720px) {{
  .b140-source-line {{
    width: min(100% - 1.25rem, 54rem);
    margin-top: 0.55rem;
    font-size: 0.78rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B140b source lines reduce noise: removed source lines from editorial narrative blocks and softened remaining map source lines ({date.today().isoformat()})."
    if "B140b source lines reduce noise" in done_text:
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

    before_blocks = len(re.findall(r"B140_SOURCE_NOTE_[A-Z0-9_]+_START", html))
    audit.append(f"B140 note blocks before patch: {before_blocks}")

    for key in REMOVE_KEYS:
        html, count = strip_keyed_note(html, key)
        audit.append(f"Removed {key}: {count}")

    for key in KEEP_KEYS:
        present = f"B140_SOURCE_NOTE_{key}_START" in html
        audit.append(f"Kept {key} present after removal step: {present}")

    css = patch_css(css)
    audit.append("OK replaced B140 CSS with quieter, centered source-line styling")

    after_blocks = len(re.findall(r"B140_SOURCE_NOTE_[A-Z0-9_]+_START", html))
    audit.append(f"B140 note blocks after patch: {after_blocks}")

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B140b - Reduce Source-Line Noise

Date: {today}

## Anlass

B140 setzte das richtige Prinzip um, erzeugte im Seitenfluss aber zu viele sichtbare Quellenzeilen.
Vor allem unter rein redaktionellen Blöcken wirkte das in der Gesamtansicht unruhig.

## Entscheidung

Quellen-/Methodenzeilen sollen dort sichtbar bleiben, wo Daten, Karten oder konkrete
Auswertungslogik gezeigt werden. Rein redaktionelle Brücken und Schlussfolgerungen müssen
nicht jeweils eine eigene Zeile erhalten, solange sie über Methode und zentralen Quellenblock
abgedeckt sind.

## Umsetzung

Entfernt wurden B140-Zeilen unter:

- Frame-Mismatch-Bridge
- Wasser-und-Governance-Block
- Konsequenz-Kicker

Beibehalten wurden B140-Zeilen unter:

- globalem Karten-/Kontextblock
- regionalem Oberschwaben-/Schnittmengenblock

Außerdem wurde die Darstellung der verbleibenden Quellenzeilen abgeschwächt:

- kleiner
- zentriert
- weniger dominant
- explizites Präfix `Quelle/Methode:`

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/140b_source_lines_reduce_noise.py`
- `docs/B140b_source_lines_reduce_noise.md`
- `docs/B140b_source_lines_reduce_noise_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- weniger Quellenzeilen im Seitenfluss
- verbleibende Zeilen stehen nur unter daten-/kartenbezogenen Blöcken
- B130b-Quellenbox bleibt erhalten
- `Methode in Kürze`-Links funktionieren
- keine Karten-/JS-/Datenänderung
"""
    write(DOC, doc_text)

    audit_text = "# B140b source lines reduce noise audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B140b source lines reduce noise patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B140b_source_lines_reduce_noise.md")
    print("  docs/B140b_source_lines_reduce_noise_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
