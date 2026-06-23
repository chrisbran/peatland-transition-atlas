# B82 - Compact Header and Overflow Fix

Date: 2026-06-23

## 1. Purpose

B82 fixes the issues visible after B81:

- the old top masthead still duplicated the actual hero,
- the top area still showed the substantive title and lead inside the navigation/header area,
- some cards and floating step panels could become too narrow,
- some map-step panels were too close to the viewport edge.

## 2. Main change

The first production header was replaced with a compact German navigation bar:

- `Moorschutz`
- `Problem`
- `Kartenfolge`
- `Umsetzung`
- `Pfade`
- `Methode`

The substantive title remains only in the actual hero section.

## 3. CSS safeguards

B82 appends CSS that:

- hides any `h1`, lead, kicker or old paragraph inside `header.site-header`,
- keeps the header compact and sticky at the top,
- stabilizes hero claim-card widths,
- prevents text overflow in cards and central map steps,
- keeps floating map step panels inside the viewport.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `docs/B82_compact_header_and_overflow_fix.md`
- `tasks/done.md`

## 5. Header replaced

`True`

## 6. Manual QA

Check:

1. No duplicated hero title in the top navigation/header.
2. Header is compact.
3. Hero title appears once.
4. Hero claim cards are readable.
5. Central map step cards are not cropped at the viewport edge.
6. Map sequence still works.
