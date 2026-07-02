from pathlib import Path
import re
import csv
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "159_editorial_elevation_audit.py"

DOC = ROOT / "docs" / "B159_editorial_elevation_audit.md"
CSV_OUT = ROOT / "docs" / "B159_editorial_section_inventory.csv"
PLAN = ROOT / "docs" / "B159_editorial_elevation_patch_plan.md"
AUDIT = ROOT / "docs" / "B159_editorial_elevation_audit.txt"
DONE = ROOT / "tasks" / "done.md"

SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"<h([1-4])\b[^>]*>(.*?)</h\1>", re.S | re.I)

WARNING_WORDS = [
    "keine Eignungskarte",
    "keine Priorisierung",
    "keine hydrologische Modellierung",
    "keine betriebliche Betroffenheitsanalyse",
    "Prüfbedarf",
    "Einzelfallprüfung",
    "Orientierung",
    "Hinweis",
    "Methodischer Hinweis",
    "Grenze der Aussage",
]

PREMIUM_CRITERIA = [
    "one_sentence_takeaway",
    "five_act_structure",
    "one_flagship_scrolly",
    "three_memorable_images",
    "reduced_caveats",
    "visual_climax_value_chain",
    "strong_mobile_pacing",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_tags(html: str) -> str:
    text = TAG_RE.sub(" ", html)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


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
    out = []
    if sid:
        out.append("#" + sid)
    if cls:
        out.append("." + ".".join(cls.split()))
    return " ".join(out)


def count_warning_words(text: str) -> int:
    low = text.lower()
    return sum(low.count(w.lower()) for w in WARNING_WORDS)


def classify_act(heading: str, text: str) -> str:
    t = (heading + " " + text).lower()

    if any(k in t for k in ["hero", "moorbodenschutz braucht", "fachlicher demonstrator", "kernargument"]):
        return "A1 Hook / promise"
    if any(k in t for k in ["wasserstand", "moorboden", "speicher", "quelle", "frame-mismatch", "globale karten", "moore sind räumlich"]):
        return "A2 Why it matters / scale jump"
    if any(k in t for k in ["oberschwaben", "schnittmenge", "fiona", "bk50", "flächenbilanz"]):
        return "A3 Regional concretisation"
    if any(k in t for k in ["transformationspfade", "wasser und governance", "einheitslösung", "nutzungskontexte"]):
        return "A4 What implementation really requires"
    if any(k in t for k in ["wertschöpfung", "engstelle", "verarbeitung", "abnahme", "standards", "kette"]):
        return "A5 Climax / bottleneck behind the field"
    if any(k in t for k in ["quellen", "methode", "nutzungsrechte", "impressum", "datenschutz"]):
        return "Method / appendix"
    return "Unclear / supporting"


def classify_action(heading: str, text: str, warning_count: int, word_count: int) -> tuple[str, str]:
    t = (heading + " " + text).lower()

    if any(k in t for k in ["quellen", "methode", "nutzungsrechte", "impressum", "datenschutz"]):
        return "move_to_appendix_or_keep_collapsed", "Method/source material should support the feature but not dominate narrative pacing."

    if any(k in t for k in ["interaktive vertiefung", "felt", "oberschwaben-felt-pilot"]):
        return "keep_and_integrate", "Strong map-quality upgrade; keep as interactive deepening, not as a second main story."

    if any(k in t for k in ["wertschöpfung", "verarbeitung", "abnahme", "standards"]):
        return "rebuild_visual_climax", "The thesis is strong, but the visual language should become a memorable editorial graphic."

    if warning_count >= 4:
        return "compress_caveats", "Too many caveats in the visible flow; move detail to method or collapse."

    if word_count > 420:
        return "cut_30_percent", "Long section; likely needs editorial compression for premium pacing."

    if any(k in t for k in ["wasser und governance", "hydrologische einheit"]):
        return "turn_into_visual_moment", "Good concept, but should become a diagrammatic editorial beat."

    if any(k in t for k in ["oberschwaben", "schnittmenge"]):
        return "keep_tighten_transition", "Core regional proof point; keep but avoid repetition with Felt and area balance."

    if any(k in t for k in ["moore sind räumlich", "maßstab", "global", "deutschland", "baden-württemberg"]):
        return "candidate_for_flagship_zoom", "This is where the premium sticky zoom should be earned."

    return "keep_or_trim", "Supportive section; retain only if it strengthens the five-act structure."


def score_section(action: str, warning_count: int, word_count: int) -> int:
    score = 7
    if action in {"keep_and_integrate", "candidate_for_flagship_zoom"}:
        score += 1
    if action in {"rebuild_visual_climax", "turn_into_visual_moment"}:
        score -= 1
    if action in {"compress_caveats", "cut_30_percent"}:
        score -= 2
    if warning_count >= 4:
        score -= 1
    if word_count > 500:
        score -= 1
    return max(1, min(10, score))


def update_done(done_text: str, today: str) -> str:
    line = f"- B159 editorial elevation audit: compared the current V2 page against premium editorial/data-feature standards and created a cut/rebuild plan ({today})."
    if "B159 editorial elevation audit" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    sections = list(SECTION_RE.finditer(html))
    today = date.today().isoformat()

    rows = []
    for i, m in enumerate(sections, start=1):
        section = m.group(0)
        text = strip_tags(section)
        heading = first_heading(section)
        open_tag = extract_section_open(section)
        words = len(text.split())
        warning_count = count_warning_words(text)
        act = classify_act(heading, text)
        action, reason = classify_action(heading, text, warning_count, words)
        score = score_section(action, warning_count, words)

        rows.append({
            "section_no": i,
            "selector": selector(open_tag),
            "heading": heading,
            "act": act,
            "word_count": words,
            "warning_count": warning_count,
            "editorial_score_1_10": score,
            "recommended_action": action,
            "reason": reason,
            "excerpt": text[:260],
        })

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "section_no",
                "selector",
                "heading",
                "act",
                "word_count",
                "warning_count",
                "editorial_score_1_10",
                "recommended_action",
                "reason",
                "excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    total_words = sum(r["word_count"] for r in rows)
    total_warnings = sum(r["warning_count"] for r in rows)
    avg_score = round(sum(r["editorial_score_1_10"] for r in rows) / max(1, len(rows)), 1)

    action_counts = {}
    for r in rows:
        action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1

    act_counts = {}
    for r in rows:
        act_counts[r["act"]] = act_counts.get(r["act"], 0) + 1

    priority_rows = [
        r for r in rows
        if r["recommended_action"] in {
            "rebuild_visual_climax",
            "candidate_for_flagship_zoom",
            "turn_into_visual_moment",
            "compress_caveats",
            "cut_30_percent",
        }
    ]

    md = []
    md.append("# B159 - Editorial Elevation Audit")
    md.append("")
    md.append(f"Date: {today}")
    md.append("")
    md.append("## Ziel")
    md.append("")
    md.append("B159 stoppt bewusst den reinen QA-/Patchmodus und bewertet die Seite als Editorial/Data-Feature.")
    md.append("Maßstab ist nicht nur fachliche Korrektheit, sondern Wirkung auf dem Niveau großer datenjournalistischer Features.")
    md.append("")
    md.append("## Kurzurteil")
    md.append("")
    md.append("> Aktueller Stand: starker fachlicher Demonstrator mit deutlich verbesserter Karte und klarer These.")
    md.append("> Noch nicht: radikal kuratiertes, visuell inszeniertes Premium-Feature.")
    md.append("")
    md.append("Die Seite ist inzwischen fachlich belastbar, aber sie erklärt noch zu viel. Für ein stärkeres Editorial-Level braucht sie weniger sichtbare Absicherung, einen klareren visuellen Höhepunkt und eine stärkere Dramaturgie.")
    md.append("")
    md.append("## Automatische Kennzahlen")
    md.append("")
    md.append(f"- untersuchte Sections: {len(rows)}")
    md.append(f"- grobe Wortzahl in Sections: {total_words}")
    md.append(f"- sichtbare Hinweis-/Warnwort-Treffer: {total_warnings}")
    md.append(f"- mittlerer Editorial-Score: {avg_score}/10")
    md.append("")
    md.append("## Fünf-Akt-Struktur")
    md.append("")
    md.append("Die Seite sollte ab jetzt konsequent auf diese fünf Akte geschnitten werden:")
    md.append("")
    md.append("1. **Moore sind klein, aber klimatisch groß.**")
    md.append("2. **Karten zeigen den Maßstabssprung von globaler Relevanz zu regionaler Planung.**")
    md.append("3. **In Oberschwaben trifft Moorbodenschutz auf reale Nutzung.**")
    md.append("4. **Aus Schnittmenge folgt Verhandlung: Wasser, Betriebe und Zuständigkeiten entscheiden.**")
    md.append("5. **Der Engpass liegt hinter dem Feld: Verarbeitung, Abnahme, Standards und Mengen.**")
    md.append("")
    md.append("Alles, was diese Akte nicht stärkt, sollte gekürzt, in Methode/Quellen verschoben oder in eine stärkere Grafik übersetzt werden.")
    md.append("")
    md.append("## Premium-Gap gegenüber NYT / ZEIT / Guardian")
    md.append("")
    md.append("| Dimension | Aktueller Stand | Premium-Ziel |")
    md.append("|---|---|---|")
    md.append("| These | klar und fachlich belastbar | noch stärker als ein erinnerbarer Satz inszenieren |")
    md.append("| Karten | Felt ist echter Qualitätssprung | ein großer choreografierter Sticky-Zoom fehlt |")
    md.append("| Pacing | stabil, aber erklärend | 20–35 % weniger sichtbarer Text im Hauptfluss |")
    md.append("| Methodik | sehr transparent | weniger sichtbare Caveats, mehr Appendix/Details |")
    md.append("| Wertschöpfung | inhaltlich stark | visuell als Climax neu denken |")
    md.append("| Mobile | pragmatisch robust | kürzerer Lesefluss, weniger Boxen, klarere Bildmomente |")
    md.append("")
    md.append("## Handlungskategorien")
    md.append("")
    md.append("| Aktion | Anzahl |")
    md.append("|---|---:|")
    for action, count in sorted(action_counts.items()):
        md.append(f"| `{action}` | {count} |")
    md.append("")
    md.append("## Story-Akte im aktuellen HTML")
    md.append("")
    md.append("| Akt | Anzahl Sections |")
    md.append("|---|---:|")
    for act, count in sorted(act_counts.items()):
        md.append(f"| {act} | {count} |")
    md.append("")
    md.append("## Prioritäre Eingriffe")
    md.append("")
    md.append("| Nr. | Überschrift | Akt | Aktion | Begründung |")
    md.append("|---:|---|---|---|---|")
    for r in priority_rows:
        h = r["heading"] or "(ohne Überschrift)"
        md.append(f"| {r['section_no']} | {h} | {r['act']} | `{r['recommended_action']}` | {r['reason']} |")
    md.append("")
    md.append("## Redaktionelle Leitentscheidung")
    md.append("")
    md.append("Ab jetzt nicht mehr fragen: `Was können wir noch hinzufügen?`")
    md.append("")
    md.append("Stattdessen fragen:")
    md.append("")
    md.append("- Was ist der eine Satz, der hängen bleibt?")
    md.append("- Welche drei Bilder bleiben im Kopf?")
    md.append("- Welche Fachdetails gehören in Methode/Quellen statt in den Hauptfluss?")
    md.append("- Wo ist der stärkste Scrolly-Moment?")
    md.append("- Wo wird aus einer richtigen Aussage eine erinnerbare Szene?")
    md.append("")
    md.append("## Empfehlung")
    md.append("")
    md.append("Der nächste produktive Schritt ist kein Release-Audit, sondern ein **Narrative Cut Plan**:")
    md.append("")
    md.append("```text")
    md.append("B160 Narrative Cut Plan")
    md.append("B161 Flagship Sticky Zoom Concept")
    md.append("B162 Value-Chain Visual Climax Redesign")
    md.append("B163 Main-Flow Caveat Reduction")
    md.append("```")
    md.append("")
    md.append("## Dateien")
    md.append("")
    md.append(f"- Section inventory: `docs/{CSV_OUT.name}`")
    write(DOC, "\n".join(md) + "\n")

    plan = []
    plan.append("# B159 - Editorial Elevation Patch Plan")
    plan.append("")
    plan.append(f"Date: {today}")
    plan.append("")
    plan.append("## Zielbild")
    plan.append("")
    plan.append("Die V2 soll nicht einfach vollständiger werden. Sie soll schärfer, visueller und erinnerbarer werden.")
    plan.append("")
    plan.append("## Empfohlene Patch-Sequenz")
    plan.append("")
    plan.append("### B160 - Narrative Cut Plan")
    plan.append("")
    plan.append("Audit/Plan, noch kein Seitenumbau.")
    plan.append("")
    plan.append("- Hauptfluss auf fünf Akte schneiden")
    plan.append("- Kandidaten für Kürzung, Verschiebung und Zusammenlegung markieren")
    plan.append("- Ziel: 20–35 % weniger sichtbarer Erklärtext im Hauptfluss")
    plan.append("")
    plan.append("### B161 - Flagship Sticky Zoom Concept")
    plan.append("")
    plan.append("Konzeptpatch.")
    plan.append("")
    plan.append("- ein einziger großer Sticky-Moment")
    plan.append("- global → Europa/Deutschland → Baden-Württemberg → Oberschwaben")
    plan.append("- kein neuer Datenanspruch, sondern stärkere Choreografie")
    plan.append("")
    plan.append("### B162 - Value-Chain Visual Climax Redesign")
    plan.append("")
    plan.append("Konzeptpatch oder isolierter Prototyp.")
    plan.append("")
    plan.append("- Scorecard in erinnerbares Editorial-Bild übersetzen")
    plan.append("- Leitmotiv: `Das Feld funktioniert. Die Kette dahinter reißt.`")
    plan.append("- weniger Tabelle, mehr visuelle Spannung")
    plan.append("")
    plan.append("### B163 - Main-Flow Caveat Reduction")
    plan.append("")
    plan.append("Kleiner Seitenpatch.")
    plan.append("")
    plan.append("- wiederholte `keine Eignungskarte`-Hinweise konsolidieren")
    plan.append("- Detailwarnungen in Methode/Quellen oder `details` verschieben")
    plan.append("- keine fachliche Grenze entfernen")
    plan.append("")
    plan.append("### B164 - Premium Pacing Polish")
    plan.append("")
    plan.append("Kleiner Seitenpatch.")
    plan.append("")
    plan.append("- Übergänge, Satzlängen, Section-Starts")
    plan.append("- stärkere statement titles")
    plan.append("- weniger Card-Übergewicht")
    plan.append("")
    plan.append("## Nicht jetzt")
    plan.append("")
    plan.append("- kein weiterer Datenlayer")
    plan.append("- keine zusätzliche Karte")
    plan.append("- kein weiterer Hinweisblock")
    plan.append("- kein Release-Candidate-Audit, bevor die Editorial-Schleife abgeschlossen ist")
    write(PLAN, "\n".join(plan) + "\n")

    audit_text = f"""# B159 editorial elevation audit

Date: {today}

Result: AUDIT ONLY. No public page files changed.

Sections scanned: {len(rows)}
Approx. words in sections: {total_words}
Warning/caveat term hits: {total_warnings}
Average editorial score: {avg_score}/10

Created/updated:

- docs/B159_editorial_elevation_audit.md
- docs/B159_editorial_section_inventory.csv
- docs/B159_editorial_elevation_patch_plan.md
- docs/B159_editorial_elevation_audit.txt
- tasks/done.md

Recommended next patch: B160 Narrative Cut Plan
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B159 editorial elevation audit complete.")
    print("Audit only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B159_editorial_elevation_audit.md")
    print("  docs/B159_editorial_section_inventory.csv")
    print("  docs/B159_editorial_elevation_patch_plan.md")
    print("  docs/B159_editorial_elevation_audit.txt")
    print("  tasks/done.md")
    print("Recommended next patch: B160 Narrative Cut Plan")


if __name__ == "__main__":
    main()
