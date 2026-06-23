# B95 - Build Oberschwaben Map Assets

Created from B94 on 2026-06-23

## Goal

Build the first source-anchored Oberschwaben map asset.

Primary output:

```text
public/maps/oberschwaben/oberschwaben_implementation_context_composite.png
```

## Source anchors from B94

Use B94 as source-stack guide:

```text
docs/B94_oberschwaben_source_stack.md
docs/B94_oberschwaben_source_stack.csv
docs/B94_oberschwaben_data_access_questions.md
docs/B94_oberschwaben_legend_and_map_logic.md
```

## Minimum decisions before generating map

- [ ] agriculture source selected,
- [ ] soil/moor context source selected,
- [ ] administrative boundary source selected,
- [ ] public display rights checked,
- [ ] first output selected: visual-only or visual + indicators,
- [ ] legend wording approved.

## Recommended first build

A visual composite map with:

- four district outlines,
- Ackerland / Grünland / Dauerkultur if available,
- Moor-/Feuchtbodenkontext,
- highlighted intersection Nutzung × Bodenkontext,
- compact legend,
- clear method note.

## Do not

- call the map an Eignungskarte,
- call the intersection Wiedervernässungspotenzial,
- imply farm-level affectedness,
- display confidential parcel/farm data,
- add the map to the website before visual and method review.
