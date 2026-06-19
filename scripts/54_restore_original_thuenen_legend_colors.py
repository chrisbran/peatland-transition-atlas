#!/usr/bin/env python3
r"""
54 - Remove B53 custom Germany legend and restore original legend swatch colors.

Run from repository root:
  python scripts\54_restore_original_thuenen_legend_colors.py
"""

from pathlib import Path
import datetime
import re

TODAY = datetime.date.today().isoformat()

B54_CSS = '\n/* B54 restore original Thuenen legend swatch colors */\n.central-map-legend i,\n.central-stage-legend i,\n.map-legend i,\n[data-central-map-legend] i,\n[data-map-legend] i {\n  display: inline-block;\n  width: .72rem;\n  height: .44rem;\n  min-width: .72rem;\n  border-radius: 999px;\n  margin-right: .38rem;\n  vertical-align: -0.05rem;\n  border: 1px solid rgba(255, 255, 255, .25);\n  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .12);\n}\n\n.central-map-legend .legend-thuenen-extent,\n.central-stage-legend .legend-thuenen-extent,\n.map-legend .legend-thuenen-extent,\n[data-central-map-legend] .legend-thuenen-extent,\n[data-map-legend] .legend-thuenen-extent {\n  background: #2F6B4F !important;\n  background-color: #2F6B4F !important;\n}\n\n.central-map-legend .legend-thuenen-hh,\n.central-stage-legend .legend-thuenen-hh,\n.map-legend .legend-thuenen-hh,\n[data-central-map-legend] .legend-thuenen-hh,\n[data-map-legend] .legend-thuenen-hh {\n  background: #6E4B78 !important;\n  background-color: #6E4B78 !important;\n}\n\n.central-map-legend .legend-thuenen-mf,\n.central-stage-legend .legend-thuenen-mf,\n.map-legend .legend-thuenen-mf,\n[data-central-map-legend] .legend-thuenen-mf,\n[data-map-legend] .legend-thuenen-mf {\n  background: #8E7A4D !important;\n  background-color: #8E7A4D !important;\n}\n\n.central-map-legend .legend-thuenen-nh,\n.central-stage-legend .legend-thuenen-nh,\n.map-legend .legend-thuenen-nh,\n[data-central-map-legend] .legend-thuenen-nh,\n[data-map-legend] .legend-thuenen-nh {\n  background: #2F6B4F !important;\n  background-color: #2F6B4F !important;\n}\n\n.central-map-legend .legend-thuenen-tief-hh,\n.central-stage-legend .legend-thuenen-tief-hh,\n.map-legend .legend-thuenen-tief-hh,\n[data-central-map-legend] .legend-thuenen-tief-hh,\n[data-map-legend] .legend-thuenen-tief-hh {\n  background: #8A5A63 !important;\n  background-color: #8A5A63 !important;\n}\n\n.central-map-legend .legend-thuenen-tief-nh,\n.central-stage-legend .legend-thuenen-tief-nh,\n.map-legend .legend-thuenen-tief-nh,\n[data-central-map-legend] .legend-thuenen-tief-nh,\n[data-map-legend] .legend-thuenen-tief-nh {\n  background: #1F7A5C !important;\n  background-color: #1F7A5C !important;\n}\n\n.central-map-legend .legend-thuenen-flach-hh,\n.central-stage-legend .legend-thuenen-flach-hh,\n.map-legend .legend-thuenen-flach-hh,\n[data-central-map-legend] .legend-thuenen-flach-hh,\n[data-map-legend] .legend-thuenen-flach-hh {\n  background: #9B7F8D !important;\n  background-color: #9B7F8D !important;\n}\n\n.central-map-legend .legend-thuenen-flach-nh,\n.central-stage-legend .legend-thuenen-flach-nh,\n.map-legend .legend-thuenen-flach-nh,\n[data-central-map-legend] .legend-thuenen-flach-nh,\n[data-map-legend] .legend-thuenen-flach-nh {\n  background: #6F9A78 !important;\n  background-color: #6F9A78 !important;\n}\n\n.central-map-legend .legend-thuenen-maechtig-hh,\n.central-stage-legend .legend-thuenen-maechtig-hh,\n.map-legend .legend-thuenen-maechtig-hh,\n[data-central-map-legend] .legend-thuenen-maechtig-hh,\n[data-map-legend] .legend-thuenen-maechtig-hh {\n  background: #B08B6C !important;\n  background-color: #B08B6C !important;\n}\n\n.central-map-legend .legend-thuenen-maechtig-nh,\n.central-stage-legend .legend-thuenen-maechtig-nh,\n.map-legend .legend-thuenen-maechtig-nh,\n[data-central-map-legend] .legend-thuenen-maechtig-nh,\n[data-map-legend] .legend-thuenen-maechtig-nh {\n  background: #B7A15A !important;\n  background-color: #B7A15A !important;\n}\n'
DOC_TEMPLATE = '# B54 - Restore Original Thuenen Legend Colors\n\nDate: {date}\n\n## Issue\n\nB53 added an extra floating Germany legend. This was not intended. The intended fix is to keep the existing central legend and only make sure that its color swatches are visible.\n\n## Fix\n\n- Remove the B53 script tag from `index.html`.\n- Delete `src/germany_thuenen_legend_fix.js` if present.\n- Remove the B53 custom legend CSS block from `src/styles.css`.\n- Add B54 CSS rules that assign colors to the original `legend-thuenen-*` classes.\n\n## Expected result\n\n- No extra floating B53 Germany legend.\n- The original central legend remains.\n- The soil-type labels in the original legend now show their corresponding colors.\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_index(index: Path):
    text = read(index)
    before = text
    text = re.sub(r'\s*<script\s+src=["\']src/germany_thuenen_legend_fix\.js["\']>\s*</script>\s*', "\n", text)
    if text != before:
        write(index, text)
        return True
    return False

