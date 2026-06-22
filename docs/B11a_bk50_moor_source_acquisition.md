# B11a — BK50-Moor Source Acquisition and Staging

Date: 2026-06-17

## Goal

Prepare the first actual peat/organic-soils spatial layer for the sticky-scroll atlas.

Recommended first source:

**BK50-Moor: Feuchtgebiets- und Moorverbreitung in Baden-Württemberg**

## Why Baden-Württemberg first?

- small enough to work with,
- directly relevant to the final regional zoom,
- strong visual endpoint for the sticky-scroll sequence,
- better regional specificity than global peatland layers.

## Source facts to preserve

The BK50-Moor dataset is an extract of moor and humus-rich groundwater soils from the Baden-Württemberg soil map BK50. It is described as a revised version of the historical moor map with focus on pedological classification of developed soil types.

The dataset is offered in ESRI Shapefile and GeoPackage formats, with reference systems including EPSG:25832 and EPSG:4326, and it is licensed under **Datenlizenz Deutschland – Namensnennung – Version 2.0** with attribution to Regierungspräsidium Freiburg – LGRB.

The LGRB readme states that the map is suitable for medium-scale use around **1:25,000 to 1:50,000**, but not for local rewetting planning or parcel-level decisions without additional investigations.

## Manual download and export workflow

### 1. Download

Download BK50-Moor from the LGRB/LUBW metadata or LGRB products portal.

Preferred format:

1. GeoPackage if available,
2. Shapefile ZIP if GeoPackage is not available.

Store raw files locally under:

```text
data/external/peat_soils/bw_bk50_moor/
```

Raw data should not be committed.

### 2. Open in QGIS

Open the BK50-Moor layer.

Check that the expected attributes exist:

```text
Kurzleg
Boden
Material
area
KE
Link
```

The most important field for web classification is:

```text
Kurzleg
```

### 3. Export to GeoJSON

Export the layer as GeoJSON:

```text
data/external/peat_soils/bw_bk50_moor/bk50_moor_wgs84.geojson
```

Export settings:

```text
CRS: EPSG:4326 / WGS84
Encoding: UTF-8
Geometry: polygons/multipolygons
```

### 4. Build web layer

Run:

```powershell
python scripts\18_build_bk50_moor_web_layer_from_geojson.py
```

Expected output:

```text
public/data/bw_bk50_moor_simplified.geojson
data/processed/bw_bk50_moor_summary.csv
docs/B11b_bk50_moor_web_layer_method.md
```

## Interpretation boundary for the atlas

Suggested caveat text:

> This layer shows the medium-scale distribution of moor, moor-like and humus-rich groundwater soils in Baden-Württemberg. It is a spatial context layer, not a local rewetting suitability map.

## Next visual step

After the simplified layer exists, add it to the sticky-scroll prototype as the final zoom step:

```text
World emissions → Europe peat/wetlands → Germany organic soils → Baden-Württemberg BK50-Moor
```
