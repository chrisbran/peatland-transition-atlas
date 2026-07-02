from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B178_scale_change_area_balance_copy_hardening.md"
AUDIT = ROOT / "docs" / "B178_scale_change_area_balance_copy_hardening_audit.txt"
CSV_OUT = ROOT / "docs" / "B178_copy_hardening_changes.csv"
DONE = ROOT / "tasks" / "done.md"

SCALE_START = "<!-- B178_SCALE_CHANGE_NOTE_START -->"
SCALE_END = "<!-- /B178_SCALE_CHANGE_NOTE_END -->"
AREA_NOTE_START = "<!-- B178_AREA_CAVEAT_START -->"
AREA_NOTE_END = "<!-- /B178_AREA_CAVEAT_END -->"
CSS_START = "/* B178_SCALE_CHANGE_AREA_BALANCE_COPY_HARDENING_START */"
CSS_END = "/* B178_SCALE_CHANGE_AREA_BALANCE_COPY_HARDENING_END */"

SCALE_NOTE = f"""{SCALE_START}
<p class="b178-scale-change-note">
  <strong>Hinweis zum Maßstabswechsel:</strong> Die Deutschlandkarte zeigt die Thünen-Kulisse
  organischer Böden – den klimarelevanten Kern. Die Oberschwaben-Karte nutzt den
  breiteren BK50-Moor-/Feuchtbodenkontext als Prüfkulisse. Beide sind bewusst
  verschieden: Der organische Boden ist die Klimazielgröße, der Feuchtbodenkontext
  markiert zusätzlich, wo genauer hingesehen werden muss.
</p>
{SCALE_END}"""

AREA_CAVEAT = f"""{AREA_NOTE_START}
<span class="b178-area-caveat">
  Oberschwaben, BK50-basiert. Orientierungsgröße, keine Flächeneignung –
  nicht als exakte oder entscheidungsreife Zahl zitieren.
</span>
{AREA_NOTE_END}"""

NEW_BALANCE_TITLE = "Vier von fünf Hektar sind Grünland — und das verändert die Transformationsfrage"

NEW_BALANCE_LEAD = """Rund 82&nbsp;% der Schnittmenge ist Grünland. Das ist die vergleichsweise anschlussfähige Seite der Bilanz: Grünland lässt sich eher an höhere Wasserstände anpassen als Ackerland. Die eigentliche Härte steckt in den rund 16&nbsp;% Ackerland und in kleineren Sonderfällen, wo Nutzung und nasser Boden schwerer zusammengehen."""

CHANGE_ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def record(change: str, status: str, detail: str) -> None:
    CHANGE_ROWS.append({"change": change, "status": status, "detail": detail})


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


def insert_scale_change_note(html: str) -> str:
    html = strip_block(html, SCALE_START, SCALE_END)

    # Preferred insertion: after the B169 data/source line that names Thünen and BK50.
    candidates = [
        r"(<p\b[^>]*class=[\"'][^\"']*b169-source-line[^\"']*[\"'][^>]*>.*?</p>)",
        r"(<p\b[^>]*>[^<]*(?:Global Peatland Map 2\.0|Thünen-Kulisse organischer Böden|BK50 Baden-Württemberg)[\s\S]*?Methode\s+in\s+Kürze[\s\S]*?</p>)",
    ]

    for pattern in candidates:
        matches = list(re.finditer(pattern, html, flags=re.I | re.S))
        if matches:
            # Use the last matching source paragraph in the B169 area.
            match = matches[0]
            for m in matches:
                if "Thünen" in m.group(0) or "BK50" in m.group(0) or "b169-source-line" in m.group(0):
                    match = m
                    break
            html = html[:match.end()] + "\n" + SCALE_NOTE + "\n" + html[match.end():]
            record("scale_change_note", "inserted", "Inserted B178 scale-change note after B169 source line.")
            return html

    record("scale_change_note", "skipped", "Could not find a safe B169 source-line insertion point.")
    return html


def find_area_balance_section(html: str):
    # Locate by robust anchors used in the published page.
    anchors = [
        "Die Schnittmenge zeigt die Größenordnung",
        "~19.900 ha landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext",
        "Flächenbilanz",
    ]

    for anchor in anchors:
        pos = html.find(anchor)
        if pos < 0:
            continue
        start = html.rfind("<section", 0, pos)
        end = html.find("</section>", pos)
        if start >= 0 and end >= 0:
            return start, end + len("</section>"), anchor

    return None


