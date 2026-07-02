from pathlib import Path
from datetime import date
import csv
import json
import re

ROOT = Path(".")
PROTOTYPE = ROOT / "docs" / "prototypes" / "B165_flagship_sticky_zoom_prototype.html"
SCRIPT = ROOT / "scripts" / "167_sticky_zoom_state_repair.py"
DOC = ROOT / "docs" / "B167_sticky_zoom_state_repair.md"
MATRIX = ROOT / "docs" / "B167_sticky_zoom_state_matrix_repaired.csv"
AUDIT = ROOT / "docs" / "B167_sticky_zoom_state_repair_audit.txt"
DONE = ROOT / "tasks" / "done.md"

BASE_STEPS = [
    {
        "state": "global-peat",
        "base": "public/maps/global/global_gpm2_peat_extent.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "kicker": "01 / Welt",
        "title": "Kleine Fläche, große Wirkung",
        "text": "Moore nehmen global wenig Raum ein. Für Klima, Wasser und Biodiversität sind sie trotzdem entscheidend.",
        "stage_label": "Globale Moorverbreitung",
        "annotation": "Die Karte zeigt die räumliche Konzentration von Mooren — nicht ihre lokale Nutzbarkeit.",
    },
    {
        "state": "global-pressure-total",
        "base": "public/maps/global/global_hotspots_total.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "kicker": "02 / Gesamt",
        "title": "Wo ist der gesamte Emissionsdruck hoch?",
        "text": "Die absolute Menge zeigt, wo drainierte organische Böden global besonders stark zur Emissionsbilanz beitragen.",
        "stage_label": "Gesamt-Emissionsdruck",
        "annotation": "Gesamtwerte zeigen große Beiträge — oft dort, wo Fläche, Entwässerung und Nutzung zusammenkommen.",
    },
    {
        "state": "global-pressure-density",
        "base": "public/maps/global/global_hotspots_density.png",
        "overlay": "public/maps/global/global_country_borders.png",
        "kicker": "03 / Intensität",
        "title": "Wo ist der Druck pro Fläche besonders hoch?",
        "text": "Die Intensitätskarte erzählt eine andere Geschichte: Nicht nur die Gesamtmenge zählt, sondern der Druck pro Fläche.",
        "stage_label": "Emissionsintensität pro Fläche",
        "annotation": "Intensität und Gesamtmenge sind unterschiedliche Aussagen. Für Planung müssen beide getrennt gelesen werden.",
    },
    {
        "state": "europe-bridge",
        "base": "public/maps/europe/europe_gpm2_peat_extent.png",
        "overlay": "public/maps/europe/europe_country_borders.png",
        "kicker": "04 / Europa",
        "title": "Aus Relevanz wird Planung",
        "text": "Der Maßstab wechselt: Klimafragen werden zu politischen und regionalen Planungskulissen.",
        "stage_label": "Europäischer Bezugsraum",
        "annotation": "Der regionale Blick wird erst verständlich, wenn der größere Bezugsraum steht.",
    },
    {
        "state": "germany-extent",
        "base": "public/maps/germany/germany_thuenen_moor_extent.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "kicker": "05 / Deutschland",
        "title": "Die nationale Karte zeigt, wo genauer hingesehen werden muss",
        "text": "Organische Böden bilden eine Planungskulisse. Welche Nutzung tragfähig ist, entscheidet sich aber erst darunter.",
        "stage_label": "Organische Böden in Deutschland",
        "annotation": "Die nationale Kulisse grenzt Prüfbedarf ein — sie ersetzt keine Standortprüfung.",
    },
    {
        "state": "germany-types",
        "base": "public/maps/germany/germany_thuenen_moor_types.png",
        "overlay": "public/maps/germany/germany_admin_context.png",
        "kicker": "06 / Bodenkontext",
        "title": "Nicht jeder Moorboden stellt dieselbe Frage",
        "text": "Typen, Nutzung und Wasserstand unterscheiden sich. Deshalb braucht Moorbodenschutz mehr als eine Flächenkarte.",
        "stage_label": "Typen organischer Böden",
        "annotation": "Die Karte bereitet die regionale Frage vor: Welche Nutzung trifft auf welchen Bodenkontext?",
    },
]

