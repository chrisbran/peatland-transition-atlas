# B69 - Retire Six-Part Story Phase 1

Date: 2026-06-22

## 1. Purpose

B69 reduces the last major redundancy before the central atlas story.

After B68/B68b, the page already has:

- a conceptual frame: `#transitionLogic`,
- a compact main-atlas-story bridge: `#mvpStoryline`,
- the central PNG sticky map story: `#centralGlobalMapStory`.

The old `#story` / "Six-part story" section now duplicates that setup and delays the main atlas story.

## 2. Changed files

- `index.html`
- `docs/B69_retire_six_part_story_phase1.md`
- `tasks/done.md`

## 3. What changed

The opening tag of `#story` was changed from:

```html
<section id="story" class="section" data-story-role="intro-overview">
```

to:

```html
<section id="story" class="section is-retired" data-story-role="retired-intro-overview" hidden aria-hidden="true" data-retired="B69" style="display: none !important;">
```

Navigation links from `#story` to `#transitionLogic` changed:

```text
0
```

## 4. What B69 does not do

B69 does not:

- delete the `#story` section content,
- remove scripts,
- remove data files,
- remove map/image assets,
- alter the central map controller,
- alter BW/BK50 layer handling,
- alter lower evidence modules.

## 5. Rationale

The page should not become more complete at this stage. It should become more understandable.

The visible entry sequence after B69 should be:

1. Hero.
2. Transition logic.
3. Compact main atlas story bridge.
4. Central PNG sticky map story.
5. Supporting evidence / explorer modules.

## 6. Required QA

After B69:

1. Run `python scripts\58_visual_qa_and_commit_check.py`.
2. Open `http://localhost:8000/?v=b69`.
3. Confirm that the old Six-part story is not visible.
4. Confirm that `#transitionLogic` remains visible.
5. Confirm that the central PNG sticky map story still works.
6. Confirm that lower evidence/pathway modules still render.
