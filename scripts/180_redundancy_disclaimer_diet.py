from pathlib import Path
from datetime import date
import re
import csv
from html import unescape

ROOT = Path(".")
INDEX = ROOT / "index.html"

DOC = ROOT / "docs" / "B180_redundancy_disclaimer_diet.md"
AUDIT = ROOT / "docs" / "B180_redundancy_disclaimer_diet_audit.txt"
CSV_OUT = ROOT / "docs" / "B180_removed_redundant_disclaimers.csv"
DONE = ROOT / "tasks" / "done.md"

B178_AREA_START = "<!-- B178_AREA_CAVEAT_START -->"
B178_AREA_END = "<!-- /B178_AREA_CAVEAT_END -->"

DISCLAIMER_PATTERNS = {
    "keine_eignungskarte": r"keine\s+Eignungskarte",
    "keine_priorisierung": r"keine\s+Priorisierung",
    "keine_hydrologie": r"keine\s+hydrologische\s+Modellierung",
    "keine_betrieb": r"keine\s+betriebliche\s+Betroffenheitsanalyse",
    "keine_flaecheneignung": r"keine\s+Flächeneignung",
    "standortpruefung": r"Standortprüfung",
    "entscheidungsreif": r"entscheidungsreif|entscheidungsreife",
}

REMOVAL_ROWS = []


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
    return {name: len(re.findall(pattern, txt, flags=re.I)) for name, pattern in DISCLAIMER_PATTERNS.items()}


def find_section_ranges(html: str) -> list[tuple[int, int, str]]:
    ranges = []

    for m in re.finditer(r"<section\b[^>]*>.*?</section>", html, flags=re.I | re.S):
        block = m.group(0)
        low = block.lower()
        block_text = text_only(block).lower()
        opening = re.match(r"<section\b[^>]*>", block, flags=re.I | re.S).group(0).lower()

        protect = None
        if "fachlicher demonstrator" in block_text and "keine eignungskarte" in block_text:
            protect = "scope_box"
        elif 'id="methode"' in opening or "id='methode'" in opening or "methode in kürze" in block_text:
            protect = "method_section"
        elif "quellen, methodik" in block_text or "datengrundlagen" in block_text or "quellenvermerke" in block_text:
            protect = "sources_section"

        if protect:
            ranges.append((m.start(), m.end(), protect))

    # Explicitly protect the new B178 inline caveat.
    start = html.find(B178_AREA_START)
    end = html.find(B178_AREA_END)
    if start >= 0 and end >= 0:
        ranges.append((start, end + len(B178_AREA_END), "b178_inline_area_caveat"))

    return ranges


def overlaps_protected(start: int, end: int, ranges: list[tuple[int, int, str]]) -> str | None:
    for a, b, label in ranges:
        if start < b and end > a:
            return label
    return None


def should_remove_block(block: str) -> tuple[bool, str]:
    txt = text_only(block)
    low = txt.lower()
    if not txt:
        return False, "empty"

    # Protect B178 caveat wherever it appears.
    if "b178_area_caveat_start" in block.lower() or "orientierungsgröße, keine flächeneignung" in low:
        return False, "b178_area_caveat"

    has_eignung = bool(re.search(r"keine\s+eignungskarte", low, flags=re.I))
    has_prior = bool(re.search(r"keine\s+priorisierung", low, flags=re.I))
    has_hydro = bool(re.search(r"keine\s+hydrologische\s+modellierung", low, flags=re.I))
    has_betrieb = bool(re.search(r"keine\s+betriebliche\s+betroffenheitsanalyse", low, flags=re.I))
    has_standort = "standortprüfung" in low
    has_decision = "entscheidungsinstrument" in low or "entscheidungsreif" in low

    # Long all-in disclaimer paragraphs outside scope/method should go.
    if has_eignung and (has_prior or has_hydro or has_betrieb or has_decision):
        return True, "long_disclaimer_cluster"

    # Exact generic caveat lines repeated under maps/cards.
    if has_hydro or has_betrieb:
        return True, "technical_scope_caveat"

    if has_standort and ("entscheidungen entstehen" in low or "entscheidungen brauchen" in low) and len(txt) <= 260:
        return True, "generic_standortpruefung_caveat"

    if has_eignung and len(txt) <= 260 and ("methode" in low or "prüfung" in low or "priorisierung" in low):
        return True, "short_eignungskarte_caveat"

    return False, "keep"


def remove_redundant_blocks(html: str) -> str:
    protected = find_section_ranges(html)
    block_re = re.compile(
        r"<(?P<tag>p|li|small|figcaption|aside)\b[^>]*>.*?</(?P=tag)>",
        flags=re.I | re.S,
    )

    matches = list(block_re.finditer(html))
    remove_ranges = []

    for m in matches:
        protected_label = overlaps_protected(m.start(), m.end(), protected)
        if protected_label:
            continue

        block = m.group(0)
        remove, reason = should_remove_block(block)
        if remove:
            remove_ranges.append((m.start(), m.end(), reason, text_only(block)[:420]))

    if not remove_ranges:
        return html

    # Remove from end to start.
    patched = html
    for start, end, reason, snippet in reversed(remove_ranges):
        REMOVAL_ROWS.append({
            "reason": reason,
            "snippet": snippet,
            "start": start,
            "end": end,
        })
        patched = patched[:start] + "" + patched[end:]

    return patched


