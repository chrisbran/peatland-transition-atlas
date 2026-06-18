#!/usr/bin/env python3
r"""
B14c — Optimize Germany organic-soils web layer after ArcGIS dissolve/simplify.

Input:
  data/external/peat_soils/germany_organic_soils/germany_organic_soils_wgs84.geojson

Run:
  python scripts\24_optimize_germany_organic_soils_web_layer.py

Outputs:
  public/data/germany_organic_soils_simplified.geojson
  data/processed/germany_organic_soils_summary.csv
  docs/B14c_germany_organic_soils_optimized_web_layer_method.md
"""

from pathlib import Path
import csv
import datetime
import json
import math


TODAY = datetime.date.today().isoformat()

INPUT = Path("data/external/peat_soils/germany_organic_soils/germany_organic_soils_wgs84.geojson")
OUTPUT = Path("public/data/germany_organic_soils_simplified.geojson")
SUMMARY = Path("data/processed/germany_organic_soils_summary.csv")
METHOD = Path("docs/B14c_germany_organic_soils_optimized_web_layer_method.md")

# Web-only generalisation for national sticky-story overview.
# 0.01° ≈ 0.7–1.1 km across Germany.
SIMPLIFY_TOLERANCE = 0.01

CLASS_CANDIDATES = [
    "KAT_KURZ", "KAT_LANG", "kat_kurz", "kat_lang",
    "Moorbodenkategorie", "moor_kat", "MoorKat", "Kategorie", "KATEGORIE",
    "Kat", "KAT", "Klasse", "klasse", "CLASS", "class",
    "GENESE", "Genese", "genese", "legend", "Legend", "LEGEND"
]

LONG_CLASS_CANDIDATES = [
    "KAT_LANG", "kat_lang", "Kategorie_lang", "category_long",
    "Moorbodenkategorie", "GENESE", "Genese", "genese"
]

AREA_CANDIDATES = [
    "SUM_AREA_HA", "SUM_AREA_HA_WG", "AREA_HA", "AREA_HA_WG",
    "sum_area_ha", "area_ha", "ha", "HA",
    "Shape_Area", "SHAPE_Area", "shape_area",
    "Flaeche", "Fläche", "FLAECHE", "area", "Area", "AREA"
]

CLASS_LABELS = {
    "NH": "Niedermoorboden",
    "HH": "Hochmoorboden",
    "XH": "Moorfolgeboden / sonstiger organischer Boden",
    "MD": "Mudde / mineralisch überdeckter organischer Boden",
}


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


def numeric(value):
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


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
        raise SystemExit(f"Input not found: {INPUT}")

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

        short_class = str(first_existing(props, CLASS_CANDIDATES, "Organic soils")).strip() or "Organic soils"
        long_class = str(first_existing(props, LONG_CLASS_CANDIDATES, "")).strip()

        if not long_class and short_class in CLASS_LABELS:
            long_class = CLASS_LABELS[short_class]

        area_raw = first_existing(props, AREA_CANDIDATES, "")
        area_num = numeric(area_raw)

        geom_in = feat.get("geometry")
        vertices_before += count_vertices(geom_in)
        geom = simplify_geometry(geom_in, SIMPLIFY_TOLERANCE)
        vertices_after += count_vertices(geom)
        bbox = feature_bbox(geom)

        summary.setdefault(short_class, {
            "class_long": long_class,
            "feature_count": 0,
            "area_sum_ha": 0.0
        })
        summary[short_class]["feature_count"] += 1
        if area_num is not None:
            summary[short_class]["area_sum_ha"] += area_num

        new_props = {
            "class": short_class,
            "class_long": long_class,
            "source_area_ha": area_raw,
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
        "name": "germany_organic_soils_simplified",
        "metadata": {
            "title": "Germany organic soils optimized simplified web layer",
            "created": TODAY,
            "source": "Thünen/OpenAgrar: Aktualisierte Kulisse organischer Böden in Deutschland",
            "interpretation": "National organic-soils context layer; not a local rewetting suitability map.",
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
        writer = csv.DictWriter(f, fieldnames=["class", "class_long", "feature_count", "area_sum_ha"])
        writer.writeheader()
        for klass, vals in sorted(summary.items(), key=lambda x: (-x[1]["area_sum_ha"], x[0])):
            writer.writerow({
                "class": klass,
                "class_long": vals["class_long"],
                "feature_count": vals["feature_count"],
                "area_sum_ha": vals["area_sum_ha"],
            })

    method = f"""# B14c — Optimized Germany Organic-Soils Web Layer

Date: {TODAY}

## Input

`{INPUT}`

The input is expected to be an ArcGIS-dissolved and simplified GeoJSON export of the Germany organic-soils layer.

## Output

`{OUTPUT}`

## Processing

- read dissolved GeoJSON,
- detect class fields including `KAT_KURZ` and `KAT_LANG`,
- detect area fields including `SUM_AREA_HA` and `AREA_HA`,
- apply additional web-only Douglas-Peucker simplification with tolerance `{SIMPLIFY_TOLERANCE}` degrees,
- export compact GeoJSON for GitHub Pages display,
- write class summary.

## Vertex reduction

- vertices before Python simplification: {vertices_before}
- vertices after Python simplification: {vertices_after}

## Interpretation boundary

This layer is a national organic-soils context layer for scrollytelling. It is not a local rewetting suitability map and should not be used for parcel-level planning.
"""

    METHOD.parent.mkdir(parents=True, exist_ok=True)
    METHOD.write_text(method, encoding="utf-8")

    size_mb = OUTPUT.stat().st_size / 1024 / 1024

    print("B14c optimized Germany organic-soils web layer built.")
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
        print("WARNING: Output is still larger than 15 MB. Consider another ArcGIS Simplify run with 500-1000 m or increase SIMPLIFY_TOLERANCE.")


if __name__ == "__main__":
    main()
