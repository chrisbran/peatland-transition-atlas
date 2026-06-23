#!/usr/bin/env python3
"""
B79 - Apply German presentation version

Purpose:
- Create the first German presentation version of the public page.
- Apply a B-led design direction: editorial nature, fachlich ruhig, kartografisch diszipliniert.
- Convert the visible main flow to German:
  Problem -> Kernargument -> Kartenfolge -> Umsetzung -> Pfade -> Methode.
- Preserve central map functionality and existing assets.
- Hide older lower explorer/prototype sections reversibly instead of deleting them.

Outputs:
- docs/B79_german_presentation_version.md
- modifies index.html
- modifies src/styles.css
- updates tasks/done.md

Does NOT:
- delete sections
- delete scripts
- alter map PNGs
- alter raw data
- change central map state names
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "src" / "styles.css"
TASKS = ROOT / "tasks"
DONE = TASKS / "done.md"
DOCS = ROOT / "docs"
DOC = DOCS / "B79_german_presentation_version.md"

B79_HIDDEN_IDS = [
    "mvpStoryline",
    "layerProvenance",
    "supportingEvidenceIntro",
    "interpretationIntro",
    "supportingEvidenceGroupIntro",
    "prototypeAppendixIntro",
    "pathwayEvidenceMatrix",
    "hotspots",
    "map",
    "pathways",
    "fit",
    "methodology",
    "data",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_element_bounds(text: str, tag: str, start_pattern: str):
    start_re = re.compile(start_pattern, flags=re.IGNORECASE | re.DOTALL)
    m = start_re.search(text)
    if not m:
        return None
    start = m.start()
    open_end = m.end()
    token_re = re.compile(rf"</?{tag}\b[^>]*>", flags=re.IGNORECASE | re.DOTALL)
    depth = 1
    for tm in token_re.finditer(text, open_end):
        token = tm.group(0)
        if token.lower().startswith(f"</{tag.lower()}"):
            depth -= 1
            if depth == 0:
                return start, open_end, tm.start(), tm.end()
        else:
            depth += 1
    return None


def replace_section_inner_by_id(text: str, section_id: str, inner: str) -> str:
    bounds = find_element_bounds(
        text,
        "section",
        rf"<section\b(?=[^>]*\bid=[\"']{re.escape(section_id)}[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    return text[:open_end] + "\n" + inner.strip() + "\n" + text[close_start:]


def replace_first_section_by_class_inner(text: str, class_name: str, inner: str, ensure_id: str | None = None) -> str:
    bounds = find_element_bounds(
        text,
        "section",
        rf"<section\b(?=[^>]*\bclass=[\"'][^\"']*\b{re.escape(class_name)}\b[^\"']*[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    opening = text[start:open_end]
    if ensure_id and not re.search(r"\bid=", opening, flags=re.IGNORECASE):
        opening = opening[:-1] + f' id="{ensure_id}">'
    elif ensure_id:
        opening = re.sub(r'\bid=["\'][^"\']+["\']', f'id="{ensure_id}"', opening, count=1, flags=re.IGNORECASE)
    return text[:start] + opening + "\n" + inner.strip() + "\n" + text[close_start:]


def replace_first_nav(text: str) -> str:
    nav = """<nav aria-label="Seitennavigation">
      <a href="#problem">Problem</a>
      <a href="#centralGlobalMapStory">Kartenfolge</a>
      <a href="#b79RegionalImplementation">Umsetzung</a>
      <a href="#b79Pathways">Pfade</a>
      <a href="#b79MethodBoundary">Methode</a>
    </nav>"""
    return re.sub(r"<nav\b[^>]*>.*?</nav>", nav, text, count=1, flags=re.IGNORECASE | re.DOTALL)


def replace_brand_text(text: str) -> str:
    # Replace first brand link text only; preserve attributes.
    return re.sub(
        r"(<a\b[^>]*\bclass=[\"'][^\"']*\bbrand\b[^\"']*[\"'][^>]*>)(.*?)(</a>)",
        r"\1Moorschutz\3",
        text,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )


def replace_doc_title(text: str) -> str:
    if re.search(r"<title>.*?</title>", text, flags=re.IGNORECASE | re.DOTALL):
        return re.sub(
            r"<title>.*?</title>",
            "<title>Moorschutz braucht räumliche Orientierung</title>",
            text,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    return text


def ensure_html_lang_de(text: str) -> str:
    if re.search(r"<html\b", text, flags=re.IGNORECASE):
        if re.search(r"<html\b[^>]*\blang=", text, flags=re.IGNORECASE):
            return re.sub(r'(<html\b[^>]*\blang=)["\'][^"\']*["\']', r'\1"de"', text, count=1, flags=re.IGNORECASE)
        return re.sub(r"<html\b", '<html lang="de"', text, count=1, flags=re.IGNORECASE)
    return text


def replace_first_tag_inside_section(text: str, section_id: str, tag: str, new_html: str, class_contains: str | None = None) -> str:
    bounds = find_element_bounds(
        text,
        "section",
        rf"<section\b(?=[^>]*\bid=[\"']{re.escape(section_id)}[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    section = text[open_end:close_start]

    if class_contains:
        pat = rf"<{tag}\b(?=[^>]*\bclass=[\"'][^\"']*{re.escape(class_contains)}[^\"']*[\"'])[^>]*>.*?</{tag}>"
    else:
        pat = rf"<{tag}\b[^>]*>.*?</{tag}>"

    new_section, n = re.subn(pat, new_html, section, count=1, flags=re.IGNORECASE | re.DOTALL)
    if n == 0:
        return text
    return text[:open_end] + new_section + text[close_start:]


def replace_article_by_state(text: str, state: str, idx: str, title: str, body: str) -> str:
    bounds = find_element_bounds(
        text,
        "article",
        rf"<article\b(?=[^>]*\bdata-global-state=[\"']{re.escape(state)}[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    inner = f"""
      <span>{idx}</span>
      <h3>{title}</h3>
      <p>{body}</p>
    """
    return text[:open_end] + "\n" + inner.strip() + "\n" + text[close_start:]


def insert_after_section(text: str, section_id: str, insertion: str) -> str:
    if f'id="{section_id}"' not in text and f"id='{section_id}'" not in text:
        return text
    if "id=\"b79RegionalImplementation\"" in text or "id='b79RegionalImplementation'" in text:
        return text
    bounds = find_element_bounds(
        text,
        "section",
        rf"<section\b(?=[^>]*\bid=[\"']{re.escape(section_id)}[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    return text[:close_end] + "\n\n" + insertion.strip() + "\n\n" + text[close_end:]


def retire_section(text: str, section_id: str) -> str:
    bounds = find_element_bounds(
        text,
        "section",
        rf"<section\b(?=[^>]*\bid=[\"']{re.escape(section_id)}[\"'])[^>]*>",
    )
    if not bounds:
        return text
    start, open_end, close_start, close_end = bounds
    opening = text[start:open_end]

    if 'data-retired="B79"' in opening or "data-retired='B79'" in opening:
        return text

    if re.search(r"\bclass=", opening, flags=re.IGNORECASE):
        opening = re.sub(
            r'\bclass=(["\'])(.*?)\1',
            lambda m: f'class={m.group(1)}{m.group(2)} b79-hidden is-retired{m.group(1)}'
            if "b79-hidden" not in m.group(2) else m.group(0),
            opening,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        opening = opening[:-1] + ' class="b79-hidden is-retired">'

    if " hidden" not in opening.lower():
        opening = opening[:-1] + " hidden>"
    if "aria-hidden" not in opening.lower():
        opening = opening[:-1] + ' aria-hidden="true">'
    if "data-retired" not in opening.lower():
        opening = opening[:-1] + ' data-retired="B79">'
    if "data-story-role" not in opening.lower():
        opening = opening[:-1] + ' data-story-role="retired-by-german-presentation-version">'
    if "style=" in opening.lower():
        opening = re.sub(
            r'\bstyle=(["\'])(.*?)\1',
            lambda m: f'style={m.group(1)}{m.group(2).rstrip(";")}; display: none !important;{m.group(1)}',
            opening,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    else:
        opening = opening[:-1] + ' style="display: none !important;">'

    return text[:start] + opening + text[open_end:]


def patch_stage_label_js() -> list[str]:
    changed = []
    path = ROOT / "src" / "central_stage_label_fix.js"
    if not path.exists():
        return changed
    txt = read(path)
    before = txt
    replacements = {
        "GLOBAL PEATLAND EXTENT": "MOORVERBREITUNG",
        "TOTAL PRESSURE": "EMISSIONSDRUCK",
        "TOTAL HOTSPOTS": "EMISSIONSDRUCK",
        "HOTSPOT DENSITY": "DRUCKDICHTE",
        "TOTAL VS DENSITY": "VERGLEICH",
        "EUROPE FRAME": "EUROPA",
        "EUROPE PEATLANDS": "EUROPÄISCHE MOORKULISSE",
        "GERMANY FRAME": "DEUTSCHLAND",
        "THUENEN ORGANIC SOILS": "ORGANISCHE BÖDEN",
        "THUENEN MOOR TYPES": "BODENKONTEXT",
        "BADEN-WUERTTEMBERG FRAME": "BADEN-WÜRTTEMBERG",
        "BK50 PEAT / WETLAND SOILS": "BK50 MOOR- UND FEUCHTBÖDEN",
    }
    for a, b in replacements.items():
        txt = txt.replace(a, b)
    if txt != before:
        write(path, txt)
        changed.append(rel(path))
    return changed


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    TASKS.mkdir(exist_ok=True)
    today = date.today().isoformat()

    html = read(INDEX)
    css = read(CSS)

    html = ensure_html_lang_de(html)
    html = replace_doc_title(html)
    html = replace_brand_text(html)
    html = replace_first_nav(html)

    hero_inner = """
    <p class="kicker">Moore · Klimaschutz · regionale Umsetzung</p>
    <h1>Moorschutz braucht räumliche Orientierung</h1>
    <p class="lead">Wiedervernässung ist nicht nur eine ökologische Maßnahme. Sie verändert Nutzung, Betriebe, Wertschöpfung und Planung.</p>
    <div class="b79-claim-grid" aria-label="Kernaussagen">
      <article>
        <span class="b79-num">01</span>
        <h3>Kleine Fläche, große Wirkung</h3>
        <p>Moore nehmen geringe Flächenanteile ein, können aber für Klimaschutz, Biodiversität und Wasserhaushalt entscheidend sein.</p>
      </article>
      <article>
        <span class="b79-num">02</span>
        <h3>Der Maßstab entscheidet</h3>
        <p>Globale Karten zeigen Relevanz. Umsetzung entsteht erst auf nationaler, regionaler und betrieblicher Ebene.</p>
      </article>
      <article>
        <span class="b79-num">03</span>
        <h3>Transformation braucht Pfade</h3>
        <p>Schutz, Wiedervernässung, angepasste Nutzung und Förderinstrumente müssen zusammen gedacht werden.</p>
      </article>
    </div>
    """
    html = replace_first_section_by_class_inner(html, "hero", hero_inner, ensure_id="problem")

    transition_inner = """
    <p class="section-kicker">Kernargument</p>
    <h2>Aus Moorbodenkontext wird eine Umsetzungsfrage</h2>
    <p class="transition-logic-lede">Moorschutz wird erst dann planbar, wenn räumliche Kulissen, regionale Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten gemeinsam betrachtet werden.</p>
    """
    html = replace_section_inner_by_id(html, "transitionLogic", transition_inner)

    html = replace_first_tag_inside_section(
        html,
        "centralGlobalMapStory",
        "p",
        '<p class="section-kicker">Kartenfolge</p>',
        class_contains="kicker",
    )
    html = replace_first_tag_inside_section(
        html,
        "centralGlobalMapStory",
        "h2",
        "<h2>Von globaler Relevanz zur regionalen Umsetzung</h2>",
    )
    html = replace_first_tag_inside_section(
        html,
        "centralGlobalMapStory",
        "p",
        '<p class="central-story-read-note">Die Kartenfolge verdichtet den Maßstab: von der weltweiten Moorverbreitung über Emissionsdruck und nationale Umsetzungskulissen bis zum Boden- und Feuchtgebietskontext in Baden-Württemberg.</p>',
        class_contains="central-story-read-note",
    )

    step_text = {
        "extent": ("01", "Wo liegen die Moore?", "Die räumliche Kulisse zeigt, wo Moorschutzfragen entstehen."),
        "total": ("02", "Wo konzentriert sich der Emissionsdruck?", "Entwässerung und Nutzung verändern Moore von Speichern zu Quellen."),
        "density": ("03", "Wo ist der Druck besonders hoch?", "Dichtekarten zeigen, wo Belastung räumlich besonders konzentriert ist."),
        "compare": ("04", "Größe und Intensität unterscheiden sich.", "Flächengröße und Emissionsintensität führen nicht immer zur selben räumlichen Aussage."),
        "europe-borders": ("05", "Europa wird zur Umsetzungsebene.", "Politische und administrative Grenzen übersetzen globale Relevanz in Handlungsräume."),
        "europe-peat": ("06", "Moorvorkommen überschreiten Grenzen.", "Moorlandschaften folgen Landschaft und Hydrologie, nicht Verwaltungslinien."),
        "germany-context": ("07", "Deutschland ist eine Umsetzungsebene.", "Nationale Kulissen übersetzen globale Relevanz in Planung und Förderung."),
        "germany-thuenen-extent": ("08", "Die Thünen-Kulisse konkretisiert organische Böden.", "Sie macht sichtbar, wo organische Böden für nationale Umsetzung relevant werden."),
        "germany-thuenen-types": ("09", "Bodenkontext prägt mögliche Nutzungspfade.", "Unterschiedliche Bodenkontexte verlangen unterschiedliche Übergänge."),
        "bw-context": ("10", "Baden-Württemberg wird konkret.", "Auf regionaler Ebene werden Moor- und Feuchtbodenkontexte zur Planungsfrage."),
        "bw-bk50-extent": ("11", "BK50 zeigt Moor- und Feuchtbodenkontext.", "Die Karte ordnet räumlich ein, ersetzt aber keine Eignungs- oder Prioritätsprüfung."),
    }
    for state, (idx, title, body) in step_text.items():
        html = replace_article_by_state(html, state, idx, title, body)

    b79_sections = """
