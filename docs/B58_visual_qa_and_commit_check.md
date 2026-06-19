# B58 - Visual QA and Commit Check

Date: 2026-06-19

## 1. Required map PNGs

- OK `public/maps/global/global_gpm2_peat_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/global/global_hotspots_total.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/global/global_hotspots_density.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/global/global_country_borders.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/europe/europe_gpm2_peat_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/europe/europe_country_borders.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/germany/germany_admin_context.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/germany/germany_thuenen_moor_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/germany/germany_thuenen_moor_types.png` — PNG header RGBA (1600, 900) bit_depth=8

## 2. Required central-story scripts

- OK `src/central_global_map_story.js`
- OK `src/central_layer_state_hardener.js`
- OK `src/central_step_state_bridge.js`
- OK `src/central_stage_label_fix.js`

## 3. index.html reference check

- OK no broken local script/image references detected

## 4. Central story states

- OK `europe-borders`
- OK `europe-peat`
- OK `germany-context`
- OK `germany-thuenen-extent`
- OK `germany-thuenen-types`

## 5. Unwanted reference check

- OK `germany_thuenen_legend_fix.js` not found in active files
- OK `B53_germany_thuenen_distinction_and_legend_fix` not found in active files
- OK `EUROPE_FRAME_V1.png` not found in active files

## 6. Git status / commit hygiene

- WARN raw-data/GIS-like files visible in git status:
  - `?? data/external/`

### Current changed/untracked files

- ` M index.html`
- ` M src/central_global_map_story.js`
- ` M src/central_step_state_bridge.js`
- ` M tasks/done.md`
- `?? data/external/`
- `?? data/metadata/peat_soils_source_catalog.csv`
- `?? docs/B10_peat_soils_data_source_inventory.md`
- `?? docs/B11a_bk50_moor_source_acquisition.md`
- `?? docs/B14a_germany_organic_soils_source_acquisition.md`
- `?? docs/B14b_germany_organic_soils_web_layer_method.md`
- `?? docs/B15c_bind_gpm2_context_images_to_sticky_story.md`
- `?? docs/B15d_fix_gpm2_context_flicker.md`
- `?? docs/B15e_fix_gpm2_overlay_exact_step.md`
- `?? docs/B17_link_transition_pathways_to_spatial_layers.md`
- `?? docs/B18a2_stabilize_scroll_driven_emissions_stage.md`
- `?? docs/B18a_scroll_driven_emissions_metric_story.md`
- `?? docs/B2_faostat_fetch_method.md`
- `?? docs/B56_fix_central_map_stage_label.md`
- `?? docs/B57_refine_germany_thuenen_story_text.md`
- `?? docs/B58_visual_qa_and_commit_check.md`
- `?? docs/B60_patch_b58_no_pillow_png_check_v2.md`
- `?? docs/B6c_ranking_map_linking.md`
- `?? public/maps/europe/README.md`
- `?? scripts/04_add_hotspot_ranking_layer.py`
- `?? scripts/10_link_rankings_and_map.py`
- `?? scripts/16_create_peat_soils_source_inventory.py`
- `?? scripts/17_prepare_bk50_moor_layer_workflow.py`
- `?? scripts/18_build_bk50_moor_web_layer_from_geojson.py`
- `?? scripts/22_prepare_germany_organic_soils_workflow.py`
- `?? scripts/23_build_germany_organic_soils_web_layer_from_geojson.py`
- `?? scripts/30_bind_gpm2_context_images_to_sticky_story.py`
- `?? scripts/31_fix_gpm2_context_flicker.py`
- `?? scripts/32_fix_gpm2_overlay_exact_step.py`
- `?? scripts/34_link_transition_pathways_to_spatial_layers.py`
- `?? scripts/36_add_scroll_driven_emissions_metric_story.py`
- `?? scripts/37_stabilize_emissions_metric_scrolly_stage.py`
- `?? scripts/40_refine_central_global_map_contrast.py`
- `?? scripts/49_bind_germany_thuenen_frame_to_central_story.py`
- `?? scripts/56_fix_central_stage_label.py`
- `?? scripts/57_refine_germany_thuenen_story_text.py`
- `?? scripts/58_visual_qa_and_commit_check.py`
- `?? scripts/59_patch_b58_no_pillow_png_check.py`
- `?? scripts/60_patch_b58_no_pillow_png_check_v2.py`
- `?? src/central_stage_label_fix.js`
- `?? src/emissions_metric_scrolly.js`
- `?? tasks/B11_build_first_peat_soils_layer.md`
- `?? tasks/B11b_process_bk50_moor_web_layer.md`
- `?? tasks/B14b_process_germany_organic_soils_web_layer.md`
- `?? tasks/B16_transition_evidence_storyline_refinement.md`
- `?? tasks/B18b_unified_map_card_system.md`
- `?? tasks/B18c_global_callouts_and_metric_interpretation.md`
- `?? tasks/B18c_global_peat_hotspot_callouts.md`
- `?? tasks/B18d_global_callouts_and_metric_interpretation.md`
- `?? tasks/B19b_bind_europe_frame_to_sticky_story.md`
- `?? tasks/B2_run_faostat_export_workflow.md`
- `?? tasks/B7_prepare_phase_B_release.md`

## 7. Suggested add list for this milestone

- `index.html`
- `src/styles.css`
- `src/central_global_map_story.js`
- `src/central_layer_state_hardener.js`
- `src/central_step_state_bridge.js`
- `src/central_stage_label_fix.js`
- `public/maps/germany/README.md`
- `public/maps/germany/germany_admin_context.png`
- `public/maps/germany/germany_thuenen_moor_extent.png`
- `public/maps/germany/germany_thuenen_moor_types.png`
- `scripts/48_prepare_germany_thuenen_frame_workflow.py`
- `scripts/50_fix_germany_state_binding.py`
- `scripts/51_add_hard_central_layer_controller.py`
- `scripts/52_add_central_step_state_bridge.py`
- `scripts/54_restore_original_thuenen_legend_colors.py`
- `scripts/55_fix_thuenen_legend_inline_swatches.py`
- `scripts/56_fix_central_stage_label.py`
- `scripts/57_refine_germany_thuenen_story_text.py`
- `docs/B19c_germany_thuenen_frame_workflow.md`
- `docs/B50_fix_germany_state_binding.md`
- `docs/B51_hard_central_map_layer_controller.md`
- `docs/B52_central_step_state_bridge.md`
- `docs/B54_restore_original_thuenen_legend_colors.md`
- `docs/B55_fix_thuenen_legend_inline_swatches.md`
- `docs/B56_fix_central_map_stage_label.md`
- `docs/B57_refine_germany_thuenen_story_text.md`
- `tasks/done.md`

## Result

PASS WITH WARNINGS — review warnings before committing.

- Forbidden/raw-data-like files are visible in git status.
