from pathlib import Path
from datetime import date
import re
import csv
from html import unescape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B181_closing_counterpoint_and_schlussbogen.md"
AUDIT = ROOT / "docs" / "B181_closing_counterpoint_and_schlussbogen_audit.txt"
CSV_OUT = ROOT / "docs" / "B181_closing_counterpoint_changes.csv"
DONE = ROOT / "tasks" / "done.md"

B181_START = "<!-- B181_CLOSING_COUNTERPOINT_START -->"
B181_END = "<!-- /B181_CLOSING_COUNTERPOINT_END -->"
CSS_START = "/* B181_CLOSING_COUNTERPOINT_START */"
CSS_END = "/* B181_CLOSING_COUNTERPOINT_END */"

OLD_CLOSING_HEADING = "Der Hebel verschiebt sich von der Fläche zur Kette"
NEW_HEADING = "Der Engpass ist real — aber nicht überall derselbe"

COUNTERPOINT_SECTION = f"""{B181_START}
<section class="b181-closing-counterpoint" aria-labelledby="b181-closing-counterpoint-title">
  <div class="b181-closing-counterpoint__inner">
    <p class="b181-closing-counterpoint__kicker">Einordnung</p>
    <h2 id="b181-closing-counterpoint-title">{NEW_HEADING}</h2>
    <p class="b181-closing-counterpoint__lead">
      Die Kettenperspektive erklärt, warum nasse Nutzung nicht allein auf der Fläche
      entschieden wird. Sie ist aber kein Argument gegen Wiedervernässung selbst:
      Wo Klimaschutz das primäre Ziel ist, geringe Nutzungsintensität vorliegt oder
      verlässliche Förderung Betriebe absichert, kann Wiedervernässung auch ohne
      Produktmarkt sinnvoll sein.
    </p>
    <p class="b181-closing-counterpoint__close">
      Der Engpass liegt vor allem dort, wo nasse Nutzung skaliert, Produkte abgesetzt
      und Betriebe dauerhaft eingebunden werden sollen. Er ist ein Argument gegen
      naive Skalierung — nicht gegen Moorbodenschutz.
    </p>
  </div>
</section>
{B181_END}"""

ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\s*", "", text, flags=re.S)


