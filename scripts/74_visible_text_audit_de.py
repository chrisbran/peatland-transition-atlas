#!/usr/bin/env python3
"""
B74 - Visible text audit DE

Audit-only step for the German presentation version.
Creates:
- docs/B74_visible_text_audit_de.md
- docs/B74_visible_text_inventory.csv
- docs/B74_german_rewrite_targets.md
- updates tasks/done.md

Does not modify index.html, CSS, scripts, maps or data.
"""
from __future__ import annotations

import csv
import html
import re
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
INDEX = ROOT / "index.html"
DONE = TASKS / "done.md"
OUT_MD = DOCS / "B74_visible_text_audit_de.md"
OUT_CSV = DOCS / "B74_visible_text_inventory.csv"
OUT_REWRITE = DOCS / "B74_german_rewrite_targets.md"

TEXT_TAGS = {"h1","h2","h3","h4","h5","h6","p","span","a","button","li","th","td","caption","figcaption","label","small","strong","em"}
SKIP_TAGS = {"script","style","template","svg","noscript"}
META_TERMS = ["atlas","prototype","module","dashboard","tool","storyline","story","evidence explorer","supporting evidence","appendix","mvp","main atlas","map story"]
EN_MARKERS = ["the","and","from","where","why","what","how","transition","pathway","pressure","extent","implementation","evidence","supporting","prototype","context","story","below","global"]
METHOD_TERMS = ["suitability","priority","rewetting potential","agricultural use","land-use","bk50","peat / wetland","wetland soil"]

