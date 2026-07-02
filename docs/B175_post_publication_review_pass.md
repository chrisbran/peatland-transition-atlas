# B175 - Post-Publication Review Pass

Date: 2026-07-02

## Ziel

V2 ist veröffentlicht und als `v2.0.0` getaggt.
B175 ist der erste Post-Publication-Review-Pass.

Dieser Patch ändert keine öffentliche Seite.
Er erstellt eine strukturierte Prüfbasis für die nächsten kleinen Korrekturen.

## Git-Kontext beim Audit

| Feld | Wert |
|---|---|
| Branch | `main` |
| HEAD | `a89c19f (HEAD -> main, tag: v2.0.0, origin/main, origin/HEAD) Refresh publication QA reports` |
| Tags at HEAD | `v2.0.0` |
| Public URL | `https://chrisbran.github.io/peatland-transition-atlas/` |

## Erzeugte Dateien

- `docs/B175_post_publication_review_pass.md`
- `docs/B175_post_publication_review_pass_audit.txt`
- `docs/B175_section_inventory.csv`
- `docs/B175_review_candidates.csv`
- `docs/B175_publication_review_checklist.md`

## Zusammenfassung

| Kategorie | Anzahl |
|---|---:|
| Sections erkannt | 21 |
| Review-Kandidaten | 5 |
| OK-Signale | 9 |
| FAIL-Signale | 0 |

## Längste Sections

| Rang | Heading | Wörter | ID/Class |
|---:|---|---:|---|
| 1 | Grundlagen | 579 | `quellen-methodik` |
| 2 | Nutzung entscheidet, welche Wertschöpfung plausibel wird | 294 | `value-chain-matrix` |
| 3 | Der Maßstab entscheidet | 249 | `karten` |
| 4 | Bis zur Ernte ist vieles anschlussfähig. Danach wird es eng. | 231 | `wertschoepfung` |
| 5 | Aus der Schnittmenge folgt Verhandlung | 229 | `pathways` |
| 6 | Jetzt kommt die Nutzung dazu | 203 | `oberschwaben-layer-story` |
| 7 | Die Schnittmenge zeigt die Größenordnung | 126 | `oberschwaben-key-figures` |
| 8 | Der Wasserstand macht aus Moorboden Speicher oder Quelle | 120 | `moor-primer` |

## Review-Kandidaten

- **Warn-/Caveat-Dichte** (`term_density`, count=19): High count can be fine, but review for repetition/caveat fatigue.
- **Methode/Quelle-Dichte** (`term_density`, count=22): High count can be fine, but review for repetition/caveat fatigue.
- **Wertschöpfungs-Dichte** (`term_density`, count=56): High count can be fine, but review for repetition/caveat fatigue.
- **Transformations-Dichte** (`term_density`, count=34): High count can be fine, but review for repetition/caveat fatigue.
- **Oberschwaben-Dichte** (`term_density`, count=16): High count can be fine, but review for repetition/caveat fatigue.


## FAIL-Signale

Keine FAIL-Signale.


## Interpretation

B175 ist kein automatisches Urteil über Qualität.
Die Ergebnisse sind eine Arbeitsliste:

- hohe Termdichte kann fachlich sinnvoll sein, aber auf Wiederholung prüfen
- lange Sections können bewusst sein, sollten aber beim Lesefluss auffallen
- Release-Signale müssen vollständig vorhanden sein
- die manuelle Checkliste bleibt entscheidend, vor allem für mobile Darstellung und öffentliche Wirkung

## Empfohlene nächste Reihenfolge

```text
B176 Final Copy Compression
B177 Source/Footer Legal Polish
B178 Performance and Asset Weight Audit
B179 Public README / Project Landing Documentation
```
