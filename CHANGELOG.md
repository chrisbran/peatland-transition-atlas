# Changelog

## v0.2.0 — Country-level hotspot atlas draft (2026-06-17)

### Added

- Country-level drained organic soils hotspot dataset.
- Public hotspot dataset for GitHub Pages.
- Natural Earth 110m country boundary join.
- Country-level choropleth map.
- Map metric toggle:
  - total emissions,
  - emissions density.
- Top-10 hotspot rankings by total emissions and emissions density.
- Ranking/map interaction with selected-country highlighting.
- Method notes for B2b–B6c.

### Known limitations

- The choropleth is national-level only.
- It is not a local rewetting suitability map.
- Some small territories are unmatched in the Natural Earth 110m join.
- The map uses a simple dependency-free SVG projection and is not yet cartographically refined.
- Highlight colors and map palette are intentionally provisional.

### Next

- B8 visual refinement:
  - softer highlight color,
  - clearer ocean/land contrast,
  - map projection/perspective review,
  - possible no-data and desert/background distinction.

## 0.1.0 — Phase A literature-driven MVP (2026-06-16)

### Added

- Static web prototype:
  - Hero section
  - Six-part story structure
  - International evidence map
  - Evidence region cards
  - Transition pathway spectrum
  - Pathway matrix
  - South Germany fit chart
  - Method and uncertainty panel

- Literature-driven datasets:
  - `papers.csv`
  - `papers.json`
  - `transition_pathways.csv`
  - `transition_pathways.json`
  - `region_case_studies.geojson`
  - `atlas_story_sections.json`
  - `atlas_wireframes.json`

- AI-agent workflow:
  - Orchestrator Agent
  - Research & Evidence Agent
  - Data & GIS Agent
  - Visualization Engineer Agent
  - Story & Editorial Agent
  - QA & Critic Agent
  - Release Agent

- Documentation:
  - GitHub setup
  - Folder structure
  - Methodology
  - Acceptance criteria
  - Release checklist
  - AI-agent learning path
  - Phase B hotspot data plan

### Reviewed

- Local preview passed.
- Transition scores reviewed and kept as qualitative codings.
- Evidence-region cards reviewed and simplified.
- Storyline revised into a clear narrative arc.

### Known limitations

- No public hotspot geodata layer yet.
- No FAO/FAOSTAT country hotspot table yet.
- Evidence-map points are approximate anchors.
- South Germany fit chart is qualitative and hypothesis-generating.
