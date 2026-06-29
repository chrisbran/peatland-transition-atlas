#!/usr/bin/env python3
# B126 - Publication wording polish

from __future__ import annotations

from datetime import date
from pathlib import Path
import html as html_lib
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CENTRAL_JS = ROOT / "src" / "central_global_map_story.js"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b126_publication_wording_polish"

REPORT = DOCS / "B126_publication_wording_polish.md"
AUDIT = DOCS / "B126_publication_wording_polish_audit.txt"
TODAY = date.today().isoformat()

NAV_ITEMS = [
    ("#problem", "Problem"),
    ("#centralGlobalMapStory", "Karten"),
    ("#b79RegionalImplementation", "Oberschwaben"),
    ("#transitionLogic", "Prüfpfade"),
    ("#quellen-methodik", "Quellen"),
]

CENTRAL_STEPS = {
    "europe-borders": (
        "Europa zeigt den größeren Bezugsraum.",
        "Moorbodenschutz ist eine regionale Aufgabe, steht aber in einem europäischen Zusammenhang von Nutzung, Entwässerung und Klimazielen.",
    ),
    "europe-peat": (
        "Planung muss Landschaftsräume mitdenken.",
        "Moor- und Feuchtbodenkontexte lassen sich nicht allein aus Verwaltungsgrenzen ableiten.",
    ),
    "germany-context": (
        "Deutschland grenzt den Prüfbedarf ein.",
        "Die nationale Kulisse zeigt, wo organische Böden in größerem Zusammenhang auftreten und wo Länder und Regionen genauer hinsehen müssen.",
    ),
    "germany-thuenen-extent": (
        "Organische Böden markieren potenzielle Konflikträume.",
        "Wo Nutzung, Entwässerung und organische Böden zusammenkommen, entsteht Prüfbedarf für Klimaschutz, Wasserstand und Bewirtschaftung.",
    ),
    "germany-thuenen-types": (
        "Die nationale Kulisse ersetzt keine Standortprüfung.",
        "Sie zeigt, wo genauer hingesehen werden muss. Welche Nutzungspfade tragfähig sind, entscheidet sich erst mit Wasserstand, Nutzung, Eigentum und regionaler Koordination.",
    ),
    "bw-context": (
        "Baden-Württemberg macht die Frage regional konkret.",
        "Hier wird sichtbar, wo Moor- und Feuchtbodenkontexte auf Nutzung, Zuständigkeiten und regionale Planung treffen.",
    ),
    "bw-bk50-extent": (
        "Der Bodenkontext zeigt, wo Prüfung beginnt.",
        "Moor- und Feuchtbodenbereiche markieren Räume, in denen Wasserstand, Nutzung und Standortbedingungen gemeinsam bewertet werden müssen.",
    ),
}

OBERSCHWABEN_STEPS = {
    "region": (
        "Vier Landkreise als Fokusraum",
        "Biberach, Ravensburg, Sigmaringen und Bodenseekreis.",
    ),
    "moor-context": (
        "Moor-/Feuchtbodenkontexte liegen quer zur Nutzung",
        "Sie markieren Räume, in denen Boden, Wasserstand und heutige Bewirtschaftung gemeinsam geprüft werden müssen.",
    ),
}

GENERIC_REPLACEMENTS = [
    ("Fachliche Klammer", "Grundlagen"),
    ("Warum Wasserstand über Klimawirkung entscheidet", "Warum Wasserstand entscheidend ist"),
    ("Fachliche Grundlage:", "Grundlagen:"),
    ("Fachliche Einordnung:", "Grundlagen:"),
    ("Grundlage:", "Grundlagen:"),
    ("Lesart der Thünen-Kulisse", "Einordnung der nationalen Kulisse"),
    ("Lesart:", "Hinweis:"),
    ("Daten: ", "Datenbasis: "),
    ("<h3>Fachliche Grundlagen</h3>", "<h3>Grundlagen</h3>"),
    (">Fachliche Grundlagen<", ">Grundlagen<"),
]

FLAECHEN_REPLACEMENTS = [
    ("Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.\nWerte gerundet.\nWerte gerundet.", "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet."),
    ("Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen. Werte gerundet. Werte gerundet.", "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet."),
    ("Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.\nWerte gerundet.", "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet."),
    ("Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen. Werte gerundet.", "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet."),
    ("Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.", "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet."),
]

REQUIRED_PATTERNS = [
    "Karten",
    "Prüfpfade",
    "Quellen",
    "Warum Wasserstand entscheidend ist",
    "Datenbasis:",
    "Hinweis:",
    "Europa zeigt den größeren Bezugsraum.",
    "Planung muss Landschaftsräume mitdenken.",
    "Deutschland grenzt den Prüfbedarf ein.",
    "Organische Böden markieren potenzielle Konflikträume.",
    "Die nationale Kulisse ersetzt keine Standortprüfung.",
    "Baden-Württemberg macht die Frage regional konkret.",
    "Der Bodenkontext zeigt, wo Prüfung beginnt.",
    "Vier Landkreise als Fokusraum",
    "Biberach, Ravensburg, Sigmaringen und Bodenseekreis.",
    "Moor-/Feuchtbodenkontexte liegen quer zur Nutzung",
    "Sie markieren Räume, in denen Boden, Wasserstand und heutige Bewirtschaftung gemeinsam geprüft werden müssen.",
    "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet.",
]

