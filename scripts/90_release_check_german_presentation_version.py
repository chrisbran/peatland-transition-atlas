#!/usr/bin/env python3
"""
B90 - Release check German presentation version

Purpose:
- Check the German presentation version after B79-B89.
- Replace the outdated B72 interpretation of "guidedStory missing = fail" with
  a German-presentation-aware release check.
- Confirm that the public-facing MVP v0.1 has the required structure:
  compact header, German hero, central map story, BW/BK50 endpoint,
  implementation/pathway/method boundary sections, and JS guards.
- Produce a release report and a public review checklist.
- Do not modify application files.

Outputs:
- docs/B90_release_check_german_presentation_version.md
- docs/B90_public_review_checklist.md
- tasks/done.md

Does NOT:
- modify index.html
- modify src/styles.css
- modify JavaScript
- alter maps/data/assets
- replace B72
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
APP = ROOT / "src" / "app.js"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"

REPORT = DOCS / "B90_release_check_german_presentation_version.md"
CHECKLIST = DOCS / "B90_public_review_checklist.md"

REQUIRED_MAPS = [
    "public/maps/global/global_gpm2_peat_extent.png",
    "public/maps/global/global_hotspots_total.png",
    "public/maps/global/global_hotspots_density.png",
    "public/maps/global/global_country_borders.png",
    "public/maps/europe/europe_gpm2_peat_extent.png",
    "public/maps/europe/europe_country_borders.png",
    "public/maps/germany/germany_admin_context.png",
    "public/maps/germany/germany_thuenen_moor_extent.png",
    "public/maps/germany/germany_thuenen_moor_types.png",
    "public/maps/bw/bw_admin_context.png",
    "public/maps/bw/bw_bk50_moor_extent.png",
]

REQUIRED_STATES = [
    "extent",
    "total",
    "density",
    "compare",
    "europe-borders",
    "europe-peat",
    "germany-context",
    "germany-thuenen-extent",
    "germany-thuenen-types",
    "bw-context",
    "bw-bk50-extent",
]

FORBIDDEN_MAIN_VISIBLE_TERMS = [
    "PORTFOLIO PROTOTYPE",
    "LITERATURE-DRIVEN MVP",
    "Peatland Transition Atlas",
    "Mapping the space between drainage-based agriculture",
    "Evidence Map",
    "South Germany Fit",
    "Prototype appendix",
    "Supporting evidence",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git_status_short() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return [f"git status failed: {result.stderr.strip()}"]
        return result.stdout.splitlines()
    except Exception as exc:
        return [f"git status failed: {exc}"]


def check(condition: bool, label: str, ok: str, fail: str, failures: list[str], warnings: list[str], results: list[str], warning: bool = False):
    if condition:
        results.append(f"- OK   `{label}` — {ok}")
    else:
        if warning:
            warnings.append(f"{label}: {fail}")
            results.append(f"- WARN `{label}` — {fail}")
        else:
            failures.append(f"{label}: {fail}")
            results.append(f"- FAIL `{label}` — {fail}")


def visible_german_presentation_active(html: str) -> bool:
    markers = [
        "Moorschutz braucht räumliche Orientierung",
        "b79RegionalImplementation",
        "b79Pathways",
        "b79MethodBoundary",
        "b88-step-card",
        "data-b87-central-story",
    ]
    return sum(1 for m in markers if m in html) >= 4


def extract_local_refs(html: str) -> list[str]:
    refs = []
    for attr in ["src", "href"]:
        for m in re.finditer(rf'\b{attr}\s*=\s*(["\'])(.*?)\1', html, flags=re.IGNORECASE):
            ref = m.group(2).strip()
            if not ref or ref.startswith("#"):
                continue
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            if ref.startswith("//"):
                continue
            # remove query/hash
            ref = ref.split("#", 1)[0].split("?", 1)[0]
            if ref:
                refs.append(ref)
    return refs


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX) if INDEX.exists() else ""
    css = read(CSS) if CSS.exists() else ""
    app = read(APP) if APP.exists() else ""

    failures: list[str] = []
    warnings: list[str] = []
    results: list[str] = []

    active = visible_german_presentation_active(html)

    check(INDEX.exists(), "index.html", "exists", "missing", failures, warnings, results)
    check(CSS.exists(), "src/styles.css", "exists", "missing", failures, warnings, results)
    check(APP.exists(), "src/app.js", "exists", "missing", failures, warnings, results)

    check(
        active,
        "German presentation mode",
        "B79-B89 markers detected",
        "German presentation markers missing",
        failures,
        warnings,
        results,
    )

    check(
        '<html lang="de"' in html or "<html lang='de'" in html,
        "HTML language",
        "lang=de present",
        "html lang=de missing",
        failures,
        warnings,
        results,
        warning=True,
    )

    check(
        "Moorschutz braucht räumliche Orientierung" in html,
        "German hero title",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )

    check(
        "MOORE · KLIMASCHUTZ · REGIONALE UMSETZUNG" in html or "Moore · Klimaschutz · regionale Umsetzung" in html,
        "German hero kicker",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )

    for nav_label in ["Problem", "Kartenfolge", "Umsetzung", "Pfade", "Methode"]:
        check(
            f">{nav_label}<" in html,
            f"nav label {nav_label}",
            "present",
            "missing",
            failures,
            warnings,
            results,
        )

    # Central story should be targetable again.
    check(
        'id="centralGlobalMapStory"' in html or "id='centralGlobalMapStory'" in html,
        "central story canonical id",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )
    check(
        'data-b87-central-story="true"' in html or "data-b87-central-story='true'" in html,
        "central story stable data attribute",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )
    check(
        "central-map-story" in html,
        "central story class",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )

    # Step cards and states.
    step_card_count = html.count("b88-step-card")
    check(
        step_card_count >= 11,
        "central step cards",
        f"{step_card_count} b88-step-card markers",
        f"only {step_card_count} b88-step-card markers",
        failures,
        warnings,
        results,
    )

    for state in REQUIRED_STATES:
        check(
            f'data-global-state="{state}"' in html or f"data-global-state='{state}'" in html,
            f"central state {state}",
            "present",
            "missing",
            failures,
            warnings,
            results,
        )

    # New lower German sections.
    for section_id in ["b79RegionalImplementation", "b79Pathways", "b79MethodBoundary"]:
        check(
            f'id="{section_id}"' in html or f"id='{section_id}'" in html,
            f"section #{section_id}",
            "present",
            "missing",
            failures,
            warnings,
            results,
        )

    boundary = "Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung"
    check(
        boundary in html,
        "method boundary sentence",
        "present",
        "missing",
        failures,
        warnings,
        results,
    )

    # guidedStory: under B90 absence is acceptable if German presentation mode is active.
    guided_present = 'id="guidedStory"' in html or "id='guidedStory'" in html
    if guided_present:
        guided_ok = ("data-retired" in html and "guidedStory" in html) or "is-retired" in html
        check(
            guided_ok,
            "#guidedStory retired if present",
            "present and apparently retired",
            "present but retirement marker not detected",
            failures,
            warnings,
            results,
            warning=True,
        )
    else:
        check(
            active,
            "#guidedStory",
            "absent; accepted because German presentation mode is active",
            "missing while German presentation mode is not detected",
            failures,
            warnings,
            results,
        )

    # TextContent guard in app.js.
    check(
        "__b83TextTarget" in app or "__b84TextTarget" in app or "?.textContent" in app,
        "app metric selector guard",
        "guard detected",
        "no guard detected; red error may return if metric DOM nodes are absent",
        failures,
        warnings,
        results,
    )

    # CSS marker stack.
    for marker in [
        "B79 German presentation version",
        "B82 compact header and overflow fix",
        "B84 harden central map story panels",
        "B87 central story id restore",
        "B88 wrap central story step cards",
        "B89 force uniform central step card state",
    ]:
        check(
            marker in css,
            f"CSS marker: {marker}",
            "present",
            "missing",
            failures,
            warnings,
            results,
            warning=True,
        )

    # Required maps exist.
    for m in REQUIRED_MAPS:
        check(
            (ROOT / m).exists(),
            m,
            "exists",
            "missing",
            failures,
            warnings,
            results,
        )

    # Broken local refs.
    broken_refs = []
    for ref in extract_local_refs(html):
        # Ignore anchors to generated docs or paths outside deployment only if necessary.
        if ref.startswith("../"):
            candidate = (ROOT / ref).resolve()
        else:
            candidate = ROOT / ref
        if not candidate.exists():
            broken_refs.append(ref)

    check(
        not broken_refs,
        "local src/href references",
        "no broken local references detected",
        "broken local references: " + ", ".join(broken_refs[:12]),
        failures,
        warnings,
        results,
    )

    # Forbidden visible old meta terms. Since hidden docs/scripts may still contain terms,
    # this only checks index.html. Terms in comments are still reported as warning, not fail.
    found_terms = [t for t in FORBIDDEN_MAIN_VISIBLE_TERMS if t in html]
    check(
        not found_terms,
        "old English/meta terms in index.html",
        "none detected",
        "terms detected: " + ", ".join(found_terms),
        failures,
        warnings,
        results,
        warning=True,
    )

    # Git hygiene warnings.
    status = git_status_short()
    for line in status:
        if line.startswith("?? data/") or line.startswith("?? data\\"):
            warnings.append(f"{line} visible in git status")
        if line.startswith("?? data/external"):
            warnings.append(f"{line} raw/external data visible")
        if line.startswith("??") and any(s in line for s in [".shp", ".dbf", ".prj", ".tif", ".tiff", ".gpkg"]):
            warnings.append(f"{line} GIS/raw-data-like untracked file visible")

    result = "PASS" if not failures else "FAIL"
    if result == "PASS" and warnings:
        result = "PASS WITH WARNINGS"

    public_url = "https://chrisbran.github.io/peatland-transition-atlas/?v=" + quote(f"b90-{today}")

    report = f"""# B90 - Release Check German Presentation Version

