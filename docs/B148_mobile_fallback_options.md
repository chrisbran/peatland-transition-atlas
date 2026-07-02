# B148 - Mobile Fallback Options for Felt Map

Date: 2026-07-01

## Problem

Der Felt-Embed funktioniert mobil technisch, aber die Felt-eigene UI nimmt auf 390 px viel Raum ein.
Legende, Popup und Kontextmenue koennen die Karte ueberlagern.

## Ziel

Mobile soll die Story nicht bremsen.
Die interaktive Karte darf optional sein, aber die Kernaussage muss ohne Interaktion sichtbar bleiben.

## Variante A - Statisches Preview plus Button

Empfohlen.

Inhalt:

```text
Schnittmenge aus landwirtschaftlicher Nutzung und Moor-/Feuchtbodenkontext.
Die interaktive Karte öffnet in einem neuen Tab.
```

Button:

```text
Interaktive Karte öffnen
```

Vorteile:

- ruhig
- schnell
- barriereärmer
- keine iframe-UI-Probleme
- kontrollierbarer Scrollfluss

Nachteile:

- kein direktes Mobile-Embed

## Variante B - bestehende PNG-Karte mobil behalten

Inhalt:

- bisherige statische Karte bleibt auf Mobile
- Felt wird nur Desktop/Tablet gezeigt
- externer Felt-Link optional darunter

Vorteile:

- kein neuer Screenshot noetig
- sehr reversibel
- geringstes Risiko

Nachteile:

- Mobile bekommt nicht den vollen Qualitaetssprung

## Variante C - iframe mobil einklappbar

Inhalt:

- Button "Interaktive Karte anzeigen"
- iframe erst nach Klick

Vorteile:

- Mobile kann interaktiv bleiben
- initialer Scrollfluss ruhiger

Nachteile:

- mehr JS/State
- externe UI bleibt klein
- hoeherer Testaufwand

## Empfehlung fuer B149

Mit Variante B oder A starten:

```text
Desktop/Tablet: Felt iframe
Mobile: statischer Fallback + externer Felt-Link
```

Falls spaeter ein hochwertiger statischer Kartenexport aus Felt moeglich ist, wird Variante A bevorzugt.
Bis dahin ist Variante B der pragmatischste Weg.
