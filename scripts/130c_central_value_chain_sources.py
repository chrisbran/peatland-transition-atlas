from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "130c_central_value_chain_sources.py"
DOC = ROOT / "docs" / "B130c_central_value_chain_sources.md"
AUDIT = ROOT / "docs" / "B130c_central_value_chain_sources_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B130C_VALUE_CHAIN_SOURCES_START -->"
HTML_END = "<!-- /B130C_VALUE_CHAIN_SOURCES_END -->"
INSERT_BEFORE_ANCHOR = "Eigene Auswertungen und Kartenexporte"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def build_source_rows() -> str:
    return f'''{HTML_START}
                <tr>
                  <td>IPCC Wetlands Supplement</td>
                  <td>Öffentlich bereitgestellter IPCC-Bericht; Quellenhinweis nach IPCC-Zitation; keine Weiterlizenzierung der Inhalte.</td>
                  <td>IPCC (2014): <em>2013 Supplement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories: Wetlands</em>, insbesondere Kapitel 2 zu drainierten organischen Böden und Kapitel 3 zu wiedervernässten organischen Böden.</td>
                </tr>
                <tr>
                  <td>VIP – Vorpommern Initiative Paludikultur</td>
                  <td>Öffentlich zugänglicher Projektbericht; Originalbedingungen und Urheberrechte der Herausgeber beachten.</td>
                  <td>Universität Greifswald / VIP: <em>Endbericht Vorpommern Initiative Paludikultur</em>; fachliche Grundlage für Aussagen zu Wertschöpfungsketten, Nachfrage, Absatzmöglichkeiten, Produktentwicklung und Zertifizierung.</td>
                </tr>
                <tr>
                  <td>Brandenburgs Moore klimafreundlich bewirtschaften</td>
                  <td>Öffentlich bereitgestellter Ratgeber; Originalbedingungen des Herausgebers beachten.</td>
                  <td>Ministerium für Landwirtschaft, Umwelt und Klimaschutz Brandenburg: <em>Brandenburgs Moore klimafreundlich bewirtschaften. Ein Ratgeber für Anwender und Interessierte</em>; fachliche Grundlage für Verwertungsoptionen, Pilotmaßstab, Marktbezug und Entwicklungsbedarf von Verwertungsketten.</td>
                </tr>
{HTML_END}'''


def insert_rows_before_anchor_row(html: str, audit: list[str]) -> str:
    pos = html.find(INSERT_BEFORE_ANCHOR)
    if pos < 0:
        audit.append(f"ERROR insertion anchor not found: {INSERT_BEFORE_ANCHOR}")
        return html

    tr_start = html.rfind("<tr", 0, pos)
    if tr_start < 0:
        audit.append(f"ERROR no preceding <tr> found for anchor: {INSERT_BEFORE_ANCHOR}")
        return html

    rows = build_source_rows()
    audit.append(f"OK inserted value-chain source rows before table row: {INSERT_BEFORE_ANCHOR}")
    return html[:tr_start] + rows + "\n" + html[tr_start:]


def update_done(done_text: str) -> str:
    line = f"- B130c central value-chain sources: added IPCC, VIP and Brandenburg value-chain references to the central source table ({date.today().isoformat()})."
    if "B130c central value-chain sources" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    old_block_present = HTML_START in html and HTML_END in html
    audit.append(f"Old B130c source block present before patch: {old_block_present}")

    html = strip_block(html, HTML_START, HTML_END)
    html = insert_rows_before_anchor_row(html, audit)

    write(INDEX, html)

    today = date.today().isoformat()

    doc_text = f"""# B130c - Central Value-Chain Sources

Date: {today}

## Ziel

B130c nimmt die fachlichen Quellen zur B130b-Scorecard in den zentralen Quellennachweis am Seitenende auf.

## Umsetzung

In der Tabelle `Datengrundlagen, Rechte und Quellenvermerke` wurden vor `Eigene Auswertungen und Kartenexporte` drei fachliche Quellen ergänzt:

- IPCC Wetlands Supplement
- VIP – Vorpommern Initiative Paludikultur
- Brandenburgs Moore klimafreundlich bewirtschaften

Die Einträge stützen die Engpass-/Wertschöpfungsketten-Grafik als qualitative, schematische Synthese.
Sie machen keine quantitativen Präzisionsangaben und ersetzen keine formale Bewertung einzelner Produkte oder Regionen.

## Geänderte Dateien

- `index.html`
- `scripts/130c_central_value_chain_sources.py`
- `docs/B130c_central_value_chain_sources.md`
- `docs/B130c_central_value_chain_sources_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Quellenblock am Seitenende enthält die drei neuen Einträge.
- B130b-Scorecard bleibt unverändert.
- Bestehende Datengrundlagen bleiben erhalten.
"""
    write(DOC, doc_text)

    audit_text = "# B130c central value-chain sources audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B130c central value-chain sources patch complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B130c_central_value_chain_sources.md")
    print("  docs/B130c_central_value_chain_sources_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
