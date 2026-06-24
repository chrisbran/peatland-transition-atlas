# B96 - Bind Oberschwaben Scrolly Layer Stack

Date: 2026-06-24

## Result

B96 inserted a scrollable Oberschwaben layer-stack module into the German presentation page.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B96_bind_oberschwaben_scrolly_layer_stack.md`
- `tasks/done.md`

## Assets used

- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

## Actions

- inserted B96 HTML before </main>
- inserted B96 JS before </body>
- appended B96 CSS block in `src/styles.css`

## Story states

1. `region` — Landkreisrahmen and labels only.
2. `agriculture` — agricultural use layer fades in.
3. `moor-context` — BK50 Moor-/Feuchtbodenkontext fades in.
4. `intersection` — intersection layer is emphasized while context layers are dimmed.
5. `method-boundary` — intersection remains visible and the method boundary is explicit.

## Method boundary

The section states that the map is a spatial contextualisation only and not a suitability map,
priority map or farm-level affectedness analysis.

## QA recommendation

Run:

```powershell
python scripts\95h_validate_oberschwaben_layer_stack.py
python scripts\58_visual_qa_and_commit_check.py
```

Then inspect the page locally and check the deployed GitHub Pages version after push.
