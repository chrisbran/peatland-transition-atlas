#!/usr/bin/env python3
r"""
Build final interim country_hotspots.csv from two local exports:

1) emissions-from-drained-organic-soils.csv
   - Area
   - Emissions (CO2)
   - Emissions (N2O) [kept as gas-specific field only]

2) emissions_agriculture_cultivated_organic_soils_e_all_data_norm.csv
   - Emissions (CO2eq) from N2O (AR5)

Dependency-free: Python standard library only.

Typical run:
  python scripts\03_build_country_hotspots_no_pandas.py --input data\external\faostat --year 2019

Outputs:
  data/processed/country_hotspots.csv
  public/data/country_hotspots.csv
  data/processed/country_hotspots_data_dictionary.csv
  docs/B2b_country_hotspots_method.md
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


def clean_header(field: str) -> str:
    return (field or "").replace("\ufeff", "").strip()


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

    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    reader.fieldnames = [clean_header(f) for f in (reader.fieldnames or [])]

    rows = []
    for row in reader:
        rows.append({clean_header(k): v for k, v in row.items()})
    return rows


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


def find_files(input_dir: Path):
    combined = None
    cultivation = None
    for path in input_dir.glob("*.csv"):
        lower = path.name.lower()
        if "emissions-from-drained-organic-soils" in lower:
            combined = path
        elif "cultivated_organic_soils" in lower or "cultivation" in lower:
            cultivation = path
    if combined is None:
        raise FileNotFoundError("Could not find emissions-from-drained-organic-soils.csv")
    if cultivation is None:
        raise FileNotFoundError("Could not find cultivation/cultivated organic soils CSV")
    return combined, cultivation


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


def build(args):
    input_dir = Path(args.input)
    combined_file, cultivation_file = find_files(input_dir)

    combined_rows = read_csv(combined_file)
    cultivation_rows = read_csv(cultivation_file)

    # From combined drained-organic-soils export:
    # sum cropland + grassland area and CO2 emissions by country/year.
    # Keep N2O gas-specific kt as a diagnostic, but do not use it for CO2e total.
    data = defaultdict(lambda: {
        "m49_code": None,
        "area_ha": 0.0,
        "co2_kt": 0.0,
        "n2o_kt_gas": 0.0,
        "has_area": False,
        "has_co2": False,
        "has_n2o_gas": False,
    })

    skipped_non_country = set()

    for row in combined_rows:
        country = (row.get("Area") or "").strip()
        if not country or is_non_country(country):
            if country:
                skipped_non_country.add(country)
            continue

        year = to_int(row.get("Year"))
        if year != args.year:
            continue

        item = (row.get("Item") or "").strip()
        if item not in {"Cropland organic soils", "Grassland organic soils"}:
            continue

        element = (row.get("Element") or "").strip()
        unit = (row.get("Unit") or "").strip().lower()
        value = to_float(row.get("Value"))
        if value is None:
            continue

        key = (country, year)
        rec = data[key]
        rec["m49_code"] = row.get("Area Code (M49)") or rec["m49_code"]

        if element == "Area" and unit == "ha":
            rec["area_ha"] += value
            rec["has_area"] = True
        elif element == "Emissions (CO2)" and unit == "kt":
            rec["co2_kt"] += value
            rec["has_co2"] = True
        elif element == "Emissions (N2O)" and unit == "kt":
            rec["n2o_kt_gas"] += value
            rec["has_n2o_gas"] = True

    # From cultivation export:
    # use AR5 CO2eq N2O total for cropland+grassland organic soils.
    n2o_ar5 = {}
    for row in cultivation_rows:
        country = (row.get("location") or "").strip()
        if not country or is_non_country(country):
            continue

        year = to_int(row.get("Date"))
        if year != args.year:
            continue

        if (row.get("item") or "").strip() != COMBINED_ITEM:
            continue

        element = (row.get("element") or "").strip()
        unit = (row.get("Unit") or "").strip()
        value = to_float(row.get("Value"))
        if value is None:
            continue

        if element == N2O_AR5_ELEMENT and unit == "Gigagrams":
            # 1 Gg CO2eq = 1 kt CO2eq
            n2o_ar5[(country, year)] = value

    output = []
    for (country, year), vals in data.items():
        area = vals["area_ha"] if vals["has_area"] else None
        co2 = vals["co2_kt"] if vals["has_co2"] else None
        n2o_co2e = n2o_ar5.get((country, year))

        total = None
        if co2 is not None and n2o_co2e is not None:
            total = co2 + n2o_co2e

        density = None
        if area and area > 0 and total is not None:
            density = total * 1000 / area

        if n2o_co2e is None:
            dq = "Missing N2O AR5 CO2e join from cultivation export."
        elif co2 is None:
            dq = "Missing CO2 field from drained-organic-soils export."
        elif area is None:
            dq = "Missing drained organic soils area."
        else:
            dq = "Interim Phase B2b country-level dataset; country-name join, ISO3 join pending."

        output.append({
            "country": country,
            "m49_code": vals.get("m49_code"),
            "iso3": "",
            "year": year,
            "drained_organic_soils_area_ha": area,
            "co2_kt_co2": co2,
            "n2o_ar5_kt_co2e": n2o_co2e,
            "n2o_kt_gas_diagnostic": vals["n2o_kt_gas"] if vals["has_n2o_gas"] else None,
            "emissions_total_kt_co2e": total,
            "emissions_density_t_co2e_per_ha": density,
            "hotspot_class": None,
            "hotspot_rank_total": None,
            "hotspot_rank_density": None,
            "source_area": combined_file.name,
            "source_co2": combined_file.name,
            "source_n2o_co2e": cultivation_file.name,
            "data_quality_note": dq,
        })

    output.sort(key=lambda r: (r["emissions_total_kt_co2e"] is None, -(r["emissions_total_kt_co2e"] or 0), r["country"]))

    classify_quantiles(output, "emissions_total_kt_co2e")
    rank_desc(output, "emissions_total_kt_co2e", "hotspot_rank_total")
    rank_desc(output, "emissions_density_t_co2e_per_ha", "hotspot_rank_density")

    fields = [
        "country", "m49_code", "iso3", "year",
        "drained_organic_soils_area_ha",
        "co2_kt_co2",
        "n2o_ar5_kt_co2e",
        "n2o_kt_gas_diagnostic",
        "emissions_total_kt_co2e",
        "emissions_density_t_co2e_per_ha",
        "hotspot_class",
        "hotspot_rank_total",
        "hotspot_rank_density",
        "source_area",
        "source_co2",
        "source_n2o_co2e",
        "data_quality_note",
    ]

    for out_path in [Path(args.out_processed), Path(args.out_public)]:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(output)

    dd_rows = [
        ["field", "description"],
        ["country", "FAOSTAT/KAPSARC country or territory name."],
        ["m49_code", "FAOSTAT Area Code (M49) from combined drained-organic-soils export."],
        ["iso3", "Reserved for ISO3 code; filled in B3 when country boundary join is prepared."],
        ["year", "Exact selected year."],
        ["drained_organic_soils_area_ha", "Sum of cropland and grassland organic soils area in hectares."],
        ["co2_kt_co2", "Sum of CO2 emissions from cropland and grassland organic soils, in kt CO2."],
        ["n2o_ar5_kt_co2e", "N2O emissions from cultivation of organic soils, AR5 CO2-equivalent, in kt CO2e."],
        ["n2o_kt_gas_diagnostic", "Gas-specific N2O emissions from combined export; diagnostic only, not used in CO2e total."],
        ["emissions_total_kt_co2e", "co2_kt_co2 + n2o_ar5_kt_co2e."],
        ["emissions_density_t_co2e_per_ha", "emissions_total_kt_co2e * 1000 / drained_organic_soils_area_ha."],
        ["hotspot_class", "Quantile-based class for MVP choropleth."],
        ["hotspot_rank_total", "Rank by total emissions; 1 = highest."],
        ["hotspot_rank_density", "Rank by emissions density; 1 = highest."],
        ["source_area", "Source file for area values."],
        ["source_co2", "Source file for CO2 values."],
        ["source_n2o_co2e", "Source file for N2O AR5 CO2e values."],
        ["data_quality_note", "Short processing caveat."],
    ]
    dd_path = Path("data/processed/country_hotspots_data_dictionary.csv")
    dd_path.parent.mkdir(parents=True, exist_ok=True)
    with dd_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(dd_rows)

    method_path = Path("docs/B2b_country_hotspots_method.md")
    method_path.parent.mkdir(parents=True, exist_ok=True)
    method_path.write_text(f"""# B2b — Country Hotspots from Drained Organic Soils

