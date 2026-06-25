# B114 – Responsive Visual QA Plan

Stand: 2026-06-25

## Purpose

B114 defines the manual visual QA for the current restored FIONA-based public version of the Moore / Peatland Transition Atlas.

It should be used after B113 method documentation and before a broader public/demo release.

## Scope

This QA does not test scientific correctness of all source data. It checks whether the public page presents the current state clearly and without obvious layout, wording or source-state errors.

## Test setup

Run locally:

```powershell
cd C:\Users\User\Documents\GitHub\peatland-transition-atlas
python -m http.server 8000
```

Open:

```text
http://localhost:8000/index.html
```

Recommended browser:

```text
Firefox or Chrome desktop, plus mobile viewport simulation in browser dev tools.
```

## Required viewports

| Viewport | Purpose |
|---|---|
| 1440 × 900 | main desktop reference |
| 1280 × 800 | typical laptop |
| 1024 × 768 | tablet-ish / constrained desktop |
| 390 × 844 | mobile fallback / phone portrait |

## Core visual questions

### A. Whole-page story

- Does the page move from global issue to regional implementation without abrupt jumps?
- Does the global hotspot sequence still feel necessary and not overly long?
- Does Germany/Baden-Württemberg prepare the Oberschwaben focus?
- Does the lower pathway/value-chain section follow logically from the map evidence?

### B. Oberschwaben section

Required order:

```text
admin context
→ agricultural use
→ BK50 Moor-/Feuchtbodenkontext
→ agriculture × BK50 intersection
→ key figures
→ pathways/value chains
```

Check:

- no active `oberschwaben_lgl` map appears;
- the old FIONA dark-map style remains active;
- the key figures follow from the intersection map;
- source note is visible but not visually dominant;
- method caveat remains close to the key figures.

### C. Sticky behaviour

Check:

- no heading is clipped by sticky offset;
- map stage is not too tall on laptop;
- step card does not obscure the key map signal;
- transitions are not flickering;
- mobile fallback is readable.

### D. Public copy

The text should not claim:

```text
Eignung
Priorisierung
Wiedervernässungspotenzial
betriebliche Betroffenheit
rechtliche Förderfähigkeit
hydrologische Machbarkeit
```

The text may claim:

```text
räumliche Orientierung
Schnittmenge
Planungskontext
Prüfpfade
Gesprächs-/Abstimmungsbedarf
```

## Manual test matrix

Use:

```text
docs/B114_manual_test_matrix.csv
```

Fill the `result` column with:

```text
PASS
WARN
FAIL
```

## Pass criteria

Minimum pass criteria:

- B58 returns `RESULT: PASS`;
- no active source-swap/LGL remnants in `index.html`;
- Oberschwaben sequence is visually stable at 1440 and 1280 px;
- no public copy implies site-level suitability or priority;
- source caveats are present in docs and compactly visible on page.

## Known non-blockers

The following are not release blockers for an MVP/demo:

- local untracked historical scripts/docs;
- parked LGL test outputs, as long as not active in public page;
- PowerShell 5.1 UTF-8 display artifacts in terminal output;
- source/method documentation still needing bibliographic completion, if release is explicitly internal/demo.

## Release blockers

For broader public dissemination:

- unresolved FIONA derivative-use/publication rights;
- missing BK50 class-selection table;
- incomplete FAOSTAT processing note;
- incomplete literature bibliography;
- untested mobile layout.
