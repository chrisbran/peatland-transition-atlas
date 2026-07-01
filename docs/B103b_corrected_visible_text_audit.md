# B103b - Corrected Visible Text Audit

Date: 2026-07-01

## Result

B103b reran the public text audit with proper inherited hidden/retired-state handling.
No source file was modified.

## Why this was needed

B103 could leak nested text from hidden or retired sections into the visible extract.
B103b separates actual visible text from hidden/retired archive text.

## Created files

- `docs/B103b_corrected_visible_text_audit.md`
- `docs/B103b_visible_text_extract_corrected.txt`
- `docs/B103b_hidden_retired_text_extract.txt`
- `docs/B103b_visible_findings.csv`
- `docs/B103b_hidden_findings.csv`
- `docs/B103b_wording_frequency.csv`

## Corrected visible frequency check

| Pattern group | Count |
|---|---:|
| Umsetzung* | 6 |
| Transform* | 9 |
| Wertschöpfung* | 19 |
| wird zu/zur/zum/eine | 0 |
| übersetz* | 0 |
| Suchkulisse/Gesprächskulisse | 0 |
| prototype/explorer | 0 |
| English cue words | 2 |

## Visible findings summary

| Category | Severity | Count |
|---|---|---:|
| wording | review | 6 |

## Hidden/retired findings summary

| Category | Severity | Count |
|---|---|---:|
| prototype/english | review | 1 |

## Interpretation

- Act only on `B103b_visible_findings.csv` for public wording.
- Use `B103b_hidden_findings.csv` only to decide whether hidden archive sections should remain in the repository.
- Do not remove central map stacks, Oberschwaben layer-stack assets or raw GIS/data folders in a wording pass.

## First visible review candidates

### 1. wording / review: `Umsetzung`

Context: rbodenschutz beginnt als Klimathema – und wird vor Ort zur Nutzungsfrage Globale Karten erklären, warum Moore relevant sind. Die Umsetzung entscheidet sich aber dort, wo Wasserstand, Nutzung, Eigentum, Betriebe und Wertschöpfungsketten zusammenkommen. 01 Klima macht

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.

### 2. wording / review: `Umsetzung`

Context: nden den Handlungsdruck. 02 Raum macht Planung notwendig Karten zeigen, dass Moorbodenschutz nicht überall gleich aussieht. 03 Umsetzung braucht lokale Ketten Wasser, Bewirtschaftung, Verarbeitung und Abnahme müssen zusammenpassen. Moore sind räumlich konzentriert

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.

### 3. wording / review: `Umsetzung`

Context: etabliert. Verwendung erhöhter Entwicklungsbedarf Kleinere Mengen, fehlende Skalierung oder unsichere Absatzwege begrenzen die Umsetzung. anschlussfähig im Aufbau erhöhter Entwicklungsbedarf Qualitative Einordnung, keine Präzisionszahlen und keine formale Bewertun

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.

### 4. wording / review: `Umsetzung`

Context: nzelnen Fläche entschieden. Der Wasserstand verbindet Parzellen, Betriebe, Gräben, Vorfluter und Nachbarschaften. Deshalb beginnt Umsetzung oft dort, wo Zuständigkeiten nicht deckungsgleich sind. 01 Parzelle zeigt Nutzung, Eigentum und Bewirtschaftung – aber nur eine

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.

### 5. wording / review: `Umsetzung`

Context: Wasserstände gemeinsam steuerbar sind – und wer dafür zusammen planen muss. Konsequenz: Karten können Prüfbedarf sichtbar machen. Umsetzung braucht zusätzlich lokale Wasserkenntnis, Abstimmung zwischen Eigentümern und Betrieben sowie tragfähige Bewirtschaftungs- und Ve

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.

### 6. wording / review: `Umsetzung`

Context: rwertungspfade. Konsequenz Der Hebel verschiebt sich von der Fläche zur Kette Wiedervernässung bleibt der ökologische Kern. Für Umsetzung reicht die Flächenperspektive aber nicht aus: Entscheidend wird, ob Wasser, Nutzung, Verarbeitung und Nachfrage als zusammenhänge

Recommendation: Keep where needed, but reduce repetition and vary with Planung/Praxis/Bewirtschaftung/Förderung.


## First hidden/retired review candidates

### 1. prototype/english / review: `prototype`

Context: ist.toggle('is-active', step.getAttribute('data-state') === state); }); } sections.forEach(function (section) { var steps = Array.prototype.slice.call(section.querySelectorAll('[data-ob-step]')); if (!steps.length) return; setState(section, steps[0].getAttribute('data-

Recommendation: Review if this is truly visible public copy. Remove/translate if visible.


## Next step

If visible prototype/English findings remain, B104 should remove or translate only those specific public sections.
If B103b shows that prototype/explorer text is hidden, B104 should focus on typos and wording polish instead.
