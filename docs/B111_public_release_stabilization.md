# B111 - Public Release Stabilization

Date: 2026-06-25

Status: **OK**

## Scope

B111 keeps the restored FIONA-based Oberschwaben story. It does not change map data, map paths or map images.

## What changed

- Consolidated the Oberschwaben source note.
- Standardized the interpretation note for the key figures.
- Added an audit for LGL/B105 leftovers and required FIONA/BK50 map references.

## Replacement counts

| Operation | Count |
|---|---:|

## Required public-state checks

| Pattern | Before | After | Expected |
|---|---:|---:|---|
| `~19.900 ha` | 1 | 1 | > 0 |
| `FIONA 2024` | 1 | 1 | > 0 |
| `BK50 Moor-/Feuchtbodenkontext` | 1 | 1 | > 0 |
| `GISCO NUTS 2024` | 1 | 1 | > 0 |
| `oberschwaben_agriculture.png` | 1 | 1 | > 0 |
| `oberschwaben_agriculture_moor_intersection.png` | 1 | 1 | > 0 |

## Forbidden/parked-state checks

| Pattern | Before | After | Expected |
|---|---:|---:|---|
| `Datenquelle in Umstellung` | 0 | 0 | 0 |
| `oberschwaben_lgl` | 0 | 0 | 0 |
| `B98c` | 0 | 0 | 0 |
| `Flächen-QA` | 0 | 0 | 0 |

## Internal note

FIONA remains the active public-story data basis for Oberschwaben in this branch. The LGL replacement work from B106-B109 is parked and should not be mixed into the public page unless deliberately reactivated later.

For project documentation, FIONA usage and publication rights should remain flagged as an item to clarify.
