# B11c — Baden-Württemberg BK50-Moor Preview Map

Date: 2026-06-18

## Purpose

Add the first regional peat/organic-soils spatial layer to the public atlas.

## Input

`public/data/bw_bk50_moor_simplified.geojson`

## Added interface

The new section `#bwPeatLayer` shows:

- a simplified BK50-Moor SVG map,
- feature count,
- class count,
- source area sum,
- class legend,
- hover/click detail display,
- interpretation caveat.

## Interpretation boundary

The map shows a regional medium-scale soil-context layer for Baden-Württemberg. It is not a local rewetting suitability map and should not be interpreted as parcel-level planning guidance.

## Technical approach

- no external mapping library,
- no build system,
- automatic bounding-box fitting,
- SVG polygon rendering,
- class-based color assignment from `properties.class`.

## Next step

Use this regional layer as the final zoom target in the planned sticky-scroll story.
