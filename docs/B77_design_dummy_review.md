# B77 - Design Dummy Review

Date: 2026-06-23

## 1. Reviewed variants

B76 created three static design dummies:

- `design_dummies/B76_A_fachlich_hell.html`
- `design_dummies/B76_B_editorial_natur.html`
- `design_dummies/B76_C_kartografisch_analytisch.html`

## 2. User preference

Preferred direction:

**B76_B_editorial_natur**

Reason:

Variant B has the strongest narrative quality. It feels less like a technical prototype and more like a guided data essay. The warmer tone, card treatment and section rhythm make the topic more accessible without abandoning seriousness.

## 3. Decision

The German presentation version should use **B as the visual base**, but not adopt B uncritically.

Target direction:

**Editorial Natur + fachliche Ruhe + kartografische Disziplin**

In other words:

- B provides warmth and narrative rhythm.
- A provides institutional calm and presentation robustness.
- C provides map, label and source discipline.

## 4. Why B works

Variant B works best because:

1. It supports the desired tone: narrativ vermittelnd.
2. It makes the page less dashboard-like.
3. It gives sections clearer breathing room.
4. It gives the hero and cards more presence.
5. It feels closer to a data essay than to a technical atlas prototype.
6. It can carry SOLAMO/LUBW context better than the colder analytical version.

## 5. Risks of B

Variant B has risks that must be controlled:

1. Too much warmth can become decorative.
2. Too many cards can weaken the hierarchy.
3. Heavy shadows can look less scientific.
4. Atmospheric gradients can compete with maps.
5. Ocker/brown accents must not replace semantic color discipline.
6. The design must not drift toward NGO campaign aesthetics.

## 6. Required corrections before production

The final German version should keep B's warmth, but apply these corrections:

### Typography

- Keep strong, left-aligned headlines.
- Slightly reduce extreme headline density if readability suffers.
- Keep Inter / Segoe UI / Helvetica / Arial.
- No serif font in v0.1.

### Color

- Warm paper background can stay.
- Petrol remains the primary accent.
- Ocker is allowed for section kickers, but should be restrained.
- Rost only for risk/emissions/conflict.
- Salbei only for land use / landscape / agriculture.
- No decorative color use.

### Cards

- Cards may stay, because they improve readability.
- Card borders should remain subtle.
- Shadows should be reduced or used only around the central map.
- Not every piece of information needs a card.

### Map stage

- The map should remain the visual anchor.
- The map frame needs clean source treatment.
- Map captions should be quieter and more systematic.
- The step list should be readable, not decorative.
- C-style source and label discipline should be imported.

### Spacing

- B's generous spacing is good.
- However, the vertical length should not become excessive.
- Section rhythm should support a 3-5 minute presentation walkthrough.

## 7. Final target

The production design should not be called B internally. It should be named:

**German presentation version v0.1**

Working visual description:

> Warm, editorial data essay; guided, precise, and source-aware.

## 8. Next step

B78 should not yet implement the full site. The next useful step is a production implementation plan:

`B78_german_presentation_implementation_plan`

Scope:

- list production files to change,
- define text replacements,
- define CSS direction,
- define what remains hidden,
- define what is deferred,
- prepare a safe patch strategy.

After B78, implementation can happen in B79.
