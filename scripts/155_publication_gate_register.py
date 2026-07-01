from pathlib import Path
from datetime import date
import csv
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "155_publication_gate_register.py"
DOC = ROOT / "docs" / "B155_publication_gate_register.md"
CSV_OUT = ROOT / "docs" / "B155_publication_gate_register.csv"
AUDIT = ROOT / "docs" / "B155_publication_gate_register_audit.txt"
DONE = ROOT / "tasks" / "done.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def contains_any(text: str, needles: list[str]) -> bool:
    low = text.lower()
    return any(n.lower() in low for n in needles)


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.I))


def gate_status(found: bool, ok_text: str = "vorhanden", open_text: str = "offen") -> str:
    return ok_text if found else open_text


def update_done(done_text: str, today: str) -> str:
    line = f"- B155 publication gate register: documented remaining publication gates for Felt, legal notices, source/method status and project disclaimer ({today})."
    if "B155 publication gate register" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    today = date.today().isoformat()

    checks = {
        "scope_box": contains_any(html, ["Fachlicher Demonstrator, keine Eignungskarte"]),
        "no_suitability_language": contains_any(html, ["keine Eignungskarte", "keine parzellenscharfe Eignungs"]),
        "method_short": contains_any(html, ["Methode in Kürze"]),
        "central_sources": contains_any(html, ["Quellen, Methodik und Nutzungsrechte"]),
        "felt_notice": contains_any(html, ["Drittanbieter-Hinweis", "Die interaktive Karte wird über Felt geladen"]),
        "felt_source_register": contains_any(html, ["Interaktive Oberschwaben-Karte", "Felt-Embed"]),
        "osm_notice": contains_any(html, ["OpenStreetMap"]),
        "fiona_bk50_gisco": contains_any(html, ["FIONA 2024"]) and contains_any(html, ["BK50"]) and contains_any(html, ["GISCO"]),
        "area_19900": contains_any(html, ["~19.900 ha", "19.900 ha", "19867"]),
        "solamo_disclaimer": contains_any(html, ["SOLAMO-BW", "kein offizielles Produkt"]),
        "impressum_privacy_words": contains_any(html, ["Impressum"]) and contains_any(html, ["Datenschutz"]),
        "b152_felt_framing": contains_any(html, ["Interaktive Vertiefung", "Die statische Karte zeigt die Lage"]),
    }

    gates = [
        {
            "gate": "Scope / Nicht-Eignungskarte",
            "status": gate_status(checks["scope_box"] and checks["no_suitability_language"], "inhaltlich gesetzt", "prüfen"),
            "evidence": "Scope-Box und wiederholte Hinweise auf keine Eignungs-/Priorisierungskarte",
            "next_action": "Nur noch auf Konsistenz achten; keine neuen decision-tool Formulierungen einführen.",
            "commit_relevance": "public",
        },
        {
            "gate": "Methode / Quellen",
            "status": gate_status(checks["method_short"] and checks["central_sources"] and checks["fiona_bk50_gisco"], "weitgehend gesetzt", "prüfen"),
            "evidence": "Methode in Kürze, Quellenregister, FIONA/BK50/GISCO-Hinweise",
            "next_action": "Final gegen Datenherkunft und Rundungslogik lesen.",
            "commit_relevance": "public",
        },
        {
            "gate": "19.900-ha-Zahl",
            "status": gate_status(checks["area_19900"], "sichtbar, methodisch noch final zu bestätigen", "offen"),
            "evidence": "~19.900 ha bzw. 19867-ha-Basiswert aus Verschneidung",
            "next_action": "Finale Methodennotiz ergänzen: Rundung, Geometrievereinfachung nicht für Flächenbilanz, FIONA/BK50/GISCO-Versionen.",
            "commit_relevance": "publication",
        },
        {
            "gate": "Felt / Drittanbieter",
            "status": gate_status(checks["felt_notice"] and checks["felt_source_register"] and checks["osm_notice"], "technisch und textlich vorbereitet", "offen"),
            "evidence": "Felt-Block, Drittanbieter-Hinweis, OpenStreetMap-Hinweis, Quellenregister",
            "next_action": "Felt-Plan/Lizenz nach Trial und Datenschutztext rechtlich/praktisch klären.",
            "commit_relevance": "publication",
        },
        {
            "gate": "Mobile / Responsive Felt",
            "status": gate_status(checks["b152_felt_framing"], "gesetzt", "prüfen"),
            "evidence": "Desktop-iframe plus Mobile-Fallback/Link-Strategie",
            "next_action": "Vor Veröffentlichung einmal 390 px und Tablet prüfen; iframe darf mobil nicht dominieren.",
            "commit_relevance": "public",
        },
        {
            "gate": "Hohenheim / SOLAMO-BW Kontext",
            "status": gate_status(checks["solamo_disclaimer"], "Hinweis vorhanden, Freigabe offen", "offen"),
            "evidence": "Footer: Kontext SOLAMO-BW / Universität Hohenheim; eigenständiger Demonstrator, kein offizielles Produkt",
            "next_action": "Freigabe/Disclaimer intern klären; ggf. präzisere Formulierung mit Projektleitung abstimmen.",
            "commit_relevance": "publication",
        },
        {
            "gate": "Impressum / Datenschutz",
            "status": gate_status(checks["impressum_privacy_words"], "Text/Linkwörter vorhanden, Zielseiten prüfen", "offen"),
            "evidence": "Impressum · Datenschutz im Footer erkannt",
            "next_action": "Prüfen, ob echte Zielseiten/Links vorhanden sind und ob Felt dort erwähnt werden muss.",
            "commit_relevance": "publication",
        },
        {
            "gate": "Git-/Datenhygiene",
            "status": "laufend",
            "evidence": "Raw-GIS-Dateien dürfen nicht in Commit; Felt-GeoJSON bleibt außerhalb public/repo",
            "next_action": "Weiterhin nur explizite Dateien stagen; kein git add .; working/ und raw GIS nicht committen.",
            "commit_relevance": "process",
        },
    ]

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gate", "status", "evidence", "next_action", "commit_relevance"],
        )
        writer.writeheader()
        writer.writerows(gates)

    md = []
    md.append("# B155 - Publication Gate Register")
    md.append("")
    md.append(f"Date: {today}")
    md.append("")
    md.append("## Ziel")
    md.append("")
    md.append("B155 bündelt nach der Felt-Integration die verbleibenden Veröffentlichungsgates.")
    md.append("Der Patch verändert die öffentliche Seite nicht. Er dokumentiert, was vor einer finalen V2-Veröffentlichung fachlich, rechtlich und prozessual noch zu prüfen ist.")
    md.append("")
    md.append("## Kurzfazit")
    md.append("")
    md.append("Die fachliche Story ist nach B152/B154 deutlich stabiler: Scope, Methodik, Oberschwaben-Rahmung, Felt-Vertiefung und Wertschöpfungsthese sind gesetzt.")
    md.append("Offen sind vor allem Veröffentlichungssicherheit, nicht Story-Substanz.")
    md.append("")
    md.append("## Gate-Übersicht")
    md.append("")
    md.append("| Gate | Status | Nächste Aktion |")
    md.append("|---|---|---|")
    for g in gates:
        md.append(f"| {g['gate']} | {g['status']} | {g['next_action']} |")
    md.append("")
    md.append("## Priorität vor Veröffentlichung")
    md.append("")
    md.append("### Muss vor Live-Freigabe geklärt sein")
    md.append("")
    md.append("1. **Impressum/Datenschutz:** echte Zielseiten oder verlässliche Links, inklusive Drittanbieter-/Felt-Hinweis.")
    md.append("2. **Felt-Lizenz/Plan:** Klären, ob Embed nach Trial stabil und zulässig bleibt.")
    md.append("3. **Hohenheim/SOLAMO-BW-Disclaimer:** Formulierung intern freigeben lassen.")
    md.append("4. **19.900-ha-Methodennotiz:** Rundung und Datenstand final absichern.")
    md.append("")
    md.append("### Sollte vor finaler Version geprüft werden")
    md.append("")
    md.append("1. Mobile 390 px und Tablet mit echtem Felt-Embed testen.")
    md.append("2. Letzter sichtbarer Wording-Pass auf Wiederholungen von `Umsetzung`.")
    md.append("3. Quellenregister gegen finale sichtbare Aussagen lesen.")
    md.append("4. Git-Status vor Commit auf raw GIS/GeoJSON prüfen.")
    md.append("")
    md.append("## Aktuelle automatische Indikatoren aus index.html")
    md.append("")
    md.append("| Indikator | Erkannt |")
    md.append("|---|---:|")
    for key, value in checks.items():
        md.append(f"| `{key}` | {str(value)} |")
    md.append("")
    md.append("## Entscheidung")
    md.append("")
    md.append("Bis zur Klärung der Veröffentlichungsgates bleibt der Felt-Block ein integrierter, aber reversibel gehaltener Kartenbaustein.")
    md.append("Die bestehende statische Oberschwaben-Karte bleibt als Story- und Fallback-Komponente erhalten.")
    md.append("")
    md.append("## Dateien")
    md.append("")
    md.append(f"- CSV-Register: `docs/{CSV_OUT.name}`")
    write(DOC, "\n".join(md) + "\n")

    audit_text = f"""# B155 publication gate register audit

Date: {today}

Result: DOCUMENTATION ONLY. No public page files changed.

Automatic indicators from index.html:

- scope_box: {checks['scope_box']}
- no_suitability_language: {checks['no_suitability_language']}
- method_short: {checks['method_short']}
- central_sources: {checks['central_sources']}
- felt_notice: {checks['felt_notice']}
- felt_source_register: {checks['felt_source_register']}
- osm_notice: {checks['osm_notice']}
- fiona_bk50_gisco: {checks['fiona_bk50_gisco']}
- area_19900: {checks['area_19900']}
- solamo_disclaimer: {checks['solamo_disclaimer']}
- impressum_privacy_words: {checks['impressum_privacy_words']}
- b152_felt_framing: {checks['b152_felt_framing']}

Created/updated:

- docs/B155_publication_gate_register.md
- docs/B155_publication_gate_register.csv
- docs/B155_publication_gate_register_audit.txt
- tasks/done.md
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B155 publication gate register complete.")
    print("Documentation only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B155_publication_gate_register.md")
    print("  docs/B155_publication_gate_register.csv")
    print("  docs/B155_publication_gate_register_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
