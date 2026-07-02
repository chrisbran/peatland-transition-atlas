from pathlib import Path
from datetime import date
import csv
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "173_publication_gate_audit.py"
DOC = ROOT / "docs" / "B173_publication_gate_audit.md"
CSV_OUT = ROOT / "docs" / "B173_publication_gate_audit.csv"
AUDIT = ROOT / "docs" / "B173_publication_gate_audit_run.txt"
DONE = ROOT / "tasks" / "done.md"

GATES = [
    {
        "gate": "scope_disclaimer",
        "label": "Fachlicher Demonstrator / keine Eignungskarte",
        "required": True,
        "patterns": [
            r"Fachlicher\s+Demonstrator",
            r"keine\s+Eignungskarte",
            r"keine\s+Entscheidungskarte",
            r"keine\s+Standortprüfung",
        ],
        "why": "The page must not be read as a parcel-level suitability or decision map.",
    },
    {
        "gate": "method_short",
        "label": "Methode in Kürze",
        "required": True,
        "patterns": [
            r"Methode\s+in\s+Kürze",
            r"methode-in-kuerze",
        ],
        "why": "Method transparency must be available from map/source lines.",
    },
    {
        "gate": "sources_section",
        "label": "Quellen / source section",
        "required": True,
        "patterns": [
            r"id=[\"']quellen[\"']",
            r">\s*Quellen\s*<",
            r"Quellenbasis",
            r"Datenbasis",
        ],
        "why": "Publication needs visible source trail.",
    },
    {
        "gate": "impressum",
        "label": "Impressum",
        "required": True,
        "patterns": [
            r"Impressum",
            r"impressum",
        ],
        "why": "Public German-facing page should have an Impressum path before wider release.",
    },
    {
        "gate": "datenschutz",
        "label": "Datenschutz",
        "required": True,
        "patterns": [
            r"Datenschutz",
            r"datenschutz",
            r"Datenschutzhinweis",
        ],
        "why": "Public page, especially with an external Felt element/link, needs a privacy path.",
    },
    {
        "gate": "external_felt_notice",
        "label": "Felt / external provider notice",
        "required": True,
        "patterns": [
            r"Felt",
            r"externer\s+Kartenprototyp",
            r"externe\s+Karte",
            r"externer\s+Anbieter",
            r"Drittanbieter",
        ],
        "why": "External map integration or link needs visible provider/privacy context.",
    },
    {
        "gate": "hohenheim_disclaimer",
        "label": "Hohenheim / SOLAMO-BW disclaimer",
        "required": True,
        "patterns": [
            r"Hohenheim",
            r"SOLAMO",
            r"SOLAMO-BW",
            r"Universität\s+Hohenheim",
        ],
        "why": "Institutional context and disclaimer/freigabe gate must be explicit before publication.",
    },
    {
        "gate": "oberschwaben_area_reference",
        "label": "Oberschwaben area reference around 19,900 ha",
        "required": True,
        "patterns": [
            r"19[.,]\s*900\s*ha",
            r"19[.,]\s*867",
            r"19867",
        ],
        "why": "The central Oberschwaben area figure should be visible and sourceable.",
    },
    {
        "gate": "source_line_under_graphics",
        "label": "Source/method lines under graphics",
        "required": True,
        "patterns": [
            r"Datenbasis:",
            r"Quelle:",
            r"Quellenbasis",
            r"kartografische\s+Aufbereitung",
        ],
        "why": "Graphics should carry compact source/method lines.",
    },
    {
        "gate": "no_raw_gis_refs",
        "label": "No raw local GIS/data paths in index",
        "required": True,
        "inverse": True,
        "patterns": [
            r"C:\\Users\\",
            r"working/",
            r"working\\",
            r"data/external/",
            r"data\\external\\",
            r"\.gdb",
            r"\.gpkg",
            r"\.shp",
        ],
        "why": "Public page must not expose local/raw GIS paths.",
    },
    {
        "gate": "b169_live_zoom",
        "label": "B169 live sticky zoom present",
        "required": True,
        "patterns": [
            r"B169_LIVE_STICKY_ZOOM_START",
            r"b169_live_sticky_zoom\.js",
            r"oberschwaben_landkreise_moor_nolabel\.png",
        ],
        "why": "The new premium map sequence should be active after B169e/B172.",
    },
    {
        "gate": "value_chain_scorecard",
        "label": "Value-chain scorecard present",
        "required": True,
        "patterns": [
            r"Bis\s+zur\s+Ernte\s+ist\s+vieles\s+anschlussfähig",
            r"Danach\s+wird\s+es\s+eng",
            r"Wertschöpfung",
            r"Scorecard",
        ],
        "why": "The value-chain climax is one of the core V2 narrative moments.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str, today: str) -> str:
    line = f"- B173 publication gate audit: checked release-critical gates such as scope disclaimer, methods, sources, Impressum/Datenschutz, Felt notice, institutional disclaimer, area reference, and absence of raw GIS paths ({today})."
    if "B173 publication gate audit" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def evaluate_gate(text: str, gate: dict) -> dict:
    matches = []
    for pattern in gate["patterns"]:
        found = bool(re.search(pattern, text, flags=re.I | re.S))
        if found:
            matches.append(pattern)

    inverse = bool(gate.get("inverse", False))
    passed = (len(matches) == 0) if inverse else (len(matches) > 0)

    if gate["required"] and not passed:
        status = "FAIL"
    elif passed:
        status = "PASS"
    else:
        status = "WARN"

    return {
        "gate": gate["gate"],
        "label": gate["label"],
        "required": gate["required"],
        "inverse": inverse,
        "status": status,
        "matches": "; ".join(matches),
        "why": gate["why"],
    }


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    text = read(INDEX)
    css = read(CSS) if CSS.exists() else ""

    rows = [evaluate_gate(text, gate) for gate in GATES]
    fail_rows = [row for row in rows if row["status"] == "FAIL"]
    warn_rows = [row for row in rows if row["status"] == "WARN"]
    pass_rows = [row for row in rows if row["status"] == "PASS"]

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gate", "label", "required", "inverse", "status", "matches", "why"],
        )
        writer.writeheader()
        writer.writerows(rows)

    doc = f"""# B173 - Publication Gate Audit

Date: {today}

## Ziel

B173 ist ein Release-Gate-Audit nach der B169–B172-Integration.

Der neue Sticky-Zoom ist visuell stark genug. Jetzt muss geprüft werden, ob die Seite vor einer breiteren Veröffentlichung die wichtigsten fachlichen, rechtlichen und redaktionellen Mindestpunkte abdeckt.

B173 ändert keine öffentliche Seite.

## Ergebnis

| Status | Anzahl |
|---|---:|
| PASS | {len(pass_rows)} |
| WARN | {len(warn_rows)} |
| FAIL | {len(fail_rows)} |

## Gate-Übersicht

| Gate | Status | Warum wichtig |
|---|---|---|
"""
    for row in rows:
        doc += f"| {row['label']} | `{row['status']}` | {row['why']} |\n"

    doc += """
## Fehlende oder kritische Gates

"""
    if fail_rows:
        for row in fail_rows:
            doc += f"### {row['label']}\n\n"
            doc += f"- Gate: `{row['gate']}`\n"
            doc += f"- Status: `{row['status']}`\n"
            doc += f"- Warum: {row['why']}\n"
            doc += "- Erwartete Signale:\n"
            for gate in GATES:
                if gate["gate"] == row["gate"]:
                    for pattern in gate["patterns"]:
                        doc += f"  - `{pattern}`\n"
            doc += "\n"
    else:
        doc += "Keine FAIL-Gates gefunden.\n\n"

    doc += """
## Interpretation

B173 ist bewusst streng. Ein FAIL bedeutet nicht zwingend, dass die Seite falsch ist.
Es bedeutet: Vor einer Veröffentlichung sollte dieser Punkt bewusst ergänzt, bestätigt oder dokumentiert werden.

## Empfohlene nächste Patches

### Falls Impressum/Datenschutz fehlen

```text
B174 Legal Footer and Provider Notice
```

Ziel:

- Impressum-Link
- Datenschutz-Link
- Felt-/Drittanbieter-Hinweis
- institutioneller Kontext
- kein juristisch überladener Text, aber sichtbarer Veröffentlichungsrahmen

### Falls Quellen/Methoden unklar sind

```text
B175 Source Register and Method Link Polish
```

Ziel:

- alle Karten-/Grafikquellen kompakt sichtbar
- Methode-in-Kürze sauber verlinkt
- Quellenbereich nicht überladen

### Falls alle Gates grün sind

```text
B174 Final Mobile/Desktop Visual QA Record
```

Ziel:

- Browser-/Viewport-QA dokumentieren
- Commit- und Release-Readiness festhalten
"""
    write(DOC, doc)

    audit = "# B173 publication gate audit run\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"index.html length: {len(text)}\n"
    audit += f"src/styles.css exists: {CSS.exists()}\n"
    audit += f"src/styles.css length: {len(css)}\n\n"
    audit += f"PASS: {len(pass_rows)}\n"
    audit += f"WARN: {len(warn_rows)}\n"
    audit += f"FAIL: {len(fail_rows)}\n\n"
    audit += "Failed gates:\n"
    if fail_rows:
        for row in fail_rows:
            audit += f"- {row['gate']}: {row['label']}\n"
    else:
        audit += "- none\n"

    audit += "\nCreated/updated:\n"
    audit += "- docs/B173_publication_gate_audit.md\n"
    audit += "- docs/B173_publication_gate_audit.csv\n"
    audit += "- docs/B173_publication_gate_audit_run.txt\n"
    audit += "- tasks/done.md\n"
    audit += "\nResult: AUDIT COMPLETE. No public page files changed.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B173 publication gate audit complete.")
    print("Audit only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B173_publication_gate_audit.md")
    print("  docs/B173_publication_gate_audit.csv")
    print("  docs/B173_publication_gate_audit_run.txt")
    print("  tasks/done.md")
    print(f"PASS: {len(pass_rows)} | WARN: {len(warn_rows)} | FAIL: {len(fail_rows)}")
    if fail_rows:
        print("Failed gates:")
        for row in fail_rows:
            print(f"  - {row['gate']}: {row['label']}")
    print("Next: inspect audit and decide B174.")


if __name__ == "__main__":
    main()
