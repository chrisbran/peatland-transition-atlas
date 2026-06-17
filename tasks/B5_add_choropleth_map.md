# Task B5 — Add Choropleth Map to Atlas Interface

## Agent

Visualization Engineer Agent

## Goal

Render `public/data/hotspot_countries_110m.geojson` as a simple interactive choropleth layer.

## Inputs

- `public/data/hotspot_countries_110m.geojson`
- existing hotspot ranking interface

## Required outputs

- map panel in the hotspot section
- legend for emissions_total_kt_co2e or hotspot_class
- hover/click detail for country, total emissions, density and area
- caveat text that the layer is country-level only

## Acceptance criteria

- page still works as static GitHub Pages site,
- no heavy build framework required,
- map loads from public/data,
- missing/unmatched countries are documented.
