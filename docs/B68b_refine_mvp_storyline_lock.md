# B68b - Refine MVP Storyline Lock

Date: 2026-06-22

## 1. Purpose

B68 added the correct narrative lock, but the first visual review showed that the block was too heavy.

B68b keeps the editorial intent but makes the intervention smaller:

- the central map is still identified as the main atlas story,
- the storyline chain remains visible,
- the supporting-evidence modules are still framed as support material,
- the page no longer adds another large explanatory block before the map.

## 2. Changed files

- `index.html`
- `src/styles.css`
- `docs/B68b_refine_mvp_storyline_lock.md`
- `tasks/done.md`

## 3. Design decision

The page already has enough explanation before the map. The narrative lock should behave like a bridge, not like a separate chapter.

Therefore B68b changes:

`MVP storyline section` -> `compact main atlas story bridge`

and:

`Supporting evidence section` -> `compact evidence explorer bridge`

## 4. What B68b does not do

B68b does not:

- delete sections,
- hide sections,
- remove scripts,
- remove assets,
- change central map states,
- change the BW/BK50 map layer stack,
- alter the lower evidence modules.

## 5. Next recommended patch

Recommended B69:

`B69_retire_or_merge_six_part_story`

Reason:

After B68b, the largest remaining redundancy is the old `#story` / "Six-part story" section above the transition logic. It should either be retired or merged into the conceptual framing.
