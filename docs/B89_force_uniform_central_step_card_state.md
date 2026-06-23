# B89 - Force Uniform Central Step Card State

Date: 2026-06-23

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
