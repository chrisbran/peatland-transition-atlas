# B56 - Fix Central Map Stage Label

Date: 2026-06-19

## Issue

After adding the Germany / Thuenen states, the small chip inside the central map stage could still read `EUROPEAN PEAT CONTEXT` while the Germany map and Germany text step were active.

## Fix

This patch adds `src/central_stage_label_fix.js`, loaded after the central step bridge.

The script observes `.central-map-story[data-state]` and updates the small map-stage chip according to the active state.

## Labels

- `extent` -> `GLOBAL PEAT CONTEXT`
- `total` -> `GLOBAL EMISSIONS PRESSURE`
- `density` -> `EMISSION DENSITY`
- `compare` -> `GLOBAL HOTSPOT INTERPRETATION`
- `europe-borders` -> `EUROPE FRAME`
- `europe-peat` -> `EUROPEAN PEAT CONTEXT`
- `germany-context` -> `GERMANY FRAME`
- `germany-thuenen-extent` -> `THUENEN KULISSE`
- `germany-thuenen-types` -> `MOOR AND SOIL TYPES`

## Acceptance check

When scrolling into the Germany / Thuenen steps, the map-stage chip should no longer remain stuck on `EUROPEAN PEAT CONTEXT`.
