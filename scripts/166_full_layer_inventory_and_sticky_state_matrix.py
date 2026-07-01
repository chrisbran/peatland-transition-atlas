from pathlib import Path
from datetime import date
import csv
import json
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
B165_PROTO = ROOT / "docs" / "prototypes" / "B165_flagship_sticky_zoom_prototype.html"

SCRIPT = ROOT / "scripts" / "166_full_layer_inventory_and_sticky_state_matrix.py"
DOC = ROOT / "docs" / "B166_full_layer_inventory_and_sticky_state_matrix.md"
ASSETS_CSV = ROOT / "docs" / "B166_map_asset_inventory.csv"
MATRIX_CSV = ROOT / "docs" / "B166_sticky_state_matrix.csv"
REPAIR = ROOT / "docs" / "B166_sticky_zoom_repair_recommendations.md"
AUDIT = ROOT / "docs" / "B166_full_layer_inventory_and_sticky_state_matrix_audit.txt"
DONE = ROOT / "tasks" / "done.md"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}

EXPECTED_ASSETS = [
    ("global_peat_extent", "public/maps/global/global_gpm2_peat_extent.png", "global", "base", "global peat extent / GPM2"),
    ("global_hotspots_total", "public/maps/global/global_hotspots_total.png", "global", "base", "absolute emissions pressure / total by country"),
    ("global_hotspots_density", "public/maps/global/global_hotspots_density.png", "global", "base", "emissions intensity per area"),
    ("global_country_borders", "public/maps/global/global_country_borders.png", "global", "overlay", "country borders for global maps"),
    ("europe_peat_extent", "public/maps/europe/europe_gpm2_peat_extent.png", "europe", "base", "European peat extent / GPM2"),
    ("europe_country_borders", "public/maps/europe/europe_country_borders.png", "europe", "overlay", "country borders for Europe maps"),
    ("germany_admin_context", "public/maps/germany/germany_admin_context.png", "germany", "overlay", "German political/admin context"),
    ("germany_thuenen_extent", "public/maps/germany/germany_thuenen_moor_extent.png", "germany", "base", "organic soils / Thünen extent"),
    ("germany_thuenen_types", "public/maps/germany/germany_thuenen_moor_types.png", "germany", "base", "organic soil types / Thünen"),
]

