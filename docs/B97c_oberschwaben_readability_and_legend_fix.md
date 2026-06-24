# B97c - Oberschwaben Readability and Legend Fix

Date: 2026-06-24

## Result

B97c added a small CSS override block to improve the B97b Oberschwaben section.

## Changed files

- `src/styles.css`
- `docs/B97c_oberschwaben_readability_and_legend_fix.md`
- `tasks/done.md`

## Action

- inserted B97c override after Oberschwaben CSS block

## Visual fixes

- Scroll text cards receive explicit z-index so they do not disappear behind the large sticky map stage.
- Desktop grid spacing is widened slightly to give the text column more breathing room.
- Legend is moved below the map stage rather than overlaid on top of map details.
- Legend background, border, blur and shadow are removed.
- B96 layer-state logic remains unchanged.

## QA recommendation

Run:

```powershell
python scripts\95h_validate_oberschwaben_layer_stack.py
python scripts\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section locally.
