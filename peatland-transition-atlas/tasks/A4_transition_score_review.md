# Task A4 — Transition Score Review

## Agent

QA & Critic Agent

## Reviewer

Human Lead

## Goal

Review whether the qualitative scores in `transition_pathways.csv` are internally consistent, scientifically cautious and useful for the MVP.

## Files to review

- `data/processed/transition_pathways.csv`
- `public/data/transition_pathways.json`
- `docs/methodology.md`
- `docs/acceptance_criteria.md`

## Review questions

1. Are the qualitative scores internally consistent across pathways?
2. Are any scores too confident?
3. Is South Germany fit too high or too low for any pathway?
4. Are trade-offs and uncertainties specific enough?
5. Does the visual encoding risk implying false precision?
6. Should any score be replaced by `uncertain` rather than 1/2/3?

## Required output

- `docs/A4_report_transition_score_review.md`
- optional revised `transition_pathways.csv`
- optional revised `transition_pathways.json`

## Acceptance criteria

- Scores are defensible as literature-informed expert codings.
- No pathway is oversold.
- South Germany fit remains a hypothesis.
- Caveats remain visible and specific.
- The chart remains simple enough for portfolio use.
