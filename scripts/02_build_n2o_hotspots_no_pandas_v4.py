#!/usr/bin/env python3
r"""
Build a cleaner 2019-only country-level N2O hotspot table from the
FAOSTAT/KAPSARC Cultivation of organic soils export.

Dependency-free: Python standard library only.

Typical run:
  python scripts\02_build_n2o_hotspots_no_pandas_v4.py --input data\external\faostat --year 2019

Outputs:
  data/processed/country_hotspots_n2o.csv
  public/data/country_hotspots_n2o.csv
  docs/B2a_n2o_hotspots_method.md
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict
from pathlib import Path


COMBINED_ITEM = "Cropland and grassland organic soils"
AREA_ELEMENT = "Area"
N2O_AR5_ELEMENT = "Emissions (CO2eq) from N2O (AR5)"

EXCLUDE_EXACT = {
    "World",
    "Africa", "Americas", "Asia", "Europe", "Oceania",
    "Northern Africa", "Sub-Saharan Africa", "Eastern Africa", "Middle Africa", "Southern Africa", "Western Africa",
    "Northern America", "Central America", "South America", "Latin America and the Caribbean", "Caribbean",
    "Central Asia", "Eastern Asia", "Southern Asia", "South-Eastern Asia", "Western Asia",
    "Eastern Europe", "Northern Europe", "Southern Europe", "Western Europe",
    "Australia and New Zealand", "Melanesia", "Micronesia", "Polynesia",
    "European Union", "European Union (27)", "European Union (28)",
    "OECD",
    "Annex I countries", "Non-Annex I countries",
    "Least Developed Countries",
    "Land Locked Developing Countries",
    "Small Island Developing States",
    "Low Income Food Deficit Countries",
    "Net Food Importing Developing Countries",
    "USSR",
    "Yugoslav SFR",
    "Czechoslovakia",
    "Belgium-Luxembourg",
    "Ethiopia PDR",
    "Serbia and Montenegro",
    "Netherlands Antilles",
}

AGGREGATE_KEYWORDS = [
    "countries",
    "income",
    "developed",
    "developing",
    "annex",
    "oecd",
    "european union",
    "world",
]

COUNTRY_EXCEPTIONS = {
    "south africa",
    "central african republic",
    "north macedonia",
    "south sudan",
    "united states of america",
    "united kingdom",
    "russian federation",
    "czechia",
    "democratic republic of the congo",
    "united republic of tanzania",
    "bolivia (plurinational state of)",
    "venezuela (bolivarian republic of)",
    "iran (islamic republic of)",
    "lao people's democratic republic",
    "syrian arab republic",
    "republic of korea",
    "democratic people's republic of korea",
}


def is_non_country(name: str) -> bool:
    n = name.strip()
    low = n.lower()
    if n in EXCLUDE_EXACT:
        return True
    if low in COUNTRY_EXCEPTIONS:
        return False
    return any(k in low for k in AGGREGATE_KEYWORDS)


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


def to_float(value: str):
    if value is None:
        return None
    v = str(value).strip().replace(",", ".")
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def to_int(value: str):
    try:
        return int(float(str(value).strip()))
    except Exception:
        return None


def classify_quantiles(rows, value_field):
    vals = sorted([r[value_field] for r in rows if r.get(value_field) is not None])
    if not vals:
        return

    def q(p):
        idx = int(round((len(vals) - 1) * p))
        return vals[idx]

    q25, q50, q75, q90 = q(.25), q(.50), q(.75), q(.90)

    for r in rows:
        v = r.get(value_field)
        if v is None:
            r["hotspot_class"] = "no_data"
        elif v >= q90:
            r["hotspot_class"] = "very_high"
        elif v >= q75:
            r["hotspot_class"] = "high"
        elif v >= q50:
            r["hotspot_class"] = "medium"
        elif v >= q25:
            r["hotspot_class"] = "low"
        else:
            r["hotspot_class"] = "very_low"


def rank_desc(rows, value_field, rank_field):
    ranked = sorted(
        [r for r in rows if r.get(value_field) is not None],
        key=lambda r: r[value_field],
        reverse=True
    )
    for i, r in enumerate(ranked, start=1):
        r[rank_field] = i


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/external/faostat", help="Folder containing CSV export.")
    parser.add_argument("--year", type=int, default=2019, help="Exact year to select. Default: 2019.")
    parser.add_argument("--out-processed", default="data/processed/country_hotspots_n2o.csv")
    parser.add_argument("--out-public", default="public/data/country_hotspots_n2o.csv")
    args = parser.parse_args()

    input_dir = Path(args.input)
    files = list(input_dir.glob("*.csv"))
    if not files:
        print(f"No CSV files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    selected = None
    records = None
    for path in files:
        rows = read_csv(path)
        if rows and {"Date", "location", "item", "element", "Value", "Unit"}.issubset(rows[0].keys()):
            selected = path
            records = rows
            break

    if selected is None:
        print("No compatible cultivated organic soils CSV found.", file=sys.stderr)
        sys.exit(2)

    data = defaultdict(lambda: {"area_ha": None, "n2o_ar5_kt_co2e": None})
    skipped_non_country = set()

    for row in records:
        country = (row.get("location") or "").strip()
        if not country or is_non_country(country):
            if country:
                skipped_non_country.add(country)
            continue

        if row.get("item") != COMBINED_ITEM:
            continue

        year = to_int(row.get("Date"))
        if year != args.year:
            continue

        element = (row.get("element") or "").strip()
        unit = (row.get("Unit") or "").strip()
        value = to_float(row.get("Value"))
        if value is None:
            continue

        key = (country, year)
        if element == AREA_ELEMENT and unit == "Ha":
            data[key]["area_ha"] = value
        elif element == N2O_AR5_ELEMENT and unit == "Gigagrams":
            data[key]["n2o_ar5_kt_co2e"] = value  # 1 Gg = 1 kt

    output = []
    for (country, year), vals in data.items():
        area = vals.get("area_ha")
        n2o = vals.get("n2o_ar5_kt_co2e")
        density = None
        if area and area > 0 and n2o is not None:
            density = n2o * 1000 / area

        output.append({
            "country": country,
            "year": year,
            "drained_organic_soils_area_ha": area,
            "n2o_ar5_kt_co2e": n2o,
            "n2o_density_t_co2e_per_ha": density,
            "hotspot_class": None,
            "n2o_rank_total": None,
            "n2o_rank_density": None,
            "source_file": selected.name,
            "source_note": "FAOSTAT/KAPSARC Cultivation of organic soils export; N2O component only.",
            "data_quality_note": "Interim Phase B2a country-level dataset; exact year only; excludes CO2 emissions from drained cropland/grassland organic soils."
        })

    output.sort(key=lambda r: (r["n2o_ar5_kt_co2e"] is None, -(r["n2o_ar5_kt_co2e"] or 0), r["country"]))
    classify_quantiles(output, "n2o_ar5_kt_co2e")
    rank_desc(output, "n2o_ar5_kt_co2e", "n2o_rank_total")
    rank_desc(output, "n2o_density_t_co2e_per_ha", "n2o_rank_density")

    fields = [
        "country", "year",
        "drained_organic_soils_area_ha",
        "n2o_ar5_kt_co2e",
        "n2o_density_t_co2e_per_ha",
        "hotspot_class",
        "n2o_rank_total",
        "n2o_rank_density",
        "source_file",
        "source_note",
        "data_quality_note"
    ]

    for out_path in [Path(args.out_processed), Path(args.out_public)]:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(output)

    method = Path("docs/B2a_n2o_hotspots_method.md")
    method.parent.mkdir(parents=True, exist_ok=True)
    method.write_text(f"""# B2a — N2O Hotspots from Cultivation of Organic Soils

