# B116 – Release Candidate State

Stand: 2026-06-25

Status: **RELEASE CANDIDATE FOR INTERNAL/PROJECT DEMO**

## Current git state

```text
Branch: main
HEAD: e514f84 Run final visible copy pass
```

Recent commits:

```text
e514f84 Run final visible copy pass
4c4dca4 Add responsive visual QA and public copy review
787de64 Add public release notes and method documentation
7c5c439 Update visual QA after release hygiene
d46aaf0 Add local git status hygiene notes
16ea24d Add local git status hygiene notes
60bbccd Fix Oberschwaben source note wording
13e3035 Stabilize FIONA public release wording
```

## Current release scope

This release candidate represents the restored **FIONA/BK50/GISCO Oberschwaben public story** within the Moore / Peatland Transition Atlas.

The current state is intended as:

```text
internal/project demonstration version
```

It is not yet a fully cleared broad public release because FIONA derivative-publication rights and some source/method appendices still require final confirmation.

## What is considered stable

- FIONA-based Oberschwaben map story restored.
- LGL source-swap branch parked.
- Oberschwaben source line corrected.
- Visible copy audit passed.
- B58 visual QA returned PASS after release hygiene.
- Overclaim-risk patterns absent from visible text.
- Key caveats are present.

## Active Oberschwaben source line

```text
Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet.
```

## Active interpretation caveat

```text
Lesart: Die Werte geben räumliche Orientierung.
Sie sind keine Eignungskarte, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## Current worktree safety summary

| Check | Count |
|---|---:|
| Git status lines | 66 |
| Modified tracked lines | 1 |
| Untracked lines | 65 |
| Staged lines | 1 |
| Raw/working visible lines | 0 |
| LGL public visible lines | 0 |

Untracked historical scripts/docs may still be visible. That is acceptable if they are not staged and B58 remains PASS.

## Remaining release caveats

For a broader public release, clarify/complete:

1. FIONA derivative-publication and use rights.
2. BK50 class-selection table.
3. FIONA original-class-to-public-class lookup.
4. FAOSTAT processing note.
5. Thünen geodata version/source note.
6. Full bibliography for literature-derived claims.
7. Browser/responsive manual QA.