## Status

Interim country-level hotspot dataset for Phase B.

## Input files

- `{combined_file}`
- `{cultivation_file}`

## Selected year

`{args.year}`

## Processing

1. From `emissions-from-drained-organic-soils.csv`:
   - sum `Area` across `Cropland organic soils` and `Grassland organic soils`
   - sum `Emissions (CO2)` across both items
   - keep `Emissions (N2O)` as diagnostic gas-specific value only

2. From `emissions_agriculture_cultivated_organic_soils_e_all_data_norm.csv`:
   - select `Cropland and grassland organic soils`
   - select `Emissions (CO2eq) from N2O (AR5)`
   - use Gigagrams as kilotonnes CO2-equivalent

3. Join by country name and year.

4. Compute:
   - `emissions_total_kt_co2e = co2_kt_co2 + n2o_ar5_kt_co2e`
   - `emissions_density_t_co2e_per_ha = emissions_total_kt_co2e * 1000 / area_ha`

## Outputs

- `data/processed/country_hotspots.csv`
- `public/data/country_hotspots.csv`
- `data/processed/country_hotspots_data_dictionary.csv`

## Important caveats

- This is an interim MVP dataset.
- ISO3 codes are not yet filled.
- Country-name joins should be checked before choropleth mapping.
- Hotspot classes are quantile-based and intended for exploratory visualisation.
- Raw FAOSTAT/KAPSARC CSV exports should remain local and not be committed.
""", encoding="utf-8")

    return output, combined_file, cultivation_file, skipped_non_country


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/external/faostat", help="Folder containing both CSV exports.")
    parser.add_argument("--year", type=int, default=2019, help="Exact year to select. Default: 2019.")
    parser.add_argument("--out-processed", default="data/processed/country_hotspots.csv")
    parser.add_argument("--out-public", default="public/data/country_hotspots.csv")
    args = parser.parse_args()

    try:
        output, combined_file, cultivation_file, skipped = build(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    complete = [r for r in output if r["emissions_total_kt_co2e"] is not None]
    missing = len(output) - len(complete)

    print(f"Combined input: {combined_file}")
    print(f"N2O AR5 input: {cultivation_file}")
    print(f"Selected exact year: {args.year}")
    print(f"Country rows written: {len(output)}")
    print(f"Rows with complete total CO2e: {len(complete)}")
    print(f"Rows with missing CO2 or N2O CO2e: {missing}")
    print(f"Non-country / historical labels skipped: {len(skipped)}")
    print("Outputs:")
    print(f"  {args.out_processed}")
    print(f"  {args.out_public}")
    print("  data/processed/country_hotspots_data_dictionary.csv")
    print("  docs/B2b_country_hotspots_method.md")
    print()
    print("Top 15 countries by total drained-organic-soils GHG emissions:")
    for r in complete[:15]:
        print(
            f"  {r['hotspot_rank_total']:>3} | {r['country']:<32} | {r['year']} | "
            f"CO2={r['co2_kt_co2']} kt | N2O_AR5={r['n2o_ar5_kt_co2e']} kt CO2e | "
            f"TOTAL={r['emissions_total_kt_co2e']} kt CO2e"
        )


if __name__ == "__main__":
    main()
