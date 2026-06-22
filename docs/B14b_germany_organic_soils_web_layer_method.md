# B14b — Germany Organic-Soils Web Layer

Date: 2026-06-18

## Input

`data\external\peat_soils\germany_organic_soils\germany_organic_soils_wgs84.geojson`

The input is expected to be a GIS export of the Thünen/OpenAgrar Germany organic-soils polygon layer in EPSG:4326 / WGS84.

## Output

`public\data\germany_organic_soils_simplified.geojson`

## Processing

- read input GeoJSON,
- identify a class field using flexible field-name candidates,
- retain class, genesis, peat-depth and source-area information where available,
- simplify polygon geometry with Douglas-Peucker tolerance `0.002` degrees,
- export compact GeoJSON for GitHub Pages display,
- write class summary.

## Source

Thünen/OpenAgrar: Aktualisierte Kulisse organischer Böden in Deutschland.

## Interpretation boundary

This layer shows national organic-soils spatial context. It is not a local rewetting suitability map and should not be interpreted as parcel-level planning guidance.

## QA checks needed

- verify that the inferred `class` field is the intended classification field,
- verify whether the area field is in square metres or hectares,
- inspect the simplified output visually,
- check file size before deploying.
