# B6b-fix — Hotspot Legend Visibility

Date: 2026-06-17

## Problem

The hotspot choropleth legend was present but visually weak/non-functional because the map color classes used SVG `fill`, while the legend swatches are normal HTML elements.

SVG paths respond to `fill`. HTML swatches need `background`.

## Change

Added explicit `background` colors for:

- `.legend-item i.map-fill-1`
- `.legend-item i.map-fill-2`
- `.legend-item i.map-fill-3`
- `.legend-item i.map-fill-4`
- `.legend-item i.map-fill-5`

Also added a subtle legend container background and border.

## Status

Visual fix only. No data-processing changes.
