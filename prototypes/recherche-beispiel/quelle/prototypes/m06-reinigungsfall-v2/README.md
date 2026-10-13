# Sauber geplant – zusätzliche Lernfassung 2

Eine deutlich überarbeitete Vorschau des Reinigungsfalls für IuM, Klasse 5. Erstellt am 13.09.2026 auf Grundlage der Lernendenanalyse. Die erste Fassung bleibt erhalten.

**[Öffentliche Lernfassung öffnen](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall-v2/)** · [Lokale Startdatei](index.html) · [erste Fassung vergleichen](../m06-reinigungsfall/reinigungsfall.html)

## Einstieg und Umfang

Die neun frei anwählbaren Lernschritte führen vom Bewegen und Drehen über eine eigene Vorhersage und Wiederholung zu einer neuen Ergänzung, Fehlerkorrektur, vollständigen Reinigung und einem eigenen Plan. Transfer und Abschluss schließen an. Die Schritte sind keine neun Unterrichtsstunden; der bestehende Rahmen von fünf Unterrichtseinheiten bleibt eine noch zu erprobende Planung.

| Schritt | Fachlicher Schwerpunkt | Eigene Lernhandlung |
|---|---|---|
| Bewegen & drehen | Ort und Blick unterscheiden | Zwei Aktionen einzeln untersuchen und erklären |
| Erst vorhersagen | Feste Folge verfolgen | Endkachel und Richtung festlegen, mit Fahrt vergleichen |
| Die Klammer verstehen | Ganzer Körper je Durchlauf | Zwei Durchläufe prüfen und Reihenfolge begründen |
| Selbst ergänzen | Neue Startlage | Passenden Drehbefehl selbst ableiten |
| Einen Fehler finden | Absicht und Code vergleichen | Erste Abweichung finden, Klammer korrigieren |
| Alles sauber? | Beendete Fahrt und Abdeckung unterscheiden | Verbliebene Kachel erreichen und Ergänzung erklären |
| Mein Reinigungsplan | Eigenen Algorithmus entwickeln | Papiergrafik, Code, Prüfung und Erklärung verbinden |
| Übertragen | Körperregel in anderem Zustandsmodell | Werkstück-Prüfstation vergleichen; Modellgrenzen und Systemeinordnung besprechen |
| Was ich jetzt kann | Eigene Sicherung | Neue Befehlsfolge selbst aufbauen, prüfen und begründen |

## Was gegenüber der ersten Fassung verbessert ist

- Aufgabenspezifische Rückmeldung: Eine richtige Vorhersage wird nicht wegen fehlender Flächendeckung abgewertet. Die Randrunde und der vollständige Reinigungsauftrag haben getrennte Kriterien.
- Der Bodenplan bleibt nach Codeänderungen sichtbar. Der alte Lauf gehört weiterhin zu seiner alten Fassung.
- Aktiver Körperbefehl und Durchlauf sind sichtbar; „Bis Körperende“ erlaubt die Untersuchung ganzer Durchläufe. Eine Fahrspur ergänzt die besuchten Kacheln.
- Die Ergänzung hat eine neue Startlage; ihre Lösung steht nicht bereits im eigenen Arbeitsbereich.
- Kurze, gezielte Erklärfragen, konkrete Vergleiche und eine optionale Teilplanung helfen beim Übergang zum eigenen Entwurf.
- Abschluss und Rückkehr verwenden unterschiedliche Beispiele. Die Lernenden bauen die Befehlsfolge selbst aus Grundbefehlen auf und erhalten eine konkrete Korrektur.
- Eingaben lassen sich als Datei mitnehmen oder nach bewusster Auswahl im Browser sichern. Code, Erklärungen, ursprüngliche Lauferwartungen und festgehaltene Vergleiche gehören zum Stand.
- Für schmale Ansichten gibt es Sprünge zwischen Auftrag und Bodenplan sowie Code direkt am Modell. Keine automatische Sperre des Lernwegs.

## Nutzung im Unterricht

Eine Erklärung bleibt ein fachliches Lernprodukt. Die Simulation prüft die Fahrt; geschlossene Aufgaben prüfen die ausgewählte bzw. aufgebaute Antwort. Eine richtige Auswahl oder eine erfolgreiche Route ist kein vollständiger Nachweis selbstständigen Verstehens. Beispielerklärungen sind Vergleichsangebote, keine Benotung.

Eine geeignete Begleitung: zunächst Bewegung und Drehung bei Bedarf gemeinsam modellieren, dann eigene Vorhersagen, Ergänzungen und Fehlererklärungen zulassen. Bei eigenen Plänen können zwei Lernende ihre unterschiedliche Flächenaufteilung vergleichen. Beide sollten dabei eine eigene Erklärung liefern. Bei Schwierigkeiten erst eine Zeile und den nächsten Zeilenwechsel planen.

Die Ablaufgrafik entsteht weiterhin auf Papier. Das kleine Diagramm in der Hilfe zeigt nur eine Teilroute. Der eigene Plan wird in Code übertragen und mit der Ausführung verglichen. Die Lehrkraft prüft, ob Papierdarstellung, Code und Erklärung zusammenpassen.

Falls das Gerät ausfällt: Raster und Pfeil auf Papier verwenden, die Befehle mit einem Gegenstand ausführen und jeweils Ort/Blick festhalten. Vor einem nächsten Termin Codekopie, offene Frage und nächste Handlung sichern. Bei unklarem Lernstand mit einer neuen kurzen Körperentfaltung beginnen.

## Sicherung

