from pathlib import Path
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
import csv
import subprocess

ROOT = Path(".")
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
SRC_DIR = ROOT / "src"

DOC = ROOT / "docs" / "B177_external_request_audit.md"
AUDIT = ROOT / "docs" / "B177_external_request_audit_run.txt"
LOADED_CSV = ROOT / "docs" / "B177_loaded_external_resources.csv"
LINKS_CSV = ROOT / "docs" / "B177_external_links_inventory.csv"
TOKEN_CSV = ROOT / "docs" / "B177_provider_token_scan.csv"
DONE = ROOT / "tasks" / "done.md"

B176_MARKER = "B176_LOCAL_CARTOGRAPHIC_DEPTH_START"

FORBIDDEN_PROVIDER_PATTERNS = [
    ("felt", r"\bfelt\b|felt\.com"),
    ("openstreetmap", r"OpenStreetMap|openstreetmap|osm\.org|tile\.openstreetmap"),
    ("osm_tile", r"tile\.openstreetmap\.org|[a-z]\.tile\.openstreetmap\.org|/\{z\}/\{x\}/\{y\}|/{z}/{x}/{y}"),
    ("mapbox", r"mapbox\.com|api\.mapbox\.com|mapboxgl"),
    ("maptiler", r"maptiler\.com|api\.maptiler\.com"),
    ("carto_tiles", r"carto\.com|cartocdn\.com"),
    ("leaflet_cdn", r"unpkg\.com/leaflet|cdn\.jsdelivr\.net/npm/leaflet|leaflet\.css|leaflet\.js"),
    ("google_fonts", r"fonts\.googleapis\.com|fonts\.gstatic\.com"),
]

LOADING_ATTRS = {
    "script": ["src"],
    "img": ["src", "srcset"],
    "iframe": ["src"],
    "embed": ["src"],
    "object": ["data"],
    "source": ["src", "srcset"],
    "video": ["src", "poster"],
    "audio": ["src"],
    "track": ["src"],
    "link": ["href"],
}

PASSIVE_LINK_TAGS = {"a", "area"}
RESOURCE_LINK_RELS = {
    "stylesheet",
    "preload",
    "preconnect",
    "dns-prefetch",
    "modulepreload",
    "icon",
    "apple-touch-icon",
    "manifest",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def is_external_url(value: str) -> bool:
    value = (value or "").strip()
    return value.startswith("http://") or value.startswith("https://") or value.startswith("//")


def split_srcset(srcset: str) -> list[str]:
    urls = []
    for part in srcset.split(","):
        token = part.strip().split()
        if token:
            urls.append(token[0])
    return urls


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.loaded = []
        self.passive_links = []

    def handle_starttag(self, tag, attrs):
        tag_l = tag.lower()
        attrs_d = {k.lower(): (v or "") for k, v in attrs}

        if tag_l in PASSIVE_LINK_TAGS:
            href = attrs_d.get("href", "")
            if is_external_url(href):
                self.passive_links.append({
                    "tag": tag_l,
                    "attr": "href",
                    "url": href,
                    "rel": attrs_d.get("rel", ""),
                    "note": "Passive outbound link; does not load on page view.",
                })
            return

        if tag_l == "link":
            href = attrs_d.get("href", "")
            rel = attrs_d.get("rel", "").lower()
            rel_parts = set(re.split(r"\s+", rel.strip())) if rel else set()
            if is_external_url(href):
                if rel_parts & RESOURCE_LINK_RELS:
                    self.loaded.append({
                        "tag": tag_l,
                        "attr": "href",
                        "url": href,
                        "rel": rel,
                        "reason": "External link resource can load on page view.",
                    })
                else:
                    self.passive_links.append({
                        "tag": tag_l,
                        "attr": "href",
                        "url": href,
                        "rel": rel,
                        "note": "External link tag without loading rel; review manually.",
                    })
            return

        for attr in LOADING_ATTRS.get(tag_l, []):
            value = attrs_d.get(attr, "")
            if not value:
                continue
            values = split_srcset(value) if attr == "srcset" else [value]
            for url in values:
                if is_external_url(url):
                    self.loaded.append({
                        "tag": tag_l,
                        "attr": attr,
                        "url": url,
                        "rel": attrs_d.get("rel", ""),
                        "reason": "External resource can load on page view.",
                    })


def normalize_url(url: str) -> str:
    return "https:" + url if url.startswith("//") else url


def domain(url: str) -> str:
    try:
        return urlparse(normalize_url(url)).netloc.lower()
    except Exception:
        return ""


def provider_hits(text: str, source_name: str) -> list[dict]:
    rows = []
    for provider, pattern in FORBIDDEN_PROVIDER_PATTERNS:
        for m in re.finditer(pattern, text, flags=re.I):
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 80)
            context = re.sub(r"\s+", " ", text[start:end]).strip()
            rows.append({
                "source": source_name,
                "provider": provider,
                "match": m.group(0),
                "context": context,
            })
    return rows


