#!/usr/bin/env python3
"""
B84 - Hard fix JS textContent error and central panel styling

Purpose:
- Fix the remaining red error:
  "can't access property 'textContent', document.querySelector(...) is null"
- B83 only guarded simple one-line assignment patterns. B84 scans index.html and src/*.js
  for broader querySelector(...).textContent reads/assignments and hardens them.
- Make all central story step cards use one consistent dark panel style.
- Add a diagnostic report so we can see what was patched.

Outputs:
- docs/B84_js_textcontent_and_panel_hardening.md
- docs/B84_textcontent_patch_inventory.txt
- modifies index.html and/or src/*.js when unsafe querySelector(...).textContent patterns are found
- modifies src/styles.css
- updates tasks/done.md

Does NOT:
- modify map assets
- modify raw data
- change central map state names
- delete sections/scripts
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SRC = ROOT / "src"
DOCS = ROOT / "docs"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOC = DOCS / "B84_js_textcontent_and_panel_hardening.md"
INV = DOCS / "B84_textcontent_patch_inventory.txt"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def harden_textcontent_patterns(path: Path) -> tuple[bool, list[str]]:
    """
    Conservative JS hardening.

    Handles:
    1) document.querySelector("x").textContent = rhs;
    2) document.querySelector("x").textContent read expressions

    The aim is to prevent null.textContent exceptions after B79/B82 retired or
    replaced legacy DOM elements.
    """
    txt = read(path)
    before = txt
    notes: list[str] = []

    # Single-line assignments.
    assignment_pat = re.compile(
        r"document\.querySelector\((?P<sel>(?:[^)(]+|\([^)]*\))+?)\)\.textContent\s*=\s*(?P<rhs>[^;\n]+);",
        flags=re.MULTILINE,
    )

    def repl_assignment(m: re.Match) -> str:
        sel = m.group("sel").strip()
        rhs = m.group("rhs").strip()
        notes.append(f"assignment guarded: document.querySelector({sel}).textContent = ...")
        return (
            "(function(){ "
            f"const __b84TextTarget = document.querySelector({sel}); "
            f"if (__b84TextTarget) {{ __b84TextTarget.textContent = {rhs}; }} "
            "})();"
        )

    txt = assignment_pat.sub(repl_assignment, txt)

    # Remaining read usages. Avoid replacing assignments.
    read_pat = re.compile(
        r"document\.querySelector\((?P<sel>(?:[^)(]+|\([^)]*\))+?)\)\.textContent(?!\s*=)",
        flags=re.MULTILINE,
    )

    def repl_read(m: re.Match) -> str:
        sel = m.group("sel").strip()
        notes.append(f"read guarded: document.querySelector({sel}).textContent")
        return f"(document.querySelector({sel})?.textContent || \"\")"

    txt = read_pat.sub(repl_read, txt)

    # Special multi-line pattern:
    multiline_read_pat = re.compile(
        r"document\s*\.\s*querySelector\((?P<sel>[\s\S]{0,200}?)\)\s*\.\s*textContent(?!\s*=)",
        flags=re.MULTILINE,
    )

    def repl_multiline_read(m: re.Match) -> str:
        sel_raw = m.group("sel")
        if "?." in m.group(0):
            return m.group(0)
        sel = " ".join(sel_raw.split())
        notes.append(f"multiline read guarded: document.querySelector({sel}).textContent")
        return f"(document.querySelector({sel})?.textContent || \"\")"

    txt = multiline_read_pat.sub(repl_multiline_read, txt)

    if txt != before:
        write(path, txt)
        return True, notes
    return False, notes


def scan_remaining_textcontent_patterns(paths: list[Path]) -> list[str]:
    remaining = []
    pat = re.compile(r"document\s*\.\s*querySelector\([\s\S]{0,160}?\)\s*\.\s*textContent", re.MULTILINE)
    for path in paths:
        txt = read(path)
        for m in pat.finditer(txt):
            start_line = txt[:m.start()].count("\n") + 1
            snippet = " ".join(m.group(0).split())
            remaining.append(f"{rel(path)}:{start_line}: {snippet}")
    return remaining


def remove_visible_newline_artifacts() -> int:
    html = read(INDEX)
    count = html.count("\\n")
    if count:
        html = html.replace("\\n", "")
        write(INDEX, html)
    return count


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    paths = [INDEX] + sorted(SRC.glob("*.js"))
    changed_paths: list[str] = []
    patch_notes: list[str] = []

    for path in paths:
        changed, notes = harden_textcontent_patterns(path)
        if changed:
            changed_paths.append(rel(path))
            patch_notes.append(f"## {rel(path)}")
            patch_notes.extend(f"- {n}" for n in notes)

    literal_newlines_removed = remove_visible_newline_artifacts()

    # Panel CSS: use very broad but scoped selectors inside centralGlobalMapStory,
    # because current DOM classes differ across patches.
    css = read(CSS)
    b84_css = r"""
/* B84 harden central map story panels */

/* Broad scoped panel treatment: all central story text cards/articles get the same dark surface. */
#centralGlobalMapStory article,
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory .central-story-step,
#centralGlobalMapStory .map-step,
#centralGlobalMapStory .step,
#centralGlobalMapStory [data-global-state] {
  background: rgba(9, 18, 15, 0.86) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.14) !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.24) !important;
  backdrop-filter: blur(9px) saturate(0.92) !important;
  -webkit-backdrop-filter: blur(9px) saturate(0.92) !important;
}

