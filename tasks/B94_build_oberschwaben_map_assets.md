# B94 - Build Oberschwaben Map Assets

Created from B93 on 2026-06-23

## Goal

Build the first Oberschwaben implementation map asset.

Primary target:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Required before starting

Confirm data decisions from:

```text
docs/B93_oberschwaben_data_decision_matrix.csv
```

At minimum decide:

1. administrative boundary source,
2. agricultural land-use source,
3. moor/organic/wetland soil context source,
4. whether first map is visual-only or includes area indicators.

## Expected workflow

1. create focus region for Ravensburg, Biberach, Sigmaringen, Bodenseekreis,
2. clip agriculture layer,
3. clip moor/soil context layer,
4. intersect agriculture and moor/soil context,
5. design first composite map,
6. export 1600 x 900 PNG,
7. document sources and method boundary,
8. run visual QA.

## Do not

- place raw GIS files in `public/maps/oberschwaben/`,
- call the intersection a suitability map,
- call it a priority map,
- expose farm-level data,
- bind to website before visual review.
