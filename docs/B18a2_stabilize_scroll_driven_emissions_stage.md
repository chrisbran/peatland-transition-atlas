# B18a2 — Stabilize Scroll-Driven Emissions Stage

Date: 2026-06-18

## Problem

The scroll-driven emissions map changed size or vertical position slightly when the active state changed. The likely cause was variable header and description height, plus different ranking/compare content heights.

## Fix

The visual stage now reserves fixed vertical space for:

- the metric header,
- the map panel,
- the ranking/compare panel,
- the source line.

This keeps the map in a stable screen position while the metric state changes from total emissions to emission density and compare mode.

## Changed files

- `src/styles.css`
- `docs/B18a2_stabilize_scroll_driven_emissions_stage.md`
- `tasks/done.md`

## Acceptance check

While scrolling through the emissions metric section:

- the map remains in a stable position,
- the map does not jump vertically,
- only the color state, title and ranking should change.