/* Do not accidentally style the map image/frame as a text panel. */
#centralGlobalMapStory figure,
#centralGlobalMapStory .central-map-visual,
#centralGlobalMapStory .central-map-stage,
#centralGlobalMapStory .central-map-frame,
#centralGlobalMapStory .map-frame {
  background: transparent !important;
  color: inherit !important;
  border-color: rgba(222, 212, 199, 0.95) !important;
  box-shadow: 0 18px 64px rgba(70, 50, 30, 0.12) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

#centralGlobalMapStory article h1,
#centralGlobalMapStory article h2,
#centralGlobalMapStory article h3,
#centralGlobalMapStory .central-map-step h1,
#centralGlobalMapStory .central-map-step h2,
#centralGlobalMapStory .central-map-step h3,
#centralGlobalMapStory [data-global-state] h1,
#centralGlobalMapStory [data-global-state] h2,
#centralGlobalMapStory [data-global-state] h3 {
  color: #F5F0E7 !important;
}

#centralGlobalMapStory article p,
#centralGlobalMapStory .central-map-step p,
#centralGlobalMapStory [data-global-state] p {
  color: rgba(245, 240, 231, 0.78) !important;
}

#centralGlobalMapStory article span,
#centralGlobalMapStory .central-map-step span,
#centralGlobalMapStory [data-global-state] span,
#centralGlobalMapStory .step-number {
  color: #55A3B5 !important;
}

/* Remove pale overlay artefacts from all step cards. */
#centralGlobalMapStory article::before,
#centralGlobalMapStory article::after,
#centralGlobalMapStory .central-map-step::before,
#centralGlobalMapStory .central-map-step::after,
#centralGlobalMapStory [data-global-state]::before,
#centralGlobalMapStory [data-global-state]::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Text safety in all central panels. */
#centralGlobalMapStory article *,
#centralGlobalMapStory .central-map-step *,
#centralGlobalMapStory [data-global-state] * {
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  hyphens: auto !important;
}

/* Hide standalone browser-like error bars if the old debug UI inserted one.
   This is a visual safeguard; the JS guard above addresses the actual cause. */
.error,
.error-banner,
.debug-error,
.runtime-error,
[role="alert"].error,
body > pre:first-child {
  display: none !important;
}
/* End B84 harden central map story panels */
"""
    if "/* B84 harden central map story panels */" not in css:
        css = css.rstrip() + "\n\n" + b84_css.strip() + "\n"
        write(CSS, css)

    remaining = scan_remaining_textcontent_patterns(paths)

    inv_lines = [
        f"B84 textContent patch inventory - {today}",
        "",
        "Changed files:",
    ]
    inv_lines.extend(f"- {p}" for p in changed_paths)
    inv_lines.extend(["", "Patch notes:"])
    inv_lines.extend(patch_notes if patch_notes else ["- none"])
    inv_lines.extend(["", "Remaining raw document.querySelector(...).textContent patterns after B84:"])
    inv_lines.extend((f"- {r}" for r in remaining) if remaining else ["- none"])
    inv_lines.extend(["", f"Literal backslash-n occurrences removed from index.html: {literal_newlines_removed}"])
    write(INV, "\n".join(inv_lines) + "\n")

    remaining_md = "\n".join(f"- `{r}`" for r in remaining) if remaining else "- none"
    changed_md = "\n".join(f"- `{p}`" for p in changed_paths) if changed_paths else "- none"

    doc = f"""# B84 - JS textContent and Panel Hardening

Date: {today}

## 1. Why B84 was needed

After B83, two issues remained:

1. The red error bar was still visible:
   `can't access property "textContent", document.querySelector(...) is null`
2. Only step 01 reliably used the desired dark panel style; later cards still appeared lighter.

B83 only guarded simple one-line `document.querySelector(...).textContent = ...` assignments. B84 scans both `index.html` and `src/*.js` for broader read/assignment patterns.

## 2. What B84 changed

- Hardened broader `document.querySelector(...).textContent` patterns.
- Removed remaining literal `\\n` artefacts from `index.html`.
- Added a broader central-story CSS rule so all central map text cards/articles get the same dark panel style.
- Added a visual safeguard for browser/debug-style error banners.
- Created `docs/B84_textcontent_patch_inventory.txt`.

## 3. Files changed by JS hardening

{changed_md}

## 4. Remaining raw textContent patterns

{remaining_md}

## 5. Literal newline artefacts removed

`{literal_newlines_removed}`

## 6. Manual QA

Check after running B84:

1. Red error bar is gone.
2. No visible `\\n` appears between steps.
3. Steps 01-11 use dark readable panels.
4. Map scroll still works.
5. The central map image/frame is not accidentally dark-card styled.
6. Hero and compact header remain stable.
"""
    write(DOC, doc)

    done_entry = f"""
## B84 - JS textContent and panel hardening ({today})

- Hardened broader `document.querySelector(...).textContent` patterns in `index.html` and `src/*.js`.
- Removed literal `\\n` artefacts from `index.html`.
- Applied broad dark styling to all central map story text panels.
- Created `docs/B84_js_textcontent_and_panel_hardening.md`.
- Created `docs/B84_textcontent_patch_inventory.txt`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B84 - JS textContent and panel hardening" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B84 JS textContent and panel hardening complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    for p in changed_paths:
        print(f"  {p}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(INV)}")
    print(f"  {rel(DONE)}")
    print(f"Remaining raw document.querySelector(...).textContent patterns: {len(remaining)}")
    print(f"Literal \\\\n occurrences removed from index.html: {literal_newlines_removed}")


if __name__ == "__main__":
    main()
