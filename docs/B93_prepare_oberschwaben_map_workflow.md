# B93 - Prepare Oberschwaben Map Workflow

Date: 2026-06-23

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
