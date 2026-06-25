# B58 - Visual QA and Commit Check

Date: 2026-06-25

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

- ` M docs/B58_visual_qa_and_commit_check.md`
- ` M index.html`
- ` M src/styles.css`
- ` M tasks/done.md`
- `?? _backup_before_clean_pre105_restore/`
- `?? _handoff_oberschwaben_restore.zip`
- `?? _handoff_oberschwaben_restore/`
- `?? data/external/`
- `?? data/metadata/peat_soils_source_catalog.csv`
- `?? data/working/`
- `?? design_dummies/`
- `?? docs/B103_public_text_audit_only.md`
- `?? docs/B103_public_text_findings.csv`
- `?? docs/B103_visible_text_extract.txt`
- `?? docs/B103_wording_frequency.csv`
- `?? docs/B103b_corrected_visible_text_audit.md`
- `?? docs/B103b_hidden_findings.csv`
- `?? docs/B103b_hidden_retired_text_extract.txt`
- `?? docs/B103b_visible_findings.csv`
- `?? docs/B103b_visible_text_extract_corrected.txt`
- `?? docs/B103b_wording_frequency.csv`
- `?? docs/B104_visible_wording_polish.md`
- `?? docs/B104_visible_wording_polish_audit.txt`
- `?? docs/B104b_second_visible_wording_and_oberschwaben_density.md`
- `?? docs/B104b_second_visible_wording_and_oberschwaben_density_audit.txt`
- `?? docs/B105_candidate_source_matrix.md`
- `?? docs/B105_fiona_public_safety_audit.txt`
- `?? docs/B105_source_swap_plan_and_fiona_safety_mode.md`
- `?? docs/B105r_restore_fiona_public_story_audit.txt`
- `?? docs/B105r_restore_fiona_public_story_state.md`
- `?? docs/B106_candidate_service_probe.csv`
- `?? docs/B106_lgl_basisdlm_capabilities_featuretypes.txt`
- `?? docs/B106_lgl_landnutzung_capabilities_featuretypes.txt`
- `?? docs/B106_source_probe.md`
- `?? docs/B106_source_probe_raw_snippets.txt`
- `?? docs/B107_lgl_landnutzung_candidate_value_counts.csv`
- `?? docs/B107_lgl_landnutzung_classification_trial.csv`
- `?? docs/B107_lgl_landnutzung_fields.csv`
- `?? docs/B107_lgl_landnutzung_probe_audit.txt`
- `?? docs/B107_lgl_landnutzung_sample_property_examples.csv`
- `?? docs/B107_lgl_landnutzung_sample_summary.md`
- `?? docs/B107_lgl_landnutzung_schema.md`
- `?? docs/B107b_lgl_landnutzung_candidate_agri_rows.csv`
- `?? docs/B107b_lgl_landnutzung_grid_sample_summary.md`
- `?? docs/B107b_lgl_landnutzung_grid_value_counts.csv`
- `?? docs/B107b_lgl_landnutzung_objectart_mapping_trial.csv`
- `?? docs/B107b_lgl_landnutzung_probe_audit.txt`
- `?? docs/B107c_lgl_landnutzung_mapping_audit.txt`
- `?? docs/B107c_lgl_landnutzung_mapping_draft.csv`
- `?? docs/B107c_lgl_landnutzung_mapping_review.md`
- `?? docs/B108_lgl_landnutzung_area_summary.csv`
- `?? docs/B108_lgl_landnutzung_bk50_intersection_area_summary.csv`
- `?? docs/B108_lgl_landnutzung_controlled_production_test.md`
- `?? docs/B108_lgl_landnutzung_download_manifest.csv`
- `?? docs/B108_lgl_landnutzung_public_numbers.txt`
- `?? docs/B108_lgl_landnutzung_qa.txt`
- `?? docs/B108b_lgl_dissolve_arcgis_notes.txt`
- `?? docs/B108b_lgl_dissolve_area_check.csv`
- `?? docs/B108b_lgl_dissolve_cartographic_layers.md`
- `?? docs/B108b_lgl_dissolve_qa.txt`
- `?? docs/B109a_arcgis_export_checklist.txt`
- `?? docs/B109a_arcgis_layer_manifest.csv`
- `?? docs/B109a_arcgis_lgl_oberschwaben_restyle_brief.md`
- `?? docs/B109a_arcgis_symbology_spec.csv`
- `?? docs/B76_static_design_dummies.md`
- `?? docs/B95d_fiona_wfs_direct_access_probe.md`
- `?? docs/B95f_fiona_wfs_post_namespace_probe.md`
- `?? docs/B98_oberschwaben_analysis_manifest.csv`
- `?? docs/B98_oberschwaben_county_landuse_area_summary.csv`
- `?? docs/B98_oberschwaben_intersection_area_qa.md`
- `?? docs/B98_oberschwaben_landuse_classification_qa.csv`
- `?? docs/B98a_oberschwaben_feature_class_inventory.csv`
- `?? docs/B98a_oberschwaben_feature_class_inventory.md`
- `?? docs/B98b_oberschwaben_counties_inventory.csv`
- `?? docs/B98b_prepare_oberschwaben_counties_from_gisco.md`
- `?? docs/B98c_oberschwaben_analysis_manifest.csv`
- `?? docs/B98c_oberschwaben_flagged_intersection_summary.csv`
- `?? docs/B98c_oberschwaben_intersection_classification_cleaned.csv`
- `?? docs/B98c_oberschwaben_intersection_classification_review.md`
- `?? docs/B98c_oberschwaben_public_safe_summary.csv`
- `?? docs/B99_reposition_transformations_after_oberschwaben.md`
- `?? docs/B99_transformations_public_readiness_audit.txt`
- `?? public/maps/bw/README.md`
- `?? public/maps/europe/README.md`
- `?? public/maps/oberschwaben_lgl/`
- `?? scripts/04_add_hotspot_ranking_layer.py`
- `?? scripts/103_public_text_audit_only.py`
- `?? scripts/103b_corrected_visible_text_audit.py`
- `?? scripts/104_visible_wording_polish.py`
- `?? scripts/104b_second_visible_wording_and_oberschwaben_density.py`
- `?? scripts/105_source_swap_plan_and_fiona_safety_mode.py`
- `?? scripts/105r_restore_fiona_public_story_state.py`
- `?? scripts/106_candidate_source_probe.py`
- `?? scripts/107_lgl_landnutzung_schema_and_oberschwaben_sample.py`
- `?? scripts/107b_lgl_landnutzung_grid_class_universe_probe.py`
- `?? scripts/107c_lgl_landnutzung_mapping_review.py`
- `?? scripts/108_lgl_landnutzung_controlled_production_test.py`
- `?? scripts/108b_lgl_dissolve_cartographic_layers.py`
- `?? scripts/109a_arcgis_lgl_oberschwaben_restyle_brief.py`
- `?? scripts/10_link_rankings_and_map.py`
- `?? scripts/110_external_source_register.py`
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
- `?? scripts/61_prepare_bw_regional_frame_workflow.py`
- `?? scripts/62_bind_bw_extent_frame_to_central_story.py`
- `?? scripts/62_bind_bw_extent_frame_to_central_story_fixed.py`
- `?? scripts/62_repair_bw_extent_state_binding.py`
- `?? scripts/76_static_design_dummies.py`
- `?? scripts/78_german_presentation_implementation_plan_fixed.py`
- `?? scripts/95c_download_fiona_2024_wfs_bbox.py`
- `?? scripts/95d_probe_fiona_wfs_direct_access.py`
- `?? scripts/95e_download_fiona_2024_wfs_with_proxy_params.py`
- `?? scripts/95f_probe_fiona_wfs_post_namespace.py`
- `?? scripts/95g_fix_fiona_wfs_projection_and_clip.py`
- `?? scripts/98_oberschwaben_intersection_area_qa.py`
- `?? scripts/98a_inventory_oberschwaben_feature_classes.py`
- `?? scripts/98b_prepare_oberschwaben_counties_from_gisco.py`
- `?? scripts/98c_oberschwaben_intersection_classification_review.py`
- `?? scripts/99_reposition_transformations_after_oberschwaben.py`
- `?? sources/`
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
- `?? tasks/B62_bind_bw_regional_frame_to_central_story.md`
- `?? tasks/B7_prepare_phase_B_release.md`
- `?? tasks/B99_reposition_transformations_after_oberschwaben.md`
- `?? working/`

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
