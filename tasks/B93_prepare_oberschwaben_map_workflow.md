# B93 - Prepare Oberschwaben Map Workflow

Created from B92 on 2026-06-23

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
