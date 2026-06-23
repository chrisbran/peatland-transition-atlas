# B90 - Release Check German Presentation Version

Date: 2026-06-23

## 1. Result

**FAIL**

## 2. Purpose

B90 is the release check for the German presentation version after B79-B89.

It replaces the outdated B72 assumption that a missing `#guidedStory` is always a failure. In the German presentation version, `#guidedStory` may be absent if the new B79/B87/B88 structure is active.

## 3. Check results

- OK   `index.html` — exists
- OK   `src/styles.css` — exists
- OK   `src/app.js` — exists
- OK   `German presentation mode` — B79-B89 markers detected
- OK   `HTML language` — lang=de present
- OK   `German hero title` — present
- OK   `German hero kicker` — present
- OK   `nav label Problem` — present
- OK   `nav label Kartenfolge` — present
- OK   `nav label Umsetzung` — present
- OK   `nav label Pfade` — present
- OK   `nav label Methode` — present
- OK   `central story canonical id` — present
- OK   `central story stable data attribute` — present
- OK   `central story class` — present
- OK   `central step cards` — 11 b88-step-card markers
- OK   `central state extent` — present
- OK   `central state total` — present
- OK   `central state density` — present
- OK   `central state compare` — present
- OK   `central state europe-borders` — present
- OK   `central state europe-peat` — present
- OK   `central state germany-context` — present
- OK   `central state germany-thuenen-extent` — present
- OK   `central state germany-thuenen-types` — present
- OK   `central state bw-context` — present
- OK   `central state bw-bk50-extent` — present
- OK   `section #b79RegionalImplementation` — present
- OK   `section #b79Pathways` — present
- FAIL `section #b79MethodBoundary` — missing
- OK   `method boundary sentence` — present
- OK   `#guidedStory` — absent; accepted because German presentation mode is active
- OK   `app metric selector guard` — guard detected
- OK   `CSS marker: B79 German presentation version` — present
- OK   `CSS marker: B82 compact header and overflow fix` — present
- OK   `CSS marker: B84 harden central map story panels` — present
- OK   `CSS marker: B87 central story id restore` — present
- OK   `CSS marker: B88 wrap central story step cards` — present
- OK   `CSS marker: B89 force uniform central step card state` — present
- OK   `public/maps/global/global_gpm2_peat_extent.png` — exists
- OK   `public/maps/global/global_hotspots_total.png` — exists
- OK   `public/maps/global/global_hotspots_density.png` — exists
- OK   `public/maps/global/global_country_borders.png` — exists
- OK   `public/maps/europe/europe_gpm2_peat_extent.png` — exists
- OK   `public/maps/europe/europe_country_borders.png` — exists
- OK   `public/maps/germany/germany_admin_context.png` — exists
- OK   `public/maps/germany/germany_thuenen_moor_extent.png` — exists
- OK   `public/maps/germany/germany_thuenen_moor_types.png` — exists
- OK   `public/maps/bw/bw_admin_context.png` — exists
- OK   `public/maps/bw/bw_bk50_moor_extent.png` — exists
- OK   `local src/href references` — no broken local references detected
- WARN `old English/meta terms in index.html` — terms detected: Prototype appendix, Supporting evidence

## 4. Failures

- section #b79MethodBoundary: missing

## 5. Warnings

- old English/meta terms in index.html: terms detected: Prototype appendix, Supporting evidence
- ?? data/external/ visible in git status
- ?? data/external/ raw/external data visible
- ?? data/metadata/peat_soils_source_catalog.csv visible in git status

## 6. Public URL for review

Use a cache-busted URL:

`https://chrisbran.github.io/peatland-transition-atlas/?v=b90-2026-06-23`

## 7. Git status snapshot

```text
?? data/external/
?? data/metadata/peat_soils_source_catalog.csv
?? design_dummies/
?? docs/B76_static_design_dummies.md
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
?? scripts/76_static_design_dummies.py
?? scripts/78_german_presentation_implementation_plan_fixed.py
?? scripts/90_release_check_german_presentation_version.py
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

## 8. Release interpretation

A B90 `PASS WITH WARNINGS` is acceptable if warnings are limited to known untracked raw-data/workflow files or old documentation artefacts.

It is not acceptable if there are failures for:

- central map states,
- BW map assets,
- method boundary,
- broken references,
- missing app selector guards.