## Status

Interim country-level dataset.

## Input

`{selected}`

## Selection

- item: `{COMBINED_ITEM}`
- area element: `{AREA_ELEMENT}`
- emissions element: `{N2O_AR5_ELEMENT}`
- unit: Gigagrams = kilotonnes CO2e
- exact year: `{args.year}`
- aggregate and historical/non-current labels removed using a conservative name filter

## Outputs

- `data/processed/country_hotspots_n2o.csv`
- `public/data/country_hotspots_n2o.csv`

## Important limitation

This is not yet total drained organic soil emissions. It excludes CO2 emissions from drained cropland/grassland organic soils.

Use this table only as an interim QA dataset until the CO2 land-use component or a combined drained-organic-soils export is added.

## Known data-processing decision

The script selects one exact year rather than the latest available year per country. This avoids mixing current countries with historical entities such as USSR or projection years such as 2050.
""", encoding="utf-8")

    print(f"Selected input: {selected}")
    print(f"Selected exact year: {args.year}")
    print(f"Country rows written: {len(output)}")
    print(f"Non-country / historical labels skipped: {len(skipped_non_country)}")
    print("Outputs:")
    print(f"  {args.out_processed}")
    print(f"  {args.out_public}")
    print("Method:")
    print("  docs/B2a_n2o_hotspots_method.md")
    print()
    print("Top 15 countries by N2O AR5 CO2eq:")
    for r in output[:15]:
        print(f"  {r['n2o_rank_total']:>3} | {r['country']:<32} | {r['year']} | {r['n2o_ar5_kt_co2e']} kt CO2e")


if __name__ == "__main__":
    main()
