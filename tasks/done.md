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
