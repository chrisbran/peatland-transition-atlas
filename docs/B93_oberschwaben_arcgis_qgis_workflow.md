# B93 - Oberschwaben ArcGIS/QGIS Workflow

Date: 2026-06-23

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
