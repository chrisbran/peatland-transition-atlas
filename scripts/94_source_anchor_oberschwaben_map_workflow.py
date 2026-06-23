#!/usr/bin/env python3
"""
B94 - Source-anchor Oberschwaben map workflow

Purpose:
- Anchor the planned Oberschwaben map module to the data-source logic visible
  in the SOLAMO-BW flyer map.
- Clarify which sources are reference anchors, which data-access decisions remain open,
  and how legend wording must avoid overclaiming.
- Prepare the next task B95 for building actual map assets.
- Do not modify the website or create map images yet.

Outputs:
- docs/B94_oberschwaben_source_stack.md
- docs/B94_oberschwaben_source_stack.csv
- docs/B94_oberschwaben_data_access_questions.md
- docs/B94_oberschwaben_legend_and_map_logic.md
- docs/B94_oberschwaben_flyer_map_reference_note.md
- tasks/B95_build_oberschwaben_map_assets.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- create or overwrite map PNGs
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

SOURCE_STACK_MD = DOCS / "B94_oberschwaben_source_stack.md"
SOURCE_STACK_CSV = DOCS / "B94_oberschwaben_source_stack.csv"
DATA_QUESTIONS = DOCS / "B94_oberschwaben_data_access_questions.md"
LEGEND_LOGIC = DOCS / "B94_oberschwaben_legend_and_map_logic.md"
FLYER_NOTE = DOCS / "B94_oberschwaben_flyer_map_reference_note.md"
TASK_B95 = TASKS / "B95_build_oberschwaben_map_assets.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_source_stack_csv() -> None:
    rows = [
        {
            "source_anchor": "Gemeinsamer Antrag Baden-Württemberg",
            "source_owner_or_label": "MLR Baden-Württemberg",
            "year_from_flyer": "2024",
            "intended_layer": "agricultural land-use context",
            "expected_classes": "Ackerland; Grünland; Dauerkultur",
            "use_in_our_map": "preferred source for agricultural use if legally and technically accessible",
            "public_use_status": "open",
            "risk": "may be restricted or not suitable for public polygon display",
            "fallback": "public land-cover layer such as ATKIS/LBM-DE/CORINE, if adequate",
        },
        {
            "source_anchor": "Feuchtgebiete und Moore der Bodenkarte Baden-Württemberg / GeoLa BK50MOOR",
            "source_owner_or_label": "LGRB",
            "year_from_flyer": "2025",
            "intended_layer": "moor/wetland/organic-soil context",
            "expected_classes": "Moor-/Feuchtbodenkontext; optional subtypes if defensible",
            "use_in_our_map": "preferred soil-context source if accessible and license-safe",
            "public_use_status": "open",
            "risk": "must not be interpreted as rewetting suitability or priority",
            "fallback": "existing BK50-derived BW layer already used in the atlas; or Thünen organic-soil layer for broader context",
        },
        {
            "source_anchor": "BKG administrative/cartographic base",
            "source_owner_or_label": "BKG",
            "year_from_flyer": "2026",
            "intended_layer": "administrative boundaries / base geography",
            "expected_classes": "Landkreisgrenzen; optional base geometry",
            "use_in_our_map": "county frame for Ravensburg, Biberach, Sigmaringen, Bodenseekreis",
            "public_use_status": "likely feasible but confirm license/attribution",
            "risk": "low",
            "fallback": "NUTS/LAU/generalised public administrative boundaries already used in project",
        },
        {
            "source_anchor": "Own overlay processing",
            "source_owner_or_label": "project-derived",
            "year_from_flyer": "n/a",
            "intended_layer": "intersection agriculture x moor/wetland context",
            "expected_classes": "Schnittmenge Nutzung × Bodenkontext",
            "use_in_our_map": "core implementation-context layer",
            "public_use_status": "depends on input source rights",
            "risk": "high risk of being misread as suitability, affected farms or priority",
            "fallback": "visual overlay only, no numeric hectares, until data rights and method are settled",
        },
    ]
    fields = [
        "source_anchor",
        "source_owner_or_label",
        "year_from_flyer",
        "intended_layer",
        "expected_classes",
        "use_in_our_map",
        "public_use_status",
        "risk",
        "fallback",
    ]
    with SOURCE_STACK_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    source_stack = f"""# B94 - Oberschwaben Source Stack

