# B104 - Visible Wording Polish

Date: 2026-06-25

## Result

B104 applied a targeted polish to visible public wording based on B103b.

## Changed files

- `index.html`
- `docs/B104_visible_wording_polish.md`
- `docs/B104_visible_wording_polish_audit.txt`
- `tasks/done.md`

## Not changed

- `src/styles.css`
- JS logic
- map PNGs
- GIS/data folders
- hidden/retired archive sections were not intentionally removed

## Replacement counts

| Pattern / old text | Replacements |
|---|---:|
| `Nasseverträgliche` | 1 |
| `Global peatland context` | 1 |
| `Peatlands are spatially concentrated.` | 1 |
| `Peatland context` | 1 |
| `Layer stack: Global Peatland Map 2.0 context and country hotspot layers.` | 1 |
| `All images exported from the same ArcGIS global map frame.` | 1 |
| `Moore · Klimaschutz · regionale Umsetzung` | 1 |
| `>Umsetzung<` | 1 |
| `Globale Karten zeigen Relevanz. Umsetzung entsteht erst auf nationaler, regionaler und betrieblic...` | 1 |
| `Aus Moorbodenkontext wird eine Umsetzungsfrage` | 1 |
| `Moorschutz wird erst dann planbar, wenn räumliche Kulissen, regionale Nutzung, betriebliche Betro...` | 1 |
| `Europa wird zur Umsetzungsebene.` | 1 |
| `Politische und administrative Grenzen übersetzen globale Relevanz in Handlungsräume.` | 1 |
| `Deutschland ist eine Umsetzungsebene.` | 1 |
| `Nationale Kulissen übersetzen globale Relevanz in Planung und Förderung.` | 1 |
| `Sie macht sichtbar, wo organische Böden für nationale Umsetzung relevant werden.` | 1 |
| `Unterschiedliche Bodenkontexte verlangen unterschiedliche Übergänge.` | 1 |
| `Baden-Württemberg wird konkret.` | 1 |
| `Auf regionaler Ebene werden Moor- und Feuchtbodenkontexte zur Planungsfrage.` | 1 |
| `Regionale Umsetzung` | 2 |
| `SOLAMO-BW untersucht regionale Betriebsmuster und die Umsetzbarkeit von Nutzungskonzepten auf wie...` | 1 |
| `Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird` | 1 |
| `Ein regionaler Umsetzungsraum` | 1 |
| `Hier wird Moorschutz zur Umsetzungsfrage` | 1 |
| `markiert Räume, in denen Transformationsfragen konkret werden: Bewirtschaftung,           Wassers...` | 1 |
| `Interne Verschneidung` | 1 |
| `Die interne Flächen-QA zeigt aber,` | 1 |
| `dass die Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext         nicht...` | 1 |
| `Ackerland, bereinigt um Sonderfälle` | 1 |
| `Stilllegung oder unklare FIONA-Zuweisung getrennt geprüft` | 1 |
| `Diese Werte beschreiben eine Such- und Gesprächskulisse.` | 1 |
| `eigene Verschneidung und B98c-Klassifikations-QA. Werte gerundet.` | 1 |
| `Von der Schnittmenge zu handhabbaren Transformationspfaden` | 1 |
| `Die Schnittmenge ist eine Such- und Gesprächskulisse.` | 1 |
| `Was die B98c-QA nahelegt` | 1 |
| `Die interne Flächen-QA stützt die qualitative Erzählung: Die Schnittmenge ist` | 1 |
| `Welche Pfade aus nassen Flächen Wertschöpfung machen könnten` | 1 |
| `Die Transformationspfade werden erst tragfähig, wenn aus Biomasse, Pflege,       Energie oder Flä...` | 1 |
| `Produktlogik` | 2 |
| `Reifegrad` | 1 |
| `Hauptengpass` | 1 |
| `collapse repeated spaces` | 1016 |

## Smoke-test counts in HTML after replacement

| Pattern | Before | After |
|---|---:|---:|
| Nasseverträgliche | 1 | 0 |
| prototype/explorer | 20 | 20 |
| peatland context | 2 | 0 |
| Umsetzung* | 12 | 0 |
| wird zu/zur/zum/eine | 2 | 0 |
| übersetz* | 2 | 0 |
| Flächen-QA | 2 | 0 |
| B98c | 2 | 0 |
| Klassifikations-QA | 2 | 1 |

## Editorial intent

- Keep the existing structure and matrix.
- Remove the obvious typo.
- Translate visible English map-context labels.
- Reduce the repeated `Umsetzung / wird zu / übersetzen` rhythm.
- Replace internal QA/build terms in visible public copy with reader-facing wording.

## Next step

Run B103b again and compare `docs/B103b_visible_findings.csv` and `docs/B103b_wording_frequency.csv`.
