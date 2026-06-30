from pathlib import Path
import re
from datetime import date

ROOT = Path('.')
INDEX = ROOT / 'index.html'
CSS = ROOT / 'src' / 'styles.css'
SCRIPT = ROOT / 'scripts' / '131c_scope_note_contrast.py'
DOC = ROOT / 'docs' / 'B131c_scope_note_contrast.md'
AUDIT = ROOT / 'docs' / 'B131c_scope_note_contrast_audit.txt'
DONE = ROOT / 'tasks' / 'done.md'

CSS_START = '/* B131_SCOPE_BOX_START */'
CSS_END = '/* B131_SCOPE_BOX_END */'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def strip_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end) + r'\s*', re.S)
    return pattern.sub('', text)


def patch_css(css: str) -> str:
    css = strip_block(css, CSS_START, CSS_END)
    block = f'''
{CSS_START}
.b131-scope-section {{
  padding-block: clamp(0.65rem, 2vw, 1.25rem);
}}

.b131-scope-note {{
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 0.85rem;
  align-items: start;
  max-width: 54rem;
  border-left: 3px solid rgba(89, 123, 82, 0.8);
  background: rgba(255, 255, 255, 0.36);
  border-radius: 0.7rem;
  padding: 0.7rem 0.9rem 0.75rem 0.95rem;
  color: #203229;
}}

.b131-scope-note__label {{
  margin: 0.18rem 0 0;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #5f735e;
  white-space: nowrap;
  font-weight: 700;
}}

.b131-scope-note__body h2 {{
  margin: 0 0 0.25rem;
  font-size: clamp(1rem, 1.7vw, 1.22rem);
  line-height: 1.25;
  color: #203229;
}}

.b131-scope-note__body p {{
  margin: 0;
  max-width: 46rem;
  color: #4e6258;
  font-size: 0.96rem;
  line-height: 1.58;
}}

.b131-scope-note__details {{
  margin-top: 0.5rem;
}}

.b131-scope-note__details summary {{
  cursor: pointer;
  color: #2b3f35;
  font-size: 0.92rem;
  font-weight: 700;
}}

.b131-scope-note__details p {{
  margin-top: 0.4rem;
  max-width: 44rem;
  color: #55685d;
}}

@media (max-width: 720px) {{
  .b131-scope-note {{
    grid-template-columns: 1fr;
    gap: 0.3rem;
    padding-left: 0.85rem;
  }}

  .b131-scope-note__label {{
    white-space: normal;
  }}
}}
{CSS_END}
'''
    return css.rstrip() + '\n\n' + block.lstrip()


def update_done(done_text: str) -> str:
    line = f'- B131c scope note contrast: strengthened contrast and subtle separation for the compact scope note ({date.today().isoformat()}).'
    if 'B131c scope note contrast' in done_text:
        return done_text
    return done_text.rstrip() + '\n' + line + '\n'


def main() -> None:
    audit: list[str] = []

    if not CSS.exists():
        raise SystemExit('src/styles.css not found')

    css = read(CSS)
    old_css_present = CSS_START in css and CSS_END in css
    audit.append(f'Existing B131 CSS block present before patch: {old_css_present}')

    css = patch_css(css)
    write(CSS, css)

    today = date.today().isoformat()

    doc_text = f'''# B131c - Scope Note Contrast

Date: {today}

## Ziel

B131c verbessert den Kontrast der kompakten Scope-Notiz aus B131b,
ohne sie wieder zu dominant werden zu lassen.

## Umsetzung

- stärkere Textkontraste für Label, Headline, Fließtext und Summary
- etwas kräftigere linke Akzentlinie
- sehr subtile helle Hinterlegung zur besseren Ablesbarkeit
- keine Änderung an HTML-Struktur oder Position

## Geänderte Dateien

- `src/styles.css`
- `scripts/131c_scope_note_contrast.py`
- `docs/B131c_scope_note_contrast.md`
- `docs/B131c_scope_note_contrast_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\\103b_corrected_visible_text_audit.py
python scripts\\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- Scope-Notiz bleibt kompakt.
- Kontrast ist deutlich besser lesbar.
- Note wirkt weiterhin nicht wie ein dominanter Warnblock.
'''
    write(DOC, doc_text)

    audit_text = '# B131c scope note contrast audit\n\n'
    audit_text += f'Date: {today}\n\n'
    audit_text += '\n'.join(audit) + '\n\n'
    audit_text += 'Result: PATCH WRITTEN. Run B103b and B58 before commit.\n'
    write(AUDIT, audit_text)

    if DONE.exists():
        done_text = read(DONE)
    else:
        done_text = '# Done\n'
    write(DONE, update_done(done_text))

    print('B131c scope note contrast patch complete.')
    print('Changed: src/styles.css')
    print('Created/updated:')
    print('  docs/B131c_scope_note_contrast.md')
    print('  docs/B131c_scope_note_contrast_audit.txt')
    print('  tasks/done.md')
    print('Next: run B103b and B58 QA.')


if __name__ == '__main__':
    main()