Date: {today}

## 1. Result

**{result}**

## 2. Purpose

B90 is the release check for the German presentation version after B79-B89.

It replaces the outdated B72 assumption that a missing `#guidedStory` is always a failure. In the German presentation version, `#guidedStory` may be absent if the new B79/B87/B88 structure is active.

## 3. Check results

{chr(10).join(results)}

## 4. Failures

{chr(10).join(f"- {f}" for f in failures) if failures else "- none"}

## 5. Warnings

{chr(10).join(f"- {w}" for w in warnings) if warnings else "- none"}

## 6. Public URL for review

Use a cache-busted URL:

`{public_url}`

## 7. Git status snapshot

```text
{chr(10).join(status) if status else "clean"}
```

## 8. Release interpretation

A B90 `PASS WITH WARNINGS` is acceptable if warnings are limited to known untracked raw-data/workflow files or old documentation artefacts.

It is not acceptable if there are failures for:

- central map states,
- BW map assets,
- method boundary,
- broken references,
- missing app selector guards.
"""
    write(REPORT, report)

    checklist = f"""# B90 - Public Review Checklist

Date: {today}

Public URL:

`{public_url}`

## Manual browser check

Open the URL in a fresh browser tab or incognito window.

### Header and hero

- [ ] Header is compact: `Moorschutz | Problem | Kartenfolge | Umsetzung | Pfade | Methode`
- [ ] No red error bar appears.
- [ ] Hero title is German: `Moorschutz braucht räumliche Orientierung`
- [ ] No visible `Portfolio prototype`, `MVP`, `Peatland Transition Atlas`, or English hero lead.

