# B144 - Oberschwaben Map Export Manifest

Date: 2026-06-30

## Ziel

B144 bereitet den Kartenqualitaets-Pilot fuer Oberschwaben organisatorisch vor.
Es wird noch keine Karte ersetzt und kein Embed in die oeffentliche Seite eingebaut.

Der Zweck ist ein klares Export- und QA-Protokoll fuer den Weg:

```text
ArcGIS -> EPSG:4326 -> GeoJSON -> mapshaper -> Felt -> iframe-Test
```

## Entscheidung aus B143

Der aktuelle PNG-/Sticky-Kartenstack bleibt stabil. Der Karten-Relaunch wird als separater
Oberschwaben-Pilot vorbereitet. Erst nach einem bestandenen Pilot-Gate wird entschieden,
ob ein Felt-Embed, ein hochwertiger statischer Reexport oder spaeter MapLibre in die
oeffentliche Seite uebernommen wird.

## Zieldatei des Pilotexports

```text
oberschwaben_schnittmenge_simpel.geojson
```

Diese Datei ist fuer Felt gedacht, wird aber waehrend des Pilots nicht automatisch committed.

## No-Commit-Regel

Nicht ins Repo committen:

```text
working/
data/external/
data/working/
sources/
*.shp
*.shx
*.dbf
*.prj
*.cpg
*.gpkg
*.gdb
*_4326.geojson
*_simpel.geojson
```

Ausnahme erst nach expliziter Entscheidung:

- stark vereinfachte, oeffentliche Web-Geometrie
- nur wenn Lizenz, Dateigroesse und Datenschutz geklaert sind
- dann bevorzugt unter `public/maps/...` mit README und Quellenzeile

## Minimale Attributstruktur

| Feld | Typ | Zweck |
|---|---|---|
| `klasse` | Text | Styling nach Nutzung / Kontext / Schnittmenge |
| `flaeche_ha` | Zahl | Tooltip und Plausibilisierung |
| `landkreis` | Text | Orientierung und Tooltip |
| `hinweis` | Text, optional | kurze Lesehilfe fuer Spezialfaelle |

Erlaubte Werte fuer `klasse`:

```text
Ackerland
Gruenland
Dauerkultur
Moor-/Feuchtbodenkontext
Schnittmenge
```

Wenn moeglich `Grünland` verwenden. Falls technische Kompatibilitaet wichtiger ist,
kann `Gruenland` intern verwendet und in Felt als Label umbenannt werden.

## Export-Gates

### Gate 1 - ArcGIS

- Layer ist wirklich nach EPSG:4326 projiziert
- `Project` verwendet, nicht `Define Projection`
- Attributtabelle ist bereinigt
- Export ist GeoJSON, nicht Esri-JSON

### Gate 2 - mapshaper

- Import ohne Geometriefehler
- `-clean` ausgefuehrt
- Vereinfachung mit `prevent shape removal`
- kleine Schnittmengen-Cluster bleiben sichtbar
- Datei moeglichst unter 2-3 MB

### Gate 3 - Felt

- Styling nach `klasse`
- Schnittmenge ist die dominanteste Farbe
- Kontextklassen sind gedämpft
- Landkreisnamen und mindestens eine Direktannotation gesetzt
- Tooltip zeigt nur wenige, lesbare Felder
- Karte ist mobil akzeptabel

### Gate 4 - Integration

- Embed-Link funktioniert ohne Login
- Datenschutz/Lizenz ist akzeptabel
- Ladezeit ist vertretbar
- PNG-Fallback bleibt erhalten
- kein aktiver Umbau von `index.html` ohne gesonderten Integrationspatch

## Zugehoerige Dateien

- `docs/B144_oberschwaben_felt_pilot_export_manifest.csv`
- `docs/B144_oberschwaben_map_export_readme.md`
- `docs/B144_oberschwaben_map_export_manifest_audit.txt`

## Naechster Schritt

B145 sollte erst beginnen, wenn der lokale Export aus ArcGIS und mapshaper vorliegt.
B145 ist dann kein Seitenumbau, sondern der Felt-Prototyp bzw. die Dokumentation des
externen Kartenentwurfs.