Date: {today}

## 1. Purpose

B94 anchors the Oberschwaben map workflow to the source logic visible in the SOLAMO-BW flyer map.

The flyer map is not treated as data. It is treated as a **reference for a plausible source stack and map logic**.

## 2. Source stack interpreted from the flyer map

The visible source note in the flyer map points to three core source groups:

1. **Gemeinsamer Antrag Baden-Württemberg / MLR, 2024**  
   Used for agricultural land-use information.

2. **Feuchtgebiete und Moore der Bodenkarte Baden-Württemberg / GeoLa BK50MOOR / LGRB, 2025**  
   Used for the moor/wetland/soil context.

3. **BKG, 2026**  
   Used for administrative/cartographic base information.

## 3. Translation into our map logic

The flyer map shows the communication potential of a regional map where agricultural use and organic/moor soil context are combined.

Our map should not simply copy the flyer. It should reproduce the **analytical logic** with clear method boundaries:

```text
Landwirtschaftliche Nutzung
+
Moor-/Feuchtbodenkontext
=
räumlicher Hinweis auf mögliche Umsetzungsbetroffenheit
```

## 4. Preferred source stack for our first own map

| Map component | Preferred source anchor | Intended role |
|---|---|---|
| Landkreisrahmen | BKG / public admin boundaries | spatial frame |
| Landwirtschaftliche Nutzung | Gemeinsamer Antrag BW, MLR 2024 | agricultural use context |
| Moor-/Feuchtbodenkontext | GeoLa BK50MOOR / LGRB 2025 | soil/moor context |
| Schnittmenge | own GIS overlay | implementation-context signal |

## 5. Source-access status

The source anchors are known, but data access is not yet settled.

Before B95 can build actual assets, we need to clarify:

- whether the Gemeinsamer Antrag layer can be used publicly,
- whether exact agricultural polygons may be displayed,
- whether BK50MOOR/GeoLa data are available in a web-display-safe form,
- which attribution wording is required,
- whether a visual-only map is safer than a map with hectare statistics.

## 6. Method boundary

The source stack supports a **context map**, not a decision map.

Do not label the resulting map as:

- Eignungskarte,
- Prioritätskarte,
- Wiedervernässungspotenzial,
- betroffene Betriebe,
- SOLAMO-Ergebnis.

Preferred wording:

- räumliche Einordnung,
- Nutzung × Bodenkontext,
- mögliche Umsetzungsbetroffenheit,
- Ausgangspunkt für sozio-ökonomische Analyse,
- Grundlage für weitere Prüfung.
"""
    write(SOURCE_STACK_MD, source_stack)
    write_source_stack_csv()

    data_questions = f"""# B94 - Oberschwaben Data Access Questions

Date: {today}

## 1. Purpose

This document lists the data-access questions that must be answered before B95 builds map assets.

## 2. Agricultural land-use data

### Preferred source anchor

**Gemeinsamer Antrag Baden-Württemberg / MLR, 2024**

### Questions

1. Do we have access to the same or equivalent data used in the SOLAMO flyer map?
2. Are the data available as polygons, raster, or already-generalised categories?
3. Can the data be displayed publicly on GitHub Pages?
4. Are there restrictions against parcel-level display?
5. Is aggregation or generalisation required?
6. Can we classify into:
   - Ackerland,
   - Grünland,
   - Dauerkultur?
7. Are there additional categories that should be hidden or merged?

### Recommended first decision

If detailed polygons are sensitive or restricted, create a **generalised visual layer** or use coarser public land-cover data.

## 3. Moor-/soil-context data

### Preferred source anchor

**Feuchtgebiete und Moore der Bodenkarte Baden-Württemberg / GeoLa BK50MOOR / LGRB, 2025**

### Questions

1. Do we have the same BK50MOOR/GeoLa layer referenced by the flyer?
2. Is it available as vector data, raster data, WMS, or only as map service?
3. Can it be exported as a public PNG context layer?
4. Which classes should be included?
5. Should the first version merge all relevant types into one class:
   `Moor-/Feuchtbodenkontext`?