def remove_b53_css(styles: Path):
    text = read(styles)
    marker = "/* B53 Germany Thuenen distinction and custom legend */"
    if marker not in text:
        return False
    start = text.find(marker)
    # B53 was appended at the end in the previous patch.
    write(styles, text[:start].rstrip() + "\n")
    return True

def add_b54_css(styles: Path):
    text = read(styles)
    if "B54 restore original Thuenen legend swatch colors" in text:
        return False
    write(styles, text.rstrip() + "\n" + B54_CSS + "\n")
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    index = root / "index.html"
    styles = root / "src" / "styles.css"
    b53_js = root / "src" / "germany_thuenen_legend_fix.js"

    for p in [index, styles]:
        if not p.exists():
            raise SystemExit(f"Required file not found: {p}")

    changed_index = patch_index(index)
    removed_css = remove_b53_css(styles)
    added_css = add_b54_css(styles)

    deleted_js = False
    if b53_js.exists():
        b53_js.unlink()
        deleted_js = True

    write(root / "docs" / "B54_restore_original_thuenen_legend_colors.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B54 completed" not in done_text:
        done_text += f"- {TODAY}: Task B54 completed - removed B53 custom legend and restored original Thuenen legend colors.\n"
        write(done, done_text)

    print("B54 original Thuenen legend color fix complete.")
    print("Changed:")
    if changed_index:
        print("  index.html")
    if removed_css or added_css:
        print("  src/styles.css")
    if deleted_js:
        print("  deleted src/germany_thuenen_legend_fix.js")
    print("  docs/B54_restore_original_thuenen_legend_colors.md")
    print("  tasks/done.md")
    print()
    print("Checks:")
    print('  Select-String -Path index.html -Pattern "germany_thuenen_legend_fix"')
    print('  Select-String -Path src\\styles.css -Pattern "B54 restore original Thuenen|legend-thuenen-hh|legend-thuenen-maechtig-nh"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
