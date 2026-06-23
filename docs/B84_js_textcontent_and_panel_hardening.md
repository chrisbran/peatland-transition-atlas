# B84 - JS textContent and Panel Hardening

Date: 2026-06-23

## 1. Why B84 was needed

After B83, two issues remained:

1. The red error bar was still visible:
   `can't access property "textContent", document.querySelector(...) is null`
2. Only step 01 reliably used the desired dark panel style; later cards still appeared lighter.

B83 only guarded simple one-line `document.querySelector(...).textContent = ...` assignments. B84 scans both `index.html` and `src/*.js` for broader read/assignment patterns.

## 2. What B84 changed

- Hardened broader `document.querySelector(...).textContent` patterns.
- Removed remaining literal `\n` artefacts from `index.html`.
- Added a broader central-story CSS rule so all central map text cards/articles get the same dark panel style.
- Added a visual safeguard for browser/debug-style error banners.
- Created `docs/B84_textcontent_patch_inventory.txt`.

## 3. Files changed by JS hardening

- none

## 4. Remaining raw textContent patterns

- none

## 5. Literal newline artefacts removed

`0`

## 6. Manual QA

Check after running B84:

1. Red error bar is gone.
2. No visible `\n` appears between steps.
3. Steps 01-11 use dark readable panels.
4. Map scroll still works.
5. The central map image/frame is not accidentally dark-card styled.
6. Hero and compact header remain stable.
