# B2 — FAOSTAT fetch method

## Status

B2 is set up as a robust manual-export workflow. This is deliberate: the first public portfolio version should not be blocked by API instability or uncertain endpoint details.

## Why manual export first?

The objective is not to build a perfect automated FAOSTAT client. The objective is to obtain a small, auditable `country_hotspots.csv` for the Phase B hotspot map.

## Data logic

FAO states that drained organic soils data are disseminated by gas and land-use class: N2O emissions on cropland and grassland under FAOSTAT Emissions-Agriculture / Cultivation of organic soils; CO2 emissions on Cropland and Grassland under FAOSTAT Emissions-Land use.

The related FAO Earth Engine DROSA-A/DROSE-A datasets distinguish:

- DROSA-A: area of organic soils drained for agricultural activities, in hectares.
- DROSE-A: carbon and N2O estimates, in gigagrams, from agricultural drainage of organic soils.

For the first MVP, the target is a country-level derived table, not raw raster data.

## Manual download steps

1. Go to FAOSTAT.
2. Open data download / explore data.
3. Download CSV exports for:
   - Cultivation of organic soils
   - Cropland organic soils
   - Grassland organic soils
   - drained organic soils area, if available separately
4. Save the CSV or ZIP files into:

```text
data/external/faostat/
```

Do not commit large raw exports if file size or licensing is unclear.

## Inspect exports

Run:

```bash
python scripts/02_build_country_hotspots_from_faostat_exports.py --input data/external/faostat --inspect
```

Check available columns, items, elements, units and years.

## Build first country table

Run:

```bash
python scripts/02_build_country_hotspots_from_faostat_exports.py --input data/external/faostat --year latest
```

or for a fixed year:

```bash
python scripts/02_build_country_hotspots_from_faostat_exports.py --input data/external/faostat --year 2019
```

## Output

The script writes:

```text
data/processed/country_hotspots.csv
public/data/country_hotspots.csv
data/processed/country_hotspots_data_dictionary.csv
```

## Critical QA checks before publication

1. Are emissions already in CO2e, or are they C / N2O values requiring conversion?
2. Which GWP convention is used for N2O if conversion is needed?
3. Is area in hectares?
4. Are country aggregates and territories handled correctly?
5. Are very small areas producing misleading density values?
6. Are Indonesia/Malaysia and other known hotspots plausible in the ranked output?

## Publication boundary

Commit:

```text
data/processed/country_hotspots.csv
public/data/country_hotspots.csv
data/processed/country_hotspots_data_dictionary.csv
docs/B2_faostat_fetch_method.md
scripts/02_build_country_hotspots_from_faostat_exports.py
```

Do not commit:

```text
large raw FAOSTAT exports
raw Earth Engine rasters
licence-unclear files
confidential project data
```
