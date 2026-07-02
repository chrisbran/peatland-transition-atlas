from pathlib import Path
from datetime import date
import re
import csv

ROOT = Path('.')
INDEX = ROOT / 'index.html'
CSS = ROOT / 'src' / 'styles.css'
DOC = ROOT / 'docs' / 'B176_remove_felt_from_public_page.md'
AUDIT = ROOT / 'docs' / 'B176_remove_felt_from_public_page_audit.txt'
CSV_OUT = ROOT / 'docs' / 'B176_removed_felt_fragments.csv'
DONE = ROOT / 'tasks' / 'done.md'

B176_START = '<!-- B176_LOCAL_CARTOGRAPHIC_DEPTH_START -->'
B176_END = '<!-- /B176_LOCAL_CARTOGRAPHIC_DEPTH_END -->'
CSS_START = '/* B176_REMOVE_FELT_FROM_PUBLIC_PAGE_START */'
CSS_END = '/* B176_REMOVE_FELT_FROM_PUBLIC_PAGE_END */'

LOCAL_DEPTH_HTML = f'''{B176_START}
<section class="b176-local-cartographic-depth" aria-labelledby="b176-local-cartographic-depth-title">
  <div class="b176-local-cartographic-depth__inner">
    <p class="b176-local-cartographic-depth__kicker">Kartografische Vertiefung</p>
    <h2 id="b176-local-cartographic-depth-title">Die Detailkarte bleibt lokal</h2>
    <p class="b176-local-cartographic-depth__lead">
      Die Detailkarte bleibt bewusst eine lokale, redaktionelle Grafik: Sie zeigt
      die Schnittmenge aus heutiger Nutzung und Moor-/Feuchtbodenkontext, ohne beim
      Seitenaufruf einen externen Kartendienst zu laden.
    </p>
    <p class="b176-local-cartographic-depth__source">
      Eigene GIS-Aufbereitung aus FIONA 2024, BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024;
      Darstellung als lokale Kartengrafik. Methodische Grenzen siehe <a href="#methode">Methode in Kürze</a>.
    </p>
    <p class="b176-local-cartographic-depth__next">
      Nach der Karte folgt die Bilanz: Wie groß ist die Schnittmenge, und welche Nutzung dominiert?
    </p>
  </div>
</section>
{B176_END}'''

SOURCE_ROW_HTML = '''<tr>
  <td>Lokale Oberschwaben-Kartengrafiken</td>
  <td>Eigene Auswahl, Klassifikation, Verschneidung und kartografische Darstellung; keine externe Karten- oder Tile-Einbindung beim Seitenaufruf.</td>
  <td>Eigene GIS-Aufbereitung aus FIONA 2024, BK50-Moor-/Feuchtbodenkontext und GISCO NUTS 2024; lokale Darstellung als redaktionelle Kartengrafik.</td>
</tr>'''

ROWS = []