RISK_PATTERNS = [
    "Fachliche Klammer",
    "Fachliche Grundlage:",
    "Fachliche Einordnung:",
    "Lesart",
    "Daten: ",
    "Grundlage:",
    "Europa zeigt den politischen Maßstab.",
    "Politische und administrative Grenzen bestimmen",
    "Moorvorkommen überschreiten Grenzen.",
    "Moorlandschaften folgen Landschaft und Hydrologie",
    "Deutschland zeigt, wo Planung und Förderung ansetzen.",
    "Nationale Karten zeigen, wo Förderprogramme",
    "Die Thünen-Kulisse zeigt organische Böden.",
    "Sie zeigt, wo Moor- und organische Böden in der Bundesplanung eine Rolle spielen.",
    "Die Thünen-Kulisse bleibt die relevante Deutschlandkarte.",
    "Für diese Maßstabsebene wird keine zweite kaum unterscheidbare Bodentyp-Karte gezeigt.",
    "Baden-Württemberg macht die Frage räumlich konkret.",
    "Auf regionaler Ebene zeigt sich",
    "BK50 ordnet den Bodenkontext ein.",
    "Sie zeigt Moor- und Feuchtbodenbereiche, ersetzt aber keine Eignungsprüfung.",
    "Vier Landkreise als Planungsraum",
    "Die Karte beginnt bewusst mit Orientierung",
    "Die BK50-basierte Ebene",
    "Werte gerundet. Werte gerundet.",
    "Ackerland ohne separat geführte Stilllegung und unklare Zuordnungen.",
    "GLOBAL_FRAME_V1",
    "Thuenen",
    "Ã",
    "�",
]


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


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def replace_first_tag(block: str, tag: str, new_inner: str) -> tuple[str, int]:
    pattern = rf"<{tag}>(.*?)</{tag}>"
    repl = f"<{tag}>{new_inner}</{tag}>"
    return re.subn(pattern, repl, block, count=1, flags=re.DOTALL)


def replace_article_step(html: str, attr_name: str, state: str, title: str, body: str) -> tuple[str, int]:
    pattern = rf'(<article\b[^>]*\b{re.escape(attr_name)}="{re.escape(state)}"[^>]*>.*?</article>)'
    m = re.search(pattern, html, flags=re.DOTALL)
    if not m:
        return html, 0

    block = m.group(1)
    new_block, h3_hits = replace_first_tag(block, "h3", title)
    new_block, p_hits = replace_first_tag(new_block, "p", body)

    if new_block == block:
        return html, 0

    return html[:m.start()] + new_block + html[m.end():], h3_hits + p_hits


def patch_nav(html: str) -> tuple[str, int]:
    nav_html = "\n".join([f'    <a href="{href}">{label}</a>' for href, label in NAV_ITEMS])
    nav_pattern = r"(<nav\b[^>]*>)(.*?)(</nav>)"
    matches = list(re.finditer(nav_pattern, html, flags=re.DOTALL | re.IGNORECASE))
    if matches:
        m = matches[0]
        new_nav = m.group(1) + "\n" + nav_html + "\n  " + m.group(3)
        return html[:m.start()] + new_nav + html[m.end():], 1

    original = html
    html = html.replace('<a href="#centralGlobalMapStory">Kartenfolge</a>', '<a href="#centralGlobalMapStory">Karten</a>')
    html = html.replace('<a href="#b79RegionalImplementation">Region</a>', '<a href="#b79RegionalImplementation">Oberschwaben</a>')
    html = re.sub(r'<a href="[^"]*">Pfade</a>', '<a href="#transitionLogic">Prüfpfade</a>', html, count=1)
    html = re.sub(r'<a href="[^"]*">Methode</a>', '<a href="#quellen-methodik">Quellen</a>', html, count=1)
    return html, 1 if html != original else 0


def apply_replacements(text: str, replacements: list[tuple[str, str]]) -> tuple[str, int]:
    hits = 0
    for old, new in replacements:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            hits += n
    return text, hits


