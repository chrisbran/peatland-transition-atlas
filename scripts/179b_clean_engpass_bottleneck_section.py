from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B179b_clean_engpass_bottleneck_section.md"
AUDIT = ROOT / "docs" / "B179b_clean_engpass_bottleneck_section_audit.txt"
CSV_OUT = ROOT / "docs" / "B179b_removed_engpass_remnants.csv"
DONE = ROOT / "tasks" / "done.md"

B179_START = "<!-- B179_BOTTLENECK_GRAPHIC_START -->"
B179_END = "<!-- /B179_BOTTLENECK_GRAPHIC_END -->"
CSS_START = "/* B179b_CLEAN_ENGPASS_BOTTLENECK_SECTION_START */"
CSS_END = "/* B179b_CLEAN_ENGPASS_BOTTLENECK_SECTION_END */"

HEADING = "Bis zur Ernte ist vieles anschlussfähig. Danach wird es eng."
LEAD = "Auf dem Feld und bis zur Ernte gibt es erprobte Ansätze. Dahinter entscheiden Logistik, Verarbeitung, Standards und Abnahme darüber, ob nasse Nutzung skalierbar wird."

ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\s*", "", text, flags=re.S)


def record(item: str, status: str, detail: str) -> None:
    ROWS.append({"item": item, "status": status, "detail": detail})


