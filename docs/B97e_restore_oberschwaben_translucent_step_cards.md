# B97e - Restore Oberschwaben Translucent Step Cards

Date: 2026-06-24

## Result

B97e restored stable semi-transparent Oberschwaben text cards.

## Changed files

- `src/styles.css`
- `docs/B97e_restore_oberschwaben_translucent_step_cards.md`
- `tasks/done.md`

## Action

- inserted B97e override after B97d block

## Visual fix

B97d made card backgrounds too opaque. B97e keeps active/inactive card states
visually stable while using translucent background colors so the map remains
partly visible behind/around the cards.

## Technical note

The override uses `background: rgba(...)` rather than element-level `opacity`,
because element opacity would also fade the card text. Text readability is
therefore retained while the card surface remains translucent.

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
