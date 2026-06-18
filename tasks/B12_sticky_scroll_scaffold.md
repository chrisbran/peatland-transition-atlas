# Task B12 — Sticky Scroll Scaffold

## Agent

Visualization Engineer Agent + Story Editor Agent + QA Critic Agent

## Goal

Create the first guided sticky-scroll scaffold without removing the existing explorer sections.

## Proposed structure

1. World country emissions
2. Global peat/organic-soils context
3. Europe wetland/peat context
4. Germany organic-soils bridge
5. Baden-Württemberg BK50-Moor zoom
6. Interpretation boundary

## First technical step

Add a new `#guidedStory` section before the explorer layers:

- left or right sticky visual container,
- 5–6 text steps,
- IntersectionObserver to set active step,
- no complex animations yet.

## Acceptance criteria

- existing explorer sections remain available,
- sticky section is readable on desktop,
- mobile fallback is simple and non-sticky,
- no heavy dependency is introduced.
