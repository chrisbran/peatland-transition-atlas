# B64 - Cleanup story flow phase 1

Date: 2026-06-22

## Purpose

This patch performs the first reversible story-flow cleanup after the BW/BK50
central story integration.

The central PNG-based sticky-scroll story is now treated as the main narrative
spine of the atlas. Older story components are not deleted, but the duplicate
guided scroll story is retired from display.

## Changes

- Rerouted top Story navigation to #centralGlobalMapStory
- Retired #guidedStory reversibly with is-retired + aria-hidden
- Updated heading: <h2>Where are drained organic soil emissions concentrated?</h2>
- Updated heading: <h2>Evidence from elsewhere</h2>
- Updated heading: <h2>Between drained farming and full restoration</h2>
- Updated heading: <h2>What fits South Germany?</h2>
- Added B64 is-retired CSS utility and scroll-margin for central story

## Deliberate non-changes

- No public data files were deleted.
- No assets were deleted.
- No scripts were removed from `index.html`.
- The central map layer controller was not refactored.
- The B62 BW/BK50 state bindings were not changed.

## Rationale

The page previously contained two separate scroll narratives:

1. `guidedStory`, an older state-based story using `world-emissions`,
   `global-peat`, `europe`, `germany`, `bw` and `boundary`.
2. `centralGlobalMapStory`, the newer PNG-based 11-step map story from global
   peatland extent and emission pressure to Europe, Germany / Thuenen and
   Baden-Wuerttemberg / BK50.

The second component is now stronger and should carry the main story. The first
component is therefore hidden with `is-retired` but left in the markup for easy
rollback.

## QA

Run:

```powershell
python scripts\58_visual_qa_and_commit_check.py
python -m http.server 8000
```

Then inspect:

```text
http://localhost:8000/?v=b64
```

Expected visual result:

- The page should no longer show the old guided story block.
- The main central PNG sticky-scroll story should remain functional.
- Hotspot, evidence, pathway, fit, methodology and data sections should remain
  visible below the main story.
