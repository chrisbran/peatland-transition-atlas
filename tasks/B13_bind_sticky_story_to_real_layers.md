# Task B13 — Bind Sticky Story to Real Map Layers

## Agent

Visualization Engineer Agent + Data & GIS Agent + Story Editor Agent

## Goal

Connect the sticky-scroll scaffold to real atlas layers.

## Candidate binding steps

1. World emissions step → reuse country hotspot map state.
2. Global peat/organic-soils step → placeholder until global layer is processed.
3. Europe step → placeholder until European Wetland Map layer is processed.
4. Germany step → placeholder until Germany organic-soils layer is processed.
5. Baden-Württemberg step → reuse `bw_bk50_moor_simplified.geojson`.
6. Boundary step → show caveat panel and layer interpretation.

## Acceptance criteria

- existing explorer sections still work,
- sticky story remains readable,
- no heavy framework is introduced,
- unsupported layers are visibly labelled as planned/future rather than pretending to be complete.
