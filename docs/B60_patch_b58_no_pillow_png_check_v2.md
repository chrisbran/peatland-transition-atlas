# B60 - Patch B58 QA Without Pillow v2

Date: 2026-06-19

## Issue

B59 used a too strict regular expression and could not locate the `image_check()` block in the local `scripts/58_visual_qa_and_commit_check.py`.

The B58 report showed that the only blocking failures were caused by missing Pillow/PIL. The central scripts, central story states, and unwanted-reference checks were already OK. The only non-blocking warning was `data/external/` being visible in git status.

## Fix

B60 replaces the `image_check()` block using a more robust substring method:

- find `def image_check(path):`
- find `def collect_index_refs(index_text):`
- replace everything between them

The new image check tries Pillow first and falls back to a standard-library PNG IHDR check.

## Next step

Run:

```powershell
python scripts\60_patch_b58_no_pillow_png_check_v2.py
python scripts\58_visual_qa_and_commit_check.py
```
