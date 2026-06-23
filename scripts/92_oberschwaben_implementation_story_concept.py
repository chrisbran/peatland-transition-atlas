#!/usr/bin/env python3
"""
B92 - Oberschwaben implementation story concept

Purpose:
- Shift from visual polish to fachliche Weiterentwicklung.
- Define the next substantive module:
  Oberschwaben as regional implementation space for agricultural peatland transition.
- Translate SOLAMO-BW and LUBW/Moorschutzprogramm context into:
  story logic, map layers, indicators, methodological boundaries and next workflow.
- Do not modify the website yet.

Outputs:
- docs/B92_oberschwaben_implementation_story_concept.md
- docs/B92_oberschwaben_storyboard.md
- docs/B92_oberschwaben_layer_spec.csv
- docs/B92_oberschwaben_indicator_spec.csv
- tasks/B93_prepare_oberschwaben_map_workflow.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- alter maps/data/assets
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

CONCEPT = DOCS / "B92_oberschwaben_implementation_story_concept.md"
STORYBOARD = DOCS / "B92_oberschwaben_storyboard.md"
LAYER_SPEC = DOCS / "B92_oberschwaben_layer_spec.csv"
INDICATOR_SPEC = DOCS / "B92_oberschwaben_indicator_spec.csv"
TASK_B93 = TASKS / "B93_prepare_oberschwaben_map_workflow.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_layer_spec() -> None:
    rows = [
        {
            "layer_id": "oberschwaben_admin_context",
            "display_name": "Oberschwaben: Landkreisrahmen",
            "purpose": "Räumlichen Fokus der SOLAMO-Region zeigen.",
            "geometry": "polygon",
            "target_extent": "Ravensburg, Biberach, Sigmaringen, Bodenseekreis",
            "preferred_source": "NUTS/Landkreisgrenzen or existing admin boundaries; use only public/reusable geometry.",
            "map_role": "context",
            "legend_group": "Räumlicher Rahmen",
            "method_boundary": "Landkreisrahmen ist nur Darstellungs- und Aggregationsebene.",
            "output_png": "public/maps/oberschwaben/oberschwaben_admin_context.png",
            "priority": "required",
        },
        {
            "layer_id": "oberschwaben_agriculture",
            "display_name": "Landwirtschaftliche Nutzung",
            "purpose": "Landwirtschaftliche Nutzungskulisse innerhalb der vier Landkreise sichtbar machen.",
            "geometry": "polygon/raster",
            "target_extent": "Oberschwaben focus region",
            "preferred_source": "IACS/InVeKoS/GA if licensed; otherwise ATKIS/CORINE/LBM-DE fallback; source/license to be decided.",
            "map_role": "agricultural context",
            "legend_group": "Nutzung",
            "method_boundary": "Zeigt Nutzungskulisse, keine Betriebsebene und keine aktuelle Betroffenheit einzelner Betriebe.",
            "output_png": "public/maps/oberschwaben/oberschwaben_agriculture.png",
            "priority": "required",
        },
        {
            "layer_id": "oberschwaben_moor_context",
            "display_name": "Moor-/organische Boden-/Feuchtbodenkulisse",
            "purpose": "Regionalen Bodenkontext für Moor- und Feuchtbodenfragen zeigen.",
            "geometry": "polygon",
            "target_extent": "Oberschwaben focus region",
            "preferred_source": "BK50 as available; Moorkataster/organische Böden if accessible and usable; source hierarchy required.",
            "map_role": "soil/peat context",
            "legend_group": "Bodenkontext",
            "method_boundary": "Bodenkontext ist keine Eignungskarte, keine Priorisierung und keine Betroffenheitsanalyse.",
            "output_png": "public/maps/oberschwaben/oberschwaben_moor_context.png",
            "priority": "required",
        },
        {
            "layer_id": "oberschwaben_agri_moor_intersection",
            "display_name": "Landwirtschaft × Moor-/Feuchtbodenkontext",
            "purpose": "Räume markieren, in denen Moorschutz besonders zur landwirtschaftlichen Umsetzungsfrage wird.",
            "geometry": "polygon",
            "target_extent": "Oberschwaben focus region",
            "preferred_source": "Overlay agriculture layer with soil/peat context layer.",
            "map_role": "implementation signal",
            "legend_group": "Schnittmenge",
            "method_boundary": "Schnittmenge zeigt potenzielle räumliche Betroffenheit, nicht Wiedervernässungseignung.",
            "output_png": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
            "priority": "required",
        },
        {
            "layer_id": "oberschwaben_landuse_classes_on_moor",
            "display_name": "Nutzungstypen auf Moor-/Feuchtbodenkontext",
            "purpose": "Unterscheiden, ob Schnittmenge eher Grünland, Ackerland oder Dauerkultur betrifft.",
            "geometry": "polygon/tabular",
            "target_extent": "Oberschwaben focus region",
            "preferred_source": "Agricultural land use classification if licensed; otherwise coarser public land cover.",
            "map_role": "interpretation",
            "legend_group": "Nutzungstypen",
            "method_boundary": "Nutzungsklassen sind generalisiert; keine betriebliche Entscheidung ableiten.",
            "output_png": "public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png",
            "priority": "recommended",
        },
        {
            "layer_id": "oberschwaben_focus_labels",
            "display_name": "Regionale Orientierungspunkte",
            "purpose": "Karte lesbar machen: Landkreisnamen, wichtige Moorlandschaften, ggf. Wurzacher Ried/Federsee/Pfrunger-Burgweiler Ried.",
            "geometry": "point/text",
            "target_extent": "Oberschwaben focus region",
            "preferred_source": "Manual cartographic labels; no new analytical claim.",
            "map_role": "orientation",
            "legend_group": "Orientierung",
            "method_boundary": "Labels dienen der Orientierung, nicht der Priorisierung.",
            "output_png": "integrated in admin/context exports",
            "priority": "optional",
        },
    ]

    fields = [
        "layer_id",
        "display_name",
        "purpose",
        "geometry",
        "target_extent",
        "preferred_source",
        "map_role",
        "legend_group",
        "method_boundary",
        "output_png",
        "priority",
    ]
    with LAYER_SPEC.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_indicator_spec() -> None:
    rows = [
        {
            "indicator_id": "agri_area_total_ha",
            "label": "Landwirtschaftliche Fläche",
            "unit": "ha",
            "level": "Landkreis / Oberschwaben total",
            "formula": "sum agricultural land area",
            "purpose": "Größe der landwirtschaftlichen Nutzungskulisse zeigen.",
            "interpretation": "Kontextgröße, nicht Betroffenheit.",
            "risk": "Source/license and crop-class definitions must be documented.",
            "priority": "required",
        },
        {
            "indicator_id": "moor_context_area_ha",
            "label": "Moor-/Feuchtbodenkontext",
            "unit": "ha",
            "level": "Landkreis / Oberschwaben total",
            "formula": "sum peat/wetland/organic soil context area",
            "purpose": "Bodenkulisse quantifizieren.",
            "interpretation": "Räumlicher Bodenhinweis; keine Eignung.",
            "risk": "BK50/Moorkataster/organische Böden definitions differ.",
            "priority": "required",
        },
        {
            "indicator_id": "agri_moor_intersection_ha",
            "label": "Landwirtschaft × Moor-/Feuchtbodenkontext",
            "unit": "ha",
            "level": "Landkreis / Oberschwaben total",
            "formula": "area(agriculture ∩ moor_context)",
            "purpose": "Kernsignal für potenzielle landwirtschaftliche Umsetzungsbetroffenheit.",
            "interpretation": "Zeigt Räume, in denen Nutzung und Moorkontext zusammen betrachtet werden müssen.",
            "risk": "Still not a farm-level affectedness analysis.",
            "priority": "required",
        },
        {
            "indicator_id": "share_agri_on_moor_pct",
            "label": "Anteil Landwirtschaft auf Moor-/Feuchtbodenkontext",
            "unit": "%",
            "level": "Landkreis",
            "formula": "100 * agri_moor_intersection_ha / agri_area_total_ha",
            "purpose": "Relative Bedeutung je Landkreis zeigen.",
            "interpretation": "Vergleichsmaß für regionale Nähe von Landwirtschaft und Moorkontext.",
            "risk": "Sensitive to land-use data resolution.",
            "priority": "required",
        },
        {
            "indicator_id": "share_moor_under_agri_pct",
            "label": "Anteil Moorkontext mit landwirtschaftlicher Nutzung",
            "unit": "%",
            "level": "Landkreis",
            "formula": "100 * agri_moor_intersection_ha / moor_context_area_ha",
            "purpose": "Zeigt, ob Moorkontext eher landwirtschaftlich geprägt ist.",
            "interpretation": "Hilft zwischen Naturschutz-/Hydrologie- und Landwirtschaftsfrage zu unterscheiden.",
            "risk": "No statement about current drainage condition unless hydrology data included.",
            "priority": "recommended",
        },
        {
            "indicator_id": "landuse_mix_on_moor_pct",
            "label": "Nutzungsmix auf Moor-/Feuchtbodenkontext",
            "unit": "%",
            "level": "Landkreis",
            "formula": "share of grassland/cropland/permanent crops within agri_moor_intersection",
            "purpose": "Nutzungspfade besser einordnen.",
            "interpretation": "Grünland-dominiert ≠ automatisch Weidepfad; Acker-dominiert ≠ automatisch Paludikulturpfad.",
            "risk": "Requires reliable land-use classes.",
            "priority": "recommended",
        },
        {
            "indicator_id": "implementation_signal_class",
            "label": "Umsetzungssignal",
            "unit": "class",
            "level": "Landkreis / map cell",
            "formula": "rule-based combination of intersection area and relative share",
            "purpose": "Kommunikativ verständliche Einordnung schaffen.",
            "interpretation": "Low/medium/high implementation attention, not priority ranking.",
            "risk": "High risk of being misread as prioritisation; use only with clear wording.",
            "priority": "optional",
        },
    ]

    fields = [
        "indicator_id",
        "label",
        "unit",
        "level",
        "formula",
        "purpose",
        "interpretation",
        "risk",
        "priority",
    ]
    with INDICATOR_SPEC.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    concept = f"""# B92 - Oberschwaben Implementation Story Concept

