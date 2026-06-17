# B7 — Phase B Release QA Checklist

## Before creating release v0.2.0

### Data

- [ ] `public/data/country_hotspots.csv` opens on GitHub Pages.
- [ ] `public/data/hotspot_countries_110m.geojson` opens on GitHub Pages.
- [ ] No raw data under `data/external/` are committed.
- [ ] Boundary join report is committed.
- [ ] Method notes B2b–B6c are committed.

### Interface

- [ ] Hotspot section loads after hard refresh.
- [ ] Total emissions map loads.
- [ ] Emissions density toggle works.
- [ ] Legend changes when the toggle changes.
- [ ] Ranking cards load.
- [ ] Ranking/map highlighting works.
- [ ] Caveat text is visible.

### Public interpretation

- [ ] README states that the layer is country-level only.
- [ ] Release notes state that the map is not local rewetting suitability.
- [ ] Known limitations are documented.

### GitHub

- [ ] All changes committed and pushed.
- [ ] GitHub Pages updated.
- [ ] Tag/release created as `v0.2.0`.
