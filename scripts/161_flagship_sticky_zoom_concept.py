from pathlib import Path
from datetime import date
import csv
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
B160_PLAN = ROOT / "docs" / "B160_narrative_cut_plan.md"
B160_OUTLINE = ROOT / "docs" / "B160_main_flow_outline.md"

SCRIPT = ROOT / "scripts" / "161_flagship_sticky_zoom_concept.py"
DOC = ROOT / "docs" / "B161_flagship_sticky_zoom_concept.md"
STORYBOARD = ROOT / "docs" / "B161_flagship_sticky_zoom_storyboard.md"
IMPLEMENTATION = ROOT / "docs" / "B161_flagship_sticky_zoom_implementation_brief.md"
ASSETS = ROOT / "docs" / "B161_flagship_sticky_zoom_asset_inventory.csv"
AUDIT = ROOT / "docs" / "B161_flagship_sticky_zoom_concept_audit.txt"
DONE = ROOT / "tasks" / "done.md"

MAP_ASSET_CANDIDATES = [
    ("global_peat_extent", "public/maps/global/global_gpm2_peat_extent.png", "Global peat extent", "A1/A2 opening geography"),
    ("global_hotspots_total", "public/maps/global/global_hotspots_total.png", "Global hotspots total", "A2 pressure / concentration"),
    ("global_hotspots_density", "public/maps/global/global_hotspots_density.png", "Global hotspots density", "A2 intensity / contrast"),
    ("global_country_borders", "public/maps/global/global_country_borders.png", "Country borders", "reference overlay"),
    ("europe_peat_extent", "public/maps/europe/europe_gpm2_peat_extent.png", "Europe peat extent", "scale bridge"),
    ("europe_country_borders", "public/maps/europe/europe_country_borders.png", "Europe country borders", "reference overlay"),
    ("germany_admin_context", "public/maps/germany/germany_admin_context.png", "Germany admin context", "national focus"),
    ("germany_thuenen_extent", "public/maps/germany/germany_thuenen_moor_extent.png", "Germany organic soils extent", "national organic soils"),
    ("germany_thuenen_types", "public/maps/germany/germany_thuenen_moor_types.png", "Germany organic soils types", "national type context"),
]

