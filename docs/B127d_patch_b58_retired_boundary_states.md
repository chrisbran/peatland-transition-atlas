# B127d – Patch B58 Retired Boundary States

Stand: 2026-06-29

Status: **OK**

## Ziel

B127d aktualisiert die B58-QA nach der Straffung der zentralen Kartenfolge.

## Änderungen

- inserted_constant: 1
- patched_loop: 0
- loop_status: for_state_loop_not_found
- removed_expected_list_lines: 2
- Constant count: 1
- Loop filter count: 0

## Review commands

```powershell
Get-Content docs\B127d_patch_b58_retired_boundary_states_audit.txt -Encoding UTF8
Select-String -Encoding UTF8 -Path scripts\58_visual_qa_and_commit_check.py -Pattern "B127_RETIRED_CENTRAL_STATES","State not fully wired","europe-borders","germany-context","bw-context"
python scripts\58_visual_qa_and_commit_check.py
```
## B127e resolution note

B58 passes after removing the retired boundary-only states from the expected state list. `Loop filter count: 0` is acceptable here because the current B58 implementation uses explicit expected-state entries rather than the generic loop pattern anticipated by B127d.
