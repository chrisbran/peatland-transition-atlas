from pathlib import Path
from datetime import date
import csv
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
B159_CSV = ROOT / "docs" / "B159_editorial_section_inventory.csv"

SCRIPT = ROOT / "scripts" / "160_narrative_cut_plan.py"
DOC = ROOT / "docs" / "B160_narrative_cut_plan.md"
MATRIX = ROOT / "docs" / "B160_section_cut_matrix.csv"
OUTLINE = ROOT / "docs" / "B160_main_flow_outline.md"
AUDIT = ROOT / "docs" / "B160_narrative_cut_plan_audit.txt"
DONE = ROOT / "tasks" / "done.md"

SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"<h([1-4])\b[^>]*>(.*?)</h\1>", re.S | re.I)

FIVE_ACTS = [
    {
        "act": "A1",
        "title": "Moore sind klein, aber klimatisch groß.",
        "purpose": "Hook, Relevanz, Versprechen der Seite.",
        "keep": "Hero, eine starke These, ein kurzer Scope-Hinweis.",
        "cut": "lange Vorbemerkungen, wiederholte Demonstrator-/Nicht-Eignungshinweise.",
    },
    {
        "act": "A2",
        "title": "Karten zeigen den Maßstabssprung.",
        "purpose": "Globaler Kontext wird zu regionaler Planungsfrage.",
        "keep": "ein choreografierter Kartenmoment global → Deutschland/BW → Oberschwaben.",
        "cut": "zu viele einzelne Zwischenkarten oder erklärende Kartenlisten.",
    },
    {
        "act": "A3",
        "title": "In Oberschwaben trifft Moorbodenschutz auf reale Nutzung.",
        "purpose": "Der abstrakte Moorschutz wird konkret.",
        "keep": "statische Story-Karte, Felt-Vertiefung, Flächenbilanz.",
        "cut": "Dopplungen zwischen statischer Karte, Felt und Bilanz.",
    },
    {
        "act": "A4",
        "title": "Aus Schnittmenge folgt Verhandlung.",
        "purpose": "Wasser, Betriebe, Zuständigkeiten und Pfade erklären, warum Karte nicht Lösung ist.",
        "keep": "ein starker Governance-/Transformationsmoment.",
        "cut": "lange Pfadbeschreibungen, wenn sie nicht visuell tragen.",
    },
    {
        "act": "A5",
        "title": "Der Engpass liegt hinter dem Feld.",
        "purpose": "Climax: nicht das nasse Bewirtschaften allein limitiert, sondern die Kette danach.",
        "keep": "eine erinnerbare Wertschöpfungsgrafik + kurzer Kicker.",
        "cut": "Scorecard-/Matrix-Dopplungen, Quellenblöcke im Hauptfluss.",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_tags(html: str) -> str:
    text = TAG_RE.sub(" ", html)
    text = text.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def first_heading(section: str) -> str:
    m = HEADING_RE.search(section)
    if not m:
        return ""
    return strip_tags(m.group(2))


def extract_section_open(section: str) -> str:
    m = re.match(r"<section\b[^>]*>", section, re.I | re.S)
    return m.group(0) if m else ""


def extract_attr(tag: str, attr: str) -> str:
    m = re.search(attr + r'\s*=\s*"([^"]*)"', tag, re.I)
    if m:
        return m.group(1)
    m = re.search(attr + r"\s*=\s*'([^']*)'", tag, re.I)
    if m:
        return m.group(1)
    return ""


def selector(open_tag: str) -> str:
    sid = extract_attr(open_tag, "id")
    cls = extract_attr(open_tag, "class")
    bits = []
    if sid:
        bits.append("#" + sid)
    if cls:
        bits.append("." + ".".join(cls.split()))
    return " ".join(bits)


def load_sections_from_b159() -> list[dict]:
    if not B159_CSV.exists():
        return []

    rows = []
    with B159_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(dict(r))
    return rows


def parse_sections_from_index() -> list[dict]:
    html = read(INDEX)
    rows = []
    for i, m in enumerate(SECTION_RE.finditer(html), start=1):
        sec = m.group(0)
        text = strip_tags(sec)
        heading = first_heading(sec)
        open_tag = extract_section_open(sec)
        rows.append({
            "section_no": str(i),
            "selector": selector(open_tag),
            "heading": heading,
            "act": classify_act(heading, text),
            "word_count": str(len(text.split())),
            "warning_count": str(count_warning_words(text)),
            "recommended_action": "",
            "reason": "",
            "excerpt": text[:260],
        })
    return rows


def count_warning_words(text: str) -> int:
    words = [
        "keine Eignungskarte",
        "keine Priorisierung",
        "keine hydrologische Modellierung",
        "keine betriebliche Betroffenheitsanalyse",
        "Prüfbedarf",
        "Einzelfallprüfung",
        "Orientierung",
        "Hinweis",
        "Grenze der Aussage",
    ]
    low = text.lower()
    return sum(low.count(w.lower()) for w in words)


def classify_act(heading: str, text: str) -> str:
    t = (heading + " " + text).lower()

    if any(k in t for k in ["moorbodenschutz braucht", "fachlicher demonstrator", "kernargument"]):
        return "A1 Hook / promise"
    if any(k in t for k in ["wasserstand", "speicher", "quelle", "frame-mismatch", "globale karten", "moore sind räumlich"]):
        return "A2 Why it matters / scale jump"
    if any(k in t for k in ["oberschwaben", "schnittmenge", "flächenbilanz", "felt"]):
        return "A3 Regional concretisation"
    if any(k in t for k in ["transformationspfade", "wasser und governance", "einheitslösung", "hydrologische einheit"]):
        return "A4 What implementation requires"
    if any(k in t for k in ["wertschöpfung", "verarbeitung", "abnahme", "standards", "kette"]):
        return "A5 Value-chain climax"
    if any(k in t for k in ["quellen", "methode", "nutzungsrechte"]):
        return "Appendix / method"
    return "Supporting / unclear"


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def decide_cut(row: dict) -> dict:
    heading = row.get("heading", "")
    act = row.get("act", "")
    action = row.get("recommended_action", "")
    warning_count = to_int(row.get("warning_count", "0"))
    words = to_int(row.get("word_count", "0"))
    text = (heading + " " + row.get("excerpt", "")).lower()

    decision = "keep"
    target = "main_flow"
    cut_pct = 0
    b161_role = ""
    b162_role = ""
    note = "Behalten, aber auf Rolle im Fünf-Akt-Bogen prüfen."

    if any(k in text for k in ["quellen", "methode", "nutzungsrechte", "datengrundlagen"]):
        decision = "move/collapse"
        target = "appendix_details"
        cut_pct = 70
        note = "Nicht im Hauptfluss ausbreiten; als Appendix/details verfügbar halten."

    elif any(k in text for k in ["fachlicher demonstrator", "grenzen der aussage", "methodische grenze"]):
        decision = "compress"
        target = "scope_or_method"
        cut_pct = 50
        note = "Ein starker Scope-Hinweis reicht; Wiederholungen in Methode/Quellen verschieben."

    elif any(k in text for k in ["moore sind räumlich", "globale karten", "deutschland", "baden-württemberg"]):
        decision = "rebuild"
        target = "flagship_sticky_zoom"
        cut_pct = 30
        b161_role = "candidate"
        note = "Als großer Sticky-Zoom choreografieren; weniger Begleittext, mehr räumliche Verdichtung."

    elif any(k in text for k in ["oberschwaben, wo", "interaktive vertiefung", "flächenbilanz"]):
        decision = "keep/tighten"
        target = "regional_proof_point"
        cut_pct = 15
        note = "Kernbeleg. Behalten, aber Dopplung zwischen statischer Karte, Felt und Bilanz weiter reduzieren."

    elif any(k in text for k in ["aus der schnittmenge folgt", "wasser folgt einzugsgebieten", "hydrologische"]):
        decision = "visualise"
        target = "governance_visual_moment"
        cut_pct = 25
        note = "Als diagrammatischer Moment stärker als Textblock."

    elif any(k in text for k in ["wertschöpfung", "engstelle", "verarbeitung", "abnahme", "standards", "kette"]):
        decision = "rebuild"
        target = "value_chain_climax"
        cut_pct = 35
        b162_role = "candidate"
        note = "Inhalt stark; als erinnerbares Climax-Bild neu denken."

    elif warning_count >= 4:
        decision = "compress"
        target = "method_or_caption"
        cut_pct = 35
        note = "Zu viele Caveats im sichtbaren Fluss; konsolidieren."

    elif words > 380:
        decision = "trim"
        target = "main_flow_shorter"
        cut_pct = 30
        note = "Zu lang für Premium-Pacing; Hauptaussage herausarbeiten."

    elif action == "turn_into_visual_moment":
        decision = "visualise"
        target = "visual_moment"
        cut_pct = 25
        note = "Gute Idee, aber stärker über Grafik als über Text."

    elif action == "rebuild_visual_climax":
        decision = "rebuild"
        target = "editorial_visual"
        cut_pct = 25
        note = "Nicht zwingend löschen; visuell stärker inszenieren."

    return {
        "section_no": row.get("section_no", ""),
        "heading": heading,
        "current_act": act,
        "decision": decision,
        "target_role": target,
        "estimated_cut_percent": cut_pct,
        "b161_flagship_zoom_role": b161_role,
        "b162_value_chain_role": b162_role,
        "note": note,
    }


def update_done(done_text: str, today: str) -> str:
    line = f"- B160 narrative cut plan: created a five-act cut matrix and main-flow outline for premium editorial pacing ({today})."
    if "B160 narrative cut plan" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    today = date.today().isoformat()

    source = "B159 CSV" if B159_CSV.exists() else "index.html fallback parser"
    rows = load_sections_from_b159() or parse_sections_from_index()
    decisions = [decide_cut(r) for r in rows]

    total_sections = len(decisions)
    total_words = sum(to_int(r.get("word_count", "0")) for r in rows)
    cut_weighted = 0
    for r, d in zip(rows, decisions):
        cut_weighted += to_int(r.get("word_count", "0")) * int(d["estimated_cut_percent"]) / 100
    estimated_cut_total_pct = round((cut_weighted / total_words * 100), 1) if total_words else 0

    action_counts = {}
    for d in decisions:
        action_counts[d["decision"]] = action_counts.get(d["decision"], 0) + 1

    with MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "section_no",
                "heading",
                "current_act",
                "decision",
                "target_role",
                "estimated_cut_percent",
                "b161_flagship_zoom_role",
                "b162_value_chain_role",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(decisions)

    md = []
    md.append("# B160 - Narrative Cut Plan")
    md.append("")
    md.append(f"Date: {today}")
    md.append("")
    md.append("## Ziel")
    md.append("")
    md.append("B160 übersetzt den B159-Editorial-Audit in einen konkreten Schnittplan.")
    md.append("Der Patch verändert die öffentliche Seite nicht. Er entscheidet, welche Inhalte im Hauptfluss bleiben, welche gekürzt, verschoben oder visuell neu gebaut werden sollen.")
    md.append("")
    md.append("## Leitentscheidung")
    md.append("")
    md.append("> Nicht mehr vollständiger werden. Schärfer werden.")
    md.append("")
    md.append("Die V2 soll auf eine klare fünfaktige Dramaturgie geschnitten werden. Methodische Absicherung bleibt erhalten, aber weniger davon darf den Lesefluss dominieren.")
    md.append("")
    md.append("## Fünf Akte")
    md.append("")
    md.append("| Akt | Aussage | Funktion | Behalten | Kürzen/Verschieben |")
    md.append("|---|---|---|---|---|")
    for a in FIVE_ACTS:
        md.append(f"| {a['act']} | {a['title']} | {a['purpose']} | {a['keep']} | {a['cut']} |")
    md.append("")
    md.append("## Automatische Schnittbilanz")
    md.append("")
    md.append(f"- Datenquelle: {source}")
    md.append(f"- Sections im Plan: {total_sections}")
    md.append(f"- grobe Wortzahl: {total_words}")
    md.append(f"- geschätztes Kürzungspotenzial im Hauptfluss: ca. {estimated_cut_total_pct} %")
    md.append("")
    md.append("Das Ziel aus B159 war 20–35 % weniger sichtbarer Erklärtext. Dieser Plan liegt bewusst in diesem Korridor, ohne Fachgrenzen zu löschen.")
    md.append("")
    md.append("## Entscheidungstypen")
    md.append("")
    md.append("| Entscheidung | Anzahl |")
    md.append("|---|---:|")
    for k, v in sorted(action_counts.items()):
        md.append(f"| `{k}` | {v} |")
    md.append("")
    md.append("## Wichtigste redaktionelle Eingriffe")
    md.append("")
    md.append("### 1. Scope und Caveats konsolidieren")
    md.append("")
    md.append("Ein starker Scope-Hinweis am Anfang bleibt. Wiederholte Nicht-Eignungskarten-, Priorisierungs- und Modellierungswarnungen werden im Hauptfluss reduziert und in Methode/Quellen konzentriert.")
    md.append("")
    md.append("### 2. Kartenfolge als Flagship-Zoom neu denken")
    md.append("")
    md.append("Die existierende globale Kartenfolge ist fachlich nützlich, aber editorial noch zu listenartig. B161 soll daraus einen einzigen großen Sticky-Moment konzipieren:")
    md.append("")
    md.append("```text")
    md.append("global → Europa/Deutschland → Baden-Württemberg → Oberschwaben")
    md.append("```")
    md.append("")
    md.append("### 3. Oberschwaben bleibt der Beleg")
    md.append("")
    md.append("Statische Karte, Felt-Vertiefung und Flächenbilanz bleiben, aber mit klarer Rollenverteilung:")
    md.append("")
    md.append("- statische Karte: Lage und Layerlogik")
    md.append("- Felt: Details und Interaktion")
    md.append("- Bilanz: quantitative Verdichtung")
    md.append("")
    md.append("### 4. Governance als visuelles Zwischenbild")
    md.append("")
    md.append("`Wasser folgt Einzugsgebieten, nicht Eigentumsgrenzen` ist stark, sollte aber weniger wie ein Fachabschnitt und stärker wie ein Diagramm wirken.")
    md.append("")
    md.append("### 5. Wertschöpfung als Climax neu bauen")
    md.append("")
    md.append("Der wichtigste Premium-Gap liegt hier. Der bestehende Scorecard-/Matrix-Ansatz ist korrekt, aber noch nicht ikonisch.")
    md.append("")
    md.append("Leitmotiv für B162:")
    md.append("")
    md.append("```text")
    md.append("Das Feld funktioniert. Die Kette dahinter reißt.")
    md.append("```")
    md.append("")
    md.append("## Abschnittsmatrix")
    md.append("")
    md.append(f"Siehe `docs/{MATRIX.name}`.")
    md.append("")
    md.append("## Nächste Patches")
    md.append("")
    md.append("```text")
    md.append("B161 Flagship Sticky Zoom Concept")
    md.append("B162 Value-Chain Visual Climax Redesign")
    md.append("B163 Main-Flow Caveat Reduction")
    md.append("B164 Premium Pacing Polish")
    md.append("```")
    write(DOC, "\n".join(md) + "\n")

    outline = []
    outline.append("# B160 - Proposed Main-Flow Outline")
    outline.append("")
    outline.append(f"Date: {today}")
    outline.append("")
    outline.append("## Premium-Hauptfluss")
    outline.append("")
    outline.append("### 1. Hook")
    outline.append("")
    outline.append("**Moorbodenschutz braucht räumliche Orientierung.**")
    outline.append("")
    outline.append("Kurzversprechen:")
    outline.append("")
    outline.append("> Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wasser und Wertschöpfung.")
    outline.append("")
    outline.append("Scope als kurzer, einklappbarer Hinweis; nicht als langer Warnblock.")
    outline.append("")
    outline.append("### 2. Warum Karten nötig sind")
    outline.append("")
    outline.append("Ein starker Sticky-Zoom statt vieler erklärender Kartenabschnitte:")
    outline.append("")
    outline.append("1. Moore sind global kleinflächig, aber relevant.")
    outline.append("2. In Europa/Deutschland wird aus Klima eine Planungskulisse.")
    outline.append("3. In Baden-Württemberg wird die Frage regional.")
    outline.append("4. In Oberschwaben trifft sie auf konkrete Nutzung.")
    outline.append("")
    outline.append("### 3. Oberschwaben als Beleg")
    outline.append("")
    outline.append("- statische Karte: Layerlogik")
    outline.append("- Felt: interaktive Details")
    outline.append("- Bilanz: `~19.900 ha`, `~82 % Grünland`, `~16 % Ackerland`")
    outline.append("")
    outline.append("### 4. Warum die Schnittmenge keine Lösung ist")
    outline.append("")
    outline.append("Ein kompakter Transformations-/Governance-Moment:")
    outline.append("")
    outline.append("- Fläche zeigt Prüfbedarf")
    outline.append("- Wasser verbindet Parzellen")
    outline.append("- Betriebe und Zuständigkeiten entscheiden mit")
    outline.append("")
    outline.append("### 5. Climax: Die Kette hinter dem Feld")
    outline.append("")
    outline.append("Eine neue Editorial-Grafik ersetzt oder dominiert Scorecard/Matrix:")
    outline.append("")
    outline.append("> Bis zur Ernte ist vieles anschlussfähig. Danach wird es eng.")
    outline.append("")
    outline.append("Visuelle Logik:")
    outline.append("")
    outline.append("```text")
    outline.append("Feld / Wasser / Ernte  →  Logistik  →  Verarbeitung  →  Standards  →  Abnahme / Markt")
    outline.append("stabiler               →  im Aufbau →  brüchig       →  brüchig    →  eigentliche Engstelle")
    outline.append("```")
    outline.append("")
    outline.append("### 6. Kicker")
    outline.append("")
    outline.append("**Der Hebel verschiebt sich von der Fläche zur Kette.**")
    outline.append("")
    outline.append("Kurz, kein weiterer Methodenblock.")
    outline.append("")
    outline.append("### 7. Methode / Quellen / Rechte")
    outline.append("")
    outline.append("Alles, was fachlich nötig ist, aber den Hauptfluss bremst:")
    outline.append("")
    outline.append("- Datenbasis")
    outline.append("- Rechte")
    outline.append("- Methode")
    outline.append("- Nicht-Eignungskarten-Grenzen")
    outline.append("- Felt/OpenStreetMap-Hinweis")
    outline.append("- Hektarbilanz-Berechnungsgrundlage")
    write(OUTLINE, "\n".join(outline) + "\n")

    audit = f"""# B160 narrative cut plan audit

Date: {today}

Result: PLAN ONLY. No public page files changed.

Input source: {source}
Sections planned: {total_sections}
Approx. words: {total_words}
Estimated weighted cut potential: {estimated_cut_total_pct} %

Created/updated:

- docs/B160_narrative_cut_plan.md
- docs/B160_section_cut_matrix.csv
- docs/B160_main_flow_outline.md
- docs/B160_narrative_cut_plan_audit.txt
- tasks/done.md

Recommended next patch: B161 Flagship Sticky Zoom Concept
"""
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B160 narrative cut plan complete.")
    print("Plan only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B160_narrative_cut_plan.md")
    print("  docs/B160_section_cut_matrix.csv")
    print("  docs/B160_main_flow_outline.md")
    print("  docs/B160_narrative_cut_plan_audit.txt")
    print("  tasks/done.md")
    print("Recommended next patch: B161 Flagship Sticky Zoom Concept")


if __name__ == "__main__":
    main()
