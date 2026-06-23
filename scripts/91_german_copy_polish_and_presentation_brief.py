#!/usr/bin/env python3
"""
B91 - German copy polish and presentation brief

Purpose:
- Freeze the current German presentation version as the working v0.1 communication basis.
- Prepare text and presentation guidance for a short project introduction.
- Identify remaining copy-polish issues without changing the website.
- Keep the current functioning design untouched.

Outputs:
- docs/B91_german_copy_polish_review.md
- docs/B91_jour_fixe_presentation_brief.md
- docs/B91_copy_polish_todo.csv
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- alter maps/data/assets
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REVIEW = DOCS / "B91_german_copy_polish_review.md"
BRIEF = DOCS / "B91_jour_fixe_presentation_brief.md"
TODO = DOCS / "B91_copy_polish_todo.csv"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.retired_depth = 0
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.items: list[tuple[str, str, str]] = []
        self.current_tag: str | None = None
        self.current_text: list[str] = []

    def handle_starttag(self, tag, attrs_list):
        attrs = {k: (v or "") for k, v in attrs_list}
        tag_l = tag.lower()

        if tag_l in {"script", "style", "template", "svg", "noscript"}:
            self.skip_depth += 1

        if tag_l == "section":
            klass = attrs.get("class", "")
            if "is-retired" in klass or "b79-hidden" in klass or "hidden" in attrs or attrs.get("aria-hidden") == "true":
                self.retired_depth += 1

        self.stack.append((tag_l, attrs))

        if self.skip_depth == 0 and self.retired_depth == 0 and tag_l in {"h1", "h2", "h3", "p", "span", "a", "button", "li", "small"}:
            self.flush()
            self.current_tag = tag_l
            self.current_text = []

    def handle_endtag(self, tag):
        tag_l = tag.lower()
        if self.current_tag == tag_l:
            self.flush()

        popped = []
        while self.stack:
            t, attrs = self.stack.pop()
            popped.append((t, attrs))
            if t == tag_l:
                break

        if tag_l in {"script", "style", "template", "svg", "noscript"} and self.skip_depth > 0:
            self.skip_depth -= 1

        if tag_l == "section":
            for t, attrs in popped:
                if t == "section":
                    klass = attrs.get("class", "")
                    if "is-retired" in klass or "b79-hidden" in klass or "hidden" in attrs or attrs.get("aria-hidden") == "true":
                        self.retired_depth = max(0, self.retired_depth - 1)
                    break

    def handle_data(self, data):
        if self.skip_depth > 0 or self.retired_depth > 0:
            return
        if self.current_tag:
            s = re.sub(r"\s+", " ", data).strip()
            if s:
                self.current_text.append(s)

    def flush(self):
        if not self.current_tag or not self.current_text:
            self.current_tag = None
            self.current_text = []
            return
        text = re.sub(r"\s+", " ", " ".join(self.current_text)).strip()
        if text:
            section_id = ""
            for t, attrs in reversed(self.stack):
                if t == "section":
                    section_id = attrs.get("id", "")
                    break
            self.items.append((section_id, self.current_tag, text))
        self.current_tag = None
        self.current_text = []


def extract_visible_text(html: str) -> list[tuple[str, str, str]]:
    parser = VisibleTextParser()
    parser.feed(html)
    parser.flush()
    seen = set()
    out = []
    for item in parser.items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX) if INDEX.exists() else ""
    visible = extract_visible_text(html)

    visible_count = len(visible)
    english_terms = [
        "prototype",
        "MVP",
        "portfolio",
        "atlas",
        "dashboard",
        "appendix",
        "evidence",
        "story",
        "mapping the space",
        "Peatland Transition",
    ]
    found_terms = []
    low = html.lower()
    for term in english_terms:
        if term.lower() in low:
            found_terms.append(term)

    headings = [(sec, tag, txt) for sec, tag, txt in visible if tag in {"h1", "h2", "h3"}]
    headings_md = "\n".join(f"- `{sec or 'top'}` / `{tag}` — {txt}" for sec, tag, txt in headings[:80]) or "- none"

    review = f"""# B91 - German Copy Polish Review

Date: {today}

## 1. Purpose

B91 freezes the current German presentation version as the working communication basis and prepares the next editorial step.

No production files are modified.

## 2. Current judgement

The current page is suitable as a **German presentation version v0.1**.