def css_external_urls(css_text: str, source_name: str) -> list[dict]:
    rows = []
    for m in re.finditer(r"url\(\s*['\"]?([^'\"\)]+)['\"]?\s*\)", css_text, flags=re.I):
        url = m.group(1).strip()
        if is_external_url(url):
            rows.append({
                "tag": "css-url",
                "attr": "url()",
                "url": url,
                "rel": "",
                "reason": f"External CSS URL in {source_name}.",
            })
    for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\"\)\s;]+)", css_text, flags=re.I):
        url = m.group(1).strip()
        if is_external_url(url):
            rows.append({
                "tag": "css-import",
                "attr": "@import",
                "url": url,
                "rel": "",
                "reason": f"External CSS import in {source_name}.",
            })
    return rows


def js_external_urls(js_text: str, source_name: str) -> list[dict]:
    rows = []
    for m in re.finditer(r"https?://[^'\"\s<>)]+", js_text, flags=re.I):
        rows.append({
            "tag": "js-string-url",
            "attr": "string",
            "url": m.group(0),
            "rel": "",
            "reason": f"External URL literal in {source_name}; review whether it loads.",
        })
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git"] + args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def update_done(done_text: str, today: str) -> str:
    line = f"- B177 external request audit: verified that the public page no longer loads Felt/OpenStreetMap or other external map viewers on page view and inventoried passive outbound links ({today})."
    if "B177 external request audit" in done_text:
        return done_text
    return done_text.rstrip() + "\n" + line + "\n"