- Standard: nur im aktuellen Tab. Beim Neuladen gehen ungesicherte Eingaben verloren.
- **Sichern → Sicherung als Datei laden:** JSON-Datei ohne Namen oder Konto. Die Datei enthält die tatsächlich eingegebenen Texte und Programme.
- **Auf diesem Gerät im Browser behalten:** freiwilliges `localStorage` unter dem eigenen Schlüssel `ium-cleaning-learning-v2`. Wiederaufnahme startet mit einer Rückkehransicht. Auf gemeinsam genutzten Geräten besser eine Datei verwenden.
- **Eine Sicherung öffnen:** Version, Struktur und Umfang werden geprüft; vor Übernahme erscheint eine Vorschau. Die Übernahme ersetzt den aktuellen Stand ausdrücklich erst nach dem zugehörigen Knopf.
- Nur Dateien dieser Version, maximal 300 KB; maximal zehn festgehaltene Vergleiche je Simulationsfall. Ein älterer Browserstand bleibt bei fehlgeschlagener Sicherung erhalten, die Oberfläche meldet den Fehler.
- Browserdaten sind an Browser und Adresse gebunden. Für andere Geräte oder einen Wechsel zur veröffentlichten Seite eine Datei mitnehmen.
- Kein Serverkonto, keine Übertragung der Lernantworten und keine Telemetrie. Browserdaten können gelöscht werden; eine zusätzliche Datei bleibt sinnvoll.

## Lokal starten

Aus dem Repository-Stamm:

```powershell
python -m http.server 43863 --bind 127.0.0.1 --directory prototypes
```

Dann `http://127.0.0.1:43863/m06-reinigungsfall-v2/` öffnen. HTML, CSS und JavaScript sind statisch und ohne externe Laufzeitabhängigkeiten. Ein vorhandener Server mit anderem Port ist ebenfalls geeignet.

## Technischer Aufbau und Prüfung

- `cleaning-core.js`: unveränderte Kopie des bisherigen Bewegungs-/Wiederholungsmodells.
- `lesson-model.js`: Lernfälle, Aktionszuordnung, fachliche Vergleiche und Sicherungsformat.
- `app.js`, `index.html`, `app.css`: zusätzliche Oberfläche.
- `lesson-model.test.cjs`: Tests für unterschiedliche Auftragsziele, Körperaktionen, neue Startlage, eigene Wege, unveränderliche Vorhersagen und Sicherungen.
- `QA.md`: tatsächliche lokale Vorprüfung und Grenzen. Der gemeinsame Veröffentlichungsbuild liegt in `../m06-reinigungsfall/build.cjs`.

```powershell
node --test prototypes/m06-reinigungsfall-v2/lesson-model.test.cjs
node --check prototypes/m06-reinigungsfall-v2/app.js
```

Bekannte Grenzen: keine reale Lernerprobung, kein vollständiges Barrierefreiheitsaudit, kein produktiver Kurs-/Dossiervertrag, keine echte Robotersteuerung. Jede besuchte Kachel einschließlich Start zählt als sauber; keine Sensoren, Bedingungen oder verschachtelten Wiederholungen. Bedingtes Reagieren und optionale ComThink-Hardware bleiben spätere Vertiefung.

## Forschungs- und Analysegrundlage

Die Fassung setzt eine Analyse von zwölf Lernhürden um: aufgabengerechte Rückmeldungen, verknüpfte Darstellungen, abgestufte Anleitung, eigene Erklärungen sowie verlässliche Sicherung. Forschung begründet diese Gestaltung, validiert aber nicht diese konkrete Fassung:

- [Paas & van Merriënboer (2020)](https://repub.eur.nl/pub/128824/Repub_128824_O-A.pdf): zusammengehörige Informationen verbinden und Anleitung dem Vorwissen anpassen.
- [Wisniewski et al. (2020)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full): Informationsgehalt von Rückmeldungen.
- [Barbieri et al. (2023)](https://www.danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf): Lösungsbeispiele; Übertragung aus Mathematik auf diesen Fall bleibt begründet, aber ungeprüft.
- [Bisra et al. (2018)](https://eric.ed.gov/?id=EJ1186664): gezielte Selbsterklärungen.
- [Yang et al. (2021)](https://pubmed.ncbi.nlm.nih.gov/33683913/): Abrufübungen und Rückmeldung.

Für den informellen Austausch im engen Kreis: Eindrücke direkt an Jan. Es wird kein strukturierter externer Prüfauftrag vorausgesetzt.

## Veröffentlichung als Beispielinhalt

Die [Projektstartseite](https://h4r7w16.github.io/ium-lernwerk/) führt zur Lernfassung 2 unter `reinigungsfall-v2/`. Die [erste Reinigungsfassung](https://h4r7w16.github.io/ium-lernwerk/reinigungsfall.html) und der frühere Prüffahrt-Entwurf bleiben erhalten. Der gemeinsame Build veröffentlicht nur ausdrücklich freigegebene statische Dateien, keine Tests oder lokalen Lernstände. Die Modelllogik ist gegenüber der lokal geprüften zusätzlichen Fassung unverändert.

Vom Repo-Stamm: `node prototypes/m06-reinigungsfall/build.cjs`. Der Ausgabeordner darf noch nicht existieren; optional einen neuen Ausgabeordner als Argument angeben. Der Workflow „Reinigungsfall Pages“ prüft beide Fassungen und den Build. Ein manueller Start auf `main` veröffentlicht. Die Startdatei `pages-entry.html` ist ausschließlich für die veröffentlichte Root-Adresse bestimmt.
