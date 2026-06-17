# Task A6 — Simplify Evidence Cards

## Agent

Visualization Engineer Agent

## Reviewer

QA & Critic Agent + Human Lead

## Goal

Improve the selected evidence-region card without overloading the interface with internal QA metadata.

## Design decision

Show only the evidence context that helps the reader interpret the card.

Show:

```text
Evidence type
Key message
Transfer hypothesis for South Germany
Main caveat
Supporting papers
```

Do not prominently show:

```text
transfer_confidence
coordinate_precision
marker_size_hint
marker_category
```

These fields remain useful internally for QA and future filtering, but they should not dominate the public-facing MVP.

## Files to modify

- `src/app.js`
- optionally `src/styles.css`

## Acceptance criteria

- Region cards remain readable.
- `evidence_type` is visible in a simple human-readable form.
- South Germany transfer is clearly framed as a hypothesis.
- Coordinate caution is shown as one short general note, not as a technical metadata field.
- The interface remains story-first, not method-first.
