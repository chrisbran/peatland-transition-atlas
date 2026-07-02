from pathlib import Path
from datetime import date
import csv
import json
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
PROTOTYPE = ROOT / "docs" / "prototypes" / "B165_flagship_sticky_zoom_prototype.html"

SCRIPT = ROOT / "scripts" / "168_sticky_zoom_integration_plan.py"
DOC = ROOT / "docs" / "B168_sticky_zoom_integration_plan.md"
STATE_PLAN = ROOT / "docs" / "B168_live_sticky_zoom_state_plan.csv"
IMPLEMENTATION = ROOT / "docs" / "B168_b169_implementation_brief.md"
AUDIT = ROOT / "docs" / "B168_sticky_zoom_integration_plan_audit.txt"
DONE = ROOT / "tasks" / "done.md"

TARGET_STATES = [
    {
        "order": 1,
        "state": "global-peat",
        "title": "Kleine Fläche, große Wirkung",
        "base": "public/maps/global/global_gpm2_peat_extent.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "integration_action": "keep_or_map_existing",
        "live_role": "opening geography",
        "copy_goal": "Moore räumlich zeigen, noch ohne Drucklogik.",
    },
    {
        "order": 2,
        "state": "global-pressure-total",
        "title": "Wo ist der gesamte Emissionsdruck hoch?",
        "base": "public/maps/global/global_hotspots_total.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "integration_action": "add_or_split_from_existing_pressure_step",
        "live_role": "absolute pressure",
        "copy_goal": "Gesamtmenge als eigene Aussage zeigen.",
    },
    {
        "order": 3,
        "state": "global-pressure-density",
        "title": "Wo ist der Druck pro Fläche besonders hoch?",
        "base": "public/maps/global/global_hotspots_density.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "integration_action": "add_or_restore_density_step",
        "live_role": "intensity per area",
        "copy_goal": "Intensität klar von Gesamtmenge trennen.",
    },
    {
        "order": 4,
        "state": "europe-bridge",
        "title": "Aus Relevanz wird Planung",
        "base": "public/maps/europe/europe_gpm2_peat_extent.png",
        "overlay": "public/maps/europe/europe_country_borders.png",
        "integration_action": "map_to_existing_europe_step",
        "live_role": "scale bridge",
        "copy_goal": "Vom globalen Kontext in den politischen Bezugsraum führen.",
    },
    {
        "order": 5,
        "state": "germany-extent",
        "title": "Die nationale Karte zeigt, wo genauer hingesehen werden muss",
        "base": "public/maps/germany/germany_thuenen_moor_extent.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "integration_action": "map_to_existing_germany_extent_state",
        "live_role": "national planning frame",
        "copy_goal": "Organische Böden als nationale Kulisse zeigen.",
    },
    {
        "order": 6,
        "state": "germany-types",
        "title": "Nicht jeder Moorboden stellt dieselbe Frage",
        "base": "public/maps/germany/germany_thuenen_moor_types.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "integration_action": "map_to_existing_germany_types_state",
        "live_role": "national differentiation",
        "copy_goal": "Typenunterschiede zeigen, aber nicht im Detail erklären.",
    },
    {
        "order": 7,
        "state": "baden-wuerttemberg",
        "title": "Jetzt wird die Frage regional",
        "base": "public/maps/bw/bw_bk50_moor_extent.png",
        "overlay": "public/maps/bw/bw_admin_context.png",
        "integration_action": "add_or_restore_bw_state",
        "live_role": "regional bridge",
        "copy_goal": "BW als Maßstab zwischen Deutschland und Oberschwaben wieder herstellen.",
    },
    {
        "order": 8,
        "state": "oberschwaben-handoff",
        "title": "Hier trifft Moorschutz auf Landwirtschaft",
        "base": "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
        "overlay": "public/maps/oberschwaben/oberschwaben_admin_context.png",
        "integration_action": "handoff_only_not_full_regional_story",
        "live_role": "handoff to existing Oberschwaben section",
        "copy_goal": "Nicht Felt ersetzen; nur zur bestehenden regionalen Story übergeben.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def extract_attrs(tag: str) -> dict[str, str]:
    attrs = {}
    for m in re.finditer(r'([a-zA-Z0-9_\-:]+)\s*=\s*"([^"]*)"', tag):
        attrs[m.group(1)] = m.group(2)
    for m in re.finditer(r"([a-zA-Z0-9_\-:]+)\s*=\s*'([^']*)'", tag):
        attrs[m.group(1)] = m.group(2)
    return attrs


def collect_index_states(html: str) -> list[str]:
    states = set()
    # data-state and data-central-state style attributes
    for attr in ["data-state", "data-central-state", "data-map-state", "data-layer-state"]:
        for m in re.finditer(attr + r'\s*=\s*"([^"]+)"', html):
            states.add(m.group(1))
        for m in re.finditer(attr + r"\s*=\s*'([^']+)'", html):
            states.add(m.group(1))
    # string states in JS classes/functions can still be useful as weak evidence
    for known in [
        "global-peat",
        "global-pressure",
        "global-pressure-total",
        "global-pressure-density",
        "europe-peat",
        "europe-bridge",
        "germany-thuenen-extent",
        "germany-thuenen-types",
        "germany-extent",
        "germany-types",
        "baden-wuerttemberg",
        "oberschwaben-handoff",
    ]:
        if known in html:
            states.add(known)
    return sorted(states)


def extract_prototype_steps(html: str) -> list[dict]:
    m = re.search(r'<script[^>]*id="b165-data"[^>]*>(.*?)</script>', html, re.I | re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def asset_exists(path: str) -> bool:
    return bool(path) and (ROOT / path).exists()


def state_presence(target_state: str, index_states: list[str], proto_states: list[str]) -> tuple[bool, bool, str]:
    aliases = {
        "global-pressure-total": ["global-pressure", "global-pressure-total"],
        "europe-bridge": ["europe-bridge", "europe-peat"],
        "germany-extent": ["germany-extent", "germany-thuenen-extent"],
        "germany-types": ["germany-types", "germany-thuenen-types"],
    }
    names = aliases.get(target_state, [target_state])
    in_index = any(name in index_states for name in names)
    in_proto = target_state in proto_states
    matched = ", ".join([name for name in names if name in index_states]) if in_index else ""
    return in_index, in_proto, matched


def update_done(done_text: str, today: str) -> str:
    line = f"- B168 sticky zoom integration plan: planned how to integrate the repaired B167b sticky-zoom logic into the existing dark central map story without replacing the stable main page structure ({today})."
    if "B168 sticky zoom integration plan" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    index_text = read(INDEX) if INDEX.exists() else ""
    proto_text = read(PROTOTYPE) if PROTOTYPE.exists() else ""

    index_states = collect_index_states(index_text)
    proto_steps = extract_prototype_steps(proto_text)
    proto_states = [s.get("state", "") for s in proto_steps]

    central_story_indicators = {
        "central_global_map_story": "central_global_map_story" in index_text,
        "src/central_global_map_story.js": "src/central_global_map_story.js" in index_text,
        "central_layer_state_hardener": "central_layer_state_hardener" in index_text,
        "central_step_state_bridge": "central_step_state_bridge" in index_text,
        "central_stage_label_fix": "central_stage_label_fix" in index_text,
        "data-state_count": index_text.count("data-state"),
    }

    rows = []
    for state in TARGET_STATES:
        in_index, in_proto, matched_index = state_presence(state["state"], index_states, proto_states)
        rows.append({
            "order": state["order"],
            "target_state": state["state"],
            "title": state["title"],
            "base": state["base"],
            "base_exists": asset_exists(state["base"]),
            "overlay": state["overlay"],
            "overlay_exists": asset_exists(state["overlay"]),
            "present_in_index_or_alias": in_index,
            "index_alias_match": matched_index,
            "present_in_b167b_prototype": in_proto,
            "integration_action": state["integration_action"],
            "live_role": state["live_role"],
            "copy_goal": state["copy_goal"],
        })

    with STATE_PLAN.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "order",
                "target_state",
                "title",
                "base",
                "base_exists",
                "overlay",
                "overlay_exists",
                "present_in_index_or_alias",
                "index_alias_match",
                "present_in_b167b_prototype",
                "integration_action",
                "live_role",
                "copy_goal",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    present_proto_count = sum(1 for r in rows if r["present_in_b167b_prototype"])
    present_index_count = sum(1 for r in rows if r["present_in_index_or_alias"])
    assets_ok = all(r["base_exists"] and r["overlay_exists"] for r in rows)

    doc = f"""# B168 - Sticky Zoom Integration Plan

Date: {today}

## Ziel

B168 plant die Integration des reparierten B167b-Sticky-Zooms in die bestehende Hauptseite.

Wichtig: B168 ist **kein** Seitenumbau. Der Patch dokumentiert, wie B169 später sauber integriert werden soll.

## Leitentscheidung

```text
Nicht den Prototyp-HTML-Block in die Hauptseite kopieren.
Die bestehende dunkle zentrale Kartenbühne behalten und mit der B167b-State-Logik verdichten.
```

Warum:

- die aktuelle Hauptseiten-Kartenstory ist technisch stabil
- die dunkle Bühne wirkt bereits hochwertig
- B165/B167b lösen die State- und Layerlogik
- die Integration soll bestehende Controller nutzen, nicht eine zweite Scrolly-Architektur einführen

## Zielsequenz

| Nr. | State | Aussage | Basis | Overlay |
|---:|---|---|---|---|
"""
    for row in rows:
        doc += f"| {row['order']} | `{row['target_state']}` | {row['title']} | `{row['base']}` | `{row['overlay']}` |\n"

    doc += f"""
## Status

- Zielstates im B167b-Prototyp vorhanden: {present_proto_count}/{len(rows)}
- Zielstates oder Aliase in `index.html` vorhanden: {present_index_count}/{len(rows)}
- Zielassets vorhanden: {assets_ok}

## Integrationsprinzip für B169

### 1. Bestehende zentrale Kartenstory verwenden

B169 soll die vorhandene zentrale Story verdichten:

```text
bestehender dunkler Scrolly → neue 8-Step-State-Matrix
```

Nicht:

```text
B165-Prototyp als neuen zweiten Sticky-Block einfügen
```

### 2. State-Aliase sauber auflösen

Einige alte States heißen anders:

| Zielstate | mögliche bestehende Aliase |
|---|---|
| `global-pressure-total` | `global-pressure` |
| `europe-bridge` | `europe-peat` |
| `germany-extent` | `germany-thuenen-extent` |
| `germany-types` | `germany-thuenen-types` |

B169 sollte entweder:

- alte Aliase beibehalten und sauber mappen, oder
- alles auf die neue State-Nomenklatur umstellen.

Empfehlung:

```text
Neue State-Namen verwenden, aber JS robust gegen alte Aliase halten.
```

### 3. Karte und Text gemeinsam kürzen

Die zentrale Kartenfolge soll nicht nur technisch neue States bekommen.
Sie soll editorial kürzer werden:

```text
aktuelle längere Kartenstory → 8 starke Steps
```

### 4. Oberschwaben bleibt Übergabe, nicht Ersatz

Der letzte Step `oberschwaben-handoff` ist nur die Brücke zur bestehenden regionalen Story.

Er darf nicht ersetzen:

- die statische Oberschwaben-Layerkarte
- den Felt-Block
- die Flächenbilanz

### 5. Mobile nicht überlasten

Desktop darf Sticky bleiben.
Mobile sollte eine einfache vertikale Sequenz bekommen oder die bestehende mobile Fallback-Logik behalten.

## B169-Gates

B169 darf erst umgesetzt werden, wenn diese Punkte akzeptiert sind:

1. 8 Steps sind rhythmisch noch tragbar.
2. Total- und Density-Karte bleiben beide, oder eine wird bewusst gestrichen.
3. BW-Step bleibt als eigene Brücke.
4. Oberschwaben-Step nutzt ausschließlich passende regionale Grenzen.
5. B58 bleibt PASS.
6. B103b zeigt keine sichtbaren Findings.

## Nicht-Ziele für B169

- kein Felt-Umbau
- keine neue Datenquelle
- keine MapLibre-Migration
- kein Löschen der regionalen Oberschwaben-Story
- keine Änderung an Wertschöpfungs-Scorecard
- kein `git add .`

## Dateien

- `docs/B168_live_sticky_zoom_state_plan.csv`
- `docs/B168_b169_implementation_brief.md`
"""
    write(DOC, doc)

    implementation = f"""# B168 - B169 Implementation Brief

Date: {today}

## Ziel für B169

Die bestehende zentrale Kartenstory in der Hauptseite soll auf die B167b-Zielmatrix gebracht werden.

## Vorbereitende Analyse

### Index-Indikatoren

| Indikator | Wert |
|---|---:|
"""
    for key, value in central_story_indicators.items():
        implementation += f"| `{key}` | {value} |\n"

    implementation += """
### Gefundene Index-States / Aliase

```text
"""
    implementation += "\n".join(index_states) if index_states else "(keine States gefunden)"
    implementation += """
```

### B167b-Prototyp-States

```text
"""
    implementation += "\n".join(proto_states) if proto_states else "(keine Prototyp-States gefunden)"
    implementation += """
```

## Empfohlene B169-Strategie

### Schritt 1: Backup vermeiden, aber Patch idempotent machen

B169 soll keine `_backup_before_*`-Ordner erzeugen.
Der Patch muss vorhandene B169-Blöcke entfernen/ersetzen können.

### Schritt 2: Zentrale Section finden

Suchanker:

```text
central_global_map_story
Moore sind räumlich konzentriert
data-state
global_gpm2_peat_extent
```

### Schritt 3: Step-Texte auf 8 Steps ersetzen

Neue Live-Texte:

| Nr. | Kicker | Titel |
|---:|---|---|
| 01 | Welt | Kleine Fläche, große Wirkung |
| 02 | Gesamt | Wo ist der gesamte Emissionsdruck hoch? |
| 03 | Intensität | Wo ist der Druck pro Fläche besonders hoch? |
| 04 | Europa | Aus Relevanz wird Planung |
| 05 | Deutschland | Die nationale Karte zeigt, wo genauer hingesehen werden muss |
| 06 | Bodenkontext | Nicht jeder Moorboden stellt dieselbe Frage |
| 07 | Baden-Württemberg | Jetzt wird die Frage regional |
| 08 | Oberschwaben | Hier trifft Moorschutz auf Landwirtschaft |

### Schritt 4: State-to-layer-Mapping in JS/CSS prüfen

B169 muss sicherstellen:

```text
global-peat              -> global_gpm2_peat_extent + global_country_borders
global-pressure-total    -> global_hotspots_total + global_country_borders
global-pressure-density  -> global_hotspots_density + global_country_borders
europe-bridge            -> europe_gpm2_peat_extent + europe_country_borders
germany-extent           -> germany_thuenen_moor_extent + germany_admin_context
germany-types            -> germany_thuenen_moor_types + germany_admin_context
baden-wuerttemberg       -> bw_bk50_moor_extent + bw_admin_context
oberschwaben-handoff     -> oberschwaben_agriculture_moor_intersection + oberschwaben_admin_context
```

### Schritt 5: QA

Nach B169:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Manuell:

- Desktop Scrolly komplett durchscrollen
- Mobile 390px prüfen
- Total/Density unterscheidbar
- BW-Step sichtbar
- Oberschwaben-Step nicht mit Deutschland-Grenzen
- Übergang zur bestehenden Oberschwaben-Section ohne Dopplung

## Entscheidungsfrage vor B169

Acht Steps sind fachlich sauber.
Falls es beim Scrollen zu lang wirkt, gibt es zwei Kürzungsvarianten:

### Variante A - Total streichen

```text
global-pressure-density bleibt
global-pressure-total entfällt
```

Vorteil: kürzer, stärker flächenbezogen.

### Variante B - Germany types streichen

```text
germany-extent bleibt
germany-types entfällt
```

Vorteil: Maßstabssprung bleibt erhalten, weniger nationale Detailtiefe.

## Empfehlung

Für den ersten Live-Integrationsprototyp: alle 8 Steps testen.
Danach auf 7 kürzen, falls der Rhythmus bricht.
"""
    write(IMPLEMENTATION, implementation)

    audit = f"""# B168 sticky zoom integration plan audit

Date: {today}

Result: PLAN ONLY. No public page files changed.

Inputs:
- index.html exists: {INDEX.exists()}
- B167b/B165 prototype exists: {PROTOTYPE.exists()}

Central story indicators:
"""
    for key, value in central_story_indicators.items():
        audit += f"- {key}: {value}\n"

    audit += f"""
Target states:
- total: {len(rows)}
- present in B167b prototype: {present_proto_count}
- present in index/aliases: {present_index_count}
- target assets all present: {assets_ok}

Created/updated:
- docs/B168_sticky_zoom_integration_plan.md
- docs/B168_live_sticky_zoom_state_plan.csv
- docs/B168_b169_implementation_brief.md
- docs/B168_sticky_zoom_integration_plan_audit.txt
- tasks/done.md

Recommended next patch: B169 Live Sticky Zoom Integration Prototype
"""
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B168 sticky zoom integration plan complete.")
    print("Plan only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B168_sticky_zoom_integration_plan.md")
    print("  docs/B168_live_sticky_zoom_state_plan.csv")
    print("  docs/B168_b169_implementation_brief.md")
    print("  docs/B168_sticky_zoom_integration_plan_audit.txt")
    print("  tasks/done.md")
    print("Recommended next patch: B169 Live Sticky Zoom Integration Prototype")


if __name__ == "__main__":
    main()
