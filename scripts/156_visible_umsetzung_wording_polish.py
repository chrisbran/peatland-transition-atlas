from pathlib import Path
import re
from datetime import date
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "156_visible_umsetzung_wording_polish.py"
DOC = ROOT / "docs" / "B156_visible_umsetzung_wording_polish.md"
CSV_OUT = ROOT / "docs" / "B156_visible_umsetzung_wording_replacements.csv"
AUDIT = ROOT / "docs" / "B156_visible_umsetzung_wording_polish_audit.txt"
DONE = ROOT / "tasks" / "done.md"

REPLACEMENTS = [
    {
        "id": "frame_mismatch_sentence",
        "pattern": r"Die\s+Umsetzung\s+entscheidet\s+sich\s+aber\s+dort,\s+wo\s+Wasserstand,\s+Nutzung,\s+Eigentum,\s+Betriebe\s+und\s+Wertschöpfungsketten\s+zusammenkommen\.",
        "replacement": "In der Praxis entscheidet sich das Thema dort, wo Wasserstand, Nutzung, Eigentum, Betriebe und Wertschöpfungsketten zusammenkommen.",
        "reason": "reduces repeated Umsetzung in the Frame-Mismatch paragraph",
    },
    {
        "id": "frame_step_heading",
        "pattern": r"Umsetzung\s+braucht\s+lokale\s+Ketten",
        "replacement": "Lokale Ketten entscheiden",
        "reason": "turns a topic label into a sharper statement title",
    },
    {
        "id": "value_chain_scaling_sentence",
        "pattern": r"Kleinere\s+Mengen,\s+fehlende\s+Skalierung\s+oder\s+unsichere\s+Absatzwege\s+begrenzen\s+die\s+Umsetzung\.",
        "replacement": "Kleinere Mengen, fehlende Skalierung oder unsichere Absatzwege begrenzen die Marktfähigkeit.",
        "reason": "makes the value-chain bottleneck more specific",
    },
    {
        "id": "water_governance_start_sentence",
        "pattern": r"Deshalb\s+beginnt\s+Umsetzung\s+oft\s+dort,\s+wo\s+Zuständigkeiten\s+nicht\s+deckungsgleich\s+sind\.",
        "replacement": "Deshalb beginnt Abstimmung oft dort, wo Zuständigkeiten nicht deckungsgleich sind.",
        "reason": "fits the water/governance argument more precisely",
    },
    {
        "id": "water_governance_consequence_sentence",
        "pattern": r"Umsetzung\s+braucht\s+zusätzlich\s+lokale\s+Wasserkenntnis,\s+Abstimmung\s+zwischen\s+Eigentümern\s+und\s+Betrieben\s+sowie\s+tragfähige\s+Bewirtschaftungs-\s+und\s+Verwertungspfade\.",
        "replacement": "Planung braucht zusätzlich lokale Wasserkenntnis, Abstimmung zwischen Eigentümern und Betrieben sowie tragfähige Bewirtschaftungs- und Verwertungspfade.",
        "reason": "uses planning language in a planning/governance sentence",
    },
    {
        "id": "consequence_sentence",
        "pattern": r"Für\s+Umsetzung\s+reicht\s+die\s+Flächenperspektive\s+aber\s+nicht\s+aus:",
        "replacement": "Für die Praxis reicht die Flächenperspektive aber nicht aus:",
        "reason": "keeps the concluding sentence concrete and avoids repetition",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str, today: str) -> str:
    line = f"- B156 visible Umsetzung wording polish: reduced repeated visible uses of Umsetzung with more specific wording ({today})."
    if "B156 visible Umsetzung wording polish" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def count_umsetzung(text: str) -> int:
    return len(re.findall(r"Umsetzung", text, flags=re.I))


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    before_count = count_umsetzung(html)

    rows = []
    patched = html

    for item in REPLACEMENTS:
        patched, n = re.subn(item["pattern"], item["replacement"], patched, flags=re.S)
        rows.append({
            "id": item["id"],
            "replacements": n,
            "replacement": item["replacement"],
            "reason": item["reason"],
        })

    after_count = count_umsetzung(patched)

    write(INDEX, patched)

    today = date.today().isoformat()

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "replacements", "replacement", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    md = []
    md.append("# B156 - Visible `Umsetzung` Wording Polish")
    md.append("")
    md.append(f"Date: {today}")
    md.append("")
    md.append("## Ziel")
    md.append("")
    md.append("B103b meldete sechs sichtbare Review-Kandidaten für wiederholte Verwendungen von `Umsetzung`.")
    md.append("B156 reduziert diese Wiederholung gezielt und ersetzt sie dort, wo präzisere Wörter fachlich besser passen.")
    md.append("")
    md.append("## Prinzip")
    md.append("")
    md.append("- keine Änderung an Karten, Daten, Quellen oder Struktur")
    md.append("- nur sichtbare Formulierungen im öffentlichen Seitenfluss")
    md.append("- keine versteckten/retired Abschnitte anfassen")
    md.append("- keine inhaltliche Abschwächung der V2-These")
    md.append("")
    md.append("## Ersetzungen")
    md.append("")
    md.append("| ID | Treffer | Neue Formulierung | Zweck |")
    md.append("|---|---:|---|---|")
    for row in rows:
        md.append(f"| `{row['id']}` | {row['replacements']} | {row['replacement']} | {row['reason']} |")
    md.append("")
    md.append("## Zählung")
    md.append("")
    md.append(f"- `Umsetzung` in `index.html` vorher: {before_count}")
    md.append(f"- `Umsetzung` in `index.html` nachher: {after_count}")
    md.append("")
    md.append("Die Zählung umfasst das gesamte HTML. Maßgeblich für die öffentliche Bewertung bleibt weiterhin `scripts/103b_corrected_visible_text_audit.py`.")
    md.append("")
    md.append("## QA")
    md.append("")
    md.append("Nach dem Patch:")
    md.append("")
    md.append("```powershell")
    md.append("python scripts\\103b_corrected_visible_text_audit.py")
    md.append("python scripts\\58_visual_qa_and_commit_check.py")
    md.append("```")
    write(DOC, "\n".join(md) + "\n")

    audit = []
    audit.append("# B156 visible Umsetzung wording polish audit")
    audit.append("")
    audit.append(f"Date: {today}")
    audit.append("")
    audit.append(f"`Umsetzung` count in index.html before: {before_count}")
    audit.append(f"`Umsetzung` count in index.html after: {after_count}")
    audit.append("")
    audit.append("Replacement results:")
    for row in rows:
        audit.append(f"- {row['id']}: {row['replacements']}")
    audit.append("")
    if any(row["replacements"] == 0 for row in rows):
        audit.append("WARN: Some planned replacements had zero matches. Check whether prior patches already changed the wording.")
    else:
        audit.append("OK: All planned replacements matched at least once.")
    audit.append("")
    audit.append("Result: PATCH WRITTEN. Run B103b and B58 before commit.")
    write(AUDIT, "\n".join(audit) + "\n")

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B156 visible Umsetzung wording polish complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B156_visible_umsetzung_wording_polish.md")
    print("  docs/B156_visible_umsetzung_wording_replacements.csv")
    print("  docs/B156_visible_umsetzung_wording_polish_audit.txt")
    print("  tasks/done.md")
    print(f"Umsetzung count before: {before_count}")
    print(f"Umsetzung count after: {after_count}")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