<section id="b79RegionalImplementation" class="b79-section b79-regional-implementation">
  <div class="b79-section-heading">
    <p class="section-kicker">Regionale Umsetzung</p>
    <h2>Oberschwaben zeigt die praktische Herausforderung</h2>
    <p>In Baden-Württemberg wird Moorschutz zur konkreten Frage: Welche Betriebe sind betroffen, welche Nutzungen bleiben möglich, welche Produkte tragen und welche Förderinstrumente sind nötig?</p>
  </div>
  <div class="b79-card-grid">
    <article>
      <h3>Planungskulisse</h3>
      <p>Die Moorschutzkonzeption Baden-Württemberg liefert den strategischen Rahmen für Schutz, Renaturierung, Monitoring und Förderung.</p>
    </article>
    <article>
      <h3>Betriebliche Betroffenheit</h3>
      <p>SOLAMO-BW untersucht regionale Betriebsmuster und die Umsetzbarkeit von Nutzungskonzepten auf wiedervernässten Moorflächen.</p>
    </article>
    <article>
      <h3>Wertschöpfung</h3>
      <p>Nasseverträgliche Kulturen, robuste Weidesysteme und stoffliche oder energetische Nutzung benötigen tragfähige Märkte.</p>
    </article>
  </div>
</section>

