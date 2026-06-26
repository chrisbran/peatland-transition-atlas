# Done
- 2026-06-17: Task B1 completed — country hotspot schema and Phase B source catalog created.
- 2026-06-17: Task B3 completed — hotspot ranking layer added to interface.
- 2026-06-17: Task B4 completed — prepared country boundary join for hotspot data.
- 2026-06-17: Task B5 completed — dependency-free choropleth map added to hotspot section.
- 2026-06-17: Task B6a completed — hotspot layout refined and sticky header disabled for cleaner screenshots.
- 2026-06-17: Task B6b completed — added total emissions vs emissions density toggle to hotspot map.
- 2026-06-17: Task B6b legend fix completed — made hotspot map legend swatches visible.
- 2026-06-17: Task B6c completed — linked hotspot rankings and map highlighting.
- 2026-06-17: Task B6c v2 completed — replaced hotspot module with robust ranking-map linking.
- 2026-06-17: Task B6c v3 completed — made ranking-map linking visibly explicit with marker and stronger highlights.
- 2026-06-17: Task B7 completed — prepared Phase B release notes, README/CHANGELOG update and QA checklist.
- 2026-06-17: Task B8a completed — added base land layer and softened hotspot map palette.
- 2026-06-17: Task B8b completed — replaced equirectangular map display with Robinson-style visual projection.
- 2026-06-17: Task B10 completed — created peat/organic-soils data source inventory and B11 layer-build task.
- 2026-06-17: Task B11a completed — prepared BK50-Moor source acquisition workflow and web-layer processor.
- 2026-06-18: Task B11c completed — added Baden-Württemberg BK50-Moor preview map to the public atlas.
- 2026-06-18: Task B12 completed — added first sticky-scroll guided story scaffold.
- 2026-06-18: Task B13 completed — bound sticky story to real world emissions and Baden-Württemberg BK50-Moor layers.
- 2026-06-18: Task B14a completed — prepared Germany organic-soils source acquisition workflow and web-layer processor.
- 2026-06-18: Task B14c optimizer prepared — added optimized Germany organic-soils web-layer builder.
- 2026-06-18: Task B14d completed — bound Germany organic-soils layer to sticky story.
- 2026-06-18: Task B15a completed — prepared Europe wetland/peat source workflow and web-layer processor.
- 2026-06-18: Task B15c completed — bound GPM 2.0 global and Europe context images to sticky story.
- 2026-06-18: Task B15d completed — fixed GPM 2.0 sticky-story flicker with stable overlay.
- 2026-06-18: Task B15e completed — fixed repeated GPM Europe overlay with exact state matching.
- 2026-06-18: Task B16 completed — refined transition-evidence storyline and layer logic.
- 2026-06-18: Task B17 completed — linked transition pathway evidence to spatial layers.
- 2026-06-18: Task B17b completed — inserted pathway evidence matrix with non-conflicting ID.
- 2026-06-18: Task B18b-new completed — added central global map story using ArcGIS-rendered layer stack.
- 2026-06-18: Task B18b4 completed — kept GPM2 context visible under total-emissions and density overlays.
- 2026-06-18: Task B18b5 completed — increased GPM2 context opacity under emissions overlays.
- 2026-06-18: Task B18b6 completed — simplified compare state to avoid mixed hotspot overlay.
- 2026-06-18: Task B18c completed — cleaned central global story stage and reduced repeated text.
- 2026-06-18: Task B19a completed — prepared Europe frame workflow and export folders.
- 2026-06-19: Task B19b completed — bound Europe frame to central sticky story.
- 2026-06-19: Task B19c completed - prepared Germany / Thuenen frame workflow.
- 2026-06-19: Task B50 completed - fixed Germany / Thuenen central-story state binding.
- 2026-06-19: Task B51 completed - added hard central map layer controller.
- 2026-06-19: Task B52 completed - added central step-state bridge.
- 2026-06-19: Task B53 completed - improved Germany Thuenen distinction and legend.
- 2026-06-19: Task B54 completed - removed B53 custom legend and restored original Thuenen legend colors.
- 2026-06-19: Task B55 completed - fixed Thuenen legend inline color swatches.
- 2026-06-19: Task B56 completed - fixed central map stage label for Germany / Thuenen states.
- 2026-06-19: Task B57 completed - refined Germany / Thuenen story text.
- 2026-06-19: Task B58 completed - ran visual QA and commit hygiene check.
- 2026-06-19: Task B60 completed - patched B58 QA with robust no-Pillow PNG header check.
- 2026-06-19: Task B61 completed - prepared BW / regional frame workflow.
- B62 repair: Completed BW extent state binding across central map hardener, bridge, labels, and CSS.

