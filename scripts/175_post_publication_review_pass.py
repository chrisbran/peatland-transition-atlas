from pathlib import Path
from datetime import date
import re
import csv
import subprocess
from html import unescape

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"

SCRIPT = ROOT / "scripts" / "175_post_publication_review_pass.py"
DOC = ROOT / "docs" / "B175_post_publication_review_pass.md"
AUDIT = ROOT / "docs" / "B175_post_publication_review_pass_audit.txt"
SECTION_CSV = ROOT / "docs" / "B175_section_inventory.csv"
CANDIDATES_CSV = ROOT / "docs" / "B175_review_candidates.csv"
CHECKLIST = ROOT / "docs" / "B175_publication_review_checklist.md"
DONE = ROOT / "tasks" / "done.md"

PUBLIC_URL = "https://chrisbran.github.io/peatland-transition-atlas/"

REQUIRED_SIGNALS = [
    ("v2_scope_box", "Fachlicher Demonstrator"),
    ("b169_live_zoom", "B169_LIVE_STICKY_ZOOM_START"),
    ("oberschwaben_no_label_map", "oberschwaben_landkreise_moor_nolabel.png"),
    ("b170_handoff", "Bis hierher ging es um Maßstab und Bodenkontext"),
    ("value_chain_climax", "Bis zur Ernte ist vieles anschlussfähig"),
    ("method_short", "Methode in Kürze"),
    ("sources_rights", "Datengrundlagen, Rechte und Quellenvermerke"),
    ("impressum_privacy", "Impressum · Datenschutz"),
    ("v2_public_tag_hint", "Stand: Juni 2026"),
]

REVIEW_TERMS = [
    ("Warn-/Caveat-Dichte", r"keine\s+Eignungskarte|keine\s+Priorisierung|keine\s+hydrologische\s+Modellierung|Standortprüfung|Einzelfallprüfung|Prüfbedarf"),
    ("Methode/Quelle-Dichte", r"Methode\s+in\s+Kürze|Datenbasis:|Grundlagen:|Quellenbasis|Datengrundlage|Rechte"),
    ("Wertschöpfungs-Dichte", r"Wertschöpfung|Abnahme|Verarbeitung|Standards|Markt|Logistik"),
    ("Transformations-Dichte", r"Transformation|Transformationspfad|Pfad|Nutzungswechsel"),
    ("Oberschwaben-Dichte", r"Oberschwaben|Biberach|Ravensburg|Sigmaringen|Bodenseekreis"),
]

SECTION_RE = re.compile(r"<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>", re.I | re.S)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git"] + args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def clean_html_text(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def attr_value(attrs: str, name: str) -> str:
    m = re.search(name + r'\s*=\s*"([^"]+)"', attrs, flags=re.I)
    if m:
        return m.group(1)
    m = re.search(name + r"\s*=\s*'([^']+)'", attrs, flags=re.I)
    if m:
        return m.group(1)
    return ""


def first_heading(body: str) -> str:
    m = re.search(r"<h[1-4]\b[^>]*>(.*?)</h[1-4]>", body, flags=re.I | re.S)
    if not m:
        return ""
    return clean_html_text(m.group(1))


def first_kicker(body: str) -> str:
    # Common project pattern: first short paragraph before heading.
    m = re.search(r'<p\b[^>]*class="[^"]*(?:kicker|eyebrow|section-kicker)[^"]*"[^>]*>(.*?)</p>', body, flags=re.I | re.S)
    if m:
        return clean_html_text(m.group(1))
    return ""


def section_inventory(html: str) -> list[dict]:
    rows = []
    for i, m in enumerate(SECTION_RE.finditer(html), start=1):
        attrs = m.group("attrs")
        body = m.group("body")
        text = clean_html_text(body)
        words = text.split()
        section_id = attr_value(attrs, "id")
        classes = attr_value(attrs, "class")
        heading = first_heading(body)
        kicker = first_kicker(body)
        rows.append({
            "order": i,
            "id": section_id,
            "class": classes,
            "kicker": kicker,
            "heading": heading,
            "word_count": len(words),
            "snippet": text[:220],
        })
    return rows


