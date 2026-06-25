# B104b - Second Visible Wording Polish and Oberschwaben Density Pass

Date: 2026-06-25

## Result

B104b applied a second targeted public-copy polish and a CSS-only density pass for the Oberschwaben scrolly cards.

## Changed files

- `index.html`
- `src/styles.css`
- `docs/B104b_second_visible_wording_and_oberschwaben_density.md`
- `docs/B104b_second_visible_wording_and_oberschwaben_density_audit.txt`
- `tasks/done.md`

## Design/editorial decisions

- Keep the method boundary, but make it read like a compact note rather than a second story block.
- Remove the redundant B98c/pathway QA note because B101 already carries the quantitative evidence.
- Keep the Oberschwaben scrolly, but reduce card size and increase card spacing.
- Avoid additional sticky modules until the current flow is visually stable.

## CSS action

- appended B104b CSS override

## Replacement counts

| Text / pattern | Count |
|---|---:|
| `Fachlicher Hintergrund in 30 Sekunden` | 1 |
| `Deutschland rahmt Planung und Förderung.` | 1 |
| `Nationale Kulissen zeigen, wo Planung und Förderung ansetzen können.` | 1 |
| `Die Thünen-Kulisse konkretisiert organische Böden.` | 1 |
| `Sie macht sichtbar, wo organische Böden für Planung und Förderung relevant sind.` | 1 |
| `BK50 zeigt Moor- und Feuchtbodenkontext.` | 1 |
| `Die Karte ordnet räumlich ein, ersetzt aber keine Eignungs- oder Prioritätsprüfung.` | 1 |
| `Politische und administrative Grenzen bestimmen, wo aus globaler Relevanz Planung wird.` | 1 |
| `Oberschwaben: regionale Ausgangslage` | 1 |
| `Oberschwaben: Wo Moorschutz auf Landwirtschaft trifft` | 1 |
| `Einordnung statt Eignungskarte` | 1 |
| `Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächenei...` | 1 |
| `Datenbasis: Global Peatland Map 2.0, Thünen-Kulisse organischer Böden, BK50 Baden-Württemberg, LUBW/Moorsch...` | 1 |
| `Hier beginnt die eigentliche Planungsfrage` | 1 |
| `Die Flächenverschneidung zeigt,` | 1 |
| `eigene Verschneidung und gesonderte Prüfung der Nutzungsklassen` | 1 |
| `eigene räumliche Verschneidung und Klassifikations-QA` | 1 |
| `remove redundant moore-pathway-note` | 1 |
| `Moorbodenkontext braucht Planung` | 1 |
| `Bodenkontext prägt mögliche Nutzungspfade.` | 1 |

## Smoke-test counts

| Pattern | Before | After |
|---|---:|---:|
| 30 Sekunden | 1 | 0 |
| B98c | 0 | 0 |
| Flächen-QA | 0 | 0 |
| Klassifikations-QA | 1 | 0 |
| Methodeische | 0 | 0 |
| Nasseverträgliche | 0 | 0 |
| Umsetzungsebene | 0 | 0 |
| Umsetzungsfrage | 0 | 0 |
| übersetzen | 0 | 0 |
| Oberschwaben colon headings | 3 | 1 |
| moore-pathway-note | 1 | 0 |

## Next step

Run B103b again and review the corrected visible findings. Then inspect the Oberschwaben scrolly locally.
