# B94 - Oberschwaben Data Access Questions

Date: 2026-06-23

## 1. Purpose

This document lists the data-access questions that must be answered before B95 builds map assets.

## 2. Agricultural land-use data

### Preferred source anchor

**Gemeinsamer Antrag Baden-Württemberg / MLR, 2024**

### Questions

1. Do we have access to the same or equivalent data used in the SOLAMO flyer map?
2. Are the data available as polygons, raster, or already-generalised categories?
3. Can the data be displayed publicly on GitHub Pages?
4. Are there restrictions against parcel-level display?
5. Is aggregation or generalisation required?
6. Can we classify into:
   - Ackerland,
   - Grünland,
   - Dauerkultur?
7. Are there additional categories that should be hidden or merged?

### Recommended first decision

If detailed polygons are sensitive or restricted, create a **generalised visual layer** or use coarser public land-cover data.

## 3. Moor-/soil-context data

### Preferred source anchor

**Feuchtgebiete und Moore der Bodenkarte Baden-Württemberg / GeoLa BK50MOOR / LGRB, 2025**

### Questions

1. Do we have the same BK50MOOR/GeoLa layer referenced by the flyer?
2. Is it available as vector data, raster data, WMS, or only as map service?
3. Can it be exported as a public PNG context layer?
4. Which classes should be included?
5. Should the first version merge all relevant types into one class:
   `Moor-/Feuchtbodenkontext`?
6. Is a distinction between Niedermoor, Hochmoor, Anmoor, Gley etc. needed now or later?

### Recommended first decision

Use one merged and methodically cautious class for the first version.

## 4. Administrative base

### Preferred source anchor

**BKG, 2026**

### Questions

1. Which district-boundary layer should be used?
2. Do we already have a suitable NUTS/administrative layer in the repo/workflow?
3. Should the first map show only the four districts or some surrounding context?
4. Which label names should be used:
   - Ravensburg,
   - Biberach,
   - Sigmaringen,
   - Bodenseekreis?

### Recommended first decision

Use four-district focus with subtle surrounding context only if needed for orientation.

## 5. Derived intersection layer

### Questions

1. Should the first B95 output be visual-only or include calculated hectares?
2. If hectares are calculated, what projection/equal-area CRS will be used?
3. Should the intersection be clipped to agricultural use only or stratified by land-use class?
4. How much geometry simplification is appropriate for public display?
5. Should the intersection be shown as exact polygons or generalised patches?

### Recommended first decision

Start with a visual composite map. Add hectare indicators only after source rights and geometry definitions are stable.

## 6. Minimum data-decision checklist before B95

B95 may proceed if these are answered:

- [ ] agriculture source chosen,
- [ ] soil/moor context source chosen,
- [ ] public display rights acceptable,
- [ ] four county boundary source chosen,
- [ ] first output type chosen: visual-only or visual + indicators,
- [ ] legend wording approved,
- [ ] method boundary approved.
