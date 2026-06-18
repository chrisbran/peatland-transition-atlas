# B15a — Europe Wetland/Peat Layer Source Acquisition and Staging

Date: 2026-06-18

## Goal

Replace the Europe placeholder in the sticky-scroll story with a real European peat/wetland context layer.

## Recommended source

European Wetland Map / Zenodo.

## Role in the story

The Europe layer should not be a high-detail analytical layer. It should function as a continental bridge between:

- global/national emissions context,
- Germany organic-soils layer,
- Baden-Württemberg BK50-Moor layer.

## Data-handling principle

For the public website, the Europe layer must be strongly filtered, dissolved and simplified.

Do **not** attempt to publish a full-resolution European wetland product directly as GeoJSON.

## Manual GIS workflow

### 1. Download

Download the European Wetland Map data.

Store raw files under:

```text
data/external/peat_soils/europe_wetland_peat/
```

Do not commit raw files.

### 2. Inspect

Open the relevant data in ArcGIS Pro or QGIS.

Identify:

```text
class field
wetland/peatland category field
format
CRS
file size
extent
```

### 3. Select/filter classes

For the sticky-story layer, select only classes relevant to peatland / organic-soil / wetland context.

Avoid using all classes if the result is too broad or too heavy.

### 4. Dissolve

Dissolve by the selected class field.

Use multipart features if available.

### 5. Simplify

Start settings:

```text
Algorithm:
Retain critical points / Douglas-Peucker

Tolerance:
2000 Meters

Minimum Area:
250000 Square Meters
```

If still too large:

```text
Tolerance:
5000 Meters

Minimum Area:
1000000 Square Meters
```

This is acceptable for a continental scrollytelling context layer.

### 6. Export to GeoJSON

Export to:

```text
data/external/peat_soils/europe_wetland_peat/europe_peat_wetland_wgs84.geojson
```

Settings:

```text
Format: GeoJSON
CRS: EPSG:4326 / WGS84
Encoding: UTF-8
```

In ArcGIS Pro:

```text
Features To JSON
Output to GeoJSON: checked
Project to WGS84: checked
Use field aliases: unchecked
Formatted JSON: unchecked
```

### 7. Build web layer

Run:

```powershell
python scripts\28_build_europe_peat_wetland_web_layer_from_geojson.py
```

Expected outputs:

```text
public/data/europe_peat_wetland_simplified.geojson
data/processed/europe_peat_wetland_summary.csv
docs/B15b_europe_peat_wetland_web_layer_method.md
```

## QA targets

```text
GeoJSON size: ideal < 8 MB, acceptable < 15 MB
Features: preferably dissolved by class
Layer purpose: continental spatial context, not site-level analysis
```

## Interpretation boundary

Suggested atlas caveat:

> This layer shows continental wetland/peat spatial context. It is not a local rewetting suitability map.
