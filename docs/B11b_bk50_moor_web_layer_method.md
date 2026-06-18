# B11b — Baden-Württemberg BK50-Moor Web Layer

Date: 2026-06-18

## Input

`data\external\peat_soils\bw_bk50_moor\bk50_moor_wgs84.geojson`

The input is expected to be a QGIS export of the BK50-Moor source layer in EPSG:4326 / WGS84.

## Output

`public\data\bw_bk50_moor_simplified.geojson`

## Processing

- read input GeoJSON,
- retain selected attributes,
- simplify polygon geometry with Douglas-Peucker tolerance `0.0008` degrees,
- export compact GeoJSON for GitHub Pages display,
- write class summary.

## Attribution

Datenquelle: Regierungspräsidium Freiburg - LGRB, www.lgrb-bw.de

License: Datenlizenz Deutschland - Namensnennung - Version 2.0

## Interpretation boundary

This layer shows the regional distribution of moor, moor-like and humus-rich groundwater soils according to BK50-Moor.

It is a medium-scale overview layer. It is not sufficient alone for local rewetting planning or parcel-level decisions.
