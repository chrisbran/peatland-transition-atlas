# B137 - Consequence Kicker

Date: 2026-06-30

## Ziel

B137 ergänzt vor dem Quellen-/Methodikbereich einen knappen Schluss- bzw. Kickerblock.
Er verdichtet die V2-Erzählung: Moorbodenschutz ist nicht nur eine Frage der Fläche,
sondern der funktionierenden Kette aus Wasser, Nutzung, Verarbeitung und Nachfrage.

## Umsetzung

- neue Section `Konsequenz`
- Aussage-Titel: `Der Hebel verschiebt sich von der Fläche zur Kette`
- drei kurze Konsequenzen:
  - Wiedervernässung ist notwendig, aber nicht ausreichend
  - Planung muss hydrologische Einheiten ernst nehmen
  - Wertschöpfung muss vor der Skalierung mitgedacht werden
- Position vor dem Quellen-/Methodikbereich
- keine Änderung an Kartenlogik, Daten, Navigation oder Scorecard

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/137_consequence_kicker.py`
- `docs/B137_consequence_kicker.md`
- `docs/B137_consequence_kicker_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Kicker steht vor Quellen/Methodik.
- Er wirkt wie eine Schlussfolgerung, nicht wie ein weiterer Datenblock.
- Desktop: drei Karten nebeneinander.
- Mobil: Karten sauber gestapelt.
- Quellenblock und Methode-in-Kürze bleiben erhalten.
