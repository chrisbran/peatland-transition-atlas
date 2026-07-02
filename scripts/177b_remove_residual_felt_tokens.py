from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

DOC = ROOT / "docs" / "B177b_remove_residual_felt_tokens.md"
AUDIT = ROOT / "docs" / "B177b_remove_residual_felt_tokens_audit.txt"
CSV_OUT = ROOT / "docs" / "B177b_removed_residual_felt_tokens.csv"
DONE = ROOT / "tasks" / "done.md"

HTML_PATTERNS = [
    (
        "html_felt_marker_block",
        re.compile(r"<!--\s*B\d+[^>]*FELT[^>]*START\s*-->.*?<!--\s*/\s*B\d+[^>]*FELT[^>]*END\s*-->\s*", re.I | re.S),
        "Removed old HTML Felt marker block."
    ),
    (
        "html_b150_felt_source_register_div",
        re.compile(r"<div\b[^>]*class=[\"'][^\"']*b150-felt-source-register[^\"']*[\"'][^>]*>.*?</div>\s*", re.I | re.S),
        "Removed old B150 Felt source-register div."
    ),
    (
        "html_felt_anchor",
        re.compile(r"<a\b[^>]*href=[\"'][^\"']*felt[^\"']*[\"'][^>]*>.*?</a>\s*", re.I | re.S),
        "Removed residual Felt anchor."
    ),
    (
        "html_felt_iframe",
        re.compile(r"<iframe\b[^>]*(?:felt|openstreetmap|osm)[^>]*>.*?</iframe>\s*", re.I | re.S),
        "Removed residual Felt/OSM iframe."
    ),
]

CSS_PATTERNS = [
    (
        "css_felt_marker_block",
        re.compile(r"/\*\s*B\d+[^*]*FELT[^*]*START\s*\*/.*?/\*\s*/?\s*B\d+[^*]*FELT[^*]*END\s*\*/\s*", re.I | re.S),
        "Removed old CSS Felt marker block."
    ),
    (
        "css_b149_felt_rules",
        re.compile(r"\.b149-felt-[^{]+{[^}]*}\s*", re.I | re.S),
        "Removed residual .b149-felt-* CSS rule."
    ),
    (
        "css_b150_felt_rules",
        re.compile(r"\.b150-felt-[^{]+{[^}]*}\s*", re.I | re.S),
        "Removed residual .b150-felt-* CSS rule."
    ),
]

