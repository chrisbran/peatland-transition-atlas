# Task B19d - Bind Germany / Thuenen Frame to Central Sticky Story

## Goal

Bind the Germany / Thuenen frame into the existing central sticky map story after the Germany PNG layers have been exported and validated.

## Required assets

- `public/maps/germany/germany_admin_context.png`
- `public/maps/germany/germany_thuenen_moor_extent.png`
- `public/maps/germany/germany_thuenen_moor_types.png`

All files must be:

- 1600 x 900 px
- PNG
- RGBA
- transparent background
- exported from the same Germany layout frame

## Planned story states

1. `germany-context`
   - hides global and Europe layers
   - shows Germany admin / federal-state context

2. `germany-thuenen-extent`
   - shows the Thuenen Kulisse as one national extent layer
   - overlays Germany admin context

3. `germany-thuenen-types`
   - shows the Thuenen Kulisse by moor / soil type
   - overlays Germany admin context
