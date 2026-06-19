#!/usr/bin/env python3
r"""
60 - Patch B58 visual QA to work without Pillow, robust replacement.

Run from repository root:
  python scripts\60_patch_b58_no_pillow_png_check_v2.py
"""

from pathlib import Path
import datetime

TODAY = datetime.date.today().isoformat()

NEW_IMAGE_CHECK = 'def png_header_check(path):\n    """Return (status, detail) for PNG dimensions/RGBA using only stdlib."""\n    try:\n        with open(path, "rb") as f:\n            sig = f.read(8)\n            if sig != b"\\x89PNG\\r\\n\\x1a\\n":\n                return ("FAIL", "not a PNG file")\n            length = int.from_bytes(f.read(4), "big")\n            chunk_type = f.read(4)\n            if chunk_type != b"IHDR" or length < 13:\n                return ("FAIL", "PNG IHDR chunk not found")\n            data = f.read(13)\n            width = int.from_bytes(data[0:4], "big")\n            height = int.from_bytes(data[4:8], "big")\n            bit_depth = data[8]\n            color_type = data[9]\n            # PNG color type 6 = truecolor with alpha, equivalent to RGBA export.\n            if (width, height) != (1600, 900):\n                return ("FAIL", f"PNG header size=({width}, {height}), expected (1600, 900)")\n            if color_type != 6:\n                return ("FAIL", f"PNG header color_type={color_type}, expected 6/RGBA")\n            return ("OK", f"PNG header RGBA ({width}, {height}) bit_depth={bit_depth}")\n    except Exception as exc:\n        return ("FAIL", f"Could not read PNG header: {exc}")\n\ndef image_check(path):\n    """Check image dimensions and alpha; use Pillow if available, stdlib PNG check otherwise."""\n    try:\n        from PIL import Image\n        try:\n            with Image.open(path) as img:\n                mode = img.mode\n                size = img.size\n                alpha = None\n                if mode == "RGBA":\n                    alpha = img.getchannel("A").getextrema()\n                if size != (1600, 900):\n                    return ("FAIL", f"{mode} {size}, expected (1600, 900)")\n                if mode != "RGBA":\n                    return ("FAIL", f"{mode} {size}, expected RGBA")\n                return ("OK", f"{mode} {size} alpha={alpha}")\n        except Exception as exc:\n            return ("FAIL", f"Could not open image with Pillow: {exc}")\n    except ImportError:\n        return png_header_check(path)\n'
DOC_TEMPLATE = '# B60 - Patch B58 QA Without Pillow v2\n\nDate: {date}\n\n## Issue\n\nB59 used a too strict regular expression and could not locate the `image_check()` block in the local `scripts/58_visual_qa_and_commit_check.py`.\n\nThe B58 report showed that the only blocking failures were caused by missing Pillow/PIL. The central scripts, central story states, and unwanted-reference checks were already OK. The only non-blocking warning was `data/external/` being visible in git status.\n\n## Fix\n\nB60 replaces the `image_check()` block using a more robust substring method:\n\n- find `def image_check(path):`\n- find `def collect_index_refs(index_text):`\n- replace everything between them\n\nThe new image check tries Pillow first and falls back to a standard-library PNG IHDR check.\n\n## Next step\n\nRun:\n\n```powershell\npython scripts\\60_patch_b58_no_pillow_png_check_v2.py\npython scripts\\58_visual_qa_and_commit_check.py\n```\n'

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_b58(path: Path) -> bool:
    text = read(path)

    if "def png_header_check(path):" in text and "PNG header RGBA" in text:
        return False

    start = text.find("def image_check(path):")
    if start == -1:
        raise SystemExit("Could not find 'def image_check(path):' in scripts/58_visual_qa_and_commit_check.py.")

    end_marker = "\ndef collect_index_refs(index_text):"
    end = text.find(end_marker, start)
    if end == -1:
        fallback = text.find("def collect_index_refs(index_text):", start)
        if fallback == -1:
            excerpt = text[start:start+1200]
            raise SystemExit(
                "Could not find 'def collect_index_refs(index_text):' after image_check(). "
                "Excerpt:\n" + excerpt
            )
        end = fallback
    else:
        end = end + 1

    patched = text[:start] + NEW_IMAGE_CHECK.rstrip() + "\n\n" + text[end:]
    write(path, patched)
    return True

def main():
    root = Path.cwd()
    if not (root / "index.html").exists():
        raise SystemExit("Run from repository root. index.html not found.")

    b58 = root / "scripts" / "58_visual_qa_and_commit_check.py"
    if not b58.exists():
        raise SystemExit("scripts/58_visual_qa_and_commit_check.py not found.")

    changed = patch_b58(b58)

    write(root / "docs" / "B60_patch_b58_no_pillow_png_check_v2.md", DOC_TEMPLATE.format(date=TODAY))

    done = root / "tasks" / "done.md"
    done_text = read(done) if done.exists() else "# Done\n"
    if "Task B60 completed" not in done_text:
        done_text += f"- {TODAY}: Task B60 completed - patched B58 QA with robust no-Pillow PNG header check.\n"
        write(done, done_text)

    print("B60 patched B58 no-Pillow PNG check with robust replacement.")
    if changed:
        print("Changed: scripts/58_visual_qa_and_commit_check.py")
    else:
        print("scripts/58_visual_qa_and_commit_check.py was already patched.")
    print("Created/updated:")
    print("  docs/B60_patch_b58_no_pillow_png_check_v2.md")
    print("  tasks/done.md")
    print()
    print("Now rerun:")
    print("  python scripts\\58_visual_qa_and_commit_check.py")

if __name__ == "__main__":
    main()
