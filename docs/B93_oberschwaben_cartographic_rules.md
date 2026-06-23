# B93 - Oberschwaben Cartographic Rules

Date: 2026-06-23

## 1. Design principle

The map should look like a professional regional implementation map, not like a GIS dump.

It should support one argument:

**Wo landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext zusammentreffen, wird Moorschutz zur Umsetzungsfrage.**

## 2. Must show

- four SOLAMO districts,
- agriculture layer,
- moor/soil context layer,
- intersection layer,
- simple legend,
- method boundary in documentation.

## 3. Must not show

- parcel-level farm information,
- confidential farm-level data,
- exact farm affectedness,
- suitability classes,
- priority classes,
- intervention recommendations.

## 4. Recommended legend wording

Use:

```text
Landkreisrahmen
Landwirtschaftliche Nutzung
Moor-/Feuchtbodenkontext
Schnittmenge: Nutzung × Bodenkontext
```

Avoid:

```text
geeignete Flächen
Prioritätsflächen
Wiedervernässungspotenzial
betroffene Betriebe
```

## 5. Color logic

Recommended direction:

- background: warm paper or transparent,
- counties: muted grey/brown,
- agriculture: restrained ochre/yellow-green,
- moor context: teal/green,
- intersection: strongest but not alarming accent.

Do not use red for intersection unless explicitly communicating risk, because it may imply alarm or priority.

## 6. Label hierarchy

Highest:

- title or module heading outside map,
- intersection layer in legend.

Medium:

- county names.

Low:

- source note,
- orientation labels.

## 7. Source note

Suggested short source note:

```text
Eigene Darstellung auf Basis von Landkreisgrenzen, landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext. Methodische Einordnung, keine Eignungs- oder Prioritätskarte.
```

Replace with exact source names once data decisions are final.
