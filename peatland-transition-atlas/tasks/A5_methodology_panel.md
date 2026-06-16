# Task A5 — Add Methodology Panel to Static Prototype

## Agent

Visualization Engineer Agent

## Reviewer

QA & Critic Agent + Human Lead

## Goal

Make the scientific limitations and data interpretation rules visible inside the web prototype.

## Files to modify

- `index.html`
- `src/styles.css`
- optionally `src/app.js`

## Required visible content

Add a methodology/uncertainty section containing:

```text
This prototype is based on curated literature coding.
Scores are qualitative literature-informed expert codings, not statistical estimates.
Evidence-map points are approximate visual anchors, not exact field-site coordinates.
South Germany fit is a transfer hypothesis, not a validated regional model result.
```

## Additional improvements

- Increase small body text readability slightly.
- Add score legend near the pathway matrix.
- Add clearer axis explanation near the South Germany Fit Chart.

## Acceptance criteria

- Methodology panel is visible on the page.
- Qualitative score scale is explained.
- Evidence-map coordinates are described as approximate anchors.
- South Germany fit is framed as a hypothesis.
- No new external dependency is added.
- Site still runs with `python -m http.server 8000`.

## Suggested implementation

Add a section between `South Germany Fit` and `Current prototype datasets`:

```html
<section id="methodology" class="section methodology-panel">
  ...
</section>
```

Add navigation link:

```html
<a href="#methodology">Method</a>
```
