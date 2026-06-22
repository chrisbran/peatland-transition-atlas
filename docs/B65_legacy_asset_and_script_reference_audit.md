# B65 - Legacy Asset and Script Reference Audit

Date: 2026-06-22

## 1. Purpose

B65 audits legacy scripts, public data files, public images and public map assets after B64 story-flow cleanup.

This is an audit-only step. No application section, script tag, data file or asset is removed by this patch.

## 2. Current section inventory

- `story` — visible — Introductory story overview; candidate to compress or merge into transitionLogic.
- `transitionLogic` — visible — Conceptual chain: Extent -> Pressure -> Implementation -> Pathways.
- `guidedStory` — retired / hidden — Retired B64 section; old scroll-driven story system.
- `layerProvenance` — visible — Layer-reading note; keep but likely shorten/reposition.
- `centralGlobalMapStory` — visible — Main PNG-based atlas story; do not touch in cleanup.
- `pathwayEvidenceMatrix` — visible — Bridge from spatial pressure to transition pathways.
- `hotspots` — visible — Country-level pressure explorer; keep as evidence explorer.
- `map` — visible — Evidence nodes / region examples; keep if supporting evidence remains useful.
- `pathways` — visible — Transition pathway cards; keep but group with evidence/pathway interpretation.
- `fit` — visible — South Germany fit matrix; keep but strengthen relation to BW endpoint.
- `methodology` — visible — Method / limitations; keep.
- `data` — visible — Prototype datasets; keep.
- `bwPeatLayer` — visible — Old BW GeoJSON interactive layer; review after central BW PNG story is stable.

## 3. Scripts loaded by `index.html`

- `src/app.js` — Evidence/pathways/fit/data app logic.
- `src/hotspots.js` — Country hotspot table/map interaction.
- `src/hotspot_base_layer.js` — Base country layer for hotspot map.
- `src/bw_peat_layer.js` — Old interactive BW BK50 GeoJSON map section.
- `src/scrolly_story.js` — Old guidedStory scroll-state driver.
- `src/scrolly_story_layers.js` — Old guidedStory GeoJSON layer renderer.
- `src/gpm2_context_images.js` — Old guidedStory image context renderer.
- `src/central_global_map_story.js` — Main central PNG map story metadata/controller.
- `src/central_layer_state_hardener.js` — Authoritative central PNG layer opacity controller.
- `src/central_step_state_bridge.js` — Central story step-state bridge.
- `src/central_stage_label_fix.js` — Central story label synchronizer.

## 4. Initial script classification

### Keep

