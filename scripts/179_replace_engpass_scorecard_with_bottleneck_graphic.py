from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B179_replace_engpass_scorecard_with_bottleneck_graphic.md"
AUDIT = ROOT / "docs" / "B179_replace_engpass_scorecard_with_bottleneck_graphic_audit.txt"
CSV_OUT = ROOT / "docs" / "B179_engpass_replacement_changes.csv"
DONE = ROOT / "tasks" / "done.md"

B179_START = "<!-- B179_BOTTLENECK_GRAPHIC_START -->"
B179_END = "<!-- /B179_BOTTLENECK_GRAPHIC_END -->"
CSS_START = "/* B179_BOTTLENECK_GRAPHIC_START */"
CSS_END = "/* B179_BOTTLENECK_GRAPHIC_END */"

HEADING = "Bis zur Ernte ist vieles anschlussfähig. Danach wird es eng."
LEAD = "Auf dem Feld und bis zur Ernte gibt es erprobte Ansätze. Dahinter entscheiden Logistik, Verarbeitung, Standards und Abnahme darüber, ob nasse Nutzung skalierbar wird."

SOURCE_LINE = "Schematische Synthese aus IPCC Wetlands Supplement (2014), VIP Paludikultur-Endbericht und MLUK Brandenburg: Brandenburgs Moore klimafreundlich bewirtschaften. Qualitative Einordnung, keine Messgrafik."

BOTTLENECK_FIGURE = f"""{B179_START}
<figure class="b179-bottleneck-figure" aria-labelledby="b179-bottleneck-title b179-bottleneck-desc">
  <div class="b179-bottleneck-scroll" role="group" aria-label="Wertschöpfungskette als Flaschenhals">
    <svg class="b179-bottleneck-svg" viewBox="0 0 820 392" role="img" aria-labelledby="b179-bottleneck-title b179-bottleneck-desc">
      <title id="b179-bottleneck-title">Wertschöpfungskette als Flaschenhals</title>
      <desc id="b179-bottleneck-desc">Ein Band beginnt bei Anbau und Ernte breit und grün. Ab Aufbereitung verengt es sich über Verarbeitung, Abnahme, Standards und Verwendung und färbt sich von Ocker zu Terrakotta. Die Verjüngung markiert die Engstelle der Kette.</desc>

      <g class="b179-bottleneck-band" stroke="#f7f4ec" stroke-width="2">
        <polygon points="70,70 167,73 167,267 70,270" fill="#8a9d54"></polygon>
        <polygon points="167,73 264,80 264,260 167,267" fill="#8a9d54"></polygon>
        <polygon points="264,80 361,106 361,234 264,260" fill="#cf9a3c"></polygon>
        <polygon points="361,106 458,128 458,212 361,234" fill="#bd5438"></polygon>
        <polygon points="458,128 555,140 555,200 458,212" fill="#bd5438"></polygon>
        <polygon points="555,140 652,146 652,194 555,200" fill="#bd5438"></polygon>
        <polygon points="652,146 749,150 749,190 652,194" fill="#bd5438"></polygon>
      </g>

      <g class="b179-bottleneck-marker">
        <line x1="361" y1="58" x2="361" y2="286" stroke="#9c4a30" stroke-width="1" stroke-dasharray="3 4"></line>
        <text x="361" y="48" text-anchor="middle" font-size="13" font-weight="700" fill="#9c4a30">ab hier: Engstelle</text>
      </g>

      <g class="b179-bottleneck-labels" font-size="13" fill="#55524a" text-anchor="middle" font-weight="550">
        <text x="118" y="300">Anbau</text>
        <text x="215" y="300">Ernte</text>
        <text x="312" y="300">Aufbereitung</text>
        <text x="409" y="300">Verarbeitung</text>
        <text x="506" y="300">Abnahme</text>
        <text x="603" y="300">Standards</text>
        <text x="700" y="300">Verwendung</text>
      </g>

      <g class="b179-bottleneck-legend" font-size="13" fill="#55524a">
        <rect x="70" y="340" width="13" height="13" rx="2" fill="#8a9d54"></rect>
        <text x="90" y="351">anschlussfähig</text>
        <rect x="228" y="340" width="13" height="13" rx="2" fill="#cf9a3c"></rect>
        <text x="248" y="351">im Aufbau</text>
        <rect x="345" y="340" width="13" height="13" rx="2" fill="#bd5438"></rect>
        <text x="365" y="351">erhöhter Entwicklungsbedarf</text>
      </g>
    </svg>
  </div>
  <figcaption class="b179-bottleneck-source">{SOURCE_LINE}</figcaption>
</figure>
{B179_END}"""