def candidate_rows(html: str, sections: list[dict]) -> list[dict]:
    text = clean_html_text(html)
    rows = []

    # Term density candidates.
    for label, pattern in REVIEW_TERMS:
        matches = re.findall(pattern, text, flags=re.I)
        rows.append({
            "type": "term_density",
            "severity": "review" if len(matches) >= 8 else "ok",
            "label": label,
            "count": len(matches),
            "detail": "High count can be fine, but review for repetition/caveat fatigue." if len(matches) >= 8 else "No immediate concern.",
        })

    # Long sections.
    for s in sections:
        wc = int(s["word_count"])
        if wc >= 650:
            rows.append({
                "type": "long_section",
                "severity": "review",
                "label": s["heading"] or s["id"] or f"section {s['order']}",
                "count": wc,
                "detail": "Long section; review whether it should be compressed or split.",
            })

    # Repeated headings.
    headings = {}
    for s in sections:
        h = s["heading"].strip()
        if not h:
            continue
        headings.setdefault(h.lower(), {"heading": h, "count": 0})
        headings[h.lower()]["count"] += 1

    for item in headings.values():
        if item["count"] > 1:
            rows.append({
                "type": "repeated_heading",
                "severity": "review",
                "label": item["heading"],
                "count": item["count"],
                "detail": "Repeated heading may be intentional, but review for orientation.",
            })

    # Publication-release checks.
    for key, signal in REQUIRED_SIGNALS:
        found = signal in html
        rows.append({
            "type": "release_signal",
            "severity": "ok" if found else "fail",
            "label": key,
            "count": 1 if found else 0,
            "detail": f"Signal `{signal}` {'found' if found else 'missing'}.",
        })

    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def update_done(done_text: str, today: str) -> str:
    line = f"- B175 post-publication review pass: created an audit-only inventory, review-candidate list and manual QA checklist for the newly published V2 page ({today})."
    if "B175 post-publication review pass" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    css = read(CSS)

    branch = run_git(["branch", "--show-current"])
    head = run_git(["log", "--oneline", "--decorate", "-n", "1"])
    tags_at_head = run_git(["tag", "--points-at", "HEAD"])
    status = run_git(["status", "--short"])

    sections = section_inventory(html)
    candidates = candidate_rows(html, sections)

    write_csv(
        SECTION_CSV,
        sections,
        ["order", "id", "class", "kicker", "heading", "word_count", "snippet"],
    )
    write_csv(
        CANDIDATES_CSV,
        candidates,
        ["type", "severity", "label", "count", "detail"],
    )

    fail_candidates = [r for r in candidates if r["severity"] == "fail"]
    review_candidates = [r for r in candidates if r["severity"] == "review"]
    ok_candidates = [r for r in candidates if r["severity"] == "ok"]

    top_sections = sorted(sections, key=lambda r: int(r["word_count"]), reverse=True)[:8]

    checklist = f"""# B175 - Publication Review Checklist

Date: {today}

Public URL:

```text
{PUBLIC_URL}
```

## Manual visual check

### Desktop, approx. 1440 px

- [ ] Hero loads without layout jump
- [ ] Scope box is visible but not dominant
- [ ] B169 sticky zoom scrolls through all 8 states
- [ ] Oberschwaben no-label map appears in the final B169 state
- [ ] Transition after sticky zoom feels intentional
- [ ] Oberschwaben detail section clearly adds current land use
- [ ] Felt link/embed section is understandable
- [ ] Value-chain scorecard is visually readable
- [ ] Footer/source section opens and remains readable

### Mobile, approx. 390 px

- [ ] Navigation does not block content
- [ ] Sticky zoom map remains connected to the numbered steps
- [ ] Stage label remains readable
- [ ] Oberschwaben handoff does not feel repetitive
- [ ] Felt external map link is clear
- [ ] Value-chain scorecard is not clipped
- [ ] Footer/source section is not overwhelming

### Browser checks

- [ ] Firefox
- [ ] Chrome / Edge
- [ ] Hard refresh tested
- [ ] Incognito/private window tested

## Editorial read-through

- [ ] No obvious typo in hero and scope box
- [ ] No duplicate explanation directly after B169/B170 handoff
- [ ] Caveats are sufficient but not exhausting
- [ ] Method/source lines are compact
- [ ] The central thesis remains clear: value chain, not only field management
- [ ] No section feels like a decision tool or suitability map
- [ ] Legal/footer wording is acceptable for public demonstrator status

## Decision

- [ ] Keep V2 online as current public version
- [ ] Patch minor issues as B176+
- [ ] If serious issue appears: switch GitHub Pages back to `v1-public / root`
"""
    write(CHECKLIST, checklist)

    doc = f"""# B175 - Post-Publication Review Pass

Date: {today}

## Ziel

V2 ist veröffentlicht und als `v2.0.0` getaggt.
B175 ist der erste Post-Publication-Review-Pass.

Dieser Patch ändert keine öffentliche Seite.
Er erstellt eine strukturierte Prüfbasis für die nächsten kleinen Korrekturen.

## Git-Kontext beim Audit

| Feld | Wert |
|---|---|
| Branch | `{branch}` |
| HEAD | `{head}` |
| Tags at HEAD | `{tags_at_head if tags_at_head else '—'}` |
| Public URL | `{PUBLIC_URL}` |

## Erzeugte Dateien

- `docs/B175_post_publication_review_pass.md`
- `docs/B175_post_publication_review_pass_audit.txt`
- `docs/B175_section_inventory.csv`
- `docs/B175_review_candidates.csv`
- `docs/B175_publication_review_checklist.md`

## Zusammenfassung

| Kategorie | Anzahl |
|---|---:|
| Sections erkannt | {len(sections)} |
| Review-Kandidaten | {len(review_candidates)} |
| OK-Signale | {len(ok_candidates)} |
| FAIL-Signale | {len(fail_candidates)} |

## Längste Sections

| Rang | Heading | Wörter | ID/Class |
|---:|---|---:|---|
"""
    for rank, s in enumerate(top_sections, start=1):
        id_class = s["id"] or s["class"] or "—"
        heading = s["heading"] or s["kicker"] or f"Section {s['order']}"
        doc += f"| {rank} | {heading} | {s['word_count']} | `{id_class}` |\n"

    doc += """
## Review-Kandidaten

"""
    if review_candidates:
        for row in review_candidates:
            doc += f"- **{row['label']}** (`{row['type']}`, count={row['count']}): {row['detail']}\n"
    else:
        doc += "Keine Review-Kandidaten nach den automatischen Heuristiken.\n"

    doc += """

## FAIL-Signale

"""
    if fail_candidates:
        for row in fail_candidates:
            doc += f"- **{row['label']}**: {row['detail']}\n"
    else:
        doc += "Keine FAIL-Signale.\n"

    doc += """

## Interpretation

B175 ist kein automatisches Urteil über Qualität.
Die Ergebnisse sind eine Arbeitsliste:

- hohe Termdichte kann fachlich sinnvoll sein, aber auf Wiederholung prüfen
- lange Sections können bewusst sein, sollten aber beim Lesefluss auffallen
- Release-Signale müssen vollständig vorhanden sein
- die manuelle Checkliste bleibt entscheidend, vor allem für mobile Darstellung und öffentliche Wirkung

## Empfohlene nächste Reihenfolge

```text
B176 Final Copy Compression
B177 Source/Footer Legal Polish
B178 Performance and Asset Weight Audit
B179 Public README / Project Landing Documentation
```
"""
    write(DOC, doc)

    audit = f"""# B175 post-publication review pass audit

Date: {today}

No public page files changed.

Git context:
- Branch: {branch}
- HEAD: {head}
- Tags at HEAD: {tags_at_head if tags_at_head else '—'}

Input files:
- index.html exists: {INDEX.exists()}
- index.html length: {len(html)}
- src/styles.css exists: {CSS.exists()}
- src/styles.css length: {len(css)}

Outputs:
- docs/B175_post_publication_review_pass.md
- docs/B175_post_publication_review_pass_audit.txt
- docs/B175_section_inventory.csv
- docs/B175_review_candidates.csv
- docs/B175_publication_review_checklist.md
- tasks/done.md

Counts:
- sections: {len(sections)}
- review candidates: {len(review_candidates)}
- fail signals: {len(fail_candidates)}

Working tree status before/around audit:
{status if status else 'clean'}

Result: AUDIT COMPLETE. No public page files changed.
"""
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B175 post-publication review pass complete.")
    print("Audit only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B175_post_publication_review_pass.md")
    print("  docs/B175_post_publication_review_pass_audit.txt")
    print("  docs/B175_section_inventory.csv")
    print("  docs/B175_review_candidates.csv")
    print("  docs/B175_publication_review_checklist.md")
    print("  tasks/done.md")
    print(f"Sections: {len(sections)} | Review candidates: {len(review_candidates)} | FAIL signals: {len(fail_candidates)}")
    print("Next: inspect docs/B175_post_publication_review_pass.md and checklist.")


if __name__ == "__main__":
    main()
