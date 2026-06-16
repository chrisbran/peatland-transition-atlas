# Phase A Tasks — Literature-driven MVP

## A1 — Local preview

**Goal:** Confirm that the prototype runs locally.

Steps:
1. Start local server.
2. Open browser.
3. Check metrics, story cards, evidence map, pathway matrix and fit chart.

Acceptance:
- No missing data.
- No browser console errors.
- All core sections render.

## A2 — Story review

**Agent:** Story & Editorial Agent

Files:
- `public/data/atlas_story_sections.json`
- `data/processed/atlas_story_sections.json`
- `docs/atlas_storyboard.md`

Acceptance:
- Each section has one clear main message.
- Claims are cautious.
- The Atlas reads like a coherent story.

## A3 — Evidence region review

**Agent:** Research & Evidence Agent

Files:
- `region_case_studies.geojson`
- `papers.csv`

Acceptance:
- Every region card has a defensible key message.
- Approximate coordinates are not misleading.
- Caveats are explicit.

## A4 — Transition score review

**Agent:** QA & Critic Agent + Human Lead

Files:
- `transition_pathways.csv`

Acceptance:
- Scores are internally consistent.
- Scores are visibly qualitative.
- South Germany fit is framed as hypothesis.

## A5 — Methodology panel

**Agent:** Visualization Engineer Agent

Goal:
Add a visible methodology/uncertainty section to the website.

Acceptance:
- Website states that scores are qualitative codings.
- Evidence-map coordinates are approximate anchors.
- PDFs and confidential data are excluded.
