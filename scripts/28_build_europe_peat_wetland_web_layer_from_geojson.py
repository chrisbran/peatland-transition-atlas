#!/usr/bin/env python3
r"""
B15b — Build a web-ready Europe peat/wetland context layer from a GIS-exported GeoJSON.

Input expected:
  data/external/peat_soils/europe_wetland_peat/europe_peat_wetland_wgs84.geojson

Recommended GIS preparation:
  1. Download European Wetland Map data.
  2. Select only peatland / organic-soil / relevant wetland classes for the atlas.
  3. Dissolve by the selected class field.
  4. Simplify for continental overview.
  5. Export to EPSG:4326 GeoJSON.

Run:
  python scripts\28_build_europe_peat_wetland_web_layer_from_geojson.py

Outputs:
  public/data/europe_peat_wetland_simplified.geojson
  data/processed/europe_peat_wetland_summary.csv
  docs/B15b_europe_peat_wetland_web_layer_method.md

No external Python dependencies.
"""

from pathlib import Path
import csv
import datetime
import json
import math


TODAY = datetime.date.today().isoformat()

INPUT = Path("data/external/peat_soils/europe_wetland_peat/europe_peat_wetland_wgs84.geojson")
OUTPUT = Path("public/data/europe_peat_wetland_simplified.geojson")
SUMMARY = Path("data/processed/europe_peat_wetland_summary.csv")
METHOD = Path("docs/B15b_europe_peat_wetland_web_layer_method.md")

# Continental overview simplification. Adjust upward if output is still too large.
SIMPLIFY_TOLERANCE = 0.02

CLASS_CANDIDATES = [
    "class", "Class", "CLASS", "klasse", "Klasse",
    "wetland", "Wetland", "wetland_type", "WetlandType", "WETLAND_TYPE",
    "peatland", "Peatland", "peat_type", "PEAT_TYPE",
    "category", "Category", "CATEGORY",
    "type", "Type", "TYPE",
    "label", "Label", "LABEL",
    "name", "Name", "NAME",
    "legend", "Legend", "LEGEND",
    "gridcode", "GRIDCODE", "code", "Code", "CODE"
]

AREA_CANDIDATES = [
    "area_ha", "AREA_HA", "ha", "HA",
    "area", "Area", "AREA",
    "Shape_Area", "SHAPE_Area", "shape_area",
    "Flaeche", "Fläche", "FLAECHE"
]


def point_line_distance(point, start, end):
    x, y = point[:2]
    x1, y1 = start[:2]
    x2, y2 = end[:2]

    if x1 == x2 and y1 == y2:
        return math.hypot(x - x1, y - y1)

    num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    den = math.hypot(y2 - y1, x2 - x1)
    return num / den


def douglas_peucker(points, tolerance):
    if len(points) <= 3:
        return points

    closed = points[0][:2] == points[-1][:2]
    work = points[:-1] if closed else points

    if len(work) <= 3:
        return points

    max_dist = 0
    index = 0
    for i in range(1, len(work) - 1):
        dist = point_line_distance(work[i], work[0], work[-1])
        if dist > max_dist:
            max_dist = dist
            index = i

    if max_dist > tolerance:
        left = douglas_peucker(work[: index + 1], tolerance)
        right = douglas_peucker(work[index:], tolerance)
        result = left[:-1] + right
    else:
        result = [work[0], work[-1]]

    if closed:
        if result[0][:2] != result[-1][:2]:
            result.append(result[0])
        if len(result) < 4:
            return points

    return result


def simplify_geometry(geom, tolerance):
    if not geom:
        return geom

    gtype = geom.get("type")
    coords = geom.get("coordinates")

    if gtype == "Polygon":
        return {"type": "Polygon", "coordinates": [douglas_peucker(ring, tolerance) for ring in coords]}

    if gtype == "MultiPolygon":
        return {
            "type": "MultiPolygon",
            "coordinates": [
                [douglas_peucker(ring, tolerance) for ring in poly]
                for poly in coords
            ],
        }

    return geom


def first_existing(props, candidates, default=""):
    lower_lookup = {str(k).lower(): k for k in props.keys()}

    for key in candidates:
        if key in props and props.get(key) not in (None, ""):
            return props.get(key)

    for key in candidates:
        actual = lower_lookup.get(str(key).lower())
        if actual is not None and props.get(actual) not in (None, ""):
            return props.get(actual)

    return default


def numeric(value):
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def feature_bbox(geom):
    xs, ys = [], []

    def visit(obj):
        if not isinstance(obj, list):
            return
        if obj and isinstance(obj[0], (int, float)) and len(obj) >= 2:
            xs.append(obj[0])
            ys.append(obj[1])
        else:
            for item in obj:
                visit(item)

    if geom:
        visit(geom.get("coordinates"))

    if not xs:
        return None

    return [min(xs), min(ys), max(xs), max(ys)]


