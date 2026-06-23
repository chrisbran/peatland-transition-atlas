#!/usr/bin/env python3
"""
B77 - Design dummy review

Purpose:
- Record the design decision after reviewing B76 dummy variants.
- Select B76_B_editorial_natur as the preferred direction.
- Define safeguards so the final design remains professional, not decorative.
- Prepare the implementation brief for the German presentation version.
- Do not modify the production website.

Outputs:
- docs/B77_design_dummy_review.md
- docs/B77_target_design_spec.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- alter scripts/maps/data
- implement the design
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REVIEW = DOCS / "B77_design_dummy_review.md"
SPEC = DOCS / "B77_target_design_spec.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    review = f"""# B77 - Design Dummy Review

Date: {today}

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
"""

    spec = f"""# B77 - Target Design Specification

Date: {today}

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
"""

    write(REVIEW, review)
    write(SPEC, spec)

    done_entry = f"""
## B77 - Design dummy review ({today})

- Reviewed B76 dummy variants.
- Selected B76_B_editorial_natur as the preferred direction.
- Defined target direction: Editorial Natur + fachliche Ruhe + kartografische Disziplin.
- Created `docs/B77_design_dummy_review.md`.
- Created `docs/B77_target_design_spec.md`.
- Did not modify production website files, maps, scripts, data or CSS.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B77 - Design dummy review" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B77 design dummy review complete.")
    print("Changed/created:")
    print(f"  {rel(REVIEW)}")
    print(f"  {rel(SPEC)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