It is strong enough for:

- a short working-group introduction,
- internal project discussion,
- demonstrating the spatial argument,
- collecting feedback from scientifically informed practitioners.

It is not yet final enough for:

- formal publication,
- press communication,
- a finished policy product.

## 3. Communication target

The page should communicate this story:

**Moorschutz wird erst dann umsetzbar, wenn globale Klimarelevanz, nationale Planungskulissen, regionale Bodenkontexte und betriebliche Nutzungsperspektiven zusammen betrachtet werden.**

The page is not the subject. The page is only the visual vehicle.

## 4. Visible text inventory

Visible non-retired text elements detected:

`{visible_count}`

## 5. Main visible headings

{headings_md}

## 6. Remaining language risks

Raw term scan in `index.html` still found these terms somewhere:

{chr(10).join(f"- `{t}`" for t in found_terms) if found_terms else "- none"}

Note: this is a raw file scan, not a visual-only judgement. Terms may appear in comments, documentation-like attributes or hidden/retired content. Before changing production copy, inspect whether they are actually visible.

## 7. Editorial priorities

### Priority 1 - Do not break the working version

The current visual and scroll behaviour should not be changed while polishing text.

### Priority 2 - Keep claims bounded

Avoid wording that implies:

- suitability,
- prioritisation,
- confirmed agricultural land use,
- final intervention recommendation,
- completed SOLAMO results.

Use:

- räumliche Einordnung,
- Umsetzungskontext,
- mögliche Nutzungspfade,
- methodische Grenze,
- betriebliche Perspektive.

### Priority 3 - Make SOLAMO/LUBW useful but not dominant

SOLAMO and LUBW should serve as the bridge from map endpoint to implementation questions:

- planning context,
- affected farms,
- use concepts,
- value chains,
- policy instruments.

Do not turn the page into a SOLAMO project flyer.

## 8. Recommended next patch

B92 should be:

`B92_final_visible_copy_polish`

Scope:

- only visible text,
- no layout changes,
- no JS changes,
- no CSS changes unless absolutely necessary,
- produce a before/after copy table first.
"""
    write(REVIEW, review)

    brief = f"""# B91 - Jour Fixe Presentation Brief

Date: {today}

## 1. One-minute version

Wir arbeiten an einer ersten visuellen Fassung, die zeigt, warum Moorschutz eine räumlich differenzierte Umsetzungsfrage ist. Der Ausgangspunkt ist: Moore sind zwar flächenmäßig begrenzt, aber für Klimaschutz, Biodiversität und Wasserhaushalt hoch relevant. Entscheidend ist aber nicht nur die globale Bedeutung, sondern die Übersetzung in konkrete Planungskulissen, regionale Bodenkontexte und betriebliche Nutzungsperspektiven.

Die Kartenfolge führt deshalb vom globalen Moorvorkommen über Emissionsdruck und europäische bzw. nationale Umsetzungsebenen bis nach Baden-Württemberg. Dort wird sichtbar: Aus Moorbodenkontext wird eine praktische Frage nach Nutzung, Betrieben, Wertschöpfung und Förderung.

Die Seite ist noch kein fertiges Entscheidungswerkzeug. Sie ist eine erste Präsentationsfassung, um die räumliche Argumentation und die Anschlussstellen für SOLAMO, LUBW-Kontext und Transformationspfade sichtbar zu machen.

## 2. Three-minute walkthrough

### Einstieg

Die zentrale These ist: **Moorschutz braucht räumliche Orientierung.**

Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung. Deshalb reicht es nicht, nur über Moorflächen oder Emissionen zu sprechen. Wir müssen die Maßstabskette sichtbar machen: global, europäisch, national, regional.

### Kartenfolge

Die Kartenfolge beginnt mit der weltweiten Moorverbreitung. Danach zeigt sie, wo sich Emissionsdruck räumlich konzentriert. Dann verschiebt sich der Maßstab nach Europa und Deutschland. Die nationale Kulisse macht deutlich, dass globale Klimarelevanz erst durch politische und planerische Umsetzung konkret wird.

Der Endpunkt der Kartenfolge ist Baden-Württemberg. Die BK50-Darstellung ist dabei ausdrücklich keine Eignungskarte und keine Priorisierung. Sie zeigt den regionalen Moor- und Feuchtbodenkontext, aus dem sich konkrete Umsetzungsfragen ergeben.

