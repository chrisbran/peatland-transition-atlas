# B8b — Projection Review and Robinson-Style Map Projection

Date: 2026-06-17

## Problem

The earlier hotspot map used a simple equirectangular projection. This was technically simple but visually exaggerated high-latitude countries and made the map look less cartographically credible.

## Decision

Implement a lightweight Robinson-style visual projection using the standard 5-degree coefficient table directly in JavaScript.

## Why this option?

- Keeps the atlas static and GitHub Pages compatible.
- Avoids adding a build system or heavy mapping library.
- Reduces high-latitude exaggeration compared with equirectangular display.
- Applies consistently to the hotspot layer and the base land layer.

## Implementation

The `project(coord)` function was replaced in:

- `src/hotspots.js`
- `src/hotspot_base_layer.js`

The projection is used only for SVG display. It is not a GIS-grade reprojection workflow.

## Remaining caveats

- The map remains country-level only.
- Small islands and fragmented archipelagos remain difficult to select.
- The projection is a visual approximation for an MVP atlas, not a scientific cartographic processing step.
- Area comparisons should still be interpreted cautiously.

## Next possible step

B8c — refine tooltip/details panel and selected-country styling.
