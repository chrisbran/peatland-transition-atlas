# Oberschwaben map assets

Created by B93 on 2026-06-23.

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
