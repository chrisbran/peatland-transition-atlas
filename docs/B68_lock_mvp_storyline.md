# B68 - Lock MVP Storyline

Date: 2026-06-22

## 1. Purpose

B68 shifts the project from technical cleanup back to product clarity.

The current MVP is not a complete GIS dashboard. It is a narrative research and policy prototype that explains a single argument:

`Extent -> Pressure -> Implementation context -> Transition pathways`

## 2. Core product goal

The Peatland Transition Atlas should show how the peatland transition problem can be read across scales:

1. Global peatland extent.
2. Global pressure / hotspot signals.
3. European context.
4. Germany / Thuenen implementation context.
5. Baden-Wuerttemberg / BK50 regional soil context.
6. Transition pathway interpretation.

## 3. Changed files

- `index.html`
- `src/styles.css`
- `docs/B68_lock_mvp_storyline.md`
- `tasks/done.md`

## 4. What B68 adds

### `#mvpStoryline`

A compact editorial lock before the central sticky map story. It states that the sticky PNG map is the main atlas story.

### `#supportingEvidenceIntro`

A compact separator before the evidence/pathway modules. It states that the lower modules are support layers, not a second main storyline.

### `data-story-role`

B68 adds `data-story-role` attributes to major sections. These are not used for functionality yet; they document the intended role of each section and make later cleanup safer.

## 5. What B68 does not do

B68 does not:

- delete sections,
- hide sections,
- remove scripts,
- remove assets,
- change map states,
- alter the central PNG story controller stack,
- remove the BW interactive layer.

## 6. Next recommended patch

Recommended B69:

`B69_refine_central_story_readability`

Scope:

- tighten central map step wording,
- make each step's role explicit,
- reduce redundant or abstract text,
- leave data, scripts and map assets untouched.

## 7. Visual QA checklist

After B68:

1. The new MVP storyline block appears before the central sticky map story.
2. The central PNG map story still works through all states.
3. The supporting evidence intro appears before pathway/evidence modules.
4. Hotspot, evidence map, pathway, fit, methodology and data sections still render.
5. No legacy guided story is visible.
