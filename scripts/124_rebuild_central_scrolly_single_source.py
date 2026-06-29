#!/usr/bin/env python3
# B124 - Rebuild central scrolly single source
# Replaces the fragile central map-story runtime with one deterministic controller.

from __future__ import annotations

from datetime import date
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b124_central_scrolly_single_source"

CENTRAL = SRC / "central_global_map_story.js"
HARDENER = SRC / "central_layer_state_hardener.js"
BRIDGE = SRC / "central_step_state_bridge.js"
LABEL_FIX = SRC / "central_stage_label_fix.js"

REPORT = DOCS / "B124_rebuild_central_scrolly_single_source.md"
AUDIT = DOCS / "B124_central_scrolly_single_source_audit.txt"
TODAY = date.today().isoformat()

CENTRAL_JS = r"""/*
 * B124 - Central map story single-source controller.
 * Owns step selection, labels, source text and PNG layer opacity for
 * #centralGlobalMapStory. Historic helper scripts are retired as no-ops.
 */
(function () {
  "use strict";

  const STORY_SELECTOR = "#centralGlobalMapStory";
  const STEP_SELECTOR = ".central-map-step[data-global-state], article[data-global-state]";

  const LAYERS = [
    "layer-gpm",
    "layer-total",
    "layer-density",
    "layer-borders",
    "layer-europe-borders",
    "layer-europe-peat",
    "layer-germany-admin",
    "layer-germany-thuenen-extent",
    "layer-germany-thuenen-types",
    "layer-bw-admin",
    "layer-bw-bk50-extent"
  ];

  const STATES = {
    "extent": {
      mode: "Globale Moorverbreitung",
      title: "Moore sind räumlich stark konzentriert.",
      legend: '<span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Daten: Global Peatland Map 2.0; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.96, "layer-borders": 0.62 }
    },
    "total": {
      mode: "Emissionsdruck",
      title: "Gesamtemissionen zeigen, wo die größten bilanziellen Hotspots liegen.",
      legend: '<span><i class="legend-total"></i>höhere Gesamtemissionen</span><span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Daten: FAOSTAT, Gesamtemissionen aus drainierten organischen Böden; Global Peatland Map 2.0 als Kontext; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.48, "layer-total": 0.92, "layer-borders": 0.84 }
    },
    "density": {
      mode: "Emissionsdichte",
      title: "Emissionsdichte zeigt, wo der Druck relativ zur Fläche besonders hoch ist.",
      legend: '<span><i class="legend-density"></i>höhere Emissionsdichte</span><span><i class="legend-peat"></i>Moorkontext</span>',
      source: "Daten: FAOSTAT, flächenbezogene Emissionsdichte aus drainierten organischen Böden; Global Peatland Map 2.0 als Kontext; eigene kartografische Aufbereitung.",
      layers: { "layer-gpm": 0.48, "layer-density": 0.92, "layer-borders": 0.86 }
    },
    "compare": {
      mode: "Lesart",
      title: "Größe und Intensität müssen getrennt gelesen werden.",
      legend: '<span><i class="legend-density"></i>Emissionsdichte</span><span><i class="legend-border"></i>Ländergrenzen</span>',
      source: "Lesart: Gesamtmenge und Emissionsdichte beantworten unterschiedliche Fragen und dürfen nicht vermischt werden.",
      layers: { "layer-gpm": 0.56, "layer-density": 0.88, "layer-borders": 0.90 }
    },
    "europe-borders": {
      mode: "Europa",
      title: "Politische Grenzen bestimmen Planung und Förderung.",
      legend: '<span><i class="legend-border"></i>Europäische Ländergrenzen</span>',
      source: "Daten: GISCO-Ländergrenzen; eigene kartografische Aufbereitung.",
      layers: { "layer-europe-borders": 0.98 }
    },
    "europe-peat": {
      mode: "Europäischer Moorkontext",
      title: "Moorvorkommen überschreiten Verwaltungsgrenzen.",
      legend: '<span><i class="legend-peat"></i>Moorkontext</span><span><i class="legend-border"></i>Europäische Ländergrenzen</span>',
      source: "Daten: Global Peatland Map 2.0; Darstellung im europäischen Kartenrahmen.",
      layers: { "layer-europe-peat": 0.98, "layer-europe-borders": 0.88 }
    },
    "germany-context": {
      mode: "Deutschland",
      title: "Deutschland zeigt, wo Planung und Förderung ansetzen.",
      legend: '<span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Daten: GISCO NUTS 1 / Bundesländer; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-admin": 0.98 }
    },
    "germany-thuenen-extent": {
      mode: "Organische Böden",
      title: "Die Thünen-Kulisse zeigt organische Böden.",
      legend: '<span><i class="legend-peat"></i>Thünen-Kulisse organischer Böden</span><span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Daten: Thünen-Kulisse organischer Böden; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-thuenen-extent": 0.98, "layer-germany-admin": 0.86 }
    },
    "germany-thuenen-types": {
      mode: "Moor- und Bodentypen",
      title: "Der Bodenkontext begrenzt, was möglich ist.",
      legend: '<span><i class="legend-peat"></i>Moor- und Bodentypen</span><span><i class="legend-border"></i>Bundesländer-Kontext</span>',
      source: "Daten: Thünen-Kulisse organischer Böden; Bodentypen nach KAT_LANG; eigene kartografische Aufbereitung.",
      layers: { "layer-germany-thuenen-types": 0.98, "layer-germany-admin": 0.84 }
    },
    "bw-context": {
      mode: "Baden-Württemberg",
      title: "Baden-Württemberg macht die Frage räumlich konkret.",
      legend: '<span><i class="legend-border"></i>Regionaler Kartenrahmen</span>',
      source: "Baden-Württemberg: regionaler Kartenrahmen; eigene kartografische Aufbereitung.",
      layers: { "layer-bw-admin": 0.98 }
    },
    "bw-bk50-extent": {
      mode: "BK50",
      title: "Die BK50 ordnet Moor- und Feuchtbodenkontexte ein.",
      legend: '<span><i class="legend-peat"></i>BK50 Moor-/Feuchtbodenkontext</span><span><i class="legend-border"></i>Regionaler Kartenrahmen</span>',
      source: "Daten: BK50 Moor-/Feuchtbodenkontext; eigene Auswahl und kartografische Aufbereitung.",
      layers: { "layer-bw-bk50-extent": 0.98, "layer-bw-admin": 0.86 }
    }
  };

  let story = null;
  let steps = [];
  let activeState = null;
  let ticking = false;

  function setText(id, value, html) {
    const el = document.getElementById(id);
    if (!el) return;
    if (html) el.innerHTML = value || "";
    else el.textContent = value || "";
  }

  function applyLayers(meta) {
    LAYERS.forEach((className, index) => {
      const opacity = meta.layers && Object.prototype.hasOwnProperty.call(meta.layers, className)
        ? meta.layers[className]
        : 0;
      document.querySelectorAll(STORY_SELECTOR + " ." + className).forEach((el) => {
        el.style.setProperty("opacity", String(opacity), "important");
        el.style.setProperty("visibility", opacity > 0 ? "visible" : "hidden", "important");
        el.style.setProperty("pointer-events", "none", "important");
        el.style.setProperty("z-index", String(10 + index), "important");
      });
    });
  }

  function applyState(state, reason) {
    if (!story || !STATES[state]) return;
    if (activeState === state && reason !== "force") return;

    activeState = state;
    const meta = STATES[state];

    story.setAttribute("data-state", state);
    story.setAttribute("data-b124-active-state", state);

    steps.forEach((step) => {
      const isActive = step.getAttribute("data-global-state") === state;
      step.classList.toggle("is-active", isActive);
      step.classList.toggle("is-current", isActive);
      if (isActive) step.setAttribute("aria-current", "step");
      else step.removeAttribute("aria-current");
    });

    setText("centralMapMode", meta.mode, false);
    setText("centralMapTitle", meta.title, false);
    setText("centralMapLegend", meta.legend, true);
    setText("centralMapSource", meta.source, false);
    applyLayers(meta);
  }

  function storyInRange() {
    if (!story) return false;
    const r = story.getBoundingClientRect();
    return r.bottom > 0 && r.top < window.innerHeight;
  }

  function pickStateFromViewport() {
    if (!steps.length) return null;
    const targetY = window.innerHeight * 0.46;
    let best = null;
    let bestScore = Infinity;

    steps.forEach((step) => {
      const rect = step.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const visible = rect.bottom >= 0 && rect.top <= window.innerHeight;
      const distance = Math.abs(center - targetY);
      const penalty = visible ? 0 : window.innerHeight;
      const score = distance + penalty;
      if (score < bestScore) {
        bestScore = score;
        best = step;
      }
    });

    return best ? best.getAttribute("data-global-state") : null;
  }

  function updateFromScroll() {
    ticking = false;
    if (!storyInRange()) return;
    const state = pickStateFromViewport();
    if (state) applyState(state, "scroll");
  }

  function scheduleUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateFromScroll);
  }

  function bindStepInteractions() {
    steps.forEach((step) => {
      const state = step.getAttribute("data-global-state");
      if (!state || !STATES[state]) return;
      step.addEventListener("mouseenter", () => applyState(state, "hover"));
      step.addEventListener("focusin", () => applyState(state, "focus"));
      step.addEventListener("click", () => applyState(state, "click"));
    });
  }

  function init() {
    story = document.querySelector(STORY_SELECTOR);
    if (!story) return;

    steps = Array.from(story.querySelectorAll(STEP_SELECTOR))
      .filter((step) => STATES[step.getAttribute("data-global-state")]);

    if (!steps.length) return;

    bindStepInteractions();

    const initial = story.getAttribute("data-state") || steps[0].getAttribute("data-global-state") || "extent";
    applyState(STATES[initial] ? initial : "extent", "force");
    scheduleUpdate();

    window.addEventListener("scroll", scheduleUpdate, { passive: true });
    window.addEventListener("resize", scheduleUpdate, { passive: true });

    window.__centralMapStoryB124 = {
      states: Object.keys(STATES),
      applyState,
      get activeState() { return activeState; }
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
"""

