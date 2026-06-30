from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "135b_fix_value_chain_nav_link.py"
DOC = ROOT / "docs" / "B135b_fix_value_chain_nav_link.md"
AUDIT = ROOT / "docs" / "B135b_fix_value_chain_nav_link_audit.txt"
DONE = ROOT / "tasks" / "done.md"

TARGET_ID = "wertschoepfung"
NAV_LABEL = "Wertschöpfung"
NAV_LINK = f'<a href="#{TARGET_ID}">{NAV_LABEL}</a>'

B130_SECTION_CLASS = "b130-engpass-climax"
FALLBACK_ANCHORS = [
    "Bis zur Ernte ist die Kette oft anschlussfähig",
    "Nutzung und Wertschöpfung",
    "Die Engstelle liegt häufig bei Menge, Verarbeitung und Abnahme",
]
INSERT_BEFORE_LABELS = ["Prüfpfade", "Quellen"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def add_id_to_tag(tag: str, target_id: str) -> tuple[str, str]:
    id_match = re.search(r'\bid\s*=\s*"([^"]*)"', tag)
    if id_match:
        if id_match.group(1) == target_id:
            return tag, "already"
        return tag, f"existing-id:{id_match.group(1)}"
    return tag[:-1] + f' id="{target_id}">', "added"


def ensure_target_id(html: str, audit: list[str]) -> str:
    if f'id="{TARGET_ID}"' in html:
        audit.append(f"OK target id already present: {TARGET_ID}")
        return html

    class_pos = html.find(B130_SECTION_CLASS)
    section_start = -1

    if class_pos >= 0:
        section_start = html.rfind("<section", 0, class_pos)
        audit.append(f"OK target section found by class: {B130_SECTION_CLASS}")

    if section_start < 0:
        for anchor in FALLBACK_ANCHORS:
            pos = html.find(anchor)
            if pos >= 0:
                section_start = html.rfind("<section", 0, pos)
                audit.append(f"OK target section found by text anchor: {anchor}")
                break

    if section_start < 0:
        audit.append("ERROR target section not found; id not added")
        return html

    tag_end = html.find(">", section_start)
    if tag_end < 0:
        audit.append("ERROR target section tag malformed")
        return html

    tag = html[section_start:tag_end + 1]
    new_tag, status = add_id_to_tag(tag, TARGET_ID)

    if status == "added":
        audit.append(f"OK added target id: {TARGET_ID}")
        return html[:section_start] + new_tag + html[tag_end + 1:]

    audit.append(f"WARN target section already has another id ({status}); id not added")
    return html


def patch_nav(html: str, audit: list[str]) -> str:
    # Important: check only the navigation markup, not the whole document.
    nav_match = re.search(r"<nav\b[^>]*>.*?</nav>", html, flags=re.S)
    if not nav_match:
        audit.append("ERROR no <nav> block found")
        return html

    nav = nav_match.group(0)

    if f'href="#{TARGET_ID}"' in nav:
        audit.append(f"OK nav link already present: #{TARGET_ID}")
        return html

    insert_match = None
    insert_label = None

    for label in INSERT_BEFORE_LABELS:
        pattern = re.compile(r'(<a\b[^>]*>\s*' + re.escape(label) + r'\s*</a>)')
        m = pattern.search(nav)
        if m:
            insert_match = m
            insert_label = label
            break

    if not insert_match:
        audit.append("ERROR no suitable nav insertion point found")
        return html

    replacement = NAV_LINK + "\n        " + insert_match.group(1)
    new_nav = nav[:insert_match.start()] + replacement + nav[insert_match.end():]
    new_html = html[:nav_match.start()] + new_nav + html[nav_match.end():]

    audit.append(f"OK inserted nav link '{NAV_LABEL}' before '{insert_label}' inside <nav>")
    return new_html


def update_done(done_text: str) -> str:
    line = f"- B135b fix value-chain nav link: inserted the missing Wertschöpfung navigation link using nav-only detection ({date.today().isoformat()})."
    if "B135b fix value-chain nav link" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)

    audit.append(f"Whole-document occurrences of '{NAV_LABEL}' before patch: {html.count(NAV_LABEL)}")
    audit.append(f"Nav href '#{TARGET_ID}' present before patch: {bool(re.search(r'<nav\\b[^>]*>.*?href=\"#' + re.escape(TARGET_ID) + r'\".*?</nav>', html, flags=re.S))}")

    html = ensure_target_id(html, audit)
    html = patch_nav(html, audit)

    write(INDEX, html)

    today = date.today().isoformat()

    doc_text = f"""# B135b - Fix Value-Chain Navigation Link

Date: {today}

## Anlass

B135 konnte den Zielanker setzen, hat den Navigationslink aber nicht sichtbar ergänzt.
Ursache: Die Prüfung auf `{NAV_LABEL}` war zu breit und konnte Treffer im Seiteninhalt
statt nur in der Navigation als vorhandenen Link interpretieren.

## Umsetzung

- prüft nur den tatsächlichen `<nav>`-Block
- ergänzt `{NAV_LABEL}` als Link zu `#{TARGET_ID}`
- Einfügung vor `Prüfpfade`, Fallback vor `Quellen`
- stellt sicher, dass der Zielanker `#{TARGET_ID}` vorhanden ist
- keine Änderung an Scorecard-Inhalt, Kartenlogik, Daten oder CSS

## Geänderte Dateien

- `index.html`
- `scripts/135b_fix_value_chain_nav_link.py`
- `docs/B135b_fix_value_chain_nav_link.md`
- `docs/B135b_fix_value_chain_nav_link_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hauptnavigation enthält `Wertschöpfung`.
- Klick auf `Wertschöpfung` springt zur Scorecard/Engpass-Section.
- Navigation bricht auf Desktop nicht unschön.
"""
    write(DOC, doc_text)

    audit_text = "# B135b fix value-chain nav link audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B135b fix value-chain nav link patch complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B135b_fix_value_chain_nav_link.md")
    print("  docs/B135b_fix_value_chain_nav_link_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
