#!/usr/bin/env python3
r"""
B4 — Prepare Natural Earth country boundary join for the hotspot atlas.

Run from repository root:

  python scripts\05_prepare_country_boundary_join.py

Inputs:
  data/processed/country_hotspots.csv

Downloads:
  Natural Earth 110m Admin 0 Countries GeoJSON

Outputs:
  public/data/hotspot_countries_110m.geojson
  data/processed/country_boundary_join_report.csv
  docs/B4_country_boundary_join_method.md

No external Python dependencies.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import json
import sys
import urllib.request
from pathlib import Path


DEFAULT_NATURAL_EARTH_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_admin_0_countries.geojson"
)

MANUAL_NAME_FIXES = {
    "United States of America": ["United States of America", "United States"],
    "Russian Federation": ["Russia", "Russian Federation"],
    "United Kingdom": ["United Kingdom"],
    "Iran (Islamic Republic of)": ["Iran"],
    "Bolivia (Plurinational State of)": ["Bolivia"],
    "Venezuela (Bolivarian Republic of)": ["Venezuela"],
    "Democratic Republic of the Congo": ["Democratic Republic of the Congo", "Dem. Rep. Congo"],
    "Congo": ["Republic of the Congo", "Congo"],
    "Côte d'Ivoire": ["Côte d'Ivoire", "Ivory Coast"],
    "Czechia": ["Czechia", "Czech Republic"],
    "Republic of Korea": ["South Korea", "Korea, Republic of"],
    "Democratic People's Republic of Korea": ["North Korea"],
    "Lao People's Democratic Republic": ["Laos"],
    "Syrian Arab Republic": ["Syria"],
    "Viet Nam": ["Vietnam"],
    "United Republic of Tanzania": ["Tanzania"],
    "Eswatini": ["eSwatini", "Eswatini", "Swaziland"],
    "Türkiye": ["Turkey", "Türkiye"],
}


def read_csv(path: Path):
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")

    sample = text[:4096]
    delimiter = ";" if sample.count(";") > sample.count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def to_float(value):
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def norm_name(value: str) -> str:
    return (
        (value or "")
        .strip()
        .lower()
        .replace("&", "and")
        .replace("’", "'")
        .replace("the ", "")
    )


def get_prop(props, candidates):
    for c in candidates:
        if c in props and props[c] not in (None, "", "-99"):
            return str(props[c])
    return ""


def download_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "peatland-transition-atlas/0.2"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def build_indexes(features):
    by_m49 = {}
    by_iso3 = {}
    by_name = {}

    for feat in features:
        props = feat.get("properties", {})

        # Natural Earth has several numeric code fields depending on version.
        m49_candidates = [
            get_prop(props, ["UN_A3"]),
            get_prop(props, ["ISO_N3"]),
            get_prop(props, ["SU_A3"]),
        ]
        for code in m49_candidates:
            if code and code != "-99":
                by_m49[code.lstrip("0") or "0"] = feat

        iso_candidates = [
            get_prop(props, ["ISO_A3"]),
            get_prop(props, ["ADM0_A3"]),
            get_prop(props, ["SOV_A3"]),
        ]
        for code in iso_candidates:
            if code and code != "-99":
                by_iso3[code.upper()] = feat

        name_candidates = [
            get_prop(props, ["ADMIN"]),
            get_prop(props, ["NAME"]),
            get_prop(props, ["NAME_LONG"]),
            get_prop(props, ["SOVEREIGNT"]),
            get_prop(props, ["BRK_NAME"]),
        ]
        for name in name_candidates:
            if name:
                by_name[norm_name(name)] = feat

    return by_m49, by_iso3, by_name


def match_feature(row, by_m49, by_iso3, by_name):
    m49 = (row.get("m49_code") or "").strip()
    iso3 = (row.get("iso3") or "").strip().upper()
    country = (row.get("country") or "").strip()

    if m49:
        key = m49.lstrip("0") or "0"
        if key in by_m49:
            return by_m49[key], "m49_code"

    if iso3 and iso3 in by_iso3:
        return by_iso3[iso3], "iso3"

    candidates = [country] + MANUAL_NAME_FIXES.get(country, [])
    for cand in candidates:
        key = norm_name(cand)
        if key in by_name:
            return by_name[key], "country_name"

    return None, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hotspots", default="data/processed/country_hotspots.csv")
    parser.add_argument("--url", default=DEFAULT_NATURAL_EARTH_URL)
    parser.add_argument("--out-geojson", default="public/data/hotspot_countries_110m.geojson")
    parser.add_argument("--out-report", default="data/processed/country_boundary_join_report.csv")
    args = parser.parse_args()

    hotspots_path = Path(args.hotspots)
    if not hotspots_path.exists():
        print(f"ERROR: Missing hotspot file: {hotspots_path}", file=sys.stderr)
        sys.exit(1)

    print("Reading hotspot data...")
    rows = read_csv(hotspots_path)

    complete_rows = [
        r for r in rows
        if to_float(r.get("emissions_total_kt_co2e")) is not None
    ]

    print("Downloading Natural Earth 110m Admin 0 Countries GeoJSON...")
    ne = download_json(args.url)
    features = ne.get("features", [])
    by_m49, by_iso3, by_name = build_indexes(features)

    joined_features = []
    report_rows = []

    for row in complete_rows:
        feat, method = match_feature(row, by_m49, by_iso3, by_name)

        if feat is None:
            report_rows.append({
                "country": row.get("country", ""),
                "m49_code": row.get("m49_code", ""),
                "iso3": row.get("iso3", ""),
                "join_status": "unmatched",
                "join_method": "",
                "emissions_total_kt_co2e": row.get("emissions_total_kt_co2e", ""),
                "emissions_density_t_co2e_per_ha": row.get("emissions_density_t_co2e_per_ha", ""),
            })
            continue

        props = feat.get("properties", {})
        out_props = {
            "country": row.get("country", ""),
            "m49_code": row.get("m49_code", ""),
            "iso3": row.get("iso3", "") or get_prop(props, ["ISO_A3", "ADM0_A3"]),
            "year": row.get("year", ""),
            "drained_organic_soils_area_ha": to_float(row.get("drained_organic_soils_area_ha")),
            "co2_kt_co2": to_float(row.get("co2_kt_co2")),
            "n2o_ar5_kt_co2e": to_float(row.get("n2o_ar5_kt_co2e")),
            "emissions_total_kt_co2e": to_float(row.get("emissions_total_kt_co2e")),
            "emissions_density_t_co2e_per_ha": to_float(row.get("emissions_density_t_co2e_per_ha")),
            "hotspot_class": row.get("hotspot_class", ""),
            "hotspot_rank_total": row.get("hotspot_rank_total", ""),
            "hotspot_rank_density": row.get("hotspot_rank_density", ""),
            "join_method": method,
            "ne_name": get_prop(props, ["ADMIN", "NAME", "NAME_LONG"]),
        }

        joined_features.append({
            "type": "Feature",
            "properties": out_props,
            "geometry": feat.get("geometry"),
        })

        report_rows.append({
            "country": row.get("country", ""),
            "m49_code": row.get("m49_code", ""),
            "iso3": out_props["iso3"],
            "join_status": "matched",
            "join_method": method,
            "ne_name": out_props["ne_name"],
            "emissions_total_kt_co2e": row.get("emissions_total_kt_co2e", ""),
            "emissions_density_t_co2e_per_ha": row.get("emissions_density_t_co2e_per_ha", ""),
        })

    out_geojson = {
        "type": "FeatureCollection",
        "name": "hotspot_countries_110m",
        "metadata": {
            "source_boundary": "Natural Earth 110m Admin 0 Countries",
            "source_hotspots": str(hotspots_path),
            "selected_records": "complete records with emissions_total_kt_co2e",
            "created": datetime.date.today().isoformat(),
            "important_caveat": "Country-level hotspot visualization only; not a local rewetting suitability map."
        },
        "features": joined_features,
    }

    out_geojson_path = Path(args.out_geojson)
    out_geojson_path.parent.mkdir(parents=True, exist_ok=True)
    out_geojson_path.write_text(json.dumps(out_geojson, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    report_path = Path(args.out_report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_fields = [
        "country", "m49_code", "iso3", "join_status", "join_method", "ne_name",
        "emissions_total_kt_co2e", "emissions_density_t_co2e_per_ha"
    ]
    with report_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(report_rows)

    method_path = Path("docs/B4_country_boundary_join_method.md")
    method_path.parent.mkdir(parents=True, exist_ok=True)
    method_path.write_text(f"""# B4 — Country Boundary Join

