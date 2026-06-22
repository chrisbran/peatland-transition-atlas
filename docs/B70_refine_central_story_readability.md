# B70 - Refine Central Story Readability

Date: 2026-06-22

## 1. Purpose

B70 improves the readability of the central PNG sticky-map story.

The goal is not to add more information. The goal is to make each step easier to read and easier to understand.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B70_refine_central_story_readability.md`
- `tasks/done.md`

## 3. Updated central story states

- `extent`
- `total`
- `density`
- `compare`
- `europe-borders`
- `europe-peat`
- `germany-context`
- `germany-thuenen-extent`
- `germany-thuenen-types`
- `bw-context`
- `bw-bk50-extent`

## 4. Readability rule

Each step should answer one simple question:

1. What scale are we at?
2. What layer or signal is being added?
3. Why does it matter for peatland transition?

## 5. What B70 does not change

B70 does not:

- change `data-global-state` values,
- change central JS state metadata,
- change layer opacity logic,
- change PNG assets,
- remove scripts,
- remove sections,
- remove data files.

## 6. Next recommended patch

Recommended B71:

`B71_refine_central_story_meta_panel`

Scope:

- only if needed after visual review,
- align the central map panel titles/sources with the clearer step wording,
- do not change state names or layer bindings.

## 7. Visual QA checklist

After B70:

1. The central story step texts are shorter and more functional.
2. The map sequence still moves through all 11 states.
3. No central map layer disappears unexpectedly.
4. Lower evidence modules still render.
5. No legacy guided story or six-part story is visible.
