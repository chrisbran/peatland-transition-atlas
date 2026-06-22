# B66 - Retire guidedStory Script Tags Phase 1

Date: 2026-06-22

## 1. Purpose

B66 removes script tags for the old guided scroll story after B64 retired `#guidedStory` from the visible page flow and B65 classified the corresponding scripts as retire candidates.

This is a reversible cleanup step.

## 2. Changed files

- `index.html`
- `docs/B66_retire_guided_story_scripts_phase1.md`
- `tasks/done.md`

## 3. Removed from `index.html`

- `src/scrolly_story.js`
- `src/scrolly_story_layers.js`
- `src/gpm2_context_images.js`

## 4. Target scripts already absent

- none

## 5. Not deleted

The following files are not deleted by B66:

- `src/scrolly_story.js`
- `src/scrolly_story_layers.js`
- `src/gpm2_context_images.js`
- `public/data/germany_organic_soils_simplified.geojson`
- `public/data/bw_bk50_moor_simplified.geojson`
- `public/images/gpm2_global_context.png`
- `public/images/gpm2_europe_context.png`

## 6. Scripts intentionally kept

- `src/app.js`
- `src/hotspots.js`
- `src/hotspot_base_layer.js`
- `src/bw_peat_layer.js`
- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`

## 7. Required visual QA

After B66, verify locally:

1. The retired `guidedStory` remains hidden.
2. The central PNG sticky story still works through all states.
3. The hotspot explorer still renders.
4. The evidence map still renders.
5. The pathway and South Germany fit sections still render.
6. The BW interactive layer still renders if retained.
7. There are no console errors caused by missing old guidedStory scripts.

## 8. Next step

Recommended B67:

`B67_legacy_asset_retirement_decision`

Scope:

- Decide whether to keep or retire `bwPeatLayer`.
- Decide whether old `public/images/gpm2_*` and old guidedStory GeoJSON-only dependencies should remain as archived assets or be removed from the public build.
- Update QA so BW PNGs and BW states are explicitly checked.
