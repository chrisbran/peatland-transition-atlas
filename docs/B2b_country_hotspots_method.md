# B2b — Country Hotspots from Drained Organic Soils

## Status

Interim country-level hotspot dataset for Phase B.

## Input files

- `data\external\faostat\emissions-from-drained-organic-soils.csv`
- `data\external\faostat\emissions_agriculture_cultivated_organic_soils_e_all_data_norm.csv`

## Selected year

`2019`

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
