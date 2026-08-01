# IUM11 – Pilotierungsdesign für `GRADE-7-WORKING-40`

**Status:** `design-approved` – schriftliches Spezifikationsreview ausstehend

**Stand:** 1. August 2026

**Scope:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klasse 7, Niveau E

**Voraussetzung:** Die Working-40-Implementierung auf Schema 3 ist angenommen; ihr Ausgangszustand bleibt `working / conditional / amber / covered / not-started / partial`.

**Implementierungsgrenze:** Diese Spezifikation entwirft Pilotprotokoll, Offline-Cockpit, Evidenzpakete, Validatoren und Reviewfolge. Sie implementiert weder das Cockpit noch Lernmodule, führt keine Pilotierung durch, erhebt keine realen Daten und verändert keinen Produktstatus.

## 1. Zweck

IUM10 enthält 36 typisierte Pilotaufträge und einen fail-closed Verfügbarkeitsvertrag für den Klasse-7-Pfad. Diese Verträge begrenzen bereits Scope, Messgrößen, Privacy und Statusfolgen. Sie sind jedoch noch keine praktisch ausführbare Pilotierung.

IUM11 operationalisiert deshalb:

- vier Clusterpiloten mit den zehn Klasse-7-Kernmodulen;
- einen nachgelagerten End-to-End-Pilot des vollständigen 40-UE-Pfads;
- klassenaggregierte Lernqualitätsindikatoren ohne Individualdiagnostik;
- ein lokales Offline-Cockpit ohne Konto, Backend oder Netzwerkzugriff;
- maschinenprüfbare Evidenz- und Entscheidungspakete;
- feste `pass`-, `fail`- und `not-evaluable`-Regeln;
- getrennte Fach-, Engineering-/Privacy- und Auftraggebergates;
- einen wiederverwendbaren Pilotkern für eine spätere Klassen-5/6-Erweiterung.

Der Pilot ist eine Entwicklungsprüfung. Er untersucht, ob der 40-UE-Pfad unter dokumentierten Einsatzbedingungen zeitlich durchführbar ist, die vereinbarten Lernhandlungen und Übergaben erhält und lernqualitätsnah tragfähig erscheint. Er ist keine vergleichende Wirkungsstudie und erlaubt keine kausale Aussage über Lernwirksamkeit.

## 2. Freigegebene Grundentscheidungen

| Frage | Entscheidung |
|---|---|
| Geltungsbereich | Klasse 7 vollständig; gemeinsamer Kern später für Klassen 5/6 wiederverwendbar |
| Evidenzanspruch | Durchführbarkeit, Vertragstreue und klassenaggregierte Lernqualitätsindikatoren |
| Replikation | Minimalpilot: je Cluster eine positive Durchführung, danach eine positive Jahresdurchführung |
| Lernendenperspektive | Lehrkraftbefund plus kurzer, ausschließlich klassenaggregierter Lernendenimpuls |
| Dokumentationsweg | lokales Offline-Formular mit validiertem, versioniertem JSON-Export |
| Gesamtarchitektur | vertragsgeführtes Pilot-Cockpit mit gemeinsamem Kern, vier Clusterpaketen und Jahrespaket |

Der Minimalpilot darf nur Aussagen für die dokumentierten Einsatzbedingungen tragen. Er begründet weder `reviewed`, `standard`, allgemeine Übertragbarkeit noch kausale Wirksamkeit.

## 3. Normative und didaktische Grundlage

### 3.1 Vertragsgrundlage

Autoritative Ausgangsbasis bleibt `roadmap/time-model.json` mit:

- `schemaVersion: 3`;
- `GRADE-7-WORKING-40`;
- `AVAIL-GRADE-7-WORKING-40`;
- den vier Integrationsverträgen;
- zehn Klasse-7-Kernmodulverträgen;
- zehn zugehörigen Modul-Pilotaufträgen;
- vier Integrations-Pilotaufträgen;
- `PILOT-GRADE-7-WORKING-40`;
- den Status- und Privacy-Invarianten.

Das Pilotierungsdesign darf diese Wahrheiten nicht duplizieren, abschwächen oder implizit ersetzen.

### 3.2 Curriculare Aussagegrenze

- Der Aufbaukurs Informatik 2016 bleibt für Klasse 7 `enacted` und normativer Curriculumanker.
- Die Lesehilfe 2026/2027 bleibt `orientation` und wird nicht zur Kompetenznorm hochgestuft.
- Curriculare Coverage wird weiterhin im Crosswalk und Coverageplan nachgewiesen, nicht durch Pilotzufriedenheit oder Zeitwerte.
- PROG-003/004 bleiben bis zu eigenständigem Fachaudit und Coveragegate `partial`.

### 3.3 Fachprofil- und WU-Grundlage

Das Design nutzt das `working`-Fachprofil Informatik und Medienbildung Gymnasium 5–7 sowie die lokal geprüften IBBW-WU-Exzerpte:

