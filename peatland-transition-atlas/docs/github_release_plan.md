# GitHub Release Plan — Phase A

## Release name

```text
v0.1.0 — Literature-driven Peatland Transition Atlas MVP
```

## Repository name

```text
peatland-transition-atlas
```

## Short repository description

```text
Interactive literature-driven atlas on peatland rewetting, GHG mitigation and transition-compatible land-use pathways.
```

## Longer public description

The Peatland Transition Atlas is an interactive data-visualisation prototype that translates curated scientific literature on agricultural peatland rewetting into a public-facing evidence atlas. It maps international evidence regions, compares transition-compatible land-use pathways and formulates cautious transfer hypotheses for South German dairy, forage and biogas landscapes.

## Suggested GitHub topics

```text
data-visualization
peatlands
rewetting
paludiculture
climate-mitigation
agriculture
scrollytelling
geojson
scientific-visualization
ai-agents
```

## Deployment

Use GitHub Pages from the repository root:

```text
Settings → Pages → Deploy from a branch → main → /root
```

## Release checklist

Before release:

- [ ] Site runs locally with `python -m http.server 8000`
- [ ] Methodology panel visible
- [ ] Evidence map works
- [ ] Pathway matrix works
- [ ] South Germany fit chart works
- [ ] README is visible and clear
- [ ] No PDFs included
- [ ] No raw large geodata included
- [ ] No confidential PALUD/RoGeR data included
- [ ] Licence and data cautions visible
- [ ] GitHub Pages enabled

## Suggested first GitHub issues after release

1. Add Phase B `country_hotspots.csv` schema.
2. Fetch FAOSTAT drained organic soils country data.
3. Prepare Natural Earth country boundaries.
4. Add hotspot choropleth layer.
5. Improve mobile layout.
6. Replace abstract evidence map with real basemap.
7. Add source citations panel.
8. Add accessibility review.

## Tagging

After the repository is pushed:

```bash
git tag v0.1.0
git push origin v0.1.0
```
