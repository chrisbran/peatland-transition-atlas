from pathlib import Path
import re
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "162c_keep_and_polish_value_chain_scorecard.py"
DOC = ROOT / "docs" / "B162c_keep_and_polish_value_chain_scorecard.md"
AUDIT = ROOT / "docs" / "B162c_keep_and_polish_value_chain_scorecard_audit.txt"
DONE = ROOT / "tasks" / "done.md"

CSS_START = "/* B162C_KEEP_AND_POLISH_VALUE_CHAIN_SCORECARD_START */"
CSS_END = "/* B162C_KEEP_AND_POLISH_VALUE_CHAIN_SCORECARD_END */"

ANCHORS = [
    "Bis zur Ernte ist die Kette oft anschlussfähig",
    "Bis zur Ernte ist vieles anschlussfähig",
    "Anbau",
    "Aufbereitung & Logistik",
]

NEW_TITLE = "Bis zur Ernte ist vieles anschlussfähig.<br>Danach wird es eng."

NEW_LEAD = (
    "Die Grafik verdichtet die zentrale Engstelle: Auf dem Feld und bis zur Ernte "
    "gibt es erprobte Ansätze. Dahinter entscheiden Logistik, Verarbeitung, Standards "
    "und Abnahme darüber, ob nasse Nutzung skalierbar wird."
)

OLD_NOTE_PATTERNS = [
    (
        r"Qualitative\s+Einordnung,\s+keine\s+Präzisionszahlen\s+und\s+keine\s+formale\s+Bewertung\s+einzelner\s+Produkte\s+oder\s+Regionen\.",
        "Qualitative Synthese, keine Messgrafik und keine formale Bewertung einzelner Produkte oder Regionen."
    ),
]

TITLE_RE = re.compile(
    r"(<h2\b[^>]*>)(?:(?!</h2>).)*?"
    r"Bis\s+zur\s+Ernte\s+ist\s+die\s+Kette\s+oft\s+anschlussfähig\s*(?:—|&mdash;|-)\s*"
    r"danach\s+besteht\s+häufig\s+Entwicklungsbedarf\.?"
    r"(?:(?!</h2>).)*?(</h2>)",
    re.S | re.I,
)

TITLE_ALREADY_RE = re.compile(
    r"(<h2\b[^>]*>)(?:(?!</h2>).)*?"
    r"Bis\s+zur\s+Ernte\s+ist\s+vieles\s+anschlussfähig\.?\s*(?:<br\s*/?>|\s+)"
    r"Danach\s+wird\s+es\s+eng\.?"
    r"(?:(?!</h2>).)*?(</h2>)",
    re.S | re.I,
)

LEAD_RE = re.compile(
    r"<p\b([^>]*)>\s*"
    r"Die\s+Grafik\s+ordnet\s+typische\s+Stufen\s+der\s+Wertschöpfungskette\s+für\s+nasse\s+Moornutzung\s+qualitativ\s+ein\.\s*"
    r"Sie\s+zeigt\s+keine\s+Messwerte,\s+sondern\s+eine\s+fachlich\s+begründete,\s+bewusst\s+vereinfachte\s+Synthese:\s*"
    r"Stromaufwärts\s+gibt\s+es\s+bereits\s+erprobte\s+Ansätze,\s+stromabwärts\s+liegen\s+die\s+größeren\s+Entwicklungsaufgaben\s+häufig\s+bei\s+Verarbeitung,\s+Abnahme,\s+Standards\s+und\s+verlässlichen\s+Mengen\.\s*"
    r"</p>",
    re.S | re.I,
)