- Band 1: Angebots-Nutzungs-Modell, Tiefenstrukturen und Orchestrierung;
- Band 5: formatives Feedback, kriteriumsbezogene Rückmeldung und nächste Schritte;
- Band 6: Aufgabenvalidität, Sinn, kognitive Aktivierung und Adaptivität;
- Band 9: lernfunktionale Digitalität, Technikroutinen und Datenschutzsensibilität.

Diese Grundlagen begründen die Auswahl der Pilotindikatoren. Sie machen aus einem positiven Pilotbefund keinen empirischen Wirkungsnachweis.

## 4. Scope und Nicht-Ziele

### 4.1 Im Scope

- wiederverwendbarer operativer Pilotkern;
- Klasse-7-Konfiguration für zehn Kernmodule, vier Integrationen und einen Jahrespfad;
- Bereitschafts-, Cluster- und Jahresprotokolle;
- strukturierte Kriterien für Lernhandlungen, Lernphasen und Übergabeprodukte;
- klassenaggregierter Lernendenimpuls;
- Offline-Cockpit und rein lokale Datenverarbeitung;
- Evidenz-, Entscheidungs- und Validierungsschema;
- Dokumentation, synthetische Beispiele und Teststrategie;
- Review- und Auftraggebergates.

### 4.2 Außerhalb des Scopes

- Entwicklung der zehn Lernmodule;
- Lernendenanwendung oder Plattformfundament;
- reale Pilotdurchführung oder Speicherung realer Pilotdaten;
- personenbezogene Diagnostik, Kompetenzprofile oder Telemetrie;
- Kontrollgruppen, Vorher-Nachher-Individualtests oder Wirkungsschätzungen;
- vollständige Pilotkonfiguration für Klassen 5/6;
- Pilotierung flexibler Vertiefungs-, Transfer- und Projektmodule;
- automatische Statusänderung in `time-model.json`;
- Statushochsetzung auf `available`, `green`, `completed`, `covered`, `reviewed` oder `standard`;
- Phase 1.

Flexible Vertiefungs-, Transfer- und Projektmodule bleiben erhalten. Sie liegen außerhalb der 40 Kern-UE und kompensieren weder gescheiterte Integrationen noch fehlende Kernzeit.

## 5. Systemarchitektur

### 5.1 Systemgrenze

Das Pilot-Cockpit ist ein eigenständiges Qualitätssicherungswerkzeug für Pilotlehrkräfte und Reviewrollen. Es ist:

- kein Teil der Lernendenanwendung;
- kein LMS;
- keine Diagnostikplattform;
- kein Bewertungssystem;
- kein Statuseditor für das produktive Zeitmodell.

Es liest versionierte Pilot- und Vertragskonfiguration, nimmt ausschließlich aggregierte Eingaben entgegen, validiert sie lokal und erzeugt explizit heruntergeladene JSON-Pakete.

### 5.2 Komponenten

1. **Pilotkern**
   - gemeinsame Feldtypen;
   - Privacyregeln;
   - Evidenzstatus;
   - Schwellenlogik;
   - Export-/Importlogik;
   - Accessibility- und Offlinebasis.

2. **Klasse-7-Adapter**
   - vier Clusterkonfigurationen;
   - zehn Modul-Unterprüfungen;
   - Integrations- und Rückfallbindungen;
   - Jahreskonfiguration.

3. **Offline-Cockpit**
   - statisches, selbstenthaltenes Webartefakt;
   - strukturierte Eingabe und lokale Validierung;
   - keine dauerhafte Browserspeicherung;
   - JSON-Export und Dateiimport.

4. **Repositoryvalidator**
   - Schema-, Vertrags-, Fingerprint-, Privacy- und Statusprüfung;
   - Zusammenführung zulässiger Pakete;
   - Erzeugung eines Entscheidungspakets;
   - keine Mutation des Zeitmodells.

5. **Review- und Publikationsschicht**
   - Lehrkräfteanleitung;
   - Fachreviewvertrag;
   - Engineering-/Privacyreviewvertrag;
   - Auftraggeberentscheidung;
   - öffentliche Zusammenfassung erst nach Freigabe.

### 5.3 Autoritätsgrenzen

| Artefakt | Autorität |
|---|---|
| `roadmap/time-model.json` | Verträge, Pilotaufträge, Status, Rückfälle |
| `pilot/pilot-protocol.json` | operative Pilotabläufe, Kriterien, Schwellen und Paketbindungen |
| Evidenzpaket | Befund genau einer durchgeführten Pilotstufe |
| Entscheidungspaket | validierte Zusammenführung, Status-Empfehlung und Aussagegrenze |
| Auftraggeberentscheidung | einzige Freigabe einer produktiven Statusänderung |

Das operative Pilotprotokoll referenziert Vertrags-IDs und einen Fingerprint des autoritativen Zeitmodells. Es enthält keine zweite Statuswahrheit.

## 6. Pilotfolge

### 6.1 Bereitschaftsprüfung

Vor jeder realen Pilotdurchführung müssen mindestens vorliegen:

- fachlich reviewfähige Lernmaterialien für alle Module des Scopes;
- zugehöriges Lehrkräftehandbuch;
- vollständige Ankeraufgaben und Kriterien;
- funktionierende digitale Werkzeuge und lokale Fallbacks;
- geprüfte Privacygrenzen;
- reale schulische Kapazität für das Cluster beziehungsweise den Jahrespfad;
- aktueller Vertrags- und Protokollfingerprint.

Fehlt eine Voraussetzung, startet der Pilot nicht. Ein Unterrichtsversuch mit unvollständigem Material ist kein negativer Pilotbefund, sondern `not-ready`.

### 6.2 Vier Clusterpiloten

| Reihenfolge | Integrationspilot | Kernmodule | Budget | Rückfall bei Scheitern |
|---:|---|---|---:|---:|
| 1 | `PILOT-INT-7-DATA-CODING` | `IUM-7-CORE-01`, `IUM-7-CORE-02` | 8 UE | +3 UE |
| 2 | `PILOT-INT-7-PROGRAMMING` | `IUM-7-CORE-03`, `IUM-7-CORE-04` | 11 UE | +2 UE |
| 3 | `PILOT-INT-7-NET-SECURITY` | `IUM-7-CORE-05`, `IUM-7-CORE-06`, `IUM-7-CORE-07` | 11 UE | +3 UE |
| 4 | `PILOT-INT-7-DATA-MEDIA-SOCIETY` | `IUM-7-CORE-08`, `IUM-7-CORE-09`, `IUM-7-CORE-10` | 10 UE | +6 UE |

Ein Clusterlauf erzeugt:

- je enthaltenem Kernmodul einen Modul-Unterbefund für `PILOT-IUM-7-CORE-*`;
- einen Integrationsbefund;
- einen Zeit- und Phasenbefund;
- einen Technik-/Privacybefund;
- einen klassenaggregierten Lernendenimpuls oder bei weniger als zehn gültigen Antworten dessen dokumentierte Unterdrückung;
- genau ein Cluster-Evidenzpaket.

Die zehn Kernmodulpiloten benötigen damit keine zehn zusätzlichen Unterrichtsdurchführungen. Ihre Evidenz entsteht innerhalb der vier Clusterläufe. Flexible Klasse-7-Modulpiloten bleiben `not-started` und außerhalb dieses Designs.

### 6.3 Nacharbeit und Wiederholung

- `pass`: Der Cluster darf als positive Voraussetzung des Jahrespiloten verwendet werden.
- `fail`: Eine Muss-Bedingung ist verletzt. Nacharbeit und erneuter Clusterlauf sind erforderlich.
- `not-evaluable`: Pflichtdaten oder Interpretierbarkeit fehlen. Ursache beheben und erneut durchführen.

Eine gescheiterte oder nicht auswertbare Durchführung erfüllt den Minimalumfang nicht. Der Minimalpilot meint mindestens einen positiven, nicht höchstens einen Lauf.

### 6.4 Jahrespilot

`PILOT-GRADE-7-WORKING-40` darf nur beginnen, wenn:

- vier positive Clusterpakete vorliegen;
- alle Pakete dieselbe zulässige Protokoll- und Vertragsversion referenzieren;
- keine verpflichtende Entwicklungswarnung unbearbeitet bleibt;
- der vollständige Material- und Technikstand für 40 UE bereit ist.

Der Jahrespilot führt die verbindliche Folge `8 + 11 + 11 + 10 = 40 UE` als zusammenhängenden Jahrespfad durch. Frühere Clusterpakete ersetzen dabei keine erneute Beobachtung der realen Übergänge im Jahreszusammenhang.

## 7. Evidenzmodell

### 7.1 Vier Evidenzspuren

Jedes Cluster- und Jahrespaket enthält getrennte Evidenzspuren:

1. `deliveryTimeEvidence` – Zeit, Phasen und Fallbacks;
2. `learningQualityEvidence` – fachliche Lernhandlungen, Produkte und Revision;
3. `learnerPulseEvidence` – ergänzende klassenaggregierte Lernendenperspektive;
4. `technicalPrivacyEvidence` – Technik, Rückfallebene und Privacy.

Keine Evidenzspur darf eine andere überschreiben.

### 7.2 Zulässige Kontextfelder

Zulässig sind ausschließlich grobe, nicht identifizierende Kontextklassen:

- Schuljahr;
- Halbjahr;
- Klassengrößenband;
- Geräteart;
- Browserfamilie;
- Netzwerkmodus;
- Pilot-Scope;
- Protokoll-, Tool- und Vertragsversion.

Klassengrößenbänder sind mindestens:

- `under-10`;
- `10-19`;
- `20-29`;
- `30-plus`.

### 7.3 Zeit- und Durchführungsevidenz

Erfasst werden:

- geplante UE;
- tatsächlich benötigte UE;
- Abschluss jeder erforderlichen Lernphase;
- Aktivierung einer Rückfallebene;
- aggregierter technischer Startaufwand;
- Unterstützungsbedarf als vordefiniertes Band;
- externe Störung, sofern sie die Interpretierbarkeit verhindert.