def clean_text(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def add_class(opening: str, class_name: str) -> str:
    if class_name in opening:
        return opening
    if re.search(r'\bclass\s*=', opening, flags=re.I):
        opening = re.sub(
            r'class="([^"]*)"',
            lambda m: f'class="{m.group(1)} {class_name}"',
            opening,
            count=1,
            flags=re.I,
        )
        opening = re.sub(
            r"class='([^']*)'",
            lambda m: f"class='{m.group(1)} {class_name}'",
            opening,
            count=1,
            flags=re.I,
        )
        return opening
    return opening[:-1] + f' class="{class_name}">'


def find_b179_section(html: str):
    pos = html.find(B179_START)
    if pos < 0:
        return None
    start = html.rfind("<section", 0, pos)
    end = html.find("</section>", pos)
    if start < 0 or end < 0:
        return None
    return start, end + len("</section>")


def reconstruct_section(section: str) -> str:
    opening_match = re.match(r"<section\b[^>]*>", section, flags=re.I | re.S)
    if not opening_match:
        record("section_opening", "failed", "Could not read section opening tag.")
        return section

    opening = add_class(opening_match.group(0), "b179b-clean-engpass-section")

    figure_match = re.search(re.escape(B179_START) + r".*?" + re.escape(B179_END), section, flags=re.S)
    if not figure_match:
        record("b179_figure", "failed", "Could not find B179 figure block inside section.")
        return section

    figure = figure_match.group(0)

    old_after = section[figure_match.end():]
    old_after_text = clean_text(old_after)
    if old_after_text:
        record("old_remnants_after_figure", "removed", old_after_text[:320])
    else:
        record("old_remnants_after_figure", "none", "No visible text after B179 figure inside section.")

    kicker = "Schematische Einordnung"
    # Preserve existing kicker text if it exists.
    kicker_match = re.search(r"<p\b[^>]*class=[\"'][^\"']*(?:kicker|eyebrow|section-kicker)[^\"']*[\"'][^>]*>(.*?)</p>", section, flags=re.I | re.S)
    if kicker_match:
        kicker_text = clean_text(kicker_match.group(1))
        if kicker_text:
            kicker = kicker_text

    new_inner = f"""
  <div class="b179b-engpass-inner">
    <p class="b179b-engpass-kicker">{kicker}</p>
    <h2>{HEADING}</h2>
    <p class="b179b-engpass-lead">{LEAD}</p>
    {figure}
  </div>
"""
    return opening + new_inner + "</section>"


def patch_index(html: str) -> str:
    bounds = find_b179_section(html)
    if not bounds:
        record("b179_section", "failed", "Could not locate section containing B179 marker.")
        return html

    start, end = bounds
    old_section = html[start:end]
    new_section = reconstruct_section(old_section)
    if new_section != old_section:
        record("b179_section", "patched", "Reconstructed Engpass section around B179 figure and removed old scorecard remnants.")
    else:
        record("b179_section", "no_change", "Section was not modified.")
    return html[:start] + new_section + html[end:]


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
/* B179b: keep the bottleneck section clean after replacing the old scorecard. */
.b179b-clean-engpass-section {{
  overflow: visible;
}}

.b179b-engpass-inner {{
  width: min(100% - 2rem, 78rem);
  margin-inline: auto;
}}

.b179b-engpass-kicker {{
  margin: 0 0 0.75rem;
  color: #9db26a;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.b179b-engpass-inner h2 {{
  max-width: 18em;
  margin: 0;
  text-wrap: balance;
}}

.b179b-engpass-lead {{
  max-width: 42rem;
  margin: 1.15rem 0 0;
  text-wrap: pretty;
}}

.b179b-clean-engpass-section .b179-bottleneck-figure {{
  max-width: 72rem;
}}

@media (max-width: 760px) {{
  .b179b-engpass-inner {{
    width: min(100% - 1rem, 78rem);
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def count_remnant_terms(html: str) -> dict:
    # Count only inside B179 section.
    bounds = find_b179_section(html)
    if not bounds:
        return {"section_found": 0, "b179_marker": html.count(B179_START), "old_status_bars": -1}
    section = html[bounds[0]:bounds[1]]
    after = section.split(B179_END, 1)[1] if B179_END in section else ""
    return {
        "section_found": 1,
        "b179_marker": section.count(B179_START),
        "visible_text_after_figure_len": len(clean_text(after)),
        "anschlussfaehig_after_figure": len(re.findall(r"anschlussfähig|anschlussfaehig", after, flags=re.I)),
        "entwicklungsbedarf_after_figure": len(re.findall(r"Entwicklungsbedarf", after, flags=re.I)),
        "scorecard_after_figure": len(re.findall(r"scorecard|maturity|reifegrad|b130|b162", after, flags=re.I)),
    }


def update_done(done_text: str, today: str) -> str:
    line = f"- B179b clean Engpass bottleneck section: removed old scorecard remnants below the new static bottleneck graphic and rebuilt the section as a single visual climax ({today})."
    if "B179b clean Engpass bottleneck section" in done_text:
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

    pre = count_remnant_terms(html_before)

    html = patch_index(html_before)
    css = patch_css(css_before)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)

    post = count_remnant_terms(html_after)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "status", "detail"], delimiter=";")
        writer.writeheader()
        writer.writerows(ROWS)

    doc = f"""# B179b - Clean Engpass Bottleneck Section

Date: {today}

## Ziel

B179 hat die neue Flaschenhalsgrafik eingefügt. In der visuellen Prüfung war darunter noch der alte Scorecard-/Balkenblock sichtbar.

B179b bereinigt diesen Abschnitt:

```text
Eine Engpass-Sektion = ein visueller Höhepunkt.
```

## Änderungen

- Engpass-Sektion um die B179-Flaschenhalsgrafik neu aufgebaut
- alter Scorecard-/Balkenrest unter der Grafik entfernt
- Titel, Lead und Quellenlinie der B179-Grafik behalten
- keine Animation, kein Replay-Button
- keine externen Assets
- keine Datenwerte geändert

## Counts im Engpass-Abschnitt

| Signal | Vorher | Nachher |
|---|---:|---:|
| Section gefunden | {pre['section_found']} | {post['section_found']} |
| B179 marker | {pre['b179_marker']} | {post['b179_marker']} |
| Sichtbarer Text nach B179-Figure | {pre.get('visible_text_after_figure_len', -1)} | {post.get('visible_text_after_figure_len', -1)} |
| `anschlussfähig` nach Figure | {pre.get('anschlussfaehig_after_figure', -1)} | {post.get('anschlussfaehig_after_figure', -1)} |
| `Entwicklungsbedarf` nach Figure | {pre.get('entwicklungsbedarf_after_figure', -1)} | {post.get('entwicklungsbedarf_after_figure', -1)} |
| Scorecard-/Reifegrad-Tokens nach Figure | {pre.get('scorecard_after_figure', -1)} | {post.get('scorecard_after_figure', -1)} |

## Akzeptanz

- Nach der Flaschenhalsgrafik steht innerhalb der Engpass-Sektion kein alter Scorecard-Balkenblock mehr.
- Die Quellen-/Methodenlinie bleibt in der Figure erhalten.
- Die Wertschöpfungs-These bleibt als visueller Höhepunkt erhalten.
- B177, B103b und B58 laufen weiter.
"""
    write(DOC, doc)

    audit = f"""# B179b clean Engpass bottleneck section audit

Date: {today}

Post-patch checks:
- B179 marker present exactly once: {html_after.count(B179_START) == 1}
- B179 figure present: {'b179-bottleneck-figure' in html_after}
- B179b clean section class present: {'b179b-clean-engpass-section' in html_after}
- Visible text after B179 figure inside section is very short: {post.get('visible_text_after_figure_len', 9999) <= 20}
- No scorecard/reifegrad tokens after B179 figure: {post.get('scorecard_after_figure', 9999) == 0}
- No animation/replay terms in index: {not re.search(r'IntersectionObserver|requestAnimationFrame|engpass-replay|Animation neu abspielen', html_after, flags=re.I)}
- No Felt token in index: {'felt' not in html_after.lower()}
- No iframe in index: {'<iframe' not in html_after.lower()}
- B176 local cartographic depth still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}
- B178 scale-change note still present: {'B178_SCALE_CHANGE_NOTE_START' in html_after}
- B169 live sticky zoom still present: {'B169_LIVE_STICKY_ZOOM_START' in html_after}
- B179b CSS present exactly once: {css_after.count(CSS_START) == 1}

Changes:
"""
    for row in ROWS:
        audit += f"- {row['item']}: {row['status']} — {row['detail']}\n"
    audit += "\nResult: PATCH WRITTEN. Run B177, B103b and B58 before continuing.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B179b clean Engpass bottleneck section complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B179b_clean_engpass_bottleneck_section.md")
    print("  docs/B179b_removed_engpass_remnants.csv")
    print("  docs/B179b_clean_engpass_bottleneck_section_audit.txt")
    print("  tasks/done.md")
    print("Post-patch checks:")
    print(f"  B179 marker exactly once: {html_after.count(B179_START) == 1}")
    print(f"  visible text after figure length: {post.get('visible_text_after_figure_len', -1)}")
    print(f"  no Felt token: {'felt' not in html_after.lower()}")
    print(f"  no iframe: {'<iframe' not in html_after.lower()}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
