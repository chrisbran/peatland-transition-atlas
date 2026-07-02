from pathlib import Path
from datetime import date
import re
import csv
from html import unescape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B180b_restore_b176_and_tighten_disclaimer_diet.md"
AUDIT = ROOT / "docs" / "B180b_restore_b176_and_tighten_disclaimer_diet_audit.txt"
CSV_OUT = ROOT / "docs" / "B180b_disclaimer_and_marker_changes.csv"
DONE = ROOT / "tasks" / "done.md"

B176_START = "<!-- B176_LOCAL_CARTOGRAPHIC_DEPTH_START -->"
B176_END = "<!-- /B176_LOCAL_CARTOGRAPHIC_DEPTH_END -->"
B178_AREA_START = "<!-- B178_AREA_CAVEAT_START -->"
B179_START = "<!-- B179_BOTTLENECK_GRAPHIC_START -->"
B180B_START = "<!-- B180B_RESTORED_LOCAL_CARTOGRAPHIC_DEPTH_START -->"
B180B_END = "<!-- /B180B_RESTORED_LOCAL_CARTOGRAPHIC_DEPTH_END -->"

B176_SECTION = f"""{B176_START}
{B180B_START}
<section class="b176-local-cartographic-depth b180b-restored-local-cartographic-depth" aria-labelledby="b180b-local-cartographic-depth-title">
  <div class="b176-local-cartographic-depth__inner">
    <p class="b176-local-cartographic-depth__kicker">Kartografische Vertiefung</p>
    <h2 id="b180b-local-cartographic-depth-title">Die Detailkarte bleibt lokal</h2>
    <p class="b176-local-cartographic-depth__lead">
      Die Detailkarte bleibt bewusst eine lokale, redaktionelle Grafik: Sie zeigt
      die Schnittmenge aus heutiger Nutzung und Moor-/Feuchtbodenkontext, ohne beim
      Seitenaufruf einen externen Kartendienst zu laden.
    </p>
    <p class="b176-local-cartographic-depth__source">
      Eigene GIS-Aufbereitung aus FIONA 2024, BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
      lokale Darstellung als redaktionelle Kartengrafik. Methodische Grenzen siehe <a href="#methode">Methode in Kürze</a>.
    </p>
  </div>
</section>
{B180B_END}
{B176_END}"""

CSS_START = "/* B180b_RESTORE_B176_AND_TIGHTEN_DISCLAIMER_DIET_START */"
CSS_END = "/* B180b_RESTORE_B176_AND_TIGHTEN_DISCLAIMER_DIET_END */"

TERM_PATTERNS = {
    "keine_eignungskarte": r"keine\s+Eignungskarte",
    "keine_priorisierung": r"keine\s+Priorisierung",
    "keine_hydrologie": r"keine\s+hydrologische\s+Modellierung",
    "keine_betrieb": r"keine\s+betriebliche\s+Betroffenheitsanalyse",
    "standortpruefung": r"Standortprüfung",
}

