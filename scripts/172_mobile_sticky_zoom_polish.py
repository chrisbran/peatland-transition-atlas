from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "172_mobile_sticky_zoom_polish.py"
DOC = ROOT / "docs" / "B172_mobile_sticky_zoom_polish.md"
AUDIT = ROOT / "docs" / "B172_mobile_sticky_zoom_polish_audit.txt"
CSV_OUT = ROOT / "docs" / "B172_mobile_sticky_zoom_checks.csv"
DONE = ROOT / "tasks" / "done.md"

B169_MARKER = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
B169_SCRIPT = "src/b169_live_sticky_zoom.js"

CSS_START = "/* B172_MOBILE_STICKY_ZOOM_POLISH_START */"
CSS_END = "/* B172_MOBILE_STICKY_ZOOM_POLISH_END */"

CHECKS = [
    {
        "check": "B169 live sticky zoom block",
        "pattern": B169_MARKER,
        "file": "index.html",
        "required": True,
    },
    {
        "check": "B169 live sticky zoom JS",
        "pattern": B169_SCRIPT,
        "file": "index.html",
        "required": True,
    },
    {
        "check": "Mobile media query exists",
        "pattern": "@media (max-width: 860px)",
        "file": "src/styles.css",
        "required": True,
    },
    {
        "check": "B169 layout class exists",
        "pattern": ".b169-layout",
        "file": "src/styles.css",
        "required": True,
    },
    {
        "check": "B169 stage wrapper exists",
        "pattern": ".b169-stage-wrap",
        "file": "src/styles.css",
        "required": True,
    },
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* Mobile polish for the B169 live sticky zoom.
   Keep desktop unchanged; on phones/tablets place the map stage before the steps
   and keep it lightly sticky so text and map stay connected. */
@media (max-width: 860px) {{
  .b169-layout {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }}

  .b169-stage-wrap {{
    order: 1;
    position: sticky;
    top: 3.15rem;
    z-index: 3;
    height: auto;
    min-height: 0;
    margin-inline: auto;
    width: min(100%, 42rem);
    display: block;
  }}

  .b169-steps {{
    order: 2;
    padding: 0 0 1rem;
  }}

  .b169-stage {{
    width: 100%;
    min-height: 0;
    height: auto;
    aspect-ratio: 16 / 10;
    border-radius: 0.9rem;
    box-shadow: 0 18px 52px rgba(25, 39, 32, 0.22);
  }}

  .b169-stage-label {{
    left: 0.65rem;
    top: 0.65rem;
    max-width: calc(100% - 1.3rem);
    padding: 0.48rem 0.58rem;
    border-radius: 0.55rem;
    font-size: 0.74rem;
    line-height: 1.18;
  }}

  .b169-step {{
    padding: clamp(1.15rem, 7vh, 2.4rem) 0;
    min-height: clamp(13rem, 46vh, 22rem);
    justify-content: center;
    border-bottom: 1px solid rgba(28, 42, 34, 0.08);
  }}

  .b169-step:last-child {{
    border-bottom: 0;
  }}

  .b169-step h3 {{
    max-width: 14em;
    font-size: clamp(1.55rem, 9vw, 2.4rem);
  }}

  .b169-step p:last-child {{
    max-width: 25rem;
    font-size: 0.98rem;
  }}

  .b169-mobile-note {{
    display: none;
  }}

  .b169-source-line {{
    margin-top: 1.4rem;
  }}
}}

@media (max-width: 420px) {{
  .b169-live-sticky-zoom {{
    padding-top: 2.5rem;
  }}

  .b169-stage-wrap {{
    top: 3rem;
    width: 100%;
  }}

  .b169-stage {{
    border-radius: 0.72rem;
  }}

  .b169-step {{
    min-height: 48vh;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B172 mobile sticky zoom polish: adjusted the live sticky zoom mobile layout so the map remains visually connected to the numbered scroll steps ({today})."
    if "B172 mobile sticky zoom polish" in done_text:
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

    rows = []
    for check in CHECKS:
        source = html if check["file"] == "index.html" else css
        found = check["pattern"] in source
        rows.append({
            "check": check["check"],
            "file": check["file"],
            "required": check["required"],
            "found": found,
            "pattern": check["pattern"],
        })

    missing_required = [r for r in rows if r["required"] and not r["found"]]
    if missing_required:
        detail = "\n".join([f"- {r['check']} ({r['pattern']})" for r in missing_required])
        raise SystemExit("Required B172 prerequisites missing:\n" + detail)

    old_css_had_block = CSS_START in css and CSS_END in css
    css = patch_css(css)
    write(CSS, css)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "file", "required", "found", "pattern"])
        writer.writeheader()
        writer.writerows(rows)

    doc = f"""# B172 - Mobile Sticky Zoom Polish

Date: {today}

## Ziel

B169 bis B170 haben die neue Live-Kartenfolge auf Desktop stabilisiert.
B172 poliert jetzt nur die mobile Darstellung.

Problem vorher:

```text
Auf kleinen Bildschirmen standen die Textsteps vor der Karte.
Dadurch war die Kartenfolge mobil nicht wirklich als Scrolly lesbar.
```

B172 ordnet die mobile Darstellung so um:

```text
Karte oben leicht sticky
nummerierte Steps darunter
```

Damit bleiben Karte und Text auch auf 390px-Breite verbunden.

## Änderungen

Nur CSS:

- `.b169-layout` wird mobil zu einer Flex-Spalte
- `.b169-stage-wrap` bekommt `order: 1`
- `.b169-steps` bekommt `order: 2`
- die Kartenbühne bleibt mobil leicht sticky
- Textsteps bekommen größere vertikale Atemräume
- die separate Mobile-Note wird ausgeblendet, weil das Layout jetzt selbsterklärender ist

## Nicht geändert

- keine HTML-Struktur
- keine JS-Logik
- keine Kartenassets
- keine Statefolge
- keine Oberschwaben-Story
- keine Felt-Integration

## Prüfen

Desktop:

- unverändert

Mobile 390px:

- Karte erscheint vor den Steps
- Karte bleibt beim Scrollen sichtbar
- aktive Steps wechseln die Karte
- Stage-Label bleibt lesbar
- keine riesige Lücke zwischen Step und Karte
"""
    write(DOC, doc)

    new_css = read(CSS)
    audit = "# B172 mobile sticky zoom polish audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"Old B172 CSS present before patch: {old_css_had_block}\n"
    audit += "Prerequisite checks:\n"
    for row in rows:
        audit += f"- {row['check']}: {row['found']}\n"

    audit += "\nPost-patch checks:\n"
    audit += f"- B172 CSS present: {CSS_START in new_css and CSS_END in new_css}\n"
    audit += f"- mobile order stage first present: {'order: 1;' in new_css and '.b169-stage-wrap' in new_css}\n"
    audit += f"- mobile order steps second present: {'order: 2;' in new_css and '.b169-steps' in new_css}\n"
    audit += f"- sticky mobile stage present: {'position: sticky;' in new_css and 'top: 3.15rem;' in new_css}\n"
    audit += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B172 mobile sticky zoom polish complete.")
    print("Changed: src/styles.css")
    print("Created/updated:")
    print("  docs/B172_mobile_sticky_zoom_polish.md")
    print("  docs/B172_mobile_sticky_zoom_checks.csv")
    print("  docs/B172_mobile_sticky_zoom_polish_audit.txt")
    print("  tasks/done.md")
    print("Next: run B103b and B58 QA, then mobile visual QA at 390px.")


if __name__ == "__main__":
    main()
