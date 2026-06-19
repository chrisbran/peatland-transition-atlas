# B18c — Clean Central Global Story Stage

Date: 2026-06-18

## Purpose

The central global map story is now visually and technically stable. This cleanup pass reduces redundancy and makes the map itself the main visual object.

## Changes

- Reduces the in-map titlebar to a compact mode label.
- Hides the repeated in-map title because the scroll card already carries the narrative statement.
- Makes scroll text cards slightly more compact.
- Keeps the scroll card as the main explanatory layer.
- Keeps legend and source visible but subordinate.

## Rationale

The previous state had two narrative text layers saying similar things:

1. the large scroll card;
2. the in-map titlebar.

This made the map feel more crowded than necessary. The new logic is:

- scroll card = narrative argument;
- in-map titlebar = current mode only;
- map = primary visual evidence.

## Acceptance check

- The central map feels calmer.
- There is less duplicate text.
- The card does not visually compete with the map.
- Total and density transitions remain unchanged.
