# B6b — Toggle Total Emissions vs Emissions Density

Date: 2026-06-17

## Status

Adds a metric toggle to the hotspot choropleth map.

## Available map modes

1. `Total emissions`
   - field: `emissions_total_kt_co2e`
   - shows national-scale hotspot magnitude

2. `Emissions density`
   - field: `emissions_density_t_co2e_per_ha`
   - shows intensity per hectare of drained organic soils

## Why this matters

Total emissions highlight large national hotspots.  
Emissions density highlights where drained organic soils are especially emission-intensive per unit area.

Together, the two views prevent the map from implying that the largest national emitters are always the most intensive land-use systems.

## Technical approach

- no external map library,
- no build system,
- reuses `public/data/hotspot_countries_110m.geojson`,
- recolors the SVG choropleth by quantiles for the selected metric,
- updates legend and hover/click details.

## Caveat

Both modes remain national-level summaries. Neither mode shows local hydrological feasibility, farm-scale land-use transition potential or rewetting suitability.
