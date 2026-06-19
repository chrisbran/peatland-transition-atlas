# B18b-new — Central Global Map Story

Date: 2026-06-18

## Purpose

Replace the growing multi-map approach with one central scroll-driven global map stage.

## Input assets

All map assets must be exported from the same ArcGIS `GLOBAL_FRAME_V1` layout:

- `public/maps/global/global_gpm2_peat_extent.png`
- `public/maps/global/global_hotspots_total.png`
- `public/maps/global/global_hotspots_density.png`
- `public/maps/global/global_country_borders.png`

All files must be exactly 1600 x 900 px.

## Design decision

The map frame, projection and placement remain fixed. Scroll states only change layer opacity and the explanatory text.

## Story states

1. Extent — GPM 2.0 peatland context.
2. Total emissions — absolute drained-organic-soil emissions.
3. Emission density — pressure relative to mapped drained organic-soil area.
4. Compare — both views are needed for prioritisation.

## Removed/replaced

The script removes earlier experimental sections if present:

- `#emissionsMetricScrolly`
- `#mapEvidencePanels`

It also removes script tags for:

- `src/emissions_metric_scrolly.js`
- `src/map_evidence_panels.js`

The files themselves are not deleted automatically.
