#!/usr/bin/env python3
"""
B93 - Prepare Oberschwaben map workflow

Purpose:
- Prepare the cartographic/GIS workflow for the Oberschwaben implementation module.
- Create folder structure, README, export specifications, data-decision matrix,
  cartographic rules and next implementation task.
- Do not create the map yet and do not modify the website.

Outputs:
- public/maps/oberschwaben/README.md
- docs/B93_prepare_oberschwaben_map_workflow.md
- docs/B93_oberschwaben_arcgis_qgis_workflow.md
- docs/B93_oberschwaben_expected_outputs.csv
- docs/B93_oberschwaben_data_decision_matrix.csv
- docs/B93_oberschwaben_cartographic_rules.md
- tasks/B94_build_oberschwaben_map_assets.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- alter existing maps/data/assets
- commit raw GIS data
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

OBER_DIR = ROOT / "public" / "maps" / "oberschwaben"
README = OBER_DIR / "README.md"

WORKFLOW = DOCS / "B93_prepare_oberschwaben_map_workflow.md"
GIS_WORKFLOW = DOCS / "B93_oberschwaben_arcgis_qgis_workflow.md"
EXPECTED_OUTPUTS = DOCS / "B93_oberschwaben_expected_outputs.csv"
DATA_MATRIX = DOCS / "B93_oberschwaben_data_decision_matrix.csv"
CARTO_RULES = DOCS / "B93_oberschwaben_cartographic_rules.md"
TASK_B94 = TASKS / "B94_build_oberschwaben_map_assets.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_expected_outputs() -> None:
    rows = [
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_admin_context.png",
            "role": "base/context",
            "content": "four SOLAMO districts: Ravensburg, Biberach, Sigmaringen, Bodenseekreis; labels and subtle boundary frame",
            "required": "yes",
            "format": "PNG, 1600x900",
            "background": "transparent preferred if used as layer stack; warm paper allowed if standalone",
            "notes": "No analytical claim. Pure orientation layer.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_agriculture.png",
            "role": "land-use context",
            "content": "agricultural land use in the four districts; ideally grouped as grassland/cropland/permanent crops if data allow",
            "required": "yes",
            "format": "PNG, 1600x900",
            "background": "transparent if layered",
            "notes": "Must not expose confidential farm-level data.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_moor_context.png",
            "role": "soil/peat context",
            "content": "peat, organic soil or wetland soil context using the selected defensible source",
            "required": "yes",
            "format": "PNG, 1600x900",
            "background": "transparent if layered",
            "notes": "Label as context, not suitability.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
            "role": "implementation signal",
            "content": "intersection of agricultural land-use context and moor/organic/wetland soil context",
            "required": "yes",
            "format": "PNG, 1600x900",
            "background": "transparent if layered",
            "notes": "Core analytical layer; wording: Nutzung × Bodenkontext.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png",
            "role": "interpretation",
            "content": "optional classification of land-use types within the intersection",
            "required": "recommended",
            "format": "PNG, 1600x900",
            "background": "transparent if layered",
            "notes": "Only if land-use classes are reliable enough.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_implementation_context_composite.png",
            "role": "presentation composite",
            "content": "single standalone map combining admin frame, agriculture, moor context and intersection",
            "required": "yes for first presentation",
            "format": "PNG, 1600x900",
            "background": "warm paper or transparent depending on page design",
            "notes": "Recommended first asset before building a scrolly/layer stack.",
        },
        {
            "output_file": "public/maps/oberschwaben/oberschwaben_map_sources.json",
            "role": "metadata",
            "content": "source names, dates, licenses, processing notes for each layer",
            "required": "yes",
            "format": "JSON",
            "background": "n/a",
            "notes": "No raw data; only metadata.",
        },
    ]
    fields = ["output_file", "role", "content", "required", "format", "background", "notes"]
    with EXPECTED_OUTPUTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_data_matrix() -> None:
    rows = [
        {
            "decision_area": "administrative boundaries",
            "preferred_option": "Landkreisgrenzen for Ravensburg, Biberach, Sigmaringen, Bodenseekreis",
            "fallback_option": "NUTS/LAU/generalised administrative boundaries",
            "decision_needed": "Which boundary source is already in the project and legally safe for public display?",
            "risk": "low",
            "status": "open",
        },
        {
            "decision_area": "agricultural land-use layer",
            "preferred_option": "Official agricultural land-use data with crop/grassland classes if public or project-usable",
            "fallback_option": "ATKIS/LBM-DE/CORINE/generalised land-cover layer",
            "decision_needed": "Can we legally use detailed agricultural polygons or only a coarser public land-cover layer?",
            "risk": "high",
            "status": "open",
        },
        {
            "decision_area": "moor/organic/wetland soil context",
            "preferred_option": "Best available regional official layer: Moorkataster if usable; otherwise BK50/organic soil context",
            "fallback_option": "Existing BK50-derived BW layer already used in the atlas",
            "decision_needed": "Which layer is fachlich strongest and license-safe for public prototype use?",
            "risk": "high",
            "status": "open",
        },
        {
            "decision_area": "intersection calculation",
            "preferred_option": "GIS overlay agriculture ∩ soil/moor context, area aggregated by district",
            "fallback_option": "visual-only overlay without numeric aggregation",
            "decision_needed": "Do we calculate hectares and shares now, or first publish visual context only?",
            "risk": "medium",
            "status": "open",
        },
        {
            "decision_area": "resolution/generalisation",
            "preferred_option": "generalised enough for public communication, detailed enough to show spatial pattern",
            "fallback_option": "district-level aggregated bars/tables without exact polygons",
            "decision_needed": "How detailed may public display be without implying farm-level affectedness?",
            "risk": "medium",
            "status": "open",
        },
        {
            "decision_area": "legend wording",
            "preferred_option": "Landwirtschaftliche Nutzung; Moor-/Feuchtbodenkontext; Schnittmenge Nutzung × Kontext",
            "fallback_option": "Bodenkontext; Nutzungskontext; Umsetzungsraum",
            "decision_needed": "Choose wording that cannot be misread as suitability or priority.",
            "risk": "medium",
            "status": "open",
        },
        {
            "decision_area": "SOLAMO link",
            "preferred_option": "Use SOLAMO as socio-economic bridge, not as completed-results claim",
            "fallback_option": "Keep SOLAMO only in documentation until project wording is approved",
            "decision_needed": "How explicitly should SOLAMO be named in the public page?",
            "risk": "medium",
            "status": "open",
        },
    ]
    fields = ["decision_area", "preferred_option", "fallback_option", "decision_needed", "risk", "status"]
    with DATA_MATRIX.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    OBER_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    readme = f"""# Oberschwaben map assets