## 2026-06-22 - B64 - Cleanup story flow phase 1

- Retired duplicate `guidedStory` section via reversible `is-retired` class.
- Rerouted top Story navigation to `#centralGlobalMapStory`.
- Reframed lower evidence/pathway headings as supporting sections.
- Added `docs/B64_cleanup_story_flow_phase1.md`.
- No data, assets or scripts were deleted.

## B65 - Legacy asset and script reference audit (2026-06-22)

- Created `docs/B65_legacy_asset_and_script_reference_audit.md`.
- Created `docs/B65_reference_inventory.csv`.
- Created `docs/B65_referenced_assets.txt`.
- Audited active sections, script tags and public asset references after B64.
- No application code, script tags, public data files or map assets were removed.

## B66 - Retire guidedStory script tags phase 1 (2026-06-22)

- Removed old guidedStory script tags from `index.html`.
- Removed script tags only; no JS files, data files, images or map assets were deleted.
- Kept central PNG map story controller stack unchanged.
- Kept hotspot, evidence, pathway, fit and BW interactive modules loaded.

## B67 - Harden retired guidedStory visibility (2026-06-22)

- Added native HTML-level hiding to `#guidedStory`.
- Kept the retired section content in `index.html` for reversibility.
- Did not delete scripts, data files, images or map assets.
- Purpose: make B64 retirement robust against public stylesheet caching.

## B68 - Lock MVP storyline (2026-06-22)

- Added a compact MVP storyline lock before the central map story.
- Added a supporting-evidence intro before the lower explorer/pathway modules.
- Added `data-story-role` attributes to major page sections.
- Added small CSS styles for the new editorial framing blocks.
- Did not delete sections, scripts, data files, images or map assets.

## B68b - Refine MVP storyline lock (2026-06-22)

- Replaced the large B68 MVP storyline block with a compact main-atlas-story bridge.
- Replaced the large supporting-evidence intro with a compact evidence-explorer bridge.
- Added compact CSS overrides.
- Did not delete sections, scripts, data files, images or map assets.

## B69 - Retire six-part story phase 1 (2026-06-22)

- Reversibly retired the old `#story` / Six-part story section.
- Retargeted navigation links from `#story` to `#transitionLogic` if present.
- Kept `#transitionLogic`, `#mvpStoryline` and `#centralGlobalMapStory` as the visible story entry.
- Did not delete sections, scripts, data files, images or map assets.

## B70 - Refine central story readability (2026-06-22)

- Rewrote central sticky-map step text for clarity and shorter interpretation.
- Added a compact read-note explaining the scale-transition sequence.
- Added small CSS refinements for central step readability.
- Did not change central map state names, layer bindings, scripts, data files, images or map assets.

## B71 - Reframe lower evidence modules (2026-06-22)

- Added lower-page grouping into interpretation, supporting evidence and prototype appendix.
- Refreshed the supporting-evidence bridge after the main map.
- Added `data-evidence-tier` attributes to lower modules.
- Reversibly retired the old `#bwPeatLayer` experimental GeoJSON section from the visible page flow.
- Did not delete sections, scripts, data files, images or map assets.

## B72 - Public MVP quality pass (2026-06-22)

- Created `docs/B72_public_mvp_quality_pass.md`.
- Created `docs/B72_public_mvp_quality_report.md`.
- Checked BW PNGs, central 11-step map states, retired legacy sections and lower evidence grouping.
- Did not change application behavior, CSS, scripts, data files, images or map assets.
- Result: FAIL.

## B73 - German presentation version brief (2026-06-23)

- Defined target audience: scientifically informed practitioners.
- Defined tone: narrative and explanatory.
- Defined scope: short and pointed first German presentation version.
- Created `docs/B73_deutsche_vorzeigefassung_brief.md`.
- Created `docs/B73_design_directions_brief.md`.
- Did not modify application files, maps, scripts, data or styling.

## B74 - Visible text audit DE (2026-06-23)

- Extracted visible non-retired text from `index.html`.
- Created `docs/B74_visible_text_audit_de.md`.
- Created `docs/B74_visible_text_inventory.csv`.
- Created `docs/B74_german_rewrite_targets.md`.
- Flagged English text, meta/tool language, long text and method-boundary risks.
- Did not modify application files, maps, scripts, data or styling.

## B75 - Design concept matrix (2026-06-23)

