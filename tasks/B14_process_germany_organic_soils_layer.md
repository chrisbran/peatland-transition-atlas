# Task B14 — Process Germany Organic-Soils Layer

## Agent

Data & GIS Agent + Visualization Engineer Agent + QA Critic Agent

## Goal

Build the next real spatial layer for the sticky-scroll sequence: Germany organic soils.

## Rationale

The sticky story currently has real layers for:

- world country emissions,
- Baden-Württemberg BK50-Moor.

The Germany step is still a labelled placeholder. A national organic-soils layer would bridge the country hotspot map and the Baden-Württemberg regional zoom.

## Candidate source

Aktualisierte Kulisse organischer Böden in Deutschland, Thünen / OpenAgrar.

## Expected workflow

1. Download raw data manually to `data/external/peat_soils/germany_organic_soils/`.
2. Inspect format, CRS, attributes and license.
3. Export/reproject to WGS84 GeoJSON if needed.
4. Simplify geometry for web display.
5. Export to `public/data/germany_organic_soils_simplified.geojson`.
6. Add method note and attribution.

## Acceptance criteria

- raw files are not committed,
- public GeoJSON is small enough for GitHub Pages,
- layer class meanings are documented,
- sticky story Germany step uses the real layer,
- caveat remains visible.
