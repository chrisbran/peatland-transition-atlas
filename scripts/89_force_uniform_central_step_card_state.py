#!/usr/bin/env python3
"""
B89 - Force uniform central step card state

Purpose:
- The central map now works, but step cards 02-11 appear grey/inactive
  until they cross a certain viewport threshold, while step 01 is dark from
  the moment it appears.
- Cause: old scrollytelling CSS/JS still applies active/inactive opacity,
  filter, blend or background transitions to the step trigger/article.
- Fix: make all visible .b88-step-card panels use the same dark style
  independent of active/inactive state, and reset opacity/filter on the
  scroll trigger article.
- Do not change map state names, JavaScript logic, maps or data.

Outputs:
- docs/B89_force_uniform_central_step_card_state.md
- modifies src/styles.css
- updates tasks/done.md
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOC = DOCS / "B89_force_uniform_central_step_card_state.md"


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

    css = read(CSS)

    b89_css = r"""
/* B89 force uniform central step card state */

/*
  Old scrollytelling rules still distinguish active/inactive steps using opacity,
  filters, blend modes or alternate backgrounds. That is why step 01 appears dark
  immediately while later steps look grey until they reach an activation threshold.

  For the German presentation version the step card should not change material
  while scrolling. State changes happen in the map, not in the card surface.
*/

/* Scroll trigger/article: keep geometry, remove visual active/inactive treatment. */
#centralGlobalMapStory article[data-global-state],
.central-map-story article[data-global-state],
[data-b87-central-story="true"] article[data-global-state],
#centralGlobalMapStory .central-map-step[data-global-state],
.central-map-story .central-map-step[data-global-state],
[data-b87-central-story="true"] .central-map-step[data-global-state] {
  opacity: 1 !important;
  filter: none !important;
  mix-blend-mode: normal !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  transition-property: transform !important;
}

/* Override common active/inactive/current/past/future classes on trigger level. */
#centralGlobalMapStory article[data-global-state].is-active,
#centralGlobalMapStory article[data-global-state].active,
#centralGlobalMapStory article[data-global-state].is-current,
#centralGlobalMapStory article[data-global-state].current,
#centralGlobalMapStory article[data-global-state].is-inactive,
#centralGlobalMapStory article[data-global-state].inactive,
#centralGlobalMapStory article[data-global-state].past,
#centralGlobalMapStory article[data-global-state].future,
.central-map-story article[data-global-state].is-active,
.central-map-story article[data-global-state].active,
.central-map-story article[data-global-state].is-current,
.central-map-story article[data-global-state].current,
.central-map-story article[data-global-state].is-inactive,
.central-map-story article[data-global-state].inactive,
.central-map-story article[data-global-state].past,
.central-map-story article[data-global-state].future,
[data-b87-central-story="true"] article[data-global-state].is-active,
[data-b87-central-story="true"] article[data-global-state].active,
[data-b87-central-story="true"] article[data-global-state].is-current,
[data-b87-central-story="true"] article[data-global-state].current,
[data-b87-central-story="true"] article[data-global-state].is-inactive,
[data-b87-central-story="true"] article[data-global-state].inactive,
[data-b87-central-story="true"] article[data-global-state].past,
[data-b87-central-story="true"] article[data-global-state].future {
  opacity: 1 !important;
  filter: none !important;
  mix-blend-mode: normal !important;
  background: transparent !important;
}

/* Actual card: one material for all steps, independent of active state. */
#centralGlobalMapStory .b88-step-card,
.central-map-story .b88-step-card,
[data-b87-central-story="true"] .b88-step-card {
  opacity: 1 !important;
  filter: none !important;
  mix-blend-mode: normal !important;
  background: rgba(9, 18, 15, 0.90) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.17) !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.30) !important;
  transition-property: transform, box-shadow !important;
}

/* Same material even when old scripts add active/inactive classes to the card itself. */
#centralGlobalMapStory .b88-step-card.is-active,
#centralGlobalMapStory .b88-step-card.active,
#centralGlobalMapStory .b88-step-card.is-current,
#centralGlobalMapStory .b88-step-card.current,
#centralGlobalMapStory .b88-step-card.is-inactive,
#centralGlobalMapStory .b88-step-card.inactive,
#centralGlobalMapStory .b88-step-card.past,
#centralGlobalMapStory .b88-step-card.future,
.central-map-story .b88-step-card.is-active,
.central-map-story .b88-step-card.active,
.central-map-story .b88-step-card.is-current,
.central-map-story .b88-step-card.current,
.central-map-story .b88-step-card.is-inactive,
.central-map-story .b88-step-card.inactive,
.central-map-story .b88-step-card.past,
.central-map-story .b88-step-card.future,
[data-b87-central-story="true"] .b88-step-card.is-active,
[data-b87-central-story="true"] .b88-step-card.active,
[data-b87-central-story="true"] .b88-step-card.is-current,
[data-b87-central-story="true"] .b88-step-card.current,
[data-b87-central-story="true"] .b88-step-card.is-inactive,
[data-b87-central-story="true"] .b88-step-card.inactive,
[data-b87-central-story="true"] .b88-step-card.past,
[data-b87-central-story="true"] .b88-step-card.future {
  opacity: 1 !important;
  filter: none !important;
  mix-blend-mode: normal !important;
  background: rgba(9, 18, 15, 0.90) !important;
  color: #F5F0E7 !important;
  border-color: rgba(245, 240, 231, 0.17) !important;
}