<section id="b79Pathways" class="b79-section b79-pathways">
  <div class="b79-section-heading">
    <p class="section-kicker">Transformationspfade</p>
    <h2>Nicht jede Fläche braucht dieselbe Lösung</h2>
    <p>Die zentrale Aufgabe ist nicht die eine Maßnahme, sondern die passende Kombination aus Wasserstand, Nutzung, Betriebsperspektive und öffentlicher Förderung.</p>
  </div>
  <div class="b79-card-grid">
    <article>
      <span class="b79-num">A</span>
      <h3>Schützen und stabilisieren</h3>
      <p>Naturnahe Moore erhalten, hydrologische Störungen begrenzen und Nährstoffeinträge reduzieren.</p>
    </article>
    <article>
      <span class="b79-num">B</span>
      <h3>Wiedervernässen und anpassen</h3>
      <p>Entwässerte Moorböden vernässen und Nutzung schrittweise auf nasse Bedingungen ausrichten.</p>
    </article>
    <article>
      <span class="b79-num">C</span>
      <h3>Nutzung neu organisieren</h3>
      <p>Produkte, Wertschöpfungsketten und Betriebsmodelle entwickeln, die mit höheren Wasserständen vereinbar sind.</p>
    </article>
  </div>
</section>

<section id="b79MethodBoundary" class="b79-section b79-method-boundary">
  <p class="section-kicker">Methodische Grenze</p>
  <h2>Einordnung statt Eignungskarte</h2>
  <p>Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.</p>
  <p class="b79-source-line">Datenbasis: Global Peatland Map 2.0, Thünen-Kulisse organischer Böden, BK50 Baden-Württemberg, LUBW/Moorschutzkonzeption, SOLAMO-BW-Projektinformationen.</p>
