#!/usr/bin/env python3
r"""
55 - Fix original Thuenen legend swatches with inline swatch markup.

Run from repository root:
  python scripts\55_fix_thuenen_legend_inline_swatches.py

Purpose:
- Keep the existing central legend.
- Do not add a second/floating legend.
- Replace collapsed/unstyled <i class="legend-thuenen-*"></i> entries with robust inline swatches.
"""

from pathlib import Path
import datetime
import re

TODAY = datetime.date.today().isoformat()

B55_CSS = '\n/* B55 robust original legend layout for inline Thuenen swatches */\n.central-map-legend span,\n.central-stage-legend span,\n.map-legend span,\n[data-central-map-legend] span,\n[data-map-legend] span {\n  align-items: center;\n}\n\n.central-map-legend .legend-entry,\n.central-stage-legend .legend-entry,\n.map-legend .legend-entry,\n[data-central-map-legend] .legend-entry,\n[data-map-legend] .legend-entry {\n  display: inline-flex;\n  align-items: center;\n  gap: .28rem;\n  white-space: nowrap;\n}\n'
DOC_TEMPLATE = '# B55 - Fix Thuenen Legend Inline Swatches\n\nDate: {date}\n\n## Issue\n\nThe original central legend showed the Thuenen soil-type labels, but the associated color swatches remained invisible. B54 attempted to style the existing `legend-thuenen-*` classes via CSS, but the active legend markup/CSS did not expose the swatches correctly.\n\n## Fix\n\nThis patch keeps the original central legend and replaces the collapsed `<i class="legend-thuenen-*"></i>` markers in JavaScript legend templates with robust inline swatch markup.\n\nNo extra floating legend is created.\n\n## Files patched\n\n- `src/central_step_state_bridge.js`\n- `src/central_global_map_story.js` if matching legend markup exists\n- `src/central_layer_state_hardener.js` if matching legend markup exists\n- `src/styles.css`\n\n## Expected result\n\n- Original legend remains in its previous position.\n- Soil-type labels remain.\n- Each label now has a visible color swatch.\n'

SWATCHES = {
    "legend-thuenen-extent": ("#2F6B4F", "Thuenen peat / organic-soils Kulisse"),
    "legend-thuenen-hh": ("#6E4B78", "Hochmoorboden"),
    "legend-thuenen-nh": ("#2F6B4F", "Niedermoorboden"),
    "legend-thuenen-mf": ("#8E7A4D", "Moorfolgeboden"),
    "legend-thuenen-tief-hh": ("#8A5A63", "Tiefumbruchboden aus Hochmoor"),
    "legend-thuenen-tief-nh": ("#1F7A5C", "Tiefumbruchboden aus Niedermoor"),
    "legend-thuenen-flach-hh": ("#9B7F8D", "flach ueberdeckter Hochmoorboden"),
    "legend-thuenen-flach-nh": ("#6F9A78", "flach ueberdeckter Niedermoorboden"),
    "legend-thuenen-maechtig-hh": ("#B08B6C", "maechtig ueberdeckter Hochmoorboden"),
    "legend-thuenen-maechtig-nh": ("#B7A15A", "maechtig ueberdeckter Niedermoorboden"),
}

SWATCH_STYLE = (
    "display:inline-block;width:.72rem;height:.44rem;min-width:.72rem;"
    "border-radius:999px;margin-right:.38rem;vertical-align:-0.05rem;"
    "border:1px solid rgba(255,255,255,.25);"
)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def swatch_markup(class_name: str) -> str:
    color, _label = SWATCHES[class_name]
    return f'<span class="legend-swatch {class_name}" style="{SWATCH_STYLE}background:{color};background-color:{color};"></span>'

def patch_legend_i_markup(text: str) -> str:
    for class_name in SWATCHES:
        text = text.replace(f'<i class="{class_name}"></i>', swatch_markup(class_name))
        text = text.replace(f"<i class='{class_name}'></i>", swatch_markup(class_name))

    text = re.sub(
        r'<span>\s*(<span class="legend-swatch [^>]+></span>\s*[^<]+)\s*</span>',
        r'<span class="legend-entry">\1</span>',
        text
    )
    return text

def patch_file(path: Path) -> bool:
    if not path.exists():
        return False
    text = read(path)
    patched = patch_legend_i_markup(text)
    if patched != text:
        write(path, patched)
        return True
    return False

def patch_styles(path: Path) -> bool:
    text = read(path)
    if "B55 robust original legend layout" in text:
        return False
    write(path, text.rstrip() + "\n" + B55_CSS + "\n")
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    changed = []
    for rel in [
        "src/central_step_state_bridge.js",
        "src/central_global_map_story.js",
        "src/central_layer_state_hardener.js",
    ]:
        p = root / rel
        if patch_file(p):
            changed.append(rel)

    if patch_styles(root / "src" / "styles.css"):
        changed.append("src/styles.css")

    write(root / "docs" / "B55_fix_thuenen_legend_inline_swatches.md", DOC_TEMPLATE.format(date=TODAY))
    changed.append("docs/B55_fix_thuenen_legend_inline_swatches.md")

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B55 completed" not in done_text:
        done_text += f"- {TODAY}: Task B55 completed - fixed Thuenen legend inline color swatches.\n"
        write(done, done_text)
        changed.append("tasks/done.md")

    print("B55 Thuenen legend inline swatch fix complete.")
    print("Changed/created:")
    for rel in changed:
        print(" ", rel)
    print()
    print("Checks:")
    print('  Select-String -Path src\\central_step_state_bridge.js -Pattern "legend-swatch|legend-thuenen-hh|background:#6E4B78"')
    print('  Select-String -Path src\\styles.css -Pattern "B55 robust original legend layout"')
    print()
    print("Then hard reload browser with Ctrl+F5.")

if __name__ == "__main__":
    main()
