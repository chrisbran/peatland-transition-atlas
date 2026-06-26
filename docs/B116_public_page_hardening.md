# B116 - Public Page Hardening

Date: 2026-06-26

Status: **REVIEW REQUIRED**

## Summary

- index.html changed: YES
- targeted replacements applied: 8
- risk/prototype visible patterns remaining: 1
- required public patterns missing: 2
- English/prototype watch count: 0

## Applied replacements

| Before | After |
|---|---|
| `Planbar wird Moorschutz erst, wenn Bodenkulissen, Nutzung, betriebliche Betroffenheit und mögliche Wertschöpfungsketten zusammen betrachtet werden.` | `Planbar wird Moorschutz erst, wenn Bodenkulissen, Nutzungskontexte, Wasserstand, betriebliche Fragen und mögliche Wertschöpfungsketten zusammen betrachtet werden.` |
| `Dichtekarten zeigen, wo Belastung räumlich besonders konzentriert ist.` | `Hotspotkarten zeigen, wo Belastung räumlich besonders deutlich wird.` |
| `Layerfolge: Global Peatland Map 2.0 als Kontext und Länder-Hotspot-Layer. Alle Bilder wurden aus demselben ArcGIS-Kartenrahmen exportiert.` | `Datenbasis: Global Peatland Map 2.0 und FAOSTAT-Emissionsdaten zu drainierten organischen Böden; eigene kartografische Aufbereitung.` |
| `In Baden-Württemberg wird Moorschutz zur konkreten Frage: Welche Betriebe sind betroffen, welche Nutzungen bleiben möglich, welche Produkte tragen und welche Förderinstrumente sind nötig?` | `In Baden-Württemberg wird Moorschutz zur konkreten Planungsfrage: Welche Nutzungskontexte sind berührt, welche betrieblichen Fragen entstehen, welche Produkte können tragfähig werden und welche Förderinstrumente wären nötig?` |
| `SOLAMO-BW untersucht regionale Betriebsmuster und die praktische Tragfähigkeit von Nutzungskonzepten auf wiedervernässten Moorflächen.` | `SOLAMO-BW untersucht regionale Betriebsperspektiven und die praktische Tragfähigkeit von Nutzungskonzepten auf wiedervernässten landwirtschaftlichen Moorflächen.` |
| `nässeverträgliche Kulturen, robuste Weidesysteme und stoffliche oder energetische Nutzung benötigen tragfähige Märkte.` | `Nässeverträgliche Kulturen, robuste Weidesysteme sowie stoffliche oder energetische Nutzung benötigen tragfähige Märkte.` |
| `Welche Nutzung nasse Flächen tragen könnten` | `Welche Nutzungen bei hohen Wasserständen tragfähig werden können` |
| `potenziell planbare Cashflows, aber hohe Qualitätsanforderungen` | `mögliche Erlöse, aber hohe Prüf- und Qualitätsanforderungen` |

## Risk findings

| Pattern | Count |
|---|---:|
| `betriebliche Betroffenheit` | 4 |

## Missing required findings

| Pattern | Count |
|---|---:|
| `Die Karte berechnet jedoch keine Treibhausgasminderung` | 0 |
| `~2 % Stilllegung / unklare FIONA-Zuweisung` | 0 |

## Review commands

```powershell
Get-Content docs\B116_public_page_hardening_audit.txt
Import-Csv docs\B116_public_text_findings.csv -Delimiter ';' | Where-Object {$_.status -in @('REVIEW','MISSING')} | Format-Table -Auto
python scripts\103b_corrected_visible_text_audit.py
python scripts\58_visual_qa_and_commit_check.py
```
