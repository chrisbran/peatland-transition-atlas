# B182 - v2.1.0 Release Checklist

Date: 2026-07-02

## Vor Commit

```powershell
python scripts\177_external_request_audit.py
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```

Erwartung:

```text
B177: PASS
B103b: 0 sichtbare Findings
B58: PASS
```

## Manuelle Sichtprüfung

- [ ] Hero und Scope-Box sichtbar
- [ ] B169 Sticky-Zoom läuft durch alle acht States
- [ ] B178 Maßstabswechsel-Hinweis steht nicht störend, aber sichtbar
- [ ] Oberschwaben-Detailkarte bleibt sichtbar
- [ ] B176 lokale Kartografie-Vertiefung ersetzt Felt
- [ ] Flächenbilanz zeigt 19.900-ha-Zahl mit Vorbehalt
- [ ] B179/B179b Flaschenhalsgrafik steht allein, ohne alte Balkenreste
- [ ] B181 Gegenposition erscheint vor Methode/Quellen
- [ ] Footer/Quellenbereich sichtbar
- [ ] Mobile Darstellung einmal prüfen

## Browser-Network-Check

DevTools → Network → Disable cache → Hard reload. Suchen nach:

```text
felt
openstreetmap
tile
mapbox
maptiler
fonts.googleapis
fonts.gstatic
```

Erwartung: keine Treffer, abgesehen von passiven Quellenlinks, die nicht beim Seitenaufruf laden.

## Nach Commit und Push

```powershell
git tag -a v2.1.0 -m "Version 2.1 public demonstrator"
git push origin v2.1.0
```

## Optional nach Deployment

- [ ] öffentliche URL hart neu laden
- [ ] Quelltext im Browser nach `felt` prüfen
- [ ] B177-Audit im Repo nachvollziehbar
