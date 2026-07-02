# B179 - Replace Engpass Scorecard With Bottleneck Graphic

Date: 2026-07-02

## Ziel

B179 ersetzt die bisherige Engpass-/Scorecard-Grafik durch eine statische Flaschenhalsgrafik.

Die Grafik macht die Aussage sichtbar: Bis zur Ernte ist die Kette breit und anschlussfähig; danach wird sie enger. Keine Animation, kein Replay-Button, keine externen Assets.

## Entscheidung

```text
Statischer Endzustand statt animierter Demo.
```

## Beibehalten

- Titel: `Bis zur Ernte ist vieles anschlussfähig. Danach wird es eng.`
- Lead: `Auf dem Feld und bis zur Ernte gibt es erprobte Ansätze. Dahinter entscheiden Logistik, Verarbeitung, Standards und Abnahme darüber, ob nasse Nutzung skalierbar wird.`
- Quellen-/Methodenlinie: qualitative Synthese, keine Messgrafik
- Wertschöpfungs-These
- keine Felt-/OSM-Einbindung

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- kein B169 Sticky-Zoom
- kein B176/B177/B178 Verhalten
- keine externen Ressourcen

## Technische Umsetzung

- Inline-SVG in `index.html`
- responsive Figure mit horizontalem Scroll auf kleinen Screens
- CSS in `src/styles.css`
- keine JS-Animation
- `role="img"` mit `title` und `desc`

## Counts

| Signal | Vorher | Nachher |
|---|---:|---:|
| B179 marker | 0 | 1 |
| Heading | 0 | 1 |
| B179 figure class | 0 | 1 |
| B179 SVG class | — | 1 |
| Animation/Replay terms | — | 2 |
| Felt token in index | 0 | 0 |
| iframe in index | 0 | 0 |
| B179 CSS marker | — | 1 |

## Akzeptanz

- Die Engpass-Grafik ist als Flaschenhals sichtbar.
- Es gibt keine Animation und keinen Replay-Button.
- Die Quellen-/Methodenlinie bleibt sichtbar.
- Mobile Darstellung bleibt lesbar über horizontalen Figure-Viewport.
- B177, B103b und B58 laufen weiter.