Date: {today}

## 1. Strategic shift

The website has a working German presentation version. The next step is no longer design polish. The next step is a substantive regional implementation module.

Current story:

```text
Global relevance -> Europe -> Germany -> Baden-Württemberg -> BK50 soil context
```

Next story layer:

```text
Baden-Württemberg -> Oberschwaben -> agriculture x peat/organic/wetland soil context -> farm affectedness -> use concepts -> value chains -> policy instruments
```

## 2. Core thesis

**Oberschwaben zeigt, dass Moorschutz nicht an der Moorgrenze endet. Er wird dort zur Umsetzungsfrage, wo Moorboden, landwirtschaftliche Nutzung, Betriebe, Wasserstand, Wertschöpfung und Förderung zusammen betrachtet werden müssen.**

## 3. Why Oberschwaben

The SOLAMO-BW flyer defines the project focus as the analysis and assessment of use concepts for rewetting peatlands in Baden-Württemberg's Oberschwaben region, specifically the districts Ravensburg, Biberach, Sigmaringen and Bodenseekreis.

The same project logic is highly compatible with the page's existing endpoint:

- affected agricultural farms,
- alternative use concepts,
- exchange with farmers, authorities and companies,
- interviews and workshops,
- future scenarios and value chains,
- economic modelling,
- climate performance and farm-level economic consequences,
- policy recommendations.

