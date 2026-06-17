# Folder Structure

Recommended repository structure for the Peatland Transition Atlas.

```text
peatland-transition-atlas/
├── index.html
├── src/
│   ├── app.js
│   └── styles.css
├── public/
│   ├── data/
│   └── assets/
├── data/
│   ├── raw/
│   ├── external/
│   ├── processed/
│   └── metadata/
├── notebooks/
├── docs/
├── LICENSE
├── .gitignore
└── README.md
```

## What goes where

### `index.html`
Main static web page.

### `src/`
Frontend source files.

- `app.js`: loads data, renders sections, map nodes, pathway matrix and fit chart.
- `styles.css`: visual design.

### `public/data/`
Small web-ready datasets loaded by the browser.

Allowed:

- CSV
- JSON
- GeoJSON
- simplified TopoJSON/GeoJSON

Avoid:

- large rasters
- original PDFs
- licence-unclear source datasets

### `data/raw/`
Local raw data used during processing. Usually not committed if large or licence-sensitive.

### `data/external/`
Downloaded third-party data. Commit only if file size and licence allow it.

### `data/processed/`
Clean, derived, lightweight outputs that can be committed.

### `data/metadata/`
Source catalogues, access dates, licence notes, field definitions.

### `notebooks/`
Python notebooks for data processing.

Suggested notebooks for Phase B:

```text
01_prepare_literature_data.ipynb
02_fetch_faostat_drained_organic_soils.ipynb
03_prepare_global_peatland_map_aggregates.ipynb
04_prepare_boundaries_natural_earth_gisco.ipynb
05_build_country_hotspots.ipynb
```

### `docs/`
Methodology, design rationale, data source notes and GitHub setup instructions.
