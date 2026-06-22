# B10 — Peat/Organic-Soils Data Source Inventory

Date: 2026-06-17

## Purpose

This inventory prepares the next atlas stage: moving from national emission hotspots to actual peat/organic-soil spatial extent.

The current Phase B map answers:

> Which countries report large drained-organic-soils emissions?

The next scrollytelling layer should answer:

> Where are peatlands and organic soils actually located within and across countries?

## Core design principle

Do not mix the meanings of the layers.

| Layer | Main question | Use |
|---|---|---|
| Country hotspot layer | Where are emissions concentrated at national level? | Screening and ranking |
| Peat/organic-soil extent layer | Where are the relevant soils/peatland areas spatially located? | Spatial context and zoom story |
| Regional suitability layer | Which areas could plausibly transition? | Not yet available; would need additional hydrology, land use, ownership and policy data |

## Recommended scrollytelling sequence

1. **World emissions hotspot view**  
   Show existing country-level drained organic soil emissions.

2. **World peat/organic-soil extent view**  
   Fade from country emissions to global peat/organic-soil distribution.

3. **Europe zoom**  
   Use European Wetland Map / European peatland classes to make continental distribution visible.

4. **Germany zoom**  
   Use the German organic-soils kulisse to connect national emissions to actual organic-soil areas.

5. **Baden-Württemberg zoom**  
   Use BK50-Moor to show regional Moor-/Feuchtgebiets-/humusreiche Grundwasserboden-Kulisse.

6. **Interpretation boundary**  
   Explain why spatial peat/soil extent is still not the same as rewetting feasibility.

## Source inventory

| Scale | Candidate layer | Provider | Priority | Atlas use | Main limitation |
|---|---|---:|---|---|---|
| Global | Global Peatland Map 2.0 / Global Peatland Database | Greifswald Mire Centre / IMCG | High | World peat/organic-soil background | Coarse for regional interpretation |
| Global | Global Peatlands dataset | Global Forest Watch | Medium | Fallback/comparison | Composite source logic must be checked |
| Europe | European Wetland Map | ALFAwetlands / WET HORIZONS / Zenodo | High | Europe zoom layer | Large dataset; class filtering needed |
| Europe | Distribution of peatland in Europe | ESDAC/JRC | Low-Medium | Reference/comparison | May be older/less suitable than EWM |
| Germany | Aktualisierte Kulisse organischer Böden in Deutschland | Thünen / OpenAgrar | Very high | Germany zoom layer | Manual download and attribute review needed |
| Baden-Württemberg | BK50-Moor | LGRB / LUBW metadata | Very high | Regional zoom layer | Not sufficient for local rewetting planning |
| Baden-Württemberg | Historische Moorbodenkarte BW | LUBW | Low-Medium | Historical/context layer | Less suitable than BK50-Moor for current climate analysis |

## Data-processing implications

For web display, raw GIS datasets must not be pushed directly into the site. The workflow should be:

1. Download raw files into `data/external/peat_soils/`.
2. Inspect projection, attributes, classes and license.
3. Reproject if necessary.
4. Clip by scale/region where relevant.
5. Dissolve or simplify geometries.
6. Export web-sized GeoJSON or TopoJSON to `public/data/`.
7. Document every transformation.

## Proposed next task

B11 should build the first minimum viable peat/organic-soils layer:

- start with **Baden-Württemberg BK50-Moor** or **Germany organic-soils kulisse**, because these are most relevant to the final regional story;
- only then add global/Europe layers for the guided scroll zoom sequence.

## Why start regionally?

The global map is visually impressive but coarse. The Baden-Württemberg/Germany layers are more directly linked to the project narrative and make the story scientifically more credible.