Created by B93 on {today}.

## Purpose

This folder will contain map assets for the Oberschwaben implementation module.

The module connects the existing Baden-Württemberg/BK50 endpoint to the SOLAMO-BW implementation question:

```text
Moor-/Feuchtbodenkontext
+
landwirtschaftliche Nutzung
=
räumlicher Hinweis auf mögliche Umsetzungsbetroffenheit
```

## Focus area

Four SOLAMO-BW districts:

- Ravensburg
- Biberach
- Sigmaringen
- Bodenseekreis

## Expected public assets

```text
oberschwaben_admin_context.png
oberschwaben_agriculture.png
oberschwaben_moor_context.png
oberschwaben_agriculture_moor_intersection.png
oberschwaben_landuse_classes_on_moor.png
oberschwaben_implementation_context_composite.png
oberschwaben_map_sources.json
```

## Export standard

Default for future PNG exports:

- 1600 x 900 px
- PNG
- 32-bit with alpha if used as layer stack
- transparent background for stack layers
- identical extent for all stack layers
- identical projection for all stack layers
- no raw GIS data in this folder

## Method boundary

These maps must be described as **räumliche Einordnung**.

They must not be labelled as:

- suitability map,
- priority map,
- affected farms,
- intervention recommendation,
- completed SOLAMO result.

Preferred wording:

- Moor-/Feuchtbodenkontext
- landwirtschaftliche Nutzung
- Schnittmenge Nutzung × Bodenkontext
- mögliche Umsetzungsbetroffenheit
- Grundlage für weitere sozio-ökonomische Analyse
"""
    write(README, readme)

    workflow = f"""# B93 - Prepare Oberschwaben Map Workflow

Date: {today}

## 1. Purpose

B93 prepares the cartographic workflow for the next substantive module:

**Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird**

It does not create the map yet and does not modify the website.

## 2. Why this module matters

The existing page now reaches Baden-Württemberg and shows regional Moor-/Feuchtbodenkontext. The next substantive question is whether and where this context overlaps with agricultural land use.

That overlap is the bridge to SOLAMO-BW:

```text
Bodenkontext -> Nutzungskontext -> mögliche betriebliche Betroffenheit -> Nutzungskonzepte -> Wertschöpfungsketten -> Politikempfehlungen
```

## 3. Focus area

Use the four SOLAMO-BW districts:

- Ravensburg
- Biberach
- Sigmaringen
- Bodenseekreis

Do not broaden the first module beyond these counties unless there is a clear cartographic reason.

## 4. Required map logic

The first map should be built as a conservative spatial context map.

It should show:

1. administrative frame,
2. agricultural land-use context,
3. moor/organic/wetland soil context,
4. intersection of agriculture and soil/moor context,
5. optional land-use classes within that intersection.

