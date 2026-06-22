# B15e — Exact-State GPM 2.0 Overlay Fix

Date: 2026-06-18

## Problem

The previous GPM 2.0 sticky-story overlay inferred the active context image from visible text. During sticky scrolling, adjacent story cards can remain partially visible, so the Europe image appeared repeatedly as a placeholder-like overlay.

## Fix

`src/gpm2_context_images.js` now uses only explicit step data attributes:

- `data-story-state`
- `data-state`
- `data-key`
- `data-layer`

It no longer infers Global/Europe GPM states from text content.

## Expected behaviour

- GPM global image appears only on the explicit global/peat context state.
- GPM Europe image appears only on the explicit Europe context state.
- Overlay is hidden for emissions, Germany, Baden-Württemberg and transition-pathway states.

## If the images disappear completely

The story steps may not expose a matching data state. In that case, the next step is to inspect the story-step attributes and bind the images directly inside `src/scrolly_story_layers.js`.
