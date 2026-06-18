# Task B15b — Process Europe Wetland/Peat Web Layer

## Agent

Data & GIS Agent + Visualization Engineer Agent + QA Critic Agent

## Preconditions

- Europe wetland/peat data has been downloaded manually.
- Relevant classes have been selected/filterd.
- The layer has been dissolved and simplified.
- It has been exported to:

`data/external/peat_soils/europe_wetland_peat/europe_peat_wetland_wgs84.geojson`

## Run

```powershell
python scripts\28_build_europe_peat_wetland_web_layer_from_geojson.py
```

## Expected outputs

- `public/data/europe_peat_wetland_simplified.geojson`
- `data/processed/europe_peat_wetland_summary.csv`
- `docs/B15b_europe_peat_wetland_web_layer_method.md`

## QA checks

- output GeoJSON opens in browser,
- file size is acceptable for GitHub Pages,
- class field is meaningful,
- visual distribution is plausible,
- no raw files under `data/external/` are committed.

## Acceptance criteria

- Europe sticky-story step can use the real layer,
- source attribution and caveat are documented,
- layer is clearly labelled as context, not rewetting suitability.