UE werden in einem vorab festgelegten Raster erfasst. Unterrichtsfremde Ausfälle werden nicht als Lernzeit gezählt und dürfen keine fachliche Kürzung legitimieren.

### 7.4 Fachliche und didaktische Evidenz

Jedes Modul erhält stabile Kriterien-IDs, die mindestens binden an:

- `centralLearningAction` des Modulvertrags;
- `centralLearningProduct` des Modulvertrags;
- erforderliche Lernphasen des `working-40`-Budgets;
- relevante `preservedLearningActions` der Integration;
- relevante `preservedProductAndCurriculumEvidence` der Integration.

Die Lehrkraft prüft die Lernprodukte ausschließlich im Unterricht. Exportiert werden weder Produkte noch Ausschnitte, Screenshots, Programme, Bilder, Texte, Links oder Dateipfade.

Für jedes Muss-Kriterium wird nur ein Klassenband exportiert:

| Band | Projektdefinition |
|---|---|
| `strong` | mindestens drei Viertel erfüllen das Kriterium mit den vorgesehenen Hilfen |
| `mixed` | mindestens die Hälfte, aber weniger als drei Viertel |
| `weak` | weniger als die Hälfte oder zentrale Lernhandlung kommt nicht zustande |

Die Schwellen sind Projekt-Akzeptanzgrenzen, keine empirischen Normen und keine Bewertung einzelner Lernender.

### 7.5 Clusterbezogene Anker

| Cluster | Fachliche Ankerspur |
|---|---|
| Daten und Codierung | getestetes Bit-Codebuch → Pixelraster und Bildcodec → Datenmengen- und Ressourcenurteil |
| Programmieren | synchrones Code-/Zustandstrace → Implementierung → Normal-, Grenz- und Gegenfälle → Debugginghypothese und begründete Reparatur |
| Netze und Sicherheit | Netz-/Client-Server-Modell → Schutzbedarf und Schlüsselmodell → Brute Force/Häufigkeitsanalyse → revidiertes Sicherheitsurteil |
| Daten, Medien und Gesellschaft | Akteurs-/Evidenzdossier → Mechanismus- und Redesignanalyse → Medienprodukt, Rechteprüfung, Gegenperspektive und Revision |

Das operative Protokoll darf diese Ankerspuren ausdifferenzieren, aber keine vertraglich erhaltene Lernhandlung entfernen.

### 7.6 Lernendenimpuls

Der Lernendenimpuls umfasst exakt drei Entwicklungsfragen:

1. `clarity`: „Ich wusste, was ich fachlich bearbeiten sollte.“
2. `cognitiveEngagement`: „Ich musste erklären, prüfen, testen oder begründen – nicht nur klicken oder abschreiben.“
3. `supportUsefulness`: „Die Hilfen halfen mir weiter, ohne die Lösung vorzugeben.“

Antwortkategorien sind:

- `agree`;
- `partly`;
- `disagree`;
- `no-answer`.

Die Lernenden geben keine Freitexte ab. Das Cockpit erhält nur bereits gezählte Klassensummen. Es speichert keine Einzelantworten oder Antwortreihenfolgen.

Bei weniger als zehn gültigen Antworten wird kein Lernendenaggregat exportiert. Stattdessen wird `suppressed-small-group` gesetzt. Dieser datenschutzbegründete Zustand macht den Gesamtpilot nicht allein `not-evaluable`, weil der Lernendenimpuls ergänzend ist.

Wenn bei einer Frage mindestens ein Drittel der gültigen Antworten `disagree` lautet, entsteht eine verpflichtende Entwicklungswarnung. Sie ist kein Kompetenzbefund, darf aber vor der nächsten Pilotstufe nicht unbearbeitet bleiben.

### 7.7 Technik- und Privacyevidenz

Erfasst werden nur:

- Funktionsfähigkeit des vorgesehenen Werkzeugs;
- verwendete Browser-/Geräteklasse;
- Einsatz der lokalen Rückfallebene;
- standardisierter Problemcode;
- standardisierte Schweregradklasse;
- Privacygate-Ergebnis.

Ein technischer Fallback ist nur positiv, wenn er dieselbe Lernfunktion innerhalb des Budgets erhält.

### 7.8 Verbotene Felder und Nutzungen

Verboten sind insbesondere:

- Namen und Initialen;
- Schul-, Lehrkraft-, Klassen- oder Kursbezeichnungen;
- E-Mail-Adressen, Konten und Kennungen;
- exakte Unterrichtsdaten oder Stundenplaninformationen;
- Freitextfelder;
- Lernendenprodukte und Produktlinks;
- Fotos, Audio, Video oder Screenshots;
- Einzelantworten und individuelle Lernverläufe;
- Geräte-, Netzwerk- oder Browserkennungen;
- IP-Adressen und Telemetrie;
- private Reflexionsinhalte;
- Noten, Rankings und Kompetenzprofile;
- automatisierte personenbezogene Bewertung;
- Schülerprodukte als Zeitbeleg.

Unbekannte Felder werden fail-closed abgelehnt.

## 8. Paketmodell und lokaler Datenfluss

