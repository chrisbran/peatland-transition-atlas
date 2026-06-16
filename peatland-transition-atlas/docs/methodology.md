# Methodology

This prototype is a literature-driven visualisation MVP.

## Evidence base

The first version uses curated peatland rewetting literature coded into three linked datasets:

1. `papers.csv`
2. `transition_pathways.csv`
3. `region_case_studies.geojson`

## Coding approach

The transition scores are qualitative, literature-informed expert codings.

They are used to support exploratory visualisation, not to claim statistically estimated effect sizes.

Score interpretation:

```text
1 = low
2 = medium
3 = high
0 = not applicable / reference state
```

## Region geometry

The evidence-map points are approximate anchors.

They can represent:

- exact-ish regional case studies,
- national model studies,
- multi-region studies,
- European policy nodes,
- global/conceptual review nodes.

Therefore, coordinates must not be interpreted as field-site coordinates.

## Publication principles

The GitHub repository should include:

- source code,
- processed lightweight datasets,
- metadata and methodology,
- links/DOIs to papers.

It should not include:

- copyrighted PDFs,
- large raw geospatial rasters,
- confidential project outputs,
- unpublished partner data.