def read(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def record(kind: str, status: str, detail: str) -> None:
    ROWS.append({'kind': kind, 'status': status, 'detail': detail})

def strip_block(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r'.*?' + re.escape(end) + r'\s*', '', text, flags=re.S)

def replace_felt_section(html: str) -> str:
    html = strip_block(html, B176_START, B176_END)
    matches = list(re.finditer(r'<section\b[^>]*>.*?</section>', html, flags=re.I | re.S))
    candidates = []
    for m in matches:
        block = m.group(0)
        low = block.lower()
        if ('interaktive vertiefung' in low or 'felt' in low or 'openstreetmap' in low) and not any(x in low for x in ['quellen, methodik', 'datengrundlagen', 'quellenvermerke']):
            candidates.append(m)
    for m in candidates:
        block = m.group(0)
        low = block.lower()
        if 'flächenbilanz' not in low and 'die schnittmenge zeigt die größenordnung' not in low and len(block) < 16000:
            record('felt_section', 'replaced', 'Replaced compact public Felt/interaktive Vertiefung section.')
            return html[:m.start()] + LOCAL_DEPTH_HTML + '\n' + html[m.end():]

    # Fallback: remove a fragment starting at the Interaktive-Vertiefung heading but do not cross Flächenbilanz.
    h = re.search(r'<h[1-4]\b[^>]*>\s*Interaktive\s+Vertiefung\s*</h[1-4]>', html, flags=re.I | re.S)
    if not h:
        h = re.search(r'Interaktive\s+Vertiefung', html, flags=re.I)
    if h:
        start = html.rfind('<section', 0, h.start())
        if start < 0:
            start = h.start()
        stops = []
        for pat in [r'<h[1-4]\b[^>]*>\s*Flächenbilanz\s*</h[1-4]>', r'<h[1-4]\b[^>]*>\s*Die\s+Schnittmenge\s+zeigt\s+die\s+Größenordnung\s*</h[1-4]>', r'Flächenbilanz']:
            sm = re.search(pat, html[h.end():], flags=re.I | re.S)
            if sm:
                stops.append(h.end() + sm.start())
        end = min(stops) if stops else html.find('</section>', h.end())
        if end < 0:
            end = h.end()
        section_close = html.find('</section>', h.end())
        if section_close >= 0 and (not stops or section_close < min(stops)):
            end = section_close + len('</section>')
        record('felt_fragment', 'replaced', 'Fallback replacement from Interaktive Vertiefung to next area-balance boundary.')
        return html[:start] + LOCAL_DEPTH_HTML + '\n' + html[end:]

    record('felt_section', 'not_found', 'No public Felt/interaktive Vertiefung section found.')
    return html

def remove_iframes(html: str) -> str:
    def repl(m: re.Match) -> str:
        record('iframe', 'removed', m.group(0)[:200].replace('\n', ' '))
        return ''
    patched, n = re.subn(r'<iframe\b.*?</iframe>\s*', repl, html, flags=re.I | re.S)
    if n == 0:
        record('iframe', 'none', 'No iframe tags found.')
    return patched

def remove_felt_links(html: str) -> str:
    def repl(m: re.Match) -> str:
        record('felt_link', 'removed', m.group(0)[:200].replace('\n', ' '))
        return ''
    patched, n = re.subn(r'<a\b[^>]*href\s*=\s*[\'\"][^\'\"]*felt[^\'\"]*[\'\"][^>]*>.*?</a>\s*', repl, html, flags=re.I | re.S)
    if n == 0:
        record('felt_link', 'none', 'No Felt anchor tags found.')
    return patched

def patch_source_register(html: str) -> str:
    def repl_row(m: re.Match) -> str:
        row = m.group(0)
        if 'felt' in row.lower() or 'openstreetmap' in row.lower():
            record('source_row', 'replaced', row[:240].replace('\n', ' '))
            return SOURCE_ROW_HTML
        return row
    html, n = re.subn(r'<tr\b[^>]*>.*?</tr>', repl_row, html, flags=re.I | re.S)
    if n == 0:
        record('source_row', 'none', 'No table rows inspected/replaced.')
    replacements = [
        (r'<p\b[^>]*>\s*Interaktive\s+Karte:\s*Felt;\s*Basiskarte/Daten:\s*OpenStreetMap\.\s*</p>\s*', '', 'Removed standalone Felt/OpenStreetMap source paragraph.'),
        (r'<p\b[^>]*>\s*Externer\s+Kartendienst:\s*Felt/OpenStreetMap\.\s*Details\s+stehen\s+im\s+Quellen-\s+und\s+Methodenbereich\.\s*</p>\s*', '', 'Removed standalone external provider paragraph.'),
        (r'Interaktive\s+Karte:\s*Felt;\s*Basiskarte/Daten:\s*OpenStreetMap\.', 'Lokale Kartengrafik: eigene GIS-Aufbereitung; keine externe Kartenansicht beim Seitenaufruf.', 'Replaced inline Felt/OpenStreetMap source sentence.'),
        (r'Externer\s+Kartendienst:\s*Felt/OpenStreetMap\.\s*Details\s+stehen\s+im\s+Quellen-\s+und\s+Methodenbereich\.', '', 'Removed inline external provider sentence.'),
        (r'Interaktive\s+Oberschwaben-Karte', 'Lokale Oberschwaben-Kartengrafiken', 'Replaced source label.'),
        (r'Felt-Embed\s+mit\s+Basiskarte\s+und\s+Hintergrunddaten\s+von\s+OpenStreetMap\.', 'Lokale Kartengrafiken ohne externe Karten- oder Tile-Einbindung beim Seitenaufruf.', 'Replaced source-register Felt-Embed phrase.'),
    ]
    for pat, repl, detail in replacements:
        html, n = re.subn(pat, repl, html, flags=re.I | re.S)
        if n:
            record('text_cleanup', 'replaced', f'{detail} ({n}x)')
    return html

def remove_remaining_provider_sentences(html: str) -> str:
    for pattern in [r'<p\b[^>]*>[^<]*(?:Felt|OpenStreetMap)[^<]*</p>\s*', r'<li\b[^>]*>[^<]*(?:Felt|OpenStreetMap)[^<]*</li>\s*']:
        def repl(m: re.Match) -> str:
            record('remaining_provider_sentence', 'removed', m.group(0)[:200].replace('\n', ' '))
            return ''
        html = re.sub(pattern, repl, html, flags=re.I | re.S)
    return html

def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f'''
{CSS_START}
/* B176: local replacement for the former external Felt map section. */
.b176-local-cartographic-depth {{
  width: min(100% - 2rem, 76rem);
  margin: clamp(2rem, 5vw, 4rem) auto;
  padding: clamp(1.4rem, 3vw, 2.2rem);
  border: 1px solid rgba(28, 42, 34, 0.12);
  border-radius: 1.25rem;
  background: rgba(250, 248, 241, 0.72);
  box-shadow: 0 16px 45px rgba(28, 42, 34, 0.06);
}}
.b176-local-cartographic-depth__inner {{ max-width: 46rem; }}
.b176-local-cartographic-depth__kicker {{
  margin: 0 0 0.55rem;
  color: #6b7f51;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.b176-local-cartographic-depth h2 {{
  margin: 0;
  max-width: 12em;
  color: #1c2a22;
  font-size: clamp(1.75rem, 4vw, 3rem);
  line-height: 0.98;
  text-wrap: balance;
}}
.b176-local-cartographic-depth__lead {{
  margin: 1rem 0 0;
  color: #334238;
  font-size: clamp(1rem, 1.35vw, 1.15rem);
  line-height: 1.5;
  text-wrap: pretty;
}}
.b176-local-cartographic-depth__source {{
  margin: 1rem 0 0;
  color: #6b766d;
  font-size: 0.86rem;
  line-height: 1.45;
}}
.b176-local-cartographic-depth__next {{
  margin: 1.25rem 0 0;
  color: #1c2a22;
  font-weight: 750;
  line-height: 1.45;
}}
@media (max-width: 760px) {{
  .b176-local-cartographic-depth {{
    width: min(100% - 1rem, 76rem);
    border-radius: 0.95rem;
    padding: 1.1rem;
  }}
}}
{CSS_END}
'''
    return css.rstrip() + '\n\n' + block.lstrip()

def update_done(done_text: str, today: str) -> str:
    line = f'- B176 remove Felt from public page: removed the external Felt/OpenStreetMap iframe/link path and replaced it with a local cartographic-depth note while keeping the regional static map untouched ({today}).'
    if 'B176 remove Felt from public page' in done_text:
        return done_text
    return done_text.rstrip() + '\n' + line + '\n'

def main() -> None:
    today = date.today().isoformat()
    if not INDEX.exists():
        raise SystemExit('index.html not found')
    if not CSS.exists():
        raise SystemExit('src/styles.css not found')

    html_before = read(INDEX)
    css_before = read(CSS)
    before = {
        'felt': html_before.lower().count('felt'),
        'openstreetmap': html_before.lower().count('openstreetmap'),
        'iframe': html_before.lower().count('<iframe'),
        'felt_url': html_before.lower().count('felt.com'),
    }

    html = replace_felt_section(html_before)
    html = remove_iframes(html)
    html = remove_felt_links(html)
    html = patch_source_register(html)
    html = remove_remaining_provider_sentences(html)
    css = patch_css(css_before)
    write(INDEX, html)
    write(CSS, css)

    html_after = read(INDEX)
    css_after = read(CSS)
    after = {
        'felt': html_after.lower().count('felt'),
        'openstreetmap': html_after.lower().count('openstreetmap'),
        'iframe': html_after.lower().count('<iframe'),
        'felt_url': html_after.lower().count('felt.com'),
    }

    with CSV_OUT.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['kind', 'status', 'detail'], delimiter=';')
        writer.writeheader()
        writer.writerows(ROWS)

    doc = f'''# B176 - Remove Felt From Public Page

Date: {today}

## Ziel

B176 entfernt die externe Felt/OpenStreetMap-Einbindung aus der öffentlichen Seite.

Die regionale statische Oberschwaben-Karte bleibt unverändert. Entfernt wird nur der externe Kartenviewer-Pfad.

## Entscheidung

```text
Felt raus.
Regionale statische Karte bleibt.
Interaktivität wird nicht grundsätzlich verworfen, sondern nur die Drittanbieter-Abhängigkeit aus der öffentlichen V2 entfernt.
```

## Öffentlicher Ersatztext

```text
Kartografische Vertiefung

Die Detailkarte bleibt bewusst eine lokale, redaktionelle Grafik: Sie zeigt
die Schnittmenge aus heutiger Nutzung und Moor-/Feuchtbodenkontext, ohne beim
Seitenaufruf einen externen Kartendienst zu laden.
```

## Änderungen

- Felt-iframe entfernt
- Felt-Link entfernt, falls vorhanden
- Abschnitt `Interaktive Vertiefung` durch lokale `Kartografische Vertiefung` ersetzt
- Quellen-/Methodenverweis zu Felt/OpenStreetMap durch lokale Kartengrafik ersetzt
- CSS für den lokalen Ersatzabschnitt ergänzt

## Nicht geändert

- regionale statische Oberschwaben-Karte
- B169 Sticky-Zoom
- Flächenbilanz
- Wertschöpfungs-Scorecard
- Datenquellen
- raw GIS/Data

## Provider-Check

| Signal in `index.html` | Vorher | Nachher |
|---|---:|---:|
| `felt` | {before['felt']} | {after['felt']} |
| `openstreetmap` | {before['openstreetmap']} | {after['openstreetmap']} |
| `<iframe` | {before['iframe']} | {after['iframe']} |
| `felt.com` | {before['felt_url']} | {after['felt_url']} |

## Akzeptanz

- kein Felt-iframe mehr in `index.html`
- kein Felt-Link mehr in `index.html`
- keine OpenStreetMap-/Felt-Erwähnung als aktiver öffentlicher Dienst
- regionale statische Karte bleibt bestehen
- B103b PASS
- B58 PASS
'''
    write(DOC, doc)

    audit = '# B176 remove Felt from public page audit\n\n'
    audit += f'Date: {today}\n\n'
    audit += 'Provider counts:\n'
    for key in before:
        audit += f'- {key}: {before[key]} -> {after[key]}\n'
    audit += '\nPost-patch checks:\n'
    audit += f'- B176 local replacement present: {B176_START in html_after and B176_END in html_after}\n'
    audit += f'- B176 CSS present: {CSS_START in css_after and CSS_END in css_after}\n'
    audit += f'- no Felt text remains in index: {"felt" not in html_after.lower()}\n'
    audit += f'- no OpenStreetMap text remains in index: {"openstreetmap" not in html_after.lower()}\n'
    audit += f'- no iframe remains in index: {"<iframe" not in html_after.lower()}\n'
    audit += f'- regional static map phrase still present: {"Die regionale Karte zerlegt den Zusammenhang" in html_after}\n'
    audit += f'- B169 live sticky zoom still present: {"B169_LIVE_STICKY_ZOOM_START" in html_after}\n'
    audit += f'- Oberschwaben no-label map still present: {"oberschwaben_landkreise_moor_nolabel.png" in html_after}\n'
    audit += '\nResult: PATCH WRITTEN. Run B103b, B58 and then B177 external-request audit.\n'
    write(AUDIT, audit)

    done_text = read(DONE) if DONE.exists() else '# Done\n'
    write(DONE, update_done(done_text, today))

    print('B176 remove Felt from public page complete.')
    print('Changed: index.html, src/styles.css')
    print('Created/updated:')
    print('  docs/B176_remove_felt_from_public_page.md')
    print('  docs/B176_removed_felt_fragments.csv')
    print('  docs/B176_remove_felt_from_public_page_audit.txt')
    print('  tasks/done.md')
    print('Provider counts:')
    for key in before:
        print(f'  {key}: {before[key]} -> {after[key]}')
    print('Next: run B103b and B58, then inspect B176 audit.')

if __name__ == '__main__':
    main()
