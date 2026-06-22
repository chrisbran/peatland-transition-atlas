from pathlib import Path
import subprocess

path = Path("src/central_global_map_story.js")

# Read the committed version directly from Git, so we avoid the corrupted working-copy encoding.
blob = subprocess.check_output(["git", "show", "HEAD:src/central_global_map_story.js"])
txt = blob.decode("utf-8-sig")

block = '''
  // B62 Baden-Wuerttemberg / BK50 states
  Object.assign(STATE_META, {
    "bw-context": {
      mode: "Baden-Wuerttemberg frame",
      title: "Baden-Wuerttemberg brings the national implementation frame to a regional planning scale.",
      legend: `
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BW frame: Baden-Wuerttemberg regional context exported from the same 16:9 ArcGIS map frame."
    },
    "bw-bk50-extent": {
      mode: "BK50 peat and wetland soils",
      title: "BK50 shows where peat and wetland soil contexts occur at regional scale.",
      legend: `
        <span><i class="legend-peat"></i>BK50 peat / wetland soil context</span>
        <span><i class="legend-border"></i>Regional frame</span>
      `,
      source: "BK50 BW layer: peat and wetland soil context shown as a single extent layer; no land-use or suitability classification is implied."
    }
  });

'''

marker = "\nfunction setState(state) {"

if marker not in txt:
    raise RuntimeError("Could not find setState marker in HEAD version of central_global_map_story.js")

if '"bw-context"' not in txt:
    txt = txt.replace(marker, "\n" + block + "function setState(state) {", 1)

path.write_text(txt, encoding="utf-8", newline="\n")
print("Rebuilt src/central_global_map_story.js from HEAD and inserted clean B62 BW block.")
