from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "136_frame_mismatch_bridge.py"
DOC = ROOT / "docs" / "B136_frame_mismatch_bridge.md"
AUDIT = ROOT / "docs" / "B136_frame_mismatch_bridge_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B136_FRAME_MISMATCH_BRIDGE_START -->"
HTML_END = "<!-- /B136_FRAME_MISMATCH_BRIDGE_END -->"
CSS_START = "/* B136_FRAME_MISMATCH_BRIDGE_START */"
CSS_END = "/* B136_FRAME_MISMATCH_BRIDGE_END */"

ANCHORS = [
    "Moorbodenschutz verändert sich beim Zoomen",
    "Moorschutz verändert sich beim Zoomen",
    "Globale Moorverbreitung",
    "Moore sind räumlich konzentriert und klimatisch wirksam",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def build_bridge_html() -> str:
    return f"""{HTML_START}
<section class="b136-frame-bridge" aria-labelledby="b136-frame-bridge-title">
  <div class="section-inner">
    <div class="b136-frame-bridge__inner">
      <p class="eyebrow">Frame-Mismatch</p>
      <h2 id="b136-frame-bridge-title">Moorbodenschutz beginnt als Klimathema – und wird vor Ort zur Nutzungsfrage</h2>
      <p class="b136-frame-bridge__lead">
        Globale Karten erklären, warum Moore relevant sind. Die Umsetzung entscheidet sich aber
        dort, wo Wasserstand, Nutzung, Eigentum, Betriebe und Wertschöpfungsketten zusammenkommen.
      </p>

      <div class="b136-frame-bridge__steps" aria-label="Vom Klimaframe zur Umsetzungsebene">
        <article>
          <span>01</span>
          <h3>Klima macht Relevanz sichtbar</h3>
          <p>Speicher, Emissionen und internationale Zielgrößen begründen den Handlungsdruck.</p>
        </article>
        <article>
          <span>02</span>
          <h3>Raum macht Planung notwendig</h3>
          <p>Karten zeigen, dass Moorbodenschutz nicht überall gleich aussieht.</p>
        </article>
        <article>
          <span>03</span>
          <h3>Umsetzung braucht lokale Ketten</h3>
          <p>Wasser, Bewirtschaftung, Verarbeitung und Abnahme müssen zusammenpassen.</p>
        </article>
      </div>
    </div>
  </div>
</section>
{HTML_END}"""


def insert_before_section_with_anchor(html: str, block: str, audit: list[str]) -> str:
    for anchor in ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        section_start = html.rfind("<section", 0, pos)
        if section_start < 0:
            audit.append(f"WARN anchor found but no section before it: {anchor}")
            continue

        audit.append(f"OK inserted B136 frame bridge before section containing anchor: {anchor}")
        return html[:section_start] + block + "\n\n" + html[section_start:]

    audit.append("ERROR no B136 insertion anchor found")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
.b136-frame-bridge {{
  padding-block: clamp(1.75rem, 4vw, 3rem);
}}

.b136-frame-bridge__inner {{
  max-width: 66rem;
  border-top: 1px solid rgba(26, 48, 38, 0.14);
  border-bottom: 1px solid rgba(26, 48, 38, 0.10);
  padding-block: clamp(1.25rem, 3vw, 2rem);
}}

.b136-frame-bridge h2 {{
  max-width: 18ch;
  margin-bottom: 0.65rem;
}}

.b136-frame-bridge__lead {{
  max-width: 45rem;
  color: var(--muted, #637266);
  font-size: clamp(1rem, 1.7vw, 1.15rem);
  line-height: 1.55;
}}

.b136-frame-bridge__steps {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 1.25rem;
}}

.b136-frame-bridge__steps article {{
  border-radius: 1rem;
  border: 1px solid rgba(26, 48, 38, 0.12);
  background: rgba(255, 255, 255, 0.46);
  padding: 0.95rem;
}}

.b136-frame-bridge__steps span {{
  display: inline-block;
  margin-bottom: 0.55rem;
  color: #6f8c42;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}}

.b136-frame-bridge__steps h3 {{
  margin: 0 0 0.35rem;
  font-size: 1.02rem;
  line-height: 1.25;
}}

.b136-frame-bridge__steps p {{
  margin: 0;
  color: var(--muted, #637266);
  font-size: 0.94rem;
  line-height: 1.48;
}}

@media (max-width: 820px) {{
  .b136-frame-bridge h2 {{
    max-width: none;
  }}

  .b136-frame-bridge__steps {{
    grid-template-columns: 1fr;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B136 frame mismatch bridge: added a compact narrative bridge from climate framing to local implementation ({date.today().isoformat()})."
    if "B136 frame mismatch bridge" in done_text:
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
    audit.append(f"Old B136 HTML block present before patch: {old_html_present}")
    audit.append(f"Old B136 CSS block present before patch: {old_css_present}")

    html = strip_block(html, HTML_START, HTML_END)
    css = strip_block(css, CSS_START, CSS_END)

    html = insert_before_section_with_anchor(html, build_bridge_html(), audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B136 - Frame Mismatch Bridge

Date: {today}

## Ziel

B136 verankert den zentralen V2-Erzählrahmen sichtbar:
Moorbodenschutz beginnt im Klimaframe, wird in der Umsetzung aber zur lokalen Frage von
Nutzung, Wasser, Eigentum, Betrieben und Wertschöpfung.

## Umsetzung

- neue kompakte Bridge-Section vor dem ersten Zoom-/Kartenblock
- drei Schritte: Klima, Raum, Umsetzung
- bewusst zurückhaltende Gestaltung mit Linien und kleinen Karten
- keine Änderung an Kartenlogik, Daten, Quellenblock oder Navigation

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/136_frame_mismatch_bridge.py`
- `docs/B136_frame_mismatch_bridge.md`
- `docs/B136_frame_mismatch_bridge_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Bridge steht vor dem ersten Zoom-/Kartenblock.
- Sie unterstützt die Story, ohne den Hero zu verdrängen.
- Drei Schritte sind auf Desktop nebeneinander und mobil gestapelt.
- Navigation und Scorecard bleiben unverändert.
"""
    write(DOC, doc_text)

    audit_text = "# B136 frame mismatch bridge audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B136 frame mismatch bridge patch complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B136_frame_mismatch_bridge.md")
    print("  docs/B136_frame_mismatch_bridge_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