def compress_duplicate_sentences(html: str) -> str:
    # Remove a small set of exact repeated defensive snippets outside protected blocks.
    protected = find_section_ranges(html)
    snippets = [
        (
            "method_limits_see_method",
            r"\s*Methodische\s+Grenzen\s+siehe\s+<a\s+href=[\"']#methode[\"']>Methode\s+in\s+Kürze</a>\.?",
        ),
        (
            "plain_method_limits_see_method",
            r"\s*Methodische\s+Grenzen\s+siehe\s+Methode\s+in\s+Kürze\.?",
        ),
    ]

    for label, pattern in snippets:
        matches = list(re.finditer(pattern, html, flags=re.I | re.S))
        # Keep the first two occurrences; remove the rest outside protected ranges.
        kept = 0
        for m in reversed(matches):
            protected_label = overlaps_protected(m.start(), m.end(), protected)
            if protected_label:
                kept += 1
                continue
            if kept < 2:
                kept += 1
                continue
            REMOVAL_ROWS.append({
                "reason": label,
                "snippet": text_only(m.group(0))[:260],
                "start": m.start(),
                "end": m.end(),
            })
            html = html[:m.start()] + "" + html[m.end():]

    return html


def update_done(done_text: str, today: str) -> str:
    line = f"- B180 redundancy/disclaimer diet: reduced repeated defensive caveats outside the scope and method sections while keeping the main scope box, B178 area caveat and method section intact ({today})."
    if "B180 redundancy/disclaimer diet" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html_before = read(INDEX)
    pre_counts = count_terms(html_before)

    html = remove_redundant_blocks(html_before)
    html = compress_duplicate_sentences(html)

    write(INDEX, html)

    html_after = read(INDEX)
    post_counts = count_terms(html_after)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["reason", "snippet", "start", "end"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(REMOVAL_ROWS)

    doc = f"""# B180 - Redundancy / Disclaimer Diet

Date: {today}

## Ziel

B180 reduziert defensive Wiederholungen, ohne die fachliche Absicherung zu entfernen.

Die Seite soll weiterhin klar sagen:

```text
Fachlicher Demonstrator, keine Eignungskarte.
```

Aber dieser Hinweis soll nicht unter jeder Karte und jeder Bilanz erneut als vollständiger Disclaimer erscheinen.

## Beibehalten

- Scope-Box oben
- Methodenteil / Methode in Kürze
- B178 inline Vorbehalt an der 19.900-ha-Zahl
- Quellen-/Methodenbereich
- B176 Entfernung von Felt/OSM
- B179/B179b Flaschenhalsgrafik

## Entfernt oder komprimiert

- lange Disclaimer-Cluster außerhalb von Scope und Methode
- wiederholte technische Caveats wie `keine hydrologische Modellierung`
- kurze generische Standortprüfungs-Hinweise, wenn sie nicht an die neue 19.900-ha-Zahl gekoppelt waren
- überzählige Wiederholungen von `Methodische Grenzen siehe Methode in Kürze`

## Term-Counts im sichtbaren Text

| Signal | Vorher | Nachher |
|---|---:|---:|
| keine Eignungskarte | {pre_counts['keine_eignungskarte']} | {post_counts['keine_eignungskarte']} |
| keine Priorisierung | {pre_counts['keine_priorisierung']} | {post_counts['keine_priorisierung']} |
| keine hydrologische Modellierung | {pre_counts['keine_hydrologie']} | {post_counts['keine_hydrologie']} |
| keine betriebliche Betroffenheitsanalyse | {pre_counts['keine_betrieb']} | {post_counts['keine_betrieb']} |
| keine Flächeneignung | {pre_counts['keine_flaecheneignung']} | {post_counts['keine_flaecheneignung']} |
| Standortprüfung | {pre_counts['standortpruefung']} | {post_counts['standortpruefung']} |
| entscheidungsreif | {pre_counts['entscheidungsreif']} | {post_counts['entscheidungsreif']} |

## Entfernte Blöcke

Details: `docs/B180_removed_redundant_disclaimers.csv`

## Akzeptanz

- Scope und Methodenteil bleiben erhalten.
- Der B178-Vorbehalt direkt an der `~19.900 ha`-Zahl bleibt erhalten.
- Die Seite wirkt weniger defensiv.
- B177, B103b und B58 laufen weiter.
"""
    write(DOC, doc)

    audit = f"""# B180 redundancy / disclaimer diet audit

Date: {today}

Post-patch checks:
- Removed block count: {len(REMOVAL_ROWS)}
- Scope box still present: {'Fachlicher Demonstrator' in html_after and 'keine Eignungskarte' in html_after}
- Method section still present: {'Methode in Kürze' in html_after}
- B178 area caveat still present: {'B178_AREA_CAVEAT_START' in html_after}
- B179 bottleneck graphic still present: {'B179_BOTTLENECK_GRAPHIC_START' in html_after}
- B176 local cartographic depth still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}
- No Felt token in index: {'felt' not in html_after.lower()}
- No iframe in index: {'<iframe' not in html_after.lower()}
- B169 live sticky zoom still present: {'B169_LIVE_STICKY_ZOOM_START' in html_after}

Counts:
"""
    for key in pre_counts:
        audit += f"- {key}: {pre_counts[key]} -> {post_counts[key]}\n"

    audit += "\nResult: PATCH WRITTEN. Run B177, B103b and B58 before continuing.\n"
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B180 redundancy / disclaimer diet complete.")
    print("Changed: index.html")
    print("Created/updated:")
    print("  docs/B180_redundancy_disclaimer_diet.md")
    print("  docs/B180_removed_redundant_disclaimers.csv")
    print("  docs/B180_redundancy_disclaimer_diet_audit.txt")
    print("  tasks/done.md")
    print(f"Removed blocks: {len(REMOVAL_ROWS)}")
    print("Counts:")
    for key in pre_counts:
        print(f"  {key}: {pre_counts[key]} -> {post_counts[key]}")
    print("Next: run B177, B103b and B58.")


if __name__ == "__main__":
    main()