## Status

Prepared a lightweight country-level GeoJSON for the Phase B hotspot layer.

## Boundary source

Natural Earth 110m Admin 0 Countries GeoJSON.

Source URL used by script:

```text
{args.url}
```

## Hotspot source

```text
{hotspots_path}
```

## Processing

1. Load complete country-level hotspot records.
2. Download Natural Earth 110m Admin 0 Countries GeoJSON.
3. Build join indexes using:
   - M49/UN numeric codes,
   - ISO3 fields,
   - Natural Earth country names.
4. Join hotspot records to country geometries.
5. Export compact web GeoJSON.

## Outputs

- `public/data/hotspot_countries_110m.geojson`
- `data/processed/country_boundary_join_report.csv`

## Caveat

This layer visualizes national hotspot concentration only. It must not be interpreted as local rewetting suitability or farm-scale prioritization.

## Next step

B5 — add choropleth map rendering to the atlas interface.
""", encoding="utf-8")

    task_path = Path("tasks/B5_add_choropleth_map.md")
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text("""# Task B5 — Add Choropleth Map to Atlas Interface

## Agent

Visualization Engineer Agent

## Goal

Render `public/data/hotspot_countries_110m.geojson` as a simple interactive choropleth layer.

## Inputs

- `public/data/hotspot_countries_110m.geojson`
- existing hotspot ranking interface

