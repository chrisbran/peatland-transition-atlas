#!/usr/bin/env python3
# B127 - Publication frame and map sequence tightening
#
# Purpose:
# - sharpen public framing from generic "Moorschutz" to "Moorbodenschutz"
# - remove central scrolly steps that only show political/administrative boundaries
# - keep the substantive Europe/Germany maps and retitle them as scale transitions
# - change "kompakt öffnen" to "Details öffnen"
# - add a provisional footer / publication frame
#
# Changed:
# - index.html
# - src/central_global_map_story.js
# - src/styles.css
# - docs/B127_publication_frame_and_sequence_tightening.md
# - docs/B127_publication_frame_and_sequence_tightening_audit.txt
# - tasks/done.md

from __future__ import annotations

from datetime import date
from pathlib import Path
import html as html_lib
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CENTRAL_JS = ROOT / "src" / "central_global_map_story.js"
CSS = ROOT / "src" / "styles.css"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b127_publication_frame_sequence"

REPORT = DOCS / "B127_publication_frame_and_sequence_tightening.md"
AUDIT = DOCS / "B127_publication_frame_and_sequence_tightening_audit.txt"
TODAY = date.today().isoformat()

REMOVE_STATES = ["europe-borders", "germany-context"]

RETITLE_STATES = {
    "europe-peat": (
        "Europa zeigt den größeren Bezugsraum.",
        "Moorbodenschutz ist eine regionale Aufgabe, steht aber in einem europäischen Zusammenhang von Nutzung, Entwässerung und Klimazielen.",
    ),
    "germany-thuenen-extent": (
        "Deutschland grenzt den Prüfbedarf ein.",
        "Die nationale Kulisse zeigt, wo organische Böden in größerem Zusammenhang auftreten und wo Länder und Regionen genauer hinsehen müssen.",
    ),
}

FOOTER_MARKER_START = "<!-- B127_PUBLICATION_FOOTER -->"
FOOTER_MARKER_END = "<!-- /B127_PUBLICATION_FOOTER -->"
CSS_MARKER = "/* B127 publication footer */"

FOOTER_HTML = """
<!-- B127_PUBLICATION_FOOTER -->
<footer class="b127-publication-footer" aria-label="Veröffentlichungsrahmen">
  <div class="b127-footer-inner">
    <p><strong>Stand: Juni 2026 · Fachlicher Demonstrator</strong></p>
    <p>Erstellt im Kontext von SOLAMO-BW / Universität Hohenheim.</p>
    <p>Diese Seite bietet räumliche Orientierung und ersetzt keine Standortprüfung.</p>
    <p class="b127-footer-links">Impressum · Datenschutz</p>
  </div>
</footer>
<!-- /B127_PUBLICATION_FOOTER -->
"""

CSS_BLOCK = """
/* B127 publication footer */
.b127-publication-footer {
  width: min(980px, calc(100% - 2rem));
  margin: 0 auto clamp(2rem, 5vw, 4rem);
  padding: 1.2rem 0 0;
  color: rgba(31, 42, 34, .72);
  font-size: .9rem;
}
.b127-footer-inner {
  border-top: 1px solid rgba(31, 42, 34, .16);
  padding-top: 1rem;
}
.b127-publication-footer p {
  margin: .25rem 0;
  line-height: 1.45;
}
.b127-footer-links {
  color: rgba(31, 42, 34, .58);
}
"""

REQUIRED = [
    "Moorbodenschutz",
    "Details öffnen",
    "Europa zeigt den größeren Bezugsraum.",
    "Moorbodenschutz ist eine regionale Aufgabe",
    "Deutschland grenzt den Prüfbedarf ein.",
    "Die nationale Kulisse zeigt, wo organische Böden in größerem Zusammenhang auftreten",
    "Stand: Juni 2026 · Fachlicher Demonstrator",
    "Erstellt im Kontext von SOLAMO-BW / Universität Hohenheim.",
    "Diese Seite bietet räumliche Orientierung und ersetzt keine Standortprüfung.",
    "Impressum · Datenschutz",
]

