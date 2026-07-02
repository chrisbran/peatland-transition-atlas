from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "170_oberschwaben_story_handoff_polish.py"
DOC = ROOT / "docs" / "B170_oberschwaben_story_handoff_polish.md"
AUDIT = ROOT / "docs" / "B170_oberschwaben_story_handoff_polish_audit.txt"
CSV_OUT = ROOT / "docs" / "B170_oberschwaben_handoff_changes.csv"
DONE = ROOT / "tasks" / "done.md"

B169_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"

BRIDGE_START = "<!-- B170_OBERSCHWABEN_HANDOFF_START -->"
BRIDGE_END = "<!-- /B170_OBERSCHWABEN_HANDOFF_END -->"

LEAD_START = "<!-- B170_OBERSCHWABEN_LEAD_START -->"
LEAD_END = "<!-- /B170_OBERSCHWABEN_LEAD_END -->"

CSS_START = "/* B170_OBERSCHWABEN_STORY_HANDOFF_POLISH_START */"
CSS_END = "/* B170_OBERSCHWABEN_STORY_HANDOFF_POLISH_END */"

BRIDGE_HTML = f"""{BRIDGE_START}
<div class="b170-oberschwaben-handoff" aria-label="Übergang vom Maßstab zur Nutzung">
  <p class="b170-handoff-kicker">Übergang</p>
  <p><strong>Bis hierher ging es um Maßstab und Bodenkontext.</strong> Jetzt kommt die heutige Nutzung dazu.</p>
</div>
{BRIDGE_END}"""

LEAD_HTML = f"""{LEAD_START}
<p class="b170-oberschwaben-lead">
  Der vorherige Zoom endet beim regionalen Moor-/Feuchtbodenkontext. Die nächste Karte legt die heutige landwirtschaftliche Nutzung darüber und zeigt, wo aus Kulisse eine konkrete Planungsfrage wird.
</p>
{LEAD_END}"""

TITLE_REPLACEMENTS = [
    (r"Oberschwaben:\s*wo\s+Moorschutz\s+auf\s+Landwirtschaft\s+trifft", "Jetzt kommt die Nutzung dazu"),
    (r"Oberschwaben,\s*wo\s+Moorschutz\s+auf\s+Landwirtschaft\s+trifft", "Jetzt kommt die Nutzung dazu"),
    (r"In\s+Oberschwaben\s+wird\s+Moorbodenschutz\s+konkret", "Jetzt kommt die Nutzung dazu"),
    (r"In\s+Oberschwaben\s+wird\s+Moorbodenschutz\s+zur\s+konkreten\s+Nutzungsfrage", "Jetzt kommt die Nutzung dazu"),
]

CHANGE_ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def add_class_to_opening_tag(opening: str, class_name: str) -> str:
    if class_name in opening:
        return opening

    if re.search(r'\bclass\s*=', opening, re.I):
        opening2 = re.sub(
            r'class="([^"]*)"',
            lambda m: f'class="{m.group(1)} {class_name}"',
            opening,
            count=1,
            flags=re.I,
        )
        opening2 = re.sub(
            r"class='([^']*)'",
            lambda m: f"class='{m.group(1)} {class_name}'",
            opening2,
            count=1,
            flags=re.I,
        )
        return opening2

    return opening[:-1] + f' class="{class_name}">'


def insert_bridge_after_b169(html: str, audit: list[str]) -> str:
    html = strip_block(html, BRIDGE_START, BRIDGE_END)

    pos = html.find(B169_END)
    if pos < 0:
        audit.append("WARN B169 end marker not found; bridge not inserted")
        return html

    insert_pos = pos + len(B169_END)
    html = html[:insert_pos] + "\n" + BRIDGE_HTML + "\n" + html[insert_pos:]
    audit.append("OK inserted B170 bridge after B169 sticky zoom")
    CHANGE_ROWS.append({
        "change": "insert_bridge",
        "status": "applied",
        "detail": "Inserted compact transition after B169 sticky zoom.",
    })
    return html