ROWS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def text_only(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    return re.sub(r"\s+", " ", html).strip()


def count_terms(html: str) -> dict:
    txt = text_only(html)
    return {key: len(re.findall(pattern, txt, flags=re.I)) for key, pattern in TERM_PATTERNS.items()}


def strip_block(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\s*", "", text, flags=re.S)


def record(kind: str, status: str, detail: str) -> None:
    ROWS.append({"kind": kind, "status": status, "detail": detail})


def find_area_balance_section_start(html: str) -> int | None:
    anchors = [
        B178_AREA_START,
        "Vier von fünf Hektar sind Grünland",
        "~19.900 ha landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext",
        "19.900 ha landwirtschaftliche Nutzung im Moor-/Feuchtbodenkontext",
    ]
    positions = [html.find(a) for a in anchors if html.find(a) >= 0]
    if not positions:
        return None
    pos = min(positions)
    start = html.rfind("<section", 0, pos)
    return start if start >= 0 else pos


def restore_b176_marker_and_note(html: str) -> str:
    # Remove any broken/restored duplicate first.
    html = strip_block(html, B180B_START, B180B_END)

    if B176_START in html and B176_END in html:
        record("b176_marker", "already_present", "B176 marker exists; no restored section inserted.")
        return html

    insert_at = find_area_balance_section_start(html)
    if insert_at is None:
        record("b176_marker", "failed", "Could not find area-balance insertion point.")
        return html

    html = html[:insert_at] + B176_SECTION + "\n" + html[insert_at:]
    record("b176_marker", "restored", "Inserted compact local cartographic-depth section immediately before area balance.")
    return html


def get_protected_ranges(html: str):
    ranges = []

    for m in re.finditer(r"<section\b[^>]*>.*?</section>", html, flags=re.I | re.S):
        block = m.group(0)
        txt = text_only(block).lower()
        opening = re.match(r"<section\b[^>]*>", block, flags=re.I | re.S).group(0).lower()

        if ("fachlicher demonstrator" in txt and "keine eignungskarte" in txt):
            ranges.append((m.start(), m.end(), "scope"))
        elif 'id="methode"' in opening or "id='methode'" in opening or "methode in kürze" in txt:
            ranges.append((m.start(), m.end(), "method"))
        elif "quellen, methodik" in txt or "datengrundlagen" in txt or "quellenvermerke" in txt:
            ranges.append((m.start(), m.end(), "sources"))

    # Keep B178 direct caveat unchanged.
    start = html.find(B178_AREA_START)
    end = html.find("<!-- /B178_AREA_CAVEAT_END -->")
    if start >= 0 and end >= 0:
        ranges.append((start, end + len("<!-- /B178_AREA_CAVEAT_END -->"), "b178_area_caveat"))

    return ranges


def in_range(pos: int, ranges) -> bool:
    return any(a <= pos < b for a, b, _ in ranges)


def replace_outside_protected(html: str, pattern: str, replacement: str, label: str, max_keep: int = 2) -> str:
    ranges = get_protected_ranges(html)
    matches = list(re.finditer(pattern, html, flags=re.I | re.S))

    # Count visible occurrences and keep protected plus first unprotected up to max_keep total.
    kept = 0
    patches = []
    for m in matches:
        if in_range(m.start(), ranges):
            kept += 1
            continue
        if kept < max_keep:
            kept += 1
            continue
        patches.append(m)

    if not patches:
        record(label, "no_extra_occurrences", f"No unprotected occurrences beyond keep limit {max_keep}.")
        return html

    for m in reversed(patches):
        snippet = text_only(m.group(0))[:220]
        html = html[:m.start()] + replacement + html[m.end():]
        record(label, "replaced", snippet)

    return html


def tighten_disclaimer_terms(html: str) -> str:
    # First collapse exact long clusters outside protected ranges.
    replacements = [
        (
            r"keine\s+Eignungskarte,\s*keine\s+Priorisierung,\s*keine\s+hydrologische\s+Modellierung\s+und\s+keine\s+betriebliche\s+Betroffenheitsanalyse",
            "Prüfkulisse, keine Entscheidung",
            "long_cluster_und",
        ),
        (
            r"keine\s+Eignungskarte,\s*keine\s+Priorisierung,\s*keine\s+hydrologische\s+Modellierung,\s*keine\s+betriebliche\s+Betroffenheitsanalyse",
            "Prüfkulisse, keine Entscheidung",
            "long_cluster_commas",
        ),
        (
            r"keine\s+Eignungskarte,\s*keine\s+Priorisierung",
            "keine Entscheidung",
            "short_eignung_priorisierung_cluster",
        ),
    ]

    for pattern, replacement, label in replacements:
        html = replace_outside_protected(html, pattern, replacement, label, max_keep=2)

    # Then reduce individual formulaic terms outside protected ranges to less repetitive language if still >2.
    individual = [
        (r"keine\s+Eignungskarte", "kein Entscheidungsinstrument", "term_keine_eignungskarte"),
        (r"keine\s+Priorisierung", "keine Rangfolge", "term_keine_priorisierung"),
        (r"keine\s+hydrologische\s+Modellierung", "keine Detailmodellierung", "term_keine_hydrologie"),
        (r"keine\s+betriebliche\s+Betroffenheitsanalyse", "keine Betriebsanalyse", "term_keine_betrieb"),
        (r"Standortprüfung", "Vor-Ort-Prüfung", "term_standortpruefung"),
    ]

    for pattern, replacement, label in individual:
        html = replace_outside_protected(html, pattern, replacement, label, max_keep=2)

    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f"""
{CSS_START}
/* B180b: compact restored local-cartography note after Felt removal. */
.b180b-restored-local-cartographic-depth {{
  margin-top: clamp(1.5rem, 4vw, 2.75rem);
  margin-bottom: clamp(1.5rem, 4vw, 2.75rem);
}}

.b180b-restored-local-cartographic-depth .b176-local-cartographic-depth__lead {{
  max-width: 50rem;
}}

.b180b-restored-local-cartographic-depth .b176-local-cartographic-depth__source {{
  max-width: 54rem;
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B180b restore B176 marker and tighten disclaimer diet: restored the local-cartography note required by the external-request audit and reduced formulaic disclaimer repetitions outside protected scope/method blocks ({today})."
    if "B180b restore B176 marker and tighten disclaimer diet" in done_text:
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
    pre = count_terms(html_before)

    html = restore_b176_marker_and_note(html_before)
    html = tighten_disclaimer_terms(html)

    css = patch_css(css_before)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)
    post = count_terms(html_after)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["kind", "status", "detail"], delimiter=";")
        writer.writeheader()
        writer.writerows(ROWS)

    doc = f"""# B180b - Restore B176 Marker and Tighten Disclaimer Diet

Date: {today}

## Ausgangspunkt

Nach B180 war die Seite technisch sauber, aber B177 fiel noch durch, weil der B176-Marker für die lokale Kartografie-Fassade nicht mehr vorhanden war. Außerdem hatte B180 die Disclaimer-Dichte nur schwach reduziert.

B180b korrigiert beides.

## Änderungen

- kompakter B176-Abschnitt `Kartografische Vertiefung / Die Detailkarte bleibt lokal` vor der Flächenbilanz wiederhergestellt
- B176-Marker für B177 wiederhergestellt
- formelhafte Disclaimer-Wiederholungen außerhalb von Scope, Methode, Quellen und B178-Zahlencaveat reduziert
- B178-19.900-ha-Vorbehalt bleibt unverändert
- B179/B179b-Flaschenhalsgrafik bleibt unverändert
- keine Datenwerte, Kartenassets oder Skripte geändert

## Term-Counts im sichtbaren Text

| Signal | Vorher | Nachher |
|---|---:|---:|
| keine Eignungskarte | {pre['keine_eignungskarte']} | {post['keine_eignungskarte']} |
| keine Priorisierung | {pre['keine_priorisierung']} | {post['keine_priorisierung']} |
| keine hydrologische Modellierung | {pre['keine_hydrologie']} | {post['keine_hydrologie']} |
| keine betriebliche Betroffenheitsanalyse | {pre['keine_betrieb']} | {post['keine_betrieb']} |
| Standortprüfung | {pre['standortpruefung']} | {post['standortpruefung']} |

## Akzeptanz

- B176 marker ist wieder vorhanden.
- Keine Felt-/OpenStreetMap-/iframe-Tokens sind wieder eingeführt.
- Disclaimer-Dichte sinkt außerhalb der geschützten Absicherungsstellen.
- B177, B103b und B58 laufen weiter.
"""
    write(DOC, doc)

    audit = f"""# B180b restore B176 marker and tighten disclaimer diet audit

Date: {today}

Post-patch checks:
- B176 marker present: {B176_START in html_after and B176_END in html_after}
- B180b restored local cartographic depth present: {B180B_START in html_after and B180B_END in html_after}
- B176 local text present: {'Die Detailkarte bleibt bewusst eine lokale' in html_after}
- B178 area caveat still present: {B178_AREA_START in html_after}
- B179 bottleneck graphic still present: {B179_START in html_after}
- Scope box still present: {'Fachlicher Demonstrator' in html_after and 'keine Eignungskarte' in html_after}
- Method section still present: {'Methode in Kürze' in html_after}
- No Felt token in index: {'felt' not in html_after.lower()}
- No OpenStreetMap token in index: {'openstreetmap' not in html_after.lower()}
- No iframe in index: {'<iframe' not in html_after.lower()}
- CSS marker present exactly once: {css_after.count(CSS_START) == 1}

Counts:
"""
    for key in pre:
        audit += f"- {key}: {pre[key]} -> {post[key]}\n"

    audit += "\nChanges:\n"
    for row in ROWS:
        audit += f"- {row['kind']}: {row['status']} — {row['detail']}\n"

    audit += "\nResult: PATCH WRITTEN. Rerun B177, B103b and B58.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B180b restore B176 marker and tighten disclaimer diet complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B180b_restore_b176_and_tighten_disclaimer_diet.md")
    print("  docs/B180b_disclaimer_and_marker_changes.csv")
    print("  docs/B180b_restore_b176_and_tighten_disclaimer_diet_audit.txt")
    print("  tasks/done.md")
    print("Post-patch checks:")
    print(f"  B176 marker present: {B176_START in html_after and B176_END in html_after}")
    print(f"  no Felt token: {'felt' not in html_after.lower()}")
    print(f"  no OpenStreetMap token: {'openstreetmap' not in html_after.lower()}")
    print(f"  no iframe: {'<iframe' not in html_after.lower()}")
    print("Counts:")
    for key in pre:
        print(f"  {key}: {pre[key]} -> {post[key]}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