## 5. First recommended public map

For the next visible website step, start with one composite map:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

Why composite first?

- easier to review,
- lower risk than a new scrolly module,
- enough for a project presentation,
- can later be decomposed into layer stack if needed.

## 6. Later optional layer stack

If the composite works, prepare identical-extent transparent PNGs:

```text
oberschwaben_admin_context.png
oberschwaben_agriculture.png
oberschwaben_moor_context.png
oberschwaben_agriculture_moor_intersection.png
```

This would allow a future scroll sequence:

```text
Landkreisrahmen -> Landwirtschaft -> Moor-/Feuchtbodenkontext -> Schnittmenge
```

## 7. Data decisions before export

See:

- `docs/B93_oberschwaben_data_decision_matrix.csv`

Main unresolved decisions:

1. legally usable agricultural land-use layer,
2. best defensible moor/organic/wetland soil layer,
3. whether to calculate hectares now or only show visual context,
4. level of spatial generalisation,
5. exact legend wording.

## 8. Expected outputs

See:

- `docs/B93_oberschwaben_expected_outputs.csv`

## 9. Method boundary

This sentence should be used in the future module documentation and likely on the page:

```text
Die Oberschwaben-Karte zeigt eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## 10. Next implementation task

B94 should build the first map assets.

B94 should not bind the map to the website yet unless the map asset is visually and methodically accepted.
"""
    write(WORKFLOW, workflow)

    gis_workflow = f"""# B93 - Oberschwaben ArcGIS/QGIS Workflow

Date: {today}

## 1. Goal

Create a first cartographic asset for the Oberschwaben implementation module.

Primary output:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

Optional stack outputs:

```text
public/maps/oberschwaben/oberschwaben_admin_context.png
public/maps/oberschwaben/oberschwaben_agriculture.png
public/maps/oberschwaben/oberschwaben_moor_context.png
public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png
```

## 2. Input data

### Required

1. Landkreis boundaries
   - Ravensburg
   - Biberach
   - Sigmaringen
   - Bodenseekreis

2. Agricultural land-use layer
   - ideally agricultural polygons/classes
   - at minimum agriculture/non-agriculture context

3. Moor-/organic-/wetland-soil context layer
   - choose one defensible source first
   - document source and interpretation

### Optional

4. land-use class layer within intersection
5. orientation labels for major moor landscapes
6. simple county-level indicator table

## 3. GIS processing steps

### Step 1 - Create Oberschwaben focus region

Select the four districts.

Suggested expression depends on source fields, for example:

```text
NAME IN ('Ravensburg', 'Biberach', 'Sigmaringen', 'Bodenseekreis')
```

or with AGS IDs if available.

Dissolve selected districts into:

```text
oberschwaben_focus_region
```

Keep original county polygons for labels and aggregation.

### Step 2 - Clip agricultural layer

Clip agriculture layer to focus region:

```text
agriculture_oberschwaben = agriculture_layer CLIP oberschwaben_focus_region
```

If land-use classes are available, harmonise into:

- Grünland
- Ackerland
- Dauerkultur
- Sonstige landwirtschaftliche Nutzung

### Step 3 - Clip moor/soil context layer

Clip selected moor/soil layer to focus region:

```text
moor_context_oberschwaben = moor_context_layer CLIP oberschwaben_focus_region
```

Do not overclassify in the first version.

Recommended initial class:

```text
Moor-/Feuchtbodenkontext
```

### Step 4 - Intersect agriculture and moor/soil context

Create:

```text
agriculture_moor_intersection = agriculture_oberschwaben INTERSECT moor_context_oberschwaben
```

This is the key implementation-context layer.

Recommended map label:

```text
Schnittmenge: Landwirtschaft × Moor-/Feuchtbodenkontext
```

Avoid:

```text
Wiedervernässungspotenzial
Priorität
Eignung
Betroffenheit der Betriebe
```

### Step 5 - Aggregate indicators by district

Calculate hectares by county:

- total agricultural area,
- moor/soil context area,
- intersection area,
- share of agriculture on moor/soil context,
- share of moor/soil context under agricultural use.

Export as table later if needed.

### Step 6 - Layout and export

Recommended layout:

- 16:9
- 1600 x 900 px
- north-up
- simple county labels
- minimal legend
- warm paper or transparent background depending on use
- no photographic basemap
- avoid visual clutter

## 4. Suggested symbology

Base:

- Landkreis boundaries: thin muted grey/brown line
- agriculture: light warm ochre or muted yellow-green
- moor/soil context: teal/green
- intersection: stronger blue-green or dark accent
- water/major context: optional very subtle

Important:

Use the intersection as the visual focus, but do not make it look like a policy priority class.

## 5. Export requirements

For transparent layer stack:

- PNG
- 1600 x 900 px
- transparent background
- identical extent across all layers
- identical legend position if legends embedded, or no embedded legend

For first standalone composite:

- PNG
- 1600 x 900 px
- warm paper background allowed
- compact legend embedded
- short source note embedded or documented in JSON

## 6. QA before website integration

Check:

1. all four counties visible and labelled,
2. no layer extends beyond focus region,
3. intersection is visible but not over-dominant,
4. legend does not imply suitability,
5. method boundary documented,
6. file names match B93 expected outputs,
7. no raw GIS files placed under `public/maps/oberschwaben/`.
"""
    write(GIS_WORKFLOW, gis_workflow)

    carto_rules = f"""# B93 - Oberschwaben Cartographic Rules

Date: {today}

## 1. Design principle

The map should look like a professional regional implementation map, not like a GIS dump.

It should support one argument:

**Wo landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext zusammentreffen, wird Moorschutz zur Umsetzungsfrage.**

## 2. Must show

- four SOLAMO districts,
- agriculture layer,
- moor/soil context layer,
- intersection layer,
- simple legend,
- method boundary in documentation.

## 3. Must not show

- parcel-level farm information,
- confidential farm-level data,
- exact farm affectedness,
- suitability classes,
- priority classes,
- intervention recommendations.

## 4. Recommended legend wording

Use:

```text
Landkreisrahmen
Landwirtschaftliche Nutzung
Moor-/Feuchtbodenkontext
Schnittmenge: Nutzung × Bodenkontext
```

Avoid:

```text
geeignete Flächen
Prioritätsflächen
Wiedervernässungspotenzial
betroffene Betriebe
```

## 5. Color logic

Recommended direction:

- background: warm paper or transparent,
- counties: muted grey/brown,
- agriculture: restrained ochre/yellow-green,
- moor context: teal/green,
- intersection: strongest but not alarming accent.

Do not use red for intersection unless explicitly communicating risk, because it may imply alarm or priority.

## 6. Label hierarchy

Highest:

- title or module heading outside map,
- intersection layer in legend.

Medium:

- county names.

Low:

- source note,
- orientation labels.

## 7. Source note

Suggested short source note:

```text
Eigene Darstellung auf Basis von Landkreisgrenzen, landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Methodische Einordnung, keine Eignungs- oder Prioritätskarte.
```

Replace with exact source names once data decisions are final.
"""
    write(CARTO_RULES, carto_rules)

    task_b94 = f"""# B94 - Build Oberschwaben Map Assets

Created from B93 on {today}

## Goal

Build the first Oberschwaben implementation map asset.

Primary target:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Required before starting

Confirm data decisions from:

```text
docs/B93_oberschwaben_data_decision_matrix.csv
```

At minimum decide:

1. administrative boundary source,
2. agricultural land-use source,
3. moor/organic/wetland soil context source,
4. whether first map is visual-only or includes area indicators.

## Expected workflow

1. create focus region for Ravensburg, Biberach, Sigmaringen, Bodenseekreis,
2. clip agriculture layer,
3. clip moor/soil context layer,
4. intersect agriculture and moor/soil context,
5. design first composite map,
6. export 1600 x 900 PNG,
7. document sources and method boundary,
8. run visual QA.

## Do not

- place raw GIS files in `public/maps/oberschwaben/`,
- call the intersection a suitability map,
- call it a priority map,
- expose farm-level data,
- bind to website before visual review.
"""
    write(TASK_B94, task_b94)

    write_expected_outputs()
    write_data_matrix()

    done_entry = f"""
## B93 - Prepare Oberschwaben map workflow ({today})

- Created `public/maps/oberschwaben/README.md`.
- Created `docs/B93_prepare_oberschwaben_map_workflow.md`.
- Created `docs/B93_oberschwaben_arcgis_qgis_workflow.md`.
- Created `docs/B93_oberschwaben_expected_outputs.csv`.
- Created `docs/B93_oberschwaben_data_decision_matrix.csv`.
- Created `docs/B93_oberschwaben_cartographic_rules.md`.
- Created `tasks/B94_build_oberschwaben_map_assets.md`.
- Prepared map workflow for Oberschwaben implementation module.
- Did not modify production HTML, CSS, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B93 - Prepare Oberschwaben map workflow" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B93 prepare Oberschwaben map workflow complete.")
    print("Changed/created:")
    for path in [README, WORKFLOW, GIS_WORKFLOW, EXPECTED_OUTPUTS, DATA_MATRIX, CARTO_RULES, TASK_B94, DONE]:
        print(f"  {rel(path)}")


if __name__ == "__main__":
    main()