- Defined three controlled design directions for the German presentation version.
- Recommended hybrid direction: fachlich hell, narrativ geführt, kartografisch diszipliniert.
- Created `docs/B75_design_concept_matrix.md`.
- Created `docs/B75_design_decision_scorecard.csv`.
- Created `docs/B75_visual_language_principles.md`.
- Did not modify application files, maps, scripts, data or CSS.
## B76 - Static design dummies (2026-06-23)

- Created three static HTML design dummies under `design_dummies/`.
- Used the same German core copy in all variants.
- Created `docs/B76_static_design_dummies.md`.
- Did not modify production `index.html`, CSS, scripts, maps or data.

## B77 - Design dummy review (2026-06-23)

- Reviewed B76 dummy variants.
- Selected B76_B_editorial_natur as the preferred direction.
- Defined target direction: Editorial Natur + fachliche Ruhe + kartografische Disziplin.
- Created `docs/B77_design_dummy_review.md`.
- Created `docs/B77_target_design_spec.md`.
- Did not modify production website files, maps, scripts, data or CSS.

## B78 - German presentation implementation plan (2026-06-23)

- Created `docs/B78_german_presentation_implementation_plan.md`.
- Created `docs/B78_german_presentation_copy_targets.csv`.
- Created `docs/B78_patch_strategy.md`.
- Defined safe B79 production implementation strategy.
- Did not modify production website files, CSS, scripts, maps or data.

## B79 - German presentation version (2026-06-23)

- Applied first German presentation version to `index.html`.
- Added B79 editorial-nature design overrides to `src/styles.css`.
- Inserted compact German implementation, pathway and method-boundary sections.
- Hid older lower explorer/prototype sections reversibly with `data-retired="B79"`.
- Created `docs/B79_german_presentation_version.md`.
- Preserved map assets and central map state names.

## B80 - Polish German presentation layout (2026-06-23)

- Polished B79 German presentation layout via CSS only.
- Kept B79 editorial-nature direction.
- Improved header behaviour, hero cards, central map step readability and map framing.
- Created `docs/B80_polish_german_presentation_layout.md`.
- Did not modify HTML, JavaScript, maps or data.

## B81 - Fix German copy and layout overflow (2026-06-23)

- Replaced remaining visible English/meta hero texts with German copy.
- Hardened hero layout to prevent narrow columns and overflow.
- Added stronger wrapping/overflow rules for hero cards and central story cards.
- Suppressed residual overlay artefacts.
- Created `docs/B81_fix_german_copy_and_layout_overflow.md`.

## B82 - Compact header and overflow fix (2026-06-23)

- Replaced the old duplicated masthead with a compact German navigation header.
- Added CSS safeguards to hide header hero/meta text.
- Stabilized hero claim-card width and card text wrapping.
- Improved central map step overflow and viewport-edge behaviour.
- Created `docs/B82_compact_header_and_overflow_fix.md`.

## B83 - Fix central panels and textContent error (2026-06-23)

- Removed literal `\n` artefacts from `index.html`.
- Applied consistent dark styling to central map step panels.
- Hardened central step text wrapping and overlay suppression.
- Guarded direct `document.querySelector(...).textContent = ...` assignment patterns in `src/*.js`.
- Created `docs/B83_fix_central_panels_and_textcontent_error.md`.

## B84 - JS textContent and panel hardening (2026-06-23)

- Hardened broader `document.querySelector(...).textContent` patterns in `index.html` and `src/*.js`.
- Removed literal `\n` artefacts from `index.html`.
- Applied broad dark styling to all central map story text panels.
- Created `docs/B84_js_textcontent_and_panel_hardening.md`.
- Created `docs/B84_textcontent_patch_inventory.txt`.

## B85 - Restore persistent dark central map stage (2026-06-23)

- Restored a persistent dark central map stage via CSS.
- Kept all central step cards on a consistent dark readable panel treatment.
- Did not alter map state names, JavaScript logic, map assets or raw data.
- Created `docs/B85_restore_persistent_dark_central_map_stage.md`.

## B87 - Restore central story id and stage targeting (2026-06-23)

- Restored canonical `id="centralGlobalMapStory"` on the actual central story section.
- Added `data-b87-central-story="true"` for stable future targeting.
- Added class/id/data-attribute CSS targeting for the central map stage and cards.
- Created `docs/B87_restore_central_story_id_and_stage_targeting.md`.

## B88 - Wrap central story step cards (2026-06-23)

