# Task B15 — Process Europe Wetland/Peat Layer

## Agent

Data & GIS Agent + Visualization Engineer Agent + QA Critic Agent

## Goal

Replace the Europe placeholder in the sticky-scroll story with a real European wetland/peat context layer.

## Candidate source

European Wetland Map / Zenodo.

## Recommended approach

1. Download relevant European Wetland Map data.
2. Identify classes suitable for peatland/organic-soil context.
3. Clip or simplify for web display.
4. Export to `public/data/europe_peat_wetland_simplified.geojson`.
5. Bind the Europe sticky-story step to the real layer.
6. Document caveats and source attribution.

## Acceptance criteria

- public file is small enough for GitHub Pages,
- Europe layer is clearly labelled as wetland/peat context,
- class meanings are documented,
- no raw files under `data/external/` are committed,
- story still distinguishes extent/context from suitability.