### 8.1 Evidenzpaket

Ein Evidenzpaket enthält mindestens:

- `schemaVersion`;
- `packageType`;
- eine zufällige, nicht auf Personen oder Institutionen abbildbare `packageId`;
- `protocolVersion`;
- `toolVersion`;
- `timeModelFingerprint`;
- `scopeType` und `scopeId`;
- zulässige Kontextklassen;
- die vier Evidenzspuren;
- berechneten Ergebnisstatus;
- Entwicklungswarnungen;
- Retentionsklasse `until-decision`.

Die `packageId` identifiziert nur das Paket. Es darf außerhalb des Pakets keine Zuordnung zu Schule, Lehrkraft oder Lerngruppe geben.

### 8.2 Offlineverarbeitung

Das Cockpit arbeitet:

- ohne Server und Backend;
- ohne Konto;
- ohne Netzwerkzugriff;
- ohne CDN, externe Schrift oder Analysedienst;
- ohne Cookie;
- ohne Local Storage;
- ohne IndexedDB;
- ohne Service-Worker-Telemetrie;
- standardmäßig nur im Arbeitsspeicher.

Ein Paket entsteht ausschließlich durch bewussten Download. Import erfolgt über standardisierte lokale Dateiauswahl. Ein Schließen der Seite ohne Export verwirft den Zustand.

### 8.3 Vertragsbindung

Das selbstenthaltene Cockpit führt einen eingebetteten Fingerprint der zulässigen Vertrags- und Protokollversion. Bei Import prüft es:

- Schema;
- Scope;
- Protokollversion;
- Toolversion-Kompatibilität;
- Zeitmodellfingerprint;
- Pflichtfelder und Typen;
- Privacy-Ausschlüsse;
- Summen und Schwellen;
- Ergebnisableitung.

Versions- oder Fingerprintkonflikte sind `not-evaluable` und blockieren Zusammenführung.

### 8.4 Entscheidungspaket

Der Repositoryvalidator erzeugt aus zulässigen Evidenzpaketen ein Entscheidungspaket mit:

- fünf Pilotresultaten;
- zehn Modul-Unterbefunden;
- vier Integrationsbefunden;
- Zeit- und Rückfallbilanz;
- Technik-/Privacybilanz;
- Entwicklungswarnungen und deren Bearbeitungsstatus;
- Aussagegrenze des Minimalpiloten;
- Status-Empfehlung;
- Reviewstatus.

Das Entscheidungspaket enthält keine produktive Statusmutation.

### 8.5 Aufbewahrung und Veröffentlichung

- Reale Evidenzpakete werden nicht in das öffentliche Git-Repository committed.
- Sie verbleiben in einer nichtöffentlichen, zugriffsbeschränkten Projektablage bis zur Auftraggeberentscheidung.
- Nach der Entscheidung werden Evidenzpakete gelöscht, sofern keine ausdrücklich dokumentierte institutionelle Aufbewahrungspflicht besteht.
- Dauerhaft erhalten bleibt nur das nichtpersonale Entscheidungspaket beziehungsweise eine weiter minimierte öffentliche Zusammenfassung.
- Das Repository enthält ausschließlich Protokoll, Schemas, Cockpitquellen, Dokumentation und synthetische Testdaten.

## 9. Entscheidungslogik

### 9.1 Clusterstatus

Ein Cluster ist nur `pass`, wenn:

- tatsächliche UE sein festes Clusterbudget nicht überschreiten;
- alle Modul-Unterbefunde `pass` sind;
- alle erforderlichen Lernphasen durchgeführt wurden;
- jedes Muss-Kriterium `strong` ist;
- das Übergabeprodukt vollständig vorliegt und funktional weiterverwendet wird;
- technische Kernfunktion oder gleichwertiger Fallback innerhalb des Budgets funktioniert;
- Privacygate positiv ist;
- keine verpflichtende Entwicklungswarnung unbearbeitet bleibt.

Ein Cluster ist `fail`, sobald eine Muss-Bedingung verletzt wird.

Ein Cluster ist `not-evaluable`, wenn:

- Pflichtdaten fehlen oder widersprüchlich sind;
- Vertrags- oder Protokollversion nicht passt;
- eine externe Störung den Zeit- oder Lernqualitätsbefund uninterpretierbar macht;
- das Paket technisch beschädigt ist.

Eine Datenschutzverletzung ist `fail`, nicht `not-evaluable`. Das betroffene Paket darf nicht exportiert oder weiterverarbeitet werden.

### 9.2 Keine Zeitverrechnung

Unterläufe eines Clusters dürfen Überläufe eines anderen Clusters nicht kompensieren. Die vier Budgets sind load-bearing, weil die Integrationen jeweils eigene fachliche Übergaben tragen.

### 9.3 Additive Rückfälle

Scheiternde Integrationen aktivieren exakt:

- Daten und Codierung: +3 UE;
- Programmieren: +2 UE;
- Netze und Sicherheit: +3 UE;
- Daten, Medien und Gesellschaft: +6 UE.