TARGET_STICKY_STATES = [
    {
        "target_order": 1,
        "target_state": "global-peat",
        "target_base": "public/maps/global/global_gpm2_peat_extent.png",
        "target_overlay": "public/maps/global/global_country_borders.png",
        "message": "Kleine Fläche, große Wirkung.",
        "purpose": "global peatland distribution / opening geography",
    },
    {
        "target_order": 2,
        "target_state": "global-pressure-total",
        "target_base": "public/maps/global/global_hotspots_total.png",
        "target_overlay": "public/maps/global/global_country_borders.png",
        "message": "Wo ist der gesamte Emissionsdruck hoch?",
        "purpose": "absolute pressure / total hotspot",
    },
    {
        "target_order": 3,
        "target_state": "global-pressure-density",
        "target_base": "public/maps/global/global_hotspots_density.png",
        "target_overlay": "public/maps/global/global_country_borders.png",
        "message": "Wo ist der Druck pro Fläche besonders intensiv?",
        "purpose": "intensity per area / density hotspot",
    },
    {
        "target_order": 4,
        "target_state": "europe-bridge",
        "target_base": "public/maps/europe/europe_gpm2_peat_extent.png",
        "target_overlay": "public/maps/europe/europe_country_borders.png",
        "message": "Aus globaler Relevanz wird politische Planung.",
        "purpose": "scale bridge from global to European planning context",
    },
    {
        "target_order": 5,
        "target_state": "germany-extent",
        "target_base": "public/maps/germany/germany_thuenen_moor_extent.png",
        "target_overlay": "public/maps/germany/germany_admin_context.png",
        "message": "Die nationale Karte zeigt, wo genauer hingesehen werden muss.",
        "purpose": "national organic soils planning frame",
    },
    {
        "target_order": 6,
        "target_state": "germany-types",
        "target_base": "public/maps/germany/germany_thuenen_moor_types.png",
        "target_overlay": "public/maps/germany/germany_admin_context.png",
        "message": "Nicht jeder Moorboden stellt dieselbe Frage.",
        "purpose": "organic soil type differentiation",
    },
    {
        "target_order": 7,
        "target_state": "oberschwaben-handoff",
        "target_base": "REGIONAL_ASSET_REQUIRED",
        "target_overlay": "MATCHING_REGIONAL_BOUNDARY_REQUIRED_OR_EMBEDDED",
        "message": "Hier trifft Moorschutz auf Landwirtschaft.",
        "purpose": "handoff from scale zoom to regional Oberschwaben story",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def normalize_ref(ref: str) -> str:
    ref = ref.strip()
    ref = ref.split("#")[0].split("?")[0]
    while ref.startswith("../"):
        ref = ref[3:]
    while ref.startswith("./"):
        ref = ref[2:]
    return ref.replace("\\", "/")


def extract_attrs(tag: str) -> dict[str, str]:
    attrs = {}
    for m in re.finditer(r'([a-zA-Z0-9_\-:]+)\s*=\s*"([^"]*)"', tag):
        attrs[m.group(1)] = m.group(2)
    for m in re.finditer(r"([a-zA-Z0-9_\-:]+)\s*=\s*'([^']*)'", tag):
        attrs[m.group(1)] = m.group(2)
    return attrs


def extract_img_refs(html: str) -> list[str]:
    refs = []
    for m in re.finditer(r"<img\b[^>]*>", html, re.I | re.S):
        attrs = extract_attrs(m.group(0))
        if "src" in attrs:
            refs.append(normalize_ref(attrs["src"]))
    return refs


def extract_b165_state_images(html: str) -> tuple[dict[str, str], dict[str, str], list[dict]]:
    base = {}
    boundary = {}

    for m in re.finditer(r"<img\b[^>]*>", html, re.I | re.S):
        attrs = extract_attrs(m.group(0))
        src = normalize_ref(attrs.get("src", ""))
        if not src:
            continue
        if "data-b165-img" in attrs:
            base[attrs["data-b165-img"]] = src
        if "data-b165-boundary" in attrs:
            boundary[attrs["data-b165-boundary"]] = src

    steps = []
    m = re.search(r'<script[^>]*id="b165-data"[^>]*>(.*?)</script>', html, re.I | re.S)
    if m:
        try:
            steps = json.loads(m.group(1))
        except Exception:
            steps = []

    return base, boundary, steps


def infer_scope(path: str) -> str:
    p = path.lower()
    if "/global/" in p:
        return "global"
    if "/europe/" in p:
        return "europe"
    if "/germany/" in p:
        return "germany"
    if "/bw/" in p or "baden" in p or "_bw" in p:
        return "bw"
    if "/oberschwaben/" in p or "oberschwaben" in p:
        return "oberschwaben"
    if "/regional/" in p:
        return "regional"
    return "unknown"


def infer_role(path: str) -> str:
    p = path.lower()
    if "country_borders" in p or "admin_context" in p or "landkreis" in p or "counties" in p or "boundary" in p or "borders" in p:
        return "political_boundary_or_admin_overlay"
    if "hotspots_density" in p or "density" in p or "intensity" in p:
        return "emissions_intensity_per_area"
    if "hotspots_total" in p or "total" in p:
        return "absolute_emissions_pressure"
    if "gpm2" in p or "peat_extent" in p:
        return "peat_extent"
    if "thuenen_moor_extent" in p:
        return "organic_soils_extent"
    if "thuenen_moor_types" in p:
        return "organic_soil_types"
    if "schnitt" in p or "intersection" in p:
        return "regional_intersection"
    if "moor" in p and "feucht" in p:
        return "regional_soil_context"
    return "map_or_image_asset"


def scan_assets() -> list[dict]:
    discovered = {}
    public_maps = ROOT / "public" / "maps"
    if public_maps.exists():
        for p in sorted(public_maps.rglob("*")):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                rel = p.as_posix()
                discovered[rel] = p

    for _, rel, *_ in EXPECTED_ASSETS:
        p = ROOT / rel
        discovered.setdefault(rel, p)

    rows = []
    index_text = read(INDEX) if INDEX.exists() else ""
    proto_text = read(B165_PROTO) if B165_PROTO.exists() else ""
    index_refs = set(extract_img_refs(index_text))
    proto_refs = set(extract_img_refs(proto_text))
    proto_base, proto_boundary, _ = extract_b165_state_images(proto_text)

    for rel in sorted(discovered.keys()):
        p = ROOT / rel
        rows.append({
            "path": rel,
            "exists": p.exists(),
            "size_bytes": p.stat().st_size if p.exists() else "",
            "scope": infer_scope(rel),
            "role": infer_role(rel),
            "referenced_in_index": rel in index_refs,
            "referenced_in_b165_prototype": rel in proto_refs,
            "used_as_b165_base_for_states": "; ".join([s for s, r in proto_base.items() if r == rel]),
            "used_as_b165_boundary_for_states": "; ".join([s for s, r in proto_boundary.items() if r == rel]),
        })

    return rows


def choose_regional_candidates(asset_rows: list[dict]) -> tuple[list[str], list[str]]:
    base_candidates = []
    boundary_candidates = []
    for r in asset_rows:
        if not r["exists"]:
            continue
        scope = r["scope"]
        role = r["role"]
        path = r["path"]
        if scope in {"bw", "oberschwaben", "regional"}:
            if role == "political_boundary_or_admin_overlay":
                boundary_candidates.append(path)
            else:
                base_candidates.append(path)

    return base_candidates, boundary_candidates


def matrix_status(target: dict, current_base: str, current_overlay: str, asset_rows: list[dict]) -> tuple[str, str]:
    existing = {r["path"]: bool(r["exists"]) for r in asset_rows}

    tb = target["target_base"]
    to = target["target_overlay"]

    if tb == "REGIONAL_ASSET_REQUIRED":
        if not current_base:
            return "missing_base", "No current regional base detected for the final handoff."
        current_scope = infer_scope(current_base)
        overlay_scope = infer_scope(current_overlay) if current_overlay else "none"
        if current_scope in {"bw", "oberschwaben", "regional"} and overlay_scope == "germany":
            return "wrongly_paired", "Regional base is paired with Germany-wide admin overlay; use matching regional boundaries or embedded boundaries."
        if current_scope in {"bw", "oberschwaben", "regional"}:
            return "usable_with_review", "Regional base detected; verify that political boundaries match the crop/projection."
        return "needs_regional_export", "Final step needs a BW/Oberschwaben-specific handoff map."

    if not existing.get(tb, False):
        return "missing_asset", f"Target base asset missing: {tb}"
    if to and to not in {"MATCHING_REGIONAL_BOUNDARY_REQUIRED_OR_EMBEDDED"} and not existing.get(to, False):
        return "missing_overlay", f"Target overlay asset missing: {to}"

    if current_base == tb and (not to or current_overlay == to):
        return "ok_current", "Current prototype pairing matches target matrix."

    if target["target_state"] == "global-pressure-total" and current_base == tb:
        return "current_state_name_differs", "Prototype uses total-pressure asset, but state should be split from density for clarity."

    if target["target_state"] == "global-pressure-density" and existing.get(tb, False) and current_base != tb:
        return "available_unused", "Density/intensity map exists but is not currently included in B165."

    return "available_not_current", "Target asset exists but current prototype needs remapping or an additional step."


def build_matrix(asset_rows: list[dict]) -> list[dict]:
    proto_text = read(B165_PROTO) if B165_PROTO.exists() else ""
    current_base, current_overlay, steps = extract_b165_state_images(proto_text)

    # Map old B165 state to split target states where applicable.
    current_lookup = dict(current_base)
    current_overlay_lookup = dict(current_overlay)

    matrix_rows = []
    for target in TARGET_STICKY_STATES:
        state = target["target_state"]
        current_state = state

        if state == "global-pressure-total":
            current_state = "global-pressure"
        elif state == "oberschwaben-handoff":
            current_state = "regional-handoff"

        cb = current_lookup.get(current_state, "")
        co = current_overlay_lookup.get(current_state, "")

        status, issue = matrix_status(target, cb, co, asset_rows)

        matrix_rows.append({
            "target_order": target["target_order"],
            "target_state": state,
            "current_b165_state": current_state if current_state in current_lookup or current_state in current_overlay_lookup else "",
            "target_base": target["target_base"],
            "current_base": cb,
            "target_overlay": target["target_overlay"],
            "current_overlay": co,
            "status": status,
            "issue_or_note": issue,
            "message": target["message"],
            "purpose": target["purpose"],
        })

    return matrix_rows


def update_done(done_text: str, today: str) -> str:
    line = f"- B166 full layer inventory and sticky state matrix: inventoried map assets and documented the complete target state matrix, including density map and regional boundary-pairing issues ({today})."
    if "B166 full layer inventory and sticky state matrix" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    asset_rows = scan_assets()
    matrix_rows = build_matrix(asset_rows)
    regional_base_candidates, regional_boundary_candidates = choose_regional_candidates(asset_rows)

    with ASSETS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "path",
                "exists",
                "size_bytes",
                "scope",
                "role",
                "referenced_in_index",
                "referenced_in_b165_prototype",
                "used_as_b165_base_for_states",
                "used_as_b165_boundary_for_states",
            ],
        )
        writer.writeheader()
        writer.writerows(asset_rows)

    with MATRIX_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "target_order",
                "target_state",
                "current_b165_state",
                "target_base",
                "current_base",
                "target_overlay",
                "current_overlay",
                "status",
                "issue_or_note",
                "message",
                "purpose",
            ],
        )
        writer.writeheader()
        writer.writerows(matrix_rows)

    status_counts = {}
    for r in matrix_rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    exists_count = sum(1 for r in asset_rows if r["exists"])
    missing_count = sum(1 for r in asset_rows if not r["exists"])
    density_row = next((r for r in asset_rows if r["path"] == "public/maps/global/global_hotspots_density.png"), None)
    total_row = next((r for r in asset_rows if r["path"] == "public/maps/global/global_hotspots_total.png"), None)
    regional_problem = [r for r in matrix_rows if r["status"] == "wrongly_paired"]

    doc = f"""# B166 - Full Layer Inventory and Sticky State Matrix

Date: {today}

## Ziel

B166 erstellt eine vollständige Inventur der Kartenassets und eine saubere Zielmatrix für den Flagship-Sticky-Zoom.

Auslöser waren zwei Befunde aus der Prototypprüfung:

1. Im Oberschwaben-/Regional-Step wurde ein regionaler Moorlayer mit den politischen Grenzen der Deutschlandkarte kombiniert.
2. Die globale Karte zur Emissionsintensität pro Fläche ist vorhanden, aber im B165-Prototyp nicht eingebunden.

B166 ändert die öffentliche Seite nicht. Es ist ein Inventur- und Entscheidungsdokument für den nächsten Reparaturpatch.

## Ergebnis kurz

- inventarisierte Karten-/Bildassets: {len(asset_rows)}
- vorhandene Assets: {exists_count}
- fehlende erwartete Assets: {missing_count}
- regionale Basis-Kandidaten: {len(regional_base_candidates)}
- regionale Boundary-Kandidaten: {len(regional_boundary_candidates)}

## Globale Druckkarten

| Karte | Vorhanden | Aktuell im B165-Prototyp | Bewertung |
|---|---:|---:|---|
| `global_hotspots_total.png` | {bool(total_row and total_row['exists'])} | {bool(total_row and total_row['referenced_in_b165_prototype'])} | Gesamt-Emissionsdruck / absoluter Druck |
| `global_hotspots_density.png` | {bool(density_row and density_row['exists'])} | {bool(density_row and density_row['referenced_in_b165_prototype'])} | Emissionsintensität pro Fläche; muss als eigener Step ergänzt werden |

## State-Matrix Status

| Status | Anzahl |
|---|---:|
"""
    for status, count in sorted(status_counts.items()):
        doc += f"| `{status}` | {count} |\n"

    doc += """
## Zielzustand für den Flagship-Sticky-Zoom

| Reihenfolge | State | Basisbild | Overlay | Aussage |
|---:|---|---|---|---|
"""
    for r in matrix_rows:
        doc += f"| {r['target_order']} | `{r['target_state']}` | `{r['target_base']}` | `{r['target_overlay']}` | {r['message']} |\n"

    doc += """
## Aktuelle Problemstellen

### 1. Globaler Druck muss in zwei Aussagen getrennt werden

Der Prototyp nutzt derzeit `global_hotspots_total.png` als Druckkarte.
Die vorhandene Intensitätskarte `global_hotspots_density.png` fehlt im Ablauf.

Empfohlene Trennung:

```text
global-pressure-total   = Wo ist der gesamte Emissionsdruck hoch?
global-pressure-density = Wo ist der Druck pro Fläche besonders intensiv?
```

Das ist editorial sinnvoll, weil Gesamtmenge und Intensität unterschiedliche Aussagen sind.

### 2. Regional-Handoff darf kein Deutschland-Overlay verwenden

Der letzte Step braucht eine passende regionale Kopplung:

```text
regional base    + regional boundaries
```

oder:

```text
regional base with boundaries already embedded + no additional overlay
```

Nicht verwenden:

```text
regional base + germany_admin_context
```

Das erzeugt die aktuell sichtbare Fehlkopplung.

## Regionale Kandidaten

### Basis-Kandidaten

"""
    if regional_base_candidates:
        for p in regional_base_candidates:
            doc += f"- `{p}`\n"
    else:
        doc += "- keine regionalen Basis-Kandidaten gefunden\n"

    doc += "\n### Boundary-Kandidaten\n\n"
    if regional_boundary_candidates:
        for p in regional_boundary_candidates:
            doc += f"- `{p}`\n"
    else:
        doc += "- keine passenden regionalen Boundary-Overlays gefunden\n"

    doc += """
## Entscheidung für den nächsten Patch

Der nächste Patch sollte den B165-Prototyp reparieren:

```text
B167 Sticky Zoom State Repair
```

Pflichten für B167:

1. `global_hotspots_density.png` als eigenen Step ergänzen.
2. `global-pressure` in `global-pressure-total` umbenennen oder sauber auftrennen.
3. `regional-handoff` in `oberschwaben-handoff` umbenennen.
4. Deutschland-Overlay im Regional-Step entfernen.
5. Nur ein regional passendes Overlay verwenden, falls vorhanden.
6. Falls kein regionales Boundary-Overlay vorhanden ist: keine zusätzliche Grenze über den Regional-Step legen und Gate für neuen Regional-Export markieren.

## Dateien

- `docs/B166_map_asset_inventory.csv`
- `docs/B166_sticky_state_matrix.csv`
- `docs/B166_sticky_zoom_repair_recommendations.md`
"""
    write(DOC, doc)

    repair = f"""# B166 - Sticky Zoom Repair Recommendations

Date: {today}

## Reparaturziel

Der B165/B165b-Prototyp soll nicht verworfen werden. Er braucht eine saubere State-Matrix.

## Reparaturliste für B167

### A. Globale Druckkarten trennen

Aktuell:

```text
global-pressure -> global_hotspots_total.png
```

Neu:

```text
global-pressure-total   -> global_hotspots_total.png
global-pressure-density -> global_hotspots_density.png
```

Textvorschläge:

```text
02 / Gesamt
Wo ist der gesamte Emissionsdruck hoch?

03 / Intensität
Wo ist der Druck pro Fläche besonders hoch?
```

### B. Regionale Übergabe reparieren

Aktuell problematisch:

```text
regional-handoff base    = regional/Oberschwaben-or-BW asset
regional-handoff overlay = germany_admin_context.png
```

Neu:

```text
oberschwaben-handoff base    = regional/BW/Oberschwaben asset
oberschwaben-handoff overlay = matching regional boundary OR none
```

Falls kein regionales Boundary-Overlay existiert:

```text
Do not overlay germany_admin_context.
Use base image only and mark regional boundary export as open gate.
```

### C. Boundary-Pairing-Regel

| Basis-Scope | Erlaubtes Overlay |
|---|---|
| global | global_country_borders |
| europe | europe_country_borders |
| germany | germany_admin_context |
| bw | BW boundary / counties / embedded |
| oberschwaben | Oberschwaben counties / embedded |
| regional | matching regional boundary / embedded |

### D. Finale Stepfolge

```text
01 global-peat
02 global-pressure-total
03 global-pressure-density
04 europe-bridge
05 germany-extent
06 germany-types
07 oberschwaben-handoff
```

### E. Integrationsentscheidung

Erst nach B167 visuell prüfen:

- Ist sieben Steps zu lang?
- Sind Total und Density beide nötig?
- Falls ja: bleiben beide.
- Falls nein: Density ist wahrscheinlich redaktionell wichtiger als Total, weil sie den Flächendruck besser zeigt.
"""
    write(REPAIR, repair)

    audit = f"""# B166 full layer inventory and sticky state matrix audit

Date: {today}

Result: INVENTORY ONLY. No public page files changed.

Inputs:
- index.html exists: {INDEX.exists()}
- B165 prototype exists: {B165_PROTO.exists()}

Assets:
- total inventoried: {len(asset_rows)}
- existing: {exists_count}
- missing expected: {missing_count}

Matrix status counts:
"""
    for status, count in sorted(status_counts.items()):
        audit += f"- {status}: {count}\n"

    audit += "\nRegional candidates:\n"
    audit += f"- base candidates: {len(regional_base_candidates)}\n"
    audit += f"- boundary candidates: {len(regional_boundary_candidates)}\n"

    if regional_problem:
        audit += "\nDetected regional pairing issue:\n"
        for r in regional_problem:
            audit += f"- {r['target_state']}: current_base={r['current_base']} current_overlay={r['current_overlay']}\n"

    audit += """
Created/updated:

- docs/B166_full_layer_inventory_and_sticky_state_matrix.md
- docs/B166_map_asset_inventory.csv
- docs/B166_sticky_state_matrix.csv
- docs/B166_sticky_zoom_repair_recommendations.md
- docs/B166_full_layer_inventory_and_sticky_state_matrix_audit.txt
- tasks/done.md

Recommended next patch: B167 Sticky Zoom State Repair
"""
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B166 full layer inventory and sticky state matrix complete.")
    print("Inventory only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B166_full_layer_inventory_and_sticky_state_matrix.md")
    print("  docs/B166_map_asset_inventory.csv")
    print("  docs/B166_sticky_state_matrix.csv")
    print("  docs/B166_sticky_zoom_repair_recommendations.md")
    print("  docs/B166_full_layer_inventory_and_sticky_state_matrix_audit.txt")
    print("  tasks/done.md")
    print("Recommended next patch: B167 Sticky Zoom State Repair")


if __name__ == "__main__":
    main()
