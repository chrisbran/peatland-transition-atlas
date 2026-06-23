# B94 - Oberschwaben Source Stack

Date: 2026-06-23

## 1. Purpose

B94 anchors the Oberschwaben map workflow to the source logic visible in the SOLAMO-BW flyer map.

The flyer map is not treated as data. It is treated as a **reference for a plausible source stack and map logic**.

## 2. Source stack interpreted from the flyer map

The visible source note in the flyer map points to three core source groups:

1. **Gemeinsamer Antrag Baden-Württemberg / MLR, 2024**  
   Used for agricultural land-use information.

2. **Feuchtgebiete und Moore der Bodenkarte Baden-Württemberg / GeoLa BK50MOOR / LGRB, 2025**  
   Used for the moor/wetland/soil context.

3. **BKG, 2026**  
   Used for administrative/cartographic base information.

## 3. Translation into our map logic

The flyer map shows the communication potential of a regional map where agricultural use and organic/moor soil context are combined.

Our map should not simply copy the flyer. It should reproduce the **analytical logic** with clear method boundaries:

```text
Landwirtschaftliche Nutzung
+
Moor-/Feuchtbodenkontext
=
räumlicher Hinweis auf mögliche Umsetzungsbetroffenheit
```

## 4. Preferred source stack for our first own map

| Map component | Preferred source anchor | Intended role |
|---|---|---|
| Landkreisrahmen | BKG / public admin boundaries | spatial frame |
| Landwirtschaftliche Nutzung | Gemeinsamer Antrag BW, MLR 2024 | agricultural use context |
| Moor-/Feuchtbodenkontext | GeoLa BK50MOOR / LGRB 2025 | soil/moor context |
| Schnittmenge | own GIS overlay | implementation-context signal |

## 5. Source-access status

The source anchors are known, but data access is not yet settled.

Before B95 can build actual assets, we need to clarify:

- whether the Gemeinsamer Antrag layer can be used publicly,
- whether exact agricultural polygons may be displayed,
- whether BK50MOOR/GeoLa data are available in a web-display-safe form,
- which attribution wording is required,
- whether a visual-only map is safer than a map with hectare statistics.

## 6. Method boundary

The source stack supports a **context map**, not a decision map.

Do not label the resulting map as:

- Eignungskarte,
- Prioritätskarte,
- Wiedervernässungspotenzial,
- betroffene Betriebe,
- SOLAMO-Ergebnis.

Preferred wording:

- räumliche Einordnung,
- Nutzung × Bodenkontext,
- mögliche Umsetzungsbetroffenheit,
- Ausgangspunkt für sozio-ökonomische Analyse,
- Grundlage für weitere Prüfung.
