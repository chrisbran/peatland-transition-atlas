from pathlib import Path
import re
import csv
from datetime import date

ROOT = Path(".")
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "scripts" / "153_map_role_and_redundancy_audit.py"
DOC = ROOT / "docs" / "B153_map_role_and_redundancy_audit.md"
CSV_OUT = ROOT / "docs" / "B153_map_role_inventory.csv"
AUDIT = ROOT / "docs" / "B153_map_role_and_redundancy_audit.txt"
DONE = ROOT / "tasks" / "done.md"

SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
HEADING_RE = re.compile(r"<h([1-4])\b[^>]*>(.*?)</h\1>", re.S | re.I)
IMG_RE = re.compile(r"<img\b[^>]*>", re.S | re.I)
IFRAME_RE = re.compile(r"<iframe\b[^>]*>", re.S | re.I)
SVG_RE = re.compile(r"<svg\b", re.I)

B149_START = "<!-- B149_FELT_DESKTOP_EMBED_MOBILE_FALLBACK_START -->"
B152_HINT = "Interaktive Vertiefung"

ROLE_PATTERNS = [
    ("global_context", ["globale moor", "world", "global", "moore sind räumlich konzentriert", "welt"]),
    ("frame_mismatch", ["maßstab", "klima", "regionale planung", "frame", "top-down"]),
    ("regional_static_story", ["oberschwaben, wo", "schnittmenge", "landwirtschaft trifft", "regionale karte"]),
    ("felt_interactive_deepening", ["felt", "interaktive vertiefung", "interaktive karte", "oberschwaben-felt-pilot"]),
    ("value_chain", ["wertschöpfung", "verarbeitung", "abnahme", "standards", "mengen"]),
    ("water_governance", ["wasser", "governance", "einzugsgebiet", "eigentu"]),
    ("method_sources", ["methode", "quellen", "nutzungsrechte", "datenquellen"]),
]

