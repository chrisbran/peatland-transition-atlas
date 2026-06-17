# B3 — Hotspot Ranking Layer

Date: 2026-06-17

## Status

Interface addition for the Phase B country-level hotspot dataset.

## Input

`public/data/country_hotspots.csv`

## What the interface shows

- number of complete country records,
- selected year,
- total emissions across complete records,
- top countries by total drained-organic-soils emissions,
- top countries by emissions density.

## Why ranking first?

The atlas does not yet include a country boundary join or a choropleth map.  
A ranking layer is the fastest useful interface step because it verifies that the hotspot data load correctly in the public site before adding geometry.

## Important caveat

This is a country-level hotspot layer, not a local rewetting suitability map.

The ranking uses complete records only:

```text
emissions_total_kt_co2e != missing
```

Records with missing CO₂ or N₂O CO₂e values remain in the dataset but are excluded from rankings.

## Next step

`B4 — Prepare Natural Earth country boundary join`
