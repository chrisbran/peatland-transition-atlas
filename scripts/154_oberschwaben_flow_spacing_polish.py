from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "154_oberschwaben_flow_spacing_polish.py"
DOC = ROOT / "docs" / "B154_oberschwaben_flow_spacing_polish.md"
AUDIT = ROOT / "docs" / "B154_oberschwaben_flow_spacing_polish_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B149_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
B149_END = "<!-- /B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_END -->"

HTML_START = "<!-- B154_OBERSCHWABEN_FLOW_TRANSITION_START -->"
HTML_END = "<!-- /B154_OBERSCHWABEN_FLOW_TRANSITION_END -->"

CSS_START = "/* B154_OBERSCHWABEN_FLOW_SPACING_POLISH_START */"
CSS_END = "/* B154_OBERSCHWABEN_FLOW_SPACING_POLISH_END */"

BILANZ_ANCHORS = [
    "Die Schnittmenge macht den Prüfbedarf sichtbar, nicht die Lösung",
    "Flächenbilanz",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def find_block_bounds(text: str, start: str, end: str) -> tuple[int, int] | None:
    m = re.search(re.escape(start) + r".*?" + re.escape(end), text, re.S)
    if not m:
        return None
    return m.start(), m.end()


def find_bilanz_section_start(html: str, audit: list[str]) -> int | None:
    for anchor in BILANZ_ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue
        section_start = html.rfind("<section", 0, pos)
        if section_start >= 0:
            audit.append(f"OK found Flächenbilanz section by anchor: {anchor}")
            return section_start
        audit.append(f"WARN anchor found but no section start before it: {anchor}")
    audit.append("WARN Flächenbilanz section not found")
    return None


def build_transition() -> str:
    return f"""{HTML_START}
<div class="b154-oberschwaben-flow-transition" role="note" aria-label="Übergang von interaktiver Karte zur Flächenbilanz">
  <p>
    Nach der räumlichen Vertiefung folgt die Bilanz: Wie groß ist diese Schnittmenge
    und welche heutige Nutzung dominiert sie?
  </p>
</div>
{HTML_END}"""


def insert_transition(html: str, audit: list[str]) -> str:
    html = strip_block(html, HTML_START, HTML_END)

    b149_bounds = find_block_bounds(html, B149_START, B149_END)
    if not b149_bounds:
        audit.append("ERROR B149/B152 Felt block not found; transition not inserted")
        return html

    _, b149_end = b149_bounds
    bilanz_start = find_bilanz_section_start(html, audit)

    if bilanz_start is not None and b149_end <= bilanz_start:
        audit.append("OK inserted B154 transition between Felt block and Flächenbilanz")
        return html[:b149_end] + "\n\n" + build_transition() + "\n" + html[b149_end:]

    audit.append("WARN Flächenbilanz position not after Felt block; inserted transition directly after Felt block")
    return html[:b149_end] + "\n\n" + build_transition() + "\n" + html[b149_end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b152-felt-integration {{
  padding-bottom: clamp(1.6rem, 4vw, 3rem);
}}

.b154-oberschwaben-flow-transition {{
  width: min(100% - 2rem, 74rem);
  max-width: 68rem;
  margin: clamp(-0.4rem, -0.6vw, 0rem) auto clamp(0.8rem, 2.3vw, 1.5rem);
  padding: 0.72rem 0.95rem;
  border-left: 3px solid rgba(8, 127, 122, 0.58);
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.48);
}}

.b154-oberschwaben-flow-transition p {{
  max-width: 48rem;
  margin: 0;
  color: var(--muted, #637266);
  font-size: 0.92rem;
  line-height: 1.5;
}}

.b154-oberschwaben-flow-transition + section {{
  padding-top: clamp(1.5rem, 3.4vw, 2.7rem);
}}

@media (max-width: 760px) {{
  .b154-oberschwaben-flow-transition {{
    width: min(100% - 1.25rem, 74rem);
    margin-block: 0 1rem;
    padding: 0.68rem 0.82rem;
  }}

  .b154-oberschwaben-flow-transition p {{
    font-size: 0.86rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B154 Oberschwaben flow spacing polish: added a quiet transition and spacing polish between static map, Felt deepening and area balance ({date.today().isoformat()})."
    if "B154 Oberschwaben flow spacing polish" in done_text:
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

    audit.append(f"B149/B152 Felt block present before patch: {B149_START in html and B149_END in html}")
    audit.append(f"Old B154 transition present before patch: {HTML_START in html and HTML_END in html}")
    audit.append(f"Old B154 CSS present before patch: {CSS_START in css and CSS_END in css}")

    html = insert_transition(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B154 - Oberschwaben Flow Spacing Polish

Date: {today}

## Ziel

B154 glättet den Übergang zwischen drei inzwischen wichtigen Oberschwaben-Bausteinen:

1. statische Oberschwaben-Storykarte
2. interaktive Felt-Vertiefung
3. Flächenbilanz der Schnittmenge

Der Patch soll die Felt-Karte nicht wie eine Dopplung wirken lassen, sondern sie als
Vertiefung zwischen räumlicher Einordnung und quantitativer Bilanz lesbar machen.

## Umsetzung

- kleiner Übergangstext nach dem Felt-Block:
  - `Nach der räumlichen Vertiefung folgt die Bilanz...`
- sanftere vertikale Abstände zwischen Felt-Block und Flächenbilanz
- keine Änderung am Felt-iframe
- keine Änderung an Kartenlogik, Daten oder Quellen
- bestehende Oberschwaben-Karte bleibt erhalten

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/154_oberschwaben_flow_spacing_polish.py`
- `docs/B154_oberschwaben_flow_spacing_polish.md`
- `docs/B154_oberschwaben_flow_spacing_polish_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Übergang zwischen Felt-Karte und Flächenbilanz ist ruhiger.
- Felt-Block wirkt als Vertiefung, nicht als Dopplung.
- Flächenbilanz folgt logisch auf die interaktive Karte.
- Desktop iframe lädt weiterhin.
- Mobile Fallback bleibt unverändert.
"""
    write(DOC, doc_text)

    audit_text = "# B154 Oberschwaben flow spacing polish audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B154 Oberschwaben flow spacing polish complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B154_oberschwaben_flow_spacing_polish.md")
    print("  docs/B154_oberschwaben_flow_spacing_polish_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