TOKEN_PATTERNS = {
    "felt": re.compile(r"\bfelt\b|felt\.com", re.I),
    "openstreetmap": re.compile(r"OpenStreetMap|openstreetmap|osm\.org|tile\.openstreetmap", re.I),
    "iframe": re.compile(r"<iframe\b", re.I),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def count_tokens(text: str) -> dict:
    return {name: len(pattern.findall(text)) for name, pattern in TOKEN_PATTERNS.items()}


def apply_patterns(text: str, patterns: list[tuple[str, re.Pattern, str]], target: str, rows: list[dict]) -> str:
    for key, pattern, note in patterns:
        def repl(m: re.Match) -> str:
            snippet = re.sub(r"\s+", " ", m.group(0)).strip()[:260]
            rows.append({
                "target": target,
                "pattern": key,
                "status": "removed",
                "note": note,
                "snippet": snippet,
            })
            return ""
        text, n = pattern.subn(repl, text)
        if n == 0:
            rows.append({
                "target": target,
                "pattern": key,
                "status": "not_found",
                "note": note,
                "snippet": "",
            })
    return text


def remove_felt_comments(text: str, target: str, rows: list[dict]) -> str:
    # Last-resort cleanup for comments that only carry old patch labels.
    patterns = [
        re.compile(r"<!--[^>]*(?:FELT|felt)[^>]*-->\s*", re.I),
        re.compile(r"/\*[^*]*(?:FELT|felt)[^*]*\*/\s*", re.I),
    ]
    for pattern in patterns:
        def repl(m: re.Match) -> str:
            rows.append({
                "target": target,
                "pattern": "felt_comment",
                "status": "removed",
                "note": "Removed residual Felt-only comment/marker.",
                "snippet": re.sub(r"\s+", " ", m.group(0)).strip()[:260],
            })
            return ""
        text = pattern.sub(repl, text)
    return text


def update_done(done_text: str, today: str) -> str:
    line = f"- B177b remove residual Felt tokens: removed leftover Felt source-register/CSS tokens after the public iframe removal so the external-request audit can pass cleanly ({today})."
    if "B177b remove residual Felt tokens" in done_text:
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

    rows = []

    html = apply_patterns(html_before, HTML_PATTERNS, "index.html", rows)
    html = remove_felt_comments(html, "index.html", rows)

    css = apply_patterns(css_before, CSS_PATTERNS, "src/styles.css", rows)
    css = remove_felt_comments(css, "src/styles.css", rows)

    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)

    before_html_counts = count_tokens(html_before)
    after_html_counts = count_tokens(html_after)
    before_css_counts = count_tokens(css_before)
    after_css_counts = count_tokens(css_after)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["target", "pattern", "status", "note", "snippet"], delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    doc = f"""# B177b - Remove Residual Felt Tokens

Date: {today}

## Ziel

B176 entfernte die öffentliche Felt/OpenStreetMap-Einbindung. B177 zeigte danach bereits:

```text
Active loaded external resources: 0
iframe in index: False
External map/tile resource references: 0
```

Der Audit fiel aber noch durch, weil ein alter Felt-Quellenblock beziehungsweise alte CSS-Marker als Texttoken im Quellcode verblieben.

B177b entfernt diese Reste.

## Änderungen

- alte HTML-Felt-Markerblöcke entfernt
- alter B150-Felt-Source-Register-Block entfernt, falls vorhanden
- alte B149/B150-Felt-CSS-Blöcke entfernt
- keine regionale Karte geändert
- kein B169/B170/B176-Inhalt geändert

## Token-Counts

| Datei | Token | Vorher | Nachher |
|---|---|---:|---:|
| `index.html` | felt | {before_html_counts['felt']} | {after_html_counts['felt']} |
| `index.html` | openstreetmap/osm | {before_html_counts['openstreetmap']} | {after_html_counts['openstreetmap']} |
| `index.html` | iframe | {before_html_counts['iframe']} | {after_html_counts['iframe']} |
| `src/styles.css` | felt | {before_css_counts['felt']} | {after_css_counts['felt']} |
| `src/styles.css` | openstreetmap/osm | {before_css_counts['openstreetmap']} | {after_css_counts['openstreetmap']} |
| `src/styles.css` | iframe | {before_css_counts['iframe']} | {after_css_counts['iframe']} |

## Akzeptanz

- `index.html` enthält kein Felt-Token mehr
- `index.html` enthält kein OpenStreetMap/OSM-Token mehr
- `index.html` enthält kein iframe mehr
- alte Felt-CSS-Regeln sind entfernt
- B177 External Request Audit kann erneut laufen
"""
    write(DOC, doc)

    audit = f"""# B177b remove residual Felt tokens audit

Date: {today}

Post-patch checks:
- index felt count: {after_html_counts['felt']}
- index openstreetmap/osm count: {after_html_counts['openstreetmap']}
- index iframe count: {after_html_counts['iframe']}
- css felt count: {after_css_counts['felt']}
- css openstreetmap/osm count: {after_css_counts['openstreetmap']}
- css iframe count: {after_css_counts['iframe']}
- B176 marker still present: {'B176_LOCAL_CARTOGRAPHIC_DEPTH_START' in html_after}
- B169 live sticky zoom still present: {'B169_LIVE_STICKY_ZOOM_START' in html_after}
- regional static map phrase still present: {'Die regionale Karte zerlegt den Zusammenhang' in html_after}

Result: PATCH WRITTEN. Rerun B177, B103b and B58.
"""
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B177b remove residual Felt tokens complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B177b_remove_residual_felt_tokens.md")
    print("  docs/B177b_removed_residual_felt_tokens.csv")
    print("  docs/B177b_remove_residual_felt_tokens_audit.txt")
    print("  tasks/done.md")
    print("Post-patch counts:")
    print(f"  index felt: {after_html_counts['felt']}")
    print(f"  index openstreetmap/osm: {after_html_counts['openstreetmap']}")
    print(f"  index iframe: {after_html_counts['iframe']}")
    print("Next: python scripts\\177_external_request_audit.py")


if __name__ == "__main__":
    main()
