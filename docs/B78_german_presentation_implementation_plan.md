# B78 - German Presentation Implementation Plan

Date: 2026-06-23

## 1. Purpose

B78 defines the implementation plan for the first German presentation version. It does not implement the website.

## 2. Strategic decision

The first German presentation version should be:

**Editorial Natur + fachliche Ruhe + kartografische Disziplin**

This means:

- B76_B_editorial_natur is the preferred visual base.
- A-style calm and presentation robustness must be preserved.
- C-style map/source/label discipline must be imported.
- The final page must feel like a warm but serious data essay.

## 3. Target audience and tone

Target group: **wissenschaftlich informierte Praxisakteure**  
Tone: **narrativ vermittelnd**  
Scope: **kurz und pointiert**

The page should be understandable in a 3-5 minute project walkthrough.

## 4. Core communication goal

The page must not explain the Atlas as a product.

It must explain the subject:

**Moorschutz wird erst dann umsetzbar, wenn globale Klimarelevanz, nationale Planungskulissen, regionale Bodenkontexte und betriebliche Nutzungsperspektiven zusammen betrachtet werden.**

## 5. Production files likely to change in B79

B79 should likely change only:

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B79_german_presentation_version.md`
- `scripts/79_apply_german_presentation_version.py`

Possible but not preferred:

- `src/central_stage_label_fix.js` if stage labels need German replacement
- `src/central_step_state_bridge.js` only if metadata labels are visible and need German text

Files that should not be touched:

- map PNGs
- raw data
- GeoJSON
- central layer visibility logic
- central map state controller logic
- retired old scripts
- old data workflows

## 6. Sections in the German presentation version

The visible main flow should become:

1. Problem
2. Kernargument
3. Kartenfolge
4. Regionale Umsetzung
5. Transformationspfade
6. Methodische Grenze

| Target section | Existing source | Action |
|---|---|---|
| Problem | Hero | Rewrite in German and restyle |
| Kernargument | transitionLogic or existing bridge | Keep/rewrite; reduce meta-language |
| Kartenfolge | centralGlobalMapStory | Keep functionality; rewrite visible text |
| Regionale Umsetzung | new compact section or existing lower intro | Add/convert; use LUBW/SOLAMO framing |
| Transformationspfade | pathways/pathway evidence area | Keep only compact first-level logic |
| Methodische Grenze | methodology/data/prototype appendix area | Keep as boundary, reduce prototype language |

## 7. Text replacement plan

The detailed copy target list is stored in:

- `docs/B78_german_presentation_copy_targets.csv`

High-level replacements:

- `Peatland Transition Atlas` -> `Moorschutz braucht räumliche Orientierung`
- `Portfolio prototype` / `MVP` -> remove
- `Story` -> `Kartenfolge` or `Problem`
- `Evidence Map` -> remove or `Einordnung`
- `Pathways` -> `Pfade`
- `South Germany Fit` -> remove or `Regionale Umsetzung`
- `Method` -> `Methode`
- `Data` -> avoid in main nav; if needed only in source/method area
- `Atlas framing` -> `Kernargument`
- `From peatland extent to transition priorities` -> `Aus Moorbodenkontext wird eine Umsetzungsfrage`
- `Main atlas story` -> `Kartenfolge`
- `Supporting evidence` -> `Einordnung und Vergleich`
- `Prototype appendix` -> `Methodische Grenze`

## 8. CSS implementation direction

The B79 CSS patch should not copy the B76 dummy blindly. It should apply the B-led visual direction to the current production structure.

Recommended CSS changes:

- page background: warm paper `#F5EFE6` or `#F7F2EA`
- text ink: `#221D18`
- muted text: `#776A5D`
- lines: `#DED4C7`
- primary accent: `#1F4E5F`
- strong left-aligned German hero
- subtle warm cards only for grouped arguments
- preserve existing sticky map functionality
- clean source-aware map frame
- German short navigation
- visible method boundary

## 9. Required method boundary text

This sentence must appear in the production version:

**Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.**

This protects the page from overstating BK50/Thünen/BW layer meaning.

## 10. SOLAMO/LUBW integration rule

SOLAMO-BW and LUBW should appear as contextual anchors, not as project promotion.

Use them to support:

- planning frame,
- farm affectedness,
- use concepts,
- value chains,
- policy instruments.

Do not overclaim SOLAMO results if results are not yet available.

## 11. Reversibility

B79 should be generated as a patch script and should:

- create documentation,
- update `tasks/done.md`,
- avoid deleting existing sections,
- prefer text replacement and CSS override,
- preserve retired sections as retired,
- make no raw-data changes.

Use comments such as:

- `<!-- B79 German presentation version -->`
- `/* B79 German presentation design */`

## 12. QA after B79

After B79 implementation, run:

```powershell
python scripts/58_visual_qa_and_commit_check.py
python scripts/72_public_mvp_quality_pass.py
```

Then manually check:

1. no visible `prototype`, `MVP`, `portfolio`, `dashboard`, `appendix` in main flow,
2. page is German in the main visible presentation path,
3. central map still works,
4. BW states still work,
5. retired sections remain hidden,
6. method boundary is visible,
7. public page matches local after cache-busted URL.

## 13. Commit strategy for B79

Expected staged files for implementation:

```text
index.html
src/styles.css
docs/B79_german_presentation_version.md
scripts/79_apply_german_presentation_version.py
tasks/done.md
docs/B58_visual_qa_and_commit_check.md
docs/B72_public_mvp_quality_report.md
```

If central stage label JS is touched, stage it explicitly and document why.

Do not stage:

- `data/`
- old scripts
- old tasks
- raw GIS files
- unrelated README files

## 14. Acceptance criteria

The German presentation version is acceptable when:

1. the main page no longer looks like a technical prototype,
2. the visible main flow is German,
3. the hero states the substantive problem,
4. the map sequence remains the central argument,
5. LUBW/SOLAMO context supports regional implementation,
6. the design feels warm but professional,
7. method boundaries are explicit,
8. a project audience can follow the page in 3-5 minutes.
