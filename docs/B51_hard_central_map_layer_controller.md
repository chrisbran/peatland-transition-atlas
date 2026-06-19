# B51 - Hard Central Map Layer Controller

Date: 2026-06-19

## Issue

Germany PNG layers were visible on Europe/global states. The previous script inserted HTML and attempted CSS/metadata binding, but the existing central story controller still allowed Germany layers to remain visible across states.

## Fix

This patch adds `src/central_layer_state_hardener.js`, loaded after `src/central_global_map_story.js`.

The hardener:

- observes `.central-map-story[data-state]`
- force-hides all known central map layers
- then explicitly shows only the layers belonging to the active state
- applies opacity using `style.setProperty(..., "important")`

## Supported states

- `extent`
- `total`
- `density`
- `compare`
- `europe-borders`
- `europe-peat`
- `germany-context`
- `germany-thuenen-extent`
- `germany-thuenen-types`

## Browser debug helper

In the browser console, a state can be forced manually:

```javascript
window.__applyCentralMapState("europe-peat")
window.__applyCentralMapState("germany-thuenen-types")
```

## Acceptance check

- Europe map states no longer show Germany overlays.
- Germany states show only their intended layers.
- Global states still work.
