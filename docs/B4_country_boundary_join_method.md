# B4 — Country Boundary Join

## Status

Prepared a lightweight country-level GeoJSON for the Phase B hotspot layer.

## Boundary source

Natural Earth 110m Admin 0 Countries GeoJSON.

Source URL used by script:

```text
https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson
```

## Hotspot source

```text
data\processed\country_hotspots.csv
```

## Processing

1. Load complete country-level hotspot records.
2. Download Natural Earth 110m Admin 0 Countries GeoJSON.
3. Build join indexes using:
   - M49/UN numeric codes,
   - ISO3 fields,
   - Natural Earth country names.
4. Join hotspot records to country geometries.
5. Export compact web GeoJSON.

## Outputs

- `public/data/hotspot_countries_110m.geojson`
- `data/processed/country_boundary_join_report.csv`

## Caveat

This layer visualizes national hotspot concentration only. It must not be interpreted as local rewetting suitability or farm-scale prioritization.

## Next step

B5 — add choropleth map rendering to the atlas interface.
