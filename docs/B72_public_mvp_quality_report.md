# B72 - Public MVP Quality Report

Date: 2026-06-22

## Result

**PASS WITH WARNINGS**

## 1. Summary

B72 checks the current MVP page state after the story-flow and evidence-module restructuring.

It explicitly checks:

- global, Europe, Germany and BW PNG map assets,
- central story controller scripts,
- all 11 central sticky-map states,
- retired legacy sections,
- lower evidence grouping sections,
- active and retired script tags,
- local broken references,
- known raw-data/git hygiene warnings.

## 2. Check results

- OK   `public/maps/global/global_gpm2_peat_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/global/global_hotspots_total.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/global/global_hotspots_density.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/global/global_country_borders.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/europe/europe_gpm2_peat_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/europe/europe_country_borders.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/germany/germany_admin_context.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/germany/germany_thuenen_moor_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/germany/germany_thuenen_moor_types.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/bw/bw_admin_context.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `public/maps/bw/bw_bk50_moor_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK   `src/central_global_map_story.js` — required central story script exists
- OK   `src/central_layer_state_hardener.js` — required central story script exists
- OK   `src/central_step_state_bridge.js` — required central story script exists
- OK   `src/central_stage_label_fix.js` — required central story script exists
- OK   `index.html references` — no broken local src/href references detected
- OK   `central state extent` — present in index.html
- OK   `central state total` — present in index.html
- OK   `central state density` — present in index.html
- OK   `central state compare` — present in index.html
- OK   `central state europe-borders` — present in index.html
- OK   `central state europe-peat` — present in index.html
- OK   `central state germany-context` — present in index.html
- OK   `central state germany-thuenen-extent` — present in index.html
- OK   `central state germany-thuenen-types` — present in index.html
- OK   `central state bw-context` — present in index.html
- OK   `central state bw-bk50-extent` — present in index.html
- OK   `public/maps/bw/bw_admin_context.png` — BW map PNG referenced by index.html
- OK   `public/maps/bw/bw_bk50_moor_extent.png` — BW map PNG referenced by index.html
- OK   `#guidedStory` — retired/hidden with B64
- OK   `#story` — retired/hidden with B69
- OK   `#bwPeatLayer` — retired/hidden with B71
- OK   `#interpretationIntro` — lower evidence grouping section present
- OK   `#supportingEvidenceGroupIntro` — lower evidence grouping section present
- OK   `#prototypeAppendixIntro` — lower evidence grouping section present
- OK   `src/app.js` — active script tag present
- OK   `src/hotspots.js` — active script tag present
- OK   `src/hotspot_base_layer.js` — active script tag present
- OK   `src/central_global_map_story.js` — active script tag present
- OK   `src/central_layer_state_hardener.js` — active script tag present
- OK   `src/central_step_state_bridge.js` — active script tag present
- OK   `src/central_stage_label_fix.js` — active script tag present
- OK   `src/scrolly_story.js` — retired guidedStory script tag absent
- OK   `src/scrolly_story_layers.js` — retired guidedStory script tag absent
- OK   `src/gpm2_context_images.js` — retired guidedStory script tag absent
- OK   `CSS marker: B68 MVP storyline lock` — present in src/styles.css
- OK   `CSS marker: B68b compact storyline bridge` — present in src/styles.css
- OK   `CSS marker: B70 central story readability pass` — present in src/styles.css
- OK   `CSS marker: B71 lower evidence reframing` — present in src/styles.css
- WARN `?? data/external/` — raw-data/GIS-like path visible in git status
- WARN `?? data/metadata/` — raw-data/GIS-like path visible in git status

## 3. Failures

- none

## 4. Warnings

- ?? data/external/ visible in git status
- ?? data/metadata/ visible in git status

## 5. Manual public-site check

After committing and pushing B72, open:

```text
https://chrisbran.github.io/peatland-transition-atlas/?v=b72
```

Check manually:

1. No Six-part story visible.
2. No old guidedStory visible.
3. Main atlas story bridge visible.
4. Central 11-step map story works.
5. Interpretation / Supporting evidence / Prototype appendix grouping visible.
6. Old BW interactive prototype layer not visible.
7. No obvious public/local mismatch after hard refresh.

## 6. Git status at B72 runtime

```text
M docs/B58_visual_qa_and_commit_check.md
 M tasks/done.md
?? data/external/
?? data/metadata/peat_soils_source_catalog.csv
?? docs/B72_public_mvp_quality_pass.md
?? docs/B72_public_mvp_quality_report.md
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
?? scripts/72_public_mvp_quality_pass.py
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
