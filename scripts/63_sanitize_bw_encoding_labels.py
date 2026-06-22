from pathlib import Path

replacements = {
    "Baden-W├╝rttemberg": "Baden-Wuerttemberg",
    "Baden-WÃ¼rttemberg": "Baden-Wuerttemberg",
    "Baden-Württemberg": "Baden-Wuerttemberg",
    "BADEN-WÜRTTEMBERG": "BADEN-WUERTTEMBERG",
    "BADEN-WÜRTTEMBERG": "BADEN-WUERTTEMBERG",
    "BADEN-WÃœRTTEMBERG": "BADEN-WUERTTEMBERG",
    "BADEN-WÃ¼RTTEMBERG": "BADEN-WUERTTEMBERG",
}

targets = [
    Path("src/central_global_map_story.js"),
    Path("src/central_step_state_bridge.js"),
    Path("src/central_stage_label_fix.js"),
]

changed = []

for path in targets:
    txt = path.read_text(encoding="utf-8")
    old = txt
    for bad, good in replacements.items():
        txt = txt.replace(bad, good)
    if txt != old:
        path.write_text(txt, encoding="utf-8", newline="\n")
        changed.append(str(path))

print("Sanitized files:")
for p in changed:
    print(" ", p)
