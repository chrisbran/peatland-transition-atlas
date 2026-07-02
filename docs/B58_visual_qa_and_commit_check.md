# B58 - Visual QA and Commit Check

Date: 2026-07-02

## 0. Active map-story mode

- OK active mode: B169 live sticky zoom
- INFO legacy central map-story source files may still exist in `src/`, but they are not treated as active wiring unless referenced by `index.html`.

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
- OK `public/maps/bw/bw_bk50_moor_extent.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/bw/bw_admin_context.png` — PNG header RGBA (1600, 900) bit_depth=8
- OK `public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png` — PNG header RGBA (1600, 900) bit_depth=8

## 2. Required map-story scripts

- OK `src/b169_live_sticky_zoom.js`
- OK no legacy central map-story scripts referenced by `index.html`

## 3. index.html reference check

- OK no broken local script/image references detected

## 4. Active map-story states

- OK `global-peat` — index=True, scripts=True
- OK `global-pressure-total` — index=True, scripts=True
- OK `global-pressure-density` — index=True, scripts=True
- OK `europe-bridge` — index=True, scripts=True
- OK `germany-extent` — index=True, scripts=True
- OK `germany-types` — index=True, scripts=True
- OK `baden-wuerttemberg` — index=True, scripts=True
- OK `oberschwaben-handoff` — index=True, scripts=True

## 5. Unwanted reference check

- OK `germany_thuenen_legend_fix.js` not found in active files
- OK `B53_germany_thuenen_distinction_and_legend_fix` not found in active files
- OK `EUROPE_FRAME_V1.png` not found in active files

## 6. Git status / commit hygiene

- OK no obvious staged raw-data/GIS files visible in git status

### Current changed/untracked files

- ` M docs/B58_visual_qa_and_commit_check.md`
- ` M index.html`
- ` M src/styles.css`
- ` M tasks/done.md`
- `?? docs/B176_remove_felt_from_public_page.md`
- `?? docs/B176_remove_felt_from_public_page_audit.txt`
- `?? docs/B176_removed_felt_fragments.csv`
- `?? docs/B177_external_links_inventory.csv`
- `?? docs/B177_external_request_audit.md`
- `?? docs/B177_external_request_audit_run.txt`
- `?? docs/B177_loaded_external_resources.csv`
- `?? docs/B177_provider_token_scan.csv`
- `?? docs/B177b_remove_residual_felt_tokens.md`
- `?? docs/B177b_remove_residual_felt_tokens_audit.txt`
- `?? docs/B177b_removed_residual_felt_tokens.csv`
- `?? docs/B178_copy_hardening_changes.csv`
- `?? docs/B178_scale_change_area_balance_copy_hardening.md`
- `?? docs/B178_scale_change_area_balance_copy_hardening_audit.txt`
- `?? docs/B179_engpass_replacement_changes.csv`
- `?? docs/B179_replace_engpass_scorecard_with_bottleneck_graphic.md`
- `?? docs/B179_replace_engpass_scorecard_with_bottleneck_graphic_audit.txt`
- `?? docs/B179b_clean_engpass_bottleneck_section.md`
- `?? docs/B179b_clean_engpass_bottleneck_section_audit.txt`
- `?? docs/B179b_removed_engpass_remnants.csv`
- `?? docs/B180_redundancy_disclaimer_diet.md`
- `?? docs/B180_redundancy_disclaimer_diet_audit.txt`
- `?? docs/B180_removed_redundant_disclaimers.csv`
- `?? docs/B180b_disclaimer_and_marker_changes.csv`
- `?? docs/B180b_restore_b176_and_tighten_disclaimer_diet.md`
- `?? docs/B180b_restore_b176_and_tighten_disclaimer_diet_audit.txt`
- `?? docs/B181_closing_counterpoint_and_schlussbogen.md`
- `?? docs/B181_closing_counterpoint_and_schlussbogen_audit.txt`
- `?? docs/B181_closing_counterpoint_changes.csv`
- `?? docs/B182_final_qa_and_v2_1_0_release.md`
- `?? docs/B182_final_qa_and_v2_1_0_release_audit.txt`
- `?? docs/B182_release_signals.csv`
- `?? docs/B182_v2_1_0_release_checklist.md`
- `?? docs/B182_v2_1_0_release_notes.md`
- `?? scripts/176_remove_felt_from_public_page.py`
- `?? scripts/177_external_request_audit.py`
- `?? scripts/177b_remove_residual_felt_tokens.py`
- `?? scripts/178_scale_change_area_balance_copy_hardening.py`
- `?? scripts/179_replace_engpass_scorecard_with_bottleneck_graphic.py`
- `?? scripts/179b_clean_engpass_bottleneck_section.py`
- `?? scripts/180_redundancy_disclaimer_diet.py`
- `?? scripts/180b_restore_b176_and_tighten_disclaimer_diet.py`
- `?? scripts/181_closing_counterpoint_and_schlussbogen.py`
- `?? scripts/182_final_qa_and_v2_1_0_release.py`

## 7. Suggested add list for this milestone

- `index.html`
- `src/styles.css`
- `src/b169_live_sticky_zoom.js`
- `public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png`
- `scripts/58_visual_qa_and_commit_check.py`
- `tasks/done.md`

## Result

PASS
