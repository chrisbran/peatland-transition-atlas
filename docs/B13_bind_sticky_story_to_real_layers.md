# B13 — Bind Sticky Story to Real Map Layers

Date: 2026-06-18

## Purpose

Connect the sticky-scroll scaffold to available real atlas layers.

## Real layers used

- `public/data/world_countries_110m_base.geojson`
- `public/data/hotspot_countries_110m.geojson`
- `public/data/bw_bk50_moor_simplified.geojson`

## Bound story states

| Scroll state | Layer status |
|---|---|
| World emissions | Real country-level hotspot layer |
| Global peat/organic soils | Placeholder, labelled as planned |
| Europe | Placeholder, labelled as planned |
| Germany | Placeholder, labelled as planned |
| Baden-Württemberg | Real BK50-Moor simplified layer |
| Interpretation boundary | Real caveat panel |

## Design decision

The story now clearly distinguishes available real data from planned future layers. It does not pretend that global, European or Germany peat/organic-soils layers have already been processed.

## Next step

Process the next missing real layer. Recommended order:

1. Germany organic-soils kulisse,
2. European Wetland Map,
3. global peat/organic-soils layer.
