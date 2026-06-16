# A3 Report — Evidence Region Review

Date: 2026-06-16

## Agent role

Research & Evidence Agent

## Task

Review and improve the evidence-region layer so that the map cards are scientifically cautious, useful and not geographically misleading.

## Files changed

- `data/processed/region_case_studies.geojson`
- `data/processed/region_case_studies.csv`
- `public/data/region_case_studies.geojson`
- `public/data/region_case_studies.csv`
- `data/processed/region_case_studies_data_dictionary.csv`
- `public/data/region_case_studies_data_dictionary.csv`

## Main changes

### 1. Evidence types added

Added `evidence_type` to distinguish:

- empirical clusters,
- model/policy clusters,
- site LCA cases,
- qualitative adoption cases,
- review/conceptual clusters,
- policy nodes.

### 2. Transfer confidence added

Added `transfer_confidence` to clarify whether a node is useful for:

- direct empirical analogy,
- conceptual framing,
- policy context,
- or only weak/niche transfer.

### 3. Coordinate precision added

Added `coordinate_precision` to reduce false spatial precision.

Examples:

- `country_anchor`
- `regional_anchor`
- `multi_region_anchor`
- `conceptual_anchor`
- `policy_anchor`

### 4. Region cards sharpened

Each region now has a more cautious:

- key message,
- South Germany transfer note,
- caveat,
- visual story role.

## Scientific caution improvements

### Netherlands

Now framed as a strong grassland/dairy analogue, but conditional on hydrology, governance, infrastructure and machinery.

### Finland

Now framed as economic-policy evidence, not a direct estimate of South German costs.

### Denmark

Now framed as reed canary grass / biomass evidence conditional on water table and LCA assumptions.

### UK Fens

Now framed as productive-peatland context, not a quantitative transfer case.

### Teufelsmoor and pioneer farms

Now clearly adoption evidence, not hydrological or GHG evidence.

### Reed and water buffalo nodes

Now framed as niche/value-chain/habitat pathways, not general substitutes for mainstream agriculture.

### International synthesis and EU policy nodes

Now clearly labelled as conceptual/policy framing rather than field evidence.

## Acceptance criteria check

| Criterion | Status |
|---|---|
| Every region card has one clear key message | PASS |
| Transfer notes are cautious | PASS |
| Conceptual/review/policy nodes separated from field evidence | PASS |
| Caveats are specific | PASS |
| Approximate coordinates are more clearly documented | PASS |
| Map remains useful as evidence map | PASS |

## Remaining issue

The current web card does not yet display the new fields:

- `evidence_type`
- `transfer_confidence`
- `coordinate_precision`

This should be handled by a small Visualization Engineer task.

## Recommended next task

Proceed to:

```text
A6 — Display evidence type and coordinate caution in map cards
```

or continue with:

```text
A4 — Transition score review
```

Recommended order: A6 first, because the new evidence-review fields should become visible in the interface.
