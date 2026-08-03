---
title: Phase 1 – Geräteprüfung – verwaltetes iPad – 2026-08-03
device-verified: not-run
run-status: prepared
---

# Geräteprüfung – verwaltetes iPad

Dieses Protokoll wird ausschließlich mit real beobachteten Gerätebefunden ergänzt. Automatisierte Browser- und CI-Tests sowie die technische Erreichbarkeit der Prüffassung ändern `device-verified: not-run` nicht. Es werden nur synthetische Testdaten verwendet.

## Technische Vorbereitung

| Feld | Eintrag |
| --- | --- |
| Kandidat | Commit `8f9e7f562c37f32d452244cb10db6da8d6097b49` |
| Prüffassung | `https://h4r7w16.github.io/ium-lernwerk/` |
| Bereitstellung | GitHub-Pages-Workflow `30790834978`, erfolgreich |
| HTTPS | erzwungen |
| Inhalt | synthetische technische Referenz; keine Curriculumwirkung |

Diese Angaben belegen nur die technische Vorbereitung des Prüflaufs, nicht das Verhalten auf dem iPad.

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
| Getesteter Basispfad | — |
| Evidenzpfad | — |

## Checkliste

Alle Felder bleiben absichtlich offen, bis die jeweilige Prüfung auf dem realen verwalteten iPad stattgefunden hat.

### Safari und VoiceOver

- [ ] Safari: Portal, Modul, Import/Export und lokaler Zustand funktionieren.
- [ ] VoiceOver: Überschriften, Landmarken, Statusmeldungen, Formularfelder und Fokusreihenfolge sind verständlich.
- [ ] Touch: Alle sichtbaren Aktionen sind erreichbar und ohne Farbcodierung verständlich.

### Netz, Offline und Installation

- [ ] Online: Erstaufruf lädt ohne externe Laufzeitressourcen oder unerwartete Drittanfragen.
- [ ] Offline nach Online-Erstaufruf: Portal, Modul und Offline-Rückfall laden erneut.
- [ ] Erster Offline-Aufruf ohne Cache: Browserverhalten ist dokumentiert und wird nicht als App-Leistung bewertet.
- [ ] Web-Clip beziehungsweise PWA-Installation: Startpfad und Scope stimmen.
- [ ] Aktualisierung: Hinweis erscheint; Zustand wird vor der bestätigten Aktualisierung gesichert.
- [ ] Fehlerhafte Aktualisierung: Die bisherige funktionsfähige Version bleibt nutzbar.

### Lokale Daten

- [ ] Bestätigte Speicherung bleibt nach Neuladen erhalten.
- [ ] Flüchtige Sitzung hinterlässt nach einer frischen Sitzung keinen Modulstand.
- [ ] Import: Gültige Datei wird übernommen; ungültige Datei wird verständlich und ohne Zustandsverlust abgelehnt.
- [ ] Export: Sensibilitätshinweis, Dateidownload und Inhalt wurden geprüft.
- [ ] Einzelnes Löschen und global löschen verlangen Bestätigung und entfernen den erwarteten Zustand.
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

`device-verified` darf erst auf `passed` gesetzt werden, wenn auch die weiteren verpflichtenden Zielkonfigurationen (verwaltetes Chromium, verwaltetes Firefox und LMS-Pfad) geprüft und das Gesamtgate geschlossen wurden.
