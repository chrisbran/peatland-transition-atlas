# B116 – Deployment Checklist

Stand: 2026-06-25

## 1. Pre-deployment checks

Run:

```powershell
cd C:\Users\User\Documents\GitHub\peatland-transition-atlas

python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py

Select-String -Path index.html -Pattern "oberschwaben_lgl","Datenquelle in Umstellung","B98c","Flächen-QA","FIONA 2024","~19.900"

git status --short
```

Expected:

```text
B103b: no public source files changed
B58: RESULT: PASS
No oberschwaben_lgl / Datenquelle in Umstellung / B98c / Flächen-QA in index.html
FIONA 2024 and ~19.900 present
No raw/working data staged
```

## 2. Manual browser check

Run local server:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/index.html
```

Check at least:

```text
1440 × 900
1280 × 800
1024 × 768
390 × 844
```

Use:

```text
docs/B114_manual_test_matrix.csv
```

## 3. Commit release-candidate docs

After B116 generation:

```powershell
git add scripts\116_release_candidate_state_and_deployment_check.py docs\B116_release_candidate_state.md docs\B116_deployment_checklist.md docs\B116_release_candidate_audit.txt tasks\done.md

git commit -m "Add release candidate state and deployment checklist"
```

If `docs/B58_visual_qa_and_commit_check.md` was modified by the final QA and you want to preserve the PASS state:

```powershell
git add docs\B58_visual_qa_and_commit_check.md
git commit -m "Update final visual QA report"
```

## 4. Push

Only after confirming `git status --short` contains no accidental staged raw/probe material:

```powershell
git push
```

## 5. Post-deployment check

After GitHub Pages updates, open the public URL:

```text
https://chrisbran.github.io/peatland-transition-atlas/
```

Check:

- page loads without missing map images;
- Oberschwaben FIONA/BK50 section appears;
- no LGL test layer appears;
- source note and caveat are visible;
- scroll behaviour matches local version.

## 6. Release note for project team

Suggested short internal release note:

```text
The current Moore / Peatland Transition Atlas demo has been stabilized around the restored FIONA/BK50/GISCO Oberschwaben story. Visual QA and visible-copy audits pass. The map should be treated as a spatial orientation and discussion layer, not a site-level suitability or priority map. FIONA derivative-publication rights and source-method appendices remain to be clarified before broader public dissemination.
```
