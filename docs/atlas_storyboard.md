# Peatland Transition Atlas — Storyboard

Story & Editorial Agent revision. This storyboard defines the public-facing Phase A narrative.

Narrative arc:

```text
Hotspot → Water-table mechanism → International evidence → Transition spectrum → South Germany transfer → Modelling frontier
```

## 1. The hidden climate hotspot

**Subtitle:** Small areas, disproportionate emissions

**Main message:** Drained agricultural peatlands are climate hotspots because peat, drainage and production overlap.

**Story text:** Drained agricultural peatlands are not only ecological remnants. Where organic soils, drainage and farming overlap, they become climate-relevant production landscapes. The Atlas starts by locating this overlap before asking which transitions are possible.

**Callout:** The hotspot is hydrological, agricultural and economic — not only ecological.

**Visualisation:** scrollytelling_map_hotspots — Global-to-European map zoom

**Interaction:** Start with a global map, then zoom to Europe and South Germany. Toggle peatland extent, drained organic soils, agricultural land cover and emissions if public layers are available.

**Data:** `country_hotspots.csv|global_peatland_extent|drained_organic_soils_emissions|natural_earth_boundaries`

## 2. The water table is the lever

**Subtitle:** Area alone does not determine mitigation

**Main message:** The decisive variable is not peatland area alone, but achievable water-table depth.

**Story text:** Peatland mitigation depends on the water table that can actually be achieved. The same mapped peatland area can lead to different climate, management and production outcomes depending on groundwater level, soil conditions and land-use intensity.

**Callout:** A hectare of peatland is not a uniform mitigation unit.

**Visualisation:** interactive_water_table_slider — Water-table gradient with linked outcome cards

**Interaction:** User drags a water-table slider from deeply drained to near-surface conditions. Cards update for CO2, CH4 risk, trafficability, production continuity and feasible land-use pathways.

**Data:** `transition_pathways.csv|papers.csv|water_table_effect_rules.csv`

## 3. Evidence from elsewhere

**Subtitle:** International studies as a structured evidence layer

**Main message:** International evidence does not provide one solution; it provides transferable lessons.

**Story text:** Different countries contribute different pieces of the transition puzzle: Dutch studies highlight raised groundwater, peat pasture and trafficability; Finnish studies model incentives and compensation; Danish studies test biomass pathways; German and UK studies add adoption, governance and productive-peatland perspectives.

**Callout:** The Atlas treats papers as evidence nodes, not as isolated references.

**Visualisation:** interactive_evidence_map — Map with evidence-region nodes and paper cards

**Interaction:** Click a region node to open a card with supporting papers, key message, pathway relevance, South Germany transfer note and caveat. Filter by hydrology, economics, biomass, grazing, adoption and governance.

**Data:** `region_case_studies.geojson|papers.csv|transition_pathways.csv`

## 4. The transition space

**Subtitle:** Between drained farming and full restoration

**Main message:** The design space is a spectrum of wetter land-use pathways, each with different trade-offs.

**Story text:** Rewetting should not be visualised as a binary choice between current farming and complete restoration. The literature describes a transition space: partial water management, raised-water-table pasture, wet mowing, wet biomass, reed value chains, robust grazing and restoration.

**Callout:** The key question is what kind of agriculture remains possible under wetter conditions.

**Visualisation:** pathway_spectrum_matrix — Horizontal wetness-gradient diagram plus comparison matrix

**Interaction:** User selects a pathway. The matrix highlights GHG potential, water-table requirement, trafficability constraint, farm compatibility, market maturity, adoption barrier and South Germany fit.

**Data:** `transition_pathways.csv|papers.csv`

## 5. What fits South Germany?

**Subtitle:** From evidence to transfer hypotheses

**Main message:** South Germany needs transition pathways that connect mitigation with recognisable farm systems.

**Story text:** Not every wet land-use pathway is equally plausible in South German dairy, forage and biogas regions. The Atlas translates international evidence into transfer hypotheses, asking which pathways might align with hydrology, machinery access, farm structure, markets and adoption conditions.

**Callout:** A pathway can be scientifically plausible and still fail without farm compatibility, machinery access or markets.

**Visualisation:** south_germany_fit_bubble_matrix — Bubble chart: hydrological requirement × farm compatibility; size = GHG potential; colour = adoption/market risk

**Interaction:** Hover on each pathway to show supporting papers and caveats. Toggle criteria: farm compatibility, market maturity, trafficability, adoption barrier.

**Data:** `transition_pathways.csv|papers.csv|regional_context_layers_optional`

## 6. The modelling frontier

**Subtitle:** Where the atlas meets research infrastructure

**Main message:** The next decision tools must connect hydrology, GHG mitigation, farm economics and viable land use.

**Story text:** The literature provides building blocks, but local decisions require integrated modelling. Hydrology determines achievable water tables; water tables shape emissions; farm structure shapes economic exposure; and viable pathways determine whether rewetting can become implementable.

**Callout:** A peatland map is not enough; the decision unit is the interaction of water, emissions, farms and transition options.

**Visualisation:** conceptual_dependency_diagram — Hydrology → water table → GHG mitigation → farm exposure → transition pathway diagram

**Interaction:** Click each node to reveal data requirements, current evidence and remaining gaps. Optional: link to PALUD/RoGeR research context without exposing sensitive data.

**Data:** `papers.csv|transition_pathways.csv|methodology_notes|future_model_outputs_optional`
