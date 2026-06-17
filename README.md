# Peatland Transition Atlas

**Interactive literature-driven prototype on peatland rewetting, GHG mitigation and transition-compatible agricultural land use.**

The project maps the space between drainage-based agriculture and rewetting-compatible land-use pathways. It starts from curated scientific literature and translates it into an exploratory web atlas: international evidence regions, transition pathways, trade-offs and transfer hypotheses for South German dairy, forage and biogas regions.

## Live prototype

After GitHub Pages is enabled, the site will be available at:

```text
https://<your-github-username>.github.io/peatland-transition-atlas/
```

## What this prototype does

Phase A is a literature-driven MVP. It contains:

- a six-part scrollytelling structure,
- an international evidence map,
- transition pathway cards,
- a qualitative pathway matrix,
- a South Germany fit chart,
- a visible method and uncertainty section,
- a file-based AI-agent workflow for supervised project development.

## What this prototype does not claim

This is **not** a validated regional decision-support model.

Important limitations:

- Scores are qualitative literature-informed expert codings, not statistical estimates.
- Evidence-map points are approximate visual anchors, not exact field-site coordinates.
- South Germany fit is a transfer hypothesis, not a validated regional model result.
- The prototype does not include confidential PALUD/RoGeR outputs.
- The repository should not include copyrighted PDFs or licence-unclear raw geodata.

## Current datasets

```text
public/data/papers.csv
public/data/papers.json
public/data/transition_pathways.csv
public/data/transition_pathways.json
public/data/region_case_studies.geojson
public/data/atlas_story_sections.json
public/data/atlas_wireframes.json
```

## Local preview

Because the site loads JSON/GeoJSON files, run it through a local server:

```bash
cd peatland-transition-atlas
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

On Windows, if `python` does not work, use:

```bash
py -m http.server 8000
```

## GitHub Pages deployment

1. Create a GitHub repository named:

```text
peatland-transition-atlas
```

2. Push or upload this project folder.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, choose:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/root**
5. Save and wait for GitHub Pages to publish.

## Repository structure

```text
peatland-transition-atlas/
├── index.html
├── src/
│   ├── app.js
│   └── styles.css
├── public/
│   └── data/
├── data/
│   ├── processed/
│   ├── raw/
│   ├── external/
│   └── metadata/
├── docs/
├── agents/
├── tasks/
├── notebooks/
├── .gitignore
├── .nojekyll
├── LICENSE
└── README.md
```

## AI-agent workflow

This repository is also a learning project for supervised AI-agent workflows.

Agent role definitions:

```text
agents/
├── 00_orchestrator.md
├── 01_research_evidence_agent.md
├── 02_data_gis_agent.md
├── 03_visualization_engineer_agent.md
├── 04_story_editorial_agent.md
├── 05_qa_critic_agent.md
└── 06_release_agent.md
```

Task files:

```text
tasks/
├── backlog.md
├── phase_A_tasks.md
├── phase_B_hotspot_tasks.md
└── done.md
```

The workflow is supervised:

```text
Agent proposes/executes bounded task → Human Lead reviews → QA gate → next task
```

## Phase B roadmap

Phase B will add public hotspot data:

- FAO/FAOSTAT drained organic soils area and emissions,
- Global Peatland Map / Global Peatland Database aggregates,
- Natural Earth country boundaries,
- Eurostat GISCO NUTS geometries,
- optional Copernicus / Thünen / LGRB context layers.

Target output:

```text
country_hotspots.csv
```

## Suggested GitHub topics

```text
data-visualization
peatlands
rewetting
paludiculture
climate-mitigation
agriculture
scrollytelling
geojson
ai-agents
scientific-visualization
```

## Licence

Code: MIT License.  
Derived literature-coding data: treat as project-authored research metadata; check and document reuse terms before external publication.

## Phase B — Country-level peatland hotspot layer

Phase B extends the atlas from a literature-driven transition prototype into a first data-backed hotspot atlas.

The current hotspot layer uses country-level drained organic soils data to show:

- total drained-organic-soils greenhouse-gas emissions,
- emissions density per hectare of drained organic soils,
- top hotspot countries by total emissions,
- top hotspot countries by emissions density,
- a lightweight country-level choropleth map,
- a toggle between total emissions and emissions density,
- linked ranking/map interaction.

Important interpretation boundary:

This layer is a national-level screening layer. It does not show local rewetting suitability, hydrological feasibility, farm-scale constraints, land tenure or policy readiness.

Key public data files:

- `public/data/country_hotspots.csv`
- `public/data/hotspot_countries_110m.geojson`
