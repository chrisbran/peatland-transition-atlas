# B130c - Central Value-Chain Sources

Date: 2026-06-30

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
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Quellenblock am Seitenende enthält die drei neuen Einträge.
- B130b-Scorecard bleibt unverändert.
- Bestehende Datengrundlagen bleiben erhalten.
