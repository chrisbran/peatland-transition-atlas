# B81 - Fix German copy and layout overflow

Date: 2026-06-23

## Ziel

B81 behebt die im Scroll-Video sichtbaren Restprobleme nach B79/B80:

1. sichtbare englische Hero-/Meta-Texte oben auf der Seite,
2. Layout-Überläufe in den Hero-Karten,
3. Texte, die aus ihren Rahmen laufen,
4. störende Overlay-/Ghost-Artefakte.

## Änderungen

### Inhalt / Copy
Sichtbare Resttexte wurden auf Deutsch gesetzt:

- `PORTFOLIO PROTOTYPE · LITERATURE-DRIVEN MVP`
  → `MOORE · KLIMASCHUTZ · REGIONALE UMSETZUNG`
- `Peatland Transition Atlas`
  → `Moorschutz braucht räumliche Orientierung`
- `Mapping the space between drainage-based agriculture and rewetting-compatible land use.`
  → `Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.`

### Layout
- Hero-Bereich hart auf einen klaren einspaltigen Präsentationsaufbau gesetzt.
- Claim-Karten auf belastbare Grid-Spalten mit Mindestbreiten umgestellt.
- Overflow-Wrapping für Karten- und Step-Texte verschärft.
- Pseudo-Element-Overlays in Hero-/Kartensteps unterdrückt.

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `docs/B81_fix_german_copy_and_layout_overflow.md`
- `tasks/done.md`

## Manuelle QA

Nach B81 prüfen:

1. Oberster Block komplett auf Deutsch.
2. Keine sichtbaren Begriffe wie `prototype`, `atlas`, `literature-driven`, `mapping the space ...`.
3. Hero-Karten brechen sauber um.
4. Kein Text läuft über Kartenränder hinaus.
5. Zentrale Kartenfolge funktioniert weiter.
