# B14d — Germany Organic-Soils Layer Bound to Sticky Story

Date: 2026-06-18

## Purpose

Replace the Germany placeholder in the sticky-scroll story with the real simplified Germany organic-soils layer.

## Input

`public/data/germany_organic_soils_simplified.geojson`

## Sticky story status after this step

| Step | Status |
|---|---|
| World emissions | Real country hotspot layer |
| Global peat/organic soils | Planned placeholder |
| Europe | Planned placeholder |
| Germany | Real organic-soils layer |
| Baden-Württemberg | Real BK50-Moor layer |
| Interpretation boundary | Caveat panel |

## Interpretation boundary

The Germany layer is a national organic-soils context layer. It is not a local rewetting suitability map.

## Technical approach

- no external map library,
- no build system,
- SVG rendering from simplified GeoJSON,
- bounding-box fit for Germany layer,
- class-based color assignment.