/* Text should not fade or grey out by state. */
#centralGlobalMapStory .b88-step-card *,
.central-map-story .b88-step-card *,
[data-b87-central-story="true"] .b88-step-card * {
  opacity: 1 !important;
  filter: none !important;
  mix-blend-mode: normal !important;
}

#centralGlobalMapStory .b88-step-card h3,
.central-map-story .b88-step-card h3,
[data-b87-central-story="true"] .b88-step-card h3 {
  color: #F5F0E7 !important;
}

#centralGlobalMapStory .b88-step-card p,
.central-map-story .b88-step-card p,
[data-b87-central-story="true"] .b88-step-card p {
  color: rgba(245, 240, 231, 0.80) !important;
}

#centralGlobalMapStory .b88-step-card span,
.central-map-story .b88-step-card span,
[data-b87-central-story="true"] .b88-step-card span {
  color: #55A3B5 !important;
}

/* If legacy CSS uses aria-current or data-active attributes, neutralise material changes there as well. */
#centralGlobalMapStory article[data-global-state][aria-current],
#centralGlobalMapStory article[data-global-state][data-active],
#centralGlobalMapStory article[data-global-state][data-current],
.central-map-story article[data-global-state][aria-current],
.central-map-story article[data-global-state][data-active],
.central-map-story article[data-global-state][data-current],
[data-b87-central-story="true"] article[data-global-state][aria-current],
[data-b87-central-story="true"] article[data-global-state][data-active],
[data-b87-central-story="true"] article[data-global-state][data-current] {
  opacity: 1 !important;
  filter: none !important;
  background: transparent !important;
}

#centralGlobalMapStory article[data-global-state][aria-current] .b88-step-card,
#centralGlobalMapStory article[data-global-state][data-active] .b88-step-card,
#centralGlobalMapStory article[data-global-state][data-current] .b88-step-card,
.central-map-story article[data-global-state][aria-current] .b88-step-card,
.central-map-story article[data-global-state][data-active] .b88-step-card,
.central-map-story article[data-global-state][data-current] .b88-step-card,
[data-b87-central-story="true"] article[data-global-state][aria-current] .b88-step-card,
[data-b87-central-story="true"] article[data-global-state][data-active] .b88-step-card,
[data-b87-central-story="true"] article[data-global-state][data-current] .b88-step-card {
  background: rgba(9, 18, 15, 0.90) !important;
  opacity: 1 !important;
  filter: none !important;
}
/* End B89 force uniform central step card state */
"""

    if "/* B89 force uniform central step card state */" not in css:
        css = css.rstrip() + "\n\n" + b89_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B89 - Force Uniform Central Step Card State

Date: {today}

## 1. Issue

After B88, the central story structure improved, but step-card appearance still changed during scroll:

- Step 01 was dark immediately when visible.
- Steps 02-11 first appeared grey or inactive.
- They became dark only after crossing a viewport activation threshold.

## 2. Cause

This is caused by old scrollytelling active/inactive styling.

The scroll logic likely adds classes or attributes such as:

- `active`
- `is-active`
- `current`
- `is-current`
- `inactive`
- `past`
- `future`
- `aria-current`
- `data-active`

or applies opacity/filter changes to the scroll-trigger article.

That behaviour is useful if cards are meant to fade in, but here it causes inconsistent card materials.

## 3. Design decision

For the German presentation version:

**The map changes state; the text card material should not.**

All visible step cards should use the same dark material from the moment they enter the viewport.

## 4. Changes

B89 appends CSS only.

It:

- resets opacity/filter/blend/background on central `article[data-global-state]` triggers,
- forces `.b88-step-card` to remain dark regardless of active/inactive class or attribute,
- prevents text from fading/greying by state,
- keeps map state logic untouched.

## 5. Files changed

- `src/styles.css`
- `docs/B89_force_uniform_central_step_card_state.md`
- `tasks/done.md`

## 6. Manual QA

Check:

1. Step cards 01-11 are dark immediately when visible.
2. Cards no longer change from grey to dark at a threshold.
3. The map still changes state while scrolling.
4. Large dark blocks do not return.
5. Hero/header/lower sections remain stable.
"""
    write(DOC, doc)

    done_entry = f"""
## B89 - Force uniform central step card state ({today})

- Forced all central `.b88-step-card` panels to use one dark material independent of active/inactive state.
- Neutralised old opacity/filter/blend/background changes on central scroll-trigger articles.
- Did not change map state names, JavaScript logic, maps or data.
- Created `docs/B89_force_uniform_central_step_card_state.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B89 - Force uniform central step card state" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B89 force uniform central step card state complete.")
    print("Changed:")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
