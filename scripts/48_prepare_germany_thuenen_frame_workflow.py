#!/usr/bin/env python3
r"""
48 - Prepare Germany Thuenen frame workflow.

Run from repository root:
  python scripts\48_prepare_germany_thuenen_frame_workflow.py

This prepares folders/docs/tasks for the Germany frame.
It does not change the website story yet.
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

README = """# Germany map frame assets

This folder contains exported transparent PNG layers for the Germany / Thuenen frame.

Required production assets:

- `germany_admin_context.png`
- `germany_thuenen_moor_extent.png`
- `germany_thuenen_moor_types.png`

Export requirements:

- Export from `GERMANY_LAYOUT_V1`, not from Map View
- Same layout frame for all layers
- Same extent and bookmark for all layers
- Target size: 1600 x 900 px
- PNG
- 32-bit with Alpha
- Transparent background: on
- Clip to graphics extent: off

Do not store raw GIS data in this folder.
"""

DOC = """# B19c - Germany / Thuenen Frame Workflow

Date: {date}

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
"""

TASK = """# Task B19d - Bind Germany / Thuenen Frame to Central Sticky Story

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
"""

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    germany_dir = root / "public" / "maps" / "germany"
    germany_dir.mkdir(parents=True, exist_ok=True)

    write(germany_dir / "README.md", README)
    write(root / "docs" / "B19c_germany_thuenen_frame_workflow.md", DOC.format(date=TODAY))
    write(root / "tasks" / "B19d_bind_germany_thuenen_frame_to_central_story.md", TASK)

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B19c completed" not in done_text:
        done_text += f"- {TODAY}: Task B19c completed - prepared Germany / Thuenen frame workflow.\n"
        write(done, done_text)

    print("B19c Germany / Thuenen frame workflow prepared.")
    print("Created/updated:")
    print("  public/maps/germany/README.md")
    print("  docs/B19c_germany_thuenen_frame_workflow.md")
    print("  tasks/B19d_bind_germany_thuenen_frame_to_central_story.md")
    print("  tasks/done.md")
    print()
    print("Next export from ArcGIS:")
    print("  public/maps/germany/germany_admin_context.png")
    print("  public/maps/germany/germany_thuenen_moor_extent.png")
    print("  public/maps/germany/germany_thuenen_moor_types.png")

if __name__ == "__main__":
    main()