def find_oberschwaben_section(html: str, audit: list[str]) -> tuple[int, int] | None:
    search_start = html.find(BRIDGE_END)
    if search_start < 0:
        search_start = html.find(B169_END)
    if search_start < 0:
        search_start = 0

    anchors = [
        "Jetzt kommt die Nutzung dazu",
        "Oberschwaben: wo Moorschutz auf Landwirtschaft trifft",
        "Oberschwaben, wo Moorschutz auf Landwirtschaft trifft",
        "Oberschwaben: wo Moorbodenschutz auf Landwirtschaft trifft",
        "Oberschwaben, wo Moorbodenschutz auf Landwirtschaft trifft",
        "Oberschwaben",
    ]

    best = None

    for anchor in anchors:
        pos = html.find(anchor, search_start)
        if pos < 0:
            continue

        section_start = html.rfind("<section", search_start, pos)
        section_end = html.find("</section>", pos)

        if section_start >= 0 and section_end >= 0:
            section_end += len("</section>")
            candidate = html[section_start:section_end]
            lower = candidate.lower()
            score = 0
            if "oberschwaben" in lower:
                score += 4
            if "landwirtschaft" in lower:
                score += 3
            if "moor" in lower:
                score += 2
            if "felt" in lower:
                score -= 1
            if "karten" in lower:
                score += 1

            if best is None or score > best[0]:
                best = (score, section_start, section_end, anchor)

    if best:
        audit.append(f"OK found Oberschwaben section by anchor `{best[3]}` with score {best[0]}")
        return best[1], best[2]

    audit.append("WARN Oberschwaben section not found")
    return None


def polish_oberschwaben_section(html: str, audit: list[str]) -> str:
    bounds = find_oberschwaben_section(html, audit)
    if not bounds:
        CHANGE_ROWS.append({
            "change": "polish_oberschwaben_section",
            "status": "skipped",
            "detail": "Section not found.",
        })
        return html

    start, end = bounds
    section = html[start:end]
    original = section

    m = re.match(r"<section\b[^>]*>", section, re.I | re.S)
    if m:
        new_opening = add_class_to_opening_tag(m.group(0), "b170-oberschwaben-detail")
        if new_opening != m.group(0):
            section = new_opening + section[m.end():]
            audit.append("OK added b170-oberschwaben-detail class")
    else:
        audit.append("WARN could not find Oberschwaben section opening tag")

    title_replacement_count = 0

    def replace_heading(match: re.Match) -> str:
        nonlocal title_replacement_count
        opening, content, closing = match.group(1), match.group(2), match.group(3)
        new_content = content
        for pattern, replacement in TITLE_REPLACEMENTS:
            new_content, n = re.subn(pattern, replacement, new_content, count=1, flags=re.I | re.S)
            title_replacement_count += n
            if n:
                break
        return opening + new_content + closing

    section = re.sub(r"(<h[23]\b[^>]*>)(.*?)(</h[23]>)", replace_heading, section, count=3, flags=re.I | re.S)
    audit.append(f"Oberschwaben title replacements: {title_replacement_count}")

    section = strip_block(section, LEAD_START, LEAD_END)
    hm = re.search(r"</h[23]>", section, re.I)
    if hm:
        section = section[:hm.end()] + "\n" + LEAD_HTML + "\n" + section[hm.end():]
        audit.append("OK inserted B170 Oberschwaben lead after first heading")
    else:
        audit.append("WARN no heading found for B170 Oberschwaben lead insertion")

    duplicated_patterns = [
        r"<p>\s*In\s+Oberschwaben\s+überlagern\s+sich\s+Moor-/Feuchtbodenkontext\s+und\s+heutige\s+Nutzung\.\s*Aus\s+Klima\s+wird\s+eine\s+regionale\s+Nutzungsfrage\.\s*</p>",
        r"<p>\s*In\s+Baden-Württemberg\s+wird\s+Moorschutz\s+zur\s+Planungsfrage:\s*Welche\s+Nutzungen\s+sind\s+berührt,\s*welche\s+betrieblichen\s+Fragen\s+entstehen\s+und\s+welche\s+Produkte\s+könnten\s+tragfähig\s+werden\?\s*</p>",
    ]

    duplicate_removed = 0
    for pattern in duplicated_patterns:
        section, n = re.subn(pattern, "", section, count=1, flags=re.I | re.S)
        duplicate_removed += n

    audit.append(f"Duplicate intro paragraphs removed: {duplicate_removed}")

    html = html[:start] + section + html[end:]

    CHANGE_ROWS.append({
        "change": "polish_oberschwaben_section",
        "status": "applied" if section != original else "no_change",
        "detail": f"title_replacements={title_replacement_count}; duplicate_removed={duplicate_removed}",
    })

    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* B170: make the handoff from scale zoom to regional use feel intentional and compact. */
.b170-oberschwaben-handoff {{
  width: min(100% - 2rem, 76rem);
  margin: clamp(0.75rem, 2vw, 1.5rem) auto clamp(2.25rem, 5vw, 4rem);
  padding-top: clamp(1rem, 2vw, 1.4rem);
  border-top: 1px solid rgba(28, 42, 34, 0.14);
  color: #5e6d63;
}}

.b170-handoff-kicker {{
  margin: 0 0 0.35rem;
  color: #6b7f51;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.b170-oberschwaben-handoff p:last-child {{
  max-width: 46rem;
  margin: 0;
  font-size: clamp(1rem, 1.35vw, 1.18rem);
  line-height: 1.45;
}}

