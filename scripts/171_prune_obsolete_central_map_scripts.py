from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"

SCRIPT = ROOT / "scripts" / "171_prune_obsolete_central_map_scripts.py"
DOC = ROOT / "docs" / "B171_prune_obsolete_central_map_scripts.md"
CSV_OUT = ROOT / "docs" / "B171_pruned_script_refs.csv"
AUDIT = ROOT / "docs" / "B171_prune_obsolete_central_map_scripts_audit.txt"
DONE = ROOT / "tasks" / "done.md"

B169_MARKER = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
B169_SCRIPT = "src/b169_live_sticky_zoom.js"

OBSOLETE_SCRIPT_HINTS = [
    "central_global_map_story.js",
    "central_layer_state_hardener",
    "central_step_state_bridge",
    "central_stage_label_fix",
    "central_map_story",
    "global_map_story",
]

KEEP_SCRIPT_HINTS = [
    "b169_live_sticky_zoom.js",
    "main.js",
    "app.js",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def extract_src(script_tag: str) -> str:
    m = re.search(r'\bsrc\s*=\s*"([^"]+)"', script_tag, re.I)
    if m:
        return m.group(1)
    m = re.search(r"\bsrc\s*=\s*'([^']+)'", script_tag, re.I)
    if m:
        return m.group(1)
    return ""


def should_remove_script(src: str) -> bool:
    low = src.lower()
    if any(keep.lower() in low for keep in KEEP_SCRIPT_HINTS):
        return False
    return any(hint.lower() in low for hint in OBSOLETE_SCRIPT_HINTS)


def prune_scripts(html: str):
    rows = []
    removed_count = 0

    def repl(match: re.Match) -> str:
        nonlocal removed_count
        tag = match.group(0)
        src = extract_src(tag)
        remove = should_remove_script(src)
        rows.append({
            "src": src,
            "removed": remove,
            "reason": "obsolete central map story script after B169 live sticky zoom" if remove else "kept",
        })
        if remove:
            removed_count += 1
            return ""
        return tag

    patched = re.sub(r"<script\b[^>]*\bsrc\s*=\s*['\"][^'\"]+['\"][^>]*>\s*</script>\s*", repl, html, flags=re.I | re.S)
    return patched, rows, removed_count


def update_done(done_text: str, today: str) -> str:
    line = f"- B171 prune obsolete central map scripts: removed old central map-story script references after the B169 live sticky zoom replaced that section ({today})."
    if "B171 prune obsolete central map scripts" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    before_len = len(html)

    b169_present = B169_MARKER in html
    b169_script_present = B169_SCRIPT in html

    if not b169_present:
        raise SystemExit("B169 live sticky zoom marker not found. Refusing to prune central map scripts before B169 is present.")

    patched, rows, removed_count = prune_scripts(html)

    write(INDEX, patched)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["src", "removed", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    removed_rows = [r for r in rows if r["removed"]]
    kept_rows = [r for r in rows if not r["removed"]]

    doc = f"""# B171 - Prune Obsolete Central Map Scripts

Date: {today}

## Ziel

Nach B169 bis B170 ist die zentrale Kartenfolge durch den neuen Live-Sticky-Zoom ersetzt.
Alte Script-Referenzen der vorherigen zentralen Kartenstory sollen nicht weiter auf der Live-Seite laufen.

B171 entfernt deshalb nur alte Script-Tags in `index.html`, die eindeutig zur vorherigen zentralen Map-Story gehören.

## Sicherheitsregel

B171 läuft nur, wenn der B169-Live-Sticky-Zoom bereits vorhanden ist:

```text
{B169_MARKER}
```

Der neue Controller bleibt erhalten:

```text
{B169_SCRIPT}
```

## Entfernte Script-Referenzen

| Script | Grund |
|---|---|
"""
    if removed_rows:
        for row in removed_rows:
            doc += f"| `{row['src']}` | {row['reason']} |\n"
    else:
        doc += "| — | Keine alten Script-Referenzen gefunden. |\n"

    doc += f"""
## Behaltene Script-Referenzen

| Script |
|---|
"""
    if kept_rows:
        for row in kept_rows:
            doc += f"| `{row['src']}` |\n"
    else:
        doc += "| — |\n"

    doc += """
## Nicht geändert

- keine Kartenassets
- keine CSS-Regeln
- keine B169/B170-Texte
- keine Felt-Integration
- keine Datenquellen
- keine raw GIS-Dateien

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Sticky-Zoom funktioniert weiterhin.
- Alle acht Steps wechseln Karte und Label.
- Oberschwaben-Step nutzt weiterhin die No-Label-Karte.
- Keine Console-Fehler zu fehlenden alten Map-Story-Funktionen.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    audit = "# B171 prune obsolete central map scripts audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"B169 marker present before patch: {b169_present}\n"
    audit += f"B169 script present before patch: {b169_script_present}\n"
    audit += f"Script tags inspected: {len(rows)}\n"
    audit += f"Script refs removed: {removed_count}\n"
    audit += f"index.html length before: {before_len}\n"
    audit += f"index.html length after: {len(new_html)}\n\n"
    audit += "Removed scripts:\n"
    if removed_rows:
        for row in removed_rows:
            audit += f"- {row['src']}\n"
    else:
        audit += "- none\n"

    audit += "\nPost-patch checks:\n"
    audit += f"- B169 marker still present: {B169_MARKER in new_html}\n"
    audit += f"- B169 script still present: {B169_SCRIPT in new_html}\n"
    audit += f"- old central script hints still referenced: {any(h.lower() in new_html.lower() for h in OBSOLETE_SCRIPT_HINTS)}\n"
    audit += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B171 prune obsolete central map scripts complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B171_prune_obsolete_central_map_scripts.md")
    print("  docs/B171_pruned_script_refs.csv")
    print("  docs/B171_prune_obsolete_central_map_scripts_audit.txt")
    print("  tasks/done.md")
    print(f"Removed script refs: {removed_count}")
    print("Next: run B103b and B58 QA, then visual QA.")


if __name__ == "__main__":
    main()
