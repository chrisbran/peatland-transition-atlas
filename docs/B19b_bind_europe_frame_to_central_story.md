# B19b — Bind Europe Frame to Central Sticky Story

Date: 2026-06-19

## Purpose

Bind the newly exported Europe frame into the existing central sticky map story.

## Input assets

Required files:

- `public/maps/europe/europe_country_borders.png`
- `public/maps/europe/europe_gpm2_peat_extent.png`

Both must be exported from the same Europe layout frame and must be exactly 1600 × 900 px.

## Added story states

1. `europe-borders`
   - hides global layers
   - shows the Europe country-boundary frame only

2. `europe-peat`
   - shows European peat extent
   - overlays Europe country borders

## Design decision

Europe is not treated as a zoomed-in global PNG. It is a separate regional frame, but it is displayed inside the same central sticky stage. This keeps the interface calm while allowing a better projection and higher regional clarity.

## Acceptance check

When scrolling through the central map story, the sequence should now read:

1. global peat extent
2. global total emissions
3. global emission density
4. interpretation
5. Europe borders
6. Europe peat extent