@dataclass
class Item:
    section_id: str
    section_role: str
    tag: str
    text: str
    hint: str

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str,str]]] = []
        self.skip = 0
        self.retired = 0
        self.current_tag: str | None = None
        self.current_hint = ""
        self.buf: list[str] = []
        self.items: list[Item] = []

    def handle_starttag(self, tag, attrs_list):
        tag = tag.lower()
        attrs = {k: (v or "") for k, v in attrs_list}
        if tag in SKIP_TAGS:
            self.skip += 1
        if tag == "section":
            cls = attrs.get("class", "")
            if "is-retired" in cls or "hidden" in attrs or attrs.get("aria-hidden") == "true":
                self.retired += 1
        self.stack.append((tag, attrs))
        if self.skip == 0 and self.retired == 0 and tag in TEXT_TAGS:
            self.flush()
            self.current_tag = tag
            parts = []
            if attrs.get("class"):
                parts.append("class=" + attrs["class"])
            if attrs.get("data-global-state"):
                parts.append("data-global-state=" + attrs["data-global-state"])
            self.current_hint = "; ".join(parts)
            self.buf = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.current_tag == tag:
            self.flush()
        popped = []
        while self.stack:
            t, attrs = self.stack.pop()
            popped.append((t, attrs))
            if t == tag:
                break
        if tag in SKIP_TAGS and self.skip > 0:
            self.skip -= 1
        if tag == "section":
            for t, attrs in popped:
                if t == "section":
                    cls = attrs.get("class", "")
                    if "is-retired" in cls or "hidden" in attrs or attrs.get("aria-hidden") == "true":
                        self.retired = max(0, self.retired - 1)
                    break

    def handle_data(self, data):
        if self.skip or self.retired or not self.current_tag:
            return
        s = data.strip()
        if s:
            self.buf.append(s)

    def flush(self):
        if not self.current_tag or not self.buf:
            self.current_tag = None
            self.buf = []
            return
        txt = norm(" ".join(self.buf))
        if txt:
            sid, role = self.section()
            self.items.append(Item(sid, role, self.current_tag, txt, self.current_hint))
        self.current_tag = None
        self.buf = []
        self.current_hint = ""

    def section(self):
        for tag, attrs in reversed(self.stack):
            if tag == "section":
                return attrs.get("id", ""), attrs.get("data-story-role", "")
        return "", ""

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def write(path: Path, txt: str):
    path.write_text(txt, encoding="utf-8", newline="\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def looks_english(text: str) -> bool:
    low = " " + text.lower() + " "
    return sum(1 for w in EN_MARKERS if f" {w} " in low) >= 2

def word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b", text))

def flags_for(text: str, tag: str) -> tuple[list[str], list[str]]:
    low = text.lower()
    flags, terms = [], []
    if looks_english(text):
        flags.append("probably_english")
    meta = [m for m in META_TERMS if m in low]
    if meta:
        flags.append("meta_tool_language"); terms.extend(meta)
    meth = [m for m in METHOD_TERMS if m in low]
    if meth:
        flags.append("method_boundary_check"); terms.extend(meth)
    wc = word_count(text)
    if wc > 34 or (tag in {"h1","h2","h3"} and wc > 12):
        flags.append("too_long")
    return flags, terms

def action(flags: list[str]) -> str:
    if "meta_tool_language" in flags:
        return "rewrite_to_subject_matter"
    if "probably_english" in flags:
        return "translate_and_tighten"
    if "method_boundary_check" in flags:
        return "check_claim_boundary"
    if "too_long" in flags:
        return "shorten"
    return "review"

def priority(tag: str, flags: list[str]) -> str:
    if tag in {"h1","h2","h3","a","button"} or "meta_tool_language" in flags or "method_boundary_check" in flags:
        return "high"
    if tag in {"p","li","figcaption"}:
        return "medium"
    return "low"

def main():
    DOCS.mkdir(exist_ok=True); TASKS.mkdir(exist_ok=True)
    parser = Parser(); parser.feed(read(INDEX)); parser.flush()
    seen = set(); rows = []
    for it in parser.items:
        key = (it.section_id, it.tag, it.text)
        if key in seen:
            continue
        seen.add(key)
        fl, terms = flags_for(it.text, it.tag)
        rows.append({
            "section_id": it.section_id,
            "section_role": it.section_role,
            "tag": it.tag,
            "priority": priority(it.tag, fl),
            "flags": "; ".join(fl),
            "flag_terms": "; ".join(terms),
            "suggested_action": action(fl),
            "current_text": it.text,
            "rewrite_de": "",
            "comment": "",
            "source_hint": it.hint,
        })

    fields = ["section_id","section_role","tag","priority","flags","flag_terms","suggested_action","current_text","rewrite_de","comment","source_hint"]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

    total = len(rows)
    high = sum(r["priority"] == "high" for r in rows)
    english = sum("probably_english" in r["flags"] for r in rows)
    meta = sum("meta_tool_language" in r["flags"] for r in rows)
    method = sum("method_boundary_check" in r["flags"] for r in rows)
    long = sum("too_long" in r["flags"] for r in rows)
    examples = [r for r in rows if r["priority"] == "high"][:30]
    example_md = "\n".join(f"- `{r['section_id']}` / `{r['tag']}` — {r['current_text']} [{r['flags'] or 'no flags'}]" for r in examples) or "- none"

    audit = f"""# B74 - Sichtbarer Textaudit Deutsch

Date: {date.today().isoformat()}

## 1. Zweck

B74 bereitet die deutsche Vorzeigefassung vor. Der Audit extrahiert sichtbare Texte aus `index.html`, ignoriert retired/hidden sections und markiert Texte, die für die deutsche Präsentationsfassung überarbeitet werden müssen.

B74 verändert keine Anwendungsdateien.

## 2. Zielbild aus B73

- Zielgruppe: wissenschaftlich informierte Praxisakteure
- Tonalität: narrativ vermittelnd
- Umfang: kurz und pointiert
- Prinzip: Form follows function

## 3. Audit-Zusammenfassung

- Sichtbare Textelemente: {total}
- Hohe Priorität: {high}
- Vermutlich Englisch: {english}
- Meta-/Toolsprache: {meta}
- Methodische Boundary prüfen: {method}
- Zu lang / zu erklärend: {long}

## 4. Wichtigste High-Priority-Funde

{example_md}

## 5. Prüfkriterien für die manuelle Redaktion

1. Spricht der Text über die Sache oder über das Tool?
2. Ist die Aussage auf Deutsch sofort verständlich?
3. Ist die Formulierung kurz genug für eine Projektvorstellung?
4. Ist die fachliche Grenze korrekt?
5. Hilft der Text der Story oder erklärt er die Website?

## 6. Arbeitstabelle

Siehe `{rel(OUT_CSV)}`. Die Spalte `rewrite_de` ist bewusst leer und wird im nächsten Schritt kuratiert gefüllt.

## 7. Empfohlener nächster Schritt

`B75_curated_german_copy_deck`

Ziel: deutsche Hauptüberschriften, Übergänge und Kartenstep-Texte kuratieren, bevor Design-Dummies erstellt werden.
"""
    write(OUT_MD, audit)

    rewrite = f"""# B74 - German Rewrite Targets

Date: {date.today().isoformat()}

## 1. Kommunikationsziel

Die deutsche Vorzeigefassung soll nicht den Atlas erklären. Sie soll die Transformationslogik vermitteln:

**Moorschutz braucht räumliche Orientierung, regionale Umsetzung und tragfähige Nutzungsperspektiven.**

## 2. Vorläufiger deutscher Kerntext

### Hero

**Moorschutz braucht räumliche Orientierung.**  
Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.

### Problemrahmen

Moore nehmen nur geringe Flächenanteile ein, haben aber eine hohe Bedeutung für Klimaschutz, Biodiversität, Wasserhaushalt und Landschaftsentwicklung. Entwässerte Moorböden können zu erheblichen Treibhausgasquellen werden.

### Übergang zur Karte

Die Kartenfolge zeigt, wie aus globaler Klimarelevanz regionale Umsetzung wird: von Moorverbreitung und Emissionsdruck über nationale Planungskulissen bis zum Bodenkontext in Baden-Württemberg.

### Methodische Grenze

Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.

### Regionale Umsetzung

In Baden-Württemberg wird Moorschutz zur konkreten Umsetzungsfrage: Welche Flächen sind betroffen, welche Nutzungen bleiben möglich, welche Wertschöpfungsketten tragen und welche Förderinstrumente sind nötig?

### SOLAMO / LUBW-Brücke

Die Moorschutzkonzeption Baden-Württemberg setzt den strategischen Rahmen. SOLAMO-BW ergänzt die sozio-ökonomische Perspektive auf betroffene Betriebe, Nutzungskonzepte, Wertschöpfungsketten und Politikempfehlungen.

## 3. Zentrale Kartensteps: deutsche Zielüberschriften

1. Wo liegen die Moore?
2. Wo konzentriert sich der Emissionsdruck?
3. Wo ist der Druck besonders hoch?
4. Größe und Intensität erzählen unterschiedliche Geschichten.
5. Europa: vom globalen Problem zur politischen Umsetzung.
6. Moorvorkommen überschreiten Grenzen.
7. Deutschland: nationale Umsetzungskulisse.
8. Die Thünen-Kulisse konkretisiert organische Böden.
9. Bodenkontext prägt mögliche Nutzungspfade.
10. Baden-Württemberg: regionale Umsetzungsebene.
11. BK50 zeigt Moor- und Feuchtbodenkontext.

## 4. Zu ersetzende Begriffe

| Sichtbarer Begriff | Problem | Ersatzrichtung |
|---|---|---|
| Atlas story | spricht über das Tool | räumliche Einordnung / Kartenfolge |
| Main atlas story | Meta-Sprache | zentrale Kartenfolge |
| Evidence explorer | intern / technisch | Einordnung und Vergleich |
| Prototype appendix | intern / unfertig | Methodische Hinweise / Datenstand |
| Supporting evidence | englisch / intern | ergänzende Einordnung |
| Implementation context | abstrakt | Umsetzungskulisse / regionale Umsetzung |
| Pathways | englisch | Transformationspfade / Nutzungspfade |
| Pressure | abstrakt | Emissionsdruck / Handlungsdruck |
| Extent | abstrakt | Moorverbreitung / räumliche Kulisse |

## 5. Textumfangsregel

- H1: maximal 8 Wörter
- H2: maximal 10 Wörter
- Step-Titel: maximal 8 Wörter
- Step-Text: maximal 1 kurzer Satz oder 2 sehr kurze Sätze
- keine erklärenden Absätze über 45 Wörter
- keine sichtbare Meta-Erklärung über den Atlas als Produkt
"""
    write(OUT_REWRITE, rewrite)

    done_entry = f"""
## B74 - Visible text audit DE ({date.today().isoformat()})

- Extracted visible non-retired text from `index.html`.
- Created `docs/B74_visible_text_audit_de.md`.
- Created `docs/B74_visible_text_inventory.csv`.
- Created `docs/B74_german_rewrite_targets.md`.
- Flagged English text, meta/tool language, long text and method-boundary risks.
- Did not modify application files, maps, scripts, data or styling.
"""
    cur = read(DONE) if DONE.exists() else "# Done\n"
    if "## B74 - Visible text audit DE" not in cur:
        write(DONE, cur.rstrip() + "\n" + done_entry)

    print("B74 visible text audit DE complete.")
    print(f"Visible text elements: {total}")
    print(f"High priority: {high}")
    print(f"Probably English: {english}")
    print(f"Meta/tool language: {meta}")
    print("Changed/created:")
    print(f"  {rel(OUT_MD)}")
    print(f"  {rel(OUT_CSV)}")
    print(f"  {rel(OUT_REWRITE)}")
    print(f"  {rel(DONE)}")

if __name__ == "__main__":
    main()