def count_vertices(geom):
    total = 0

    def visit(obj):
        nonlocal total
        if not isinstance(obj, list):
            return
        if obj and isinstance(obj[0], (int, float)) and len(obj) >= 2:
            total += 1
        else:
            for item in obj:
                visit(item)

    if geom:
        visit(geom.get("coordinates"))

    return total


def main():
    if not INPUT.exists():
        raise SystemExit(
            f"Input not found: {INPUT}\n"
            "Export a filtered/dissolved/simplified Europe wetland/peat layer as EPSG:4326 GeoJSON first."
        )

    with INPUT.open("r", encoding="utf-8") as f:
        geo = json.load(f)

    features = geo.get("features", [])
    if not features:
        raise SystemExit("Input GeoJSON has no features.")

    out_features = []
    summary = {}
    vertices_before = 0
    vertices_after = 0

    for feat in features:
        props = feat.get("properties", {}) or {}
        klass = str(first_existing(props, CLASS_CANDIDATES, "Peat/wetland context")).strip() or "Peat/wetland context"
        area_raw = first_existing(props, AREA_CANDIDATES, "")
        area_num = numeric(area_raw)

        geom_in = feat.get("geometry")
        vertices_before += count_vertices(geom_in)
        geom = simplify_geometry(geom_in, SIMPLIFY_TOLERANCE)
        vertices_after += count_vertices(geom)
        bbox = feature_bbox(geom)

        summary.setdefault(klass, {"feature_count": 0, "area_sum_raw": 0.0})
        summary[klass]["feature_count"] += 1
        if area_num is not None:
            summary[klass]["area_sum_raw"] += area_num

        new_props = {
            "class": klass,
            "source_area": area_raw,
        }

        if bbox:
            new_props["bbox"] = bbox

        out_features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": geom,
        })

    output_geo = {
        "type": "FeatureCollection",
        "name": "europe_peat_wetland_simplified",
        "metadata": {
            "title": "Europe peat/wetland simplified web layer",
            "created": TODAY,
            "source": "European Wetland Map / user-filtered GIS export",
            "interpretation": "Continental wetland/peat spatial context layer; not a local rewetting suitability map.",
            "input": str(INPUT),
            "simplification_tolerance_degrees": SIMPLIFY_TOLERANCE,
            "vertices_before": vertices_before,
            "vertices_after": vertices_after,
        },
        "features": out_features,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(output_geo, f, ensure_ascii=False, separators=(",", ":"))

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["class", "feature_count", "area_sum_raw"])
        writer.writeheader()
        for klass, vals in sorted(summary.items(), key=lambda x: (-x[1]["feature_count"], x[0])):
            writer.writerow({
                "class": klass,
                "feature_count": vals["feature_count"],
                "area_sum_raw": vals["area_sum_raw"],
            })

    method = f"""# B15b — Europe Peat/Wetland Web Layer

Date: {TODAY}

## Input

`{INPUT}`

The input is expected to be a GIS-filtered, dissolved and simplified GeoJSON export of the European Wetland Map or another European peat/wetland context layer.

## Output

`{OUTPUT}`

## Processing

- read input GeoJSON,
- detect class fields flexibly,
- retain class and area information where available,
- apply additional web-only Douglas-Peucker simplification with tolerance `{SIMPLIFY_TOLERANCE}` degrees,
- export compact GeoJSON for GitHub Pages display,
- write class summary.

## Vertex reduction

- vertices before Python simplification: {vertices_before}
- vertices after Python simplification: {vertices_after}

## Interpretation boundary

This layer is a continental spatial context layer. It is not a local rewetting suitability map and should not be used for site-level planning.
"""

    METHOD.parent.mkdir(parents=True, exist_ok=True)
    METHOD.write_text(method, encoding="utf-8")

    size_mb = OUTPUT.stat().st_size / 1024 / 1024

    print("B15b Europe peat/wetland web layer built.")
    print("Input features:", len(features))
    print("Output features:", len(out_features))
    print("Vertices before:", vertices_before)
    print("Vertices after:", vertices_after)
    print(f"Output size: {size_mb:.2f} MB")
    print("Output:", OUTPUT)
    print("Summary:", SUMMARY)
    print("Method:", METHOD)

    if size_mb > 15:
        print()
        print("WARNING: Output is still larger than 15 MB. Increase GIS simplification or SIMPLIFY_TOLERANCE.")


if __name__ == "__main__":
    main()
