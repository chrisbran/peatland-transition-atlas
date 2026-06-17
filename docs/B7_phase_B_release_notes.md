# Phase B Release Notes — v0.2.0 Draft

Date: 2026-06-17

## Release title

`v0.2.0 — Country-level hotspot atlas draft`

## Summary

This release adds the first data-backed hotspot layer to the Peatland Transition Atlas. The prototype now moves beyond literature/evidence mapping and includes a country-level drained organic soils emissions layer.

## Main additions

- `country_hotspots.csv`: country-level hotspot dataset.
- `hotspot_countries_110m.geojson`: lightweight GeoJSON for web mapping.
- Hotspot metrics:
  - total emissions,
  - emissions density.
- Interactive hotspot section:
  - key metrics,
  - choropleth map,
  - ranking cards,
  - metric toggle,
  - linked ranking/map highlighting.

## Interpretation boundary

The hotspot layer is a national screening layer. It does not identify parcels, farms or local rewetting opportunities.

The map must not be interpreted as:

- local suitability,
- hydrological feasibility,
- investment readiness,
- farm-scale transition advice.

## Known limitations

- Some small territories remain unmatched in the boundary join.
- The map uses Natural Earth 110m geometry and a simple SVG projection.
- Colors and highlight states are provisional.
- Ranking-map interaction is functional but should be visually refined later.
- Country-name and M49 joins should be reviewed before scientific publication use.

## Suggested GitHub release description

```text
This release adds the first country-level drained organic soils hotspot layer to the Peatland Transition Atlas.

New features:
- public hotspot dataset,
- Natural Earth country boundary join,
- choropleth map,
- total-emissions vs emissions-density toggle,
- ranking/map interaction.

The hotspot layer is intended as a national screening layer. It is not a local rewetting suitability map.
```
