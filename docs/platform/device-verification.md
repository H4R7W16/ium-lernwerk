---
title: Phase 1 – Geräte- und Schulnetzprüfung
device-verified: not-run
---

# Geräte- und Schulnetzprüfung

Dieses Protokoll darf erst nach einer realen Prüfung ausgefüllt werden. Automatisierte Browser- und CI-Tests ändern `device-verified: not-run` nicht. Pro Prüfkonfiguration wird eine Kopie angelegt; Befunde müssen über einen nachvollziehbaren Evidenzpfad auf datenschutzkonforme Screenshots, Logs oder Testnotizen verweisen. Keine realen Lernendendaten verwenden.

## Prüfkonfiguration

| Feld | Eintrag |
| --- | --- |
| Datum | — |
| Prüfperson | — |
| Gerät und Modell | — |
| Betriebssystem und Version | — |
| Browser-Version | — |
| MDM-Profil | — |
| Web-Clip-Konfiguration | — |
| Speicherrichtlinie / Löschfrist | — |
| Filterrichtlinie / Proxy | — |
| Netz (Schul-WLAN/Gastnetz) | — |
| Getesteter Basispfad | `/` oder `/ium-lernwerk/` |
| Evidenzpfad | — |

## Checkliste

Alle Felder bleiben absichtlich offen, bis eine reale Prüfung stattgefunden hat.

### Browser und assistive Technik

- [ ] Safari: Portal, Modul, Import/Export und lokaler Zustand funktionieren.
- [ ] Chromium: Portal und Modul funktionieren in der verwalteten Zielkonfiguration.
- [ ] Firefox: Portal und Modul funktionieren in der verwalteten Zielkonfiguration.
- [ ] VoiceOver: Überschriften, Landmarken, Statusmeldungen, Formularfelder und Fokusreihenfolge sind verständlich.
- [ ] Tastatur: Skip-Link, Navigation, Dialoge und Modulbedienung sind vollständig erreichbar.

### Netz, Offline und Installation

- [ ] Online: Erstaufruf lädt ohne externe Laufzeitressourcen oder unerwartete Drittanfragen.
- [ ] Offline nach Online-Erstaufruf: Portal, Modul und Offline-Rückfall laden erneut.
- [ ] Erster Offline-Aufruf ohne Cache: Browserverhalten ist dokumentiert und wird nicht als App-Leistung bewertet.
- [ ] Web-Clip beziehungsweise PWA-Installation: Startpfad und Scope stimmen.
- [ ] Aktualisierung: Hinweis erscheint; Zustand wird vor der bestätigten Aktualisierung gesichert.
- [ ] Fehlerhafte Aktualisierung: Die bisherige funktionsfähige Version bleibt nutzbar.

### Daten und Einbettung

- [ ] Bestätigte Speicherung bleibt nach Neuladen erhalten.
- [ ] Flüchtige Sitzung hinterlässt nach Schließen oder Neuladen keinen Modulstand.
- [ ] Import: Gültige Datei wird übernommen; ungültige Datei wird verständlich und ohne Zustandsverlust abgelehnt.
- [ ] Export: Sensibilitätshinweis, Dateidownload und Inhalt wurden geprüft.
- [ ] Einzelnes Löschen und global löschen verlangen Bestätigung und entfernen den erwarteten Zustand.
- [ ] LMS-/iframe-Einbettung funktioniert oder verweist verständlich auf „in eigenem Tab öffnen“.
- [ ] MDM-, Web-Clip-, Speicherrichtlinie und Filterrichtlinie verursachen keinen stillen Funktions- oder Datenverlust.

## Ergebnis

| Feld | Eintrag |
| --- | --- |
| Ergebnis (`pass`, `fail`, `blocked`) | — |
| Befund | — |
| Reproduktionsschritte | — |
| Erwartetes Verhalten | — |
| Tatsächliches Verhalten | — |
| Evidenzpfad | — |
| Nacharbeit / verantwortliche Rolle | — |

`device-verified` darf erst auf `passed` gesetzt werden, wenn alle erforderlichen Zielkonfigurationen geprüft, offene Fehler geschlossen oder ausdrücklich als akzeptierte Einschränkung entschieden und die Evidenzpfade kontrolliert wurden.
