# B132 - Statement Titles

Date: 2026-06-30

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
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hero bleibt unverändert.
- Überschriften wirken aussagekräftiger, aber nicht reißerisch.
- Keine Überschrift bricht unschön auf Desktop oder mobil.
- Karten- und Scrolly-Funktion bleiben unverändert.