NOOPS = {
    "central_layer_state_hardener.js": """/*
 * B124 - retired central layer state hardener.
 * Layer visibility is now owned by src/central_global_map_story.js.
 */
(function () { window.__centralLayerStateHardenerRetired = true; })();
""",
    "central_step_state_bridge.js": """/*
 * B124 - retired central step state bridge.
 * Step-to-map state selection is now owned by src/central_global_map_story.js.
 */
(function () { window.__centralStepStateBridgeRetired = true; })();
""",
    "central_stage_label_fix.js": """/*
 * B124 - retired central stage label fixer.
 * Mode, title, legend and source are now owned by src/central_global_map_story.js.
 */
(function () { window.__centralStageLabelFixRetired = true; })();
""",
}

RISK_PATTERNS = [
    "GLOBAL_FRAME_V1", "EUROPE_FRAME_V1", "Country hotspot layer:", "GPM context underneath",
    "same ArcGIS frame", "Europe frame:", "Germany frame:", "BW frame:", "Baden-Wuerttemberg",
    "ArcGIS", "Peatland context", "Peat in soil mosaic", "Higher total emissions",
    "Higher emission density", "Emission density view", "European country borders",
    "Federal-state context", "Thuenen", "TOTAL EMISSIONS", "EMISSION DENSITY",
    "INTERPRETATION", "Ã", "�"
]

