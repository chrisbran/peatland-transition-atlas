# B113 – Release Checklist

Stand: 2026-06-25

## A. Current technical state

- [ ] `python scripts\103b_corrected_visible_text_audit.py` runs without changing public source files.
- [ ] `python scripts\58_visual_qa_and_commit_check.py` returns `RESULT: PASS`.
- [ ] `git status --short` contains no staged raw/working data.
- [ ] `index.html` contains no active `oberschwaben_lgl` reference.
- [ ] `index.html` contains no `Datenquelle in Umstellung`.
- [ ] `index.html` contains the current Oberschwaben source note: `FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024`.

## B. Public story checks

- [ ] Global peatland story is understandable without technical explanation.
- [ ] Hotspot/emissions framing does not overclaim precision.
- [ ] Germany/Baden-Württemberg transition is clear.
- [ ] Oberschwaben section clearly explains why this region is shown.
- [ ] Oberschwaben sequence shows: region → use → BK50 context → intersection.
- [ ] Flächenbilanz follows directly from the intersection.
- [ ] Value-chain/pathway section does not read as a finished recommendation catalogue.

## C. Method and source checks

- [ ] Source register exists and is up to date.
- [ ] BK50 selection rule is documented.
- [ ] FIONA classification table is documented.
- [ ] FAOSTAT processing note is documented.
- [ ] Thünen geodata source/version is documented.
- [ ] Literature references have DOI/author/year/journal.
- [ ] LGRB attribution text is included in source register.
- [ ] GISCO attribution is included in source register.
- [ ] FIONA rights/publication status is explicitly marked.

## D. Caveat checks

- [ ] Page does not claim suitability.
- [ ] Page does not claim prioritization.
- [ ] Page does not imply farm-level affectedness.
- [ ] Page does not imply legal eligibility.
- [ ] Page does not claim hydrological feasibility.
- [ ] Page frames maps as orientation and discussion layers.

## E. Visual QA

- [ ] Desktop scroll tested at 1440px width.
- [ ] Desktop scroll tested at 1280px width.
- [ ] Tablet-ish width around 1024px checked.
- [ ] Mobile fallback checked.
- [ ] No sticky heading is clipped.
- [ ] Step cards are readable.
- [ ] Source notes do not dominate the visual flow.
- [ ] Oberschwaben maps remain visually stable through scroll.

## F. Release decision

Recommended release status:

```text
Suitable for internal/project demonstration after B113.
Suitable for broader public release only after FIONA rights clarification and source/method appendix completion.
```