</section>
"""
    html = insert_after_section(html, "centralGlobalMapStory", b79_sections)

    for section_id in B79_HIDDEN_IDS:
        html = retire_section(html, section_id)

    b79_css = r"""
/* B79 German presentation version */
:root {
  --b79-paper: #F5EFE6;
  --b79-paper-soft: #FFFCF7;
  --b79-ink: #221D18;
  --b79-lead: #3B3129;
  --b79-muted: #776A5D;
  --b79-line: #DED4C7;
  --b79-accent: #1F4E5F;
  --b79-ocker: #C8901A;
  --b79-salbei: #7A8B74;
  --b79-rost: #A65041;
}

html,
body {
  background:
    radial-gradient(circle at 15% 4%, rgba(200, 144, 26, 0.10), transparent 34rem),
    radial-gradient(circle at 86% 18%, rgba(122, 139, 116, 0.14), transparent 32rem),
    var(--b79-paper) !important;
  color: var(--b79-ink) !important;
}

body {
  font-family: Inter, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}

.site-header,
.header,
.navbar {
  background: color-mix(in srgb, var(--b79-paper) 92%, white) !important;
  border-bottom: 1px solid var(--b79-line) !important;
  color: var(--b79-ink) !important;
  backdrop-filter: blur(14px);
}

