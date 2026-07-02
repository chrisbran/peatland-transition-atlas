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

- ` M tasks/done.md`
- `?? docs/B175_post_publication_review_pass.md`
- `?? docs/B175_post_publication_review_pass_audit.txt`
- `?? docs/B175_publication_review_checklist.md`
- `?? docs/B175_review_candidates.csv`
- `?? docs/B175_section_inventory.csv`
- `?? scripts/175_post_publication_review_pass.py`

## 7. Suggested add list for this milestone

- `index.html`
- `src/styles.css`
- `src/b169_live_sticky_zoom.js`
- `public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png`
- `scripts/58_visual_qa_and_commit_check.py`
- `tasks/done.md`

## Result

PASS
