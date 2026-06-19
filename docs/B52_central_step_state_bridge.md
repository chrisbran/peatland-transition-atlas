# B52 - Central Step State Bridge

Date: 2026-06-19

## Issue

After adding the hard layer controller, the Germany layers disappeared because the central map story's `data-state` was not updated when the newly inserted Germany steps became active.

The text card could move to a Germany step while the map stage remained in a previous Europe state.

## Fix

This patch adds `src/central_step_state_bridge.js`.

The bridge:

- observes all `.central-map-step[data-global-state]` elements
- sets `.central-map-story[data-state]` to the active step's state
- calls `window.__applyCentralMapState(state)` from the hard layer controller if available
- includes fallback scroll-position logic
- updates common metadata/legend fields if matching elements exist

## Expected result

- Europe steps show Europe layers.
- Germany steps show Germany layers.
- Germany layers no longer overlay Europe/global states.
- Germany no longer disappears when its steps are active.