def patch_area_balance(html: str) -> str:
    html = strip_block(html, AREA_NOTE_START, AREA_NOTE_END)

    bounds = find_area_balance_section(html)
    if not bounds:
        record("area_balance", "skipped", "Could not locate Flächenbilanz section.")
        return html

    start, end, anchor = bounds
    section = html[start:end]
    original = section

    # Add class to section.
    m = re.match(r"<section\b[^>]*>", section, flags=re.I | re.S)
    if m:
        new_opening = add_class_to_opening_tag(m.group(0), "b178-area-balance")
        section = new_opening + section[m.end():]

    # Replace the main section title if present.
    title_patterns = [
        r"(<h[1-4]\b[^>]*>)\s*Die\s+Schnittmenge\s+zeigt\s+die\s+Größenordnung\s*(</h[1-4]>)",
        r"(<h[1-4]\b[^>]*>)\s*Flächenbilanz\s*(</h[1-4]>)",
    ]
    title_done = False
    for pattern in title_patterns:
        section, n = re.subn(pattern, rf"\1{NEW_BALANCE_TITLE}\2", section, count=1, flags=re.I | re.S)
        if n:
            title_done = True
            break
    record("balance_title", "replaced" if title_done else "not_found", NEW_BALANCE_TITLE)

    # Replace/strengthen the neutral first lead paragraph after heading.
    neutral_patterns = [
        r"<p\b[^>]*>\s*Die\s+Verschneidung\s+zeigt,\s*dass\s+die\s+Überschneidung\s+von\s+landwirtschaftlicher\s+Nutzung\s+und\s+Moor-/Feuchtbodenkontext\s+auch\s+in\s+der\s+Bilanz\s+relevant\s+wird\.\s*</p>",
        r"<p\b[^>]*>\s*Diese\s+Werte\s+zeigen\s+Größenordnung\s+und\s+Nutzungsmix\.\s*</p>",
    ]

    lead_done = False
    for pattern in neutral_patterns:
        section, n = re.subn(pattern, f'<p class="b178-balance-lead">{NEW_BALANCE_LEAD}</p>', section, count=1, flags=re.I | re.S)
        if n:
            lead_done = True
            break

    if not lead_done:
        # Insert after first heading inside the section.
        hm = re.search(r"</h[1-4]>", section, flags=re.I)
        if hm:
            section = section[:hm.end()] + f'\n<p class="b178-balance-lead">{NEW_BALANCE_LEAD}</p>\n' + section[hm.end():]
            lead_done = True

    record("balance_lead", "inserted_or_replaced" if lead_done else "skipped", "Added interpretive 82% Grünland / 16% Ackerland lead.")

    # Attach screenshot-proof caveat to the 19,900 ha metric.
    area_patterns = [
        r"(<[^>]*>\s*~?19[.,]\s*900\s*ha\s+landwirtschaftliche\s+Nutzung\s+im\s+Moor-/Feuchtbodenkontext\s*</[^>]+>)",
        r"(<[^>]*>\s*~?19[.,]\s*900\s*ha[^<]*</[^>]+>)",
    ]

    caveat_done = False
    for pattern in area_patterns:
        def repl(match: re.Match) -> str:
            return match.group(1) + "\n" + AREA_CAVEAT
        section, n = re.subn(pattern, repl, section, count=1, flags=re.I | re.S)
        if n:
            caveat_done = True
            break

    if not caveat_done:
        section = re.sub(
            r"(~?19[.,]\s*900\s*ha\s+landwirtschaftliche\s+Nutzung\s+im\s+Moor-/Feuchtbodenkontext)",
            r"\1 " + AREA_CAVEAT,
            section,
            count=1,
            flags=re.I,
        )
        caveat_done = AREA_START_PRESENT = AREA_NOTE_START in section

    record("area_caveat", "inserted" if caveat_done else "skipped", "Added screenshot-proof caveat directly to 19,900 ha number.")

    # Avoid duplicating older generic hint if it now doubles the new caveat too closely.
    section, removed_hint = re.subn(
        r"<p\b[^>]*>\s*Hinweis:\s*Diese\s+Werte\s+zeigen\s+Größenordnung\s+und\s+Nutzungsmix\.\s*Entscheidungen\s+entstehen\s+erst\s+in\s+der\s+Standortprüfung\.\s*</p>\s*",
        "",
        section,
        count=1,
        flags=re.I | re.S,
    )
    record("old_generic_area_hint", "removed" if removed_hint else "not_found", "Removed generic hint if superseded by B178 inline caveat.")

    if section == original:
        record("area_balance", "no_change", f"Located by anchor {anchor}, but no edits applied.")
    else:
        record("area_balance", "patched", f"Located by anchor {anchor}.")

    return html[:start] + section + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* B178: small copy-hardening elements for scale-change honesty and screenshot-safe area figures. */