def patch_files() -> dict[str, int]:
    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)

    backup(INDEX)
    backup(CENTRAL_JS)

    counters = {
        "nav_hits": 0,
        "generic_html_hits": 0,
        "generic_js_hits": 0,
        "central_index_step_hits": 0,
        "oberschwaben_step_hits": 0,
        "central_js_title_hits": 0,
        "flaechen_hits": 0,
    }

    html, counters["nav_hits"] = patch_nav(html)

    html, n = apply_replacements(html, GENERIC_REPLACEMENTS)
    counters["generic_html_hits"] += n
    js, n = apply_replacements(js, GENERIC_REPLACEMENTS)
    counters["generic_js_hits"] += n

    html, n = apply_replacements(html, FLAECHEN_REPLACEMENTS)
    counters["flaechen_hits"] += n
    html, n = re.subn(
        r"Hinweis:\s*Stilllegung und unklare Zuweisungen sind separat ausgewiesen;\s*Werte gerundet\.\s*Werte gerundet\.",
        "Hinweis: Stilllegung und unklare Zuweisungen sind separat ausgewiesen; Werte gerundet.",
        html,
    )
    counters["flaechen_hits"] += n

    for state, (title, body) in CENTRAL_STEPS.items():
        html, n = replace_article_step(html, "data-global-state", state, title, body)
        counters["central_index_step_hits"] += n

    for state, (title, body) in OBERSCHWABEN_STEPS.items():
        html, n = replace_article_step(html, "data-state", state, title, body)
        counters["oberschwaben_step_hits"] += n

    for state, (title, _body) in CENTRAL_STEPS.items():
        pattern = rf'("{re.escape(state)}":\s*\{{.*?title:\s*")[^"]*(")'
        new_js, n = re.subn(pattern, rf'\1{title}\2', js, flags=re.DOTALL)
        if n:
            js = new_js
            counters["central_js_title_hits"] += n

    js = js.replace('mode: "Lesart",', 'mode: "Einordnung",')
    js = js.replace('mode: "Lesart der Thünen-Kulisse",', 'mode: "Einordnung der nationalen Kulisse",')

    write_text(INDEX, html)
    write_text(CENTRAL_JS, js)

    return counters


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B126 - Publication wording polish"
    if marker in current:
        return
    entry = f"""
## B126 - Publication wording polish ({TODAY})

- Updated header navigation to `Problem · Karten · Oberschwaben · Prüfpfade · Quellen`.
- Replaced internal wording such as `Fachliche Klammer` and avoided `Lesart`.
- Standardized short prefixes to `Datenbasis:`, `Grundlagen:` and `Hinweis:`.
- Rewrote central map steps 05–11 around planning relevance and Prüfbedarf instead of map-type explanations.
- Shortened Oberschwaben region and soil-context step cards.
- Removed duplicate `Werte gerundet` wording in the Oberschwaben area balance.
- Did not modify maps, data, CSS or scrolly mechanics.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(counters: dict[str, int]) -> dict[str, object]:
    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)
    combined_visible = visible_text(html)
    combined_raw = html + "\n" + js

    required_counts = {p: combined_raw.count(p) for p in REQUIRED_PATTERNS}
    visible_risk_counts = {p: combined_visible.count(p) for p in RISK_PATTERNS}
    raw_risk_counts = {p: combined_raw.count(p) for p in RISK_PATTERNS}

    nav_ok = all(f'<a href="{href}">{label}</a>' in html for href, label in NAV_ITEMS)

    return {
        "required_counts": required_counts,
        "visible_risk_counts": visible_risk_counts,
        "raw_risk_counts": raw_risk_counts,
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "visible_risk_findings": sum(1 for v in visible_risk_counts.values() if v > 0),
        "raw_risk_findings": sum(1 for v in raw_risk_counts.values() if v > 0),
        "nav_ok": nav_ok,
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = result["missing_required"] == 0 and result["visible_risk_findings"] == 0 and result["nav_ok"]
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B126 – Publication Wording Polish",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B126 schärft die öffentliche Fachkommunikation: weniger Projektlogik, mehr fachliche Aussage und Prüfbedarf.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Navigation OK: {result['nav_ok']}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B126_publication_wording_polish_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\central_global_map_story.js -Pattern \"Problem\",\"Karten\",\"Oberschwaben\",\"Prüfpfade\",\"Quellen\",\"Fachliche Klammer\",\"Lesart\",\"Daten: \",\"Fachliche Grundlage:\",\"Europa zeigt den größeren Bezugsraum\",\"Deutschland grenzt den Prüfbedarf ein\",\"Die nationale Kulisse ersetzt keine Standortprüfung\",\"Werte gerundet. Werte gerundet\",\"Ackerland ohne separat\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B126 publication wording polish audit",
        "",
        f"- Status: {status}",
        f"- Navigation OK: {result['nav_ok']}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
        "",
        "## Replacement counters",
        "",
        "| Counter | Count |",
        "|---|---:|",
    ]
    for k, v in result["counters"].items():
        audit_lines.append(f"| `{k}` | {v} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["required_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Visible risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["visible_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Raw risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["raw_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)
    if not CENTRAL_JS.exists():
        print(f"Missing {rel(CENTRAL_JS)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    counters = patch_files()
    update_done()
    result = audit(counters)
    write_docs(result)

    ok = result["missing_required"] == 0 and result["visible_risk_findings"] == 0 and result["nav_ok"]

    print("B126 publication wording polish complete.")
    print("Changed/created:")
    for p in [INDEX, CENTRAL_JS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Navigation OK: {result['nav_ok']}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['visible_risk_findings']}")
    print(f"Raw risk findings: {result['raw_risk_findings']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B126_publication_wording_polish_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
