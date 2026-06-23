# B77 - Target Design Specification

Date: 2026-06-23

## 1. Chosen direction

**B-led hybrid**

Formal name:

**Editorial Natur / fachlich ruhig / kartografisch diszipliniert**

## 2. Design goals

The German presentation version must feel like:

- a data essay,
- a policy-relevant visual explanation,
- a serious project presentation,
- a guided spatial argument.

It must not feel like:

- a raw prototype,
- a GIS dashboard,
- a nature-themed campaign page,
- a decorative portfolio piece.

## 3. Page background

Recommended:

- warm paper base: `#F5EFE6` or slightly lighter `#F7F2EA`
- optional very subtle radial gradients
- gradients must be nearly invisible and never reduce map readability

Avoid:

- full dark background,
- saturated green wash,
- photographic texture backgrounds.

## 4. Core colors

### Primary

- Ink: `#221D18` or `#1A1A1A`
- Muted: `#776A5D` or `#6E6E6E`
- Line: `#DED4C7`
- Accent Petrol: `#1F4E5F`

### Secondary semantic colors

- Ocker: `#C8901A` for policy/instrument accents only
- Salbei: `#7A8B74` for land use / landscape / agriculture
- Rost: `#A65041` for risk/emissions/conflict only
- Neutral grey for context

## 5. Typography

- Font stack: `Inter, Segoe UI, Helvetica Neue, Arial, sans-serif`
- H1: strong, left aligned, statement title
- H2: short, assertive section claims
- Body: restrained, readable
- Captions/sources: small but legible

Text rule:

- titles state the message, not the topic.

Example:

Bad:

`Peatland Transition Atlas`

Good:

`Moorschutz braucht räumliche Orientierung`

## 6. Layout

- max content width around 1120-1240 px
- left-aligned content
- no centered poster layout
- generous spacing between sections
- cards only where they group real alternatives or arguments
- map stage has priority over surrounding UI

## 7. Hero

Hero should communicate the core argument immediately.

Recommended hero:

**Moorschutz braucht räumliche Orientierung**

Lead:

**Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.**

The hero should not mention:

- Atlas
- Prototype
- MVP
- Dashboard
- Portfolio

## 8. Navigation

German, functional, short:

- Problem
- Kartenfolge
- Umsetzung
- Pfade
- Methode

No:

- Story
- Evidence Map
- Appendix
- Data Explorer

## 9. Map section

The map section should use the B layout rhythm but C discipline.

Required:

- clean map frame,
- low visual noise,
- readable source caption,
- no excessive shadow,
- direct map-step labels,
- method caveat for BK50.

Map-step target wording:

1. Wo liegen die Moore?
2. Wo konzentriert sich der Emissionsdruck?
3. Deutschland ist eine Umsetzungsebene.
4. Baden-Württemberg wird konkret.

For full production, the actual 11 central states can retain their existing interaction, but text should be German and shorter.

## 10. Regional implementation section

This is where LUBW and SOLAMO become useful, but they should not dominate the page.

Recommended structure:

- Planungskulisse
- Betriebliche Betroffenheit
- Wertschöpfung

Purpose:

To show that the regional map endpoint leads to implementation questions.

## 11. Transformationspfade

Recommended first-level framing:

- Schützen und stabilisieren
- Wiedervernässen und anpassen
- Nutzung neu organisieren

Avoid claiming suitability or priority unless supported by data.

## 12. Method boundary

Must remain visible, ideally near the end:

**Einordnung statt Eignungskarte**

Key sentence:

**Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.**

## 13. Implementation constraints

When B79 implements this into the production site:

- make a minimal reversible CSS patch,
- avoid deleting existing structures,
- avoid touching raw data,
- avoid large JS rewrites,
- keep central story functionality intact,
- document every visible text replacement.

## 14. Design acceptance criteria

A production page passes if:

1. no visible prototype/meta language remains in the main presentation flow,
2. the page works in German,
3. the visual tone is warm but professional,
4. the central map remains dominant,
5. sources and method boundaries are visible,
6. the page can be explained in 3-5 minutes to scientifically informed practitioners.