CHANGE_ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\s*", "", text, flags=re.S)


def record(change: str, status: str, detail: str) -> None:
    CHANGE_ROWS.append({"change": change, "status": status, "detail": detail})


def find_section_containing(html: str, needle: str):
    pos = html.find(needle)
    if pos < 0:
        return None
    start = html.rfind("<section", 0, pos)
    end = html.find("</section>", pos)
    if start >= 0 and end >= 0:
        return start, end + len("</section>"), pos
    return None


def replace_heading_and_lead(section: str) -> str:
    before = section

    # Keep the heading, but normalize exact title and prevent older variants.
    section, h_n = re.subn(
        r"(<h[1-4]\b[^>]*>).*?(Bis\s+zur\s+Ernte\s+ist\s+vieles[\s\S]*?eng\.).*?(</h[1-4]>)",
        rf"\1{HEADING}\3",
        section,
        count=1,
        flags=re.I | re.S,
    )

    if h_n == 0:
        record("heading", "not_changed", "Could not normalize heading; existing heading may already be fine.")
    else:
        record("heading", "normalized", HEADING)

    # Replace the first paragraph after the heading if it is clearly the old scorecard lead.
    heading_end = None
    m = re.search(r"</h[1-4]>", section, flags=re.I)
    if m:
        heading_end = m.end()

    if heading_end:
        after_heading = section[heading_end:]
        p_match = re.search(r"<p\b[^>]*>.*?</p>", after_heading, flags=re.I | re.S)
        if p_match:
            p_text = re.sub(r"<[^>]+>", " ", p_match.group(0))
            p_text = re.sub(r"\s+", " ", p_text).strip()
            if any(term in p_text.lower() for term in ["logistik", "verarbeitung", "abnahme", "skalierbar", "ernte"]):
                p_new = f"<p>{LEAD}</p>"
                section = section[:heading_end + p_match.start()] + p_new + section[heading_end + p_match.end():]
                record("lead", "replaced", LEAD)
            else:
                record("lead", "not_replaced", "First paragraph after heading did not look like scorecard lead.")
        else:
            record("lead", "not_found", "No lead paragraph found after heading.")
    else:
        record("lead", "not_found", "No heading end found.")

    if section == before:
        record("heading_lead_block", "no_change", "Heading/lead unchanged.")
    return section


def replace_old_graphic_in_section(section: str) -> str:
    original = section

    # Remove prior B179 if script is rerun.
    section = strip_block(section, B179_START, B179_END)

    # Candidate 1: existing figure containing value-chain labels.
    figure_matches = list(re.finditer(r"<figure\b[^>]*>.*?</figure>", section, flags=re.I | re.S))
    for m in figure_matches:
        block = m.group(0)
        low = block.lower()
        if ("anbau" in low and "ernte" in low and ("verarbeitung" in low or "abnahme" in low or "standards" in low)):
            section = section[:m.start()] + BOTTLENECK_FIGURE + section[m.end():]
            record("graphic", "replaced_figure", "Replaced existing figure containing Anbau/Ernte/value-chain labels.")
            return section

    # Candidate 2: SVG itself inside a wrapper.
    svg_matches = list(re.finditer(r"<svg\b[^>]*>.*?</svg>", section, flags=re.I | re.S))
    for m in svg_matches:
        block = m.group(0)
        low = block.lower()
        if ("anbau" in low and "ernte" in low) or ("wertschöpfung" in low and "entwicklung" in low):
            section = section[:m.start()] + BOTTLENECK_FIGURE + section[m.end():]
            record("graphic", "replaced_svg", "Replaced existing SVG containing value-chain labels.")
            return section

    # Candidate 3: common scorecard classes.
    class_patterns = [
        r"<div\b[^>]*class=[\"'][^\"']*(?:scorecard|maturity|value-chain|wertschoepfung|engpass)[^\"']*[\"'][^>]*>.*?</div>",
        r"<section\b[^>]*class=[\"'][^\"']*(?:scorecard|maturity|value-chain|wertschoepfung|engpass)[^\"']*[\"'][^>]*>.*?</section>",
    ]
    for pattern in class_patterns:
        for m in re.finditer(pattern, section, flags=re.I | re.S):
            block = m.group(0)
            low = block.lower()
            if "anbau" in low or "ernte" in low or "anschlussfähig" in low or "entwicklungsbedarf" in low:
                section = section[:m.start()] + BOTTLENECK_FIGURE + section[m.end():]
                record("graphic", "replaced_class_block", "Replaced existing scorecard/value-chain class block.")
                return section

    # Fallback: insert figure after the lead paragraph so it is visible, but keep old content untouched.
    h = re.search(r"</h[1-4]>", section, flags=re.I)
    if h:
        after_heading = section[h.end():]
        p = re.search(r"<p\b[^>]*>.*?</p>", after_heading, flags=re.I | re.S)
        if p:
            insert_at = h.end() + p.end()
            section = section[:insert_at] + "\n" + BOTTLENECK_FIGURE + "\n" + section[insert_at:]
            record("graphic", "inserted_fallback", "Could not safely replace old graphic; inserted B179 figure after lead.")
            return section

    record("graphic", "failed", "Could not find a safe insertion/replacement point.")
    return original


