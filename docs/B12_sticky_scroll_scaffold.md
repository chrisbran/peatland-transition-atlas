# B12 — Sticky Scroll Scaffold

Date: 2026-06-18

## Purpose

Create the first guided scrollytelling section without removing the existing explorer sections.

## What this adds

- `#guidedStory` section,
- sticky visual container,
- six narrative scroll steps,
- IntersectionObserver-based active-step handling,
- abstract visual states for world emissions, peat/organic-soil context, Europe, Germany, Baden-Württemberg and interpretation boundary.

## Design decision

This is a scaffold, not the final animated atlas. The existing explorer sections remain intact.

## Why scaffold first?

The project now has several functioning components:

- country hotspot map,
- regional Baden-Württemberg BK50-Moor layer,
- evidence/pathway sections.

The sticky-scroll section provides the narrative spine that can later bind those components into a guided story.

## Next step

B13 should replace the abstract visual states with real map layer states where feasible.
