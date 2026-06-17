# Task B8 — Visual and Cartographic Refinement

## Agent

Visualization Engineer Agent + QA Critic Agent

## Goal

Improve the visual quality of the hotspot map after the Phase B MVP is functional.

## Issues to review

- Highlight color is currently too bright/neon.
- Ocean and dark land/desert/background areas are not sufficiently distinguishable.
- The current equirectangular world map visually distorts high-latitude countries.
- Some small countries and fragmented archipelagos are hard to interact with.
- No-data and missing-geometries treatment should be clearer.

## Candidate improvements

- softer selected-country highlight color,
- separate ocean/background color,
- subtle base land fill for all countries,
- improved color ramp for total and density modes,
- optional Robinson/Natural Earth-style projection if implemented without heavy dependencies,
- fixed selected-country details panel instead of relying mainly on hover.

## Acceptance criteria

- map remains static and GitHub Pages compatible,
- no heavy framework is introduced,
- palette is readable but not visually aggressive,
- country-level caveat remains visible.
