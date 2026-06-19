# B18b6 — Simplify Compare State

Date: 2026-06-18

## Problem

The central global map appeared to show an additional map layer after the total-emissions and emission-density states. This was not an export error. It came from the compare state, where total and density overlays were intentionally shown together.

## Decision

The mixed overlay is visually confusing. The compare state should not introduce a fourth visual map state.

## Fix

The compare state now keeps the density view visible and uses the text to explain the metric comparison:

- total emissions = absolute national climate relevance;
- emission density = intensity relative to mapped drained organic-soil area.

## Acceptance check

During scroll, the sequence should read as:

1. peatland extent;
2. total emissions;
3. emission density;
4. interpretation text without a new mixed map layer.

There should be no apparent extra hotspot layer after density.
