# Task B8b — Projection and Map Geometry Review

## Agent

Visualization Engineer Agent + QA Critic Agent

## Goal

Review whether the current equirectangular SVG projection is good enough for the portfolio version or whether a more appropriate world projection should be implemented.

## Issues

- High-latitude countries are visually exaggerated.
- Country areas are not visually comparable in the current projection.
- Small countries and archipelagos are difficult to select.
- A more cartographically balanced projection may improve visual credibility.

## Candidate options

1. Keep current equirectangular projection and document limitation.
2. Implement a simple Robinson/Natural Earth-style approximation without external dependencies.
3. Use pre-projected simplified SVG/GeoJSON geometry.
4. Move to a lightweight mapping library only if needed.

## Acceptance criteria

- no heavy framework unless clearly justified,
- static GitHub Pages deployment remains functional,
- map caveat remains visible,
- visual credibility improves without overengineering.
