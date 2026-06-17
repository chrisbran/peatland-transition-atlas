# B6a — Hotspot Layout Refinement

Date: 2026-06-17

## Reason

After B5, the hotspot map loaded correctly, but the sticky header created a visual problem in long full-page screenshots. It appeared again inside the page and overlapped the hotspot section.

## Change

- Disabled sticky header behavior for this static portfolio prototype.
- Added spacing around the hotspot section.
- Improved responsive behavior for hotspot rankings and legend.
- Kept the dependency-free SVG map approach.

## Status

This is a visual/layout refinement only. It does not change the hotspot data or the choropleth join.

## Next possible refinement

- Add toggle: total emissions vs emissions density.
- Link map hover with ranking rows.
- Improve country tooltip.
