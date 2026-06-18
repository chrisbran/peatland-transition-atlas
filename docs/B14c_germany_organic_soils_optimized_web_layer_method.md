# B14c — Optimized Germany Organic-Soils Web Layer

Date: 2026-06-18

## Input

`data\external\peat_soils\germany_organic_soils\germany_organic_soils_wgs84.geojson`

The input is expected to be an ArcGIS-dissolved and simplified GeoJSON export of the Germany organic-soils layer.

## Output

`public\data\germany_organic_soils_simplified.geojson`

## Processing

- read dissolved GeoJSON,
- detect class fields including `KAT_KURZ` and `KAT_LANG`,
- detect area fields including `SUM_AREA_HA` and `AREA_HA`,
- apply additional web-only Douglas-Peucker simplification with tolerance `0.01` degrees,
- export compact GeoJSON for GitHub Pages display,
- write class summary.

## Vertex reduction

- vertices before Python simplification: 86388
- vertices after Python simplification: 79872

## Interpretation boundary

This layer is a national organic-soils context layer for scrollytelling. It is not a local rewetting suitability map and should not be used for parcel-level planning.
