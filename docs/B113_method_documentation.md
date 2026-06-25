# B113 – Method Documentation

Stand: 2026-06-25

## Purpose

This document records the current method logic behind the public Moore / Peatland Transition Atlas state, with emphasis on the restored FIONA-based Oberschwaben map sequence.

It is intended for project documentation and release review. It is not a replacement for a full reproducibility package.

## Processing chain overview

### 1. Global and country context

**Input concepts**

- Global peatland distribution from Global Peatland Map 2.0 / Global Peatland Database.
- Country-level drained organic-soil emissions from FAOSTAT-derived data.

**Project use**

- Global spatial framing.
- Country hotspot and emissions framing.
- Narrative transition from global distribution to climate relevance.

**Method boundary**

The global maps support orientation and storytelling. They do not establish local intervention priorities.

### 2. Germany and Baden-Württemberg context

**Input concepts**

- Germany organic-soil / peat-soil context from Thünen-related sources.
- Baden-Württemberg BK50 / GeoLa-derived peat/wet-soil context.

**Project use**

- Translate global problem into German and regional planning context.
- Show that the question narrows from global hotspots to specific regional implementation contexts.

**Method boundary**

The Germany and Baden-Württemberg maps are context frames. They do not replace detailed soil, hydrology or land-use verification.

### 3. Oberschwaben spatial frame

Oberschwaben is represented through four counties:

- Biberach
- Bodenseekreis
- Ravensburg
- Sigmaringen

The current administrative frame is derived from GISCO NUTS 2024 / project-processed county geometry.

### 4. BK50 Moor-/Feuchtbodenkontext

**Input**

- LGRB dBK50 / GeoLa BK50 county-level vector data.
- Four relevant county downloads were identified for Biberach, Bodenseekreis, Ravensburg and Sigmaringen.

**Project-derived layers**

The local project contains derived layers corresponding to:

```text
bk50_moor_oberschwaben_raw
bk50_moor_oberschwaben_context
```

**Interpretation**

This is a BK50-derived **Moor-/Feuchtbodenkontext**, not a final hydrological planning or rewetting suitability layer.

**Documentation need**

The exact BK50 class-selection rule must be documented in a dedicated table:

```text
BK50 field / class / unit → include or exclude → reason
```

### 5. FIONA agricultural-use layer

**Input**

- FIONA 2024 / FIONA-Flächeninformation.
- Used as agricultural-use layer for the restored public Oberschwaben story.

**Project-derived layers**

The project used/created derived layers corresponding to:

```text
fiona_2024_oberschwaben_agri3
fiona_2024_oberschwaben_agri3_dissolved
agriculture_bk50_intersection_oberschwaben
agriculture_bk50_intersection_oberschwaben_dissolved
```

**Classification logic**

FIONA land-use classes were grouped into broad public classes:

```text
Grünland
Ackerland
Dauerkultur / Sondernutzung where applicable
Stilllegung or unclear assignment separately reported
```

**Documentation need**

A final method appendix should include:

- source field(s) used for classification;
- lookup table from original FIONA class to public class;
- handling of unclear/review classes;
- date/version of FIONA service/data;
- legal/publication-use clarification.

### 6. FIONA × BK50 intersection

**Purpose**

The intersection answers the regional orientation question:

```text
Where does agricultural use overlap with BK50 Moor-/Feuchtbodenkontext in Oberschwaben?
```

**Derived figure**

The current public value is rounded:

```text
~19,900 ha agricultural use in BK50 Moor-/Feuchtbodenkontext
```

**Class split**

```text
~82 % Grünland
~16 % Ackerland
~2 % Stilllegung or unclear assignment separately reported
```

These values are public-orientation numbers, not a regulatory area statement.

### 7. Cartographic treatment

The active Oberschwaben cartographic logic is:

```text
admin context
→ agricultural use
→ BK50 Moor-/Feuchtbodenkontext
→ agricultural use × BK50 intersection
```

Analytical layers and cartographic layers are not identical:

- analytical layers support area calculations and QA;
- dissolved/cartographic layers support readable web maps.

This distinction explains why earlier FIONA maps looked calmer than raw LGL test maps.

### 8. LGL replacement branch

**Status**

Parked.

**Reason**

LGL Landnutzung WFS was tested as a possible public-safe replacement for FIONA. It proved technically usable, but cartographic fragmentation was too high for the current public story without additional generalization.

**Implication**

LGL outputs should not be mixed into the active FIONA-based public page.

## Interpretation rules for public communication

Use formulations like:

```text
Die Karte zeigt räumliche Schnittmengen und Planungskontexte.
```

Avoid formulations like:

```text
Die Karte zeigt Wiedervernässungspotenzial.
Die Karte zeigt geeignete Flächen.
Die Karte priorisiert Maßnahmen.
Die Karte zeigt betroffene Betriebe.
```

## Minimum reproducibility package still needed

For a stronger release package, create or finalize:

1. **Source register**  
   `docs/B110_external_source_register.md`

2. **BK50 class-selection table**  
   original BK50 class → included/excluded → rationale

3. **FIONA classification table**  
   original FIONA use/class → public class → review flag

4. **FAOSTAT processing note**  
   source table, years, variables, GWP conversion

5. **Map asset manifest**  
   public PNG → source layers → export date → software → extent/projection

6. **Rights and caveats note**  
   FIONA derivative-use clarification, LGRB attribution, FAOSTAT attribution, GISCO attribution

## Suggested public source line

For the current public page:

```text
Datenbasis: Global Peatland Map 2.0; FAOSTAT drained organic soils; Thünen-Kulisse organischer Böden; Regierungspräsidium Freiburg – LGRB, dBK50 / GeoLa BK50; FIONA 2024; GISCO NUTS 2024; eigene Auswahl, Klassifikation, Verschneidung und kartografische Aufbereitung.
```

For Oberschwaben specifically:

```text
Datenbasis: FIONA 2024, BK50 Moor-/Feuchtbodenkontext und GISCO NUTS 2024; eigene Auswahl, Klassifikation und Verschneidung. Werte gerundet.
```

## Known release blockers

| Blocker | Severity | Action |
|---|---:|---|
| FIONA public derivative-use rights | high | clarify before broad public dissemination |
| BK50 inclusion rule missing as table | medium | document class selection |
| FAOSTAT reproducibility note incomplete | medium | add source/API/method note |
| Literature references incomplete | medium | complete DOI/author/year list |
| Responsive/browser QA pending | medium | run final visual QA |
