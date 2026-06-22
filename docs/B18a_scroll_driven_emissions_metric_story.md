# B18a — Scroll-Driven Emissions Metric States

Date: 2026-06-18

## Purpose

Turn the country hotspot metric switch into a guided scroll sequence.

The existing click toggle remains useful for the explorer, but the main story should not depend on the user discovering a button.

## Added section

`#emissionsMetricScrolly`

## Story states

1. Total emissions — absolute national climate pressure.
2. Emission density — intensity relative to mapped drained organic-soil area.
3. Compare — both views are needed for prioritisation.

## Technical approach

- independent SVG renderer using `public/data/hotspot_countries_110m.geojson`
- flexible detection of total-emissions and density fields
- same public data layer, different metric state
- no external libraries
- existing hotspot explorer remains unchanged

## Design principle

The metric shift is no longer a UI option only. It becomes a narrative argument:

> Total emissions and emission density tell different stories.

## Next step

B18b should introduce a unified map-card system for Europe, Germany and Baden-Württemberg, including stronger geographic context and larger map panels.
