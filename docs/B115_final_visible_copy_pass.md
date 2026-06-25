# B115 – Final Visible Copy Pass

Stand: 2026-06-25

Status: **OK**

## Scope

B115 performs a conservative final copy pass and no-overclaim audit for the restored FIONA-based public page.

It does not change:

- map paths;
- map images;
- CSS/layout;
- data processing;
- the parked LGL branch.

## Changed files

- `docs/B115_final_visible_copy_pass.md`
- `docs/B115_visible_copy_audit.txt`
- `docs/B115_visible_copy_findings.csv`
- `tasks/done.md`

## Summary

| Check | Count |
|---|---:|
| Targeted replacements applied | 0 |
| Risk patterns remaining in visible text | 0 |
| Required safe/caveat patterns missing | 0 |
| Watch terms present | 5 |

## Interpretation

A `WATCH` term is not automatically a problem. For example, `Maßnahme` or `Potenzial` can appear in a negated caveat or a general explanatory context. Remaining `WATCH` terms should be reviewed in `docs/B115_visible_copy_findings.csv`.

A `REVIEW` risk pattern should be inspected before release.

## Core public-copy rule

The page may say:

```text
Die Karten zeigen räumliche Orientierung, Schnittmengen und Planungskontexte.
```

The page should not say:

```text
Die Karten zeigen geeignete Flächen, Prioritätsflächen oder Wiedervernässungspotenzial.
```

## Next step

If the audit status is OK, proceed to browser-responsive QA and final release review.

If `REVIEW REQUIRED`, inspect:

```powershell
Import-Csv docs\B115_visible_copy_findings.csv -Delimiter ';' | Format-Table -Auto
```