## 4. Why the existing BW/BK50 endpoint is not enough

The current BK50/BW map shows a regional soil and wetland context. That is useful, but incomplete.

It does not answer:

- Which parts of the regional soil context are agriculturally used?
- Which districts carry the strongest overlap between agriculture and peat/wetland soil context?
- Which land-use types dominate that overlap?
- Where does the question become a farm and value-chain problem?
- Which instruments would be needed to make transition feasible?

Therefore the next analytical object is not simply a moor map.

The next analytical object is:

**Landwirtschaftliche Nutzung auf Moor-/organischem Boden-/Feuchtbodenkontext in Oberschwaben.**

## 5. Proposed map module

Working title:

**Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird**

Map sequence:

1. `Oberschwaben: Landkreisrahmen`
2. `Landwirtschaftliche Nutzung`
3. `Moor-/organische Boden-/Feuchtbodenkulisse`
4. `Schnittmenge Landwirtschaft × Moor-/Feuchtbodenkontext`
5. optional: `Nutzungstypen auf Moor-/Feuchtbodenkontext`

This should initially be a static map module, not an interactive dashboard.

## 6. Suggested narrative section

Place after the current central map story and before or inside the existing regional implementation section.

Suggested text:

```text
Oberschwaben zeigt die praktische Herausforderung.

In den Landkreisen Ravensburg, Biberach, Sigmaringen und dem Bodenseekreis treffen Moor- und Feuchtbodenkontexte auf intensive landwirtschaftliche Nutzung. Damit wird Moorschutz nicht nur zur Frage des Wasserstands, sondern zur Frage betrieblicher Betroffenheit, möglicher Nutzungspfade, Wertschöpfungsketten und Förderinstrumente.
```

