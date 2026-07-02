# B172 - Mobile Sticky Zoom Polish

Date: 2026-07-01

## Ziel

B169 bis B170 haben die neue Live-Kartenfolge auf Desktop stabilisiert.
B172 poliert jetzt nur die mobile Darstellung.

Problem vorher:

```text
Auf kleinen Bildschirmen standen die Textsteps vor der Karte.
Dadurch war die Kartenfolge mobil nicht wirklich als Scrolly lesbar.
```

B172 ordnet die mobile Darstellung so um:

```text
Karte oben leicht sticky
nummerierte Steps darunter
```

Damit bleiben Karte und Text auch auf 390px-Breite verbunden.

## Änderungen

Nur CSS:

- `.b169-layout` wird mobil zu einer Flex-Spalte
- `.b169-stage-wrap` bekommt `order: 1`
- `.b169-steps` bekommt `order: 2`
- die Kartenbühne bleibt mobil leicht sticky
- Textsteps bekommen größere vertikale Atemräume
- die separate Mobile-Note wird ausgeblendet, weil das Layout jetzt selbsterklärender ist

## Nicht geändert

- keine HTML-Struktur
- keine JS-Logik
- keine Kartenassets
- keine Statefolge
- keine Oberschwaben-Story
- keine Felt-Integration

## Prüfen

Desktop:

- unverändert

Mobile 390px:

- Karte erscheint vor den Steps
- Karte bleibt beim Scrollen sichtbar
- aktive Steps wechseln die Karte
- Stage-Label bleibt lesbar
- keine riesige Lücke zwischen Step und Karte
