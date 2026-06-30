# B139 - Water Governance Block

Date: 2026-06-30

## Ziel

B139 ergänzt den V2-Abschnitt `Wasser und Governance`.
Er macht sichtbar, dass Moorbodenschutz nicht nur auf Parzellenebene funktioniert:
Parzelle, Betrieb und hydrologische Einheit sind unterschiedliche Planungsebenen.

## Umsetzung

- neue Section vor dem Konsequenz-Kicker bzw. vor Quellen/Methodik
- Titel: `Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen`
- drei Planungsebenen:
  - Parzelle
  - Betrieb
  - Hydrologische Einheit
- kurze Schlussnotiz zur Abstimmung zwischen Wasserkenntnis, Eigentümern, Betrieben und Wertschöpfung
- keine Änderung an Kartenlogik, Daten, Navigation, Scorecard oder Quellenblock

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/139_water_governance_block.py`
- `docs/B139_water_governance_block.md`
- `docs/B139_water_governance_block_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Block steht vor dem Konsequenz-Kicker oder vor Quellen/Methodik.
- Er wirkt wie eine fachliche Brücke zwischen Wertschöpfung und Schlussfolgerung.
- Desktop: drei Karten nebeneinander.
- Mobil: Karten sauber gestapelt.
- Keine Änderung an Scorecard, Navigation und Karten.