RISK = [
    "kompakt öffnen",
    "Europa zeigt den politischen Maßstab.",
    "Politische und administrative Grenzen bestimmen",
    "Deutschland zeigt, wo Planung und Förderung ansetzen.",
    "Nationale Karten zeigen, wo Förderprogramme",
    "data-global-state=\"europe-borders\"",
    "data-global-state=\"germany-context\"",
    "GLOBAL_FRAME_V1",
    "Thuenen",
    "Ã",
    "�",
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


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def replace_first_tag(block: str, tag: str, new_inner: str) -> tuple[str, int]:
    pattern = rf"<{tag}>(.*?)</{tag}>"
    repl = f"<{tag}>{new_inner}</{tag}>"
    return re.subn(pattern, repl, block, count=1, flags=re.DOTALL)


def replace_article_step(html: str, state: str, title: str, body: str) -> tuple[str, int]:
    pattern = rf'(<article\b[^>]*\bdata-global-state="{re.escape(state)}"[^>]*>.*?</article>)'
    m = re.search(pattern, html, flags=re.DOTALL)
    if not m:
        return html, 0

    block = m.group(1)
    new_block, h3_hits = replace_first_tag(block, "h3", title)
    new_block, p_hits = replace_first_tag(new_block, "p", body)
    return html[:m.start()] + new_block + html[m.end():], h3_hits + p_hits


def remove_article_step(html: str, state: str) -> tuple[str, int]:
    pattern = rf'\s*<article\b[^>]*\bdata-global-state="{re.escape(state)}"[^>]*>.*?</article>\s*'
    return re.subn(pattern, "\n", html, count=1, flags=re.DOTALL)


def patch_branding(html: str) -> tuple[str, int]:
    hits = 0

    replacements = [
        (">Moorschutz</a>", ">Moorbodenschutz</a>"),
        (">Moorschutz</div>", ">Moorbodenschutz</div>"),
        ("<span>Moorschutz</span>", "<span>Moorbodenschutz</span>"),
        ("<title>Moorschutz", "<title>Moorbodenschutz"),
        ("Moorschutz braucht räumliche Orientierung", "Moorbodenschutz braucht räumliche Orientierung"),
    ]

    for old, new in replacements:
        n = html.count(old)
        if n:
            html = html.replace(old, new, 1 if old in [">Moorschutz</a>", ">Moorschutz</div>", "<span>Moorschutz</span>"] else -1)
            hits += n

    return html, hits


def patch_footer(html: str) -> tuple[str, int]:
    html = re.sub(
        r"\n?<!-- B127_PUBLICATION_FOOTER -->.*?<!-- /B127_PUBLICATION_FOOTER -->\n?",
        "\n",
        html,
        flags=re.DOTALL,
    )

    pos = html.rfind("</body>")
    if pos >= 0:
        return html[:pos] + "\n\n" + FOOTER_HTML.strip() + "\n\n" + html[pos:], 1

    return html.rstrip() + "\n\n" + FOOTER_HTML.strip() + "\n", 1


def patch_css(css: str) -> tuple[str, int]:
    css = re.sub(
        r"\n?/\* B127 publication footer \*/.*?(?=\n/\* |\Z)",
        "\n",
        css,
        flags=re.DOTALL,
    )
    return css.rstrip() + "\n\n" + CSS_BLOCK.strip() + "\n", 1


def patch_js_titles(js: str) -> tuple[str, int]:
    hits = 0
    for state, (title, _body) in RETITLE_STATES.items():
        pattern = rf'("{re.escape(state)}":\s*\{{.*?title:\s*")[^"]*(")'
        js, n = re.subn(pattern, rf'\1{title}\2', js, flags=re.DOTALL)
        hits += n
    return js, hits


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B127 - Publication frame and sequence tightening"
    if marker in current:
        return

    entry = f"""
## B127 - Publication frame and sequence tightening ({TODAY})

- Sharpened public framing from generic `Moorschutz` to `Moorbodenschutz`.
- Removed central scrolly steps that only showed Europe/Germany boundary frames.
- Retitled the substantive Europe and Germany layers as scale transitions.
- Changed `kompakt öffnen` to `Details öffnen`.
- Added a provisional publication footer with status, context, method boundary and Impressum/Datenschutz line.
- Did not modify map images, data or layer mechanics.
"""
    write_text(DONE, current.rstrip() + "\n" + entry)


def audit(counters: dict[str, int]) -> dict[str, object]:
    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)
    css = read_text(CSS)
    visible = visible_text(html)
    raw = html + "\n" + js + "\n" + css

    required_counts = {p: raw.count(p) for p in REQUIRED}
    visible_risk_counts = {p: visible.count(p) for p in RISK}
    raw_risk_counts = {p: raw.count(p) for p in RISK}

    return {
        "required_counts": required_counts,
        "visible_risk_counts": visible_risk_counts,
        "raw_risk_counts": raw_risk_counts,
        "missing_required": sum(1 for v in required_counts.values() if v == 0),
        "visible_risk_findings": sum(1 for v in visible_risk_counts.values() if v > 0),
        "raw_risk_findings": sum(1 for v in raw_risk_counts.values() if v > 0),
        "footer_count": html.count(FOOTER_MARKER_START),
        "css_marker_count": css.count(CSS_MARKER),
        "counters": counters,
    }


