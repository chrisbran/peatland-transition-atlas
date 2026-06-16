# Phase B Tasks — Hotspot Data

## B1 — Define country hotspot schema

**Agent:** Data & GIS Agent

Output:
- `data/processed/country_hotspots_schema.csv`
- `docs/phase_B_hotspot_data_method.md`

## B2 — Fetch FAOSTAT / FAO drained organic soils data

Output:
- raw data saved locally if licence permits
- derived `country_hotspots.csv`

Acceptance:
- Source documented.
- Country codes harmonised.
- Emissions fields clearly defined.

## B3 — Prepare Natural Earth boundaries

Output:
- simplified boundaries in `public/data/`
- source and licence note

Acceptance:
- File size suitable for GitHub Pages.
- Projection and simplification documented.

## B4 — Build hotspot map section

Agent:
- Visualization Engineer Agent

Acceptance:
- Choropleth loads on GitHub Pages.
- Legend and units are clear.
- Missing data is visually handled.

## B5 — QA and release

Agent:
- QA & Critic Agent
- Release Agent

Acceptance:
- No licence-sensitive raw data committed.
- All sources documented.
- Hotspot claims are defensible.
