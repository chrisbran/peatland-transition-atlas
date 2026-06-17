# Task A3 — Evidence Region Review

## Agent

Research & Evidence Agent

## Reviewer

QA & Critic Agent + Human Lead

## Goal

Improve the evidence-region layer so that map cards are scientifically cautious, useful and not geographically misleading.

## Files to review

- `data/processed/region_case_studies.geojson`
- `data/processed/region_case_studies.csv`
- `public/data/region_case_studies.geojson`
- `data/processed/papers.csv`

## Review questions

1. Is every region card's key message supported by the listed papers?
2. Are national/review/policy nodes clearly distinguished from field case studies?
3. Are approximate coordinates sufficiently explained?
4. Are South Germany transfer notes cautious and useful?
5. Are caveats strong enough?
6. Are marker categories useful for filtering?

## Required output

- revised `region_case_studies.geojson`
- revised `region_case_studies.csv`
- `docs/A3_report_evidence_region_review.md`

## Acceptance criteria

- Every region card has one clear key message.
- Every transfer note is phrased as a hypothesis or analogy.
- Conceptual/review/policy nodes are not presented as field evidence.
- Caveats are visible and specific.
- The map remains useful as an evidence map, not a false precision map.
