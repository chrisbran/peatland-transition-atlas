# B8a — Base Land Layer and Softer Hotspot Palette

Date: 2026-06-17

## Problem

The first functional hotspot map worked, but several visual issues were visible:

- ocean/background and non-hotspot land were hard to distinguish,
- the selected-country highlight was too bright/neon,
- countries without hotspot data did not appear as a neutral base layer,
- the map looked more like a data overlay floating on a dark background than a geographic map.

## Change

This patch adds a non-interactive Natural Earth 110m base-country layer behind the hotspot countries and softens the color palette.

## Files

- `public/data/world_countries_110m_base.geojson`
- `src/hotspot_base_layer.js`
- `src/styles.css`

## Technical approach

- no external JavaScript map library,
- no build system,
- dependency-free SVG enhancement,
- base layer is inserted behind existing hotspot SVG paths,
- MutationObserver re-inserts the base layer after metric-toggle map re-rendering.

## Interpretation boundary

The map remains a country-level screening layer. It still does not show local rewetting suitability.

## Remaining cartographic limitations

- the map still uses a simple equirectangular projection,
- high-latitude countries remain visually distorted,
- small islands and territories remain difficult to interact with.
