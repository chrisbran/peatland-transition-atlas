# B169e - Replace Oberschwaben Zoom Map

Date: 2026-07-01

## Ziel

B169e ersetzt im Live-Sticky-Zoom direkt die Oberschwaben-Handoff-Karte.

Neue Karte:

```text
public/maps/oberschwaben/oberschwaben_landkreise_moor_nolabel.png
```

Diese Karte zeigt bewusst:

- Landkreisgrenzen
- Moor-/Feuchtbodenkontext
- keine Labels
- keine Überlagerung mit landwirtschaftlicher Nutzung

## Warum

Die Überlagerung von Moor-/Feuchtbodenkontext und Landwirtschaft soll später in der regionalen Story ihre Rolle spielen.
Im Sticky-Zoom geht es nur um die Maßstabsbrücke:

```text
Deutschland → Baden-Württemberg → Oberschwaben als regionaler Bodenkontext
```

## Änderungen

- Oberschwaben-State nutzt jetzt `oberschwaben_landkreise_moor_nolabel.png`.
- Oberschwaben-Overlay-Hack aus B169d wird entfernt.
- Oberschwaben-Text wird angepasst:
  - nicht mehr „Moorschutz trifft Landwirtschaft“
  - sondern „Region wird lesbar, Nutzungsfrage folgt“
- JS bleibt schlank: keine Annotationen, nur Step/Image/Label-State.

## Nicht geändert

- keine neue Statefolge
- keine neue Datenquelle
- keine Änderung an Felt
- keine Änderung an der späteren Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Visuelle QA

Prüfen:

- Oberschwaben-Step zeigt Landkreisgrenzen ohne Namen.
- Moor-/Feuchtbodenkontext ist sichtbar.
- Die landwirtschaftliche Überschneidung wird noch nicht vorweggenommen.
- Keine extra Overlay-Artefakte.
- Übergang zur nachfolgenden Oberschwaben-Story bleibt logisch.
