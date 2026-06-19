#!/usr/bin/env python3
"""
B19a — Prepare Europe frame workflow.

Run from repository root:

    python scripts\\46_prepare_europe_frame_workflow.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

DOC = f"""# B19a — Europe Frame Workflow

Date: {TODAY}

## Goal

Prepare the next scrolly-map stage: a **Europe frame** that follows the global frame.
The Europe frame should use the same basic logic as the central global map:

- fixed map area
- dark background
- aligned PNG exports from ArcGIS Pro
- simple layer swapping in the web front-end

## Why this step comes next

The global frame is now stable enough to serve as the visual entry point.
The next story movement should narrow the scale from:

1. global peatland extent and hotspot comparison
2. to Europe as the first regional frame
3. then later to Germany
4. then Baden-Württemberg

This keeps the scale transition logical and easier to follow.

## Output folders

This workflow creates / uses:

- `public/maps/europe/`
- `data/external/arcgis_work/europe_frame_exports/`

## Expected Europe export files

Please export the following PNG files from ArcGIS Pro into `public/maps/europe/`:

1. `europe_country_borders.png`
   - Europe frame with country borders only
   - transparent background
   - no labels

2. `europe_gpm2_peat_extent.png`
   - Global Peatland Map 2.0 clipped / shown in Europe extent
   - transparent background
   - country borders may remain **off** in this layer if they are exported separately

Optional later:

3. `europe_context_labels.png`
   - only if a very sparse labeling layer is needed later
   - not required for B19a/B19b

## ArcGIS Pro setup recommendation

### 1. Duplicate the global frame logic

Use the same visual export logic as for the global frame:

- same dark-site target in mind
- same PNG export type
- same canvas size
- transparent background

### 2. Create a new Europe map / bookmark

Suggested names:

- map: `EUROPE_FRAME_V1`
- bookmark: `EUROPE_FRAME_V1`

### 3. Projection and export consistency

Use the same projection family as your Europe map decision in ArcGIS Pro.
What matters most for the web step is:

- all Europe PNGs must have the **same extent**
- all Europe PNGs must have the **same pixel size**
- all Europe PNGs must align perfectly when stacked

Recommended export size:

- **1600 × 900 px**

This matches the global exports and simplifies CSS handling.

### 4. Recommended layer exports

#### A. Country borders export

Visible layers:

- `world_countries_110m_base` (or the Europe equivalent in the map)

Style recommendation:

- no fill
- subtle warm light outline
- thin stroke
- transparent map background

Export to:

- `public/maps/europe/europe_country_borders.png`

#### B. GPM2 peat extent export

Visible layers:

- `peatGPA22WGS_2cl.tif`
- optional country borders only if needed for orientation, but preferably keep borders separate

Style recommendation:

- keep the darker site palette that worked on the global frame
- preserve the two-class distinction:
  - peat dominated
  - peat in soil mosaic

Export to:

- `public/maps/europe/europe_gpm2_peat_extent.png`

## Acceptance checks before web integration

Before proceeding to B19b, please verify:

1. both files exist in `public/maps/europe/`
2. both files have identical dimensions
3. both files visually align when toggled
4. borders are readable on the dark site background
5. peat extent is visible but not over-bright

## PowerShell check

From repository root:

```powershell
Get-Item public\maps\europe\*.png |
  Select-Object Name,Length

python -c "from PIL import Image; from pathlib import Path; [print(p.name, Image.open(p).size) for p in Path('public/maps/europe').glob('*.png')]"
```

## Next step

After the two Europe PNGs are exported and validated, continue with:

- **B19b — Bind Europe frame to sticky story**
"""

TASK = """# Task B19b — Bind Europe Frame to Sticky Story

## Goal

Integrate a Europe stage into the story directly after the global frame.

## Intended story logic

1. Global extent
2. Global total emissions
3. Global emissions density
4. Europe frame appears
5. Europe peat extent is shown with country borders
6. Short text explains that the story is now moving from global comparison to regional structure
7. Next transition later goes to Germany

## Requirements

- reuse the central-map logic where possible
- avoid adding a second competing map panel
- keep one dominant map stage
- keep the text concise
- maintain responsive behaviour

## Acceptance criteria

- Europe frame appears as a clean continuation of the global story
- PNG switching is stable and does not flicker
- Europe borders improve orientation
- the scale change from world to Europe is obvious and calm
"""

README = """# Europe frame exports

Put aligned Europe PNG exports here.

Expected files for B19a/B19b:

- europe_country_borders.png
- europe_gpm2_peat_extent.png

Recommended export size:

- 1600 x 900 px

All files must share the same extent and pixel dimensions.
"""


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    root = Path.cwd()
    if not (root / 'index.html').exists():
        raise SystemExit('Run from repository root. index.html not found.')

    public_dir = root / 'public' / 'maps' / 'europe'
    external_dir = root / 'data' / 'external' / 'arcgis_work' / 'europe_frame_exports'
    docs_path = root / 'docs' / 'B19a_europe_frame_workflow.md'
    task_path = root / 'tasks' / 'B19b_bind_europe_frame_to_sticky_story.md'
    readme_path = public_dir / 'README.md'

    public_dir.mkdir(parents=True, exist_ok=True)
    external_dir.mkdir(parents=True, exist_ok=True)

    write(docs_path, DOC)
    write(task_path, TASK)
    write(readme_path, README)

    done = root / 'tasks' / 'done.md'
    done_text = read(done) if done.exists() else '# Done\n'
    marker = 'Task B19a completed'
    if marker not in done_text:
        done_text += f'- {TODAY}: Task B19a completed — prepared Europe frame workflow and export folders.\n'
        write(done, done_text)

    print('B19a Europe frame workflow prepared.')
    print('Changed/created:')
    print('  public/maps/europe/README.md')
    print('  docs/B19a_europe_frame_workflow.md')
    print('  tasks/B19b_bind_europe_frame_to_sticky_story.md')
    print('  tasks/done.md')
    print('  data/external/arcgis_work/europe_frame_exports/')
    print()
    print('Next:')
    print('  1. Export aligned Europe PNGs into public/maps/europe/')
    print('  2. Verify both are the same size')
    print('  3. Continue with B19b')


if __name__ == '__main__':
    main()
