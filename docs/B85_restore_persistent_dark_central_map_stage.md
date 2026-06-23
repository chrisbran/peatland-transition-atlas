# B85 - Restore Persistent Dark Central Map Stage

Date: 2026-06-23

## 1. Issue

After B84:

- the red `textContent` error was fixed,
- but the dark map/stage background still appeared mainly around step 01,
- the middle of the central story could collapse visually into a grey scroll field with small floating cards.

## 2. Interpretation

The issue is visual/CSS-based, not data-based.

The central map visual needs to remain the persistent anchor throughout the 01-11 story sequence. B85 restores a sticky dark map stage and keeps all step cards above it.

## 3. Changes

B85 appends CSS only.

It:

- gives `#centralGlobalMapStory` a persistent dark gradient field,
- makes likely central map containers sticky again,
- gives map containers a dark stage background,
- keeps central step cards dark and above the map stage,
- avoids changing central map state names or JavaScript logic.

## 4. Files changed

- `src/styles.css`
- `docs/B85_restore_persistent_dark_central_map_stage.md`
- `tasks/done.md`

## 5. Manual QA

Check:

1. The red error bar remains gone.
2. The central map/story section no longer becomes a plain grey field between steps.
3. Steps 01-11 all have dark readable cards.
4. The map frame remains visible as the visual anchor through the central story.
5. Global, Europe, Germany and BW states still switch correctly.
