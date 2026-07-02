# v2.1.0 Release Notes - Peatland Transition Atlas

Date: 2026-07-02

## Zweck

`v2.1.0` schließt die öffentliche V2 nach dem Post-Publication-Review ab.

## Änderungen gegenüber v2.0.0

- Felt/OpenStreetMap-iframe aus der öffentlichen Seite entfernt.
- Externer Kartenviewer durch lokale kartografische Vertiefung ersetzt.
- External-Request-Audit ergänzt.
- Maßstabswechsel zwischen Thünen-Kulisse organischer Böden und BK50-Moor-/Feuchtbodenkontext explizit benannt.
- `~19.900 ha`-Zahl mit direktem Vorbehalt versehen.
- Flächenbilanz stärker als Aussage formuliert: vier von fünf Hektar sind Grünland.
- Engpass-Grafik durch statische Flaschenhalsgrafik ersetzt.
- Alte Scorecard-Reste aus der Engpass-Sektion entfernt.
- Schlussbogen durch Gegenposition präzisiert: Kettenperspektive ist wichtig, aber nicht jede Wiedervernässung braucht einen Produktmarkt.

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- keine Rohdaten
- keine externe Karten-/Tile-Einbindung
- B169 Sticky-Zoom bleibt aktiv
- regionale statische Karte bleibt aktiv

## QA-Soll

- B177 External Request Audit: PASS
- B103b Corrected Visible Text Audit: PASS / 0 sichtbare Findings
- B58 Visual QA and Commit Check: PASS

## Tagging

Nach Commit und Push:

```powershell
git tag -a v2.1.0 -m "Version 2.1 public demonstrator"
git push origin v2.1.0
```
