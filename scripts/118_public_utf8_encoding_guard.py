#!/usr/bin/env python3
"""
B118 - Public UTF-8 encoding guard

Purpose
-------
Fix visible umlaut/mojibake issues after recent public hardening.

Symptoms this addresses:
- German umlauts show as "Ã¤", "Ã¶", "Ã¼", "ÃŸ"
- CO₂ shows as "COâ‚‚"
- punctuation shows as "â€“", "â€ž", "Â·", etc.

Actions:
- ensure <meta charset="utf-8"> is the first meta element inside <head>;
- remove duplicate charset meta tags;
- repair common mojibake sequences if they are already present in index.html;
- write index.html as UTF-8;
- create a minimal audit.

Changed:
- index.html
- docs/B118_public_utf8_encoding_audit.txt
- tasks/done.md

Not changed:
- maps
- CSS
- data
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import html as html_lib
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
BACKUP_DIR = ROOT / "_backup_before_b118_utf8_encoding_guard"
AUDIT = DOCS / "B118_public_utf8_encoding_audit.txt"

TODAY = date.today().isoformat()

MOJIBAKE_REPLACEMENTS = {
    "Ã¤": "ä",
    "Ã¶": "ö",
    "Ã¼": "ü",
    "Ã„": "Ä",
    "Ã–": "Ö",
    "Ãœ": "Ü",
    "ÃŸ": "ß",
    "Ã©": "é",
    "Ãè": "è",
    "Ã¡": "á",
    "Ã ": "à",
    "Â·": "·",
    "Â ": " ",
    "Â ": " ",
    "Â­": "",
    "Â": "",
    "â€“": "–",
    "â€”": "—",
    "â€˜": "‘",
    "â€™": "’",
    "â€œ": "“",
    "â€\x9d": "”",
    "â€ž": "„",
    "â€¦": "…",
    "â†’": "→",
    "â‰¥": "≥",
    "â‰¤": "≤",
    "â‚¬": "€",
    "COâ‚‚": "CO₂",
    "COâ‚‚e": "CO₂e",
    "COâ‚‚-": "CO₂-",
    "COâ‚‚Äquivalente": "CO₂-Äquivalente",
    "COâ‚‚-Ã„quivalente": "CO₂-Äquivalente",
}

RISK_PATTERNS = [
    "Ã",
    "Â",
    "â€",
    "â€“",
    "â€”",
    "â€¦",
    "â‚",
    "�",
]

REQUIRED_PATTERNS = [
    '<meta charset="utf-8">',
    "Baden-Württemberg",
    "räumliche Orientierung",
    "Moor-/Feuchtbodenkontext",
    "Treibhausgasminderung",
    "Oberschwaben",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    # utf-8-sig handles a BOM if one exists.
    return data.decode("utf-8-sig", errors="replace")


def write_text_utf8(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def visible_text(raw: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def ensure_meta_charset(raw: str) -> tuple[str, int, bool]:
    # Remove all existing charset metas, regardless of exact charset.
    charset_meta_re = re.compile(r"\s*<meta\s+[^>]*charset\s*=\s*['\"]?[^'\"\s/>]+['\"]?[^>]*>\s*", flags=re.IGNORECASE)
    raw2, removed = charset_meta_re.subn("\n", raw)

    head_re = re.compile(r"<head\b[^>]*>", flags=re.IGNORECASE)
    m = head_re.search(raw2)
    if not m:
        # Last-resort insertion for malformed HTML.
        return '<head>\n  <meta charset="utf-8">\n</head>\n' + raw2, removed, True

    insert_at = m.end()
    raw3 = raw2[:insert_at] + '\n  <meta charset="utf-8">' + raw2[insert_at:]
    return raw3, removed, True


def fix_mojibake(raw: str) -> tuple[str, dict[str, int]]:
    out = raw
    counts: dict[str, int] = {}
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        n = out.count(bad)
        if n:
            out = out.replace(bad, good)
        counts[bad] = n
    return out, counts


def update_done() -> None:
    current = read_text(DONE) if DONE.exists() else "# Done\n"
    marker = "## B118 - Public UTF-8 encoding guard"
    if marker in current:
        return
    entry = f"""
