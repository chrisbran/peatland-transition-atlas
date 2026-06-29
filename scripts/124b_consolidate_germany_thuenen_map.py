#!/usr/bin/env python3
# B124b - Consolidate Germany Thuenen states onto one map

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CENTRAL = ROOT / "src" / "central_global_map_story.js"
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b124b_consolidate_germany_thuenen_map"

REPORT = DOCS / "B124b_consolidate_germany_thuenen_map.md"
AUDIT = DOCS / "B124b_consolidate_germany_thuenen_map_audit.txt"
TODAY = date.today().isoformat()

NEW_STATE_BLOCK = """    "germany-thuenen-types": {
      mode: "Lesart der Thünen-Kulisse",
      title: "Für den Deutschland-Maßstab reicht eine Thünen-Karte.",
      legend: '<span><i class="legend-peat"></i>Thünen-Kulisse organischer Böden</span><span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Daten: Thünen-Kulisse organischer Böden; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-thuenen-extent": 0.98, "layer-germany-admin": 0.86 }
    },"""

NEW_STEP_TITLE = "Die Thünen-Kulisse bleibt die relevante Deutschlandkarte."
NEW_STEP_TEXT = "Für diese Maßstabsebene wird keine zweite kaum unterscheidbare Bodentyp-Karte gezeigt. Entscheidend ist die Einordnung als nationale Planungskulisse; die nächste fachliche Differenzierung erfolgt erst regional und hydrologisch."


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup(path: Path) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / rel(path).replace("/", "__").replace("\\", "__")
    if path.exists() and not dest.exists():
        shutil.copy2(path, dest)


def patch_central() -> int:
    text = read_text(CENTRAL)
    pattern = r'    "germany-thuenen-types": \{.*?\n    \},(?=\n    "bw-context":)'
    new_text, n = re.subn(pattern, NEW_STATE_BLOCK, text, flags=re.DOTALL)
    if n:
        backup(CENTRAL)
        write_text(CENTRAL, new_text)
    return n


def replace_first_tag(block: str, tag: str, new_inner: str) -> tuple[str, int]:
    pattern = rf"<{tag}>(.*?)</{tag}>"
    repl = f"<{tag}>{new_inner}</{tag}>"
    return re.subn(pattern, repl, block, count=1, flags=re.DOTALL)


def patch_index() -> int:
    text = read_text(INDEX)
    article_pattern = r'(<article class="central-map-step" data-global-state="germany-thuenen-types">.*?</article>)'
    m = re.search(article_pattern, text, flags=re.DOTALL)
    if not m:
        return 0

    block = m.group(1)
    new_block, n_h3 = replace_first_tag(block, "h3", NEW_STEP_TITLE)
    new_block, n_p = replace_first_tag(new_block, "p", NEW_STEP_TEXT)

    if new_block != block:
        backup(INDEX)
        text = text[:m.start()] + new_block + text[m.end():]
        write_text(INDEX, text)
        return n_h3 + n_p
    return 0


def audit() -> dict[str, int]:
    central = read_text(CENTRAL)
    index = read_text(INDEX)

    return {
        "state_present": central.count('"germany-thuenen-types"'),
        "types_layer_in_state": central.count('"layer-germany-thuenen-types": 0.98'),
        "extent_layer_in_types_state": central.count('"layer-germany-thuenen-extent": 0.98'),
        "kat_lang_in_types_state": central.count("Bodentypen nach KAT_LANG"),
        "new_step_title": index.count(NEW_STEP_TITLE),
        "new_step_text": index.count(NEW_STEP_TEXT),
        "germany_thuenen_types_step": index.count('data-global-state="germany-thuenen-types"'),
        "risk_thuenen_ascii": central.count("Thuenen") + index.count("Thuenen"),
        "risk_mojibake": central.count("Ã") + index.count("Ã") + central.count("�") + index.count("�"),
    }


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B124b - Consolidate Germany Thünen map"
    if marker in current:
        return
    entry = f"""
## B124b - Consolidate Germany Thünen map ({TODAY})

- Kept the central scrolly sequence stable after B124.
- Consolidated the two Germany/Thünen steps onto one readable Thünen extent map.
- Reworded the second Germany/Thünen text step as an interpretation step instead of a second map.
- Did not modify maps, CSS or data.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_docs(result: dict[str, int], central_hits: int, index_hits: int) -> None:
    ok = (
        central_hits == 1
        and index_hits >= 1
        and result["state_present"] >= 1
        and result["types_layer_in_state"] == 0
        and result["new_step_title"] == 1
        and result["new_step_text"] == 1
        and result["germany_thuenen_types_step"] == 1
        and result["risk_thuenen_ascii"] == 0
        and result["risk_mojibake"] == 0
    )
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B124b – Consolidate Germany Thünen Map",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "Die Deutschland/Thünen-Sequenz bleibt stabil, zeigt aber nicht mehr zwei kaum unterscheidbare Karten nacheinander.",
        "",
        "## Änderungen",
        "",
        f"- JS state replacement hits: {central_hits}",
        f"- HTML step text replacement hits: {index_hits}",
        "- `germany-thuenen-types` bleibt als State erhalten, nutzt aber dieselbe sichtbare Thünen-Kulisse wie `germany-thuenen-extent`.",
        "- Keine Karten-, CSS- oder Datenänderung.",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B124b_consolidate_germany_thuenen_map_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\central_global_map_story.js -Pattern \"germany-thuenen-types\",\"layer-germany-thuenen-types\",\"layer-germany-thuenen-extent\",\"Für den Deutschland-Maßstab reicht eine Thünen-Karte\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B124b consolidate Germany Thünen map audit",
        "",
        f"- Status: {status}",
        f"- JS state replacement hits: {central_hits}",
        f"- HTML step text replacement hits: {index_hits}",
        "",
        "| Check | Count |",
        "|---|---:|",
    ]
    for key, value in result.items():
        audit_lines.append(f"| `{key}` | {value} |")
    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not CENTRAL.exists():
        print(f"Missing {rel(CENTRAL)}")
        sys.exit(1)
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    central_hits = patch_central()
    index_hits = patch_index()
    update_done()
    result = audit()
    write_docs(result, central_hits, index_hits)

    ok = (
        central_hits == 1
        and index_hits >= 1
        and result["types_layer_in_state"] == 0
        and result["new_step_title"] == 1
        and result["new_step_text"] == 1
        and result["risk_thuenen_ascii"] == 0
        and result["risk_mojibake"] == 0
    )

    print("B124b Germany Thünen map consolidation complete.")
    print("Changed/created:")
    for p in [CENTRAL, INDEX, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"JS state replacement hits: {central_hits}")
    print(f"HTML step text replacement hits: {index_hits}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B124b_consolidate_germany_thuenen_map_audit.txt -Encoding UTF8")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
