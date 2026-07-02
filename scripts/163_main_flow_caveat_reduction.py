from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"

SCRIPT = ROOT / "scripts" / "163_main_flow_caveat_reduction.py"
DOC = ROOT / "docs" / "B163_main_flow_caveat_reduction.md"
CSV_OUT = ROOT / "docs" / "B163_main_flow_caveat_replacements.csv"
AUDIT = ROOT / "docs" / "B163_main_flow_caveat_reduction_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CAVEAT_TERMS = [
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine hydrologische Modellierung",
    "keine betriebliche Betroffenheitsanalyse",
    "keine Flächeneignung",
    "keine Standortempfehlung",
    "Prüfbedarf",
    "Orientierung",
    "Hinweis",
]

REPLACEMENTS = [
    {
        "id": "oberschwaben_step_label",
        "pattern": r"5\s*/\s*Grenze\s+der\s+Aussage",
        "replacement": "5 / Einordnung",
        "reason": "turns a warning label into a quieter map-reading label",
    },
    {
        "id": "oberschwaben_step_title",
        "pattern": r"Einordnung,\s*nicht\s+Priorisierung",
        "replacement": "Einordnung statt Entscheidung",
        "reason": "keeps the limitation but removes repetitive negative phrasing",
    },
    {
        "id": "oberschwaben_step_body",
        "pattern": (
            r"Die\s+Karte\s+zeigt\s+eine\s+räumliche\s+Einordnung\s+der\s+Überschneidung\s+von\s+landwirtschaftlicher\s*"
            r"Nutzung\s+und\s+Moor-/Feuchtbodenkontext\.\s*"
            r"Sie\s+ersetzt\s+keine\s+Flächeneignungsprüfung,\s*"
            r"keine\s+Priorisierung\s+und\s+keine\s+betriebliche\s+Betroffenheitsanalyse\."
        ),
        "replacement": (
            "Die Karte ordnet die Überschneidung von landwirtschaftlicher Nutzung und "
            "Moor-/Feuchtbodenkontext räumlich ein. Entscheidungen brauchen eine Standortprüfung."
        ),
        "reason": "keeps the meaning with one positive sentence and one concise boundary",
    },
    {
        "id": "felt_source_line",
        "pattern": (
            r"Orientierung,\s*keine\s+parzellenscharfe\s+Eignungs-\s*"
            r"oder\s+Priorisierungskarte\.\s*"
            r"<a\s+href=\"#methode-in-kuerze\">Methode\s+in\s+Kürze</a>\."
        ),
        "replacement": 'Methodische Grenzen siehe <a href="#methode-in-kuerze">Methode in Kürze</a>.',
        "reason": "moves repeated caveat wording into the method link",
    },
    {
        "id": "area_balance_note",
        "pattern": (
            r"Diese\s+Werte\s+geben\s+räumliche\s+Orientierung\.\s*"
            r"Sie\s+sind\s+keine\s*"
            r"Eignungskarte,\s*keine\s+Priorisierung\s+und\s+keine\s+betriebliche\s+Betroffenheitsanalyse\."
        ),
        "replacement": (
            "Diese Werte zeigen Größenordnung und Nutzungsmix. "
            "Entscheidungen entstehen erst in der Standortprüfung."
        ),
        "reason": "reduces a repeated warning block in the area-balance section",
    },
    {
        "id": "area_balance_source_line",
        "pattern": (
            r"Eigene\s+Verschneidung\s+und\s+kartografische\s+Generalisierung\s+aus\s+FIONA\s+2024,\s*"
            r"BK50-Moor-/Feuchtbodenkontext\s+und\s+GISCO\s+NUTS\s+2024;\s*"
            r"Orientierung,\s*keine\s+Flächeneignung\."
        ),
        "replacement": (
            "Eigene Verschneidung und kartografische Generalisierung aus FIONA 2024, "
            "BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024; gerundete Orientierungswerte."
        ),
        "reason": "keeps data/source line but removes repeated no-suitability phrasing",
    },
    {
        "id": "transform_paths_work_rule",
        "pattern": (
            r"Die\s+Schnittmenge\s+ist\s+ein\s+Ausgangspunkt\s+für\s+Prüfung\s+und\s+Abstimmung\.\s*"
            r"Sie\s+ist\s+keine\s+Eignungskarte,\s*"
            r"keine\s+Priorisierung\s+und\s+keine\s+betriebliche\s+Betroffenheitsanalyse\."
        ),
        "replacement": (
            "Die Schnittmenge ist Ausgangspunkt für Prüfung und Abstimmung; "
            "tragfähig werden Pfade erst mit Wasserstand, Betrieb und Kooperation."
        ),
        "reason": "turns another caveat repetition into the section's positive argument",
    },
    {
        "id": "matrix_footer",
        "pattern": (
            r"diese\s+Matrix\s+ist\s+eine\s+Orientierung,\s*"
            r"keine\s+Standortempfehlung\."
        ),
        "replacement": (
            "diese Matrix ordnet typische Pfade und Engpässe, ersetzt aber keine Standortentscheidung."
        ),
        "reason": "keeps the methodological boundary in less repetitive wording",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def count_terms(text: str) -> dict[str, int]:
    low = text.lower()
    return {term: low.count(term.lower()) for term in CAVEAT_TERMS}


def total_terms(counts: dict[str, int]) -> int:
    return sum(counts.values())


def update_done(done_text: str, today: str) -> str:
    line = f"- B163 main-flow caveat reduction: consolidated repeated visible caveats while keeping core scope and method boundaries intact ({today})."
    if "B163 main-flow caveat reduction" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    before_counts = count_terms(html)
    patched = html

    rows = []
    for item in REPLACEMENTS:
        patched, n = re.subn(item["pattern"], item["replacement"], patched, flags=re.S | re.I)
        rows.append({
            "id": item["id"],
            "replacements": n,
            "replacement": item["replacement"],
            "reason": item["reason"],
        })

    after_counts = count_terms(patched)

    write(INDEX, patched)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "replacements", "replacement", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    doc = f"""# B163 - Main-Flow Caveat Reduction

Date: {today}

## Ziel

B163 reduziert wiederholte sichtbare Caveats im Hauptfluss, ohne fachliche Grenzen zu löschen.

Nach B158 und B162c ist die Seite ruhiger, aber in den regionalen Abschnitten erscheinen noch mehrfach ähnliche Warnformeln:

```text
keine Eignungskarte
keine Priorisierung
keine betriebliche Betroffenheitsanalyse
Orientierung
Prüfbedarf
```

Diese Aussagen bleiben fachlich wichtig. Für Premium-Pacing sollen sie aber nicht ständig als Bremsklotz im Lesefluss stehen.

## Prinzip

- Scope-Box am Anfang bleibt erhalten.
- Methode/Quellen bleiben der Ort für Detailgrenzen.
- Regionale Kartenabschnitte behalten ihre Aussagegrenzen, aber in knapperer Form.
- Keine neue Fachbehauptung.
- Keine Änderung an Karten, Felt, Scorecard, Matrixstruktur oder Daten.

## Ersetzungen

| ID | Treffer | Zweck |
|---|---:|---|
"""
    for row in rows:
        doc += f"| `{row['id']}` | {row['replacements']} | {row['reason']} |\n"

    doc += f"""
## Caveat-Term-Zählung in `index.html`

| Begriff | Vorher | Nachher |
|---|---:|---:|
"""
    for term in CAVEAT_TERMS:
        doc += f"| {term} | {before_counts[term]} | {after_counts[term]} |\n"

    doc += f"""
Gesamt:

- vorher: {total_terms(before_counts)}
- nachher: {total_terms(after_counts)}

Die Zählung ist nur ein grober Indikator. Entscheidend bleibt die sichtbare Lesbarkeit im Hauptfluss.

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- regionale Kartenabschnitte wirken weniger defensiv
- Scope bleibt fachlich klar
- Flächenbilanz bleibt methodisch abgesichert
- keine Layoutänderung
"""
    write(DOC, doc)

    audit = "# B163 main-flow caveat reduction audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"Caveat term total before: {total_terms(before_counts)}\n"
    audit += f"Caveat term total after: {total_terms(after_counts)}\n\n"
    audit += "Replacement results:\n"
    for row in rows:
        audit += f"- {row['id']}: {row['replacements']}\n"

    audit += "\n"
    if any(row["replacements"] == 0 for row in rows):
        audit += "WARN: Some replacement patterns had zero matches. Prior patches may have changed the wording; inspect manually.\n"
    else:
        audit += "OK: All planned caveat reductions matched at least once.\n"
    audit += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B163 main-flow caveat reduction complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B163_main_flow_caveat_reduction.md")
    print("  docs/B163_main_flow_caveat_replacements.csv")
    print("  docs/B163_main_flow_caveat_reduction_audit.txt")
    print("  tasks/done.md")
    print(f"Caveat term total before: {total_terms(before_counts)}")
    print(f"Caveat term total after: {total_terms(after_counts)}")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
