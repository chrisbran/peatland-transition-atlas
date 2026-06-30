from pathlib import Path
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "132_statement_titles.py"
DOC = ROOT / "docs" / "B132_statement_titles.md"
AUDIT = ROOT / "docs" / "B132_statement_titles_audit.txt"
DONE = ROOT / "tasks" / "done.md"

# B132 focuses only on title/caption microcopy.
# It deliberately avoids changing map state attributes, JS, images or data references.
REPLACEMENTS = [
    (
        "Warum Wasserstand entscheidend ist",
        "Der Wasserstand entscheidet, ob Moorboden speichert oder emittiert",
    ),
    (
        "Moorbodenkontext braucht konkrete Planung",
        "Moorbodenschutz wird erst mit Boden, Nutzung und Wasserstand planbar",
    ),
    (
        "Globale Moorverbreitung",
        "Moore sind räumlich konzentriert und klimatisch wirksam",
    ),
    (
        "Warum die Karte beim Wasser beginnt",
        "Der Wasserstand macht aus Moorboden Speicher oder Quelle",
    ),
    (
        "Oberschwaben als Ausgangspunkt",
        "In Oberschwaben wird Moorbodenschutz zur konkreten Nutzungsfrage",
    ),
    (
        "Nicht jede Fläche braucht dieselbe Lösung",
        "Unterschiedliche Flächen brauchen unterschiedliche Transformationspfade",
    ),
    (
        "Was die Karten nicht leisten",
        "Die Karten zeigen Prüfbedarf, aber keine Flächeneignung",
    ),
    (
        "Was die Schnittmenge in Oberschwaben zeigt",
        "Die Schnittmenge macht den Prüfbedarf sichtbar, nicht die Lösung",
    ),
    (
        "Was aus der Schnittmenge folgt",
        "Aus der Schnittmenge folgt Verhandlung, keine Einheitslösung",
    ),
    (
        "Welche Prüfpfade folgen aus unterschiedlichen Nutzungskontexten?",
        "Nutzungskontexte entscheiden, welche Wertschöpfungspfade plausibel sind",
    ),
    (
        "Die eigentliche Engstelle liegt selten im Anbau allein",
        "Die Engstelle liegt häufig bei Menge, Verarbeitung und Abnahme",
    ),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B132 statement titles: converted selected section and graphic headings from topic labels to claim-based titles ({date.today().isoformat()})."
    if "B132 statement titles" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    audit = []
    changed = 0

    for old, new in REPLACEMENTS:
        old_count = html.count(old)
        new_count_before = html.count(new)

        if old_count:
            html = html.replace(old, new)
            changed += old_count
            audit.append(f"OK replaced {old_count}x: {old} -> {new}")
        elif new_count_before:
            audit.append(f"OK already replaced: {new}")
        else:
            audit.append(f"MISS not found: {old}")

    write(INDEX, html)

    today = date.today().isoformat()

    doc_text = f"""# B132 - Statement Titles

Date: {today}

## Ziel

B132 setzt den V2-Designstandard `Aussagesätze als Grafik-Titel` um.
Ausgewählte Abschnitts- und Grafiküberschriften werden von neutralen Themenlabels zu
fachlich vorsichtigen Befund- oder Aussagesätzen umformuliert.

## Leitprinzip

Der Titel benennt die Aussage, die der folgende Abschnitt oder die Grafik plausibilisiert.
Die Formulierungen bleiben demonstrator-gerecht und vermeiden harte Entscheidungs- oder
Eignungsaussagen.

## Umsetzung

Geändert wurden nur sichtbare Titel/Microcopy in `index.html`.

Nicht geändert wurden:

- Kartenlogik
- JavaScript
- Bildquellen
- Daten
- zentrale Quellen- und Rechtetabelle
- B130b-Scorecard-Struktur

## Geänderte Dateien

- `index.html`
- `scripts/132_statement_titles.py`
- `docs/B132_statement_titles.md`
- `docs/B132_statement_titles_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hero bleibt unverändert.
- Überschriften wirken aussagekräftiger, aber nicht reißerisch.
- Keine Überschrift bricht unschön auf Desktop oder mobil.
- Karten- und Scrolly-Funktion bleiben unverändert.
"""
    write(DOC, doc_text)

    audit_text = "# B132 statement titles audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += f"Total replacements applied: {changed}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B132 statement titles patch complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B132_statement_titles.md")
    print("  docs/B132_statement_titles_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