REGIONAL_BASE_PREFERENCE = [
    "public/maps/oberschwaben/oberschwaben_agriculture_moor_intersection.png",
    "public/maps/oberschwaben_lgl/oberschwaben_lgl_landuse_bk50_intersection.png",
    "public/maps/oberschwaben/oberschwaben_moor_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
]

REGIONAL_OVERLAY_PREFERENCE = [
    "public/maps/oberschwaben/oberschwaben_admin_context.png",
    "public/maps/bw/bw_admin_context.png",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def exists(rel: str) -> bool:
    if not rel or rel in {"REGIONAL_ASSET_REQUIRED", "MATCHING_REGIONAL_BOUNDARY_REQUIRED_OR_EMBEDDED"}:
        return False
    return (ROOT / rel).exists()


def first_existing(paths: list[str]) -> str:
    for rel in paths:
        if exists(rel):
            return rel
    return ""


def rel_from_prototype(path: str) -> str:
    return "../../" + path.replace("\\", "/")


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def build_steps() -> tuple[list[dict], list[str]]:
    audit = []
    steps = []

    for step in BASE_STEPS:
        base_exists = exists(step["base"])
        overlay_exists = exists(step["overlay"])
        audit.append(f"{step['state']}: base exists={base_exists}; overlay exists={overlay_exists}")
        if not base_exists:
            audit.append(f"WARN skipping {step['state']} because base asset is missing: {step['base']}")
            continue

        s = dict(step)
        s["base_exists"] = base_exists
        s["overlay_exists"] = overlay_exists
        s["src"] = rel_from_prototype(s["base"])
        s["overlay_src"] = rel_from_prototype(s["overlay"]) if overlay_exists else ""
        steps.append(s)

    regional_base = first_existing(REGIONAL_BASE_PREFERENCE)
    regional_overlay = first_existing(REGIONAL_OVERLAY_PREFERENCE)

    if regional_base:
        regional_scope = "oberschwaben" if "/oberschwaben/" in regional_base or "oberschwaben_" in regional_base else "bw"
        overlay_scope = "none"
        if regional_overlay:
            overlay_scope = "oberschwaben" if "/oberschwaben/" in regional_overlay or "oberschwaben_" in regional_overlay else "bw"

        # Only use a matching regional overlay. Never use germany_admin_context for this state.
        use_overlay = ""
        if regional_overlay and (
            (regional_scope == "oberschwaben" and overlay_scope == "oberschwaben") or
            (regional_scope == "bw" and overlay_scope in {"bw", "oberschwaben"})
        ):
            use_overlay = regional_overlay

        steps.append({
            "state": "oberschwaben-handoff",
            "base": regional_base,
            "overlay": use_overlay,
            "base_exists": True,
            "overlay_exists": bool(use_overlay),
            "src": rel_from_prototype(regional_base),
            "overlay_src": rel_from_prototype(use_overlay) if use_overlay else "",
            "kicker": "07 / Region",
            "title": "Hier trifft Moorschutz auf Landwirtschaft",
            "text": "In Oberschwaben überlagern sich Moor-/Feuchtbodenkontext und heutige Nutzung. Aus Klima wird eine regionale Nutzungsfrage.",
            "stage_label": "Übergang nach Oberschwaben",
            "annotation": "Der Sticky-Zoom endet mit einer regional passenden Karte — ohne Deutschland-Grenzen als falsches Overlay.",
        })
        audit.append(f"oberschwaben-handoff: selected regional base={regional_base}")
        audit.append(f"oberschwaben-handoff: selected regional overlay={use_overlay or 'none'}")
    else:
        steps.append({
            "state": "oberschwaben-handoff",
            "base": "",
            "overlay": "",
            "base_exists": False,
            "overlay_exists": False,
            "src": "",
            "overlay_src": "",
            "kicker": "07 / Region",
            "title": "Hier müsste Oberschwaben erscheinen",
            "text": "Für den finalen Übergabeschritt fehlt noch ein regionales Exportbild mit passender Grenze.",
            "stage_label": "Regionaler Export fehlt",
            "annotation": "Gate offen: regionales Oberschwaben/BW-Asset exportieren.",
        })
        audit.append("WARN no regional base asset found for oberschwaben-handoff")

    return steps, audit


def build_html(steps: list[dict], today: str) -> str:
    initial = steps[0] if steps else {
        "stage_label": "Keine Assets gefunden",
        "annotation": "Bitte Kartenassets prüfen.",
        "state": "none",
    }

    step_markup = []
    for i, step in enumerate(steps):
        active = " is-active" if i == 0 else ""
        step_markup.append(f"""
          <article class="b165-step{active}" data-b165-step data-state="{html_escape(step['state'])}" tabindex="0">
            <p class="b165-kicker">{html_escape(step['kicker'])}</p>
            <h3>{html_escape(step['title'])}</h3>
            <p>{html_escape(step['text'])}</p>
          </article>""")

    base_imgs = []
    overlay_imgs = []

    for i, step in enumerate(steps):
        if step.get("src"):
            cls = "is-active" if i == 0 else ""
            base_imgs.append(
                f'<img src="{html_escape(step["src"])}" alt="{html_escape(step["stage_label"])}" '
                f'data-b165-img="{html_escape(step["state"])}" class="{cls}">'
            )
        if step.get("overlay_src"):
            cls = "is-active" if i == 0 else ""
            overlay_imgs.append(
                f'<img src="{html_escape(step["overlay_src"])}" alt="{html_escape("politische Grenzen / Orientierung für " + step["state"])}" '
                f'data-b165-boundary="{html_escape(step["state"])}" class="{cls}">'
            )

    data_json = json.dumps(steps, ensure_ascii=False, indent=2)

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>B167 Repaired Flagship Sticky Zoom Prototype</title>
  <style>
    :root {{
      --bg: #f7f2e8;
      --ink: #192720;
      --muted: #637266;
      --panel: rgba(255,255,255,0.72);
      --dark: #101511;
      --accent: #087f7a;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    .b165-page {{
      min-height: 100vh;
    }}

    .b165-hero {{
      width: min(100% - 2rem, 76rem);
      margin: 0 auto;
      padding: 4rem 0 2.5rem;
    }}

    .b165-eyebrow {{
      margin: 0 0 0.8rem;
      color: #6b7f51;
      font-size: 0.78rem;
      font-weight: 900;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}

    h1 {{
      max-width: 13ch;
      margin: 0;
      font-size: clamp(2.6rem, 7vw, 6.2rem);
      line-height: 0.94;
      letter-spacing: -0.06em;
      text-wrap: balance;
    }}

    .b165-hero p:not(.b165-eyebrow) {{
      max-width: 48rem;
      margin: 1.2rem 0 0;
      color: var(--muted);
      font-size: clamp(1.05rem, 1.6vw, 1.35rem);
      line-height: 1.45;
    }}

    .b165-sticky {{
      width: min(100% - 2rem, 82rem);
      margin: 0 auto;
      padding: 1rem 0 5rem;
      display: grid;
      grid-template-columns: minmax(18rem, 24rem) minmax(0, 1fr);
      gap: clamp(1.4rem, 3vw, 3rem);
      align-items: start;
    }}

    .b165-steps {{
      padding: 18vh 0 28vh;
    }}

    .b165-step {{
      min-height: 42vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 0.42;
      transition: opacity 180ms ease, transform 180ms ease;
    }}

    .b165-step.is-active {{
      opacity: 1;
      transform: translateX(0.35rem);
    }}

    .b165-kicker {{
      margin: 0 0 0.5rem;
      color: #6b7f51;
      font-size: 0.74rem;
      font-weight: 900;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}

    .b165-step h3 {{
      margin: 0;
      max-width: 13em;
      font-size: clamp(1.5rem, 2.8vw, 2.35rem);
      line-height: 1.02;
      letter-spacing: -0.035em;
      text-wrap: balance;
    }}

    .b165-step p:last-child {{
      max-width: 24rem;
      margin: 0.85rem 0 0;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.5;
      text-wrap: pretty;
    }}

    .b165-stage-wrap {{
      position: sticky;
      top: 2rem;
      height: calc(100vh - 4rem);
      min-height: 34rem;
      display: grid;
      place-items: center;
    }}

    .b165-stage {{
      position: relative;
      width: 100%;
      height: min(78vh, 46rem);
      min-height: 31rem;
      overflow: hidden;
      border-radius: 1.15rem;
      background: var(--dark);
      border: 1px solid rgba(25, 39, 32, 0.18);
      box-shadow: 0 28px 86px rgba(25, 39, 32, 0.25);
    }}

    .b165-stage img {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0;
      transform: scale(1.018);
      transition: opacity 360ms ease, transform 560ms ease;
    }}

    .b165-stage img.is-active {{
      opacity: 1;
      transform: scale(1);
    }}

    .b165-stage img[data-b165-img] {{
      z-index: 1;
    }}

    .b165-stage img[data-b165-boundary] {{
      z-index: 2;
      object-fit: cover;
      mix-blend-mode: screen;
      opacity: 0;
      filter: contrast(1.08) brightness(1.16);
      pointer-events: none;
      transform: scale(1.018);
    }}

    .b165-stage img[data-b165-boundary].is-active {{
      opacity: 0.62;
      transform: scale(1);
    }}

    .b165-stage-label {{
      position: absolute;
      left: 1rem;
      top: 1rem;
      z-index: 4;
      max-width: min(28rem, calc(100% - 2rem));
      padding: 0.72rem 0.86rem;
      border-radius: 0.75rem;
      background: rgba(13, 20, 16, 0.76);
      color: rgba(248, 245, 236, 0.94);
      font-weight: 850;
      letter-spacing: -0.02em;
      backdrop-filter: blur(10px);
    }}

    .b165-annotation {{
      position: absolute;
      right: 1rem;
      bottom: 1rem;
      z-index: 4;
      max-width: min(30rem, calc(100% - 2rem));
      padding: 0.8rem 0.9rem;
      border-left: 3px solid rgba(8, 127, 122, 0.85);
      border-radius: 0.75rem;
      background: rgba(248, 245, 236, 0.88);
      color: #24352c;
      font-size: 0.92rem;
      line-height: 1.42;
      box-shadow: 0 16px 42px rgba(0,0,0,0.18);
    }}

    .b165-source {{
      width: min(100% - 2rem, 76rem);
      margin: -2.5rem auto 4rem;
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.45;
    }}

    .b165-mobile-note {{
      display: none;
      width: min(100% - 2rem, 76rem);
      margin: 0 auto 2rem;
      padding: 0.9rem 1rem;
      border-radius: 0.85rem;
      background: var(--panel);
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.45;
    }}

    @media (max-width: 800px) {{
      .b165-hero {{
        padding-top: 2.5rem;
      }}

      .b165-sticky {{
        display: block;
        width: min(100% - 1.25rem, 82rem);
        padding-bottom: 2rem;
      }}

      .b165-mobile-note {{
        display: block;
      }}

      .b165-steps {{
        padding: 0;
      }}

      .b165-step {{
        min-height: auto;
        padding: 1.5rem 0 0.75rem;
        opacity: 1;
        transform: none;
      }}

      .b165-stage-wrap {{
        position: static;
        height: auto;
        min-height: 0;
      }}

      .b165-stage {{
        height: auto;
        min-height: 0;
        aspect-ratio: 16 / 10;
      }}

      .b165-stage img[data-b165-boundary].is-active {{
        opacity: 0.72;
      }}

      .b165-annotation {{
        position: static;
        max-width: none;
        margin: 0.75rem 0 0;
        border-radius: 0.75rem;
      }}

      .b165-stage-label {{
        font-size: 0.86rem;
      }}
    }}
  </style>
</head>
<body>
  <main class="b165-page">
    <header class="b165-hero">
      <p class="b165-eyebrow">B167 · reparierter Prototyp</p>
      <h1>Der Maßstab entscheidet</h1>
      <p>Globale Karten zeigen, warum Moore relevant sind. Regional wird sichtbar, wo Planung beginnt.</p>
    </header>

    <p class="b165-mobile-note">
      Mobile Prototyp-Logik: Der spätere Seitenumbau sollte auf kleinen Bildschirmen eine vereinfachte
      vertikale Kartenfolge nutzen, statt einen schweren Sticky-Zoom zu erzwingen.
    </p>

    <section class="b165-sticky" aria-label="Flagship Sticky Zoom Prototype">
      <div class="b165-steps">
        {''.join(step_markup)}
      </div>

      <div class="b165-stage-wrap">
        <figure class="b165-stage" aria-label="Kartenbühne">
          <div class="b165-stage-label" data-b165-label>{html_escape(initial['stage_label'])}</div>
          {"".join(base_imgs)}
          {"".join(overlay_imgs)}
          <figcaption class="b165-annotation" data-b165-annotation>{html_escape(initial['annotation'])}</figcaption>
        </figure>
      </div>
    </section>

    <p class="b165-source">
      Isolierter Prototyp auf Basis vorhandener Kartenassets. Kein neuer Datenanspruch.
      Repariert nach B166: Total- und Intensitätskarte getrennt; Regional-Step mit passendem regionalem Overlay.
      Erst nach redaktioneller Prüfung in die Hauptseite integrieren.
    </p>
  </main>

  <script type="application/json" id="b165-data">
{data_json}
  </script>
  <script>
    (function () {{
      var dataEl = document.getElementById('b165-data');
      var data = JSON.parse(dataEl.textContent);
      var steps = Array.prototype.slice.call(document.querySelectorAll('[data-b165-step]'));
      var imgs = Array.prototype.slice.call(document.querySelectorAll('[data-b165-img]'));
      var boundaries = Array.prototype.slice.call(document.querySelectorAll('[data-b165-boundary]'));
      var label = document.querySelector('[data-b165-label]');
      var annotation = document.querySelector('[data-b165-annotation]');

      function setState(state) {{
        var item = data.find(function (d) {{ return d.state === state; }}) || data[0];
        steps.forEach(function (step) {{
          step.classList.toggle('is-active', step.getAttribute('data-state') === state);
        }});
        imgs.forEach(function (img) {{
          img.classList.toggle('is-active', img.getAttribute('data-b165-img') === state);
        }});
        boundaries.forEach(function (img) {{
          img.classList.toggle('is-active', img.getAttribute('data-b165-boundary') === state);
        }});
        if (label && item) label.textContent = item.stage_label;
        if (annotation && item) annotation.textContent = item.annotation;
      }}

      if (!steps.length) return;
      setState(steps[0].getAttribute('data-state'));

      if (!('IntersectionObserver' in window)) {{
        steps.forEach(function (step) {{
          step.addEventListener('mouseenter', function () {{ setState(step.getAttribute('data-state')); }});
          step.addEventListener('focusin', function () {{ setState(step.getAttribute('data-state')); }});
        }});
        return;
      }}

      var observer = new IntersectionObserver(function (entries) {{
        entries.forEach(function (entry) {{
          if (entry.isIntersecting) {{
            setState(entry.target.getAttribute('data-state'));
          }}
        }});
      }}, {{
        root: null,
        rootMargin: '-38% 0px -42% 0px',
        threshold: 0.01
      }});

      steps.forEach(function (step) {{ observer.observe(step); }});
    }})();
  </script>
</body>
</html>
"""


def update_done(done_text: str, today: str) -> str:
    line = f"- B167 sticky zoom state repair: repaired the isolated sticky-zoom prototype by splitting total/density pressure states and using a matching regional boundary overlay ({today})."
    if "B167 sticky zoom state repair" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    old_exists = PROTOTYPE.exists()
    old_contains_density = False
    old_regional_germany_overlay = False

    if old_exists:
        old_text = read(PROTOTYPE)
        old_contains_density = "global_hotspots_density.png" in old_text
        old_regional_germany_overlay = (
            'data-b165-boundary="regional-handoff"' in old_text
            and "germany_admin_context.png" in old_text
        )

    steps, step_audit = build_steps()

    write(PROTOTYPE, build_html(steps, today))

    with MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "order",
                "state",
                "base",
                "base_exists",
                "overlay",
                "overlay_exists",
                "title",
                "stage_label",
            ],
        )
        writer.writeheader()
        for i, step in enumerate(steps, start=1):
            writer.writerow({
                "order": i,
                "state": step["state"],
                "base": step.get("base", ""),
                "base_exists": step.get("base_exists", False),
                "overlay": step.get("overlay", ""),
                "overlay_exists": step.get("overlay_exists", False),
                "title": step["title"],
                "stage_label": step["stage_label"],
            })

    doc = f"""# B167 - Sticky Zoom State Repair

Date: {today}

## Ziel

B167 repariert den isolierten B165/B165b-Sticky-Zoom-Prototyp nach der B166-Inventur.

B166 hatte zwei konkrete Probleme markiert:

1. Die vorhandene globale Emissionsintensitätskarte `global_hotspots_density.png` fehlte im Prototyp.
2. Der regionale Oberschwaben-Step war falsch gekoppelt: regionale Basiskarte plus Deutschland-Admin-Overlay.

## Änderungen

### 1. Globaler Druck getrennt

Alt:

```text
global-pressure -> global_hotspots_total.png
```

Neu:

```text
global-pressure-total   -> global_hotspots_total.png
global-pressure-density -> global_hotspots_density.png
```

Damit unterscheidet der Prototyp jetzt zwischen:

- absolutem Gesamt-Emissionsdruck
- Emissionsintensität pro Fläche

### 2. Regional-Step repariert

Alt:

```text
regional-handoff base    = regionales Oberschwaben-Asset
regional-handoff overlay = germany_admin_context.png
```

Neu:

```text
oberschwaben-handoff base    = regionales Oberschwaben-Asset
oberschwaben-handoff overlay = passendes regionales Overlay, falls vorhanden
```

Die Deutschland-Grenzen werden im Regional-Step nicht mehr als Overlay verwendet.

### 3. Prototyp neu geschrieben

Der isolierte Prototyp bleibt:

```text
docs/prototypes/B165_flagship_sticky_zoom_prototype.html
```

Die Hauptseite bleibt unverändert.

## Finale Stepfolge im Prototyp

| Nr. | State | Basis | Overlay |
|---:|---|---|---|
"""
    for i, step in enumerate(steps, start=1):
        doc += f"| {i} | `{step['state']}` | `{step.get('base','')}` | `{step.get('overlay','') or 'none'}` |\n"

    doc += """
## Nicht geändert

- keine Änderung an `index.html`
- keine Änderung an `src/styles.css`
- keine Änderung an der öffentlichen Hauptseite
- keine neuen Kartenexports
- keine raw GIS-Dateien

## Visuelle Prüfung

Nach B167 prüfen:

- Total- und Density-Step sind beide sichtbar und unterscheidbar.
- Der Oberschwaben-Step zeigt keine Deutschland-Grenzen mehr als falsches Overlay.
- Regionale Grenzen, falls eingeblendet, passen zur regionalen Karte.
- Sieben Steps sind noch rhythmisch tragbar.
- Falls sieben Steps zu lang wirken: Total oder Density redaktionell priorisieren.
"""
    write(DOC, doc)

    audit = "# B167 sticky zoom state repair audit\n\n"
    audit += f"Date: {today}\n\n"
    audit += f"Old prototype existed: {old_exists}\n"
    audit += f"Old prototype already contained density map: {old_contains_density}\n"
    audit += f"Old prototype had regional Germany overlay pattern: {old_regional_germany_overlay}\n\n"
    audit += "Step audit:\n"
    for line in step_audit:
        audit += f"- {line}\n"

    new_text = read(PROTOTYPE)
    audit += "\nPost-patch checks:\n"
    audit += f"- density map in prototype: {'global_hotspots_density.png' in new_text}\n"
    audit += f"- global-pressure-total state in prototype: {'global-pressure-total' in new_text}\n"
    audit += f"- global-pressure-density state in prototype: {'global-pressure-density' in new_text}\n"
    audit += f"- oberschwaben-handoff state in prototype: {'oberschwaben-handoff' in new_text}\n"
    audit += f"- regional-handoff state removed: {'regional-handoff' not in new_text}\n"
    audit += f"- Germany overlay tied to oberschwaben-handoff: {('data-b165-boundary=\"oberschwaben-handoff\"' in new_text and 'germany_admin_context.png' in new_text)}\n"
    audit += "\nResult: PROTOTYPE PATCH WRITTEN. No public page files changed.\n"
    write(AUDIT, audit)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B167 sticky zoom state repair complete.")
    print("Changed:")
    print("  docs/prototypes/B165_flagship_sticky_zoom_prototype.html")
    print("Created/updated:")
    print("  docs/B167_sticky_zoom_state_repair.md")
    print("  docs/B167_sticky_zoom_state_matrix_repaired.csv")
    print("  docs/B167_sticky_zoom_state_repair_audit.txt")
    print("  tasks/done.md")
    print("Next: open prototype locally and review.")


if __name__ == "__main__":
    main()
