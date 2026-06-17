# B2a — N2O Hotspots from Cultivation of Organic Soils

## Status

Interim country-level dataset.

## Input

`data\external\faostat\emissions_agriculture_cultivated_organic_soils_e_all_data_norm.csv`

## Selection

- item: `Cropland and grassland organic soils`
- area element: `Area`
- emissions element: `Emissions (CO2eq) from N2O (AR5)`
- unit: Gigagrams = kilotonnes CO2e
- exact year: `2019`
- aggregate and historical/non-current labels removed using a conservative name filter

## Outputs

- `data/processed/country_hotspots_n2o.csv`
- `public/data/country_hotspots_n2o.csv`

## Important limitation

This is not yet total drained organic soil emissions. It excludes CO2 emissions from drained cropland/grassland organic soils.

Use this table only as an interim QA dataset until the CO2 land-use component or a combined drained-organic-soils export is added.

## Known data-processing decision

The script selects one exact year rather than the latest available year per country. This avoids mixing current countries with historical entities such as USSR or projection years such as 2050.
