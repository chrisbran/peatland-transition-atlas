# Phase B — Public Hotspot Data Plan

Phase B extends the literature-driven Transition Atlas with spatial hotspot data.

## Target output

```text
data/processed/country_hotspots.csv
public/data/country_hotspots.csv
```

Suggested schema:

```text
country_iso3
country_name
peatland_area_km2
drained_organic_soils_area_ha
co2_emissions_gg
n2o_emissions_gg
co2eq_emissions_t
emissions_per_ha_tco2eq
hotspot_rank
data_source
source_year
processing_note
```

## Priority data sources

### 1. FAOSTAT / FAO Drained Organic Soils

Purpose:
- country-level or raster-derived estimates of drained organic soils area and emissions.

Access:
- FAOSTAT download/API
- FAO Google Earth Engine datasets if using raster workflow

Processing:
- filter for latest available year
- aggregate by country
- harmonise ISO3 country codes
- calculate emissions per ha

### 2. Global Peatland Map / Global Peatland Database

Purpose:
- global peatland/organic soil extent.

Processing:
- download raster if allowed
- aggregate peatland cells by country boundary
- export only country-level aggregates for GitHub

### 3. Natural Earth

Purpose:
- country boundaries for static map.
- public-domain, lightweight base layer.

Processing:
- download low-resolution country polygons
- simplify geometry
- export GeoJSON or TopoJSON

### 4. Eurostat GISCO NUTS

Purpose:
- Europe/Germany zoom layer.

Processing:
- download NUTS GeoJSON/TopoJSON
- simplify geometry
- aggregate hotspot data later if compatible

## Implementation sequence

1. Create `country_hotspots_schema.csv`.
2. Fetch country-level FAOSTAT drained organic soil emissions.
3. Add Natural Earth country boundaries.
4. Join emissions to boundaries.
5. Build a first global hotspot choropleth.
6. Add Global Peatland Map aggregates only if licence and processing workflow are clear.
7. Add European / Germany zoom layers later.