- `src/app.js` — required while evidence/pathway/fit/data sections stay visible.
- `src/hotspots.js` — required while the country hotspot explorer stays visible.
- `src/hotspot_base_layer.js` — required by the country hotspot map base.
- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`
- `src/styles.css` ? main stylesheet linked by `index.html`; keep.

### Review

- `src/bw_peat_layer.js` — Old interactive BW BK50 GeoJSON map section.
- `src/emissions_metric_scrolly.js` — Untracked/legacy emissions metric scrolly module; review.

### Retire candidates

- `src/gpm2_context_images.js` — Old guidedStory image context renderer.
- `src/scrolly_story.js` — Old guidedStory scroll-state driver.
- `src/scrolly_story_layers.js` — Old guidedStory GeoJSON layer renderer.

Interpretation: these scripts appear tied to the old guided scroll story that B64 has hidden. They should not be deleted yet. B66 should first remove their script tags only if local visual QA confirms no visible section depends on them.

## 5. Initial asset classification

### Retire candidates

- `public/data/germany_organic_soils_simplified.geojson` — Appears tied to old guidedStory GeoJSON renderer; verify after script-tag audit.
- `public/images/gpm2_europe_context.png` — Likely old guidedStory image context; central PNG map stack now uses public/maps.
- `public/images/gpm2_global_context.png` — Likely old guidedStory image context; central PNG map stack now uses public/maps.

### Review

- `public/data/bw_bk50_moor_simplified.geojson` — Used by old BW interactive layer and old guidedStory; central BW PNG story reduces need.
- `public/data/papers.csv` — Public data file; check whether it is linked as dataset, loaded by JS, or only legacy.
- `public/data/transition_pathways.csv` — Public data file; check whether it is linked as dataset, loaded by JS, or only legacy.

### Unreferenced in active code scan

- `public/data/atlas_story_sections.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/atlas_story_sections_data_dictionary.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/atlas_wireframes.json` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/country_hotspots_n2o.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/country_hotspots_schema.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/papers_data_dictionary.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/region_case_studies.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/region_case_studies_data_dictionary.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/data/transition_pathways_data_dictionary.csv` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/maps/bw/README.md` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/maps/europe/README.md` — No reference found in index.html or src/*.js/css; do not delete until reviewed.
- `public/maps/germany/README.md` — No reference found in index.html or src/*.js/css; do not delete until reviewed.

Unreferenced does not automatically mean safe to delete. Some files are linked only from documentation, generated for future use, or intentionally retained as provenance.

## 6. Do not touch in B66

Do not touch the central PNG story map stack:

- `public/maps/global/`
- `public/maps/europe/`
- `public/maps/germany/`
- `public/maps/bw/`

Do not touch the central story controller stack:

- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`
- `src/styles.css` ? main stylesheet linked by `index.html`; keep.

## 7. Proposed B66 scope

Recommended B66 title:

`B66_retire_guided_story_scripts_phase1`

Recommended B66 scope:

1. Keep `guidedStory` hidden.
2. Remove script tags for old guided-story drivers only after confirming they are not needed:
   - `src/scrolly_story.js`
   - `src/scrolly_story_layers.js`
   - `src/gpm2_context_images.js`
3. Do not delete the JS files yet.
4. Do not delete GeoJSON or image assets yet.
5. Run local visual QA and confirm that:
   - central PNG story still works,
   - hotspot explorer still works,
   - evidence map still works,
   - pathway and South Germany fit sections still render.

## 8. Generated inventory files

- `docs/B65_reference_inventory.csv`
- `docs/B65_referenced_assets.txt`

## 9. Git hygiene note

`git status --short` at audit time:

```text
M docs/B58_visual_qa_and_commit_check.md
 M tasks/done.md
?? data/external/
?? data/metadata/peat_soils_source_catalog.csv
?? docs/B65_legacy_asset_and_script_reference_audit.md
?? docs/B65_reference_inventory.csv
?? docs/B65_referenced_assets.txt
?? public/maps/bw/README.md
?? public/maps/europe/README.md
?? scripts/04_add_hotspot_ranking_layer.py
?? scripts/10_link_rankings_and_map.py
?? scripts/16_create_peat_soils_source_inventory.py
?? scripts/17_prepare_bk50_moor_layer_workflow.py
?? scripts/18_build_bk50_moor_web_layer_from_geojson.py
?? scripts/22_prepare_germany_organic_soils_workflow.py
?? scripts/23_build_germany_organic_soils_web_layer_from_geojson.py
?? scripts/30_bind_gpm2_context_images_to_sticky_story.py
?? scripts/31_fix_gpm2_context_flicker.py
?? scripts/32_fix_gpm2_overlay_exact_step.py
?? scripts/34_link_transition_pathways_to_spatial_layers.py
?? scripts/36_add_scroll_driven_emissions_metric_story.py
?? scripts/37_stabilize_emissions_metric_scrolly_stage.py
?? scripts/40_refine_central_global_map_contrast.py
?? scripts/49_bind_germany_thuenen_frame_to_central_story.py
?? scripts/61_prepare_bw_regional_frame_workflow.py
?? scripts/62_bind_bw_extent_frame_to_central_story.py
?? scripts/62_bind_bw_extent_frame_to_central_story_fixed.py
?? scripts/62_repair_bw_extent_state_binding.py
?? scripts/65_legacy_asset_and_script_reference_audit.py
?? src/emissions_metric_scrolly.js
?? tasks/B11_build_first_peat_soils_layer.md
?? tasks/B11b_process_bk50_moor_web_layer.md
?? tasks/B14b_process_germany_organic_soils_web_layer.md
?? tasks/B16_transition_evidence_storyline_refinement.md
?? tasks/B18b_unified_map_card_system.md
?? tasks/B18c_global_callouts_and_metric_interpretation.md
?? tasks/B18c_global_peat_hotspot_callouts.md
?? tasks/B18d_global_callouts_and_metric_interpretation.md
?? tasks/B19b_bind_europe_frame_to_sticky_story.md
?? tasks/B2_run_faostat_export_workflow.md
?? tasks/B62_bind_bw_regional_frame_to_central_story.md
?? tasks/B7_prepare_phase_B_release.md
```