.b170-oberschwaben-handoff strong {{
  color: #1c2a22;
  font-weight: 850;
}}

.b170-oberschwaben-detail {{
  scroll-margin-top: 7rem;
}}

.b170-oberschwaben-lead {{
  max-width: 42rem;
  margin: 1rem 0 clamp(1.25rem, 2vw, 1.75rem);
  color: #5e6d63;
  font-size: clamp(1rem, 1.25vw, 1.12rem);
  line-height: 1.5;
  text-wrap: pretty;
}}

@media (max-width: 760px) {{
  .b170-oberschwaben-handoff {{
    margin-top: 0.25rem;
    margin-bottom: 2rem;
  }}

  .b170-oberschwaben-detail {{
    scroll-margin-top: 5rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B170 Oberschwaben story handoff polish: added a compact transition from the live sticky zoom to the Oberschwaben detail section and reframed the section as the step where current use is added to the regional soil context ({today})."
    if "B170 Oberschwaben story handoff polish" in done_text:
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

    audit = []
    audit.append(f"B169 marker present before patch: {B169_END in html}")
    audit.append(f"Old B170 bridge present before patch: {BRIDGE_START in html and BRIDGE_END in html}")
    audit.append(f"Old B170 CSS present before patch: {CSS_START in css and CSS_END in css}")

    html = strip_block(html, LEAD_START, LEAD_END)
    html = insert_bridge_after_b169(html, audit)
    html = polish_oberschwaben_section(html, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["change", "status", "detail"])
        writer.writeheader()
        writer.writerows(CHANGE_ROWS)

    doc = f"""# B170 - Oberschwaben Story Handoff Polish

Date: {today}

## Ziel

Nach B169e endet der Live-Sticky-Zoom bewusst mit dem regionalen Moor-/Feuchtbodenkontext.
Die Nutzung-×-Bodenkontext-Karte soll erst danach ihre Wirkung entfalten.

B170 poliert genau diesen Übergang:

```text
Maßstab und Bodenkontext → heutige Nutzung kommt dazu
```

## Änderungen

### 1. Kompakter Übergang nach dem Sticky-Zoom

Neu:

```text
Bis hierher ging es um Maßstab und Bodenkontext.
Jetzt kommt die heutige Nutzung dazu.
```

Das ist kein Warnkasten, sondern ein kurzer dramaturgischer Übergang.

### 2. Oberschwaben-Detailsection wird stärker als nächster Schritt gerahmt

Falls die Überschrift erkannt wird, wird sie zu:

```text
Jetzt kommt die Nutzung dazu
```

Zusätzlich ergänzt B170 einen Lead:

```text
Der vorherige Zoom endet beim regionalen Moor-/Feuchtbodenkontext.
Die nächste Karte legt die heutige landwirtschaftliche Nutzung darüber
und zeigt, wo aus Kulisse eine konkrete Planungsfrage wird.
```

### 3. Dopplung reduziert

Häufige alte Intro-Sätze werden entfernt, falls sie direkt doppeln.

## Nicht geändert

- keine neue Karte
- keine neue Datenquelle
- kein Felt-Umbau
- keine Änderung an Wertschöpfungs-Scorecard
- keine Änderung an B169e-Oberschwaben-Zoomkarte

## Prüfen

- Der Übergang nach dem Sticky-Zoom wirkt kurz und editorial.
- Die Oberschwaben-Detailkarte löst die Ankündigung aus dem Zoom ein.
- Keine zusätzliche Warn-/Hinweisflut.
- Kein Gefühl, dass dieselbe Karte zweimal erklärt wird.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    new_css = read(CSS)

    audit_text = "# B170 Oberschwaben story handoff polish audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Post-patch checks:\n"
    audit_text += f"- B170 bridge present: {BRIDGE_START in new_html and BRIDGE_END in new_html}\n"
    audit_text += f"- B170 Oberschwaben lead present: {LEAD_START in new_html and LEAD_END in new_html}\n"
    audit_text += f"- B170 CSS present: {CSS_START in new_css and CSS_END in new_css}\n"
    audit_text += f"- phrase `Jetzt kommt die heutige Nutzung dazu` present: {'Jetzt kommt die heutige Nutzung dazu' in new_html}\n"
    audit_text += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B170 Oberschwaben story handoff polish complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B170_oberschwaben_story_handoff_polish.md")
    print("  docs/B170_oberschwaben_handoff_changes.csv")
    print("  docs/B170_oberschwaben_story_handoff_polish_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA, then visual QA.")


if __name__ == "__main__":
    main()
