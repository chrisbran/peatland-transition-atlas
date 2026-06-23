# B79 - German Presentation Version

Date: 2026-06-23

## 1. Purpose

B79 applies the first German presentation version to the production page.

Target direction:

**Editorial Natur + fachliche Ruhe + kartografische Disziplin**

## 2. Main changes

- Rewrote the hero into German subject-matter language.
- Replaced top navigation with German presentation path:
  - Problem
  - Kartenfolge
  - Umsetzung
  - Pfade
  - Methode
- Rewrote `#transitionLogic` as the main argument.
- Rewrote visible central map step texts into German.
- Inserted compact German sections:
  - `#b79RegionalImplementation`
  - `#b79Pathways`
  - `#b79MethodBoundary`
- Hid older lower explorer/prototype sections reversibly with `data-retired="B79"`.
- Added B79 CSS overrides to `src/styles.css`.
- Preserved map PNGs, state names and central layer logic.

## 3. Method boundary

The production page now includes this boundary:

> Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B79_german_presentation_version.md`
- `src/central_stage_label_fix.js`

## 5. Reversibility

No deleted sections, scripts, data or assets. Older lower sections were hidden rather than removed.

## 6. Required QA

Run:

```powershell
python scripts\58_visual_qa_and_commit_check.py
python scripts\72_public_mvp_quality_pass.py
```

Manual checks:

1. Page opens locally.
2. Main visible flow is German.
3. Central map sequence still works.
4. BW states still work.
5. Retired B79 sections remain hidden.
6. No visible main-flow `prototype`, `MVP`, `portfolio`, `dashboard`, `appendix`.
7. Method boundary is visible.
