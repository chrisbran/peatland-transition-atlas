# B95h - Oberschwaben Scrolly Layer-Stack QA

Date: 2026-06-24

## Result

**PASS**

## Required layer-stack assets

- `public/maps/oberschwaben/oberschwaben_admin_context.png` — admin context: Landkreisgrenzen und Landkreisnamen; should normally be visible above thematic layers.
- `public/maps/oberschwaben/oberschwaben_agriculture.png` — agriculture layer: FIONA 2024 Ackerland / Grünland / Dauerkultur; no admin labels baked in.
- `public/maps/oberschwaben/oberschwaben_moor_context.png` — moor/wetland soil context: BK50 Moor-/Feuchtbodenkontext; no admin labels baked in.
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png` — intersection layer: Schnittmenge: Nutzung × Bodenkontext; no admin labels baked in.

## Optional assets

- `public/maps/oberschwaben/oberschwaben_landuse_classes_on_moor.png` — optional interpretive layer: Schnittmenge nach Ackerland / Grünland / Dauerkultur.
- `public/maps/oberschwaben/oberschwaben_implementation_context_composite.png` — optional composite fallback: Static fallback/composite, not required for scrolly layer-stack.

## Failures

- none

## Warnings

- none

## Layer-stack interpretation

The Oberschwaben module should be implemented as a scrollable layer stack, not as a static publication-style map. The admin context layer should remain visible above the thematic layers. The agriculture, moor-context and intersection layers should be faded in/out by scroll state.

## Recommended state sequence

1. `region` — admin context only
2. `agriculture` — agriculture + admin
3. `moor-context` — agriculture + moor context + admin
4. `intersection` — intersection emphasized + context layers dimmed + admin
5. `method-boundary` — intersection remains visible; method boundary text visible

## Manifest

- `docs/B95h_oberschwaben_layer_stack_manifest.csv`