6. Is a distinction between Niedermoor, Hochmoor, Anmoor, Gley etc. needed now or later?

### Recommended first decision

Use one merged and methodically cautious class for the first version.

## 4. Administrative base

### Preferred source anchor

**BKG, 2026**

### Questions

1. Which district-boundary layer should be used?
2. Do we already have a suitable NUTS/administrative layer in the repo/workflow?
3. Should the first map show only the four districts or some surrounding context?
4. Which label names should be used:
   - Ravensburg,
   - Biberach,
   - Sigmaringen,
   - Bodenseekreis?

### Recommended first decision

Use four-district focus with subtle surrounding context only if needed for orientation.

## 5. Derived intersection layer

### Questions

1. Should the first B95 output be visual-only or include calculated hectares?
2. If hectares are calculated, what projection/equal-area CRS will be used?
3. Should the intersection be clipped to agricultural use only or stratified by land-use class?
4. How much geometry simplification is appropriate for public display?
5. Should the intersection be shown as exact polygons or generalised patches?

### Recommended first decision

Start with a visual composite map. Add hectare indicators only after source rights and geometry definitions are stable.

## 6. Minimum data-decision checklist before B95

B95 may proceed if these are answered:

- [ ] agriculture source chosen,
- [ ] soil/moor context source chosen,
- [ ] public display rights acceptable,
- [ ] four county boundary source chosen,
- [ ] first output type chosen: visual-only or visual + indicators,
- [ ] legend wording approved,
- [ ] method boundary approved.
"""
    write(DATA_QUESTIONS, data_questions)

    legend_logic = f"""# B94 - Oberschwaben Legend and Map Logic

Date: {today}

## 1. Purpose

Define a legend and map logic that follows the SOLAMO flyer source stack but avoids overclaiming.

## 2. Working map title

Preferred:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

Alternative shorter:

```text
Oberschwaben: Nutzung × Moorbodenkontext
```

## 3. Core map statement

```text
Die Karte zeigt, wo landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext räumlich zusammentreffen.
```

## 4. Legend entries

Recommended first legend:

| Legend entry | Meaning | Visual role |
|---|---|---|
| Landkreisrahmen | four SOLAMO districts | orientation |
| Ackerland | agricultural use class | land-use context |
| Grünland | agricultural use class | land-use context |
| Dauerkultur | agricultural use class | land-use context |
| Moor-/Feuchtbodenkontext | soil/moor/wetland context | environmental context |
| Schnittmenge Nutzung × Bodenkontext | agriculture on/within moor-wetland context | implementation signal |

## 5. Alternative simplified legend

If the map becomes too dense:

| Legend entry | Meaning |
|---|---|
| Landwirtschaftliche Nutzung | merged agriculture |
| Moor-/Feuchtbodenkontext | merged soil/moor context |
| Schnittmenge Nutzung × Bodenkontext | overlap |

This may be better for the website.

## 6. Wording to avoid

Do not use:

- Wiedervernässungspotenzial,
- Prioritätsfläche,
- geeignete Fläche,
- betroffene Betriebe,
- Maßnahmenfläche,
- Paludikulturfläche,
- SOLAMO-Ergebnis.

## 7. Preferred explanatory note

