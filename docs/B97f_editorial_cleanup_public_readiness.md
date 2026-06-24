# B97f - Editorial Cleanup / Public-Readiness

Date: 2026-06-24

## Result

B97f applied a conservative editorial cleanup to `index.html`.

## Changed files

- `index.html`
- `docs/B97f_editorial_cleanup_public_readiness.md`
- `docs/B97f_public_readiness_red_flag_scan.txt`
- `tasks/done.md`

## Replacements applied

- `Methodeische Grenze` -> `Methodische Grenze`: 1
- `Guided scrollytelling prototype` -> `Geführte Kartenstory`: 1
- `Prototype visual state` -> `Methodischer Hinweis`: 1
- `The next implementation will bind these states to real map layers.` -> `Diese Ansicht dient der räumlichen Einordnung und ersetzt keine Eignungs- oder Prioritätskarte.`: 1
- neutralized Phase-B hotspot note: 1
- disambiguated Oberschwaben heading `Oberschwaben zeigt die praktische Herausforderung` -> `Oberschwaben: regionale Ausgangslage`: 1

## Remaining red-flag scan

- Scan file: `docs/B97f_public_readiness_red_flag_scan.txt`
- Remaining hit count: 17

Hits are not automatically failures. They indicate places worth checking manually before external sharing.

## Editorial decisions

- Fixed the prominent typo `Methodeische Grenze` where present.
- Reduced visible prototype/build language.
- Reduced prominent English/German mixing where exact known phrases were present.
- Distinguished the older Oberschwaben explanatory heading from the newer Oberschwaben scrolly map heading.
- Did not move Transformationspfade. That should be handled in B99 after B98 quantitative QA.

## Next recommended steps

1. Run visual QA.
2. Manually inspect remaining red-flag scan.
3. Continue with B98: Oberschwaben intersection area and classification QA.
