from pathlib import Path
import subprocess

targets = {
    "src/central_step_state_bridge.js": {
        "Baden-Württemberg": "Baden-Wuerttemberg",
        "Baden-WÃ¼rttemberg": "Baden-Wuerttemberg",
        "Baden-W├╝rttemberg": "Baden-Wuerttemberg",
    },
    "src/central_stage_label_fix.js": {
        "BADEN-WÜRTTEMBERG": "BADEN-WUERTTEMBERG",
        "BADEN-WÜRTTEMBERG": "BADEN-WUERTTEMBERG",
        "BADEN-WÃœRTTEMBERG": "BADEN-WUERTTEMBERG",
        "BADEN-WÃ¼RTTEMBERG": "BADEN-WUERTTEMBERG",
    },
}

for rel, replacements in targets.items():
    blob = subprocess.check_output(["git", "show", f"HEAD:{rel}"])
    txt = blob.decode("utf-8-sig")
    for bad, good in replacements.items():
        txt = txt.replace(bad, good)
    txt = txt.rstrip() + "\n"
    Path(rel).write_text(txt, encoding="utf-8", newline="\n")
    print(f"Rebuilt clean: {rel}")