### Central map story

- [ ] The central map appears after the argument section.
- [ ] Step 01 is dark and readable.
- [ ] Steps 02-11 are dark immediately when visible.
- [ ] No cards change from grey to dark at an activation threshold.
- [ ] No large dark blocks/columns appear on the left.
- [ ] Map state changes are visible while scrolling.
- [ ] Europe, Germany and Baden-Württemberg frames appear.
- [ ] BW/BK50 endpoint appears.

### Lower German sections

- [ ] `Regionale Umsetzung` appears.
- [ ] `Transformationspfade` appears.
- [ ] `Einordnung statt Eignungskarte` appears.
- [ ] Method boundary sentence is visible.

### Presentation readiness

- [ ] Page can be explained in 3-5 minutes.
- [ ] No obvious English/meta prototype language in the main flow.
- [ ] No broken images.
- [ ] No browser console/runtime error is visible in the page.

## Suggested release label

`German presentation version v0.1`
"""
    write(CHECKLIST, checklist)

    done_entry = f"""
## B90 - Release check German presentation version ({today})

- Created `docs/B90_release_check_german_presentation_version.md`.
- Created `docs/B90_public_review_checklist.md`.
- Checked German presentation structure, central states, map assets, app selector guard and method boundary.
- Treated missing `#guidedStory` as acceptable when German presentation mode is active.
- Did not modify application files, CSS, JavaScript, maps or data.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B90 - Release check German presentation version" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B90 release check German presentation version complete.")
    print(f"Result: {result}")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("Warnings:")
        for w in warnings[:12]:
            print(f"  - {w}")
        if len(warnings) > 12:
            print(f"  ... {len(warnings) - 12} more warnings")
    print("Changed/created:")
    print(f"  {rel(REPORT)}")
    print(f"  {rel(CHECKLIST)}")
    print(f"  {rel(DONE)}")
    print(f"Public review URL: {public_url}")


if __name__ == "__main__":
    main()
