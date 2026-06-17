# B6c v3 — Visible Ranking-Map Linking

Date: 2026-06-17

## Problem

The ranking-map linking was technically present but visually too weak.

## Change

This patch makes selected countries explicit by adding:

- stronger active country fill and outline,
- stronger active ranking-row styling,
- a centroid-based marker and label on the map,
- a clearer selected-country details box.

## Status

Visual/interaction refinement only. No data changes.

## Caveat

The marker is centroid-based and approximate. It is a visual selection aid, not a geographic measurement.