- Wrapped central `article[data-global-state]` contents in `.b88-step-card`.
- Reset scroll-trigger articles to transparent so they no longer render as giant dark blocks.
- Styled only `.b88-step-card` as the visible dark step panel.
- Created `docs/B88_wrap_central_story_step_cards.md`.

## B89 - Force uniform central step card state (2026-06-23)

- Forced all central `.b88-step-card` panels to use one dark material independent of active/inactive state.
- Neutralised old opacity/filter/blend/background changes on central scroll-trigger articles.
- Did not change map state names, JavaScript logic, maps or data.
- Created `docs/B89_force_uniform_central_step_card_state.md`.

## B90 - Release check German presentation version (2026-06-23)

- Created `docs/B90_release_check_german_presentation_version.md`.
- Created `docs/B90_public_review_checklist.md`.
- Checked German presentation structure, central states, map assets, app selector guard and method boundary.
- Treated missing `#guidedStory` as acceptable when German presentation mode is active.
- Did not modify application files, CSS, JavaScript, maps or data.

## B91 - German copy polish and presentation brief (2026-06-23)

- Created `docs/B91_german_copy_polish_review.md`.
- Created `docs/B91_jour_fixe_presentation_brief.md`.
- Created `docs/B91_copy_polish_todo.csv`.
- Prepared a short German project-presentation narrative.
- Did not modify production HTML, CSS, JavaScript, maps or data.

## B92 - Oberschwaben implementation story concept (2026-06-23)

- Created `docs/B92_oberschwaben_implementation_story_concept.md`.
- Created `docs/B92_oberschwaben_storyboard.md`.
- Created `docs/B92_oberschwaben_layer_spec.csv`.
- Created `docs/B92_oberschwaben_indicator_spec.csv`.
- Created `tasks/B93_prepare_oberschwaben_map_workflow.md`.
- Shifted next development from visual polish to a regional implementation module.
- Did not modify production HTML, CSS, JavaScript, maps or data.

## B93 - Prepare Oberschwaben map workflow (2026-06-23)

- Created `public/maps/oberschwaben/README.md`.
- Created `docs/B93_prepare_oberschwaben_map_workflow.md`.
- Created `docs/B93_oberschwaben_arcgis_qgis_workflow.md`.
- Created `docs/B93_oberschwaben_expected_outputs.csv`.
- Created `docs/B93_oberschwaben_data_decision_matrix.csv`.
- Created `docs/B93_oberschwaben_cartographic_rules.md`.
- Created `tasks/B94_build_oberschwaben_map_assets.md`.
- Prepared map workflow for Oberschwaben implementation module.
- Did not modify production HTML, CSS, JavaScript, maps or data.

## B94 - Source-anchor Oberschwaben map workflow (2026-06-23)

- Created `docs/B94_oberschwaben_source_stack.md`.
- Created `docs/B94_oberschwaben_source_stack.csv`.
- Created `docs/B94_oberschwaben_data_access_questions.md`.
- Created `docs/B94_oberschwaben_legend_and_map_logic.md`.
- Created `docs/B94_oberschwaben_flyer_map_reference_note.md`.
- Created `tasks/B95_build_oberschwaben_map_assets.md`.
- Anchored the Oberschwaben map workflow to the SOLAMO flyer source-stack logic.
- Did not modify production HTML, CSS, JavaScript, maps or data.

## B95 - Build Oberschwaben map asset package (2026-06-23)

- Created `public/maps/oberschwaben/oberschwaben_map_sources.json`.
- Created `docs/B95_build_oberschwaben_map_assets.md`.
- Created `docs/B95_oberschwaben_asset_manifest.csv`.
- Created `docs/B95_oberschwaben_source_candidate_scan.txt`.
- Created `docs/B95_oberschwaben_png_asset_qa.md`.
- Created `docs/B95_oberschwaben_manual_export_checklist.md`.
- Created `tasks/B96_bind_oberschwaben_map_section.md`.
- Prepared Oberschwaben map asset package and QA without creating fake map images.

## B95h - Validate Oberschwaben scrolly layer-stack assets (2026-06-24)

- Validated Oberschwaben scrolly layer-stack PNG assets.
- Created `docs/B95h_oberschwaben_layer_stack_qa.md`.
- Created `docs/B95h_oberschwaben_layer_stack_manifest.csv`.
- Created `tasks/B96_bind_oberschwaben_scrolly_layer_stack.md`.
- Updated the Oberschwaben implementation direction from static composite map to scrollable layer stack.

## B96 - Bind Oberschwaben scrolly layer stack (2026-06-24)

