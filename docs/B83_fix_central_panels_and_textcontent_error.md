# B83 - Fix Central Panels and textContent Error

Date: 2026-06-23

## 1. Issue

The B82 video showed three remaining issues:

1. A visible literal `\n` artefact between central story steps.
2. Step 01 had a good dark panel treatment, while later central story panels looked lighter/ghosted.
3. A red browser/app error appeared at the top:

```text
can't access property "textContent", document.querySelector(...) is null
```

## 2. Why the error appeared

The error means that a JavaScript file tried to do this:

```js
document.querySelector(...).textContent = ...
```

but the selector did not find an element.

That is plausible after B79/B82 because older prototype sections were retired or the header/labels were replaced. A script still expected a DOM element that no longer exists in the visible page.

## 3. Changes

B83:

- removes literal `\n` artefacts from `index.html`,
- applies a consistent dark panel treatment to all central map step cards,
- hardens text wrapping inside central step panels,
- suppresses old pseudo-element panel overlays,
- guards direct `document.querySelector(...).textContent = ...` assignment patterns in `src/*.js`.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B83_fix_central_panels_and_textcontent_error.md`

JavaScript files patched:

- `src/app.js`

## 5. Literal newline artefacts

Occurrences removed from `index.html`:

`1`

## 6. Manual QA

Check:

1. No red error bar at the top.
2. No visible `\n` between steps.
3. Central step panels 01-11 use the same dark readable style.
4. Text stays inside panel frames.
5. Central map sequence still scrolls correctly.
6. Navigation and hero remain stable.
