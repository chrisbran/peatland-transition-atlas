# B97b - Lighten Oberschwaben Stage

Date: 2026-06-24

## Result

B97b replaced the dark B97 Oberschwaben visual treatment with a lighter editorial
stage while keeping the larger central-story scale.

## Changed files

- `src/styles.css`
- `docs/B97b_lighten_oberschwaben_stage.md`
- `tasks/done.md`

## Not changed

- `index.html`
- `public/maps/oberschwaben/*.png`
- GIS/raw data
- B96 scroll-state JavaScript

## Reason

The B97 stage size was correct, but the dark/vignetted treatment reduced
readability for the fine-grained Oberschwaben polygons and district labels.
A lighter warm stage is more suitable for this regional, high-detail map.

## Design changes

- Warm editorial section background instead of dark background.
- Light 16:9 map card, preserving the large central-story scale.
- Compact light legend overlay.
- Light glass story cards.
- Higher thematic layer readability and lower dark vignette.

## QA recommendation

Run:

```powershell
python scripts\95h_validate_oberschwaben_layer_stack.py
python scripts\58_visual_qa_and_commit_check.py
```

Then inspect the Oberschwaben section locally in the browser/video.
