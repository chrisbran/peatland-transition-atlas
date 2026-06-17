# B5 — Choropleth Map Layer

Date: 2026-06-17

## Status

Adds a first dependency-free country-level choropleth map to the hotspot section.

## Input

`public/data/hotspot_countries_110m.geojson`

## Rendering approach

- SVG map
- no external JavaScript map library
- equirectangular projection
- quantile color classes based on `emissions_total_kt_co2e`
- hover/click details for:
  - total emissions,
  - emissions density,
  - drained organic soils area.

## Why this simple map first?

This is a portfolio MVP. The aim is to make the hotspot layer visible on the public site without adding a build system or complex web-mapping dependency.

## Caveat

The layer is national-level only. It does not show local rewetting suitability, hydrological feasibility, land tenure or farm-scale transition constraints.

## Next step

B6 — interaction and layout refinement.
