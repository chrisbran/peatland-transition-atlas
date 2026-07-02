# B140b - Reduce Source-Line Noise

Date: 2026-06-30

## Anlass

B140 setzte das richtige Prinzip um, erzeugte im Seitenfluss aber zu viele sichtbare Quellenzeilen.
Vor allem unter rein redaktionellen Blöcken wirkte das in der Gesamtansicht unruhig.

## Entscheidung

Quellen-/Methodenzeilen sollen dort sichtbar bleiben, wo Daten, Karten oder konkrete
Auswertungslogik gezeigt werden. Rein redaktionelle Brücken und Schlussfolgerungen müssen
nicht jeweils eine eigene Zeile erhalten, solange sie über Methode und zentralen Quellenblock
abgedeckt sind.

## Umsetzung

Entfernt wurden B140-Zeilen unter:

- Frame-Mismatch-Bridge
- Wasser-und-Governance-Block
- Konsequenz-Kicker

Beibehalten wurden B140-Zeilen unter:

- globalem Karten-/Kontextblock
- regionalem Oberschwaben-/Schnittmengenblock

Außerdem wurde die Darstellung der verbleibenden Quellenzeilen abgeschwächt:

- kleiner
- zentriert
- weniger dominant
- explizites Präfix `Quelle/Methode:`

## Geänderte Dateien

- `index.html`
- `src/styles.css`
- `scripts/140b_source_lines_reduce_noise.py`
- `docs/B140b_source_lines_reduce_noise.md`
- `docs/B140b_source_lines_reduce_noise_audit.txt`
- `tasks/done.md`

## QA

Nach dem Patch ausführen:

```powershell
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Visuell prüfen:

- weniger Quellenzeilen im Seitenfluss
- verbleibende Zeilen stehen nur unter daten-/kartenbezogenen Blöcken
- B130b-Quellenbox bleibt erhalten
- `Methode in Kürze`-Links funktionieren
- keine Karten-/JS-/Datenänderung
