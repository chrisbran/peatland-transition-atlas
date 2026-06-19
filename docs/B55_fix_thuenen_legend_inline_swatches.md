# B55 - Fix Thuenen Legend Inline Swatches

Date: 2026-06-19

## Issue

The original central legend showed the Thuenen soil-type labels, but the associated color swatches remained invisible. B54 attempted to style the existing `legend-thuenen-*` classes via CSS, but the active legend markup/CSS did not expose the swatches correctly.

## Fix

This patch keeps the original central legend and replaces the collapsed `<i class="legend-thuenen-*"></i>` markers in JavaScript legend templates with robust inline swatch markup.

No extra floating legend is created.

## Files patched

- `src/central_step_state_bridge.js`
- `src/central_global_map_story.js` if matching legend markup exists
- `src/central_layer_state_hardener.js` if matching legend markup exists
- `src/styles.css`

## Expected result

- Original legend remains in its previous position.
- Soil-type labels remain.
- Each label now has a visible color swatch.
