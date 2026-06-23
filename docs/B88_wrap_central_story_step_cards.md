# B88 - Wrap Central Story Step Cards

Date: 2026-06-23

## 1. Why B88 was needed

After B87, the selector targeting finally reached the central story, but the visible result showed a new problem:

- the map stage responded,
- but whole scrollytelling trigger articles were styled as dark cards,
- this created large dark columns/blocks on the left,
- the actual text cards were not visually separated from the scroll geometry.

## 2. Fix

B88 separates two things:

1. **Trigger geometry**  
   The `article[data-global-state]` element remains available for scroll/state logic but becomes visually transparent.

2. **Visible text card**  
   The contents of each state article are wrapped in:

```html
<div class="b88-step-card">...</div>
```

Only `.b88-step-card` receives the dark card styling.

## 3. Files changed

- `index.html`
- `src/styles.css`
- `docs/B88_wrap_central_story_step_cards.md`
- `tasks/done.md`

## 4. Wrapped state articles

`11`

## 5. Manual QA

Check:

1. Large dark columns/blocks on the left are gone.
2. Steps 01-11 show compact dark cards.
3. Cards remain readable.
4. The map remains visible as the central visual anchor.
5. Scroll/state switching still works.
6. Hero, header and lower German sections remain stable.
