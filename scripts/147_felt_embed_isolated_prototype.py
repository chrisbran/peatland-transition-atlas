from pathlib import Path
import re
from datetime import date
from html import escape

ROOT = Path(".")
SCRIPT = ROOT / "scripts" / "147_felt_embed_isolated_prototype.py"
CANDIDATE = ROOT / "docs" / "B146_felt_embed_candidate.md"
PROTO_DIR = ROOT / "docs" / "prototypes"
PROTO = PROTO_DIR / "oberschwaben_felt_embed_test.html"
DOC = ROOT / "docs" / "B147_felt_embed_isolated_prototype.md"
AUDIT = ROOT / "docs" / "B147_felt_embed_isolated_prototype_audit.txt"
DONE = ROOT / "tasks" / "done.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_done(done_text: str) -> str:
    line = f"- B147 Felt embed isolated prototype: created a docs-only iframe prototype for local desktop/mobile testing before touching the public page ({date.today().isoformat()})."
    if "B147 Felt embed isolated prototype" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def extract_iframe(text: str) -> str:
    m = re.search(r"<iframe\b.*?</iframe>", text, re.S | re.I)
    if not m:
        return ""
    iframe = m.group(0).strip()

    # Remove fixed width/height attributes so the prototype can control responsiveness.
    iframe = re.sub(r'\swidth\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\swidth\s*=\s*'[^']*'", "", iframe, flags=re.I)
    iframe = re.sub(r'\sheight\s*=\s*"[^"]*"', "", iframe, flags=re.I)
    iframe = re.sub(r"\sheight\s*=\s*'[^']*'", "", iframe, flags=re.I)

    if "title=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe title="Oberschwaben Felt map pilot"', 1)

    if "loading=" not in iframe.lower():
        iframe = iframe.replace("<iframe", '<iframe loading="lazy"', 1)

    if "allowfullscreen" not in iframe.lower():
        iframe = iframe.replace("<iframe", "<iframe allowfullscreen", 1)

    return iframe


def extract_share_url(text: str) -> str:
    # Prefer first Felt map URL, ignoring placeholder strings.
    urls = re.findall(r"https://felt\.com/map/[^\s)`\"<>]+", text)
    if urls:
        return urls[0]

    # Fallback: any Felt URL.
    urls = re.findall(r"https://felt\.com/[^\s)`\"<>]+", text)
    if urls:
        return urls[0]

    return ""


def build_proto(today: str, iframe: str, share_url: str) -> str:
    if iframe:
        iframe_html = iframe
    elif share_url:
        iframe_html = f'<iframe title="Oberschwaben Felt map pilot" loading="lazy" allowfullscreen src="{escape(share_url)}"></iframe>'
    else:
        iframe_html = '<div class="missing">No Felt iframe/share URL found in docs/B146_felt_embed_candidate.md.</div>'

    share_link = f'<a href="{escape(share_url)}" target="_blank" rel="noopener noreferrer">Open Felt map in a new tab</a>' if share_url else "No share URL detected."

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>B147 Felt Embed Prototype - Oberschwaben</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #111512;
      --panel: #1b211d;
      --text: #f4efe4;
      --muted: #adb8aa;
      --line: rgba(244, 239, 228, 0.14);
      --accent: #087f7a;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      width: min(100% - 2rem, 82rem);
      margin-inline: auto;
      padding: 1rem 0 2rem;
    }}

    header {{
      display: grid;
      gap: 0.35rem;
      padding-block: 0.75rem 1rem;
      border-bottom: 1px solid var(--line);
    }}

    .eyebrow {{
      margin: 0;
      color: #9ac47c;
      font-size: 0.78rem;
      letter-spacing: 0.09em;
      text-transform: uppercase;
      font-weight: 800;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(1.35rem, 3.5vw, 2.4rem);
      line-height: 1.05;
    }}

    .lead {{
      max-width: 58rem;
      margin: 0.4rem 0 0;
      color: var(--muted);
      font-size: 0.98rem;
    }}

    .embed-wrap {{
      margin-top: 1rem;
      border: 1px solid var(--line);
      border-radius: 1rem;
      overflow: hidden;
      background: #0d100e;
      box-shadow: 0 18px 54px rgba(0, 0, 0, 0.34);
    }}

    .embed-ratio {{
      position: relative;
      width: 100%;
      min-height: min(76vh, 52rem);
      height: 76vh;
    }}

    iframe {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }}

    .missing {{
      display: grid;
      place-items: center;
      min-height: 22rem;
      padding: 2rem;
      color: #ffb4a8;
      text-align: center;
    }}

    .qa {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 1rem;
      margin-top: 1rem;
    }}

    section {{
      border: 1px solid var(--line);
      border-radius: 1rem;
      background: var(--panel);
      padding: 1rem;
    }}

    h2 {{
      margin: 0 0 0.6rem;
      font-size: 1rem;
    }}

    ul {{
      margin: 0;
      padding-left: 1.2rem;
      color: var(--muted);
      font-size: 0.92rem;
    }}

    li + li {{
      margin-top: 0.25rem;
    }}

    a {{
      color: #a3d6d1;
      text-underline-offset: 0.18em;
    }}

    .meta {{
      color: var(--muted);
      font-size: 0.84rem;
    }}

    @media (max-width: 760px) {{
      main {{
        width: min(100% - 1rem, 82rem);
      }}

      .embed-ratio {{
        height: 72vh;
        min-height: 34rem;
      }}

      .qa {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">B147 · isolated prototype</p>
      <h1>Oberschwaben Felt-Embed-Test</h1>
      <p class="lead">
        Isolierter Test des Felt-Kartenkandidaten. Diese Datei ist keine Live-Integration
        und ersetzt nicht die bestehende PNG-/Sticky-Karte in <code>index.html</code>.
      </p>
      <p class="meta">Generated: {today}. {share_link}</p>
    </header>

    <div class="embed-wrap" aria-label="Felt iframe prototype">
      <div class="embed-ratio">
        {iframe_html}
      </div>
    </div>

    <div class="qa">
      <section>
        <h2>Desktop/Mobile prüfen</h2>
        <ul>
          <li>Karte lädt ohne Login.</li>
          <li>Annotation ist sichtbar.</li>
          <li>Legende verdeckt nicht zu viel.</li>
          <li>Popup funktioniert per Klick.</li>
          <li>390-px-Breite bleibt brauchbar.</li>
        </ul>
      </section>
      <section>
        <h2>Vor Live-Einbau offen</h2>
        <ul>
          <li>Datenschutz-/Drittanbieter-Hinweis prüfen.</li>
          <li>Felt-Plan/Lizenz nach Trial klären.</li>
          <li>Fallback zur bestehenden PNG-Karte erhalten.</li>
          <li>Erst danach aktiver Integrationspatch.</li>
        </ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def build_doc(today: str, iframe_present: bool, share_url: str) -> str:
    return f"""# B147 - Felt Embed Isolated Prototype

Date: {today}

## Ziel

B147 erstellt einen isolierten iframe-Prototyp fuer den Felt-Kartenkandidaten.
Die Hauptseite wird weiterhin nicht veraendert.

## Erzeugte Prototype-Datei

```text
docs/prototypes/oberschwaben_felt_embed_test.html
```

Diese Datei dient nur zum lokalen Testen:

- Desktop
- mobile Breiten
- iframe-Ladeverhalten
- Popup/Interaktion
- Legende/Annotation
- visuelle Hoehe im Browser

## Status

| Punkt | Status |
|---|---|
| iframe aus B146 erkannt | {'ja' if iframe_present else 'nein'} |
| Share-URL erkannt | {'ja' if share_url else 'nein'} |
| public `index.html` geaendert | nein |
| `src/styles.css` geaendert | nein |
| lokale GeoJSON/Shapefiles committed | nein |

## Share-URL

```text
{share_url if share_url else '<not detected>'}
```

## Testanleitung

Lokal Server starten:

```powershell
python -m http.server 8000
```

Dann im Browser:

```text
http://localhost:8000/docs/prototypes/oberschwaben_felt_embed_test.html
```

Responsive Test:

```text
390 px Breite
```

## Entscheidung

B147 ist noch keine Live-Integration.
Wenn der isolierte Prototyp bestanden ist, kann B148 als eigentlicher Integrationsentscheid folgen:

- entweder Felt-Embed in die Oberschwaben-Section integrieren
- oder Felt nur als externer Link anbieten
- oder hochwertigen statischen Export/PNG-Fallback verwenden
"""


def main() -> None:
    today = date.today().isoformat()

    if CANDIDATE.exists():
        candidate_text = read(CANDIDATE)
    else:
        candidate_text = ""

    iframe = extract_iframe(candidate_text)
    share_url = extract_share_url(candidate_text)

    write(PROTO, build_proto(today, iframe, share_url))
    write(DOC, build_doc(today, bool(iframe), share_url))

    audit_text = f"""# B147 Felt embed isolated prototype audit

Date: {today}

Result: PROTOTYPE ONLY. No public page files changed.

Read:

- docs/B146_felt_embed_candidate.md exists: {CANDIDATE.exists()}

Extracted:

- iframe present: {bool(iframe)}
- share URL present: {bool(share_url)}
- share URL: {share_url if share_url else '<not detected>'}

Created/updated:

- docs/prototypes/oberschwaben_felt_embed_test.html
- docs/B147_felt_embed_isolated_prototype.md
- docs/B147_felt_embed_isolated_prototype_audit.txt
- tasks/done.md

No iframe was added to index.html.
No CSS was changed.
No local GeoJSON/Shapefile/GPKG files were staged or referenced for commit.
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text))

    print("B147 Felt embed isolated prototype complete.")
    print("Prototype only. No public page files changed.")
    print("Created/updated:")
    print("  docs/prototypes/oberschwaben_felt_embed_test.html")
    print("  docs/B147_felt_embed_isolated_prototype.md")
    print("  docs/B147_felt_embed_isolated_prototype_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