Follow-up:

```text
Die Karte zeigt keine Eignung und keine Priorität. Sie markiert Räume, in denen landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext gemeinsam betrachtet werden müssen.
```

## 7. Map interpretation logic

The regional map should answer four questions:

### 1. Where is the soil context?

Where do peat, organic or wetland soil contexts occur in the four SOLAMO districts?

### 2. Where is the agricultural use context?

Where is agricultural land use located within the same regional frame?

### 3. Where do both overlap?

Where does the transition problem become a land-use and farm affectedness question?

### 4. What does this imply?

Which transition pathways are plausible enough to discuss, without claiming suitability?

Possible interpretation categories:

- `Schützen und stabilisieren`
- `Wiedervernässen und extensivieren`
- `Nasse Nutzung entwickeln`
- `Nutzung und Flächenorganisation neu ordnen`
- `Förder- und Wertschöpfungsketten prüfen`

## 8. Data hierarchy

Preferred data hierarchy:

1. Best available official or project-compatible soil/moor layer
2. Best available official agricultural land-use layer
3. County boundaries for the four SOLAMO districts
4. Derived intersection layer
5. Aggregated district indicators

Do not use confidential farm-level data for the public prototype.

## 9. Method boundaries

The regional module must explicitly avoid overclaiming.

Never write:

- suitable for rewetting,
- priority area,
- affected farm,
- recommended intervention,
- profitable use concept,
- SOLAMO result.

Preferred wording:

- regional context,
- land-use and soil-context overlap,
- possible implementation attention,
- potential farm affectedness,
- transition question,
- basis for further analysis.

## 10. Relation to LUBW Moorschutzprogramm

The LUBW Moorschutzprogramm provides the state-level framework for moor protection, renaturation, planning and implementation. It is useful as the policy and planning context.

Relevant conceptual anchors:

- Moorschutzkonzeption bundles sectoral goals and instruments.
- Moor protection is linked to nature conservation, soil protection, climate protection, water management, agriculture and forestry.
- The Moorkataster is a key information basis.
- Implementation requires regional prioritisation, coordination, funding and stakeholder involvement.

## 11. Relation to SOLAMO-BW

SOLAMO-BW provides the socio-economic implementation logic.

Relevant conceptual anchors:

- farm affectedness,
- regional farm patterns,
- alternative use concepts,
- interviews,
- stakeholder workshops,
- value chains,
- economic modelling,
- climate performance,
- farm-level consequences,
- policy recommendations.

## 12. Recommended page evolution

Next visible page evolution:

```text
Current:
Problem -> Kartenfolge -> Regionale Umsetzung -> Pfade -> Methode

Future:
Problem -> Kartenfolge -> Oberschwaben implementation map -> Betroffenheit -> Nutzungspfade -> Politik-/Förderfrage -> Methode
```

## 13. Recommended next technical step

B93 should prepare the map workflow, not bind anything to the website yet.

B93 should create:

- `public/maps/oberschwaben/README.md`
- export specifications for 16:9 PNGs
- layer naming convention
- required data checklist
- ArcGIS/QGIS workflow
- expected output PNG names
- QA checks for PNG size/alpha/reference
"""

    storyboard = f"""# B92 - Oberschwaben Storyboard

Date: {today}

## Storyboard goal

Turn the current Baden-Württemberg endpoint into a concrete regional implementation story.

## Module title

**Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird**

## Position on page

After central map story and before current `Regionale Umsetzung` cards.

## Scroll or static?

Start static.

Do not build a new sticky scrolly yet.

## Proposed module structure

### Block 1 - Transition sentence

