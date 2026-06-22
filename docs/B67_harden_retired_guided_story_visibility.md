# B67 - Harden Retired guidedStory Visibility

Date: 2026-06-22

## 1. Purpose

B67 makes the B64 retirement of `#guidedStory` robust against public-site stylesheet caching.

B64 intentionally kept the old guided story in the HTML and hid it by class/CSS. On GitHub Pages or in a browser cache, an outdated stylesheet can still make the retired section visible. B67 therefore adds native HTML-level hiding to the `#guidedStory` section.

## 2. Changed files

- `index.html`
- `docs/B67_harden_retired_guided_story_visibility.md`
- `tasks/done.md`

## 3. Opening tag before patch

```html
<section id="guidedStory" class="section guided-story is-retired" aria-hidden="true">
```

## 4. Opening tag after patch

```html
<section id="guidedStory" class="section guided-story is-retired" aria-hidden="true" data-retired="B64" style="display: none !important;">
```

## 5. Not changed

B67 does not delete:

- the `guidedStory` section content,
- any JavaScript file,
- any public data file,
- any map/image asset.

## 6. Reasoning

This is a defensive patch. It makes the retired section hidden even if the browser or GitHub Pages serves an outdated stylesheet.

## 7. Required QA

After B67:

1. Run `python scripts\58_visual_qa_and_commit_check.py`.
2. Open `http://localhost:8000/?v=b67`.
3. Open `https://chrisbran.github.io/peatland-transition-atlas/?v=b67` after push.
4. Confirm that `guidedStory` is not visible in either version.
5. Confirm that the central PNG story, hotspots, evidence map, pathways and fit sections still render.