Mehrere Rückfälle werden addiert. Der berechnete Bedarf erzeugt keine automatisch verfügbare Jahresvariante.

### 9.4 Jahresstatus

Der Jahrespilot ist nur `pass`, wenn:

- vier zulässige positive Clusterpakete vorliegen;
- die Jahresdurchführung selbst exakt die vereinbarte Folge erhält;
- jedes Cluster erneut innerhalb seines Budgets bleibt;
- die Gesamtsumme 40 UE nicht überschreitet;
- erforderliche Lernphasen, Übergaben und Anker erneut positiv sind;
- die fünf Verfügbarkeitsgates positiv sind;
- keine verbotene Kompensation verwendet wird.

### 9.5 Status-Empfehlung

Ein vollständig positiver Minimalpilot erzeugt ausschließlich:

```text
eligible-for-working-availability-review
```

Er setzt keinen Status automatisch. Erst nach:

1. Fachreview;
2. Engineering-/Privacyreview;
3. schriftlichem Auftraggebergate

dürfen `availabilityStatus: available`, `timeFeasibilityStatus: green` und `pilotStatus: completed` gesetzt werden.

Dabei bleibt:

- `status: working`;
- `semanticCoverageStatus: partial`, bis ein separates Fachaudit und Coveragegate PROG-003/004 tragen;
- jede Aussage auf die dokumentierten Einsatzbedingungen begrenzt.

`reviewed` und `standard` sind durch den Minimalpilot ausgeschlossen. `reviewed` benötigt mindestens eine unabhängige zweite End-to-End-Jahresdurchführung sowie ein neues Review- und Auftraggebergate.

## 10. Rollen und Verantwortlichkeiten

### 10.1 Pilotlehrkraft

- führt den Unterricht durch;
- prüft Lernprodukte ausschließlich lokal;
- aggregiert Beobachtungen und Lernendenimpuls;
- exportiert das Evidenzpaket;
- entscheidet nicht allein über Produktstatus.

### 10.2 Pilotkoordination

- prüft formale Vollständigkeit;
- verwaltet nichtöffentliche Evidenzpakete;
- besitzt keinen Bedarf an Rohprodukten oder Individualdaten;
- veranlasst Wiederholung bei `fail` oder `not-evaluable`;
- erzeugt keine fachliche Freigabe.

### 10.3 Fachreview

Prüft mindestens:

- Curriculumanbindung und Operatorentiefe;
- zentrale Lernhandlungen und Lernprodukte;
- Qualität der Ankeraufgaben;
- Übung, Feedback, Revision, Sicherung und Transfer;
- tatsächliche Übergabekontinuität;
- Aussagegrenzen der Klassenbänder und des Minimalpiloten.

### 10.4 Engineering-/Privacyreview

Prüft mindestens:

- Schema- und Fingerprintkonsistenz;
- Offline- und No-Persistence-Verhalten;
- fail-closed Ableitung;
- verbotene Felder und Exporte;
- additive Rückfälle;
- Paket- und Dokumentationssynchronität;
- Accessibility- und Browserbaseline.

### 10.5 Auftraggeber

Allein der Auftraggeber entscheidet schriftlich über eine produktive Statusänderung. Eine technisch erzeugte Empfehlung besitzt keine Freigabewirkung.

## 11. Technische Artefakte

Die spätere Umsetzung soll mindestens enthalten:

```text
pilot/pilot-protocol.json
pilot/schemas/evidence-package.schema.json
pilot/schemas/decision-package.schema.json
pilot/cockpit/index.html
pilot/cockpit/assets/
pilot/docs/teacher-guide.md
pilot/docs/review-guide.md
pilot/examples/synthetic-cluster-pass.json
pilot/examples/synthetic-cluster-fail.json
pilot/examples/synthetic-annual-pass.json
scripts/validate_ium11.py
tests/test_validate_ium11.py
tests/test_ium11_cockpit_contract.py
```

Der konkrete Buildzuschnitt wird im späteren TDD-Plan festgelegt. Das ausgelieferte Cockpit muss als selbstenthaltenes statisches Artefakt ohne externe Runtime-Abhängigkeit funktionieren.

## 12. Wiederverwendung für Klassen 5 und 6

Wiederverwendbar sind:

- Evidenzspurtypen;
- Klassenbänder;
- Lernendenimpuls;
- Privacy-Ausschlüsse;
- Paket- und Fingerprintmodell;
- Offline-Cockpit;
- Status- und Reviewpipeline.

Jahrgangsspezifisch bleiben:

- Modul- und Integrations-IDs;
- Budgets;
- Lernhandlungen und Produkte;
- Cluster- oder Pfadfolge;
- Rückfalllogik;
- fachliche Ankeraufgaben.

Klassen 5/6 werden später durch Konfigurationsadapter ergänzt. IUM11 legt dafür keine scheinbar vollständigen Pilotverträge an.

## 13. Fehlerbehandlung

