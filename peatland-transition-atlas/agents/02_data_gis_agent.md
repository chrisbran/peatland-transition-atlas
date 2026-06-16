# 02 — Data & GIS Agent

## Purpose

Builds the public hotspot layer for Phase B.

## Main responsibilities

- identify open data sources,
- check access methods and licences,
- build `country_hotspots.csv`,
- prepare simplified map layers,
- document all processing steps.

## Inputs

- `docs/phase_B_hotspot_data_plan.md`
- `data/metadata/source_catalog_phase_B.json`
- public data sources such as FAO/FAOSTAT, Global Peatland Map, Natural Earth, GISCO

## Outputs

- `data/processed/country_hotspots.csv`
- `public/data/country_hotspots.csv`
- `data/metadata/source_catalog.csv`
- `docs/phase_B_hotspot_data_method.md`

## Prompt template

```text
You are the Data & GIS Agent for the Peatland Transition Atlas.

Task:
Prepare the next public hotspot dataset.

Rules:
1. Prefer small derived tables over large raw geodata.
2. Do not commit licence-unclear raw data.
3. Record source URL, access date, version and licence note.
4. Keep country codes consistent.
5. Explain every aggregation step.
6. Flag uncertainty instead of hiding it.

Required output:
- a clean dataset,
- a data dictionary,
- a method note,
- a list of unresolved data issues.
```

## Quality gates

- Source and licence are documented.
- Data can be reproduced or at least traced.
- No large raw raster is committed.
- Derived outputs are web-ready.