- Added Oberschwaben scrollable layer-stack section to `index.html`.
- Added B96-specific CSS for sticky stage, PNG layer opacity states and story cards.
- Added a small self-contained IntersectionObserver script in `index.html`.
- Used B95h layer assets:
  - `public/maps/oberschwaben/oberschwaben_admin_context.png`
  - `public/maps/oberschwaben/oberschwaben_agriculture.png`
  - `public/maps/oberschwaben/oberschwaben_moor_context.png`
  - `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

## B97 - Align Oberschwaben stage with central story (2026-06-24)

- Replaced the B96 Oberschwaben CSS block with a larger, darker central-story-aligned map stage.
- Preserved the B96 HTML, JS and validated layer assets.
- Added `docs/B97_align_oberschwaben_stage_with_central_story.md`.

## B97b - Lighten Oberschwaben stage (2026-06-24)

- Replaced the dark B97 Oberschwaben CSS treatment with a lighter warm editorial stage.
- Kept the large central-story scale introduced by B97.
- Preserved B96 HTML/JS and the validated B95h layer assets.
- Added `docs/B97b_lighten_oberschwaben_stage.md`.

## B97c - Oberschwaben readability and legend fix (2026-06-24)

- Added a CSS override block so Oberschwaben scroll text cards render above the large sticky map stage.
- Removed the legend's white overlay background and placed the legend below the map.
- Preserved B96 HTML/JS and B97b light-stage treatment.
- Added `docs/B97c_oberschwaben_readability_and_legend_fix.md`.

## B97d - Stabilize Oberschwaben step card opacity (2026-06-24)

- Added a CSS override block to keep Oberschwaben text-card opacity/background stable while scrolling.
- Preserved B96 HTML/JS, B97b light-stage treatment and B97c legend/z-index fixes.
- Added `docs/B97d_stabilize_oberschwaben_step_card_opacity.md`.

## B97e - Restore Oberschwaben translucent step cards (2026-06-24)

- Added a CSS override block that restores stable semi-transparent Oberschwaben text-card backgrounds.
- Preserved stable active/inactive behavior from B97d while making the map visible through/around the cards again.
- Added `docs/B97e_restore_oberschwaben_translucent_step_cards.md`.

## B97f - Editorial cleanup / public-readiness (2026-06-24)

- Applied targeted editorial cleanup to `index.html`.
- Fixed visible typo variants for `Methodische Grenze` if present.
- Neutralized visible prototype/build notes where exact patterns were found.
- Reduced selected German/English mixing in prominent page copy.
- Added `docs/B97f_editorial_cleanup_public_readiness.md`.
- Added `docs/B97f_public_readiness_red_flag_scan.txt`.

## B97g - Clean remaining public copy red flags (2026-06-24)

- Applied a second conservative editorial cleanup to visible public copy in `index.html`.
- Generated a classified residual red-flag scan distinguishing visible-review, hidden-retired and script false-positive hits.
- Left hidden retired prototype appendix sections untouched.
- Added `docs/B97g_clean_remaining_public_copy_red_flags.md`.
- Added `docs/B97g_public_readiness_red_flag_scan_classified.txt`.

## B98a - Oberschwaben feature class inventory (2026-06-24)

- Added ArcGIS feature-class inventory to diagnose missing county feature class for B98.
- Created `docs/B98a_oberschwaben_feature_class_inventory.md`.
- Created `docs/B98a_oberschwaben_feature_class_inventory.csv`.

## B98b - Prepare Oberschwaben counties from GISCO (2026-06-24)

- Created missing `oberschwaben_counties_25832` feature class in the Oberschwaben working geodatabase.
- Selected GISCO NUTS 2024 level-3 IDs DE146, DE147, DE148, DE149.
- Created `docs/B98b_prepare_oberschwaben_counties_from_gisco.md`.
- Created `docs/B98b_oberschwaben_counties_inventory.csv`.

## B98 - Oberschwaben intersection area and classification QA (2026-06-24)

- Quantified FIONA 2024 agriculture × BK50 Moor-/Feuchtbodenkontext intersection by Landkreis and land-use group.
- Created `docs/B98_oberschwaben_intersection_area_qa.md`.
- Created `docs/B98_oberschwaben_county_landuse_area_summary.csv`.
- Created `docs/B98_oberschwaben_landuse_classification_qa.csv`.
- Created `docs/B98_oberschwaben_analysis_manifest.csv`.
- Created `tasks/B99_reposition_transformations_after_oberschwaben.md`.

## B98c - Oberschwaben intersection classification review (2026-06-24)

- Reviewed actual Oberschwaben intersection by original FIONA class.
- Separated `Aus der Produktion genommene Flächen/Stilllegung` and `ZUWEISUNG FEHLT` from normal Ackerland.
- Created `docs/B98c_oberschwaben_intersection_classification_review.md`.
- Created `docs/B98c_oberschwaben_intersection_classification_cleaned.csv`.
- Created `docs/B98c_oberschwaben_public_safe_summary.csv`.
- Created `docs/B98c_oberschwaben_flagged_intersection_summary.csv`.
- Created `docs/B98c_oberschwaben_analysis_manifest.csv`.

## B99 - Reposition Transformationspfade after Oberschwaben (2026-06-24)

- Replaced and moved the `#pathways` section so it follows the Oberschwaben scrolly map.
- Reframed Transformationspfade as the answer to the spatial intersection rather than a prior abstract module.
- Added conservative B98c-based qualitative interpretation without publishing exact hectare numbers.
- Added `docs/B99_reposition_transformations_after_oberschwaben.md`.
- Added `docs/B99_transformations_public_readiness_audit.txt`.

