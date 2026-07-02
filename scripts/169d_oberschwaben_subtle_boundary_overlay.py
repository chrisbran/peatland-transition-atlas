from pathlib import Path
from datetime import date
import csv
import re

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "169d_oberschwaben_subtle_boundary_overlay.py"
DOC = ROOT / "docs" / "B169d_oberschwaben_subtle_boundary_overlay.md"
CSV_OUT = ROOT / "docs" / "B169d_oberschwaben_boundary_candidates.csv"
AUDIT = ROOT / "docs" / "B169d_oberschwaben_subtle_boundary_overlay_audit.txt"
DONE = ROOT / "tasks" / "done.md"

HTML_START = "<!-- B169_LIVE_STICKY_ZOOM_START -->"
HTML_END = "<!-- /B169_LIVE_STICKY_ZOOM_END -->"
CSS_START = "/* B169D_OBERSCHWABEN_SUBTLE_BOUNDARY_OVERLAY_START */"
CSS_END = "/* B169D_OBERSCHWABEN_SUBTLE_BOUNDARY_OVERLAY_END */"

STATE = "oberschwaben-handoff"
BASE = "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png"

# Prefer label-free boundary/outline candidates if such assets exist.
PREFERRED_OVERLAYS = [
    "public/maps/oberschwaben/oberschwaben_boundary_outline.png",
    "public/maps/oberschwaben/oberschwaben_boundaries.png",
    "public/maps/oberschwaben/oberschwaben_landkreis_boundaries.png",
    "public/maps/oberschwaben/oberschwaben_county_boundaries.png",
    "public/maps/oberschwaben/oberschwaben_admin_boundaries.png",
    "public/maps/oberschwaben/oberschwaben_admin_context_no_labels.png",
    "public/maps/oberschwaben/oberschwaben_admin_context.png",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\s*", re.S)
    return pattern.sub("", text)


def html_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def candidate_score(path: str) -> int:
    lower = path.lower()
    score = 0
    if "oberschwaben" in lower:
        score += 20
    if "boundary" in lower or "boundaries" in lower or "grenz" in lower or "outline" in lower:
        score += 12
    if "landkreis" in lower or "county" in lower or "admin" in lower:
        score += 7
    if "no_label" in lower or "nolabel" in lower or "no-label" in lower:
        score += 10
    if "context" in lower:
        score += 2
    # Penalize likely label-rich rasters, but allow as fallback.
    if "admin_context" in lower and not ("no_label" in lower or "nolabel" in lower or "no-label" in lower):
        score -= 4
    return score


def discover_candidates() -> list[dict]:
    candidates = []

    for rel in PREFERRED_OVERLAYS:
        p = ROOT / rel
        candidates.append({
            "path": rel,
            "exists": p.exists(),
            "size_bytes": p.stat().st_size if p.exists() else "",
            "score": candidate_score(rel),
            "source": "preferred",
        })

    maps_root = ROOT / "public" / "maps"
    if maps_root.exists():
        for p in sorted(maps_root.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
                continue
            rel = p.as_posix()
            lower = rel.lower()
            if "oberschwaben" not in lower:
                continue
            if not any(token in lower for token in ["admin", "boundary", "boundaries", "grenz", "outline", "landkreis", "county"]):
                continue
            if any(c["path"] == rel for c in candidates):
                continue
            candidates.append({
                "path": rel,
                "exists": True,
                "size_bytes": p.stat().st_size,
                "score": candidate_score(rel),
                "source": "discovered",
            })

    candidates.sort(key=lambda r: (bool(r["exists"]), r["score"], str(r["path"])), reverse=True)
    return candidates


def choose_overlay(candidates: list[dict]) -> tuple[str, str]:
    existing = [c for c in candidates if c["exists"]]
    if not existing:
        return "", "none_found"

    selected = existing[0]["path"]
    if selected.endswith("oberschwaben_admin_context.png"):
        return selected, "fallback_admin_context_softened"
    return selected, "preferred_label_free_or_boundary_asset"


def make_overlay_tag(overlay: str, mode: str) -> str:
    klass = "is-active"  # It will be active only when the state is active via JS; initial class is harmless if JS updates.
    soft = "true" if mode == "fallback_admin_context_softened" else "false"
    return (
        f'<img src="{html_escape(overlay)}" alt="Grenzen / Orientierung für Oberschwaben" '
        f'data-b169-overlay="{STATE}" data-b169-oberschwaben-boundary="true" '
        f'data-b169-soft-boundary="{soft}" class="{klass}" loading="lazy">'
    )


def patch_html(html: str, overlay: str, mode: str, audit: list[str]) -> str:
    start = html.find(HTML_START)
    end = html.find(HTML_END)
    if start < 0 or end < 0:
        raise SystemExit("B169 marked block not found. Run B169/B169c before B169d.")
    end += len(HTML_END)

    block = html[start:end]
    old_overlay_count = block.count(f'data-b169-overlay="{STATE}"')
    audit.append(f"Old oberschwaben overlay count in B169 block: {old_overlay_count}")

    # Remove existing Oberschwaben overlay tags first, including B169c's removed state if partially present.
    block = re.sub(
        r'\s*<img\b(?=[^>]*data-b169-overlay="' + re.escape(STATE) + r'")[^>]*>',
        "",
        block,
        flags=re.I | re.S,
    )

    if overlay:
        # Insert after the base image for the same state.
        base_pattern = re.compile(
            r'(<img\b(?=[^>]*data-b169-base="' + re.escape(STATE) + r'")[^>]*>)',
            re.I | re.S,
        )
        m = base_pattern.search(block)
        if not m:
            raise SystemExit("Could not find Oberschwaben base image in B169 block.")

        overlay_tag = make_overlay_tag(overlay, mode)
        block = block[:m.end()] + "\n        " + overlay_tag + block[m.end():]
        audit.append(f"Inserted oberschwaben overlay: {overlay}")
        audit.append(f"Overlay mode: {mode}")
    else:
        audit.append("WARN no overlay inserted because no candidate exists")

    html = html[:start] + block + html[end:]
    return html


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)

    block = f"""
{CSS_START}
/* B169d: bring back Oberschwaben orientation, but keep label-heavy overlays subdued. */
.b169-stage img[data-b169-oberschwaben-boundary="true"] {{
  opacity: 0;
  mix-blend-mode: screen;
  filter: grayscale(1) contrast(1.35) brightness(1.28);
}}

.b169-stage img[data-b169-oberschwaben-boundary="true"].is-active {{
  opacity: 0.28;
}}

.b169-stage img[data-b169-soft-boundary="true"].is-active {{
  opacity: 0.18;
  filter: grayscale(1) contrast(1.65) brightness(1.05);
}}

@media (max-width: 860px) {{
  .b169-stage img[data-b169-oberschwaben-boundary="true"].is-active {{
    opacity: 0.34;
  }}

  .b169-stage img[data-b169-soft-boundary="true"].is-active {{
    opacity: 0.22;
  }}
}}
{CSS_END}
"""
    return css.rstrip() + "\n\n" + block.lstrip()


def update_done(done_text: str, today: str) -> str:
    line = f"- B169d Oberschwaben subtle boundary overlay: restored a subdued regional boundary overlay in the live sticky zoom to keep orientation without making Landkreis labels dominate ({today})."
    if "B169d Oberschwaben subtle boundary overlay" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")
    if not CSS.exists():
        raise SystemExit("src/styles.css not found")

    candidates = discover_candidates()
    overlay, mode = choose_overlay(candidates)

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "exists", "size_bytes", "score", "source"])
        writer.writeheader()
        writer.writerows(candidates)

    audit = []
    audit.append(f"Selected overlay: {overlay or 'none'}")
    audit.append(f"Selected mode: {mode}")

    html = read(INDEX)
    css = read(CSS)

    html = patch_html(html, overlay, mode, audit)
    css = patch_css(css)

    write(INDEX, html)
    write(CSS, css)

    doc = f"""# B169d - Oberschwaben Subtle Boundary Overlay

Date: {today}

## Ziel

B169c entfernte das Oberschwaben-Admin-Overlay, weil Landkreisnamen im Sticky-Zoom wie Artefakte wirkten.
Ganz ohne Grenzen fehlt aber räumliche Orientierung.

B169d stellt deshalb eine **subtile regionale Orientierungsebene** wieder her.

## Vorgehen

Der Patch sucht zuerst nach möglichst label-freien Oberschwaben-Grenzassets, zum Beispiel:

```text
oberschwaben_boundary_outline.png
oberschwaben_landkreis_boundaries.png
oberschwaben_admin_context_no_labels.png
```

Falls kein label-freies Asset vorhanden ist, nutzt er als Fallback:

```text
public/maps/oberschwaben/oberschwaben_admin_context.png
```

aber stark abgeschwächt.

## Gewähltes Overlay

```text
{overlay or 'kein Overlay gefunden'}
```

Modus:

```text
{mode}
```

## CSS-Logik

Für Oberschwaben wird das Overlay separat markiert:

```html
data-b169-oberschwaben-boundary="true"
```

Bei Fallback auf `admin_context` zusätzlich:

```html
data-b169-soft-boundary="true"
```

Dadurch können Grenzen sichtbar bleiben, während Label-Artefakte möglichst wenig dominieren.

## Nicht geändert

- keine neue Statefolge
- keine neue Karte erzeugt
- keine Änderung an Felt
- keine Änderung an Oberschwaben-Detailkarte
- keine Änderung an Scorecard

## Bessere langfristige Lösung

Für den finalen Live-Zoom wäre ein echtes label-freies Boundary-Asset besser:

```text
public/maps/oberschwaben/oberschwaben_landkreis_boundaries.png
```

oder:

```text
public/maps/oberschwaben/oberschwaben_boundary_outline.png
```

Das sollte später aus ArcGIS/mapshaper exportiert werden, falls die abgeschwächte Admin-Kontext-Ebene noch zu unruhig wirkt.
"""
    write(DOC, doc)

    new_html = read(INDEX)
    new_css = read(CSS)

    audit_text = "# B169d Oberschwaben subtle boundary overlay audit\n\n"
    audit_text += f"Date: {today}\n\n"
    audit_text += "\n".join(audit) + "\n\n"
    audit_text += "Candidate count: " + str(len(candidates)) + "\n\n"
    audit_text += "Post-patch checks:\n"
    audit_text += f"- oberschwaben overlay present: {f'data-b169-overlay=\"{STATE}\"' in new_html}\n"
    audit_text += f"- oberschwaben boundary marker present: {'data-b169-oberschwaben-boundary=\"true\"' in new_html}\n"
    audit_text += f"- soft boundary mode present: {'data-b169-soft-boundary=\"true\"' in new_html}\n"
    audit_text += f"- B169d CSS present: {CSS_START in new_css and CSS_END in new_css}\n"
    audit_text += "\nResult: PATCH WRITTEN. Run B103b and B58 before commit.\n"
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B169d Oberschwaben subtle boundary overlay complete.")
    print("Changed: index.html, src/styles.css")
    print("Created/updated:")
    print("  docs/B169d_oberschwaben_subtle_boundary_overlay.md")
    print("  docs/B169d_oberschwaben_boundary_candidates.csv")
    print("  docs/B169d_oberschwaben_subtle_boundary_overlay_audit.txt")
    print("  tasks/done.md")
    print(f"Selected overlay: {overlay or 'none'}")
    print(f"Mode: {mode}")
    print("Next: hard-refresh browser and visually check Oberschwaben step.")


if __name__ == "__main__":
    main()