.site-header a,
.header a,
.navbar a {
  color: var(--b79-muted) !important;
}

.site-header a:hover,
.header a:hover,
.navbar a:hover {
  color: var(--b79-accent) !important;
}

.brand {
  color: var(--b79-ink) !important;
  font-weight: 750;
}

section.hero,
.hero {
  background: transparent !important;
  color: var(--b79-ink) !important;
  max-width: 1180px;
  margin-inline: auto;
  padding-top: clamp(86px, 12vw, 152px);
  padding-bottom: clamp(72px, 9vw, 128px);
}

.hero .kicker,
.section-kicker,
.kicker {
  color: #8A5E11 !important;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  font-weight: 760;
}

.hero h1,
section.hero h1 {
  color: var(--b79-ink) !important;
  max-width: 920px;
  font-size: clamp(3rem, 7vw, 6.2rem);
  line-height: 0.94;
  letter-spacing: -0.07em;
}

.hero .lead,
.lead {
  color: var(--b79-lead) !important;
  max-width: 760px;
  font-size: clamp(1.25rem, 2vw, 1.65rem);
  line-height: 1.35;
}

.b79-claim-grid,
.b79-card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(18px, 3vw, 32px);
  margin-top: clamp(38px, 6vw, 70px);
}

.b79-claim-grid article,
.b79-card-grid article {
  border: 1px solid var(--b79-line);
  background: color-mix(in srgb, var(--b79-paper-soft) 76%, transparent);
  padding: clamp(20px, 2.8vw, 30px);
}

