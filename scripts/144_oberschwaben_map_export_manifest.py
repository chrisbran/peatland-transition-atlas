from pathlib import Path
import csv
from datetime import date

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "144_oberschwaben_map_export_manifest.py"
DOC = ROOT / "docs" / "B144_oberschwaben_map_export_manifest.md"
README = ROOT / "docs" / "B144_oberschwaben_map_export_readme.md"
CSV_OUT = ROOT / "docs" / "B144_oberschwaben_felt_pilot_export_manifest.csv"
AUDIT = ROOT / "docs" / "B144_oberschwaben_map_export_manifest_audit.txt"
DONE = ROOT / "tasks" / "done.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B144 Oberschwaben map export manifest: documented local export files, QA gates and no-commit rules for the Felt pilot ({date.today().isoformat()})."
    if "B144 Oberschwaben map export manifest" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def build_manifest_rows() -> list[dict[str, str]]:
    return [
        {
            "stage": "01_arcgis_projected_working",
            "filename": "oberschwaben_felt_pilot_4326.gpkg",
            "local_path_example": "working/oberschwaben_felt_pilot/oberschwaben_felt_pilot_4326.gpkg",
            "commit_status": "DO_NOT_COMMIT",
            "purpose": "Local projected working copy in EPSG:4326 before GeoJSON export.",
            "required_fields": "klasse; flaeche_ha; landkreis",
            "crs": "EPSG:4326",
            "size_target": "not relevant",
            "notes": "Created with ArcGIS Project, not Define Projection. Keep local only.",
        },
        {
            "stage": "02_arcgis_geojson_export",
            "filename": "oberschwaben_schnittmenge_4326.geojson",
            "local_path_example": "working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_4326.geojson",
            "commit_status": "DO_NOT_COMMIT",
            "purpose": "Full-resolution GeoJSON export from ArcGIS for mapshaper import.",
            "required_fields": "klasse; flaeche_ha; landkreis",
            "crs": "EPSG:4326",
            "size_target": "temporary, may be large",
            "notes": "Must be GeoJSON, not Esri JSON. Use Features To JSON with GeoJSON option.",
        },
        {
            "stage": "03_mapshaper_cleaned_simplified",
            "filename": "oberschwaben_schnittmenge_simpel.geojson",
            "local_path_example": "working/oberschwaben_felt_pilot/oberschwaben_schnittmenge_simpel.geojson",
            "commit_status": "DO_NOT_COMMIT_UNTIL_DECISION",
            "purpose": "Simplified GeoJSON for Felt upload and pilot testing.",
            "required_fields": "klasse; flaeche_ha; landkreis",
            "crs": "EPSG:4326",
            "size_target": "ideally < 2-3 MB",
            "notes": "Use mapshaper simplify with prevent shape removal and clean. Do not commit during pilot.",
        },
        {
            "stage": "04_felt_upload",
            "filename": "Felt map link / embed URL",
            "local_path_example": "docs/B145_felt_embed_candidate.txt",
            "commit_status": "COMMIT_ONLY_LINK_IF_APPROVED",
            "purpose": "Store candidate Felt share/embed URL after license/privacy check.",
            "required_fields": "n/a",
            "crs": "n/a",
            "size_target": "n/a",
            "notes": "Do not publish embed before decision gate.",
        },
        {
            "stage": "05_visual_qa",
            "filename": "felt_oberschwaben_desktop_mobile_screenshots",
            "local_path_example": "docs/screenshots/B145_felt_oberschwaben_*.png",
            "commit_status": "OPTIONAL_COMMIT_IF_SMALL",
            "purpose": "Document desktop and mobile appearance of the pilot map.",
            "required_fields": "n/a",
            "crs": "n/a",
            "size_target": "keep small",
            "notes": "Only commit compressed QA screenshots if they are useful.",
        },
        {
            "stage": "06_public_integration_candidate",
            "filename": "oberschwaben_felt_embed_test.html",
            "local_path_example": "docs/prototypes/oberschwaben_felt_embed_test.html",
            "commit_status": "OPTIONAL_DOCS_ONLY",
            "purpose": "Isolated iframe test, not active public page integration.",
            "required_fields": "n/a",
            "crs": "n/a",
            "size_target": "small",
            "notes": "The active index.html remains unchanged until the pilot is approved.",
        },
    ]


def build_doc(today: str) -> str:
    return f"""# B144 - Oberschwaben Map Export Manifest

Date: {today}

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
"""


def build_readme(today: str) -> str:
    return f"""# B144 - Oberschwaben Export README

Date: {today}

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
"""


def main() -> None:
    today = date.today().isoformat()

    write(DOC, build_doc(today))
    write(README, build_readme(today))

    rows = build_manifest_rows()
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "stage",
                "filename",
                "local_path_example",
                "commit_status",
                "purpose",
                "required_fields",
                "crs",
                "size_target",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    audit_text = f"""# B144 Oberschwaben map export manifest audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Created/updated:

- docs/B144_oberschwaben_map_export_manifest.md
- docs/B144_oberschwaben_map_export_readme.md
- docs/B144_oberschwaben_felt_pilot_export_manifest.csv
- docs/B144_oberschwaben_map_export_manifest_audit.txt
- tasks/done.md

Raw GIS/export files are intentionally not created and not staged.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B144 Oberschwaben map export manifest complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B144_oberschwaben_map_export_manifest.md")
    print("  docs/B144_oberschwaben_map_export_readme.md")
    print("  docs/B144_oberschwaben_felt_pilot_export_manifest.csv")
    print("  docs/B144_oberschwaben_map_export_manifest_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
