# B74 - Sichtbarer Textaudit Deutsch

Date: 2026-06-23

## 1. Zweck

B74 bereitet die deutsche Vorzeigefassung vor. Der Audit extrahiert sichtbare Texte aus `index.html`, ignoriert retired/hidden sections und markiert Texte, die für die deutsche Präsentationsfassung überarbeitet werden müssen.

B74 verändert keine Anwendungsdateien.

## 2. Zielbild aus B73

- Zielgruppe: wissenschaftlich informierte Praxisakteure
- Tonalität: narrativ vermittelnd
- Umfang: kurz und pointiert
- Prinzip: Form follows function

## 3. Audit-Zusammenfassung

- Sichtbare Textelemente: 187
- Hohe Priorität: 93
- Vermutlich Englisch: 52
- Meta-/Toolsprache: 31
- Methodische Boundary prüfen: 7
- Zu lang / zu erklärend: 2

## 4. Wichtigste High-Priority-Funde

- `` / `p` — Portfolio prototype · Literature-driven MVP [meta_tool_language]
- `` / `h1` — Peatland Transition Atlas [meta_tool_language]
- `` / `a` — Story [meta_tool_language]
- `` / `a` — Hotspots [no flags]
- `` / `a` — Evidence Map [no flags]
- `` / `a` — Pathways [no flags]
- `` / `a` — South Germany Fit [no flags]
- `` / `a` — Method [no flags]
- `` / `a` — Data [no flags]
- `` / `h2` — The climate problem is spatial. The transition problem is systemic. [probably_english]
- `` / `p` — This prototype turns a curated peatland rewetting literature review into an exploratory atlas: where international evidence comes from, what transition pathways it supports, and which options might be relevant for South German dairy, forage and biogas regions. [probably_english; meta_tool_language; too_long]
- `transitionLogic` / `p` — Atlas framing [meta_tool_language]
- `transitionLogic` / `h2` — From peatland extent to transition priorities [probably_english]
- `transitionLogic` / `p` — This prototype is not a general peatland-awareness atlas. It tests how spatial peatland extent, drained organic-soil emissions, national implementation layers and literature evidence can be linked into a transition-priority workflow. [probably_english; meta_tool_language; method_boundary_check]
- `transitionLogic` / `h3` — Extent [no flags]
- `transitionLogic` / `h3` — Pressure [no flags]
- `transitionLogic` / `h3` — Implementation [no flags]
- `transitionLogic` / `h3` — Pathways [no flags]
- `transitionLogic` / `h3` — What this atlas is [meta_tool_language]
- `transitionLogic` / `p` — A data-visualization and decision-support prototype that connects spatial layers, emissions hotspots, regional implementation constraints and evidence-based transition pathways. [probably_english; meta_tool_language]
- `transitionLogic` / `h3` — What this atlas is not [meta_tool_language]
- `transitionLogic` / `p` — It is not a parcel-level rewetting suitability map, not a substitute for hydrological planning, and not a general educational Mooratlas replica. [meta_tool_language; method_boundary_check]
- `layerProvenance` / `h2` — Each map layer answers a different question [no flags]
- `layerProvenance` / `h3` — Where are peatlands? [no flags]
- `layerProvenance` / `h3` — Where are emissions concentrated? [no flags]
- `layerProvenance` / `h3` — Where do constraints become concrete? [no flags]
- `layerProvenance` / `h3` — What transition pathways are plausible? [probably_english]
- `layerProvenance` / `p` — Literature-derived pathways translate spatial pressure into possible land-use transitions. [method_boundary_check]
- `mvpStoryline` / `p` — Main atlas story [meta_tool_language]
- `mvpStoryline` / `h2` — The map below is the core narrative. [probably_english]

## 5. Prüfkriterien für die manuelle Redaktion

1. Spricht der Text über die Sache oder über das Tool?
2. Ist die Aussage auf Deutsch sofort verständlich?
3. Ist die Formulierung kurz genug für eine Projektvorstellung?
4. Ist die fachliche Grenze korrekt?
5. Hilft der Text der Story oder erklärt er die Website?

## 6. Arbeitstabelle

Siehe `docs/B74_visible_text_inventory.csv`. Die Spalte `rewrite_de` ist bewusst leer und wird im nächsten Schritt kuratiert gefüllt.

## 7. Empfohlener nächster Schritt

`B75_curated_german_copy_deck`

Ziel: deutsche Hauptüberschriften, Übergänge und Kartenstep-Texte kuratieren, bevor Design-Dummies erstellt werden.
