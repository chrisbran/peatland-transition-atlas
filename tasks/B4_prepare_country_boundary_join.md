# Task B4 — Prepare Natural Earth Country Boundary Join

## Agent

Data & GIS Agent + Visualization Engineer Agent

## Goal

Prepare the first geographic choropleth layer for the Phase B hotspot data.

## Inputs

- `public/data/country_hotspots.csv`
- Natural Earth Admin 0 country boundaries
- ISO/M49/country-name join table

## Required outputs

- lightweight country boundary GeoJSON for web use
- join method note
- list of unmatched countries
- updated hotspot interface with choropleth map

## Acceptance criteria

- raw large geodata are not committed,
- web GeoJSON is small enough for GitHub Pages,
- country joins are documented,
- missing/unmatched countries are visible,
- the map does not imply local rewetting suitability.