.b79-claim-grid h3,
.b79-card-grid h3 {
  color: var(--b79-ink) !important;
  font-size: 1.05rem;
  line-height: 1.2;
  margin: 0 0 0.65rem;
}

.b79-claim-grid p,
.b79-card-grid p {
  color: var(--b79-muted) !important;
  margin: 0;
}

.b79-num,
.central-map-step span,
.central-map-step .step-number {
  color: var(--b79-accent) !important;
  font-weight: 800;
  letter-spacing: 0.08em;
  font-size: 0.78rem;
}

#transitionLogic {
  background: transparent !important;
  border-top: 1px solid var(--b79-line);
  border-bottom: 1px solid var(--b79-line);
  color: var(--b79-ink) !important;
}

#transitionLogic h2,
#centralGlobalMapStory h2,
.b79-section h2 {
  color: var(--b79-ink) !important;
  max-width: 820px;
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1.02;
  letter-spacing: -0.045em;
}

#transitionLogic p,
#centralGlobalMapStory p,
.b79-section p {
  color: var(--b79-muted) !important;
}

#centralGlobalMapStory {
  background: transparent !important;
  color: var(--b79-ink) !important;
}

#centralGlobalMapStory .central-story-read-note {
  color: var(--b79-muted) !important;
  max-width: 860px;
}

#centralGlobalMapStory .central-map-step,
#centralGlobalMapStory article[data-global-state] {
  background: color-mix(in srgb, var(--b79-paper-soft) 74%, transparent) !important;
  border: 1px solid var(--b79-line) !important;
  color: var(--b79-ink) !important;
  box-shadow: none !important;
}

#centralGlobalMapStory .central-map-step h3,
#centralGlobalMapStory article[data-global-state] h3 {
  color: var(--b79-ink) !important;
}

#centralGlobalMapStory .central-map-step p,
#centralGlobalMapStory article[data-global-state] p {
  color: var(--b79-muted) !important;
}

#centralGlobalMapStory .central-map-visual,
#centralGlobalMapStory .central-map-stage,
#centralGlobalMapStory .map-frame,
#centralGlobalMapStory figure {
  background: var(--b79-paper-soft) !important;
  border-color: var(--b79-line) !important;
  box-shadow: 0 18px 70px rgba(70, 50, 30, 0.10) !important;
}

#centralGlobalMapStory figcaption,
#centralGlobalMapStory .source,
#centralGlobalMapStory .source-line {
  color: var(--b79-muted) !important;
  font-size: 0.78rem;
}

.b79-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: clamp(76px, 9vw, 128px) clamp(20px, 6vw, 72px);
  background: transparent !important;
  color: var(--b79-ink) !important;
}

.b79-section-heading {
  max-width: 860px;
}

.b79-method-boundary {
  margin-top: clamp(32px, 4vw, 64px);
  margin-bottom: clamp(64px, 8vw, 120px);
  background: color-mix(in srgb, var(--b79-paper-soft) 84%, transparent) !important;
  border: 1px solid var(--b79-line);
}