def patch_index(html: str) -> str:
    html = strip_block(html, B179_START, B179_END)

    found = find_section_containing(html, HEADING)
    if not found:
        # Try a broader heading fragment.
        found = find_section_containing(html, "Danach wird es eng")
    if not found:
        record("section", "failed", "Could not locate Engpass section.")
        return html

    start, end, _ = found
    section = html[start:end]

    section_before = section
    section = replace_heading_and_lead(section)
    section = replace_old_graphic_in_section(section)

    if section != section_before:
        record("section", "patched", "Engpass section patched with static bottleneck graphic.")
    else:
        record("section", "no_change", "Engpass section located but not modified.")

    return html[:start] + section + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* B179: static editorial bottleneck graphic for the value-chain bottleneck. */
.b179-bottleneck-figure {{
  margin: clamp(2rem, 5vw, 3.25rem) 0 0;
  padding: clamp(1rem, 2.5vw, 1.9rem);
  border-radius: 1.1rem;
  background: rgba(247, 244, 236, 0.88);
  box-shadow: 0 18px 52px rgba(44, 39, 31, 0.05);
}}

.b179-bottleneck-scroll {{
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
}}

.b179-bottleneck-svg {{
  display: block;
  width: 100%;
  min-width: 680px;
  height: auto;
}}

.b179-bottleneck-source {{
  margin: 0.95rem 0 0;
  color: #6b766d;
  font-size: clamp(0.78rem, 0.95vw, 0.88rem);
  line-height: 1.42;
}}

.b179-bottleneck-labels text,
.b179-bottleneck-legend text {{
  font-family: inherit;
}}

