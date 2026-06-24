# B97d - Stabilize Oberschwaben Step Card Opacity

Date: 2026-06-24

## Result

B97d added a small CSS override to keep Oberschwaben story-card transparency
stable during scrolling.

## Changed files

- `src/styles.css`
- `docs/B97d_stabilize_oberschwaben_step_card_opacity.md`
- `tasks/done.md`

## Action

- inserted B97d override after B97c block

## Visual fix

The active scroll step still controls the visible Oberschwaben map layer state,
but it no longer changes the transparency/background of the text cards.

## Not changed

- `index.html`
- B96 JavaScript
- PNG layer assets
- GIS/raw data

## QA recommendation

Run:

```powershell
python scripts\95h_validate_oberschwaben_layer_stack.py
python scripts\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section locally.
