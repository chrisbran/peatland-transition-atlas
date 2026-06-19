# B50 - Fix Germany / Thuenen State Binding

Date: 2026-06-19

## Issue

Script 49 inserted Germany layers and steps into `index.html`, but the JavaScript metadata patch did not apply because the expected `STATE_META` closing marker was different in the current file.

This caused the Germany PNG layers to appear across other map states and overlay the Europe/global map.

## Fix

- Add robust CSS rules that hide Germany layers by default.
- Add Germany-specific show/hide rules for:
  - `germany-context`
  - `germany-thuenen-extent`
  - `germany-thuenen-types`
- Inject Germany state metadata into `src/central_global_map_story.js` via `Object.assign(STATE_META, ...)` before `function setState`.

## Acceptance check

- Europe steps no longer show Germany overlays.
- Germany steps correctly update the map title, legend, source text and layer stack.
- No duplicate Germany HTML blocks are created.
