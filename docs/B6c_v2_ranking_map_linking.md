# B6c v2 — Robust Ranking-Map Linking

Date: 2026-06-17

## Problem

The first B6c patch did not create a clearly visible new interaction. In practice, map hover showed neon borders, but ranking-map cross-highlighting was not reliably visible.

## Change

Replaced the hotspot JavaScript module with one integrated implementation.

The module now handles:

- ranking rendering,
- country-level choropleth rendering,
- metric toggle,
- legend updates,
- shared `data-country-key` identifiers,
- ranking-to-map highlighting,
- map-to-ranking highlighting.

## Interaction

- Hover/focus/click a ranking row highlights the matching country on the map.
- Hover/focus/click a country highlights matching ranking rows when the country is present in the top-10 list.
- The details text updates to the active country and selected metric.

## Visual change

The active country now receives both a stronger stroke and a temporary fill override. This is more visible than boundary-only highlighting.

## Caveat

Only countries present in the current top-10 rankings can be highlighted as ranking rows. The map itself contains all matched hotspot countries.
