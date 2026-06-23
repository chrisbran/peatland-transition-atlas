# B92 - Oberschwaben Implementation Story Concept

Date: 2026-06-23

## 1. Strategic shift

The website has a working German presentation version. The next step is no longer design polish. The next step is a substantive regional implementation module.

Current story:

```text
Global relevance -> Europe -> Germany -> Baden-Württemberg -> BK50 soil context
```

Next story layer:

```text
Baden-Württemberg -> Oberschwaben -> agriculture x peat/organic/wetland soil context -> farm affectedness -> use concepts -> value chains -> policy instruments
```

## 2. Core thesis

**Oberschwaben zeigt, dass Moorschutz nicht an der Moorgrenze endet. Er wird dort zur Umsetzungsfrage, wo Moorboden, landwirtschaftliche Nutzung, Betriebe, Wasserstand, Wertschöpfung und Förderung zusammen betrachtet werden müssen.**

## 3. Why Oberschwaben

The SOLAMO-BW flyer defines the project focus as the analysis and assessment of use concepts for rewetting peatlands in Baden-Württemberg's Oberschwaben region, specifically the districts Ravensburg, Biberach, Sigmaringen and Bodenseekreis.

The same project logic is highly compatible with the page's existing endpoint:

- affected agricultural farms,
- alternative use concepts,
- exchange with farmers, authorities and companies,
- interviews and workshops,
- future scenarios and value chains,
- economic modelling,
- climate performance and farm-level economic consequences,
- policy recommendations.

## 4. Why the existing BW/BK50 endpoint is not enough

The current BK50/BW map shows a regional soil and wetland context. That is useful, but incomplete.

It does not answer:

- Which parts of the regional soil context are agriculturally used?
- Which districts carry the strongest overlap between agriculture and peat/wetland soil context?
- Which land-use types dominate that overlap?
- Where does the question become a farm and value-chain problem?
- Which instruments would be needed to make transition feasible?

Therefore the next analytical object is not simply a moor map.

The next analytical object is:

**Landwirtschaftliche Nutzung auf Moor-/organischem Boden-/Feuchtbodenkontext in Oberschwaben.**

## 5. Proposed map module

Working title:

**Oberschwaben: Wo Moorschutz zur landwirtschaftlichen Umsetzungsfrage wird**

Map sequence:

1. `Oberschwaben: Landkreisrahmen`
2. `Landwirtschaftliche Nutzung`
3. `Moor-/organische Boden-/Feuchtbodenkulisse`
4. `Schnittmenge Landwirtschaft × Moor-/Feuchtbodenkontext`
5. optional: `Nutzungstypen auf Moor-/Feuchtbodenkontext`

This should initially be a static map module, not an interactive dashboard.

## 6. Suggested narrative section

Place after the current central map story and before or inside the existing regional implementation section.

Suggested text:

```text
Oberschwaben zeigt die praktische Herausforderung.

In den Landkreisen Ravensburg, Biberach, Sigmaringen und dem Bodenseekreis treffen Moor- und Feuchtbodenkontexte auf intensive landwirtschaftliche Nutzung. Damit wird Moorschutz nicht nur zur Frage des Wasserstands, sondern zur Frage betrieblicher Betroffenheit, möglicher Nutzungspfade, Wertschöpfungsketten und Förderinstrumente.
```

Follow-up:

```text
Die Karte zeigt keine Eignung und keine Priorität. Sie markiert Räume, in denen landwirtschaftliche Nutzung und Moor-/Feuchtbodenkontext gemeinsam betrachtet werden müssen.
```

## 7. Map interpretation logic

The regional map should answer four questions:

### 1. Where is the soil context?

Where do peat, organic or wetland soil contexts occur in the four SOLAMO districts?

### 2. Where is the agricultural use context?

Where is agricultural land use located within the same regional frame?

### 3. Where do both overlap?

Where does the transition problem become a land-use and farm affectedness question?

### 4. What does this imply?

Which transition pathways are plausible enough to discuss, without claiming suitability?

Possible interpretation categories:

- `Schützen und stabilisieren`
- `Wiedervernässen und extensivieren`
- `Nasse Nutzung entwickeln`
- `Nutzung und Flächenorganisation neu ordnen`
- `Förder- und Wertschöpfungsketten prüfen`

## 8. Data hierarchy

Preferred data hierarchy:

1. Best available official or project-compatible soil/moor layer
2. Best available official agricultural land-use layer
3. County boundaries for the four SOLAMO districts
4. Derived intersection layer
5. Aggregated district indicators

Do not use confidential farm-level data for the public prototype.

## 9. Method boundaries

The regional module must explicitly avoid overclaiming.

Never write:

- suitable for rewetting,
- priority area,
- affected farm,
- recommended intervention,
- profitable use concept,
- SOLAMO result.

Preferred wording:

- regional context,
- land-use and soil-context overlap,
- possible implementation attention,
- potential farm affectedness,
- transition question,
- basis for further analysis.

## 10. Relation to LUBW Moorschutzprogramm

The LUBW Moorschutzprogramm provides the state-level framework for moor protection, renaturation, planning and implementation. It is useful as the policy and planning context.

Relevant conceptual anchors:

- Moorschutzkonzeption bundles sectoral goals and instruments.
- Moor protection is linked to nature conservation, soil protection, climate protection, water management, agriculture and forestry.
- The Moorkataster is a key information basis.
- Implementation requires regional prioritisation, coordination, funding and stakeholder involvement.

## 11. Relation to SOLAMO-BW

SOLAMO-BW provides the socio-economic implementation logic.

Relevant conceptual anchors:

- farm affectedness,
- regional farm patterns,
- alternative use concepts,
- interviews,
- stakeholder workshops,
- value chains,
- economic modelling,
- climate performance,
- farm-level consequences,
- policy recommendations.

## 12. Recommended page evolution

Next visible page evolution:

```text
Current:
Problem -> Kartenfolge -> Regionale Umsetzung -> Pfade -> Methode

Future:
Problem -> Kartenfolge -> Oberschwaben implementation map -> Betroffenheit -> Nutzungspfade -> Politik-/Förderfrage -> Methode
```

## 13. Recommended next technical step

B93 should prepare the map workflow, not bind anything to the website yet.

B93 should create:

- `public/maps/oberschwaben/README.md`
- export specifications for 16:9 PNGs
- layer naming convention
- required data checklist
- ArcGIS/QGIS workflow
- expected output PNG names
- QA checks for PNG size/alpha/reference