## B100 - Add moor primer section (2026-06-24)

- Added a compact `Moore verstehen` primer before the Oberschwaben implementation story.
- Explained the water-level / peat-decomposition / emissions mechanism.
- Added functional Niedermoor/Hochmoor and use-path context without creating suitability claims.
- Added `docs/B100_add_moor_primer_section.md`.
- Added `docs/B100_moor_primer_public_readiness_audit.txt`.

## B100b - Recast moor primer as compact bridge (2026-06-24)

- Replaced the textbook-like B100 primer with a compact editorial bridge.
- Reduced the visible mechanism to three chips: Nass/Speicher, Entwässert/Quelle, Wiedervernässt/Verhandlung.
- Moved detailed moor background into an optional disclosure element.
- Added `docs/B100b_recast_moor_primer_as_compact_bridge.md`.
- Added `docs/B100b_moor_primer_bridge_audit.txt`.

## B101 - Add Oberschwaben key-figures capsule (2026-06-24)

- Added a compact rounded key-figures capsule after the Oberschwaben scrolly map.
- Used B98c qualitatively and with rounded values: ~19,900 ha, ~82% Grünland, ~16% Ackerland, ~2% separated/reviewed categories.
- Kept the method boundary explicit: no suitability, no prioritization, no farm-level affectedness.
- Added `docs/B101_add_oberschwaben_key_figures_capsule.md`.
- Added `docs/B101_oberschwaben_key_figures_audit.txt`.

## B102 - Add usage-path / value-chain matrix (2026-06-24)

- Added a compact matrix for Nassgrünland, Nassweide, Schilf/Rohrkolben/Seggen, Sphagnum and Moor-PV.
- Translated transformation pathways into product logic, maturity and bottlenecks.
- Added the value-chain bottleneck: quantity, secure offtake, quality, standards and competitive products.
- Added `docs/B102_add_usage_value_chain_matrix.md`.
- Added `docs/B102_usage_value_chain_matrix_audit.txt`.

## B103 - Public text QA audit only (2026-06-24)

- Ran a non-destructive public text audit on `index.html`.
- Created visible text extract, findings CSV and wording frequency CSV.
- Did not modify public HTML/CSS/JS.

## B103b - Corrected visible text audit (2026-06-24)

- Reran public text audit with proper inherited hidden/retired-state handling.
- Separated actual visible text from hidden/retired archive text.
- Created corrected visible extract, hidden extract, visible findings and hidden findings.
- Did not modify public HTML/CSS/JS.

## B104 - Visible wording polish (2026-06-24)

- Fixed visible typo `Nasseverträgliche` -> `nässeverträgliche`.
- Translated visible English peatland-context labels.
- Reduced repeated `Umsetzung`, `wird zu/zur`, and `übersetzen` phrasing.
- Replaced public internal QA wording (`Flächen-QA`, `B98c`, `Klassifikations-QA`) with reader-facing wording.
- Did not intentionally remove hidden/retired prototype/archive sections.

## B104b - Second visible wording polish and Oberschwaben density (2026-06-24)

- Removed remaining self-referential wording and reduced colon-heavy headings.
- Removed `30 Sekunden` from the moor-primer detail label.
- Kept the method boundary but compressed its wording.
- Removed redundant public B98c/pathway QA note.
- Added CSS override to make Oberschwaben step cards smaller and more spaced.

## B105 - Source-swap plan and FIONA public safety mode (2026-06-25)

