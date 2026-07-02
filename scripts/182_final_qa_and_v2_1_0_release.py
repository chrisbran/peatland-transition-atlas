from pathlib import Path
from datetime import date
import re
import csv
import subprocess
from html import unescape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B182_final_qa_and_v2_1_0_release.md"
AUDIT = ROOT / "docs" / "B182_final_qa_and_v2_1_0_release_audit.txt"
CHECKLIST = ROOT / "docs" / "B182_v2_1_0_release_checklist.md"
NOTES = ROOT / "docs" / "B182_v2_1_0_release_notes.md"
SIGNALS_CSV = ROOT / "docs" / "B182_release_signals.csv"
DONE = ROOT / "tasks" / "done.md"

EXPECTED_SIGNALS = [
    ("B169 live sticky zoom", "B169_LIVE_STICKY_ZOOM_START", "must"),
    ("B176 local cartographic depth", "B176_LOCAL_CARTOGRAPHIC_DEPTH_START", "must"),
    ("B178 scale-change note", "B178_SCALE_CHANGE_NOTE_START", "must"),
    ("B178 area caveat", "B178_AREA_CAVEAT_START", "must"),
    ("B179 bottleneck graphic", "B179_BOTTLENECK_GRAPHIC_START", "must"),
    ("B181 closing counterpoint", "B181_CLOSING_COUNTERPOINT_START", "must"),
    ("No Felt token", "felt", "must_not_lower"),
    ("No OpenStreetMap token", "openstreetmap", "must_not_lower"),
    ("No iframe", "<iframe", "must_not_lower"),
    ("Scope box", "Fachlicher Demonstrator", "must"),
    ("Method section", "Methode in Kürze", "must"),
    ("Sources section", "Datengrundlagen, Rechte und Quellenvermerke", "should"),
]

