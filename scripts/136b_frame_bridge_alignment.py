from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
CSS = ROOT / "src" / "styles.css"
SCRIPT = ROOT / "scripts" / "136b_frame_bridge_alignment.py"
DOC = ROOT / "docs" / "B136b_frame_bridge_alignment.md"
AUDIT = ROOT / "docs" / "B136b_frame_bridge_alignment_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CSS_START = "/* B136_FRAME_MISMATCH_BRIDGE_START */"
CSS_END = "/* B136_FRAME_MISMATCH_BRIDGE_END */"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def patch_css(css: str, audit: list[str]) -> str:
    old_present = CSS_START in css and CSS_END in css
    audit.append(f"Existing B136 CSS block present before patch: {old_present}")

    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
.b136-frame-bridge {{
  padding-block: clamp(1.75rem, 4vw, 3rem);
}}

.b136-frame-bridge .section-inner {{
  width: min(100% - 2rem, 74rem);
  margin-inline: auto;
}}

.b136-frame-bridge__inner {{
  width: min(100%, 66rem);
  margin-inline: auto;
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
  .b136-frame-bridge .section-inner {{
    width: min(100% - 1.25rem, 74rem);
  }}

  .b136-frame-bridge h2 {{
    max-width: none;
  }}

  .b136-frame-bridge__steps {{
    grid-template-columns: 1fr;
  }}
}}
{CSS_END}
"""
    audit.append("OK replaced B136 CSS with centered section-inner and centered inner wrapper")
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str) -> str:
    line = f"- B136b frame bridge alignment: centered the frame-mismatch bridge and added safe horizontal gutters ({date.today().isoformat()})."
    if "B136b frame bridge alignment" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    css = read(CSS)
    css = patch_css(css, audit)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f"""# B136b - Frame Bridge Alignment

Date: {today}

## Anlass

Die B136-Frame-Mismatch-Bridge stand im lokalen Screenshot zu dicht am linken Rand.
Ursache ist wahrscheinlich, dass der neue Bridge-Block zwar eine innere Maximalbreite hatte,
aber nicht ausreichend gegen den Viewport zentriert und gepolstert wurde.

## Umsetzung

- B136-CSS-Block ersetzt
- `.b136-frame-bridge .section-inner` erhält explizite Breite, horizontale Gutters und Zentrierung
- `.b136-frame-bridge__inner` wird ebenfalls zentriert
- keine Änderung an HTML, Text, Navigation, Kartenlogik oder Daten

## Geänderte Dateien

- `src/styles.css`
- `scripts/136b_frame_bridge_alignment.py`
- `docs/B136b_frame_bridge_alignment.md`
- `docs/B136b_frame_bridge_alignment_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Bridge steht nicht mehr am linken Rand.
- Bridge ist horizontal ähnlich eingebunden wie die übrigen Content-Blöcke.
- Desktop und mobile Ansicht behalten ausreichende Seitenabstände.
- Die drei Karten bleiben sauber nebeneinander bzw. mobil gestapelt.
"""
    write(DOC, doc_text)

    audit_text = "# B136b frame bridge alignment audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B136b frame bridge alignment patch complete.")
    print("Changed: src/styles.css")
    print("Created/updated:")
    print("  docs/B136b_frame_bridge_alignment.md")
    print("  docs/B136b_frame_bridge_alignment_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
