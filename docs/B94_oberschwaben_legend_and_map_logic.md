# B94 - Oberschwaben Legend and Map Logic

Date: 2026-06-23

## 1. Purpose

Define a legend and map logic that follows the SOLAMO flyer source stack but avoids overclaiming.

## 2. Working map title

Preferred:

```text
Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird
```

Alternative shorter:

```text
Oberschwaben: Nutzung × Moorbodenkontext
```

## 3. Core map statement

```text
Die Karte zeigt, wo landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext räumlich zusammentreffen.
```

## 4. Legend entries

Recommended first legend:

| Legend entry | Meaning | Visual role |
|---|---|---|
| Landkreisrahmen | four SOLAMO districts | orientation |
| Ackerland | agricultural use class | land-use context |
| Grünland | agricultural use class | land-use context |
| Dauerkultur | agricultural use class | land-use context |
| Moor-/Feuchtbodenkontext | soil/moor/wetland context | environmental context |
| Schnittmenge Nutzung × Bodenkontext | agriculture on/within moor-wetland context | implementation signal |

## 5. Alternative simplified legend

If the map becomes too dense:

| Legend entry | Meaning |
|---|---|
| Landwirtschaftliche Nutzung | merged agriculture |
| Moor-/Feuchtbodenkontext | merged soil/moor context |
| Schnittmenge Nutzung × Bodenkontext | overlap |

This may be better for the website.

## 6. Wording to avoid

Do not use:

- Wiedervernässungspotenzial,
- Prioritätsfläche,
- geeignete Fläche,
- betroffene Betriebe,
- Maßnahmenfläche,
- Paludikulturfläche,
- SOLAMO-Ergebnis.

## 7. Preferred explanatory note

```text
Die Darstellung zeigt eine räumliche Einordnung. Sie ersetzt keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.
```

## 8. Interpretation cards for the future page

### Karte zeigt Kontext

```text
Die Karte markiert Räume, in denen landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext zusammenfallen.
```

### Daraus entsteht Betroffenheit

```text
Erst aus der Überschneidung von Fläche, Nutzung und Betriebsstruktur wird eine Umsetzungsfrage.
```

### Daraus folgen Nutzungspfade

```text
Mögliche Pfade reichen von Schutz und Stabilisierung über Wiedervernässung bis zu nasser Nutzung und Wertschöpfungsketten.
```

## 9. Visual hierarchy

The intersection layer should be the focus, but it should not look like an alarm or priority class.

Recommended visual hierarchy:

1. intersection layer strongest,
2. moor-/soil context second,
3. agriculture classes restrained,
4. county boundaries and labels quiet.

## 10. First map design choice

For B95, prefer a **single composite map** first.

Reason:

- easier to review,
- lower implementation risk,
- enough for project discussion,
- avoids adding another scroll system before the map logic is stable.
