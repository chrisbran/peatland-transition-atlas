# B1 — Country Hotspots Data Plan

Date: 2026-06-17

## Agent role

Data & GIS Agent

## Phase B objective

Build the first real hotspot layer for the Peatland Transition Atlas.

Phase A shows literature evidence and transition pathways. Phase B adds a spatial country-level hotspot layer:

```text
Where are drained agricultural organic soils producing the largest GHG emissions?
```

## MVP output

The first Phase B target dataset is:

```text
data/processed/country_hotspots.csv
public/data/country_hotspots.csv
```

For B1, only the schema and source catalog are created:

```text
data/processed/country_hotspots_schema.csv
public/data/country_hotspots_schema.csv
data/metadata/source_catalog_phase_B.csv
data/metadata/source_catalog_phase_B.json
```

## Core dataset logic

The MVP should be country-level, not raster-level.

Reasons:

1. It is easier to reproduce.
2. It is small enough for GitHub Pages.
3. It creates a meaningful hotspot map quickly.
4. It avoids committing heavy raw geodata.
5. It keeps Phase B aligned with the portfolio goal.

## Required variables

```text
iso3
country
year
drained_organic_soils_area_ha
emissions_total_kt_co2e
emissions_density_t_co2e_per_ha
hotspot_class
source_area
source_emissions
```

## Recommended variables

```text
emissions_co2_kt
emissions_n2o_kt_co2e
hotspot_rank_total
hotspot_rank_density
data_quality_note
```

## Optional later variables

```text
peatland_area_km2
drained_share_of_peatland
```

## Source priority

### Priority 1 — FAOSTAT / FAO drained organic soils data

Use for country-level drained organic soils area and emissions.

### Priority 2 — Natural Earth Admin 0 Countries

Use for lightweight country geometries and ISO joins.

### Priority 3 — Global Peatland Map 2.0

Use later for peatland extent context. Do not make this the first blocking dependency.

### Fallback / validation — FAO Earth Engine DROSA-A and DROSE-A

Use only if country-level FAOSTAT extraction is difficult or if validation/geospatial context is needed.

## Derived metrics

```text
emissions_density_t_co2e_per_ha =
    emissions_total_kt_co2e * 1000 / drained_organic_soils_area_ha
```

Initial hotspot classes:

```text
very_high
high
medium
low
no_data
```

Use quantiles for first MVP. Replace with policy-relevant thresholds only if justified later.

## Important caveats

1. Country-level hotspots do not identify local rewetting opportunities.
2. Total emissions and emissions density answer different questions.
3. Small drained areas can produce unstable density values.
4. FAO/FAOSTAT estimates are modelled/geospatially derived and may differ from national inventory reporting.
5. Global peatland extent and drained organic soil area are not directly comparable without harmonisation.

## Publication rule

Commit to GitHub:

```text
small derived CSV/JSON/GeoJSON files
method notes
source catalog
scripts/notebooks
```

Do not commit:

```text
large raw rasters
licence-unclear geodata
copyrighted PDFs
confidential PALUD/RoGeR data
API keys
```

## Next task

```text
B2 — Fetch FAOSTAT drained organic soils country data
```
