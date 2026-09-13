# Prüfung der zusätzlichen Lernfassung

Stand: 13.09.2026. Eigenständige lokale Vorschau, keine Produkt-/Pilotabnahme. Browserprüfung mit synthetischen Eingaben in einem eigenen Tab.

## Automatisiert

`node --test prototypes/m06-reinigungsfall-v2/lesson-model.test.cjs prototypes/m06-reinigungsfall/reinigungsfall.test.cjs`: **19/19 erfolgreich**, davon elf Tests der neuen Lernlogik und acht bestehende Bewegungstests. Syntaxprüfung für `app.js` und `lesson-model.js` erfolgreich.

Die Tests prüfen unter anderem unterschiedliche Auftragskriterien, Körperaktionen bei gleichen Befehlen innerhalb eines Körpers, zwei verschiedene Startlagen, 12/12 mit und ohne Wiederholung, unveränderliche Vorhersagen, selbst aufgebaute Abruffolgen sowie vollständige und fehlerhafte Sicherungen. Eine Sicherung mit widersprüchlicher Codefassung/Prüflauf wird abgewiesen. Zu große Daten werden bereits beim Export zurückgewiesen.

SHA-256 des übernommenen Bewegungskerns und des unveränderten Originals identisch:

```text
AD73431D0DE4C7FD7027B316B6C2B0AE08F2857E4E9969DAEF6FFDEC9D4B0676
```

Lokale HTTP-Abrufe von HTML, CSS, App, Lernlogik, Kern und README jeweils Status 200.

## Im Browser beobachtet

| Ablauf | Beobachtung |
|---|---|
| Einstieg, zwei Einzelschritte | Nach `vor`, `links`: (2,2), Blick oben, 2/4. Rückmeldung unterscheidet Ort und Blick. |
| Vorhersage: (2,1), Blick oben wählen | Fahrt endet dort, 3/4; Rückmeldung erkennt die passende Vorhersage an. Die Erwartung ist nach der ersten Prüfung unveränderlich. |
| Zweimal „Bis Körperende“ | Aktion 4/8, Durchlauf 2/4, (2,1), Blick links; nur der Körperbefehl `links` ist aktiv markiert. |
| Neue Ergänzung | Drehbefehl ausgewählt und ausgeführt; korrekte/falsche Variante zusätzlich im Modelltest mit neuer Startlage geprüft. |
| Klammerfehler | Stopp bei Aktion 3 an (3,3), Blick rechts; Rückmeldung fordert zum Rückblick auf den Zustand auf. |
| Code nach diesem Lauf korrigieren | Grundriss bleibt sichtbar und zeigt den Start; alte Fassung ist getrennt erhalten. Fokus bleibt im Codefeld. |
| Korrigierte Randrunde | 8/9; Rückmeldung „Die geplante Randrunde gelingt“, beide zugehörigen Kriterien erfüllt. |
| Gleicher Code im Flächenauftrag | 8/9; fehlende Abdeckung als offenes Kriterium, kein Randfehler. |
| `vor`, `links`, `vor` ergänzen | 9/9, Ende (2,2), Blick oben; beide Flächenkriterien erfüllt. |
| Eigene Route mit drei Zeilen | 12/12 nach 15 Aktionen, Ende (4,1), Blick rechts; Abdeckung, sichere Fahrt und Wiederholung erfüllt. |
| Erklärung und Lauf festhalten | Eine Kopie mit der eigenen Erklärung angelegt. |
| Browsersicherung wählen und neu laden | Rückkehr nennt „Mein Reinigungsplan“; Code, Erklärung und festgehaltener Vergleich wiederhergestellt. |
| Transfer Prüfstation | Antwort „zweites aufnehmen“ erhält eine konkrete Erklärung des belegten Zustands und des vollständigen Arbeitsgangs. |
| Abschlussfolge `links;links;vor;vor` selbst aufbauen | Konkrekte Gegenüberstellung zur richtigen Entfaltung, keine Anerkennung der falschen Gruppierung. |
| Folge durch Zurücknehmen und Anhängen verbessern | `links;vor;links;vor` wird als zwei vollständige Durchläufe erkannt. |
| 390 × 844 | Kein horizontaler Seitenüberlauf; Sprung zum Bodenplan fokussiert dessen Überschrift. Befehle stehen in der schmalen Ansicht direkt beim Modell. |
| Breite Ansicht / Wiederherstellung | Ansicht um 1280 Pixel betrachtet; gesamter kleiner Raum, Code und erste Ausführung gemeinsam sichtbar. Viewport-Override anschließend zurückgesetzt. |
| Browserfehler | Keine Error-Einträge in der abgefragten Browser-Konsole. |

Der temporäre Browser-Teststand wurde über die Oberfläche aus der Browsersicherung entfernt. Zum Abschluss wurde der Einstieg neu geladen; die geöffnete Vorschau enthält einen frischen Stand.

## Grenzen der Prüfung

- Export-/Importformat mit gültigen und ungültigen Daten automatisiert geprüft, Importvorschau implementiert. Der vollständige Betriebssystem-Dateiauswahl-/Download-Rundlauf wurde nicht automatisiert im Browser geprüft.
- Sichtbare Fokusziele nach Ausführung und Sprüngen beobachtet; kein vollständiger Tastatur- oder Screenreaderdurchlauf. Responsive Stichprobe ist kein umfassendes Barrierefreiheitsaudit.
- Keine echte Lerngruppe, keine empirische Lernwirkungs- oder Zeitpassungsprüfung.
- Dieser Bericht hält die lokale Vorprüfung vor der Aufnahme ins Repository fest. Die anschließende Veröffentlichung wird über den Workflow „Reinigungsfall Pages“ protokolliert; die erste Fassung bleibt unter ihrer Adresse erhalten.