```text
Der regionale Bodenkontext ist erst der Anfang. In Oberschwaben entscheidet sich, wo Moor- und Feuchtbodenkontexte auf landwirtschaftliche Nutzung, Betriebe und Wertschöpfung treffen.
```

### Block 2 - Map

One composite map:

- four district outlines,
- agriculture,
- peat/wetland/organic soil context,
- intersection layer highlighted,
- simple legend.

### Block 3 - Three interpretation cards

#### Karte zeigt Kontext

```text
Die Karte markiert Räume, in denen landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext zusammenfallen.
```

#### Daraus entsteht Betroffenheit

```text
Erst aus der Überschneidung von Fläche, Nutzung und Betriebsstruktur wird eine Umsetzungsfrage.
```

#### Daraus folgen Nutzungspfade

```text
Mögliche Pfade reichen von Schutz und Stabilisierung über Wiedervernässung bis zu nasser Nutzung und Wertschöpfungsketten.
```

### Block 4 - SOLAMO bridge

```text
Hier setzt SOLAMO-BW an: Betroffenheit erfassen, Nutzungskonzepte prüfen, Wertschöpfungsketten mit regionalen Akteuren bewerten und Politikempfehlungen ableiten.
```

### Block 5 - Method boundary

```text
Die Darstellung ist keine Eignungskarte und keine Priorisierung. Sie zeigt den räumlichen Ausgangspunkt für weitere sozio-ökonomische und betriebliche Analysen.
```

## Optional second-stage scroll version

After the static map is accepted, convert into four steps:

1. `Landkreisrahmen`
2. `Landwirtschaftliche Nutzung`
3. `Moor-/Feuchtbodenkontext`
4. `Schnittmenge und Umsetzungsfrage`

Do not implement this before the data and map design are settled.
"""

    task_b93 = f"""# B93 - Prepare Oberschwaben Map Workflow

Created from B92 on {today}

## Goal

Prepare the cartographic workflow for a new Oberschwaben implementation module.

## Required outputs

Create:

- `public/maps/oberschwaben/README.md`
- `docs/B93_prepare_oberschwaben_map_workflow.md`
- possibly `scripts/93_prepare_oberschwaben_map_workflow.py`

Expected future PNGs:

```text
public/maps/oberschwaben/oberschwaben_admin_context.png
public/maps/oberschwaben/oberschwaben_agriculture.png
public/maps/oberschwaben/oberschwaben_moor_context.png
public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png
public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png
```

## Required decisions before map export

1. Which agriculture layer is legally and technically usable?
2. Which soil/moor context layer is preferred?
   - BK50?
   - Moorkataster?
   - Thünen organic soils?
   - another official layer?
3. Should the first map use only the four SOLAMO counties or a broader visual frame?
4. Should the map show exact polygons or generalized/simplified patterns?
5. Which indicators can be calculated without farm-level data?

## Suggested map frame

- Region: Ravensburg, Biberach, Sigmaringen, Bodenseekreis
- Projection: same or compatible with BW export frame
- Output: 1600 x 900 px PNG
- Transparent background: yes, if used as layer stack
- White/warm background: yes, if used as standalone map card
- Keep legend simple.

## Method boundary

All exports must carry this note in documentation:

> Die Oberschwaben-Karten zeigen eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
"""
    write(CONCEPT, concept)
    write(STORYBOARD, storyboard)
    write(TASK_B93, task_b93)
    write_layer_spec()
    write_indicator_spec()

    done_entry = f"""
## B92 - Oberschwaben implementation story concept ({today})

- Created `docs/B92_oberschwaben_implementation_story_concept.md`.
- Created `docs/B92_oberschwaben_storyboard.md`.
- Created `docs/B92_oberschwaben_layer_spec.csv`.
- Created `docs/B92_oberschwaben_indicator_spec.csv`.
- Created `tasks/B93_prepare_oberschwaben_map_workflow.md`.
- Shifted next development from visual polish to a regional implementation module.
- Did not modify production HTML, CSS, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B92 - Oberschwaben implementation story concept" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B92 Oberschwaben implementation story concept complete.")
    print("Changed/created:")
    for path in [CONCEPT, STORYBOARD, LAYER_SPEC, INDICATOR_SPEC, TASK_B93, DONE]:
        print(f"  {rel(path)}")


if __name__ == "__main__":
    main()