EXPECTED_REPORTS = [
    ("B177 external request audit", ROOT / "docs" / "B177_external_request_audit_run.txt", r"Result:\s*PASS"),
    ("B58 visual QA", ROOT / "docs" / "B58_visual_qa_and_commit_check.md", r"## Result\s*PASS"),
    ("B103b visible text audit", ROOT / "docs" / "B103b_corrected_visible_text_audit.md", r"Visible findings:\s*0|visible findings\s*0|Visible findings.*?0"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def text_only(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    return re.sub(r"\s+", " ", html).strip()


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git"] + args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def check_signals(html: str) -> list[dict]:
    rows = []
    lower = html.lower()

    for label, needle, mode in EXPECTED_SIGNALS:
        if mode == "must":
            ok = needle in html
            count = html.count(needle)
        elif mode == "should":
            ok = needle in html
            count = html.count(needle)
        elif mode == "must_not_lower":
            ok = needle.lower() not in lower
            count = lower.count(needle.lower())
        else:
            ok = False
            count = -1

        rows.append({
            "category": "source_signal",
            "label": label,
            "mode": mode,
            "count": count,
            "status": "PASS" if ok else ("WARN" if mode == "should" else "FAIL"),
            "detail": f"`{needle}` {'found' if count else 'not found'}",
        })

    return rows


def check_reports() -> list[dict]:
    rows = []
    for label, path, pattern in EXPECTED_REPORTS:
        exists = path.exists()
        content = read(path) if exists else ""
        ok = bool(re.search(pattern, content, flags=re.I | re.S)) if exists else False

        rows.append({
            "category": "report",
            "label": label,
            "mode": "expected_pass",
            "count": 1 if ok else 0,
            "status": "PASS" if ok else ("WARN" if not exists and "B103b" in label else "FAIL"),
            "detail": f"{path.as_posix()} {'matches expected PASS pattern' if ok else 'missing or not matching expected PASS pattern'}",
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = ["category", "label", "mode", "count", "status", "detail"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def update_done(done_text: str, today: str) -> str:
    line = f"- B182 final QA and v2.1.0 release prep: documented the post-Felt V2.1 release state, final QA checklist, release notes and tag instructions ({today})."
    if "B182 final QA and v2.1.0 release prep" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    css = read(CSS)

    rows = check_signals(html)
    rows.extend(check_reports())

    fails = [r for r in rows if r["status"] == "FAIL"]
    warns = [r for r in rows if r["status"] == "WARN"]
    passes = [r for r in rows if r["status"] == "PASS"]

    git_branch = run_git(["branch", "--show-current"])
    git_head = run_git(["log", "--oneline", "--decorate", "-n", "1"])
    git_tags = run_git(["tag", "--points-at", "HEAD"])
    git_status = run_git(["status", "--short"])

    visible_text = text_only(html)
    word_count = len(visible_text.split())

    write_csv(SIGNALS_CSV, rows)

    release_notes = f"""# v2.1.0 Release Notes - Peatland Transition Atlas

Date: {today}

## Zweck

`v2.1.0` schließt die öffentliche V2 nach dem Post-Publication-Review ab.

## Änderungen gegenüber v2.0.0

- Felt/OpenStreetMap-iframe aus der öffentlichen Seite entfernt.
- Externer Kartenviewer durch lokale kartografische Vertiefung ersetzt.
- External-Request-Audit ergänzt.
- Maßstabswechsel zwischen Thünen-Kulisse organischer Böden und BK50-Moor-/Feuchtbodenkontext explizit benannt.
- `~19.900 ha`-Zahl mit direktem Vorbehalt versehen.
- Flächenbilanz stärker als Aussage formuliert: vier von fünf Hektar sind Grünland.
- Engpass-Grafik durch statische Flaschenhalsgrafik ersetzt.
- Alte Scorecard-Reste aus der Engpass-Sektion entfernt.
- Schlussbogen durch Gegenposition präzisiert: Kettenperspektive ist wichtig, aber nicht jede Wiedervernässung braucht einen Produktmarkt.

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- keine Rohdaten
- keine externe Karten-/Tile-Einbindung
- B169 Sticky-Zoom bleibt aktiv
- regionale statische Karte bleibt aktiv

## QA-Soll

- B177 External Request Audit: PASS
- B103b Corrected Visible Text Audit: PASS / 0 sichtbare Findings
- B58 Visual QA and Commit Check: PASS

## Tagging

Nach Commit und Push:

```powershell
git tag -a v2.1.0 -m "Version 2.1 public demonstrator"
git push origin v2.1.0
```
"""
    write(NOTES, release_notes)

    checklist = f"""# B182 - v2.1.0 Release Checklist

Date: {today}

## Vor Commit

```powershell
python scripts\\177_external_request_audit.py
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Erwartung:

```text
B177: PASS
B103b: 0 sichtbare Findings
B58: PASS
```

## Manuelle Sichtprüfung

- [ ] Hero und Scope-Box sichtbar
- [ ] B169 Sticky-Zoom läuft durch alle acht States
- [ ] B178 Maßstabswechsel-Hinweis steht nicht störend, aber sichtbar
- [ ] Oberschwaben-Detailkarte bleibt sichtbar
- [ ] B176 lokale Kartografie-Vertiefung ersetzt Felt
- [ ] Flächenbilanz zeigt 19.900-ha-Zahl mit Vorbehalt
- [ ] B179/B179b Flaschenhalsgrafik steht allein, ohne alte Balkenreste
- [ ] B181 Gegenposition erscheint vor Methode/Quellen
- [ ] Footer/Quellenbereich sichtbar
- [ ] Mobile Darstellung einmal prüfen

## Browser-Network-Check

DevTools → Network → Disable cache → Hard reload. Suchen nach:

```text
felt
openstreetmap
tile
mapbox
maptiler
fonts.googleapis
fonts.gstatic
```

Erwartung: keine Treffer, abgesehen von passiven Quellenlinks, die nicht beim Seitenaufruf laden.

## Nach Commit und Push

```powershell
git tag -a v2.1.0 -m "Version 2.1 public demonstrator"
git push origin v2.1.0
```

## Optional nach Deployment

- [ ] öffentliche URL hart neu laden
- [ ] Quelltext im Browser nach `felt` prüfen
- [ ] B177-Audit im Repo nachvollziehbar
"""
    write(CHECKLIST, checklist)

    doc = f"""# B182 - Final QA and v2.1.0 Release Prep

Date: {today}

## Ziel

B182 dokumentiert den finalen V2.1-Stand nach den Patches B176-B181 und bereitet Commit, Push und Tag `v2.1.0` vor.

B182 ändert keine öffentliche Seite.

## Git-Kontext beim Audit

| Feld | Wert |
|---|---|
| Branch | `{git_branch}` |
| HEAD | `{git_head}` |
| Tags at HEAD | `{git_tags if git_tags else '—'}` |
| Word count visible text approx. | {word_count} |

## Ergebnis der Release-Signale

| Status | Anzahl |
|---|---:|
| PASS | {len(passes)} |
| WARN | {len(warns)} |
| FAIL | {len(fails)} |

Details: `docs/B182_release_signals.csv`

## PASS-Signale

"""
    for r in passes:
        doc += f"- **{r['label']}** — {r['detail']}\n"

    doc += "\n## WARN-Signale\n\n"
    if warns:
        for r in warns:
            doc += f"- **{r['label']}** — {r['detail']}\n"
    else:
        doc += "Keine WARN-Signale.\n"

    doc += "\n## FAIL-Signale\n\n"
    if fails:
        for r in fails:
            doc += f"- **{r['label']}** — {r['detail']}\n"
    else:
        doc += "Keine FAIL-Signale.\n"

    doc += f"""

## Arbeitsbaum beim Audit

```text
{git_status if git_status else 'clean'}
```

## Empfehlung

Wenn B177, B103b und B58 nach B182 erneut PASS melden:

```text
Commit → Push main → Tag v2.1.0
```

## Erzeugte Dateien

- `docs/B182_final_qa_and_v2_1_0_release.md`
- `docs/B182_final_qa_and_v2_1_0_release_audit.txt`
- `docs/B182_release_signals.csv`
- `docs/B182_v2_1_0_release_checklist.md`
- `docs/B182_v2_1_0_release_notes.md`
"""
    write(DOC, doc)

    audit = f"""# B182 final QA and v2.1.0 release audit

Date: {today}

No public page files changed.

Git:
- Branch: {git_branch}
- HEAD: {git_head}
- Tags at HEAD: {git_tags if git_tags else '—'}

Counts:
- PASS: {len(passes)}
- WARN: {len(warns)}
- FAIL: {len(fails)}
- Visible word count approx.: {word_count}

Core checks:
- B169 live sticky zoom: {'B169_LIVE_STICKY_ZOOM_START' in html}
- B176 local cartographic depth: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html}
- B178 scale-change note: {'B178_SCALE_CHANGE_NOTE_START' in html}
- B178 area caveat: {'B178_AREA_CAVEAT_START' in html}
- B179 bottleneck graphic: {'B179_BOTTLENECK_GRAPHIC_START' in html}
- B181 closing counterpoint: {'B181_CLOSING_COUNTERPOINT_START' in html}
- No Felt token: {'felt' not in html.lower()}
- No OpenStreetMap token: {'openstreetmap' not in html.lower()}
- No iframe: {'<iframe' not in html.lower()}

Result: {'PASS' if not fails else 'CHECK FAILS BEFORE RELEASE'}
"""
    if fails:
        audit += "\nFailures:\n"
        for r in fails:
            audit += f"- {r['label']}: {r['detail']}\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B182 final QA and v2.1.0 release prep complete.")
    print("Audit only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B182_final_qa_and_v2_1_0_release.md")
    print("  docs/B182_final_qa_and_v2_1_0_release_audit.txt")
    print("  docs/B182_release_signals.csv")
    print("  docs/B182_v2_1_0_release_checklist.md")
    print("  docs/B182_v2_1_0_release_notes.md")
    print("  tasks/done.md")
    print(f"Signals: PASS={len(passes)} WARN={len(warns)} FAIL={len(fails)}")
    print("Next: run B177, B103b and B58 one final time.")


if __name__ == "__main__":
    main()