## B118 - Public UTF-8 encoding guard ({TODAY})

- Ensured `<meta charset="utf-8">` is present at the top of the HTML head.
- Removed duplicate charset meta tags.
- Repaired common mojibake sequences for German umlauts, CO₂ and punctuation if present.
- Did not modify maps, CSS or data.
"""
    write_text_utf8(DONE, current.rstrip() + "\n" + entry)


def write_audit(meta_removed: int, meta_inserted: bool, mojibake_counts: dict[str, int], before: str, after: str) -> None:
    vis = visible_text(after)
    risk_counts = {p: vis.count(p) for p in RISK_PATTERNS}
    required_counts = {p: after.count(p) if p.startswith("<meta") else vis.count(p) for p in REQUIRED_PATTERNS}

    status = "OK" if all(c == 0 for c in risk_counts.values()) and all(c > 0 for c in required_counts.values()) else "REVIEW REQUIRED"

    lines = [
        "# B118 public UTF-8 encoding audit",
        "",
        f"- Status: {status}",
        f"- index.html changed: {'YES' if before != after else 'NO'}",
        f"- charset meta tags removed before insertion: {meta_removed}",
        f"- charset meta inserted: {meta_inserted}",
        "",
        "## Mojibake replacements applied",
        "",
        "| Sequence | Replacement count |",
        "|---|---:|",
    ]

    applied = {k: v for k, v in mojibake_counts.items() if v}
    if applied:
        for k, v in applied.items():
            display = k.encode("unicode_escape").decode("ascii")
            lines.append(f"| `{display}` | {v} |")
    else:
        lines.append("| none | 0 |")

    lines.extend([
        "",
        "## Remaining risk patterns in visible text",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ])
    for p, c in risk_counts.items():
        display = p.encode("unicode_escape").decode("ascii")
        lines.append(f"| `{display}` | {c} |")

    lines.extend([
        "",
        "## Required patterns",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ])
    for p, c in required_counts.items():
        display = p.encode("unicode_escape").decode("ascii")
        lines.append(f"| `{display}` | {c} |")

    lines.extend([
        "",
        "## Review commands",
        "",
        "```powershell",
        "Get-Content index.html -TotalCount 15",
        "Select-String -Path index.html -Pattern \"Ã\",\"Â\",\"â€\",\"â€“\",\"â‚\",\"�\",\"charset\",\"Baden-Württemberg\",\"räumliche Orientierung\",\"CO₂\"",
        "python scripts\\103b_corrected_visible_text_audit.py",
        "python scripts\\58_visual_qa_and_commit_check.py",
        "python -m http.server 8000",
        "```",
        "",
    ])
    write_text_utf8(AUDIT, "\n".join(lines))


def main() -> None:
    if not INDEX.exists():
        print(f"Missing {rel(INDEX)}")
        sys.exit(1)

    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    backup = BACKUP_DIR / "index_before_b118.html"
    if not backup.exists():
        shutil.copy2(INDEX, backup)

    original = read_text(INDEX)
    fixed, mojibake_counts = fix_mojibake(original)
    fixed, meta_removed, meta_inserted = ensure_meta_charset(fixed)

    write_text_utf8(INDEX, fixed)
    update_done()
    write_audit(meta_removed, meta_inserted, mojibake_counts, original, fixed)

    vis = visible_text(fixed)
    risk_total = sum(vis.count(p) for p in RISK_PATTERNS)

    print("B118 public UTF-8 encoding guard complete.")
    print("Changed/created:")
    for p in [INDEX, AUDIT, DONE]:
        print(f"  {rel(p)}")
    print(f"  {rel(backup)}")
    print("")
    print(f"Remaining mojibake risk pattern hits: {risk_total}")
    print("")
    print("Review:")
    print("  Get-Content docs\\B118_public_utf8_encoding_audit.txt")
    print("  Select-String -Path index.html -Pattern \"Ã\",\"Â\",\"â€\",\"â€“\",\"â‚\",\"�\",\"charset\",\"Baden-Württemberg\",\"räumliche Orientierung\",\"CO₂\"")
    print("  python scripts\\58_visual_qa_and_commit_check.py")


if __name__ == "__main__":
    main()