- Put public Oberschwaben land-use section into source-swap safety mode.
- Replaced public FIONA key figures with a source-in-transition capsule.
- Prevented public HTML from referencing FIONA-derived Oberschwaben agriculture/intersection map rasters.
- Documented candidate replacement sources: LGL/ATKIS first, BKG LBM-DE second, Copernicus/ESA fallback.
- Did not delete raw/working GIS data or hidden/retired archive sections.

## B106 - Candidate source probe (2026-06-25)

- Probed candidate open-data sources for replacing FIONA-derived Oberschwaben land-use evidence.
- Checked LGL Landnutzung WFS, LGL Basis-DLM WFS, BKG LBM-DE metadata and Copernicus/ESA fallback metadata.
- Created source-probe CSV, feature-type extracts and raw snippets.
- Did not modify public HTML/CSS/JS or GIS data.

## B107 - LGL Landnutzung schema and Oberschwaben sample (2026-06-25)

- Probed `nora:v_ln_landnutzung` schema via DescribeFeatureType.
- Queried a small Oberschwaben EPSG:25832 bbox sample via WFS GetFeature.
- Created field inventory, candidate value counts, sample examples and trial classification.
- Did not modify public HTML/CSS/JS, map PNGs or GIS/raw data folders.

## B107b - LGL Landnutzung grid class-universe probe (2026-06-25)

- Sampled the LGL Landnutzung WFS across an Oberschwaben bbox grid.
- Aggregated class/value combinations without saving raw GeoJSON or geometry.
- Created candidate agricultural rows and objectart mapping trial tables.
- Did not modify public HTML/CSS/JS, map PNGs or GIS/raw data folders.

## B107c - LGL Landnutzung mapping review (2026-06-25)

- Converted B107b candidate agricultural class rows into a conservative draft mapping.
- Mapped explicit Ackerland, Grünland and Sonder-/Dauerkultur classes.
- Flagged `1300 Betriebsfläche Landwirtschaft` for separate handling.
- Did not modify public HTML/CSS/JS, map PNGs or GIS/raw data folders.

## B108 - LGL Landnutzung controlled production test (2026-06-25)

- Built staged LGL Landnutzung replacement maps for Oberschwaben.
- Filtered Landwirtschaft (`objektart=223100`) and applied B107c mapping.
- Intersected mapped LGL land use with BK50 Moor-/Feuchtbodenkontext.
- Reported `Betriebsfläche Landwirtschaft` separately.
- Did not modify public HTML/CSS/JS or overwrite existing Oberschwaben PNGs.

## B109a - ArcGIS restyle brief for LGL Oberschwaben maps (2026-06-25)

- Prepared ArcGIS Pro restyle instructions for LGL-based Oberschwaben maps.
- Defined layer manifest, symbology, four-map export logic and QA checklist.
- Kept earlier FIONA map language only as visual reference.
- Did not modify public HTML/CSS/JS, map PNGs or GIS/raw data folders.

## B108b - LGL dissolve cartographic layers (2026-06-25)

- Created dissolved cartographic GPKG layers for LGL agriculture and LGL x BK50 intersection.
- Reduced raw LGL feature fragmentation for ArcGIS map export.
- Preserved internal `Landwirtschaft_unspezifisch` but documented public label replacement.
- Did not modify public HTML/CSS/JS or overwrite public PNGs.

## B105r - Restore FIONA public story state (2026-06-25)

- Reverted the public-page safety mode introduced by B105.
- Restored FIONA-based Oberschwaben map/story wording and key figures.
- Removed B105 source-swap CSS and `source_swap_status` metadata when present.
- Parked LGL replacement work from B106-B108b without deleting it.
- Did not modify raw/working data folders or public map PNGs.

## B110 - External source register

- Created source register for map data, project sources, literature groups and tested alternatives.
- Did not modify website, map PNGs or data folders.

## B111 - Public release stabilization (2026-06-25)

- Stabilized restored FIONA-based Oberschwaben public story.
- Consolidated source and interpretation notes.
- Confirmed LGL/source-swap leftovers are not active in `index.html`.
- Did not modify map data, map PNGs or LGL parked material.

## B111b - Oberschwaben source-note fix (2026-06-25)

- Applied targeted source-note wording correction in the Oberschwaben key-figure capsule.
- Kept FIONA/BK50/GISCO public story state.
- Did not modify map paths, map images, CSS or data.

## B112 - Git status hygiene via local exclude (2026-06-25)

