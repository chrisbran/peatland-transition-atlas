# QA Report — Phase A Initial Local Preview

Date: 2026-06-16

## Scope

Initial QA after local preview of the Phase A literature-driven prototype.

Reviewed components:

- Hero / project introduction
- Metrics panel
- Six-part story cards
- International evidence map
- Evidence region card
- Transition pathway spectrum
- Pathway matrix
- South Germany fit chart
- Current prototype datasets section

## Result

**Status: PASS for Phase A local preview**

The prototype loads and renders the expected core components:

- 21 papers
- 8 transition pathways
- 11 evidence regions
- story sections visible
- evidence map visible
- evidence card visible
- pathway matrix visible
- South Germany fit chart visible
- data links visible

## Observations

### What works well

1. The visual identity is coherent and suitable for a portfolio prototype.
2. The dark, quiet colour palette fits the peatland/climate topic.
3. The story structure is immediately visible.
4. The prototype already communicates that this is a literature-driven MVP.
5. The transition-pathway section is a strong core graphic.
6. The South Germany fit chart makes the transfer question tangible.

### Issues to address before public GitHub release

#### 1. Typography readability

Some text appears quite small in the screenshot, especially:

- metric labels,
- card body text,
- map caveat text,
- pathway details.

**Recommendation:** slightly increase minimum body/card font sizes and line height.

#### 2. Methodology visibility

The prototype mentions qualitative scores in places, but the methodological caution should be more prominent.

Add a visible section or info panel:

```text
Scores are qualitative literature-informed codings, not statistical estimates.
Evidence-map points are approximate visual anchors, not exact field-site coordinates.
```

#### 3. Evidence-map geography

The current map is intentionally abstract. That is acceptable for Phase A, but before public release it should say more clearly:

```text
This is an evidence map, not a spatial distribution map.
```

#### 4. Axis labels in South Germany Fit Chart

The axis labels are visible but could be more explicit.

Suggested labels:

- x-axis: water-table / wetness requirement
- y-axis: compatibility with existing South German dairy/forage systems
- bubble size: qualitative GHG mitigation potential
- colour: adoption / market barrier

#### 5. Transition score explanation

The bars in the pathway matrix are visually clear, but the meaning of 1/2/3 should be visible close to the chart.

Suggested microcopy:

```text
1 = low, 2 = medium, 3 = high; based on literature-informed expert coding.
```

## Acceptance criteria check

| Criterion | Status | Note |
|---|---|---|
| Site loads locally | PASS | Confirmed by screenshot |
| Metrics render | PASS | 21 / 8 / 11 visible |
| Story cards render | PASS | Six cards visible |
| Evidence map renders | PASS | Points and card visible |
| Pathway matrix works | PASS | Selected pathway panel visible |
| Fit chart renders | PASS | Bubbles visible |
| Methodology caveat visible | CONDITIONAL | Present in text but should be stronger |
| No overclaim visible in first screen | PASS | Language is mostly cautious |
| Ready for GitHub Pages | CONDITIONAL PASS | Needs methodology panel and small readability improvements |

## Recommended next task

Proceed to:

```text
A5 — Add visible methodology panel to static prototype
```

Agent:

```text
Visualization Engineer Agent + QA & Critic Agent
```

Acceptance:

- visible method/caveat panel added,
- qualitative score explanation added,
- approximate evidence-map coordinate caveat added,
- small typography refinements implemented,
- local preview still works.
