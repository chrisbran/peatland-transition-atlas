# B96 - Bind Oberschwaben Scrolly Layer Stack

Created from B95h on 2026-06-24

## Goal

Implement an Oberschwaben scrollable layer-stack module in the German presentation page.

## Required assets

- `public/maps/oberschwaben/oberschwaben_admin_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture.png`
- `public/maps/oberschwaben/oberschwaben_moor_context.png`
- `public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png`

## Section concept

Working title:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

## State sequence

1. Region: Landkreisrahmen + Namen.
2. Landwirtschaft: Ackerland, Grünland, Dauerkultur.
3. Bodenkontext: BK50 Moor-/Feuchtbodenkontext.
4. Schnittmenge: Nutzung × Bodenkontext.
5. Methodische Grenze: räumliche Einordnung, keine Eignungs- oder Prioritätskarte.

## Implementation requirements

- Use a sticky map stage with stacked PNG layers.
- Keep `oberschwaben_admin_context.png` on top in all states.
- Do not use the static composite map as the primary module.
- Do not call the intersection Wiedervernässungspotenzial.
- Do not imply farm-level affectedness.
- Keep the method boundary visible.

## Method boundary text

```text
Die Karte zeigt eine räumliche Einordnung der Überschneidung von landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```
