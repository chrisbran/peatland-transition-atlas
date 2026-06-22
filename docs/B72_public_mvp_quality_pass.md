# B72 - Public MVP Quality Pass

Date: 2026-06-22

## 1. Purpose

B72 freezes the current page as a reviewable MVP prototype and adds a stricter QA report for the current story architecture.

The MVP structure is:

1. Hero / problem statement.
2. Transition logic.
3. Main atlas story bridge.
4. Central PNG sticky-map story.
5. Interpretation.
6. Supporting evidence.
7. Prototype appendix.

## 2. Created files

- `docs/B72_public_mvp_quality_pass.md`
- `docs/B72_public_mvp_quality_report.md`

## 3. What B72 checks

B72 checks:

- BW PNGs in addition to global, Europe and Germany PNGs,
- all 11 central map states,
- retired legacy sections:
  - `#guidedStory`
  - `#story`
  - `#bwPeatLayer`
- lower evidence grouping:
  - `#interpretationIntro`
  - `#supportingEvidenceGroupIntro`
  - `#prototypeAppendixIntro`
- retired guidedStory scripts are no longer active,
- no broken local references in `index.html`.

## 4. What B72 does not do

B72 does not change application behavior. It does not:

- alter `index.html`,
- alter `src/styles.css`,
- alter central story JS,
- delete or move files,
- remove script tags,
- change map layers.

## 5. Current B72 result

`PASS WITH WARNINGS`

See:

- `docs/B72_public_mvp_quality_report.md`

## 6. Next recommended step

Recommended B73:

`B73_mvp_copy_and_source_polish`

Scope:

- polish hero and section copy,
- check source wording,
- add a clear prototype/disclaimer sentence near the footer,
- no new functionality,
- no additional cleanup.
