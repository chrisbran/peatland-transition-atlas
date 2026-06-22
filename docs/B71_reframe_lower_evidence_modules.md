# B71 - Reframe Lower Evidence Modules

Date: 2026-06-22

## 1. Purpose

B71 makes the lower half of the page behave like an evidence explorer and prototype appendix rather than a second main storyline.

The central PNG sticky map story remains the main narrative.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B71_reframe_lower_evidence_modules.md`
- `tasks/done.md`

## 3. New lower-page grouping

B71 adds three compact group separators:

1. `#interpretationIntro` before `#pathwayEvidenceMatrix`
2. `#supportingEvidenceGroupIntro` before `#hotspots`
3. `#prototypeAppendixIntro` before `#methodology`

## 4. Lower module tiers

- Interpretation:
  - `#pathwayEvidenceMatrix`
  - `#pathways`

- Supporting evidence:
  - `#hotspots`
  - `#map`
  - `#fit`

- Prototype appendix:
  - `#methodology`
  - `#data`

## 5. BW interactive layer decision

B71 reversibly retires `#bwPeatLayer` from the visible page flow.

Reason:

- The central BW/BK50 PNG story now carries the regional endpoint.
- The old BW GeoJSON layer is useful as an experimental prototype, but it weakens the current MVP narrative when shown as a full visible section.
- No files are deleted.

BW layer retired:

```text
True
```

Old opening tag:

```html
<section id="bwPeatLayer" class="section bw-moor-section" data-story-role="experimental-regional-layer" data-evidence-tier="retired-experimental-layer">
```

New opening tag:

```html
<section id="bwPeatLayer" class="section bw-moor-section is-retired" data-story-role="retired-experimental-regional-layer" data-evidence-tier="retired-experimental-layer" hidden aria-hidden="true" data-retired="B71" style="display: none !important;">
```

## 6. What B71 does not do

B71 does not:

- delete `#bwPeatLayer`,
- delete `src/bw_peat_layer.js`,
- remove the `src/bw_peat_layer.js` script tag,
- delete `public/data/bw_bk50_moor_simplified.geojson`,
- alter central map states,
- alter central map PNG assets,
- remove lower evidence modules.

## 7. Next recommended patch

Recommended B72:

`B72_public_mvp_quality_pass`

Scope:

- check the public GitHub Pages version,
- update QA to include BW PNGs and B69/B71 retired sections,
- optionally add a small "prototype status" note near the footer.