```text
Die Darstellung zeigt eine räumliche Einordnung. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## 8. Interpretation cards for the future page

### Karte zeigt Kontext

```text
Die Karte markiert Räume, in denen landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext zusammenfallen.
```

### Daraus entsteht Betroffenheit

```text
Erst aus der Überschneidung von Fläche, Nutzung und Betriebsstruktur wird eine Umsetzungsfrage.
```

### Daraus folgen Nutzungspfade

```text
Mögliche Pfade reichen von Schutz und Stabilisierung über Wiedervernässung bis zu nasser Nutzung und Wertschöpfungsketten.
```

## 9. Visual hierarchy

The intersection layer should be the focus, but it should not look like an alarm or priority class.

Recommended visual hierarchy:

1. intersection layer strongest,
2. moor-/soil context second,
3. agriculture classes restrained,
4. county boundaries and labels quiet.

## 10. First map design choice

For B95, prefer a **single composite map** first.

Reason:

- easier to review,
- lower implementation risk,
- enough for project discussion,
- avoids adding another scroll system before the map logic is stable.
"""
    write(LEGEND_LOGIC, legend_logic)

    flyer_note = f"""# B94 - Oberschwaben Flyer Map Reference Note

Date: {today}

## 1. Purpose

This note records how the SOLAMO-BW flyer map informs the Oberschwaben map workflow.

## 2. What the flyer map contributes

The flyer map contributes three things:

1. a regional focus,
2. a visual precedent,
3. a source-stack hint.

## 3. Regional focus

The map and flyer focus on the SOLAMO-BW region:

- Sigmaringen,
- Biberach,
- Ravensburg,
- Bodenseekreis.

## 4. Visual precedent

The flyer map shows agricultural use on organic soils with classes such as:

- Ackerland,
- Grünland,
- Dauerkultur.

This confirms that a map combining agricultural use and soil/moor context is communicatively plausible.

## 5. Source-stack hint

The visible source note points to:

- Gemeinsamer Antrag Baden-Württemberg / MLR, 2024,
- Feuchtgebiete und Moore der Bodenkarte BW / GeoLa BK50MOOR / LGRB, 2025,
- BKG, 2026.

## 6. How we use this

We use the flyer map as a reference for **which data families to investigate**.

We do not treat the screenshot as raw data.

We do not copy the map.

We build an own source-documented map if the data access and license situation allow it.

## 7. Method boundary

Even if we reproduce a similar source stack, our page must state:

```text
Die Darstellung ist eine räumliche Einordnung. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```
"""
    write(FLYER_NOTE, flyer_note)

    task_b95 = f"""# B95 - Build Oberschwaben Map Assets

Created from B94 on {today}

## Goal

Build the first source-anchored Oberschwaben map asset.

Primary output:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Source anchors from B94

Use B94 as source-stack guide:

```text
docs/B94_oberschwaben_source_stack.md
docs/B94_oberschwaben_source_stack.csv
docs/B94_oberschwaben_data_access_questions.md
docs/B94_oberschwaben_legend_and_map_logic.md
```

## Minimum decisions before generating map

- [ ] agriculture source selected,
- [ ] soil/moor context source selected,
- [ ] administrative boundary source selected,
- [ ] public display rights checked,
- [ ] first output selected: visual-only or visual + indicators,
- [ ] legend wording approved.

## Recommended first build

A visual composite map with:

- four district outlines,
- Ackerland / Grünland / Dauerkultur if available,
- Moor-/Feuchtbodenkontext,
- highlighted intersection Nutzung × Bodenkontext,
- compact legend,
- clear method note.

## Do not

- call the map an Eignungskarte,
- call the intersection Wiedervernässungspotenzial,
- imply farm-level affectedness,
- display confidential parcel/farm data,
- add the map to the website before visual and method review.
"""
    write(TASK_B95, task_b95)

    done_entry = f"""
## B94 - Source-anchor Oberschwaben map workflow ({today})

- Created `docs/B94_oberschwaben_source_stack.md`.
- Created `docs/B94_oberschwaben_source_stack.csv`.
- Created `docs/B94_oberschwaben_data_access_questions.md`.
- Created `docs/B94_oberschwaben_legend_and_map_logic.md`.
- Created `docs/B94_oberschwaben_flyer_map_reference_note.md`.
- Created `tasks/B95_build_oberschwaben_map_assets.md`.
- Anchored the Oberschwaben map workflow to the SOLAMO flyer source-stack logic.
- Did not modify production HTML, CSS, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B94 - Source-anchor Oberschwaben map workflow" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B94 source-anchor Oberschwaben map workflow complete.")
    print("Changed/created:")
    for path in [SOURCE_STACK_MD, SOURCE_STACK_CSV, DATA_QUESTIONS, LEGEND_LOGIC, FLYER_NOTE, TASK_B95, DONE]:
        print(f"  {rel(path)}")


if __name__ == "__main__":
    main()