LEAD_ALREADY_RE = re.compile(
    r"<p\b[^>]*class=\"[^\"]*b162c-scorecard-lead[^\"]*\"[^>]*>.*?</p>",
    re.S | re.I,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def find_scorecard_section(html: str, audit: list[str]) -> tuple[int, int] | None:
    # Prefer the actual scorecard title.
    for anchor in ANCHORS:
        pos = html.find(anchor)
        if pos < 0:
            continue

        section_start = html.rfind("<section", 0, pos)
        section_end = html.find("</section>", pos)

        if section_start >= 0 and section_end >= 0:
            section_end += len("</section>")
            audit.append(f"OK found value-chain scorecard section by anchor: {anchor}")
            return section_start, section_end

        audit.append(f"WARN anchor found but section bounds missing: {anchor}")

    audit.append("ERROR value-chain scorecard section not found")
    return None


def add_section_class(section: str, audit: list[str]) -> str:
    m = re.match(r"<section\b[^>]*>", section, re.S | re.I)
    if not m:
        audit.append("WARN could not find section opening tag")
        return section

    opening = m.group(0)
    if "b162c-scorecard-polish" in opening:
        audit.append("OK b162c section class already present")
        return section

    if re.search(r'\bclass\s*=', opening, re.I):
        new_opening = re.sub(
            r'class="([^"]*)"',
            lambda mm: f'class="{mm.group(1)} b162c-scorecard-polish"',
            opening,
            count=1,
            flags=re.I,
        )
        if new_opening == opening:
            new_opening = re.sub(
                r"class='([^']*)'",
                lambda mm: f"class='{mm.group(1)} b162c-scorecard-polish'",
                opening,
                count=1,
                flags=re.I,
            )
    else:
        new_opening = opening[:-1] + ' class="b162c-scorecard-polish">'

    audit.append("OK added b162c-scorecard-polish section class")
    return new_opening + section[len(opening):]


def replace_title(section: str, audit: list[str]) -> str:
    if TITLE_ALREADY_RE.search(section):
        audit.append("OK scorecard title already polished")
        return section

    section, n = TITLE_RE.subn(r"\1" + NEW_TITLE + r"\2", section, count=1)
    audit.append(f"Title replacements: {n}")
    if n == 0:
        audit.append("WARN title pattern not matched; check scorecard heading manually")
    return section


def replace_lead(section: str, audit: list[str]) -> str:
    replacement = f'<p class="b162c-scorecard-lead">{NEW_LEAD}</p>'

    if LEAD_ALREADY_RE.search(section):
        section, n = LEAD_ALREADY_RE.subn(replacement, section, count=1)
        audit.append(f"Lead already-polished replacements: {n}")
        return section

    section, n = LEAD_RE.subn(replacement, section, count=1)
    audit.append(f"Lead replacements: {n}")
    if n == 0:
        audit.append("WARN lead paragraph pattern not matched; check intro paragraph manually")
    return section


def replace_notes(section: str, audit: list[str]) -> str:
    for pattern, replacement in OLD_NOTE_PATTERNS:
        section, n = re.subn(pattern, replacement, section, count=1, flags=re.S | re.I)
        audit.append(f"Note replacement `{replacement[:32]}...`: {n}")
    return section


def patch_scorecard(html: str, audit: list[str]) -> str:
    bounds = find_scorecard_section(html, audit)
    if not bounds:
        raise SystemExit("Could not find value-chain scorecard section.")

    start, end = bounds
    section = html[start:end]

    section = add_section_class(section, audit)
    section = replace_title(section, audit)
    section = replace_lead(section, audit)
    section = replace_notes(section, audit)

    return html[:start] + section + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* Keep the existing dark scorecard direction; polish hierarchy rather than replacing it. */
.b162c-scorecard-polish {{
  position: relative;
}}

.b162c-scorecard-polish h2 {{
  max-width: 12.5em;
  letter-spacing: -0.025em;
  line-height: 1.05;
}}

.b162c-scorecard-polish .b162c-scorecard-lead {{
  max-width: 58rem;
  margin-top: 1rem;
  color: rgba(245, 241, 232, 0.82);
  font-size: clamp(1rem, 1.25vw, 1.13rem);
  line-height: 1.48;
}}

.b162c-scorecard-polish .b162c-scorecard-lead + * {{
  margin-top: clamp(1.3rem, 2.6vw, 2rem);
}}

.b162c-scorecard-polish h3,
.b162c-scorecard-polish h4 {{
  text-wrap: balance;
}}

.b162c-scorecard-polish [class*="card"] {{
  transition: transform 160ms ease, border-color 160ms ease, background-color 160ms ease;
}}

.b162c-scorecard-polish [class*="card"]:hover {{
  transform: translateY(-2px);
}}

.b162c-scorecard-polish [class*="legend"],
.b162c-scorecard-polish [class*="source"],
.b162c-scorecard-polish [class*="note"] {{
  color: rgba(245, 241, 232, 0.72);
}}

@media (max-width: 760px) {{
  .b162c-scorecard-polish h2 {{
    max-width: 11.5em;
  }}

  .b162c-scorecard-polish .b162c-scorecard-lead {{
    font-size: 0.96rem;
    line-height: 1.48;
  }}

  .b162c-scorecard-polish [class*="card"]:hover {{
    transform: none;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B162c keep and polish value-chain scorecard: kept the existing dark scorecard direction, sharpened the title and shortened the lead instead of replacing it with the B162 wireframe ({today})."
    if "B162c keep and polish value-chain scorecard" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()
    audit: list[str] = []

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    html = read(INDEX)
    css = read(CSS)

    audit.append(f"Old B162c CSS present before patch: {CSS_START in css and CSS_END in css}")
    audit.append(f"Old scorecard title present before patch: {'Bis zur Ernte ist die Kette oft anschlussfähig' in html}")
    audit.append(f"Polished scorecard title present before patch: {'Bis zur Ernte ist vieles anschlussfähig' in html}")

    html = patch_scorecard(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    doc = f"""# B162c - Keep and Polish Value-Chain Scorecard

Date: {today}

## Ziel

B162/B162b waren als Experiment sinnvoll, aber der SVG-Wireframe war nicht stärker als die vorhandene dunkle Scorecard.
B162c korrigiert die Richtung:

```text
Nicht ersetzen. Premiumisieren.
```

## Entscheidung

Die bestehende dunkle Scorecard bleibt die Basis für den Wertschöpfungs-Climax.

Warum:

- die dunkle Bühne ist stark
- die Farbdramaturgie ist sofort verständlich
- die Kartenfolge ist ruhig und seriös
- das Modul sitzt bereits gut im Seitenfluss
- es wirkt weniger didaktisch als der Wireframe

## Änderungen

### 1. Titel geschärft

Alt:

```text
Bis zur Ernte ist die Kette oft anschlussfähig —
danach besteht häufig Entwicklungsbedarf.
```

Neu:

```text
Bis zur Ernte ist vieles anschlussfähig.
Danach wird es eng.
```

### 2. Lead gekürzt

Der erklärende Absatz wird halbiert und stärker auf die zentrale These ausgerichtet:

```text
Auf dem Feld und bis zur Ernte gibt es erprobte Ansätze.
Dahinter entscheiden Logistik, Verarbeitung, Standards und Abnahme darüber,
ob nasse Nutzung skalierbar wird.
```

### 3. Methodische Fußnote ruhiger formuliert

Aus der langen Einordnung wird:

```text
Qualitative Synthese, keine Messgrafik und keine formale Bewertung einzelner Produkte oder Regionen.
```

### 4. Leichte CSS-Politur

- stärkere Titelhierarchie
- Lead ruhiger
- leichte Hover-Anhebung der Karten auf Desktop
- keine strukturelle Änderung der Scorecard

## Nicht geändert

- kein Einbau des SVG-Wireframes
- keine neue Grafik
- keine neue Datenbehauptung
- keine Änderung an Quellenbasis
- keine Änderung an Matrix
- keine Änderung an Felt/Oberschwaben

## Folgeentscheidung

B162/B162b bleiben als dokumentiertes Experiment nützlich, sollten aber nicht die Richtung der öffentlichen Seite bestimmen.
Für die nächste konkrete UI-Arbeit ist die Scorecard-Basis maßgeblich.
"""
    write(DOC, doc)

    audit_text = "# B162c keep and polish value-chain scorecard audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Result: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B162c keep and polish value-chain scorecard complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B162c_keep_and_polish_value_chain_scorecard.md")
    print("  docs/B162c_keep_and_polish_value_chain_scorecard_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA.")


if __name__ == "__main__":
    main()
