# Task B2 — Fetch FAOSTAT Drained Organic Soils Country Data

## Agent

Data & GIS Agent

## Reviewer

Human Lead + QA & Critic Agent

## Goal

Build the first real `country_hotspots.csv` dataset from FAO/FAOSTAT drained organic soils area and emissions data.

## Inputs

- `data/processed/country_hotspots_schema.csv`
- `data/metadata/source_catalog_phase_B.csv`
- FAOSTAT / FAO drained organic soils data
- optional FAO Earth Engine DROSA-A / DROSE-A documentation as fallback

## Required outputs

- `data/processed/country_hotspots.csv`
- `public/data/country_hotspots.csv`
- `data/processed/country_hotspots_data_dictionary.csv`
- `docs/B2_faostat_fetch_method.md`
- optional `notebooks/02_fetch_faostat_drained_organic_soils.ipynb`

## Required checks

1. Determine the most reliable current access route:
   - FAOSTAT API
   - FAOSTAT bulk download
   - FAO data portal
   - fallback through derived/manual CSV export

2. Identify exact variables:
   - drained organic soils area
   - CO2 emissions
   - N2O emissions
   - total CO2e emissions if available

3. Harmonise country codes:
   - country name
   - FAOSTAT area code
   - ISO3

4. Compute:
   - total emissions
   - emissions density
   - hotspot ranks
   - hotspot class

5. Document:
   - access date
   - source URL
   - variables
   - units
   - conversions
   - limitations

## Acceptance criteria

- `country_hotspots.csv` contains one row per country/year selected.
- Units are explicit.
- Missing data are not hidden.
- Derived fields are reproducible.
- File is small enough for GitHub.
- No licence-sensitive raw data are committed.
