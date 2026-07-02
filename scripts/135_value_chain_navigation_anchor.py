from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "135_value_chain_navigation_anchor.py"
DOC = ROOT / "docs" / "B135_value_chain_navigation_anchor.md"
AUDIT = ROOT / "docs" / "B135_value_chain_navigation_anchor_audit.txt"
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
NAV_INSERT_BEFORE = "Prüfpfade"


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


def find_b130_section_start(html: str, audit: list[str]) -> int:
    # Prefer the B130b/B130 section class.
    class_pos = html.find(B130_SECTION_CLASS)
    if class_pos >= 0:
        section_start = html.rfind("<section", 0, class_pos)
        if section_start >= 0:
            audit.append(f"OK found target section by class: {B130_SECTION_CLASS}")
            return section_start

    # Fallback to text anchors.
    for anchor in FALLBACK_ANCHORS:
        pos = html.find(anchor)
        if pos >= 0:
            section_start = html.rfind("<section", 0, pos)
            if section_start >= 0:
                audit.append(f"OK found target section by text anchor: {anchor}")
                return section_start

    audit.append("ERROR target value-chain/B130 section not found")
    return -1


def patch_target_id(html: str, audit: list[str]) -> str:
    # If the target id already exists anywhere, do not add a duplicate.
    if f'id="{TARGET_ID}"' in html:
        audit.append(f"OK target id already present: {TARGET_ID}")
        return html

    section_start = find_b130_section_start(html, audit)
    if section_start < 0:
        return html

    tag_end = html.find(">", section_start)
    if tag_end < 0:
        audit.append("ERROR malformed target section tag")
        return html

    section_tag = html[section_start:tag_end + 1]
    new_tag, status = add_id_to_tag(section_tag, TARGET_ID)

    if status == "added":
        audit.append(f"OK added id to target section: {TARGET_ID}")
        return html[:section_start] + new_tag + html[tag_end + 1:]

    if status == "already":
        audit.append(f"OK target section already has id: {TARGET_ID}")
        return html

    audit.append(f"WARN target section already has another id ({status}); nav will not be inserted to avoid duplicate semantics")
    return html


def patch_navigation(html: str, audit: list[str]) -> str:
    if NAV_LINK in html or NAV_LABEL in html:
        audit.append(f"OK navigation label already present: {NAV_LABEL}")
        return html

    pattern = re.compile(r'(<a\b[^>]*>\s*' + re.escape(NAV_INSERT_BEFORE) + r'\s*</a>)')
    match = pattern.search(html)

    if match:
        insert = NAV_LINK + "\n        " + match.group(1)
        html = html[:match.start()] + insert + html[match.end():]
        audit.append(f"OK inserted nav link before: {NAV_INSERT_BEFORE}")
        return html

    # Fallback: insert before Quellen if Prüfpfade cannot be found.
    fallback_pattern = re.compile(r'(<a\b[^>]*>\s*Quellen\s*</a>)')
    fallback_match = fallback_pattern.search(html)
    if fallback_match:
        insert = NAV_LINK + "\n        " + fallback_match.group(1)
        html = html[:fallback_match.start()] + insert + html[fallback_match.end():]
        audit.append("OK inserted nav link before fallback: Quellen")
        return html

    audit.append("ERROR no suitable navigation insertion point found")
    return html


def update_done(done_text: str) -> str:
    line = f"- B135 value-chain navigation anchor: added a navigation target for the value-chain/Engpass section ({date.today().isoformat()})."
    if "B135 value-chain navigation anchor" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)

    b134_still_present = "b134-value-chain-table" in html or "B134_RESPONSIVE_VALUE_CHAIN_MATRIX_START" in html
    audit.append(f"B134 responsive matrix markers still present before B135: {b134_still_present}")

    html = patch_target_id(html, audit)
    html = patch_navigation(html, audit)

    write(INDEX, html)

    today = date.today().isoformat()

    doc_text = f"""# B135 - Value-Chain Navigation Anchor

Date: {today}

## Ziel

B135 macht die neue V2-Kernaussage zur Wertschöpfungskette navigierbar.
Die Engpass-/Scorecard-Section erhält einen stabilen Anker und die Hauptnavigation
einen Eintrag `Wertschöpfung`.

## Fachlicher Grund

Die V2-Erzählung verschiebt den Schwerpunkt von reiner Moor- und Nutzungskartierung
hin zur Frage, ob Verarbeitung, Abnahme, Standards und Mengen als Kette funktionieren.
Diese Stelle sollte daher direkt erreichbar sein.

## Umsetzung

- Zielanker `#{TARGET_ID}` an der B130/B130b-Wertschöpfungs-Scorecard
- neuer Navigationslink `{NAV_LABEL}`
- Einfügung vor `Prüfpfade`, falls möglich
- keine Änderung an Kartenlogik, Daten, Scorecard-Inhalt oder Matrix

## Hinweis zu B134

Der Audit vermerkt, ob noch B134-Marker im Arbeitsbaum sichtbar sind.
B134 sollte vor einem Commit verworfen sein, falls der mobile Matrix-Test nicht übernommen werden soll.

## Geänderte Dateien

- `index.html`
- `scripts/135_value_chain_navigation_anchor.py`
- `docs/B135_value_chain_navigation_anchor.md`
- `docs/B135_value_chain_navigation_anchor_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Navigation enthält `Wertschöpfung`.
- Klick auf `Wertschöpfung` springt zur Scorecard/Engpass-Section.
- Navigation bricht auf Desktop nicht unschön.
- B134 ist nicht versehentlich im Commit enthalten.
"""
    write(DOC, doc_text)

    audit_text = "# B135 value-chain navigation anchor audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B135 value-chain navigation anchor patch complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B135_value_chain_navigation_anchor.md")
    print("  docs/B135_value_chain_navigation_anchor_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
