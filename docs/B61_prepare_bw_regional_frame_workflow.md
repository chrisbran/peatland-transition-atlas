# B61 - Prepare BW / Regional Frame Workflow

Date: 2026-06-19

## Purpose

Prepare the next scale in the Peatland Transition Atlas story:

```text
Global -> Europe -> Germany / Thuenen -> Baden-Wuerttemberg / regional soil frame
```

The current Germany / Thuenen block establishes national implementation geography. The next step should show why national layers are still too coarse for local planning and why a regional soil frame is needed.

## Target narrative

The BW / regional frame should make one argument:

> National peatland layers identify the implementation arena, but local decisions depend on higher-resolution soil geography, hydrological feasibility, and land-use context.

## Proposed story cards

### 10 - Regional implementation frame

**Heading**

Regional planning needs a finer spatial frame.

**Text**

Germany identifies the national target geography, but implementation decisions are made at much finer scales. Baden-Wuerttemberg provides a test frame for linking national peatland policy to regional soil information, land-use constraints, and local transition pathways.

### 11 - BK50 / regional peat extent

**Heading**

The regional peat and organic-soils footprint is spatially specific.

**Text**

A one-colour regional extent layer should first establish where peat and organic soils occur within the regional planning frame. This creates the local target geography for mitigation and adaptation options.

### 12 - Soil context and transition feasibility

**Heading**

Local soil context changes what transition can mean.

**Text**

At regional scale, the relevant question is no longer only where peat soils are located. Soil type, depth, cover, drainage context, and surrounding land use shape which pathways are technically plausible and which require further evidence.

## Required map assets

Create these web-ready transparent PNGs:

```text
public/maps/bw/bw_admin_context.png
public/maps/bw/bw_bk50_moor_extent.png
public/maps/bw/bw_bk50_moor_types_or_soil_context.png
```

All should be:

```text
1600 x 900 px
RGBA / 32-bit with alpha
transparent background
same extent
same projection
same layout frame
```

## ArcGIS export guidance

Use the same 16:9 export logic as for Europe and Germany:

```text
Layout width: 40.64 cm
Layout height: 22.86 cm
Map frame: full layout
Export: PNG
Resolution: 100 DPI
Color depth: 32-bit with Alpha
Transparent background: ON
Clip to graphics extent: OFF
```

## Visual hierarchy

The regional frame should be calmer than the national Germany map:

- admin context: thin warm-grey lines, low opacity
- extent layer: one muted peat/green tone
- type/context layer: limited palette, no rainbow colours
- avoid dense labels unless necessary

## Acceptance criteria for next binding step

Before binding the BW frame into the central story, check:

- all three PNGs exist
- all three are 1600 x 900
- all three are RGBA / transparent
- all three align exactly
- the extent layer is visually distinct from the type/context layer
- legend is either unnecessary or clearly mapped to visible colours