RECOMMENDED_ROLES = {
    "global_context": "Kontext: Relevanz und Maßstabswechsel vorbereiten.",
    "frame_mismatch": "Narrative Brücke: globale Klimabegründung trifft lokale Umsetzungslogik.",
    "regional_static_story": "Story-Karte: räumliche Einordnung der Schnittmenge im Lesefluss.",
    "felt_interactive_deepening": "Vertiefung: dieselbe Schnittmenge interaktiv, scharf und klickbar.",
    "value_chain": "These/Climax: Engpass hinter dem Feld sichtbar machen.",
    "water_governance": "Planungslogik: Parzelle/Betrieb/Wasser-Einheit trennen.",
    "method_sources": "Transparenz: Methodik, Quellen und Grenzen bündeln.",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_tags(html: str) -> str:
    text = TAG_RE.sub(" ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_attr(tag: str, attr: str) -> str:
    m = re.search(attr + r'\s*=\s*"([^"]*)"', tag, re.I)
    if m:
        return m.group(1)
    m = re.search(attr + r"\s*=\s*'([^']*)'", tag, re.I)
    if m:
        return m.group(1)
    return ""


def selector(open_tag: str) -> str:
    sid = extract_attr(open_tag, "id")
    cls = extract_attr(open_tag, "class")
    bits = []
    if sid:
        bits.append("#" + sid)
    if cls:
        bits.append("." + ".".join(cls.split()))
    return " ".join(bits) if bits else ""


def first_heading(section: str) -> str:
    m = HEADING_RE.search(section)
    if not m:
        return ""
    return strip_tags(m.group(2))


def classify_roles(text: str, raw_section: str) -> list[str]:
    t = text.lower()
    roles = []
    for role, patterns in ROLE_PATTERNS:
        if any(p in t or p in raw_section.lower() for p in patterns):
            roles.append(role)
    return roles


def role_summary(roles: list[str]) -> str:
    if not roles:
        return "Keine klare Karten-/Grafikrolle erkannt."
    return " | ".join(RECOMMENDED_ROLES.get(r, r) for r in roles)


def classify_redundancy(roles: list[str], text: str, has_img: bool, has_iframe: bool) -> str:
    t = text.lower()

    if "regional_static_story" in roles and "felt_interactive_deepening" in roles:
        return "potenzielle Dopplung: statische Story-Karte und interaktive Vertiefung im selben Abschnitt genau prüfen"
    if "regional_static_story" in roles:
        return "behalten: Einordnung im Lesefluss; nicht durch Felt ersetzen, solange Sticky/Story-Kontext gebraucht wird"
    if "felt_interactive_deepening" in roles:
        return "behalten: interaktive Vertiefung; klar als Detailschicht rahmen, nicht als zweite Hauptkarte"
    if "global_context" in roles and has_img:
        return "behalten: Kontext-/Maßstabskarte; nicht mit regionaler Detailkarte vermischen"
    if "value_chain" in roles:
        return "kein Kartenersatz: Wertschöpfungslogik bleibt separates Climax-Bild"
    if "water_governance" in roles:
        return "vorsichtig: schematische Planungsaussage, keine zusätzliche Detailkarte erzwingen"
    if has_iframe:
        return "prüfen: iframe ohne klare Rolle"
    if has_img or SVG_RE.search(text):
        return "prüfen: Grafik/Karte ohne eindeutige Rolle"
    return "niedrig"


def main() -> None:
    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    sections = list(SECTION_RE.finditer(html))

    rows = []
    for i, match in enumerate(sections, start=1):
        section = match.group(0)
        open_tag_m = re.match(r"<section\b[^>]*>", section, re.I | re.S)
        open_tag = open_tag_m.group(0) if open_tag_m else ""
        text = strip_tags(section)
        heading = first_heading(section)
        roles = classify_roles(text, section)
        has_img = bool(IMG_RE.search(section))
        has_iframe = bool(IFRAME_RE.search(section))
        has_svg = bool(SVG_RE.search(section))
        redundancy = classify_redundancy(roles, text, has_img, has_iframe)

        rows.append({
            "section_no": i,
            "selector": selector(open_tag),
            "heading": heading,
            "roles": "; ".join(roles),
            "has_img": has_img,
            "has_iframe": has_iframe,
            "has_svg": has_svg,
            "role_summary": role_summary(roles),
            "redundancy_note": redundancy,
            "excerpt": text[:260],
        })

    high_attention = [
        r for r in rows
        if "potenzielle Dopplung" in r["redundancy_note"]
        or "felt_interactive_deepening" in r["roles"]
        or "regional_static_story" in r["roles"]
    ]

    role_counts = {}
    for r in rows:
        for role in filter(None, r["roles"].split("; ")):
            role_counts[role] = role_counts.get(role, 0) + 1

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "section_no",
                "selector",
                "heading",
                "roles",
                "has_img",
                "has_iframe",
                "has_svg",
                "role_summary",
                "redundancy_note",
                "excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    today = date.today().isoformat()

    md = []
    md.append("# B153 - Map Role and Redundancy Audit")
    md.append("")
    md.append(f"Date: {today}")
    md.append("")
    md.append("## Ziel")
    md.append("")
    md.append("B153 prüft nach der Felt-Integration, welche Karten- und Grafikblöcke welche Rolle im Storyboard haben.")
    md.append("Der Patch verändert die öffentliche Seite nicht. Er dient als redaktionelles Audit, bevor weitere Kartenblöcke umgebaut werden.")
    md.append("")
    md.append("## Ergebnis")
    md.append("")
    md.append(f"- untersuchte Sections: {len(rows)}")
    md.append(f"- Sections mit besonderer Relevanz für Oberschwaben/Felt: {len(high_attention)}")
    md.append(f"- B149/Felt-Block im HTML erkannt: {'ja' if B149_START in html else 'nein'}")
    md.append(f"- B152-Rahmung `Interaktive Vertiefung` erkannt: {'ja' if B152_HINT in html else 'nein'}")
    md.append("")
    md.append("## Rollen-Zählung")
    md.append("")
    if role_counts:
        md.append("| Rolle | Anzahl |")
        md.append("|---|---:|")
        for role, count in sorted(role_counts.items()):
            md.append(f"| `{role}` | {count} |")
    else:
        md.append("Keine Rollen erkannt.")
    md.append("")
    md.append("## Relevante Karten-/Redundanzstellen")
    md.append("")
    if high_attention:
        md.append("| Nr. | Überschrift | Rolle | Audit-Notiz |")
        md.append("|---:|---|---|---|")
        for r in high_attention:
            heading = r["heading"] or "(ohne Überschrift)"
            md.append(f"| {r['section_no']} | {heading} | {r['roles']} | {r['redundancy_note']} |")
    else:
        md.append("Keine besonders relevanten Karten-/Redundanzstellen erkannt.")
    md.append("")
    md.append("## Redaktionelle Entscheidung nach B152")
    md.append("")
    md.append("Die bestehende Oberschwaben-Karte und die Felt-Karte sollten nicht gegeneinander ausgespielt werden.")
    md.append("")
    md.append("- **Statische Oberschwaben-Karte:** bleibt Story- und Orientierungskarte im Lesefluss.")
    md.append("- **Felt-Karte:** bleibt interaktive Vertiefung für Details, Popup und Vektorqualität.")
    md.append("- **Mobile:** Felt bleibt optional über externen Link; die Story darf nicht vom iframe abhängig werden.")
    md.append("")
    md.append("## Empfohlene nächste Schritte")
    md.append("")
    md.append("1. Keine weitere neue Karte hinzufügen, bevor die Rollen konsolidiert sind.")
    md.append("2. In B154 nur Abstände/Übergänge zwischen statischer Karte und Felt-Vertiefung feinjustieren, falls visuell nötig.")
    md.append("3. In B155 Veröffentlichungsgates aktualisieren: Felt-Lizenz, Datenschutz, Hohenheim/SOLAMO-BW-Freigabe, 19.900-ha-Methodennotiz.")
    md.append("4. Den großen Sticky-Zoom erst später als eigenen Strang behandeln.")
    md.append("")
    md.append("## Dateien")
    md.append("")
    md.append(f"- CSV-Inventar: `docs/{CSV_OUT.name}`")
    write(DOC, "\n".join(md) + "\n")

    audit_text = f"""# B153 map role and redundancy audit

Date: {today}

Result: AUDIT ONLY. No public page files changed.

Sections scanned: {len(rows)}
High-attention map/Felt sections: {len(high_attention)}
B149 block detected: {B149_START in html}
B152 framing detected: {B152_HINT in html}

Created/updated:

- docs/B153_map_role_and_redundancy_audit.md
- docs/B153_map_role_inventory.csv
- docs/B153_map_role_and_redundancy_audit.txt
- tasks/done.md
"""
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = "# Done\n"
    line = f"- B153 map role and redundancy audit: inventoried map/graphic roles after Felt integration and documented static-vs-interactive Oberschwaben roles ({today})."
    if "B153 map role and redundancy audit" not in done_text:
        write(DONE, done_text.rstrip() + "\n" + line + "\n")
    else:
        write(DONE, done_text)

    print("B153 map role and redundancy audit complete.")
    print("Audit only. No public page files changed.")
    print("Created/updated:")
    print("  docs/B153_map_role_and_redundancy_audit.md")
    print("  docs/B153_map_role_inventory.csv")
    print("  docs/B153_map_role_and_redundancy_audit.txt")
    print("  tasks/done.md")


if __name__ == "__main__":
    main()