| Fehlerklasse | Cockpitreaktion | Paketfolge |
|---|---|---|
| Pflichtfeld fehlt | Export blockieren | `not-evaluable` |
| Summe widersprüchlich | Export blockieren | `not-evaluable` |
| unbekanntes/verbotenes Feld | Import/Export blockieren | Privacy-/Schemagate negativ |
| Fingerprint falsch | Import blockieren | `not-evaluable` |
| Paket beschädigt | Import blockieren | `not-evaluable` |
| Clusterbudget überschritten | Export mit negativem Ergebnis | `fail`, Rückfall aktivieren |
| Muss-Kriterium `mixed`/`weak` | Export mit negativem Ergebnis | `fail` |
| Technik versagt ohne gleichwertigen Fallback | Export mit negativem Ergebnis | `fail` |
| Privacyverletzung | Export und Verarbeitung blockieren | `fail`, Wiederholung erforderlich |
| kleine Gruppe beim Lernendenimpuls | Aggregat unterdrücken | `suppressed-small-group`, kein Alleinblocker |
| Lernendenwarnung | Warnung erzwingen | vor nächster Stufe bearbeiten |

Das Cockpit zeigt immer Ursache, betroffenen Scope und zulässigen nächsten Schritt. Es bietet keine Umgehung eines negativen Gates an.

## 14. Test- und Validierungsstrategie

### 14.1 Struktur- und Vertragsgates

- alle zehn Klasse-7-Kernmodule genau einmal in den vier Clustern;
- exakt vier Integrationspiloten und ein Jahrespilot;
- Modul-Unterbefunde an die zehn vorhandenen Modul-Pilot-IDs gebunden;
- Budgets exakt `8 / 11 / 11 / 10` und Gesamt `40`;
- Rückfälle exakt `3 / 2 / 3 / 6` und maximal `54`;
- keine flexible Modul-ID im Kernpfad;
- Klassen 5/6 unverändert.

### 14.2 Schema- und Mutationstests

Mindestens folgende Mutationen müssen scheitern:

- Personen-, Schul-, Klassen- oder Lehrkraftfeld ergänzt;
- Freitext, Produkt, Bild, Link oder Gerätekennung ergänzt;
- unbekanntes Feld eingeschleust;
- Klassensummen widersprüchlich;
- Lernendenimpuls unter Privacyschwelle exportiert;
- Muss-Kriterium `mixed` oder `weak` als `pass` gewertet;
- Clusterbudget überschritten und durch anderen Cluster kompensiert;
- technische Rückfallebene ohne gleiche Lernfunktion akzeptiert;
- Privacyverletzung als `not-evaluable` statt `fail` behandelt;
- Jahrespilot ohne vier positive Clusterpakete akzeptiert;
- Jahrespilot mit gemischten Fingerprints akzeptiert;
- Minimalpilot empfiehlt `reviewed` oder `standard`;
- Entscheidungspaket mutiert das produktive Zeitmodell.

### 14.3 Cockpitprüfung

- Export-/Import-Rundlauf ist verlustfrei;
- Zustand wird ohne Export nicht persistent gespeichert;
- kein Request verlässt das Cockpit;
- keine externe Schrift, Bibliothek, CDN oder Telemetrie;
- beschädigte Dateien werden verständlich abgewiesen;
- Tastatur- und Touchbedienung funktionieren;
- WCAG 2.2 AA ist technische Baseline;
- Fokus, Statusmeldungen, Fehlermeldungen und Kontrast sind zugänglich;
- aktuelle schulische Zielbrowser werden dokumentiert geprüft.

### 14.4 Repositorygates

Vor Implementierungsabnahme müssen frisch bestehen:

- vollständige Python-Testsuite;
- IUM11-Validator;
- IUM10-, IUM09- und Phase-0-Validator;
- JSON-, UTF-8- und Python-AST-Prüfung;
- Privacy-/Placeholder-/Legacy-Scans;
- Offline-/Netzwerkfreiheitstest;
- Dokumentationssynchronität;
- getrenntes Fach- und Engineeringreview.

## 15. WU-Check des Pilotierungsdesigns

- **Kognitive Aktivierung:** Positive Pilotbefunde benötigen ausgeführte fachliche Ankerhandlungen, nicht bloße Aktivität oder Produkterstellung.
- **Konstruktive Unterstützung:** Hilfen werden als Lernfunktion beobachtet; `strong` darf mit vorgesehenen Hilfen erreicht werden, ohne Hilfen als Defizitmerkmal einzelner Lernender zu behandeln.
- **Klassenführung und Struktur:** feste Pilotfolge, Pflichtfelder und Übergabegates schützen Lernzeit und Zielklarheit.
- **Aufgabenqualität:** Ankeraufgaben müssen das intendierte fachliche Ziel treffen; ihre Kriterien binden an Modul- und Integrationsverträge.
- **Feedback und Diagnose:** Produktprüfung und Lernendenimpuls steuern Materialrevision, erzeugen aber keine Individualdiagnostik.
- **Kooperation und Verantwortlichkeit:** Kooperative Produktbestandteile bleiben modulspezifisch; das Pilotdesign erfindet keine zusätzliche Gruppenmethode.
- **Diagnose-Fallback:** Fehlende oder nicht auswertbare Evidenz führt zu Nachsicherung und Wiederholung, nicht zu positiver Annahme.
- **Sprachsensibilität und Zugänglichkeit:** Kriterien, Impulsfragen und Cockpitmeldungen müssen verständlich und zugänglich sein.
- **Digitalität:** Das Offline-Cockpit nutzt Code für Validierung, Konsistenz und Wiederverwendung; es ersetzt keine fachliche Lehrkraftbeobachtung.
- **Wichtigste Grenze:** Ein einmaliger positiver Minimalpilot ist eine lokale Entwicklungsfreigabe, kein allgemeiner Wirksamkeitsnachweis.
- **WU-Quellenbasis:** IBBW-WU-Bände 1, 5, 6 und 9 in den lokal geprüften Exzerpten.

