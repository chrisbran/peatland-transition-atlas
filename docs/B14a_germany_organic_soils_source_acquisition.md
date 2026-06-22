# B14a — Germany Organic-Soils Source Acquisition and Staging

Date: 2026-06-18

## Goal

Prepare the Germany organic-soils layer for the sticky-scroll sequence.

The current sticky story has real layers for:

- world country emissions,
- Baden-Württemberg BK50-Moor.

The Germany step is still a labelled placeholder. This task prepares the Germany layer that bridges national emissions and the Baden-Württemberg regional zoom.

## Source

Recommended source:

**Aktualisierte Kulisse organischer Böden in Deutschland**  
Authors: Mareille Wittnebel, Stefan Frank, Bärbel Tiemeyer  
Repository: OpenAgrar / Thünen

## Source facts to preserve

The OpenAgrar record lists the dataset as a GeoPackage with 16 CSV files and 3 PDF files. The Thünen newsroom describes the geodata as freely downloadable from OpenAgrar, with detailed explanation of classification and aggregation of the federal-state datasets. The accompanying Working Paper states that the spatial dataset is citable on OpenAgrar and available for download.

## Manual workflow

### 1. Download

Download the dataset from OpenAgrar.

Store raw files locally under:

```text
data/external/peat_soils/germany_organic_soils/
```

Do not commit raw files.

### 2. Inspect in ArcGIS Pro or QGIS

Open the GeoPackage or extracted polygon layer.

Check:

```text
CRS
geometry type
available attribute fields
classification fields
area field
```

Likely relevant fields may include categories related to:

```text
Moorbodenkategorie
Genese
Torfmächtigkeit
mineralische Überdeckung
Abmoorigkeit
Tiefumbruch
unterlagernde Mudden
```

The processor script uses flexible field-name detection, but the inferred class field must be checked manually.

### 3. Export to GeoJSON

Export the polygon layer to:

```text
data/external/peat_soils/germany_organic_soils/germany_organic_soils_wgs84.geojson
```

Export settings:

```text
Format: GeoJSON
CRS: EPSG:4326 / WGS84
Encoding: UTF-8
```

In ArcGIS Pro, use **Features To JSON** with:

```text
Output to GeoJSON: checked
Project to WGS84: checked
Use field aliases: unchecked
```

### 4. Build web layer

Run:

```powershell
python scripts\23_build_germany_organic_soils_web_layer_from_geojson.py
```

Expected outputs:

```text
public/data/germany_organic_soils_simplified.geojson
data/processed/germany_organic_soils_summary.csv
docs/B14b_germany_organic_soils_web_layer_method.md
```

## Interpretation boundary

Suggested atlas caveat:

> This layer shows the national distribution of organic soils in Germany. It is a spatial context layer, not a local rewetting suitability map.

## QA focus

The important QA issue is not only whether the layer displays. The important issue is whether the selected classification field is meaningful for the story.

Before using the layer in the public sticky-scroll step, inspect:

```text
class names
area field units
geometry simplification quality
file size
visual distribution
```
