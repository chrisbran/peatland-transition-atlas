# B80 - Polish German Presentation Layout

Date: 2026-06-23

## 1. Purpose

B80 refines the B79 German presentation version after video review.

The B79 direction works: the page now reads as a German, editorial-nature presentation rather than a technical prototype. B80 keeps that direction and only polishes layout behaviour.

## 2. Observed issues

The video review showed:

1. The German content direction works.
2. The warm editorial design works better than the earlier dark prototype.
3. The navigation/brand behaviour can appear like a bottom overlay in the scroll recording.
4. Central map text panels are readable but still show some ghosted/grey overlay behaviour from older sticky-story styling.
5. The map section needs stronger source-aware polish without changing map logic.

## 3. B80 changes

B80 only appends CSS overrides.

It:

- keeps navigation top-oriented and calm,
- improves hero claim-card spacing,
- makes central map step panels more opaque and readable,
- suppresses old pseudo-element overlay artefacts,
- keeps dark map PNGs but frames them deliberately on the warm page,
- quiets source/caption typography,
- improves transition into the German lower sections.

## 4. Files changed

- `src/styles.css`
- `docs/B80_polish_german_presentation_layout.md`
- `tasks/done.md`

## 5. Files not changed

- `index.html`
- JavaScript
- map PNGs
- data
- central map state names

## 6. QA

After B80, check visually:

1. Header/navigation stays at top and no longer distracts at bottom.
2. Hero still resembles the preferred B76_B direction.
3. Central map story still scrolls correctly.
4. Step panels are readable and not washed out.
5. Map remains dominant.
6. German lower sections still appear after the map.
