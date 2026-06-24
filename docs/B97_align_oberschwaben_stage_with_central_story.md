# B97 - Align Oberschwaben Stage With Central Story

Date: 2026-06-24

## Result

B97 replaced the B96 Oberschwaben CSS block with a larger and darker
central-story-aligned visual treatment.

## Changed files

- `src/styles.css`
- `docs/B97_align_oberschwaben_stage_with_central_story.md`
- `tasks/done.md`

## Not changed

- `index.html`
- `public/maps/oberschwaben/*.png`
- GIS/raw data
- B96 scroll-state JavaScript

## Design changes

- Enlarged sticky map stage.
- Changed section background from light figure-like treatment to dark editorial map-stage treatment.
- Moved legend into a compact overlay-style treatment.
- Adapted story cards to a glass/dark style closer to the Global/Europe/Germany/BW map narrative.
- Preserved B96 state sequence and method-boundary language.

## QA recommendation

Run:

```powershell
python scripts\95h_validate_oberschwaben_layer_stack.py
python scripts\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section in the browser/video.
