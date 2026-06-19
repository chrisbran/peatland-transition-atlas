# B18b5 — Increase GPM2 Context Opacity in Emissions States

Date: 2026-06-18

## Purpose

The transparent ArcGIS layer stack now works well, but the GPM2 peatland context was still too subtle beneath the emissions layers.

## Change

This small CSS override increases GPM2 opacity while preserving the emissions layer as the dominant analytical layer:

| State | Previous GPM2 opacity | New GPM2 opacity |
|---|---:|---:|
| Total emissions | 0.58 | 0.68 |
| Emission density | 0.58 | 0.68 |
| Compare | 0.42 | 0.50 |

## Acceptance check

- GPM2 remains visible beneath total and density layers.
- Emissions remain the dominant visual signal.
- No milky haze returns.
- The map remains stable and aligned.