- Added local `.git/info/exclude` rules for backup bundles, raw/working data, parked LGL/FIONA probe material and generated audit extracts.
- Did not modify public page files, maps, raw data or `.gitignore`.
- Kept the hygiene rules local to this working copy.

## B113 - Public release notes and method documentation (2026-06-25)

- Created public release notes for the restored FIONA-based atlas state.
- Created method documentation for map sources, derived layers, interpretation rules and caveats.
- Created release checklist for source, method, caveat and visual QA.
- Did not modify website, CSS, maps or data.

## B114 - Responsive visual QA and public copy review (2026-06-25)

- Created responsive visual QA plan for desktop, laptop, tablet-like and mobile viewports.
- Created manual test matrix for Oberschwaben scrolly, key figures, source notes and pathway section.
- Created public copy/risk review for claims, caveats and parked LGL branch.
- Did not modify website, CSS, map images or data.

## B115 - Final visible copy pass and no-overclaim audit (2026-06-25)

- Ran a conservative final copy pass for risky public-copy phrases.
- Created visible-copy audit for overclaiming, required caveats and watch terms.
- Kept FIONA/BK50/GISCO Oberschwaben public state active.
- Did not modify maps, CSS, data or LGL parked material.

## B116 - Release candidate state and deployment check (2026-06-25)

- Created release-candidate state report for the restored FIONA/BK50/GISCO public demo.
- Created deployment checklist for local QA, commit, push and post-deployment checks.
- Audited required source/caveat patterns, forbidden LGL/source-swap remnants and worktree safety.
- Did not modify website, CSS, maps or data.

## B116 - Public page hardening (2026-06-26)

- Removed old English prototype/explorer sections from the public page when matching markers were present.
- Strengthened the GHG mechanism and Oberschwaben planning rationale.
- De-risked wording around farm affectedness, suitability, priority, GHG mitigation and Moor-PV cashflow.
- Simplified the Oberschwaben area-balance labels.
- Did not modify CSS, map images or data.

## B117 - Cartographic caption and legend hardening (2026-06-26)

- Replaced public-facing technical map-caption remnants where exact text matches were found.
- Fixed Thuenen/Thünen and several English/GIS-internal caption phrases.
- Audited cartographic risk terms, required source terms and Oberschwaben legend labels.
- Created a colour specification for the next Oberschwaben map/legend export.
- Did not modify CSS, map images or data.

## B117b - Oberschwaben PNG palette probe (2026-06-26)

- Analysed current Oberschwaben PNG files with a stdlib-only PNG reader.
- Exported dominant exact, quantized and saturated candidate colours.
- Scanned index.html and src/styles.css for HEX colours near the B117 target palette.
- Did not modify maps, CSS, index.html or data.

## B117c - Oberschwaben map palette restyle (2026-06-26)

- Restyled already-derived Oberschwaben PNG layers to a clearer publication palette.
- Synchronized CSS legend swatches with the restyled PNG palette.
- Preserved geometry, alpha masks, source layers, FIONA/BK50/GISCO story logic and area values.
- Did not modify raw data or run GIS processing.

## B118 - Public UTF-8 encoding guard (2026-06-26)

- Ensured `<meta charset="utf-8">` is present at the top of the HTML head.
- Removed duplicate charset meta tags.
- Repaired common mojibake sequences for German umlauts, CO₂ and punctuation if present.
- Did not modify maps, CSS or data.

## B119 - Fachliche Klammer (2026-06-26)

- Added a concise GHG/water-table mechanism block.
- Added a focused Oberschwaben rationale without turning the page into a SOLAMO project brochure.
- Reframed transformation pathways as land-use-context-specific Prüfpfade.
- Added compact public source links to IPCC, UBA, BMUV, LUBW, LAZBW, MLR BW and SOLAMO-BW.
- Did not modify maps, map data, map colours or raw data.

## B120 - Final public readiness cleanup (2026-06-26)

- Removed/translated remaining public English structure labels.
- Finalized Oberschwaben area-balance labels and method note.
- Harmonized older "Moore verstehen" wording with the B119 water-table/GHG mechanism.
- Audited visible public text for prototype remnants, overclaims and encoding artefacts.
- Did not modify maps, CSS, map colours or data.

## B121 - Raster caption and final wording cleanup (2026-06-26)

- Cleaned remaining HTML-visible English/internal map-caption remnants.
- Harmonized final wording in Moore-verstehen, the transformation matrix and the final method note.
- Created a raster-caption review page because embedded PNG text cannot be found by HTML audits.
- Did not modify maps, map colours, CSS or data.
