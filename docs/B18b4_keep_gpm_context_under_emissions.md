# B18b4 — Keep GPM2 Context Visible Beneath Emissions Overlays

Date: 2026-06-18

## Purpose

The central global map now uses transparent ArcGIS PNG overlays. With true alpha transparency, the GPM2 peatland context can remain visible underneath the emissions layers without creating the previous milky haze.

## Change

The CSS state logic is refined so that:

- `global_gpm2_peat_extent.png` remains visible in total-emissions and density states;
- emissions overlays remain dominant but semi-transparent enough to reveal peatland context;
- country borders remain visible for orientation;
- CSS filters are explicitly disabled, because the visual quality should now come from the ArcGIS-rendered PNGs, not browser post-processing.

## State opacity logic

| State | GPM2 | Total | Density | Borders |
|---|---:|---:|---:|---:|
| Extent | 1.00 | 0.00 | 0.00 | 0.82 |
| Total emissions | 0.58 | 0.86 | 0.00 | 0.96 |
| Emission density | 0.58 | 0.00 | 0.86 | 0.96 |
| Compare | 0.42 | 0.62 | 0.58 | 1.00 |

## Acceptance check

The map should now show:

1. peatland extent as a persistent geographic context;
2. emissions as the dominant analytical layer;
3. country borders clearly enough for orientation;
4. no milky overlay or browser filter artefacts.
