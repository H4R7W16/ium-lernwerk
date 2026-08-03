---
title: Phase 1 – Geräteprüfung – verwaltetes iPad – 2026-08-03
device-verified: not-run
run-status: in-progress
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

## Beobachtete Teilbefunde

### Runde 1 – Safari-Erstlauf und persistenter Zustand

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung des geführten Prüfschritts auf dem realen verwalteten iPad ohne gemeldete Abweichung:

- die öffentliche HTTPS-Prüffassung ließ sich in Safari öffnen;
- die technische Systemprobe ließ sich öffnen;
- der synthetische Text `IUM Geräteprobe` und die Auswahl `Beta` wurden lokal gespeichert;
- Text und Auswahl waren nach dem Neuladen weiterhin vorhanden.

Dieser Teilbefund belegt den ausgeführten Safari-/Local-First-Pfad. Modell, iPadOS-Version, Richtlinienangaben, exakte Statustexte und die weiteren Prüfschritte sind noch nicht protokolliert. Evidenzpfad: dieser Abschnitt als datensparsame Testnotiz der Auftraggeberbestätigung.

### Runde 2 – Transfer, Löschung und flüchtiger Zustand

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen zweiten Prüfrunde ohne gemeldete Abweichung:

- der synthetische Arbeitsstand ließ sich in Safari als JSON-Datei exportieren;
- die bestätigte Einzellöschung entfernte Text und Auswahl;
- der anschließende Import derselben Datei stellte `IUM Geräteprobe` und `Beta` vollständig wieder her;
- die bestätigte globale Löschung entfernte den Arbeitsstand;
- im ausdrücklich gewählten flüchtigen Modus verschwanden `Nur Sitzung` und `Alpha` nach dem Neuladen.

Nicht ausdrücklich berichtet wurden der genaue Exporthinweis, die Dateiinhaltsprüfung und ein absichtlich ungültiger Import. Diese Punkte bleiben offen. Evidenzpfad: dieser Abschnitt als datensparsame Testnotiz der Auftraggeberbestätigung.

### Runde 3 – Offlinebetrieb und Home-Bildschirm

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen dritten Prüfrunde ohne gemeldete Abweichung:

- Safari bestätigte nach der Online-Installation die Offlinebereitschaft;
- die Systemprobe blieb ohne Netzverbindung aufrufbar und der synthetische Zustand `Offline erhalten` plus `Beta` blieb nach dem Neuladen erhalten;
- Lernmodulübersicht und lokale Datenverwaltung ließen sich offline öffnen;
- der zuvor nicht aufgerufene Pfad `/nicht-im-cache/` zeigte den vorgesehenen Offline-Rückfall;
- nach Wiederherstellung der Verbindung blieb der synthetische Zustand erhalten;
- die Installation zum Home-Bildschirm und der anschließende Start am korrekten IuM-Basispfad funktionierten.

Dieser Teilbefund belegt den realen Safari-/Service-Worker-/Web-Clip-Pfad auf dem verwalteten iPad. Exakte Geräte- und Richtlinienangaben bleiben noch zu ergänzen. Evidenzpfad: dieser Abschnitt als datensparsame Testnotiz der Auftraggeberbestätigung.

## Checkliste

Alle Felder bleiben absichtlich offen, bis die jeweilige Prüfung auf dem realen verwalteten iPad stattgefunden hat.

### Safari und VoiceOver

- [x] Safari: Portal, Modul, Import/Export und lokaler Zustand funktionieren.
- [ ] VoiceOver: Überschriften, Landmarken, Statusmeldungen, Formularfelder und Fokusreihenfolge sind verständlich.
- [ ] Touch: Alle sichtbaren Aktionen sind erreichbar und ohne Farbcodierung verständlich.

### Netz, Offline und Installation

- [ ] Online: Erstaufruf lädt ohne externe Laufzeitressourcen oder unerwartete Drittanfragen.
- [x] Offline nach Online-Erstaufruf: Portal, Modul und Offline-Rückfall laden erneut.
- [x] Erster Offline-Aufruf ohne Cache: Browserverhalten ist dokumentiert und wird nicht als App-Leistung bewertet.
- [x] Web-Clip beziehungsweise PWA-Installation: Startpfad und Scope stimmen.
- [ ] Aktualisierung: Hinweis erscheint; Zustand wird vor der bestätigten Aktualisierung gesichert.
- [ ] Fehlerhafte Aktualisierung: Die bisherige funktionsfähige Version bleibt nutzbar.

### Lokale Daten

- [x] Bestätigte Speicherung bleibt nach Neuladen erhalten.
- [x] Flüchtige Sitzung hinterlässt nach einer frischen Sitzung keinen Modulstand.
- [ ] Import: Gültige Datei wird übernommen; ungültige Datei wird verständlich und ohne Zustandsverlust abgelehnt.
- [ ] Export: Sensibilitätshinweis, Dateidownload und Inhalt wurden geprüft.
- [x] Einzelnes Löschen und global löschen verlangen Bestätigung und entfernen den erwarteten Zustand.
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