.b178-scale-change-note {{
  max-width: 48rem;
  margin: clamp(0.9rem, 2vw, 1.35rem) auto 0;
  padding: 0.9rem 1rem;
  border-left: 3px solid rgba(107, 127, 81, 0.85);
  border-radius: 0.75rem;
  background: rgba(250, 248, 241, 0.08);
  color: rgba(245, 242, 232, 0.82);
  font-size: 0.9rem;
  line-height: 1.48;
  text-wrap: pretty;
}}

.b178-scale-change-note strong {{
  color: rgba(255, 255, 255, 0.94);
  font-weight: 850;
}}

.b178-area-balance {{
  scroll-margin-top: 7rem;
}}

.b178-balance-lead {{
  max-width: 48rem;
  margin: 1rem 0 clamp(1.25rem, 2.5vw, 2rem);
  color: #334238;
  font-size: clamp(1.02rem, 1.35vw, 1.18rem);
  line-height: 1.5;
  text-wrap: pretty;
}}

.b178-area-caveat {{
  display: block;
  max-width: 36rem;
  margin-top: 0.55rem;
  color: #6b766d;
  font-size: clamp(0.82rem, 1.05vw, 0.92rem);
  font-weight: 520;
  line-height: 1.35;
}}

@media (max-width: 760px) {{
  .b178-scale-change-note {{
    margin-top: 0.75rem;
    padding: 0.8rem 0.85rem;
    font-size: 0.86rem;
  }}

  .b178-area-caveat {{
    font-size: 0.82rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B178 scale-change and area-balance copy hardening: added an explicit Thünen-vs-BK50 scale-change note, made the 19,900-ha figure screenshot-safe, and reframed the area balance around the 82% Grünland / 16% Ackerland interpretation ({today})."
    if "B178 scale-change and area-balance copy hardening" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    html_before = read(INDEX)
    css_before = read(CSS)

    pre_counts = {
        "scale_note": html_before.count(SCALE_START),
        "area_caveat": html_before.count(AREA_NOTE_START),
        "old_title": html_before.count("Die Schnittmenge zeigt die Größenordnung"),
        "new_title": html_before.count(NEW_BALANCE_TITLE),
        "nineteen_ha": len(re.findall(r"19[.,]\s*900\s*ha", html_before, flags=re.I)),
    }

    html = html_before
    html = insert_scale_change_note(html)
    html = patch_area_balance(html)
    css = patch_css(css_before)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)

    post_counts = {
        "scale_note": html_after.count(SCALE_START),
        "area_caveat": html_after.count(AREA_NOTE_START),
        "old_title": html_after.count("Die Schnittmenge zeigt die Größenordnung"),
        "new_title": html_after.count(NEW_BALANCE_TITLE),
        "nineteen_ha": len(re.findall(r"19[.,]\s*900\s*ha", html_after, flags=re.I)),
    }

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["change", "status", "detail"], delimiter=";")
        writer.writeheader()
        writer.writerows(CHANGE_ROWS)

    doc = f"""# B178 - Scale-Change and Area-Balance Copy Hardening

Date: {today}

## Ziel

B178 härtet drei kleine, aber publizistisch wichtige Stellen:

1. Der Maßstabswechsel von der nationalen Thünen-Kulisse organischer Böden zur regionalen BK50-Moor-/Feuchtbodenkulisse wird explizit benannt.
2. Die `~19.900 ha`-Zahl wird screenshot-fester, indem der Vorbehalt direkt an die Zahl gekoppelt wird.
3. Die Flächenbilanz bekommt eine interpretierende Pointe: `82 % Grünland` ist nicht nur eine Statistik, sondern sagt etwas über die Transformationshärte.

## Neuer Hinweis zum Maßstabswechsel

```text
Hinweis zum Maßstabswechsel: Die Deutschlandkarte zeigt die Thünen-Kulisse
organischer Böden – den klimarelevanten Kern. Die Oberschwaben-Karte nutzt den
breiteren BK50-Moor-/Feuchtbodenkontext als Prüfkulisse. Beide sind bewusst
verschieden: Der organische Boden ist die Klimazielgröße, der Feuchtbodenkontext
markiert zusätzlich, wo genauer hingesehen werden muss.
```

## Neue Bilanzpointe

```text
{NEW_BALANCE_TITLE}
```

Lead:

```text
Rund 82 % der Schnittmenge ist Grünland. Das ist die vergleichsweise anschlussfähige Seite der Bilanz: Grünland lässt sich eher an höhere Wasserstände anpassen als Ackerland. Die eigentliche Härte steckt in den rund 16 % Ackerland und in kleineren Sonderfällen, wo Nutzung und nasser Boden schwerer zusammengehen.
```

## Screenshot-fester Zusatz zur Zahl

```text
Oberschwaben, BK50-basiert. Orientierungsgröße, keine Flächeneignung –
nicht als exakte oder entscheidungsreife Zahl zitieren.
```

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- kein B169-Sticky-Zoom
- keine B176-Felt-Entfernung
- keine Quellenstruktur
- keine raw GIS/Data

## Counts

| Signal | Vorher | Nachher |
|---|---:|---:|
| Scale note marker | {pre_counts['scale_note']} | {post_counts['scale_note']} |
| Area caveat marker | {pre_counts['area_caveat']} | {post_counts['area_caveat']} |
| Alte Bilanzüberschrift | {pre_counts['old_title']} | {post_counts['old_title']} |
| Neue Bilanzüberschrift | {pre_counts['new_title']} | {post_counts['new_title']} |
| 19.900-ha-Erwähnungen | {pre_counts['nineteen_ha']} | {post_counts['nineteen_ha']} |
"""
    write(DOC, doc)

    audit = "# B178 scale-change and area-balance copy hardening audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += "Post-patch checks:\n"
    audit += f"- Scale-change note present exactly once: {post_counts['scale_note'] == 1}\n"
    audit += f"- Area caveat present exactly once: {post_counts['area_caveat'] == 1}\n"
    audit += f"- New balance title present: {NEW_BALANCE_TITLE in html_after}\n"
    audit += f"- Old neutral balance title absent: {'Die Schnittmenge zeigt die Größenordnung' not in html_after}\n"
    audit += f"- 82% interpretation present: {'82&nbsp;%' in html_after and '16&nbsp;%' in html_after}\n"
    audit += f"- B176 local cartographic depth still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}\n"
    audit += f"- No Felt token in index: {'felt' not in html_after.lower()}\n"
    audit += f"- No iframe in index: {'<iframe' not in html_after.lower()}\n"
    audit += f"- B169 live sticky zoom still present: {'B169_LIVE_STICKY_ZOOM_START' in html_after}\n"
    audit += f"- B178 CSS present: {CSS_START in css_after and CSS_END in css_after}\n"
    audit += "\nChanges:\n"
    for row in CHANGE_ROWS:
        audit += f"- {row['change']}: {row['status']} — {row['detail']}\n"
    audit += "\nResult: PATCH WRITTEN. Run B177, B103b and B58 before commit.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B178 scale-change and area-balance copy hardening complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B178_scale_change_area_balance_copy_hardening.md")
    print("  docs/B178_copy_hardening_changes.csv")
    print("  docs/B178_scale_change_area_balance_copy_hardening_audit.txt")
    print("  tasks/done.md")
    print("Post-patch checks:")
    print(f"  scale note exactly once: {post_counts['scale_note'] == 1}")
    print(f"  area caveat exactly once: {post_counts['area_caveat'] == 1}")
    print(f"  new title present: {NEW_BALANCE_TITLE in html_after}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