OPTIONAL_PATTERNS = [
    ("bw", "public/maps/bw"),
    ("oberschwaben", "public/maps/oberschwaben"),
    ("regional", "public/maps/regional"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def count_in_file(path: Path, patterns: list[str]) -> dict[str, int]:
    if not path.exists():
        return {p: 0 for p in patterns}
    text = read(path)
    return {p: len(re.findall(re.escape(p), text, flags=re.I)) for p in patterns}


def update_done(done_text: str, today: str) -> str:
    line = f"- B161 flagship sticky zoom concept: designed the premium one-earned-sticky map zoom concept from global relevance to Oberschwaben proof point ({today})."
    if "B161 flagship sticky zoom concept" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    index_exists = INDEX.exists()
    b160_plan_exists = B160_PLAN.exists()
    b160_outline_exists = B160_OUTLINE.exists()

    inventory = []
    for asset_id, rel, label, use in MAP_ASSET_CANDIDATES:
        p = ROOT / rel
        inventory.append({
            "asset_id": asset_id,
            "path": rel,
            "exists": p.exists(),
            "size_bytes": p.stat().st_size if p.exists() else "",
            "label": label,
            "proposed_use": use,
        })

    optional_found = []
    for name, rel_dir in OPTIONAL_PATTERNS:
        p = ROOT / rel_dir
        if p.exists():
            files = sorted([x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}])
            optional_found.append((name, rel_dir, len(files), [str(x.as_posix()) for x in files[:12]]))
        else:
            optional_found.append((name, rel_dir, 0, []))

    with ASSETS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["asset_id", "path", "exists", "size_bytes", "label", "proposed_use"])
        writer.writeheader()
        writer.writerows(inventory)

    index_counts = count_in_file(INDEX, [
        "central_global_map_story",
        "data-state",
        "oberschwaben",
        "felt",
        "Methode in Kürze",
    ])

    concept = f"""# B161 - Flagship Sticky Zoom Concept

Date: {today}

## Ziel

B161 konzipiert den einen großen, verdienten Sticky-Moment der V2.

Der bisherige Atlas ist fachlich stabil, aber noch zu sehr eine Abfolge richtiger Abschnitte.
Ein Premium-Feature braucht einen klaren visuellen Sog: Die Lesenden sollen nicht nur verstehen,
dass Moorbodenschutz räumlich differenziert ist. Sie sollen es beim Scrollen sehen.

## Leitidee

```text
Vom globalen Klimathema zur regionalen Nutzungsfrage.
```

Oder als redaktioneller Satz:

```text
Das Problem beginnt global. Handlungsfähig wird es erst lokal.
```

## Rolle im Fünf-Akt-Bogen

Der Sticky-Zoom ist **Akt 2** der Seite:

1. Hook: Moore sind klein, aber klimatisch groß.
2. **Flagship Sticky Zoom: Karten zeigen den Maßstabssprung.**
3. Oberschwaben: Moorbodenschutz trifft reale Nutzung.
4. Aus Schnittmenge folgt Verhandlung.
5. Der Engpass liegt hinter dem Feld.

## Kernproblem des aktuellen Stands

Die vorhandene Kartenfolge ist informativ, aber editorial noch listenartig:

```text
Karte 1 erklärt etwas.
Karte 2 erklärt etwas.
Karte 3 erklärt etwas.
...
```

Der Premium-Moment muss dagegen so wirken:

```text
Eine einzige Frage wird räumlich immer konkreter.
```

## Zielbild

Ein großer Sticky-Block, links kurze Scrollsteps, rechts eine ruhige Kartenbühne:

```text
[Scrolltext]        [Sticky map stage]
01 Global           Weltkarte
02 Druck            Hotspot / Emissionsdruck
03 Europa/Deutschl. Maßstab wird politisch
04 Deutschland      organische Böden als Planungskulisse
05 Baden-Württemberg regionale Zuständigkeit
06 Oberschwaben     konkrete Nutzungsfrage
```

Der Abschnitt endet nicht mit einer weiteren Karte, sondern mit der Übergabe:

```text
Jetzt wird aus Klima eine Nutzungsfrage.
```

## Nicht-Ziel

B161 fordert keine neuen Datenlayer.

Der erste Premium-Schritt ist Choreografie, nicht Datenbeschaffung:

- vorhandene Global-/Europa-/Deutschland-Karten stärker inszenieren
- Oberschwaben erst als Zielpunkt verwenden
- Felt bleibt anschließend interaktive Vertiefung, nicht Teil des Sticky-Zooms
- Mobile bekommt eine vereinfachte statische Sequenz, keinen schweren Scrolly-Zwang

## Empfohlener Titel des Sticky-Blocks

```text
Der Maßstab entscheidet
```

Untertitel:

```text
Globale Karten zeigen, warum Moore relevant sind. Regional wird sichtbar, wo Planung beginnt.
```

## Dramaturgische Regeln

1. **Eine Karte, eine Aussage.**
   Kein Schritt darf mehr als einen Gedanken tragen.

2. **Weniger Legende, mehr Annotation.**
   Die Karte soll nicht gelesen werden wie GIS, sondern wie ein Argument.

3. **Nicht alle Daten zeigen.**
   Nur die Ebene zeigen, die für den nächsten Maßstab nötig ist.

4. **Oberschwaben ist nicht Start, sondern Ziel.**
   Die Region wirkt stärker, wenn sie als Endpunkt eines Maßstabssprungs erscheint.

5. **Kein Methodenblock im Sticky-Moment.**
   Quellenzeile knapp, Details unten.

## Textprinzip

Der Sticky-Text muss knapper werden als bisher.

Maximal pro Step:

- 1 Mini-Kicker
- 1 starker Satz
- optional 1 Halbsatz Erklärung

Beispiel:

```text
01
Kleine Fläche, große Wirkung.
Moore nehmen wenig Raum ein – aber sie verändern die Klimabilanz ganzer Landschaften.
```

## Mobile-Prinzip

Auf Mobile kein komplexer Sticky-Zwang.

Empfehlung:

```text
Desktop:
echter Sticky-Zoom

Mobile:
vertikale Kartenfolge mit 4–5 statischen Panels
```

Die mobile Version darf weniger interaktiv sein, aber sie muss schnell und klar bleiben.

## Entscheidung

Der Flagship-Zoom soll die bestehende globale Kartenfolge nicht einfach erweitern,
sondern perspektivisch ersetzen oder stark verdichten.

Die vorhandene Felt-Karte bleibt davon getrennt:

- Sticky-Zoom = Maßstabssprung
- statische Oberschwaben-Karte = Layerlogik
- Felt = interaktive regionale Vertiefung
- Flächenbilanz = quantitative Verdichtung
"""

    write(DOC, concept)

    storyboard = f"""# B161 - Flagship Sticky Zoom Storyboard

Date: {today}

## Arbeitstitel

```text
Der Maßstab entscheidet
```

## Storyboard V1

| Step | Bühnenbild | Textfunktion | Sichtbarer Textvorschlag | Karten-/Grafiklogik |
|---:|---|---|---|---|
| 00 | Dunkle/ruhige Kartenbühne, globale Konturen | Einstieg | `Moorbodenschutz beginnt als Klimathema.` | Weltkarte sehr reduziert, noch ohne Detaildruck |
| 01 | Globale Moorverbreitung | Relevanz | `Kleine Fläche, große Wirkung.` | Global Peatland Map 2.0; Moore als konzentrierte Flächen |
| 02 | Hotspot-/Druckebene | Druck | `Der Druck ist räumlich ungleich verteilt.` | Hotspots total oder density; nur wenige visuelle Schwerpunkte |
| 03 | Europa/Deutschland rückt ins Bild | Maßstab | `Aus globaler Relevanz wird politische Planung.` | Europa-/Deutschland-Kontext, Grenzen sehr zurückhaltend |
| 04 | Deutschland organische Böden | nationale Kulisse | `Die nationale Karte zeigt, wo genauer hingesehen werden muss.` | Thünen-Kulisse organischer Böden |
| 05 | Baden-Württemberg / Süddeutschland | regionale Konkretisierung | `In Baden-Württemberg wird die Frage regional.` | BW/Region als Zielausschnitt; falls Asset fehlt, mit vorhandener Deutschlandkarte + Annotation |
| 06 | Oberschwaben als Fokus | Übergabe | `In Oberschwaben trifft Moorbodenschutz auf Nutzung.` | Übergang zur bestehenden Oberschwaben-Storykarte, nicht Felt |
| 07 | Textübergabe | Abschluss | `Jetzt beginnt die eigentliche Planungsfrage.` | Karte blendet in den regionalen Abschnitt aus |

## Premium-Redaktion

Der Abschnitt soll nicht erklären, dass es mehrere Datenquellen gibt.
Er soll zeigen, dass die gleiche Frage auf jedem Maßstab anders aussieht.

## Kürzungsziel gegenüber aktueller Kartenfolge

- bestehende mehrteilige Kartenliste um 30–50 % Text reduzieren
- Methodik in eine einzige Quellenzeile plus Methodenteil verschieben
- Step-Zahl ideal: 5–7, nicht 10+

## Starkes Schlussbild

Der letzte Step darf nicht nach Dateninventar aussehen.
Er muss als Übergabe funktionieren:

```text
Die Karte zeigt nicht die Lösung.
Sie zeigt, wo die Verhandlung beginnt.
```

## Offene Designentscheidung

Variante A: vorhandene PNG-Stages nutzen  
Schneller, robust, näher an aktuellem Code.

Variante B: neue statische Kartenexports bauen  
Visuell stärker, aber höherer Aufwand.

Variante C: MapLibre/Vektor später  
Nicht für diese Schleife. Zu groß, solange Story/Pacing noch offen sind.

## Empfehlung

Für V2: **Variante A+**.

Das heißt:

- vorhandene PNG-Stages nutzen
- Step-Texte radikal kürzen
- Labels/Annotationen neu setzen
- Übergang nach Oberschwaben stärker inszenieren
- später nur gezielt einzelne Karten neu exportieren, falls visuell nötig
"""

    write(STORYBOARD, storyboard)

    implementation = f"""# B161 - Flagship Sticky Zoom Implementation Brief

Date: {today}

## Ziel des späteren Umsetzungspatches

Ein späterer Umsetzungspatch soll die vorhandene zentrale Kartenfolge zu einem Premium-Sticky-Zoom verdichten.

B161 selbst ändert die öffentliche Seite nicht.

## Wahrscheinliche Umsetzungsstrategie

### Phase 1: Inventarisieren und verdichten

- vorhandene `central_global_map_story`-Struktur prüfen
- aktuelle Steps und States auf 5–7 reduzieren
- keine neuen Datenquellen
- keine zusätzliche Kartenbibliothek

### Phase 2: Copy und Step-Logik

Zielstruktur:

```text
00 intro
01 global peat extent
02 global pressure/hotspot
03 europe/germany bridge
04 germany organic soils
05 Baden-Württemberg / regional focus
06 Oberschwaben handoff
```

### Phase 3: Bühnenbild

- Sticky-Stage bleibt groß
- Textspalte wird knapper
- Stage-Labels werden stärker statement-orientiert
- Quellenzeile wird ruhiger
- kein Methodenabschnitt mitten im Sticky

### Phase 4: Mobile

Mobile darf keine schwere Sticky-Mechanik erzwingen.

Mögliche Regel:

```css
@media (max-width: 760px) {{
  /* Sticky aus, Kartenpanels sequenziell */
}}
```

## Existing asset inventory

Die Datei `docs/B161_flagship_sticky_zoom_asset_inventory.csv` listet die verfügbaren Kartenassets.

Kurzstatus:

| Asset | Status |
|---|---:|
"""
    for item in inventory:
        implementation += f"| `{item['path']}` | {'vorhanden' if item['exists'] else 'fehlt'} |\n"

    implementation += """
## Optional gefundene regionale Asset-Verzeichnisse

"""
    for name, rel_dir, count, files in optional_found:
        implementation += f"### `{rel_dir}`\n\n"
        implementation += f"- gefundene Bilddateien: {count}\n"
        if files:
            for fp in files:
                implementation += f"- `{fp}`\n"
        implementation += "\n"

    implementation += """## Technische Vorsicht

Nicht sofort `index.html` hart umbauen.

Empfohlene Reihenfolge:

```text
B161 Konzept
B162 Wertschöpfungs-Climax-Konzept
B163 Caveat-Reduction
B164 Premium-Pacing
B165 erst dann: Flagship-Zoom-Prototyp
```

Warum: Der Sticky-Zoom muss zur gekürzten Dramaturgie passen. Wenn wir ihn zu früh bauen,
zementieren wir eventuell die aktuelle Überfülle.

## QA-Anforderungen für späteren Umsetzungspatch

- B103b visible findings: 0
- B58 PASS
- Desktop: Sticky-Stage sauber
- Mobile: kein blockierendes Scrollytelling
- keine neuen raw GIS-Dateien
- kein `git add .`
"""

    write(IMPLEMENTATION, implementation)

    audit_text = f"""# B161 flagship sticky zoom concept audit

Date: {today}

Result: CONCEPT ONLY. No public page files changed.

Inputs detected:

- index.html exists: {index_exists}
- docs/B160_narrative_cut_plan.md exists: {b160_plan_exists}
- docs/B160_main_flow_outline.md exists: {b160_outline_exists}

Index indicators:

- central_global_map_story: {index_counts.get('central_global_map_story', 0)}
- data-state: {index_counts.get('data-state', 0)}
- oberschwaben: {index_counts.get('oberschwaben', 0)}
- felt: {index_counts.get('felt', 0)}
- Methode in Kürze: {index_counts.get('Methode in Kürze', 0)}

Created/updated:

- docs/B161_flagship_sticky_zoom_concept.md
- docs/B161_flagship_sticky_zoom_storyboard.md
- docs/B161_flagship_sticky_zoom_implementation_brief.md
- docs/B161_flagship_sticky_zoom_asset_inventory.csv
- docs/B161_flagship_sticky_zoom_concept_audit.txt
- tasks/done.md

Recommended next patch: B162 Value-Chain Visual Climax Redesign
"""

    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B161 flagship sticky zoom concept complete.")
    print("Concept only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B161_flagship_sticky_zoom_concept.md")
    print("  docs/B161_flagship_sticky_zoom_storyboard.md")
    print("  docs/B161_flagship_sticky_zoom_implementation_brief.md")
    print("  docs/B161_flagship_sticky_zoom_asset_inventory.csv")
    print("  docs/B161_flagship_sticky_zoom_concept_audit.txt")
    print("  tasks/done.md")
    print("Recommended next patch: B162 Value-Chain Visual Climax Redesign")


if __name__ == "__main__":
    main()