def text_only(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    return re.sub(r"\s+", " ", html).strip()


def record(item: str, status: str, detail: str) -> None:
    ROWS.append({"item": item, "status": status, "detail": detail})


def find_section_by_text(html: str, needles: list[str]):
    sections = list(re.finditer(r"<section\b[^>]*>.*?</section>", html, flags=re.I | re.S))
    for needle in needles:
        for m in sections:
            if needle.lower() in text_only(m.group(0)).lower():
                return m.start(), m.end(), needle
    return None


def find_method_or_sources_start(html: str) -> int | None:
    anchors = [
        "Methode in Kürze",
        "Quellen, Methodik und Nutzungsrechte",
        "Datengrundlagen, Rechte und Quellenvermerke",
        "Quellenvermerke",
    ]
    positions = [html.find(a) for a in anchors if html.find(a) >= 0]
    if not positions:
        return None
    pos = min(positions)
    sec_start = html.rfind("<section", 0, pos)
    return sec_start if sec_start >= 0 else pos


def patch_index(html: str) -> str:
    html = strip_block(html, B181_START, B181_END)

    # Preferred: replace the repetitive final consequence section.
    found = find_section_by_text(html, [
        OLD_CLOSING_HEADING,
        "Der Hebel verschiebt sich",
        "Fläche zur Kette",
    ])

    if found:
        start, end, needle = found
        old_text = text_only(html[start:end])
        html = html[:start] + COUNTERPOINT_SECTION + "\n" + html[end:]
        record("closing_section", "replaced", f"Replaced section containing `{needle}`. Old visible text length: {len(old_text)}.")
        return html

    # Fallback: insert before method/sources.
    insert_at = find_method_or_sources_start(html)
    if insert_at is not None:
        html = html[:insert_at] + COUNTERPOINT_SECTION + "\n" + html[insert_at:]
        record("closing_section", "inserted_fallback", "Could not find old consequence section; inserted before method/source section.")
        return html

    record("closing_section", "failed", "Could not find old consequence section or method/source insertion point.")
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* B181: compact closing counterpoint to avoid a one-note conclusion. */
.b181-closing-counterpoint {{
  width: min(100% - 2rem, 76rem);
  margin: clamp(2.5rem, 7vw, 5.5rem) auto;
  padding: clamp(1.35rem, 3vw, 2.2rem);
  border: 1px solid rgba(28, 42, 34, 0.12);
  border-radius: 1.2rem;
  background: rgba(250, 248, 241, 0.72);
  box-shadow: 0 18px 52px rgba(44, 39, 31, 0.055);
}}

.b181-closing-counterpoint__inner {{
  max-width: 52rem;
}}

.b181-closing-counterpoint__kicker {{
  margin: 0 0 0.65rem;
  color: #6b7f51;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.b181-closing-counterpoint h2 {{
  max-width: 14em;
  margin: 0;
  color: #1c2a22;
  font-size: clamp(1.85rem, 4.2vw, 3.4rem);
  line-height: 0.98;
  text-wrap: balance;
}}

.b181-closing-counterpoint__lead {{
  margin: 1.15rem 0 0;
  color: #334238;
  font-size: clamp(1.02rem, 1.35vw, 1.18rem);
  line-height: 1.5;
  text-wrap: pretty;
}}

.b181-closing-counterpoint__close {{
  margin: 1rem 0 0;
  padding-top: 1rem;
  border-top: 1px solid rgba(28, 42, 34, 0.12);
  color: #1c2a22;
  font-weight: 760;
  line-height: 1.45;
  text-wrap: pretty;
}}

@media (max-width: 760px) {{
  .b181-closing-counterpoint {{
    width: min(100% - 1rem, 76rem);
    margin-block: 2rem;
    padding: 1.1rem;
    border-radius: 0.95rem;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def count_signals(html: str) -> dict:
    txt = text_only(html)
    return {
        "old_heading": txt.count(OLD_CLOSING_HEADING),
        "new_heading": txt.count(NEW_HEADING),
        "gegen_argument": len(re.findall(r"kein\s+Argument\s+gegen\s+Wiedervernässung|nicht\s+gegen\s+Moorbodenschutz|naive\s+Skalierung", txt, flags=re.I)),
        "flaeche_kette": len(re.findall(r"Fläche\s+zur\s+Kette|Fläche\s+→\s*Kette|Fläche\s+->\s*Kette", txt, flags=re.I)),
        "felt": html.lower().count("felt"),
        "iframe": html.lower().count("<iframe"),
    }


def update_done(done_text: str, today: str) -> str:
    line = f"- B181 closing counterpoint and Schlussbogen: replaced the repeated final Fläche-zu-Kette conclusion with a compact counterpoint that limits the chain thesis without weakening the Moorbodenschutz argument ({today})."
    if "B181 closing counterpoint and Schlussbogen" in done_text:
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

    pre = count_signals(html_before)

    html = patch_index(html_before)
    css = patch_css(css_before)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)

    post = count_signals(html_after)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["item", "status", "detail"], delimiter=";")
        writer.writeheader()
        writer.writerows(ROWS)

    doc = f"""# B181 - Closing Counterpoint and Schlussbogen

Date: {today}

## Ziel

B181 strafft den Schlussbogen und ergänzt eine begrenzende Gegenposition.

Die Seite soll nicht so enden, als würde die Wertschöpfungskette jede Wiedervernässungsfrage erklären. Die Kettenperspektive bleibt zentral, wird aber präzisiert.

## Neue Schlusssektion

```text
{NEW_HEADING}
```

Kerntext:

```text
Die Kettenperspektive erklärt, warum nasse Nutzung nicht allein auf der Fläche
entschieden wird. Sie ist aber kein Argument gegen Wiedervernässung selbst:
Wo Klimaschutz das primäre Ziel ist, geringe Nutzungsintensität vorliegt oder
verlässliche Förderung Betriebe absichert, kann Wiedervernässung auch ohne
Produktmarkt sinnvoll sein.
```

Schlusszeile:

```text
Der Engpass liegt vor allem dort, wo nasse Nutzung skaliert, Produkte abgesetzt
und Betriebe dauerhaft eingebunden werden sollen. Er ist ein Argument gegen
naive Skalierung — nicht gegen Moorbodenschutz.
```

## Wirkung

- Der Schluss wiederholt nicht nur `Fläche → Kette`.
- Die zentrale These wird intellektuell ehrlicher.
- Die Gegenposition schwächt den Demonstrator nicht, sondern grenzt seinen Aussagebereich sauber ein.

## Nicht geändert

- keine Datenwerte
- keine Kartenassets
- keine Quellenstruktur
- keine B176/B177/B178/B179-Inhalte
- keine externen Ressourcen

## Counts

| Signal | Vorher | Nachher |
|---|---:|---:|
| Alte Schlussüberschrift | {pre['old_heading']} | {post['old_heading']} |
| Neue Schlussüberschrift | {pre['new_heading']} | {post['new_heading']} |
| Gegenpositions-Signale | {pre['gegen_argument']} | {post['gegen_argument']} |
| Fläche-zur-Kette-Formel | {pre['flaeche_kette']} | {post['flaeche_kette']} |
| Felt token | {pre['felt']} | {post['felt']} |
| iframe | {pre['iframe']} | {post['iframe']} |
"""
    write(DOC, doc)

    audit = f"""# B181 closing counterpoint and Schlussbogen audit

Date: {today}

Post-patch checks:
- B181 marker present exactly once: {html_after.count(B181_START) == 1}
- New closing heading present: {NEW_HEADING in html_after}
- Old closing heading absent: {OLD_CLOSING_HEADING not in html_after}
- Counterpoint text present: {'kein Argument gegen Wiedervernässung selbst' in html_after}
- Naive scaling line present: {'naive Skalierung' in html_after and 'nicht gegen Moorbodenschutz' in html_after}
- B176 local cartographic depth still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}
- B178 area caveat still present: {'B178_AREA_CAVEAT_START' in html_after}
- B179 bottleneck graphic still present: {'B179_BOTTLENECK_GRAPHIC_START' in html_after}
- No Felt token in index: {'felt' not in html_after.lower()}
- No iframe in index: {'<iframe' not in html_after.lower()}
- B181 CSS present exactly once: {css_after.count(CSS_START) == 1}

Changes:
"""
    for row in ROWS:
        audit += f"- {row['item']}: {row['status']} — {row['detail']}\n"

    audit += "\nResult: PATCH WRITTEN. Run B177, B103b and B58 before final QA.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B181 closing counterpoint and Schlussbogen complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B181_closing_counterpoint_and_schlussbogen.md")
    print("  docs/B181_closing_counterpoint_changes.csv")
    print("  docs/B181_closing_counterpoint_and_schlussbogen_audit.txt")
    print("  tasks/done.md")
    print("Post-patch checks:")
    print(f"  B181 marker exactly once: {html_after.count(B181_START) == 1}")
    print(f"  old heading absent: {OLD_CLOSING_HEADING not in html_after}")
    print(f"  no Felt token: {'felt' not in html_after.lower()}")
    print(f"  no iframe: {'<iframe' not in html_after.lower()}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