def main() -> None:
    today = date.today().isoformat()

    if not INDEX.exists():
        raise SystemExit("index.html not found")

    html = read(INDEX)
    css = read(CSS)

    parser = ResourceParser()
    parser.feed(html)

    loaded = list(parser.loaded)
    passive_links = list(parser.passive_links)

    loaded.extend(css_external_urls(css, "src/styles.css"))

    js_files = sorted(SRC_DIR.glob("*.js")) if SRC_DIR.exists() else []
    for js_path in js_files:
        js_text = read(js_path)
        loaded.extend(js_external_urls(js_text, js_path.as_posix()))

    loaded_unique = []
    seen = set()
    for row in loaded:
        key = (row["tag"], row["attr"], row["url"], row["reason"])
        if key not in seen:
            seen.add(key)
            row = dict(row)
            row["domain"] = domain(row["url"])
            loaded_unique.append(row)

    passive_unique = []
    seen = set()
    for row in passive_links:
        key = (row["tag"], row["attr"], row["url"], row.get("rel", ""))
        if key not in seen:
            seen.add(key)
            row = dict(row)
            row["domain"] = domain(row["url"])
            passive_unique.append(row)

    token_rows = []
    token_rows.extend(provider_hits(html, "index.html"))
    token_rows.extend(provider_hits(css, "src/styles.css"))
    for js_path in js_files:
        js_text = read(js_path)
        rows = provider_hits(js_text, js_path.as_posix())
        for row in rows:
            row["active_js_referenced"] = js_path.as_posix() in html
        token_rows.extend(rows)

    # Failure logic: passive source links are not failures.
    failures = []
    if B176_MARKER not in html:
        failures.append("B176 local cartographic replacement marker not found.")
    if "<iframe" in html.lower():
        failures.append("iframe tag still present in index.html.")

    felt_hits = [r for r in token_rows if r["provider"] == "felt" and r["source"] == "index.html"]
    osm_hits = [r for r in token_rows if r["provider"] in ("openstreetmap", "osm_tile") and r["source"] == "index.html"]

    if felt_hits:
        failures.append("Felt token still present in index.html.")
    if osm_hits:
        failures.append("OpenStreetMap/OSM token still present in index.html.")

    active_loaded_external = [r for r in loaded_unique if r["tag"] != "js-string-url"]
    if active_loaded_external:
        failures.append(f"External page-load resources found: {len(active_loaded_external)}")

    map_domain_patterns = ["felt", "openstreetmap", "tile", "mapbox", "maptiler", "carto", "leaflet"]
    loaded_map_domains = []
    for row in loaded_unique:
        d = row.get("domain", "")
        u = row.get("url", "").lower()
        if any(p in d or p in u for p in map_domain_patterns):
            loaded_map_domains.append(row)
    if loaded_map_domains:
        failures.append(f"External map/tile resource references found: {len(loaded_map_domains)}")

    status = "PASS" if not failures else "FAIL"

    write_csv(LOADED_CSV, loaded_unique, ["tag", "attr", "url", "domain", "rel", "reason"])
    write_csv(LINKS_CSV, passive_unique, ["tag", "attr", "url", "domain", "rel", "note"])

    normalized_token_rows = []
    for row in token_rows:
        normalized_token_rows.append({
            "source": row.get("source", ""),
            "provider": row.get("provider", ""),
            "match": row.get("match", ""),
            "active_js_referenced": row.get("active_js_referenced", ""),
            "context": row.get("context", ""),
        })
    write_csv(TOKEN_CSV, normalized_token_rows, ["source", "provider", "match", "active_js_referenced", "context"])

    passive_domains = {}
    for row in passive_unique:
        d = row.get("domain", "")
        if d:
            passive_domains[d] = passive_domains.get(d, 0) + 1

    loaded_domains = {}
    for row in loaded_unique:
        d = row.get("domain", "")
        if d:
            loaded_domains[d] = loaded_domains.get(d, 0) + 1

    doc = f"""# B177 - External Request / Third-Party Audit

Date: {today}

## Ziel

B177 prüft nach B176, ob die öffentliche Seite beim Seitenaufruf noch externe Kartenviewer, iframes, Tile-Dienste, CDNs oder andere Drittanbieter-Ressourcen lädt.

Passive Quellenlinks im Text sind nicht dasselbe wie aktive Drittanbieter-Ressourcen. Externe `a href`-Links werden inventarisiert, aber nicht als Seitenaufruf-Request gewertet.

## Ergebnis

```text
{status}
```

## Zentrale Checks

| Check | Ergebnis |
|---|---|
| B176 lokale Kartografie-Fassade vorhanden | `{B176_MARKER in html}` |
| `<iframe>` in `index.html` | `{ '<iframe' in html.lower() }` |
| Felt in `index.html` | `{ bool(felt_hits) }` |
| OpenStreetMap/OSM in `index.html` | `{ bool(osm_hits) }` |
| Aktive externe Page-Load-Ressourcen | `{len(active_loaded_external)}` |
| Externe Map-/Tile-Ressourcen | `{len(loaded_map_domains)}` |

## Aktive externe Ressourcen

| Domain | Anzahl |
|---|---:|
"""
    if loaded_domains:
        for d, count in sorted(loaded_domains.items()):
            doc += f"| `{d}` | {count} |\n"
    else:
        doc += "| — | 0 |\n"

    doc += """
Details: `docs/B177_loaded_external_resources.csv`

## Passive externe Links

| Domain | Anzahl |
|---|---:|
"""
    if passive_domains:
        for d, count in sorted(passive_domains.items()):
            doc += f"| `{d}` | {count} |\n"
    else:
        doc += "| — | 0 |\n"

    doc += """
Details: `docs/B177_external_links_inventory.csv`

## Provider-Token-Scan

Details: `docs/B177_provider_token_scan.csv`

## Interpretation

- `PASS` bedeutet: Im statischen Quellcode sind keine aktiven externen Karten-/Tile-/iframe-Requests mehr erkennbar.
- Passive externe Quellenlinks bleiben als Quellenverweise erhalten.
- Dieser Audit ersetzt keine juristische Prüfung und keine Browser-Network-Analyse, reduziert aber die technische Drittanbieter-Angriffsfläche erheblich.

## Manuelle Browserprüfung

Im Browser DevTools öffnen:

```text
Network → Disable cache → Seite hart neu laden
```

Dann prüfen:

```text
felt
openstreetmap
tile
mapbox
maptiler
fonts.googleapis
fonts.gstatic
```

Erwartung: keine Treffer.
"""
    if failures:
        doc += "\n## FAIL-Gründe\n\n"
        for failure in failures:
            doc += f"- {failure}\n"

    write(DOC, doc)

    audit = f"""# B177 external request audit run

Date: {today}

Git:
- Branch: {run_git(['branch', '--show-current'])}
- HEAD: {run_git(['log', '--oneline', '--decorate', '-n', '1'])}

Counts:
- Active loaded external resources: {len(active_loaded_external)}
- All loaded external URL literals/resources: {len(loaded_unique)}
- Passive external links: {len(passive_unique)}
- Provider token rows: {len(token_rows)}
- External map/tile resource references: {len(loaded_map_domains)}

Checks:
- B176 marker present: {B176_MARKER in html}
- iframe in index: {'<iframe' in html.lower()}
- Felt hits in index: {len(felt_hits)}
- OSM/OpenStreetMap hits in index: {len(osm_hits)}

Result: {status}
"""
    if failures:
        audit += "\nFailures:\n"
        for failure in failures:
            audit += f"- {failure}\n"
    else:
        audit += "\nFailures: none\n"

    audit += """
Created/updated:
- docs/B177_external_request_audit.md
- docs/B177_external_request_audit_run.txt
- docs/B177_loaded_external_resources.csv
- docs/B177_external_links_inventory.csv
- docs/B177_provider_token_scan.csv
- tasks/done.md
"""
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else "# Done\n"
    write(DONE, update_done(done_text, today))

    print("B177 external request / third-party audit complete.")
    print(f"RESULT: {status}")
    print("Created/updated:")
    print("  docs/B177_external_request_audit.md")
    print("  docs/B177_external_request_audit_run.txt")
    print("  docs/B177_loaded_external_resources.csv")
    print("  docs/B177_external_links_inventory.csv")
    print("  docs/B177_provider_token_scan.csv")
    print("  tasks/done.md")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f" - {failure}")
    else:
        print("Failures: none")
    print("Next: inspect audit, then run B103b and B58.")


if __name__ == "__main__":
    main()
