# B19a — Europe Frame Workflow

Date: 2026-06-18

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
