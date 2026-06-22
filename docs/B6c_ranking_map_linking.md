# B6c — Link Rankings and Map Interaction

Date: 2026-06-17

## Status

Adds cross-highlighting between hotspot ranking rows and the SVG country map.

## Interaction

- Hover/focus/click a ranking row → corresponding country on the map is highlighted.
- Hover/focus/click a country on the map → corresponding ranking row is highlighted when the country is in the top-10 ranking.
- Ranking-based highlights update the map detail text with a short prompt.

## Technical approach

- dependency-free JavaScript,
- no map library,
- no build system,
- uses `data-country` attributes on ranking rows and SVG paths,
- event delegation from the hotspot section.

## Caveat

Only countries present in the top-10 rankings can be highlighted as ranking rows. The map still contains all matched complete hotspot countries.
