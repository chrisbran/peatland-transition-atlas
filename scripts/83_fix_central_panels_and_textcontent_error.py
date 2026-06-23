#!/usr/bin/env python3
"""
B83 - Fix central story panels and JS textContent guard

Purpose:
- Remove visible literal "\\n" artefacts.
- Make all central map step panels consistently dark/readable like step 01.
- Guard JS patterns of document.querySelector(...).textContent that can fail after
  sections were retired/replaced.
- Document why the top red error appeared.

Outputs:
- docs/B83_fix_central_panels_and_textcontent_error.md
- modifies index.html
- modifies src/styles.css
- may modify src/*.js files containing unsafe querySelector(...).textContent assignments
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
DOC = DOCS / "B83_fix_central_panels_and_textcontent_error.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def remove_literal_newline_artefacts(html: str) -> tuple[str, int]:
    # Remove literal backslash+n text nodes that can become visible as "\n" between cards.
    before = html
    html = re.sub(r">\s*\\n\s*<", ">\n<", html)
    # Remove remaining isolated literal \n occurrences outside script/style-like content.
    # index.html should not contain production JS string literals requiring backslash-n.
    html = html.replace("\\n", "")
    return html, before.count("\\n")


def patch_textcontent_queryselector_assignments() -> list[str]:
    changed = []
    # Handles common simple assignment form:
    # document.querySelector("...").textContent = value;
    pattern = re.compile(
        r"document\.querySelector\((?P<selector>[^;\n]+?)\)\.textContent\s*=\s*(?P<rhs>[^;\n]+);",
        flags=re.MULTILINE,
    )

    for path in sorted(SRC.glob("*.js")):
        txt = read(path)
        before = txt

        def repl(m: re.Match) -> str:
            whole = m.group(0)
            if "__b83TextTarget" in whole:
                return whole
            selector = m.group("selector").strip()
            rhs = m.group("rhs").strip()
            return (
                f"(function() {{ "
                f"const __b83TextTarget = document.querySelector({selector}); "
                f"if (__b83TextTarget) {{ __b83TextTarget.textContent = {rhs}; }} "
                f"}})();"
            )

        txt = pattern.sub(repl, txt)

        if txt != before:
            write(path, txt)
            changed.append(rel(path))

    return changed


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS)

    html, n_literal_newlines = remove_literal_newline_artefacts(html)
    write(INDEX, html)

    changed_js = patch_textcontent_queryselector_assignments()

    b83_css = r"""
/* B83 central story panel polish and overflow guard */

/* All central step panels should use the same dark, legible treatment.
   This removes the mismatch where step 01 looked intentional but later cards looked pale/ghosted. */
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state],
#centralGlobalMapStory .central-map-step[style],
#centralGlobalMapStory article[data-global-state][style] {
  background: rgba(9, 18, 15, 0.84) !important;
  color: #F5F0E7 !important;
  border: 1px solid rgba(245, 240, 231, 0.14) !important;
  box-shadow: 0 18px 54px rgba(0, 0, 0, 0.24) !important;
  backdrop-filter: blur(9px) saturate(0.92) !important;
  -webkit-backdrop-filter: blur(9px) saturate(0.92) !important;
  overflow: hidden !important;
}

#centralGlobalMapStory .central-map-step h3,
#centralGlobalMapStory article[data-global-state] h3 {
  color: #F5F0E7 !important;
  text-shadow: none !important;
}

#centralGlobalMapStory .central-map-step p,
#centralGlobalMapStory article[data-global-state] p {
  color: rgba(245, 240, 231, 0.78) !important;
  text-shadow: none !important;
}

#centralGlobalMapStory .central-map-step span,
#centralGlobalMapStory article[data-global-state] span,
#centralGlobalMapStory .central-map-step .step-number,
#centralGlobalMapStory article[data-global-state] .step-number {
  color: #55A3B5 !important;
}

/* Remove any old light/grey pseudo panel artefacts. */
#centralGlobalMapStory .central-map-step::before,
#centralGlobalMapStory .central-map-step::after,
#centralGlobalMapStory article[data-global-state]::before,
#centralGlobalMapStory article[data-global-state]::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* Keep step panels away from the exact viewport edge without breaking the scroll script. */
#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state] {
  max-width: min(420px, calc(100vw - 56px)) !important;
  min-width: min(300px, calc(100vw - 56px)) !important;
  box-sizing: border-box !important;
}

#centralGlobalMapStory .central-map-step *,
#centralGlobalMapStory article[data-global-state] * {
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  hyphens: auto !important;
}

/* Kill visible stray newline artefacts if any survived as standalone text-like blocks. */
#centralGlobalMapStory .central-map-copy,
#centralGlobalMapStory .central-map-step {
  white-space: normal !important;
}

@media (max-width: 860px) {
  #centralGlobalMapStory .central-map-step,
  #centralGlobalMapStory article[data-global-state] {
    min-width: 0 !important;
    max-width: calc(100vw - 32px) !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
  }
}
/* End B83 central story panel polish and overflow guard */
"""

    if "/* B83 central story panel polish and overflow guard */" not in css:
        css = css.rstrip() + "\n\n" + b83_css.strip() + "\n"
        write(CSS, css)

    doc = f"""# B83 - Fix Central Panels and textContent Error

Date: {today}

## 1. Issue

The B82 video showed three remaining issues:

1. A visible literal `\\n` artefact between central story steps.
2. Step 01 had a good dark panel treatment, while later central story panels looked lighter/ghosted.
3. A red browser/app error appeared at the top:

```text
can't access property "textContent", document.querySelector(...) is null
```

## 2. Why the error appeared

The error means that a JavaScript file tried to do this:

```js
document.querySelector(...).textContent = ...
```

but the selector did not find an element.

That is plausible after B79/B82 because older prototype sections were retired or the header/labels were replaced. A script still expected a DOM element that no longer exists in the visible page.

## 3. Changes

B83:

- removes literal `\\n` artefacts from `index.html`,
- applies a consistent dark panel treatment to all central map step cards,
- hardens text wrapping inside central step panels,
- suppresses old pseudo-element panel overlays,
- guards direct `document.querySelector(...).textContent = ...` assignment patterns in `src/*.js`.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B83_fix_central_panels_and_textcontent_error.md`

JavaScript files patched:

{chr(10).join(f"- `{p}`" for p in changed_js) if changed_js else "- none detected"}

## 5. Literal newline artefacts

Occurrences removed from `index.html`:

`{n_literal_newlines}`

## 6. Manual QA

Check:

1. No red error bar at the top.
2. No visible `\\n` between steps.
3. Central step panels 01-11 use the same dark readable style.
4. Text stays inside panel frames.
5. Central map sequence still scrolls correctly.
6. Navigation and hero remain stable.
"""
    write(DOC, doc)

    done_entry = f"""
## B83 - Fix central panels and textContent error ({today})

- Removed literal `\\n` artefacts from `index.html`.
- Applied consistent dark styling to central map step panels.
- Hardened central step text wrapping and overlay suppression.
- Guarded direct `document.querySelector(...).textContent = ...` assignment patterns in `src/*.js`.
- Created `docs/B83_fix_central_panels_and_textcontent_error.md`.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B83 - Fix central panels and textContent error" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B83 central panels and textContent error fix complete.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    if changed_js:
        for p in changed_js:
            print(f"  {p}")
    print(f"  {rel(DOC)}")
    print(f"  {rel(DONE)}")
    print(f"Literal \\\\n occurrences removed from index.html: {n_literal_newlines}")


if __name__ == "__main__":
    main()
