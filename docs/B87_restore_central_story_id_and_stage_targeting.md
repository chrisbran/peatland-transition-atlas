# B87 - Restore Central Story ID and Stage Targeting

Date: 2026-06-23

## 1. Why B87 was needed

B86 reported that `#centralGlobalMapStory` was not found in `index.html`. That explains why B83-B85 selectors targeting `#centralGlobalMapStory` did not visibly affect the central story.

## 2. What B87 did

B87 located the actual central story section using fallback signals:

- `central-map-sticky`
- `central-map-shell`
- `central-map-layer-stack`
- `central-map-layer`
- `central-map-step`
- `data-global-state`
- BW map-layer references

Then it restored:

- `id="centralGlobalMapStory"`
- `class="central-map-story"` if missing
- `data-b87-central-story="true"`

It also appended CSS that targets all three:

- `#centralGlobalMapStory`
- `.central-map-story`
- `[data-b87-central-story="true"]`

## 3. Detection

Original had canonical id:

`False`

Detection reason:

`direct section selector`

Opening tag before:

```html
<section id="centralGlobalMapProblem" class="central-map-story" data-state="extent" data-story-role="main-atlas-story">
```

Opening tag after:

```html
<section id="centralGlobalMapStory" class="central-map-story" data-state="extent" data-story-role="main-atlas-story" data-b87-central-story="true">
```

## 4. Files changed

- `index.html`
- `src/styles.css`
- `docs/B87_restore_central_story_id_and_stage_targeting.md`
- `tasks/done.md`

## 5. Manual QA

Check:

1. The central story is still visible.
2. Steps 01-11 use dark panels.
3. The map stage remains visually present through the central scroll sequence.
4. Global, Europe, Germany and BW/BK50 states still switch.
5. Header and hero remain stable.
