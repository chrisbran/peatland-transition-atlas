from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "164_premium_pacing_polish.py"
DOC = ROOT / "docs" / "B164_premium_pacing_polish.md"
CSV_OUT = ROOT / "docs" / "B164_premium_pacing_replacements.csv"
AUDIT = ROOT / "docs" / "B164_premium_pacing_polish_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CSS_START = "/* B164_PREMIUM_PACING_POLISH_START */"
CSS_END = "/* B164_PREMIUM_PACING_POLISH_END */"

REPLACEMENTS = [
    {
        "id": "hero_subtitle",
        "pattern": (
            r"Wiedervernässung\s+ist\s+nicht\s+nur\s+eine\s+ökologische\s+Maßnahme\.\s*"
            r"Sie\s+verändert\s+Nutzung,\s+Betriebe,\s+Wertschöpfung\s+und\s+Planung\."
        ),
        "replacement": (
            "Wiedervernässung verändert mehr als Wasserstände. "
            "Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung."
        ),
        "reason": "sharpens the opening promise without adding detail",
    },
    {
        "id": "hero_card_3_title",
        "pattern": r"Transformation\s+braucht\s+Pfade",
        "replacement": "Nasse Flächen brauchen Pfade",
        "reason": "more concrete and image-led than abstract transformation language",
    },
    {
        "id": "hero_card_3_body",
        "pattern": r"Schutz,\s+Wiedervernässung,\s+angepasste\s+Nutzung\s+und\s+Förderinstrumente\s+müssen\s+zusammen\s+gedacht\s+werden\.",
        "replacement": "Schutz, Nutzung und Förderung müssen zusammen gedacht werden.",
        "reason": "shorter hero-card copy",
    },
    {
        "id": "core_argument_heading",
        "pattern": r"Moorbodenschutz\s+wird\s+erst\s+mit\s+Boden,\s+Nutzung\s+und\s+Wasserstand\s+planbar",
        "replacement": "Planbar wird Moorbodenschutz erst mit Boden, Nutzung und Wasser",
        "reason": "turns the headline into a more memorable sentence",
    },
    {
        "id": "core_argument_body",
        "pattern": (
            r"Planbar\s+wird\s+Moorschutz\s+erst,\s+wenn\s+Bodenkulissen,\s+Nutzungskontexte,\s+Wasserstand,\s+"
            r"betriebliche\s+Fragen\s+und\s+mögliche\s+Wertschöpfungsketten\s+zusammen\s+betrachtet\s+werden\."
        ),
        "replacement": (
            "Moorschutz wird planbar, wenn Boden, Nutzung, Wasserstand, Betriebe "
            "und Wertschöpfung zusammen betrachtet werden."
        ),
        "reason": "removes stacked nouns in the early thesis paragraph",
    },
    {
        "id": "regional_heading",
        "pattern": r"In\s+Oberschwaben\s+wird\s+Moorbodenschutz\s+zur\s+konkreten\s+Nutzungsfrage",
        "replacement": "In Oberschwaben wird Moorbodenschutz konkret",
        "reason": "shorter regional section title",
    },
    {
        "id": "regional_intro",
        "pattern": (
            r"In\s+Baden-Württemberg\s+wird\s+Moorschutz\s+zur\s+konkreten\s+Planungsfrage:\s*"
            r"Welche\s+Nutzungskontexte\s+sind\s+berührt,\s+welche\s+betrieblichen\s+Fragen\s+entstehen,\s+"
            r"welche\s+Produkte\s+können\s+tragfähig\s+werden\s+und\s+welche\s+Förderinstrumente\s+wären\s+nötig\?"
        ),
        "replacement": (
            "In Baden-Württemberg wird Moorschutz zur Planungsfrage: Welche Nutzungen sind berührt, "
            "welche betrieblichen Fragen entstehen und welche Produkte könnten tragfähig werden?"
        ),
        "reason": "reduces a long question chain",
    },
    {
        "id": "paths_heading",
        "pattern": r"Unterschiedliche\s+Flächen\s+brauchen\s+unterschiedliche\s+Transformationspfade",
        "replacement": "Nicht jede Fläche braucht denselben Pfad",
        "reason": "more editorial and less administrative",
    },
    {
        "id": "paths_lead",
        "pattern": (
            r"Die\s+zentrale\s+Aufgabe\s+ist\s+nicht\s+die\s+eine\s+Maßnahme,\s+sondern\s+die\s+passende\s+"
            r"Kombination\s+aus\s+Wasserstand,\s+Nutzung,\s+Betriebsperspektive\s+und\s+öffentlicher\s+Förderung\."
        ),
        "replacement": (
            "Entscheidend ist die passende Kombination aus Wasserstand, Nutzung, "
            "Betriebsperspektive und Förderung."
        ),
        "reason": "shortens an explanatory lead",
    },
    {
        "id": "oberschwaben_heading_punctuation",
        "pattern": r"Oberschwaben,\s+wo\s+Moorschutz\s+auf\s+Landwirtschaft\s+trifft",
        "replacement": "Oberschwaben: wo Moorschutz auf Landwirtschaft trifft",
        "reason": "clearer title rhythm",
    },
    {
        "id": "felt_heading",
        "pattern": r"Die\s+statische\s+Karte\s+zeigt\s+die\s+Lage\s+–\s+die\s+interaktive\s+Karte\s+zeigt\s+die\s+Details",
        "replacement": "Erst die Lage. Dann die Details.",
        "reason": "turns a functional label into an editorial transition",
    },
    {
        "id": "felt_lead",
        "pattern": (
            r"Der\s+vorherige\s+Kartenabschnitt\s+ordnet\s+die\s+Schnittmenge\s+im\s+Seitenfluss\s+ein\.\s*"
            r"Diese\s+interaktive\s+Version\s+ist\s+die\s+Vertiefung:\s+Sie\s+zeigt\s+dieselbe\s+Kernaussage\s*"
            r"als\s+scharfe\s+Vektorkarte,\s+mit\s+Landkreisorientierung\s+und\s+Klick-Information\s+zur\s*"
            r"Gesamtfläche\s+der\s+Schnittmenge\."
        ),
        "replacement": (
            "Die statische Karte ordnet ein. Die interaktive Version vertieft: "
            "Sie zeigt dieselbe Schnittmenge als scharfe Vektorkarte mit Landkreisorientierung."
        ),
        "reason": "removes explanatory meta-language around the Felt block",
    },
    {
        "id": "felt_to_balance_transition",
        "pattern": (
            r"Nach\s+der\s+räumlichen\s+Vertiefung\s+folgt\s+die\s+Bilanz:\s*"
            r"Wie\s+groß\s+ist\s+diese\s+Schnittmenge\s+und\s+welche\s+heutige\s+Nutzung\s+dominiert\s+sie\?"
        ),
        "replacement": "Nach der Karte folgt die Bilanz: Wie groß ist die Schnittmenge, und welche Nutzung dominiert?",
        "reason": "shorter transition after Felt",
    },
    {
        "id": "area_balance_heading",
        "pattern": r"Die\s+Schnittmenge\s+macht\s+den\s+Prüfbedarf\s+sichtbar,\s+nicht\s+die\s+Lösung",
        "replacement": "Die Schnittmenge zeigt die Größenordnung",
        "reason": "reduces caveat framing and improves section rhythm",
    },
    {
        "id": "area_balance_body",
        "pattern": (
            r"Die\s+Karte\s+bleibt\s+eine\s+räumliche\s+Einordnung\.\s*"
            r"Die\s+Verschneidung\s+zeigt,\s*"
            r"dass\s+die\s+Überschneidung\s+von\s+landwirtschaftlicher\s+Nutzung\s+und\s+Moor-/Feuchtbodenkontext\s*"
            r"auch\s+in\s+der\s+Bilanz\s+sichtbar\s+wird\."
        ),
        "replacement": (
            "Die Verschneidung zeigt, dass die Überschneidung von landwirtschaftlicher Nutzung "
            "und Moor-/Feuchtbodenkontext auch in der Bilanz relevant wird."
        ),
        "reason": "turns two defensive sentences into one active sentence",
    },
    {
        "id": "negotiation_heading",
        "pattern": r"Aus\s+der\s+Schnittmenge\s+folgt\s+Verhandlung,\s+keine\s+Einheitslösung",
        "replacement": "Aus der Schnittmenge folgt Verhandlung",
        "reason": "removes a repeated negative clause",
    },
    {
        "id": "value_context_heading",
        "pattern": r"Nutzungskontexte\s+entscheiden,\s+welche\s+Wertschöpfungspfade\s+plausibel\s+sind",
        "replacement": "Nutzung entscheidet, welche Wertschöpfung plausibel wird",
        "reason": "shorter and more active value-chain matrix heading",
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* Small pacing polish: improve heading rhythm without changing layout structure. */
@supports (text-wrap: balance) {{
  h1,
  h2,
  h3,
  .hero-title {{
    text-wrap: balance;
  }}
}}

@supports (text-wrap: pretty) {{
  p,
  li {{
    text-wrap: pretty;
  }}
}}

.b164-pacing-marker {{
  display: none;
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B164 premium pacing polish: tightened section titles, leads and transitions for a more editorial main-flow rhythm ({today})."
    if "B164 premium pacing polish" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    html = read(INDEX)
    css = read(CSS)

    before_len = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).split())

    rows = []
    patched = html

    for item in REPLACEMENTS:
        patched, n = re.subn(item["pattern"], item["replacement"], patched, count=1, flags=re.S | re.I)
        rows.append({
            "id": item["id"],
            "replacements": n,
            "replacement": item["replacement"],
            "reason": item["reason"],
        })

    after_len = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", patched)).split())

    css = patch_css(css)

    write(INDEX, patched)
    write(CSS, css)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "replacements", "replacement", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    doc = f"""# B164 - Premium Pacing Polish

Date: {today}

## Ziel

B164 schärft den Lesefluss nach B163. Es werden keine neuen Inhalte, Karten oder Grafiken ergänzt.
Stattdessen werden Titel, Leads und Übergänge knapper und stärker auf Feature-Rhythmus getrimmt.

## Prinzip

- kürzere Aussagen
- weniger Meta-Sprache
- mehr aktive Sätze
- keine fachlichen Grenzen entfernen
- keine Strukturänderung
- keine neue Section

## Ersetzungen

| ID | Treffer | Zweck |
|---|---:|---|
"""
    for row in rows:
        doc += f"| `{row['id']}` | {row['replacements']} | {row['reason']} |\n"

    doc += f"""
## Grobe Wortzählung

Die folgende Zählung ist nur ein Indikator, weil sie HTML und technische Texte nicht perfekt trennt.

- vorher: {before_len}
- nachher: {after_len}
- Differenz: {before_len - after_len}

## CSS

B164 ergänzt nur eine kleine Text-Rhythmus-Politur:

- `text-wrap: balance` für Überschriften, falls Browser es unterstützt
- `text-wrap: pretty` für Absätze/Listen, falls Browser es unterstützt

## QA

Nach dem Patch:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Hero bleibt stark
- zentrale Kartenstory bleibt unverändert
- Oberschwaben/Felt Übergang klingt kürzer
- Flächenbilanz startet direkter
- Scorecard bleibt unverändert zu B162c
"""
    write(DOC, doc)

    audit = "# B164 premium pacing polish audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"Approx. word count before: {before_len}\n"
    audit += f"Approx. word count after: {after_len}\n"
    audit += f"Approx. delta: {before_len - after_len}\n\n"
    audit += "Replacement results:\n"
    for row in rows:
        audit += f"- {row['id']}: {row['replacements']}\n"
    audit += "\n"
    if any(row["replacements"] == 0 for row in rows):
        audit += "WARN: Some planned pacing replacements had zero matches. Prior patches may have changed wording; inspect manually.\n"
    else:
        audit += "OK: All planned pacing replacements matched at least once.\n"
    audit += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B164 premium pacing polish complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B164_premium_pacing_polish.md")
    print("  docs/B164_premium_pacing_replacements.csv")
    print("  docs/B164_premium_pacing_polish_audit.txt")
    print("  tasks/done.md")
    print(f"Approx. word count before: {before_len}")
    print(f"Approx. word count after: {after_len}")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
