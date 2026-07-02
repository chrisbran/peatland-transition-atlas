# B169c - Live Sticky Zoom Text and Artifact Fix

Date: 2026-07-01

## Ziel

Die B169/B169b-Ansicht hatte drei sichtbare Probleme:

1. Links erschien vor `02 / Gesamt` ein unnummerierter Textblock im anderen Design.
2. Die Textsteps wirkten beim Aktivwerden so, als würden sie leicht nach links springen.
3. Im Oberschwaben-Step wirkten Landkreisnamen wie Artefakte.

B169c korrigiert diese Punkte, ohne die Statefolge zu ändern.

## Änderungen

### 1. Keine separate Kartenannotation mehr

Die schwebende Annotation unten rechts und mögliche unnummerierte Annotationstexte werden entfernt.
Die linke Textspur besteht jetzt nur noch aus nummerierten Steps:

```text
01 / Welt
02 / Gesamt
03 / Intensität
...
```

### 2. Kein seitlicher Step-Sprung

Der aktive Step wird nicht mehr per `translateX()` verschoben.
Es ändert sich nur noch die Opazität.

### 3. Oberschwaben-Overlay deaktiviert

Für `oberschwaben-handoff` wird kein separates Admin-Overlay mehr eingeblendet.
Die Landkreisnamen wirkten im Live-Zoom wie Artefakte und sind für den Übergabeschritt nicht nötig.
Die Detailorientierung kommt später in der regionalen Oberschwaben-Section und im Felt-Block.

## Nicht geändert

- keine neue Karte
- keine neue Statefolge
- keine neue Datenquelle
- keine Änderung an Felt
- keine Änderung an Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Prüfen

- `01 / Welt` erscheint als erster normaler Textstep.
- Kein unnummerierter Vorabtext vor `02 / Gesamt`.
- Beim Scrollen kein seitliches Springen der Textblöcke.
- Oberschwaben-Step wirkt sauberer, ohne störende Landkreisnamen.
