# B145 - Felt Pilot QA Checklist

Date: 2026-06-30

## 1. Daten-QA

- [ ] Karte liegt geografisch korrekt in Oberschwaben.
- [ ] Alle vier Landkreise sind erkennbar.
- [ ] `klasse` ist vorhanden.
- [ ] `flaeche_ha` ist vorhanden.
- [ ] `landkreis` ist vorhanden.
- [ ] Keine technischen Felder im Tooltip sichtbar.
- [ ] Kleine Schnittmengen-Cluster sind nicht durch Simplification verschwunden.

## 2. Kartografie-QA

- [ ] Schnittmenge ist das stärkste visuelle Signal.
- [ ] Kontextklassen sind gedämpft.
- [ ] Farben sind ausreichend unterscheidbar.
- [ ] Karte ist rotgrün-sicher genug.
- [ ] Landkreisnamen sind lesbar.
- [ ] Direktannotation erklärt die Schnittmenge.
- [ ] Karte wirkt nicht wie ein ArcGIS-Roh-Export.

## 3. Story-QA

- [ ] Karte unterstützt die Aussage `Prüfbedarf, nicht Eignung`.
- [ ] Karte erklärt die Überlagerung aus Nutzung und Moor-/Feuchtbodenkontext.
- [ ] Karte suggeriert keine Priorisierung.
- [ ] Karte suggeriert keine parzellenscharfe Eignung.
- [ ] Karte passt zur B138-Präzisierung.

## 4. Interaktions-QA

- [ ] Hover/Tooltip funktioniert am Desktop.
- [ ] Mobile Nutzung ist akzeptabel.
- [ ] Falls mobile Hover nicht sinnvoll ist: Karte bleibt auch ohne Tooltip verständlich.
- [ ] Embed lädt ohne Login.
- [ ] Embed lädt in normalem Browserfenster und privatem Fenster.

## 5. Performance-QA

- [ ] Karte lädt subjektiv schnell.
- [ ] Kein auffälliges Ruckeln.
- [ ] GeoJSON-Datei ist ausreichend vereinfacht.
- [ ] Felt-Embed blockiert nicht den restlichen Seitenaufbau.

## 6. Integrationsentscheidung

- [ ] Felt-Lizenz/Plan akzeptabel.
- [ ] Datenschutz/externes Embed akzeptabel.
- [ ] Bestehende PNG-Karte bleibt als Fallback erhalten.
- [ ] Kein aktiver Einbau in `index.html` ohne eigenen B146/B147-Patch.

## Entscheidung

```text
[ ] übernehmen als Embed-Pilot
[ ] besser als statischer Reexport verwenden
[ ] verwerfen und PNG-Version behalten
[ ] MapLibre-Minimaltest als Alternative starten
```
