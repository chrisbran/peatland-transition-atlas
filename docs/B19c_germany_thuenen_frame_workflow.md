# B19c - Germany / Thuenen Frame Workflow

Date: 2026-06-19

## Purpose

Prepare the Germany frame as the national implementation scale after Global and Europe.

The Germany frame uses the Thuenen peat / organic-soils Kulisse as the thematic layer. It should be exported as transparent, aligned PNG layers and later bound into the central sticky map story.

## Required web assets

Export these files:

- `public/maps/germany/germany_admin_context.png`
- `public/maps/germany/germany_thuenen_moor_extent.png`
- `public/maps/germany/germany_thuenen_moor_types.png`

## ArcGIS setup

Map:

`GERMANY_FRAME_V1`

Recommended projection:

`ETRS 1989 LAEA Europe / EPSG:3035`

Layout:

`GERMANY_LAYOUT_V1`

If ArcGIS uses centimeters:

- Width: 40.64 cm
- Height: 22.86 cm

The map frame should fill the page:

- X: 0 cm
- Y: 0 cm
- Width: 40.64 cm
- Height: 22.86 cm

Use bookmark:

`GERMANY_FRAME_V1`

## Layer logic

### 1. Admin context

Export file:

`germany_admin_context.png`

Visible layers:

- NUTS 1 Germany / federal-state boundaries
- optional Germany outer boundary / neighboring country context if very subtle

Hidden layers:

- Thuenen extent
- Thuenen types
- basemaps
- hillshade

### 2. Thuenen extent

Export file:

`germany_thuenen_moor_extent.png`

Visible layers:

- Thuenen_extent as one single symbol

Suggested color:

- `#2F6B4F`

Hidden layers:

- NUTS
- country borders
- Thuenen types
- basemaps
- hillshade

### 3. Thuenen types

Export file:

`germany_thuenen_moor_types.png`

Visible layers:

- Thuenen_types symbolized by `KAT_LANG` or `KAT_KURZ`

Suggested palette:

- Hochmoorboden: `#6E4B78`
- Moorfolgeboden: `#8E7A4D`
- Niedermoorboden: `#2F6B4F`
- Tiefumbruchboden aus Hochmoor: `#8A5A63`
- Tiefumbruchboden aus Niedermoor: `#1F7A5C`
- flach ueberdeckter Hochmoorboden: `#9B7F8D`
- flach ueberdeckter Niedermoorboden: `#6F9A78`
- maechtig ueberdeckter Hochmoorboden: `#B08B6C`
- maechtig ueberdeckter Niedermoorboden: `#B7A15A`

Hidden layers:

- NUTS
- country borders
- Thuenen extent
- basemaps
- hillshade

## Export settings

Use `Share -> Export Layout`, not `Export Map`.

Settings:

- File type: PNG
- Resolution: 100 DPI
- Width: 1600 px
- Height: 900 px
- Color depth: 32-bit with Alpha
- Transparent background: on
- Clip to graphics extent: off

## Validation

Run from repository root:

```powershell
python -c "from PIL import Image; from pathlib import Path; [print(p.name, Image.open(p).mode, Image.open(p).size, Image.open(p).getchannel('A').getextrema() if Image.open(p).mode == 'RGBA' else 'NO ALPHA') for p in Path('public/maps/germany').glob('*.png')]"
```

Expected:

```text
germany_admin_context.png RGBA (1600, 900) (...)
germany_thuenen_moor_extent.png RGBA (1600, 900) (...)
germany_thuenen_moor_types.png RGBA (1600, 900) (...)
```

## Acceptance criteria

- All three PNGs are 1600 x 900 px.
- All three PNGs are RGBA and transparent.
- Germany is not clipped.
- Layers are aligned.
- The admin context is subtle.
- The extent layer is readable as one national Kulisse.
- The types layer is differentiated but not visually overloaded.

## Next task

B19d / Script 49 will bind these Germany / Thuenen assets into the central sticky story.
