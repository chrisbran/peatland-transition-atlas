# B15d — Stable GPM 2.0 Sticky-Story Overlay

Date: 2026-06-18

## Problem

The first B15c implementation replaced the sticky-story visual stage content directly. The original scrolly renderer also writes to that stage during scroll/intersection updates. This caused a visible flicker: the GPM image appeared briefly and was then overwritten by the canonical renderer.

## Fix

The new implementation does not mutate the stage content. Instead, it creates a stable overlay above the existing story visual and toggles it only during the Global/Europe peatland-context steps.

## Files changed

- `src/gpm2_context_images.js`
- `src/styles.css`
- `docs/B15d_fix_gpm2_context_flicker.md`
- `tasks/done.md`

## Data assets

- `public/images/gpm2_global_context.png`
- `public/images/gpm2_europe_context.png`

## Interpretation boundary

The GPM 2.0 images remain context layers, not local planning or rewetting-suitability layers.