## Required outputs

- map panel in the hotspot section
- legend for emissions_total_kt_co2e or hotspot_class
- hover/click detail for country, total emissions, density and area
- caveat text that the layer is country-level only

## Acceptance criteria

- page still works as static GitHub Pages site,
- no heavy build framework required,
- map loads from public/data,
- missing/unmatched countries are documented.
""", encoding="utf-8")

    done = Path("tasks/done.md")
    done_text = done.read_text(encoding="utf-8") if done.exists() else "# Done\n"
    if "Task B4 completed" not in done_text:
        done_text += f"- {datetime.date.today().isoformat()}: Task B4 completed — prepared country boundary join for hotspot data.\n"
        done.write_text(done_text, encoding="utf-8")

    matched = sum(1 for r in report_rows if r["join_status"] == "matched")
    unmatched = sum(1 for r in report_rows if r["join_status"] == "unmatched")

    print("B4 boundary join prepared.")
    print(f"Complete hotspot records: {len(complete_rows)}")
    print(f"Matched countries: {matched}")
    print(f"Unmatched countries: {unmatched}")
    print("Outputs:")
    print(f"  {args.out_geojson}")
    print(f"  {args.out_report}")
    print("  docs/B4_country_boundary_join_method.md")
    print("  tasks/B5_add_choropleth_map.md")
    if unmatched:
        print()
        print("Unmatched countries:")
        for r in report_rows:
            if r["join_status"] == "unmatched":
                print(f"  - {r['country']} | M49={r['m49_code']} | ISO3={r['iso3']}")


if __name__ == "__main__":
    main()
