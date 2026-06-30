# B144 - Oberschwaben Export README

Date: 2026-06-30

## Kurzworkflow

```text
ArcGIS Pro
  -> Project nach EPSG:4326
  -> Attribute bereinigen
  -> Features To JSON mit GeoJSON-Option

mapshaper
  -> Import GeoJSON
  -> Simplify mit prevent shape removal
  -> -clean
  -> Export GeoJSON

Felt
  -> Upload
  -> Style by klasse
  -> Annotationen und Tooltips
  -> Embed-Link nur als Pilot
```

## ArcGIS-Schritte

1. Ausgangslayer oeffnen.
2. Koordinatensystem pruefen.
3. Falls nicht WGS84/EPSG:4326:
   - Werkzeug `Project`
   - Ziel: `GCS_WGS_1984` / EPSG:4326
4. Attributtabelle bereinigen.
5. Nur die Pilotfelder behalten:
   - `klasse`
   - `flaeche_ha`
   - `landkreis`
   - optional `hinweis`
6. `Features To JSON` ausfuehren.
7. Option `Output to GeoJSON` aktivieren.
8. Datei lokal speichern:

```text
working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_4326.geojson
```

## mapshaper-Schritte

1. `oberschwaben_schnittmenge_4326.geojson` in mapshaper importieren.
2. `Simplify`:
   - Methode: Visvalingam / weighted area
   - `prevent shape removal` aktivieren
   - 5-15 Prozent testen
3. Console:

```text
-clean
```

4. Export als GeoJSON:

```text
working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_simpel.geojson
```

## Optionale mapshaper-Kommandos

Falls sehr viele Splitter oder riesige Dateien entstehen, nur testen, nicht blind anwenden:

```text
-clean
-filter-fields klasse,flaeche_ha,landkreis,hinweis
```

Falls gleichartige Nachbarflaechen wirklich zusammengefasst werden sollen:

```text
-dissolve klasse
```

Achtung: `-dissolve` kann fachliche Details verlieren. Nur verwenden, wenn die Pilotkarte
dadurch klarer wird und die Schnittmenge nicht verfälscht wird.

## Felt-Styling

Startprinzip:

- Schnittmenge: satte Akzentfarbe
- Moor-/Feuchtbodenkontext: gedämpftes Blaugrau
- Ackerland: gedämpftes Ocker
- Grünland: gedämpftes Salbeigrün
- Dauerkultur: gedämpftes Violett

Direktannotation:

```text
Schnittmenge = Prüfbedarf, nicht Eignung
```

Tooltip:

```text
klasse
flaeche_ha
landkreis
```

## Git-Regel

Diese Exportdateien bleiben lokal:

```text
working/oberschwaben_felt_pilot/*
```

Nicht mit `git add .` arbeiten.
