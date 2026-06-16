# Peatland Transition Atlas — Storyboard

This storyboard defines the first public MVP structure for a combined Peatland Hotspot Atlas and Transition Atlas.

The sequence is designed as a scrollytelling portfolio project: the user moves from spatial climate hotspot framing to hydrology, international evidence, transition pathways, South Germany transfer, and the modelling frontier.

## 1. The hidden climate hotspot

**Subtitle:** Small areas, disproportionate emissions

**Main message:** Peatland climate mitigation starts with identifying where organic soils, agricultural use and emissions overlap.

**Story:** Drained agricultural peatlands and organic soils occupy a relatively small share of agricultural land, but they can dominate land-use related greenhouse gas emissions. The Atlas opens with the spatial problem: where peatlands, drainage and agricultural land use overlap, climate mitigation becomes a land-use question.

**Visualisation:** scrollytelling_map_hotspots — Global-to-European map zoom

**Interaction:** Start with a global map, then zoom to Europe and South Germany. Toggle peatland extent, drained organic soils, agricultural land cover and emissions if public layers are available.

**Required data:** `country_hotspots.csv|global_peatland_extent|drained_organic_soils_emissions|natural_earth_boundaries`

**Related papers:** `P001|P021|P005`

**Related pathways:** `T01|T08`

**Callout:** The hotspot is not only ecological. It is hydrological, agricultural and economic.

## 2. The water table is the lever

**Subtitle:** Rewetting only matters if groundwater actually rises

**Main message:** GHG mitigation potential is not determined by peatland area alone, but by achievable water-table depth and site response.

**Story:** The mitigation effect of peatland rewetting is controlled by the water table that can actually be achieved. A hectare of peatland is therefore not a uniform mitigation unit. Hydrological feasibility, spatial heterogeneity and management determine whether rewetting turns into real greenhouse gas reduction.

**Visualisation:** interactive_water_table_slider — Water-table gradient with linked outcome cards

**Interaction:** User drags a water-table slider from deeply drained to near-surface conditions. Cards update for CO2, CH4 risk, trafficability, production continuity and feasible land-use pathways.

**Required data:** `transition_pathways.csv|papers.csv|water_table_effect_rules.csv`

**Related papers:** `P006|P007|P008|P009|P010|P011`

**Related pathways:** `T01|T02|T03|T04|T05|T08`

**Callout:** The same rewetting target can create very different outcomes depending on the water table that is actually reached.

## 3. Evidence from elsewhere

**Subtitle:** What international studies contribute to the transition debate

**Main message:** The international literature does not offer one universal solution. It provides a structured set of transferable lessons.

**Story:** Different countries contribute different pieces of the evidence base. The Netherlands provides strong evidence on peat pasture, water management and trafficability. Finland contributes farm-level and national economic modelling. Denmark provides water-table mapping and reed canary grass evidence. Germany and the UK contribute adoption, policy and productive peatland transition perspectives.

**Visualisation:** interactive_evidence_map — Map with evidence-region nodes and paper cards

**Interaction:** Click a region node to open a card with supporting papers, key message, pathway relevance, South Germany transfer note and caveat. Filter by hydrology, economics, biomass, grazing, adoption and governance.

**Required data:** `region_case_studies.geojson|papers.csv|transition_pathways.csv`

**Related papers:** `P004|P006|P007|P008|P009|P010|P011|P014|P016|P017|P018`

**Related pathways:** `T02|T03|T04|T05|T06|T07|T08`

**Callout:** The Atlas treats papers as evidence nodes, not as isolated references.

## 4. The transition space

**Subtitle:** Between drained farming and full restoration

**Main message:** The relevant design space is a spectrum of wet or partially wet land-use pathways, each with different trade-offs.

**Story:** The literature suggests that agricultural peatland rewetting should not be visualised as a binary choice. Between current drainage-based farming and full restoration lies a transition space: partial water management, raised-water-table pasture, wet mowing, reed canary grass biomass, reed value chains and robust grazing.

**Visualisation:** pathway_spectrum_matrix — Horizontal wetness-gradient diagram plus comparison matrix

**Interaction:** User selects a pathway. The matrix highlights GHG potential, water-table requirement, trafficability constraint, farm compatibility, market maturity, adoption barrier and South Germany fit.

**Required data:** `transition_pathways.csv|papers.csv`

**Related papers:** `P001|P002|P003|P004|P006|P008|P009|P014|P015|P016|P017|P020|P021`

**Related pathways:** `T01|T02|T03|T04|T05|T06|T07|T08`

**Callout:** The question is not whether agriculture stays or disappears, but what kind of agriculture remains possible under wetter conditions.

## 5. What fits South Germany?

**Subtitle:** From international evidence to regional transition hypotheses

**Main message:** South Germany needs transition-compatible pathways that connect GHG mitigation with recognisable farm systems.

**Story:** Not every wet land-use pathway is equally plausible in South German dairy, forage and biogas regions. The Atlas translates international evidence into a South Germany fit view. Raised-water-table peat pasture and wet grassland mowing appear more compatible with existing grassland systems than highly specialised product chains, although all pathways depend on hydrology, machinery access, markets and farmer adoption.

**Visualisation:** south_germany_fit_bubble_matrix — Bubble chart: hydrological requirement × farm compatibility; size = GHG potential; colour = adoption/market risk

**Interaction:** Hover on each pathway to show supporting papers and caveats. Toggle criteria: farm compatibility, market maturity, trafficability, adoption barrier.

**Required data:** `transition_pathways.csv|papers.csv|regional_context_layers_optional`

**Related papers:** `P008|P009|P014|P015|P016|P017|P020`

**Related pathways:** `T03|T04|T05|T06|T07`

**Callout:** A pathway can be scientifically plausible but regionally weak if it lacks farm compatibility, machinery access or markets.

## 6. The modelling frontier

**Subtitle:** Connecting hydrology, mitigation and farm-level exposure

**Main message:** The next generation of peatland decision tools must connect hydrological feasibility, GHG mitigation, farm-level economics and transition-compatible land use.

**Story:** The Atlas ends with the research frontier: international evidence provides many building blocks, but local decisions require integrated modelling. Hydrology determines achievable water tables and mitigation; farm structure determines economic exposure; transition pathways determine whether rewetting can become an implementable land-use transformation.

**Visualisation:** conceptual_dependency_diagram — Hydrology → water table → GHG mitigation → farm exposure → transition pathway diagram

**Interaction:** Click each node to reveal data requirements, current evidence and remaining gaps. Optional: link to PALUD/RoGeR research context without exposing sensitive data.

**Required data:** `papers.csv|transition_pathways.csv|methodology_notes|future_model_outputs_optional`

**Related papers:** `P001|P006|P010|P011|P016|P018|P021`

**Related pathways:** `T02|T03|T04|T08`

**Callout:** A map of peatland area is not enough. The real decision unit is the interaction of water, emissions, farms and feasible transitions.
