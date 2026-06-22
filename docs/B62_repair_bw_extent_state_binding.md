# B62 repair — BW extent state binding

Date: 2026-06-22 13:43

## Purpose

Repairs the partial B62 state where BW image tags and story steps existed in `index.html`,
but the opacity/state controllers did not yet know `bw-context` and `bw-bk50-extent`.

## Scope

- Registers BW layers in `central_layer_state_hardener.js`.
- Adds BW metadata to `central_step_state_bridge.js`.
- Adds BW chip labels to `central_stage_label_fix.js`.
- Adds minimal CSS fallback rules in `styles.css`.
- Optionally extends `central_global_map_story.js` metadata if its structure allows robust insertion.

## Interpretation constraint

The BW extent is only a BK50 peat / wetland soil context layer. It does not imply agricultural use or rewetting suitability.