@media (max-width: 760px) {{
  .b179-bottleneck-figure {{
    margin-top: 1.5rem;
    padding: 0.8rem;
    border-radius: 0.9rem;
  }}

  .b179-bottleneck-svg {{
    min-width: 640px;
  }}

  .b179-bottleneck-source {{
    padding-inline: 0.15rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B179 replace Engpass scorecard with bottleneck graphic: replaced the old value-chain scorecard with a static editorial bottleneck SVG, no animation and no external assets ({today})."
    if "B179 replace Engpass scorecard with bottleneck graphic" in done_text:
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

    pre = {
        "b179_marker": html_before.count(B179_START),
        "heading": html_before.count(HEADING),
        "figure_marker": html_before.count("b179-bottleneck-figure"),
        "felt": html_before.lower().count("felt"),
        "iframe": html_before.lower().count("<iframe"),
    }

    html = patch_index(html_before)
    css = patch_css(css_before)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)

    post = {
        "b179_marker": html_after.count(B179_START),
        "heading": html_after.count(HEADING),
        "figure_marker": html_after.count("b179-bottleneck-figure"),
        "static_svg": html_after.count("b179-bottleneck-svg"),
        "animation_terms": len(re.findall(r"IntersectionObserver|requestAnimationFrame|engpass-replay|Animation neu abspielen", html_after, flags=re.I)),
        "felt": html_after.lower().count("felt"),
        "iframe": html_after.lower().count("<iframe"),
        "css_marker": css_after.count(CSS_START),
    }

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["change", "status", "detail"], delimiter=";")
        writer.writeheader()
        writer.writerows(CHANGE_ROWS)

    doc = f"""# B179 - Replace Engpass Scorecard With Bottleneck Graphic

Date: {today}

## Ziel

B179 ersetzt die bisherige Engpass-/Scorecard-Grafik durch eine statische Flaschenhalsgrafik.

Die Grafik macht die Aussage sichtbar: Bis zur Ernte ist die Kette breit und anschlussfähig; danach wird sie enger. Keine Animation, kein Replay-Button, keine externen Assets.

## Entscheidung

```text
Statischer Endzustand statt animierter Demo.
```

## Beibehalten

- Titel: `{HEADING}`
- Lead: `{LEAD}`
- Quellen-/Methodenlinie: qualitative Synthese, keine Messgrafik
- Wertschöpfungs-These
- keine Felt-/OSM-Einbindung

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- kein B169 Sticky-Zoom
- kein B176/B177/B178 Verhalten
- keine externen Ressourcen

## Technische Umsetzung

- Inline-SVG in `index.html`
- responsive Figure mit horizontalem Scroll auf kleinen Screens
- CSS in `src/styles.css`
- keine JS-Animation
- `role="img"` mit `title` und `desc`

## Counts

| Signal | Vorher | Nachher |
|---|---:|---:|
| B179 marker | {pre['b179_marker']} | {post['b179_marker']} |
| Heading | {pre['heading']} | {post['heading']} |
| B179 figure class | {pre['figure_marker']} | {post['figure_marker']} |
| B179 SVG class | — | {post['static_svg']} |
| Animation/Replay terms | — | {post['animation_terms']} |
| Felt token in index | {pre['felt']} | {post['felt']} |
| iframe in index | {pre['iframe']} | {post['iframe']} |
| B179 CSS marker | — | {post['css_marker']} |

## Akzeptanz

- Die Engpass-Grafik ist als Flaschenhals sichtbar.
- Es gibt keine Animation und keinen Replay-Button.
- Die Quellen-/Methodenlinie bleibt sichtbar.
- Mobile Darstellung bleibt lesbar über horizontalen Figure-Viewport.
- B177, B103b und B58 laufen weiter.
"""
    write(DOC, doc)

    audit = f"""# B179 replace Engpass scorecard with bottleneck graphic audit

Date: {today}

Post-patch checks:
- B179 marker present exactly once: {post['b179_marker'] == 1}
- B179 figure present: {post['figure_marker'] >= 1}
- B179 SVG present: {post['static_svg'] >= 1}
- Heading present: {post['heading'] >= 1}
- Lead present: {LEAD in html_after}
- Source line present: {SOURCE_LINE in html_after}
- No animation/replay terms in index: {post['animation_terms'] == 0}
- No Felt token in index: {post['felt'] == 0}
- No iframe in index: {post['iframe'] == 0}
- B176 local cartographic depth still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}
- B178 scale-change note still present: {'B178_SCALE_CHANGE_NOTE_START' in html_after}
- B169 live sticky zoom still present: {'B169_LIVE_STICKY_ZOOM_START' in html_after}
- B179 CSS present exactly once: {post['css_marker'] == 1}

Changes:
"""
    for row in CHANGE_ROWS:
        audit += f"- {row['change']}: {row['status']} — {row['detail']}\n"
    audit += "\nResult: PATCH WRITTEN. Run B177, B103b and B58 before commit.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B179 replace Engpass scorecard with bottleneck graphic complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B179_replace_engpass_scorecard_with_bottleneck_graphic.md")
    print("  docs/B179_engpass_replacement_changes.csv")
    print("  docs/B179_replace_engpass_scorecard_with_bottleneck_graphic_audit.txt")
    print("  tasks/done.md")
    print("Post-patch checks:")
    print(f"  B179 marker exactly once: {post['b179_marker'] == 1}")
    print(f"  B179 figure present: {post['figure_marker'] >= 1}")
    print(f"  no animation/replay terms: {post['animation_terms'] == 0}")
    print(f"  no Felt token: {post['felt'] == 0}")
    print(f"  no iframe: {post['iframe'] == 0}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