def write_docs(result: dict[str, object]) -> None:
    ok = (
        result["missing_required"] == 0
        and result["visible_risk_findings"] == 0
        and result["footer_count"] == 1
        and result["css_marker_count"] == 1
    )
    status = "OK" if ok else "REVIEW REQUIRED"

    report = [
        "# B127 – Publication Frame and Sequence Tightening",
        "",
        f"Stand: {TODAY}",
        "",
        f"Status: **{status}**",
        "",
        "## Ziel",
        "",
        "B127 schärft den Veröffentlichungsrahmen und entfernt reine Grenz-/Rahmenkarten aus der zentralen Kartenfolge.",
        "",
        "## Änderungen",
        "",
    ]
    for k, v in result["counters"].items():
        report.append(f"- {k}: {v}")

    report.extend([
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
        f"- Footer count: {result['footer_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content docs\\B127_publication_frame_and_sequence_tightening_audit.txt -Encoding UTF8",
        "Select-String -Encoding UTF8 -Path index.html,src\\central_global_map_story.js,src\\styles.css -Pattern \"Moorbodenschutz\",\"Details öffnen\",\"Europa zeigt den größeren Bezugsraum\",\"Deutschland grenzt den Prüfbedarf ein\",\"Stand: Juni 2026\",\"kompakt öffnen\",\"data-global-state=`\"europe-borders`\"\",\"data-global-state=`\"germany-context`\"\",\"GLOBAL_FRAME_V1\",\"Thuenen\",\"Ã\",\"�\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text(REPORT, "\n".join(report))

    audit_lines = [
        "# B127 publication frame and sequence tightening audit",
        "",
        f"- Status: {status}",
        f"- Missing required entries: {result['missing_required']}",
        f"- Visible risk findings: {result['visible_risk_findings']}",
        f"- Raw risk findings: {result['raw_risk_findings']}",
        f"- Footer count: {result['footer_count']}",
        f"- CSS marker count: {result['css_marker_count']}",
        "",
        "## Counters",
        "",
        "| Counter | Count |",
        "|---|---:|",
    ]
    for k, v in result["counters"].items():
        audit_lines.append(f"| `{k}` | {v} |")

    audit_lines.extend(["", "## Required patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["required_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Visible risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["visible_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    audit_lines.extend(["", "## Raw risk patterns", "", "| Pattern | Count |", "|---|---:|"])
    for p, c in result["raw_risk_counts"].items():
        audit_lines.append(f"| `{p}` | {c} |")

    write_text(AUDIT, "\n".join(audit_lines))


def main() -> None:
    for path in [INDEX, CENTRAL_JS, CSS]:
        if not path.exists():
            print(f"Missing {rel(path)}")
            sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)

    for path in [INDEX, CENTRAL_JS, CSS]:
        backup(path)

    html = read_text(INDEX)
    js = read_text(CENTRAL_JS)
    css = read_text(CSS)

    counters = {
        "branding_hits": 0,
        "removed_boundary_steps": 0,
        "retitled_html_steps": 0,
        "retitled_js_titles": 0,
        "details_label_hits": 0,
        "footer_hits": 0,
        "css_hits": 0,
    }

    html, n = patch_branding(html)
    counters["branding_hits"] += n

    n = html.count("kompakt öffnen")
    if n:
        html = html.replace("kompakt öffnen", "Details öffnen")
    counters["details_label_hits"] += n

    for state in REMOVE_STATES:
        html, n = remove_article_step(html, state)
        counters["removed_boundary_steps"] += n

    for state, (title, body) in RETITLE_STATES.items():
        html, n = replace_article_step(html, state, title, body)
        counters["retitled_html_steps"] += n

    js, n = patch_js_titles(js)
    counters["retitled_js_titles"] += n

    html, n = patch_footer(html)
    counters["footer_hits"] += n

    css, n = patch_css(css)
    counters["css_hits"] += n

    write_text(INDEX, html)
    write_text(CENTRAL_JS, js)
    write_text(CSS, css)
    update_done()

    result = audit(counters)
    write_docs(result)

    ok = (
        result["missing_required"] == 0
        and result["visible_risk_findings"] == 0
        and result["footer_count"] == 1
        and result["css_marker_count"] == 1
    )

    print("B127 publication frame and sequence tightening complete.")
    print("Changed/created:")
    for p in [INDEX, CENTRAL_JS, CSS, REPORT, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(BACKUP_DIR)}")
    print("")
    print(f"Status: {'OK' if ok else 'REVIEW REQUIRED'}")
    print(f"Missing required entries: {result['missing_required']}")
    print(f"Visible risk findings: {result['visible_risk_findings']}")
    print(f"Raw risk findings: {result['raw_risk_findings']}")
    print(f"Footer count: {result['footer_count']}")
    print(f"CSS marker count: {result['css_marker_count']}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B127_publication_frame_and_sequence_tightening_audit.txt -Encoding UTF8")
    print("  python scripts\\103b_corrected_visible_text_audit.py")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python -m http.server 8000")


if __name__ == "__main__":
    main()