## 16. Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| Einmaliger Pilot wird übergeneralisiert | Aussagegrenze im Paket, Review und jeder Publikation verpflichtend |
| Lehrkraftband ist zu subjektiv | feste Kriterien, Schwellen, Ankeraufgaben und unabhängiges Fachreview |
| Lernendenimpuls wird als Lernerfolg interpretiert | explizit ergänzender Entwicklungsindikator; kein Kompetenzgate |
| Kleine Gruppe wird indirekt identifizierbar | Klassengrößenbänder und Unterdrückung unter zehn Antworten |
| Freitext enthält Personenbezug | keine Freitextfelder im Exportmodell |
| Rohprodukte gelangen in die Pilotablage | Schemagate, kein Uploadfeld, keine Produktlinks |
| Technikzeit wird idealisiert | tatsächliche UE, Technikaufwand und Fallback sichtbar erfassen |
| Clusterzeit wird querverrechnet | jedes Clusterbudget als eigenes hartes Gate |
| Jahrespilot nutzt veraltete Clusterdaten | einheitlicher Vertrags- und Protokollfingerprint erforderlich |
| Cockpit erzeugt Scheinautorität | nur Empfehlung; drei getrennte menschliche Gates |
| Materialien fehlen | Bereitschaftsgate blockiert reale Pilotierung |

## 17. Akzeptanzkriterien der späteren Implementierung

- [ ] Der Pilotkern ist unabhängig von Klasse-7-Konfigurationen verständlich und testbar.
- [ ] Vier Clusterpakete operationalisieren zehn Kernmodul- und vier Integrationspiloten.
- [ ] Der Jahrespilot akzeptiert nur vier positive, versionsgleiche Clusterpakete.
- [ ] Zeit-, Lernqualitäts-, Lernenden- und Technik/Privacyevidenz bleiben getrennt.
- [ ] Klassenbänder und Lernendenwarnung werden exakt wie freigegeben berechnet.
- [ ] Keine Personen-, Schul-, Lehrkraft-, Klassen-, Freitext- oder Produktdaten sind zulässig.
- [ ] Unter zehn Lernendenantworten wird das Aggregat unterdrückt.
- [ ] Das Cockpit arbeitet ohne Netzwerk und dauerhafte Browserspeicherung.
- [ ] Evidenzpakete sind versioniert, fingerprintgebunden und fail-closed validiert.
- [ ] Additive Rückfälle werden korrekt abgeleitet und nicht automatisch angeboten.
- [ ] Der Minimalpilot kann niemals `reviewed` oder `standard` empfehlen.
- [ ] Produktstatus wird ausschließlich nach Fachreview, Engineering-/Privacyreview und Auftraggebergate geändert.
- [ ] Klassen 5/6 und flexible Module bleiben unverändert.
- [ ] Öffentliche Repositoryartefakte enthalten nur Schemas, Werkzeug, Dokumentation und synthetische Daten.
- [ ] Fach-, WU-, Accessibility-, Privacy- und Engineeringgates sind dokumentiert.
- [ ] Alle Repositorytests und Validatoren bestehen.

## 18. Freigabefolge

1. Scope, Evidenzanspruch, Replikation, Lernendenperspektive und Dokumentationsweg wurden einzeln entschieden.
2. Das vertragsgeführte Pilot-Cockpit wurde als Gesamtarchitektur gewählt.
3. Systemgrenzen und Pilotfolge wurden freigegeben.
4. Evidenzarchitektur und Datenminimierung wurden freigegeben.
5. Schwellen, Fehlerbehandlung und Statusfolgen wurden freigegeben.
6. Artefakte, Datenfluss, Rollen, Wiederverwendung und Prüfstrategie wurden freigegeben.
7. Das Gesamtdesign wurde am 1. August 2026 ausdrücklich freigegeben.
8. Als nächstes folgt das Review dieser schriftlichen Spezifikation.
9. Erst nach schriftlicher Spezifikationsfreigabe darf mit `superpowers:writing-plans` ein TDD-Implementierungsplan erstellt werden.

Keine Freigabe dieses Dokuments erlaubt Cockpitimplementierung, Lernmodulentwicklung, reale Pilotierung, Datenerhebung, Statushochsetzung, Release oder Phase 1.