.b79-source-line {
  font-size: 0.82rem;
  color: var(--b79-muted) !important;
  margin-top: 1.5rem;
}

section[data-retired="B79"],
.b79-hidden {
  display: none !important;
}

@media (max-width: 860px) {
  .b79-claim-grid,
  .b79-card-grid {
    grid-template-columns: 1fr;
  }

  .hero h1,
  section.hero h1 {
    font-size: clamp(2.6rem, 12vw, 4.2rem);
  }
}
/* End B79 German presentation version */
"""

    if "/* B79 German presentation version */" not in css:
        css = css.rstrip() + "\n\n" + b79_css.strip() + "\n"

    write(INDEX, html)
    write(CSS, css)
    changed_js = patch_stage_label_js()

    doc = f"""# B79 - German Presentation Version

Date: {today}

## 1. Purpose

B79 applies the first German presentation version to the production page.

Target direction:

**Editorial Natur + fachliche Ruhe + kartografische Disziplin**

## 2. Main changes

- Rewrote the hero into German subject-matter language.
- Replaced top navigation with German presentation path:
  - Problem
  - Kartenfolge
  - Umsetzung
  - Pfade
  - Methode
- Rewrote `#transitionLogic` as the main argument.
- Rewrote visible central map step texts into German.
- Inserted compact German sections:
  - `#b79RegionalImplementation`
  - `#b79Pathways`
  - `#b79MethodBoundary`
- Hid older lower explorer/prototype sections reversibly with `data-retired="B79"`.
- Added B79 CSS overrides to `src/styles.css`.
- Preserved map PNGs, state names and central layer logic.

## 3. Method boundary

The production page now includes this boundary:

> Die dargestellten Boden- und Moorinformationen sind eine räumliche Einordnung. Sie ersetzen keine Flächeneignungsprüfung, keine Priorisierung und keine betriebliche Betroffenheitsanalyse.

## 4. Files changed

- `index.html`
- `src/styles.css`
- `tasks/done.md`
- `docs/B79_german_presentation_version.md`
{chr(10).join(f"- `{p}`" for p in changed_js) if changed_js else ""}

## 5. Reversibility

No deleted sections, scripts, data or assets. Older lower sections were hidden rather than removed.

## 6. Required QA

Run:

```powershell
python scripts\\58_visual_qa_and_commit_check.py
python scripts\\72_public_mvp_quality_pass.py
```

Manual checks:

1. Page opens locally.
2. Main visible flow is German.
3. Central map sequence still works.
4. BW states still work.
5. Retired B79 sections remain hidden.
6. No visible main-flow `prototype`, `MVP`, `portfolio`, `dashboard`, `appendix`.
7. Method boundary is visible.
"""
    write(DOC, doc)

    done_entry = f"""
## B79 - German presentation version ({today})

- Applied first German presentation version to `index.html`.
- Added B79 editorial-nature design overrides to `src/styles.css`.
- Inserted compact German implementation, pathway and method-boundary sections.
- Hid older lower explorer/prototype sections reversibly with `data-retired="B79"`.
- Created `docs/B79_german_presentation_version.md`.
- Preserved map assets and central map state names.
"""
    current = read(DONE) if DONE.exists() else "# Done\n"
    if "## B79 - German presentation version" not in current:
        write(DONE, current.rstrip() + "\n" + done_entry)

    print("B79 German presentation version applied.")
    print("Changed:")
    print(f"  {rel(INDEX)}")
    print(f"  {rel(CSS)}")
    print(f"  {rel(DOC)}")
    if changed_js:
        for p in changed_js:
            print(f"  {p}")
    print(f"  {rel(DONE)}")
    print("\nNext:")
    print("  python scripts\\58_visual_qa_and_commit_check.py")
    print("  python scripts\\72_public_mvp_quality_pass.py")


if __name__ == "__main__":
    main()