REQUIRED_STATES = [
    "extent", "total", "density", "compare", "europe-borders", "europe-peat",
    "germany-context", "germany-thuenen-extent", "germany-thuenen-types",
    "bw-context", "bw-bk50-extent"
]

REQUIRED_PUBLIC_STRINGS = [
    "Daten: Global Peatland Map 2.0",
    "Daten: FAOSTAT, Gesamtemissionen",
    "Daten: FAOSTAT, flächenbezogene Emissionsdichte",
    "Daten: GISCO-Ländergrenzen",
    "Daten: GISCO NUTS 1 / Bundesländer",
    "Daten: Thünen-Kulisse organischer Böden",
    "Baden-Württemberg: regionaler Kartenrahmen",
    "Daten: BK50 Moor-/Feuchtbodenkontext",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def backup(path: Path) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / rel(path).replace("/", "__").replace("\\", "__")
    if path.exists() and not dest.exists():
        shutil.copy2(path, dest)


def write_runtime() -> None:
    backup(CENTRAL)
    write_text(CENTRAL, CENTRAL_JS)
    for filename, content in NOOPS.items():
        path = SRC / filename
        if path.exists():
            backup(path)
            write_text(path, content)


def scan_runtime() -> dict[str, object]:
    files = [CENTRAL, HARDENER, BRIDGE, LABEL_FIX]
    runtime = "\n".join(read_text(p) for p in files if p.exists())
    central = read_text(CENTRAL) if CENTRAL.exists() else ""

    risk_counts = {p: runtime.count(p) for p in RISK_PATTERNS}
    state_counts = {p: central.count(p) for p in REQUIRED_STATES}
    public_counts = {p: central.count(p) for p in REQUIRED_PUBLIC_STRINGS}

    helper_counts = {}
    for p in [HARDENER, BRIDGE, LABEL_FIX]:
        txt = read_text(p) if p.exists() else ""
        helper_counts[rel(p) + ":IntersectionObserver"] = txt.count("IntersectionObserver")
        helper_counts[rel(p) + ":MutationObserver"] = txt.count("MutationObserver")
        helper_counts[rel(p) + ":data-state"] = txt.count("data-state")

    return {
        "risk_counts": risk_counts,
        "state_counts": state_counts,
        "public_counts": public_counts,
        "helper_counts": helper_counts,
        "risk_findings": sum(1 for v in risk_counts.values() if v > 0),
        "missing_states": sum(1 for v in state_counts.values() if v == 0),
        "missing_public_strings": sum(1 for v in public_counts.values() if v == 0),
        "active_helper_observers": sum(helper_counts.values()),
    }


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B124 - Rebuild central scrolly single source"
    if marker in current:
        return
    entry = f"""
## B124 - Rebuild central scrolly single source ({TODAY})

- Rebuilt `src/central_global_map_story.js` as the only active controller for the central scrolly map sequence.
- Retired `central_layer_state_hardener.js`, `central_step_state_bridge.js` and `central_stage_label_fix.js` as no-op files.
- Centralized step-to-layer, title, legend and source text in one state table.
- Did not modify maps, data, HTML structure or CSS.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def write_docs(result: dict[str, object]) -> None:
    status = (
        "OK"
        if result["risk_findings"] == 0
        and result["missing_states"] == 0
        and result["missing_public_strings"] == 0
        and result["active_helper_observers"] == 0
        else "REVIEW REQUIRED"
    )

    report = [
        "# B124 – Rebuild Central Scrolly Single Source",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B124 ersetzt die fragile zentrale Kartensteuerung durch einen einzelnen Controller mit einer einzigen State-Tabelle.",
        "",
        "## Architektur",
        "",
        "- aktiv: `src/central_global_map_story.js`",
        "- no-op: `src/central_layer_state_hardener.js`",
        "- no-op: `src/central_step_state_bridge.js`",
        "- no-op: `src/central_stage_label_fix.js`",
        "",
        "## Audit summary",
        "",
        f"- Risk findings: {result['risk_findings']}",
        f"- Missing states: {result['missing_states']}",
        f"- Missing public strings: {result['missing_public_strings']}",
        f"- Active helper observer/data-state hits: {result['active_helper_observers']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B124_central_scrolly_single_source_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\*.js,src\\*.css -Pattern \"GLOBAL_FRAME_V1\",\"Country hotspot layer\",\"Peatland context\",\"Thuenen\",\"ArcGIS\",\"BW frame\",\"Daten: FAOSTAT\",\"Daten: GISCO\",\"Daten: Thünen\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ]
    write_text(REPORT, "\n".join(report))

    audit = [
        "# B124 central scrolly single-source audit",
        "",
        f"- Status: {status}",
        f"- Risk findings: {result['risk_findings']}",
        f"- Missing states: {result['missing_states']}",
        f"- Missing public strings: {result['missing_public_strings']}",
        f"- Active helper observer/data-state hits: {result['active_helper_observers']}",
        "",
        "## Risk counts",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ]
    for p, c in result["risk_counts"].items():
        audit.append(f"| `{p}` | {c} |")

    audit.extend(["", "## State counts", "", "| State | Count |", "|---|---:|"])
    for p, c in result["state_counts"].items():
        audit.append(f"| `{p}` | {c} |")

    audit.extend(["", "## Public string counts", "", "| String | Count |", "|---|---:|"])
    for p, c in result["public_counts"].items():
        audit.append(f"| `{p}` | {c} |")

    audit.extend(["", "## Retired helper counts", "", "| Check | Count |", "|---|---:|"])
    for p, c in result["helper_counts"].items():
        audit.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit))


def main() -> None:
    if not CENTRAL.exists():
        print(f"Missing {rel(CENTRAL)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    write_runtime()
    update_done()
    result = scan_runtime()
    write_docs(result)

    ok = (
        result["risk_findings"] == 0
        and result["missing_states"] == 0
        and result["missing_public_strings"] == 0
        and result["active_helper_observers"] == 0
    )

    print("B124 central scrolly single-source rebuild complete.")
    print("Changed/created:")
    for p in [CENTRAL, HARDENER, BRIDGE, LABEL_FIX, REPORT, AUDIT, DONE]:
        if p.exists():
            print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Risk findings: {result['risk_findings']}")
    print(f"Missing states: {result['missing_states']}")
    print(f"Missing public strings: {result['missing_public_strings']}")
    print(f"Active helper observer/data-state hits: {result['active_helper_observers']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B124_central_scrolly_single_source_audit.txt -Encoding UTF8")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
