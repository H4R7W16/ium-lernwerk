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
| Kontrollierter Updatekandidat | `device-update-2026-08-03-1`, Workflow `30796505219`, erfolgreich |
| Kontrollierter Fehlerkandidat | `device-broken-2026-08-03-1`, Workflow `30798577054`, bewusst unvollständig bereitgestellt |
| Wiederherstellung | `device-update-2026-08-03-1`, Workflow `30799268044`, erfolgreich |
| Exporthinweis-Kandidat | `device-export-notice-2026-08-03-1`, Commit `038e16f6cbe804615fbd28e641c2bde42a27d9ff` |
| Exporthinweis-Bereitstellung | GitHub-Pages-Workflow `30806326885`, erfolgreich |
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

### Runde 4 – Kontrollierte Aktualisierung

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen vierten Prüfrunde ohne gemeldete Abweichung:

- der veröffentlichte Kandidat `device-update-2026-08-03-1` wurde als verfügbare Aktualisierung angezeigt;
- vor der Aktivierung wurde der synthetische Zustand `Vor Update bestätigt` plus `Beta` lokal gespeichert;
- die bewusst gewählte Aktion „Speichern und aktualisieren“ aktivierte den Kandidaten und lud die Seite neu;
- Text und Auswahl blieben nach der Aktualisierung erhalten;
- die aktualisierte Fassung blieb anschließend offline nutzbar.

Dieser Teilbefund belegt die reale Updateaufforderung, explizite Nutzerentscheidung, Flush-vor-Aktivierung und Zustandserhaltung auf dem iPad. Evidenzpfad: dieser Abschnitt sowie GitHub-Pages-Lauf `30796505219`.

### Runde 5 – Fehlerhafte Aktualisierung bleibt fail-closed

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen fünften Prüfrunde ohne gemeldete Abweichung:

- der synthetische Zustand `Vor Fehlerkandidat` plus `Beta` wurde in der weiterhin funktionsfähigen Fassung lokal gespeichert;
- nach vollständigem Schließen, erneutem Öffnen und der vorgesehenen Wartezeit erschien kein Aktualisierungshinweis für den bewusst unvollständigen Kandidaten;
- nach Wechsel in den Offlinezustand blieben App, Navigation und der zuvor gespeicherte synthetische Zustand beim Neuladen nutzbar;
- die Verbindung wurde anschließend wiederhergestellt.

Der gekoppelte Befund aus dem öffentlich nachgewiesenen Fehlerkandidaten – HTML und finalisierter Service Worker HTTP 200, referenziertes Offline-Artefakt HTTP 404 – und der realen iPad-Beobachtung belegt das vorgesehene Fail-closed-Verhalten: Der fehlerhafte Kandidat verdrängte die bisherige funktionsfähige Version nicht. Die gültige Serverfassung wurde danach über GitHub-Pages-Lauf `30799268044` wiederhergestellt und mit HTTP 200 für HTML, Service Worker und Offline-Artefakt verifiziert.

### Runde 6 – VoiceOver und Touch

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen sechsten Prüfrunde ohne gemeldete Abweichung:

- VoiceOver gab Marke, Hauptnavigation, Links, Überschriften, Statusbereiche, Formularfelder und Aktionen verständlich wieder;
- die lineare Reihenfolge und die Navigation über Überschriften beziehungsweise Orientierungspunkte waren schlüssig und ohne Fokusfalle nutzbar;
- die Eingabe `VoiceOver Test` und die Auswahl `Alpha` waren bedienbar; der Status `Lokal gespeichert` wurde hörbar angekündigt;
- der Löschdialog wurde mit Titel und Aktionen verständlich wiedergegeben; nach `Abbrechen` kehrte der Fokus zur auslösenden Schaltfläche zurück;
- Navigation, Eingabefelder und Aktionen waren anschließend ohne VoiceOver per Touch sicher erreichbar, ohne unbeabsichtigte Nachbaraktion;
- Speicher- und Verbindungszustände waren als Text und nicht ausschließlich durch Farbe verständlich.

Dieser Teilbefund belegt die reale VoiceOver-, Fokus- und Touchbedienung der synthetischen Prüffassung auf dem verwalteten iPad. Der Fehlerfokus bei einem abgelehnten Import wird getrennt geprüft; deshalb bleibt das zusammenfassende VoiceOver-Kriterium bis dahin offen. Automatisierte Accessibility-Tests ergänzen diesen Befund, ersetzen ihn aber nicht.