### Umsetzung

Für die Praxis ist entscheidend, was daraus folgt: Welche Betriebe sind betroffen? Welche Nutzungen bleiben möglich? Welche Wertschöpfungsketten können mit höheren Wasserständen funktionieren? Welche Förderinstrumente wären nötig?

Hier liegt die Verbindung zu SOLAMO und zur Moorschutzkonzeption Baden-Württemberg: Die räumliche Einordnung wird zur Frage nach Nutzungskonzepten, regionaler Umsetzbarkeit und Politikempfehlungen.

### Methodische Grenze

Der aktuelle Stand ist bewusst eine Einordnung. Die Seite ersetzt keine Flächeneignungsprüfung und keine betriebliche Betroffenheitsanalyse. Sie soll zuerst die komplexe Story verständlich machen und dann als Grundlage für weitere Datenintegration und Diskussion dienen.

## 3. Key sentences

- Moorschutz ist nicht nur eine Flächenfrage, sondern eine Umsetzungsfrage.
- Der Maßstab entscheidet: globale Relevanz wird erst regional handlungsfähig.
- BK50 zeigt Kontext, nicht Eignung.
- Transformationspfade müssen Wasserstand, Nutzung, Betriebsperspektive und Förderung zusammendenken.
- Die Seite ist ein visuelles Argument, kein fertiges DSS.

## 4. Anticipated questions

### Ist das schon ein Entscheidungswerkzeug?

Nein. Es ist eine Präsentations- und Diskussionsfassung. Sie zeigt eine räumliche Argumentationskette und markiert, welche Daten später für ein Entscheidungswerkzeug relevant wären.

### Zeigt BK50 geeignete Wiedervernässungsflächen?

Nein. BK50 zeigt Moor- und Feuchtbodenkontext. Eignung, Priorisierung und betriebliche Betroffenheit müssen gesondert geprüft werden.

### Wo kommt SOLAMO ins Spiel?

SOLAMO ist relevant, sobald aus Bodenkontext konkrete Umsetzung wird: Betriebe, Nutzungskonzepte, Wertschöpfungsketten und Politikempfehlungen.

### Was ist der nächste Entwicklungsschritt?

Die nächsten Schritte sind Text- und Quellenpolish, eine klarere SOLAMO/LUBW-Verankerung und später die Integration weiterer regionaler Evidenz.
"""
    write(BRIEF, brief)

    rows = [
        {
            "priority": "high",
            "area": "whole main flow",
            "issue": "check for visible residual English/meta terms",
            "recommendation": "Remove or translate only if actually visible; do not change hidden/debug/script text unnecessarily.",
            "status": "open",
        },
        {
            "priority": "high",
            "area": "BK50 step",
            "issue": "method boundary must remain clear",
            "recommendation": "Keep 'Kontext, nicht Eignung/Priorisierung' wording.",
            "status": "keep",
        },
        {
            "priority": "medium",
            "area": "regional implementation",
            "issue": "SOLAMO and LUBW can be linked more precisely",
            "recommendation": "Add factual details only after source-checking and only if they serve the argument.",
            "status": "later",
        },
        {
            "priority": "medium",
            "area": "central map step titles",
            "issue": "some titles may be slightly long for live presentation",
            "recommendation": "Shorten only after confirming no layout regression.",
            "status": "later",
        },
        {
            "priority": "low",
            "area": "method/source area",
            "issue": "source line may need formal citation style",
            "recommendation": "Add a concise source note once final source wording is decided.",
            "status": "later",
        },
    ]

    with TODO.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["priority", "area", "issue", "recommendation", "status"])
        writer.writeheader()
        writer.writerows(rows)

    done_entry = f"""
## B91 - German copy polish and presentation brief ({today})

- Created `docs/B91_german_copy_polish_review.md`.
- Created `docs/B91_jour_fixe_presentation_brief.md`.
- Created `docs/B91_copy_polish_todo.csv`.
- Prepared a short German project-presentation narrative.
- Did not modify production HTML, CSS, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B91 - German copy polish and presentation brief" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B91 German copy polish and presentation brief complete.")
    print("Changed/created:")
    print(f"  {rel(REVIEW)}")
    print(f"  {rel(BRIEF)}")
    print(f"  {rel(TODO)}")
    print(f"  {rel(DONE)}")


if __name__ == "__main__":
    main()
