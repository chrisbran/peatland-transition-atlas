# B78 - Patch Strategy for B79

Date: 2026-06-23

## 1. Recommended B79 approach

B79 should be a single conservative patch:

`79_apply_german_presentation_version.py`

It should:

1. read `index.html`,
2. apply targeted text replacements,
3. inject or append B79 CSS overrides in `src/styles.css`,
4. add a short regional implementation block if needed,
5. create `docs/B79_german_presentation_version.md`,
6. update `tasks/done.md`.

## 2. Safer than manual editing

Manual editing is risky because:

- the page has multiple retired sections,
- central map state binding must stay intact,
- old scripts have been retired but not deleted,
- previous patches showed encoding risk with PowerShell.

Therefore B79 should write UTF-8 LF and avoid PowerShell `Set-Content`.

## 3. Text replacement strategy

Use precise replacements where possible.

Avoid broad regex replacements that might touch hidden/retired sections unless intended.

Priority order:

1. Hero and nav
2. Transition logic / argument block
3. Central map section headings and visible steps
4. Lower evidence headings
5. Method boundary
6. Source/caption cleanup

## 4. CSS strategy

Do not remove old CSS.

Append a clear B79 override block at the end:

```css
/* B79 German presentation version */
...
```

Benefits:

- reversible,
- low risk,
- easy diff,
- avoids breaking older layout.

## 5. What not to do in B79

Do not:

- delete sections,
- delete scripts,
- rewrite map JS,
- touch map PNGs,
- add new data,
- add external fonts,
- add decorative photos,
- create a new interaction model,
- change central map state names.

## 6. Rollback

If B79 looks wrong:

```powershell
git checkout -- index.html src/styles.css tasks/done.md
```

If docs/scripts are uncommitted:

```powershell
Remove-Item docs/B79_german_presentation_version.md -ErrorAction SilentlyContinue
Remove-Item scripts/79_apply_german_presentation_version.py -ErrorAction SilentlyContinue
```

If already committed:

```powershell
git revert <commit>
```

## 7. Next decision before B79

Recommended decisions:

1. Main visible path should become German first; lower technical material can follow later.
2. Old lower evidence/explorer areas should be reduced visually, not deleted.
3. Main navigation should use: `Problem · Kartenfolge · Umsetzung · Pfade · Methode`.