### Runde 7 – Importablehnung, Importbestätigung und Exportdatei

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen siebten Prüfrunde ohne gemeldete Abweichung:

- aus dem synthetischen Zustand `Exportprüfung` plus `Beta` wurde eine lokale JSON-Datei heruntergeladen;
- Dateiname und Inhalt waren prüfbar; die Datei enthielt die erwartete Modulkennung `TEST-PLATFORM-REFERENCE` sowie `Exportprüfung` und `beta` im Payload;
- nach Speicherung von `Vor Importfehler` plus `Alpha` wurde die öffentlich geprüfte, synthetische und absichtlich ungeeignete Repositorydatei `package.json` mit VoiceOver als Import ausgewählt;
- der Fokus wechselte zur Fehlermeldung; Titel, Meldung und nächste Handlung wurden verständlich angesagt;
- der abgelehnte Import veränderte den aktiven Zustand nicht, auch nicht nach Neuladen;
- beim anschließenden Import der gültigen Exportdatei waren Vorschau und Aktionen mit VoiceOver verständlich; die bestätigte Übernahme stellte `Exportprüfung` plus `Beta` wieder her und meldete `Import lokal gespeichert`.

Damit sind gültiger und ungültiger Import einschließlich Fehlerfokus, Zustandsintegrität, Bestätigungsdialog und der technische Exportinhalt real belegt. Der im Plattformvertrag geforderte Sensibilitätshinweis fehlt jedoch in der aktuellen Oberfläche; dieser getrennte Produktbefund verhindert weiterhin den Abschluss des Exportkriteriums.

### Runde 8 – Sensibilitätshinweis beim Export

Am 3. August 2026 bestätigte der Auftraggeber nach Ausführung der vollständig beschriebenen achten Prüfrunde mit dem veröffentlichten Kandidaten `device-export-notice-2026-08-03-1` ohne gemeldete Abweichung:

- der Sensibilitätshinweis war im Exportbereich sichtbar;
- beim Fokussieren der Schaltfläche `Exportieren` mit VoiceOver wurde der über `aria-describedby` verbundene Hinweis verständlich mit angesagt;
- die Schaltfläche startete weiterhin unmittelbar den Dateidownload, ohne einen zusätzlichen Dialog einzuführen.

Damit ist die in Runde 7 festgestellte Produktlücke auf dem realen verwalteten iPad nachgeprüft und geschlossen. Diese Nutzerbestätigung belegt ausschließlich den beschriebenen iPad-Befund; die noch fehlenden Konfigurationsangaben und weiteren Zielkonfigurationen bleiben offen.

## Checkliste

Alle Felder bleiben absichtlich offen, bis die jeweilige Prüfung auf dem realen verwalteten iPad stattgefunden hat.

### Safari und VoiceOver

- [x] Safari: Portal, Modul, Import/Export und lokaler Zustand funktionieren.
- [x] VoiceOver: Überschriften, Landmarken, Statusmeldungen, Formularfelder, Fehlerfokus und Fokusreihenfolge sind verständlich.
- [x] Touch: Alle sichtbaren Aktionen sind erreichbar und ohne Farbcodierung verständlich.

### Netz, Offline und Installation

- [ ] Online: Erstaufruf lädt ohne externe Laufzeitressourcen oder unerwartete Drittanfragen.
- [x] Offline nach Online-Erstaufruf: Portal, Modul und Offline-Rückfall laden erneut.
- [x] Erster Offline-Aufruf ohne Cache: Browserverhalten ist dokumentiert und wird nicht als App-Leistung bewertet.
- [x] Web-Clip beziehungsweise PWA-Installation: Startpfad und Scope stimmen.
- [x] Aktualisierung: Hinweis erscheint; Zustand wird vor der bestätigten Aktualisierung gesichert.
- [x] Fehlerhafte Aktualisierung: Die bisherige funktionsfähige Version bleibt nutzbar.

### Lokale Daten

- [x] Bestätigte Speicherung bleibt nach Neuladen erhalten.
- [x] Flüchtige Sitzung hinterlässt nach einer frischen Sitzung keinen Modulstand.
- [x] Import: Gültige Datei wird übernommen; ungültige Datei wird verständlich und ohne Zustandsverlust abgelehnt.
- [x] Export: Dateidownload und Inhalt geprüft; der Sensibilitätshinweis ist sichtbar und mit dem Exportbutton für VoiceOver verbunden.
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
