# Fachprofil Informatik und Medienbildung – Gymnasium 5–7

**Status:** `working`
**Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
**Stand:** 29. Juli 2026

## 1. Zweck, Scope, Status und Abgrenzung

Dieses Profil übersetzt fachliche, fachdidaktische, lernpsychologische, curriculare und projektbezogene Grundlagen in Planungs- und Reviewregeln für das IuM-Lernwerk. Es steuert Modulroadmap, Lernaufgaben, Lernendenmaterial und Lehrkräftehandbuch; es ist weder Curriculum-Crosswalk noch Modulimplementierung.

- **Projektentscheidung:** Das Lernwerk ist ein öffentliches, offen lizenziertes digitales Primärmedium für lehrkraftorchestrierten Unterricht und soll einen vollständigen Lehrwerksersatz ermöglichen. ([Gesamtdesign, Abschnitte 1, 2.1, 2.3 und 2.5](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung:** Die erste Ausbaustufe gilt für Gymnasium 5–7 auf Niveau E; Niveaudifferenzierung und Klassen 8–11 sind nicht Teil dieses Profils. ([Gesamtdesign, Abschnitte 1 und 15](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · `working`:** Das Profil darf Planung vorläufig leiten. Es ist weder `reviewed` noch `standard`; die jahrgangsgenaue normative Verteilung bleibt bis zum Curriculum-Crosswalk in Task 12 offen. ([Gesamtdesign, Abschnitte 9.5 und 14](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung:** Das Profil legt keine Plattformkomponenten, Speicher- oder PWA-Implementierung und keine konkrete Modulserie fest. ([Gesamtdesign, Abschnitt 14](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 2. Quellenbasis und Regelhierarchie

Planungsleitende Aussagen werden in vier Regeltypen getrennt:

| Regeltyp | Kennzeichnung | Funktion und Reife |
| --- | --- | --- |
| persönliche pädagogische Arbeitsannahme | **Persönliche Arbeitsannahme · `working`** | stammt aus dem pädagogischen Workspace-Profil; darf vorläufig leiten, ist keine Forschungsaussage |
| Forschungsbefund oder inferentielle Forschungsfolge | **Forschungsregel** oder **Forschungsfolge** | zitiert nahe am Satz registrierte `CLAIM-*`-IDs; die Übertragung auf IuM 5–7 bleibt dort vorsichtig, wo der Claim sie begrenzt |
| curriculare oder normative Vorgabe | **Curriculumregel** | zitiert nahe am Satz eine amtliche `SRC-CUR-*`-Quelle und übernimmt deren Geltungsstatus |
| freigegebene Projektentscheidung | **Projektentscheidung** | verweist auf die freigegebene Projektspezifikation mit Abschnitt |

**Projektentscheidung:** In Kraft gesetzte curriculare Vorgaben begrenzen Projektentscheidungen; Projektentscheidungen konkretisieren den Produktscope; geprüfte Forschung begründet Lernfunktionen; persönliche Arbeitsannahmen konkretisieren Unterrichtskultur, dürfen aber keine der drei anderen Ebenen überschreiben. ([Gesamtdesign, Abschnitte 3 und 9.5](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

### Curriculare Quellen und Geltung

- **Curriculumregel:** Der Basiskurs Medienbildung 2016 ist für seinen ausgewiesenen Geltungsbereich `enacted` und normativer Anker für Medienbildung in Klasse 5. [SRC-CUR-BMB-2016]
- **Curriculumregel:** Der Aufbaukurs Informatik 2016 ist für Klasse 7 `enacted` und normativer Anker für Informatik in Klasse 7. [SRC-CUR-INF7-2016]
- **Curriculumregel · Orientierung:** Die Lesehilfe 2026/2027 ist `orientation`, nicht in Kraft gesetzte Norm. Sie darf Übergang, mögliche Verknüpfungen und ein vorläufiges Progressionsgerüst orientieren, aber BMB 2016 oder INF7 2016 nicht verdrängen. [SRC-CUR-LESEHILFE-2026-27]
- **Curriculumregel · administrativer Kontext:** `SRC-CUR-KM-FACHSEITE` und `SRC-CUR-KM-FAQ-REFORM` beschreiben den administrativen Übergang; sie sind keine Kompetenznormen.

### Weitere Grundlagen

- **Forschungsregel:** Die 15 Designprinzipien beruhen auf registrierten Claims. Ihre Status bleiben unverändert: zwölf `working`, drei `reviewed`, kein `draft` und kein `standard`.
- **Persönliche Arbeitsannahme · `working`:** Unterricht wird vom Lernprozess, einer sinnvollen Eigenleistung, gymnasialem Anspruch bei realistischer Zugänglichkeit, Transparenz und lernfunktionaler Digitalität her geplant. Diese Annahme stammt aus dem pädagogischen Workspace-Profil und ist kein empirischer Wirkungsnachweis.
- **Projektentscheidung:** Das Curriculum-Mapping, nicht eine Themenliste oder dieses Profil, muss die vollständige Abdeckung nachweisen. ([Gesamtdesign, Abschnitt 3](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 3. Fachkern und zentrale Denkweisen

Der Fachkern besteht aus zwei eigenständigen, aufeinander beziehbaren Strängen. Informatik untersucht und gestaltet Daten, Algorithmen und digitale Systeme. Medienbildung untersucht und gestaltet mediale Kommunikation, Repräsentationen, Interessen, Wirkungen und gesellschaftliche Handlungsmöglichkeiten.

### Gemeinsame Denkweisen

- **Curriculumregel:** Modellieren, implementieren, strukturieren, analysieren, vergleichen, testen, bewerten, kommunizieren und kooperieren müssen als fachliche Handlungen sichtbar werden; reine Themenzuordnung genügt nicht. [SRC-CUR-BMB-2016; SRC-CUR-INF7-2016]
- **Forschungsregel:** Jede Aktivität weist Ziel, fachliche Denkhandlung, Unterstützung, Rückmeldung und Sicherung aus; Medium oder Methode allein sind kein Qualitätsnachweis. [CLAIM-LP-001; CLAIM-DLE-014]
- **Forschungsregel:** Modelle werden konstruiert, auf Fälle angewandt, mit beobachtbarem Verhalten oder Realität verglichen und an ihren Grenzen geprüft. [CLAIM-INF-005; CLAIM-INF-010]
- **Persönliche Arbeitsannahme · `working`:** Lernende sollen fachlich ernst genommen werden und eigene Erklärungen, Modelle, Programme, Analysen, Urteile oder Produkte entwickeln, deren Zweck und Qualitätsmaßstäbe transparent sind.

## 4. Eigenständiger Lernstrang Informatik

**Projektentscheidung:** Der Informatikstrang bleibt auch in integrierten Modulen fachlich identifizierbar. ([Gesamtdesign, Abschnitte 5 und 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

- **Curriculumregel:** In Klasse 7 gehören Daten und Codierung, Algorithmen, Rechner und Netze sowie Informationsgesellschaft und Datensicherheit zusammen mit den prozessbezogenen Kompetenzen zum normativen Informatikkern. [SRC-CUR-INF7-2016]
- **Curriculumregel:** Aufgaben zu Algorithmen und Programmen verlangen je nach Ziel das Erläutern von Grundbausteinen, Entwerfen, Implementieren, schrittweise Untersuchen, Testen und Bewerten; informatische Modelle und Realsituation werden verglichen. [SRC-CUR-INF7-2016]
- **Forschungsregel:** Kontrollstrukturen bilden eine kontextabhängige Lerntrajektorie, keine starre Begriffsliste; die konkrete Folge für 10- bis 13-Jährige ist zu erproben. [CLAIM-INF-001]
- **Forschungsregel:** Tracing, Syntaxarbeit, Musterverständnis, Testen, Debugging und Eigenkonstruktion sind unterscheidbare Praktiken. [CLAIM-INF-003; CLAIM-INF-007]
- **Forschungsregel:** Repräsentationen verbinden Daten oder Code, Ausführung, Zustand und Ausgabe; Lernende bearbeiten sie durch Vorhersage, Ergänzung, Erklärung, Vergleich oder Korrektur. [CLAIM-INF-004; CLAIM-INF-005]
- **Projektentscheidung · No-Gate:** Softwarebedienung ist Mittel für eine informatische Handlung, nicht dauerhafter Fachkern. ([Gesamtdesign, Abschnitt 5.1](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 5. Eigenständiger Lernstrang Medienbildung

**Projektentscheidung:** Der Medienbildungsstrang bleibt auch bei technischer Fundierung als Analyse-, Gestaltungs- und Urteilspraxis identifizierbar. ([Gesamtdesign, Abschnitte 5 und 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

- **Curriculumregel:** In Klasse 5 sind Information und Wissen, Produktion und Präsentation, Kommunikation und Kooperation, Mediengesellschaft sowie Grundlagen digitaler Medienarbeit mit Sach-, Handlungs- und Reflexionskompetenz zu verbinden. [SRC-CUR-BMB-2016]
- **Curriculumregel:** Recherchieren, Quellen auswählen und einschätzen, Medienprodukte planen und gestalten, Rechte und Datenschutz beachten, Kommunikationsregeln anwenden und Medienwirkungen kriteriengeleitet untersuchen sind normative Lernhandlungen. [SRC-CUR-BMB-2016]
- **Forschungsregel:** Medienbildungsaufgaben verlangen aktive Analyse, Belegprüfung, Produktion oder Revision; kleine mittlere Interventionseffekte begründen weder eine feste Sequenz noch die Überlegenheit eines Mediums. [CLAIM-MED-002]
- **Forschungsregel:** Privatsphäre, Empfehlung und Werbung werden über Datenarten, Akteure, Interessen und Gestaltungsmechanismen erschlossen. [CLAIM-MED-001; CLAIM-MED-005; CLAIM-MED-006]
- **Forschungsregel:** Desinformation und KI-Ausgaben werden wiederholt als prüfbare Behauptungen bearbeitet; ein KI- oder Detektorlabel ist kein Endurteil. [CLAIM-MED-003; CLAIM-MED-004]
- **Projektentscheidung · No-Gate:** Warnbotschaften, Risikoaufzählungen und bloße Anwendungsfertigkeiten ersetzen weder Mechanismuserklärung noch begründetes Urteil. ([Gesamtdesign, Abschnitte 5.2 und 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 6. Fachlich begründete Integration beider Stränge

- **Projektentscheidung:** Informatik und Medienbildung dürfen verbunden werden, wenn eine gemeinsame fachliche Frage oder ein gemeinsames System-, Daten- oder Gestaltungsproblem beide Perspektiven benötigt. Nicht jedes Modul muss beide Stränge enthalten. ([Gesamtdesign, Abschnitte 5.4 und 14](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · `working`:** Vor Freigabe benennt ein integriertes Modul getrennt (a) den informatischen Erkenntnisgewinn, (b) den medienbildnerischen Erkenntnisgewinn und (c) die Beziehung, die erst durch ihre Verbindung verständlich wird. ([Gesamtdesign, Abschnitt 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Technische, ökonomische, gestalterische und gesellschaftliche Beziehungen werden nur so weit verbunden, wie sie die konkrete fachliche Frage tragen. [CLAIM-MED-001; CLAIM-MED-005; CLAIM-MED-006]
- **Projektentscheidung · `working`:** Geeignete Verbindungen sind unter anderem Datenfluss und informationelle Selbstbestimmung; Empfehlungsalgorithmus und Plattforminteresse; Codierung und mediale Repräsentation; Netzmodell und Kommunikationsentscheidung; Bildbearbeitung und Wirkungsabsicht; Kryptografie und Sicherheitsurteil. ([Gesamtdesign, Abschnitte 5.2 bis 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · No-Gate:** Ein gemeinsames digitales Werkzeug, ein Lebensweltbezug oder das Wort „Digitalität“ ist noch keine fachliche Integration. ([Gesamtdesign, Abschnitt 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 7. Alters- und jahrgangsbezogene Progression 5–7

**Projektentscheidung · `working`:** Die folgende Progression ist ein Gerüst für Roadmap und Aufgabenprüfung. Sie ist keine abschließende normative Klassenverteilung; diese wird in Task 12 aus dem vollständigen Crosswalk festgelegt. ([Gesamtdesign, Abschnitte 3 und 5](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

| Jahrgang | Vorläufige Leitidee | Zunehmende fachliche Handlung | Status- und Quellenbezug |
| --- | --- | --- | --- |
| 5 | in schulischen und alltäglichen digitalen Umgebungen handlungsfähig, sicher und reflektiert werden | bedienen und benennen → auswählen und beschreiben → erste Kriterien anwenden → einfach produzieren und einschätzen | normative BMB-Basis [SRC-CUR-BMB-2016]; persönliche und projektbezogene Ausgestaltung `working` |
| 6 | Informationen, Datenflüsse, Auswahlmechanismen und Medienwirkungen mit ersten informatischen Modellen durchschauen | vergleichen und erklären → Belege prüfen → Modellgrenzen markieren → Produkt nach Kriterien revidieren | Übergangsgerüst `working`; Lesehilfe nur `orientation` [SRC-CUR-LESEHILFE-2026-27] |
| 7 | Daten, Algorithmen, Netze und Sicherheit systematisch analysieren, implementieren, testen und bewerten und mit Medienfragen begründet verbinden | modellieren und entwerfen → implementieren und tracen → testen und debuggen → bewerten und übertragen | normative Informatikbasis [SRC-CUR-INF7-2016]; zusätzliche Integrationen `working` |

- **Forschungsregel:** Klasse 5 erhält bei Exploration ein eigenes Überforderungsgate; begrenzte Exploration muss in explizite Erklärung und Sicherung münden. [CLAIM-LP-012]
- **Forschungsregel:** Block- und Textdarstellungen besitzen keinen evidenzbasierten festen Alterswechsel; Lernziel, Syntaxlast und Anschlussweg entscheiden. [CLAIM-INF-008]
- **Forschungsregel:** Spätere Module greifen Kernkonzepte mit Abstand und veränderter fachlicher Handlung wieder auf; Wiedersehen allein ist kein aktiver Abruf oder Transfer. [CLAIM-LP-007; CLAIM-LP-008; CLAIM-LP-009]
- **Projektentscheidung:** Ein verbindlicher progressiver Kernlernweg wird durch flexible Ergänzungen erweitert. ([Gesamtdesign, Abschnitt 2.2](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

> Vertiefungs-, Transfer- und Projektmodule können an definierte Voraussetzungen andocken und flexibel eingesetzt werden.

## 8. Material- und Repräsentationsstandards

- **Forschungsregel:** Material wird danach ausgewählt, welche fachliche Denkhandlung es ermöglicht; zusätzliche Such-, Bedien- und Darstellungsbelastung wird begrenzt. [CLAIM-LP-001; CLAIM-LP-003]
- **Forschungsregel:** Zusammengehörige Informationen stehen räumlich oder zeitlich zusammen; wechselnde Darstellungen verwenden konsistente Bezeichner und sichtbare Zuordnungen. [CLAIM-LP-003]
- **Forschungsregel:** Worked Examples sind Aufgabenmaterial: Lernende sagen voraus, ergänzen, erklären, vergleichen, testen oder korrigieren sie. [CLAIM-INF-004; CLAIM-LP-004; CLAIM-LP-005]
- **Forschungsregel:** Informatische Ausführungsdarstellungen zeigen mindestens relevante Eingabe, Ausführungsposition, Zustand und Ausgabe; jede Darstellung nennt ihren Zweck und ihre Modellgrenze. [CLAIM-INF-005]
- **Curriculumregel:** Materialien und Aufträge verwenden die amtlichen Fachbegriffe und passenden Operatoren der jeweiligen geltenden Quelle; Beispiele werden nicht als verbindliche Kompetenzen ausgegeben. [SRC-CUR-BMB-2016; SRC-CUR-INF7-2016]
- **Projektentscheidung:** Lernendenmaterial, Lehrkräftehandbuch, Curriculum-/Quellenmapping und gegebenenfalls begründetes Analogmaterial bilden zusammen das vollständige Modul. ([Gesamtdesign, Abschnitt 6](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 9. Standards für Programmieraufgaben

**Forschungsfolge · `working`:** Jede Programmiersequenz weist aus, welche der folgenden Praktiken tatsächlich gelernt und geprüft wird. Die Praktiken operationalisieren die curricularen Handlungen und die Befunde zu PRIMM, getrennten Programmierpraktiken und Debugging. [CLAIM-INF-002; CLAIM-INF-003; CLAIM-INF-007]

1. **Vorhersagen:** Ausgabe, Zustand oder nächsten Schritt vor der Ausführung begründen.
2. **Ausführen und Tracing:** Code schrittweise mit Eingabe, Zustand und Ausgabe verfolgen.
3. **Erklären:** Wirkung, Kontrollfluss, Datenbeziehung oder Muster fachsprachlich erläutern.
4. **Modifizieren:** eine begründete Veränderung vornehmen und ihre erwartete Wirkung angeben.
5. **Testen:** geeignete Normal-, Grenz- und Gegenfälle entwerfen, durchführen und auswerten.
6. **Debugging:** Fehler bemerken, lokalisieren, eine Hypothese formulieren, gezielt testen, reparieren und die Reparatur begründen.
7. **Eigenkonstruktion:** Problem strukturieren, Modell beziehungsweise Algorithmus entwerfen, implementieren und gegen Kriterien prüfen.

- **Curriculumregel:** Entwerfen, Implementieren, Untersuchen, Testen, Erklären und Bewerten sind im Aufbaukurs eigenständige fachliche Leistungen. [SRC-CUR-INF7-2016]
- **Forschungsregel:** Predict–Run–Investigate–Modify–Make ist ein geeigneter zu erprobender Zyklus, aber kein Beleg dafür, dass jede Phase isoliert wirkt oder immer dieselbe Reihenfolge braucht. [CLAIM-INF-002]
- **Forschungsregel:** Debugging ist Problemlösen mit Hypothese und Test, nicht bloß das Beseitigen einer Fehlermeldung. [CLAIM-INF-007]
- **Forschungsregel:** Block-/Textübergänge nutzen isomorphe Beispiele, Übersetzungsaufgaben oder strukturierte Editoren; sie werden nicht allein an ein Alter gebunden. [CLAIM-INF-008]
- **Forschungsfolge · `working`:** Lauffähiger Code reicht nicht. Mindestens eine Erklärung, ein Trace, begründete Testfälle oder eine dokumentierte Revision müssen Verständnis sichtbar machen. [CLAIM-INF-003; CLAIM-INF-007]

## 10. Standards für Medienanalyse und Medienproduktion

### Medienanalyse

- **Forschungsregel:** Der wiederkehrende Analysezyklus umfasst Mechanismus, Akteur, Interesse, Beleg, Gegenbeleg, Unsicherheit und Revision. [CLAIM-MED-001; CLAIM-MED-003; CLAIM-MED-004; CLAIM-MED-005; CLAIM-MED-006]
- **Curriculumregel:** Quellenqualität, Darstellungsabsicht, Medienwirkung, Kommunikation und rechtliche beziehungsweise moralische Grenzen werden an Kriterien untersucht und eingeschätzt. [SRC-CUR-BMB-2016]
- **Forschungsregel:** Aussagen über Wirkungen unterscheiden Beobachtung, Korrelation, mögliche Erklärung und individuelle Unsicherheit; aus Gruppenbefunden entsteht keine Individualdiagnose. [CLAIM-MED-008; CLAIM-MED-010]
- **Forschungsfolge · `working`:** Ein Analyseprodukt enthält mindestens einen belegten Befund, eine alternative Erklärung oder einen Gegenbeleg und ein revidierbares Unsicherheitsurteil. [CLAIM-MED-003; CLAIM-MED-004; CLAIM-MED-008]

### Medienproduktion

- **Curriculumregel:** Digitale Medienprodukte werden geplant, gestaltet, präsentiert und anhand transparenter Kriterien eingeschätzt; Urheberrecht und Datenschutz sind zu beachten. [SRC-CUR-BMB-2016]
- **Projektentscheidung · `working`:** Jede Aufgabe führt durch Ziel und Adressat, Wirkungsabsicht, begründete Gestaltungsentscheidung, Rechte- und Quellenprüfung, Test beziehungsweise Feedback sowie dokumentierte Überarbeitung. ([Gesamtdesign, Abschnitte 4.5 und 4.6](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Produktion ist eine aktive Medienbildungsleistung, wenn Gestaltungsentscheidungen erklärt und aufgrund von Kriterien oder Feedback revidiert werden. [CLAIM-MED-002; CLAIM-LP-010]
- **Forschungsregel:** Offene Produktion dokumentiert Titel, Urheber, Quelle, Lizenz, Lizenzlink, Änderungen und eigene Anteile. [CLAIM-MED-013; CLAIM-DLE-010; CLAIM-DLE-011]

## 11. Typische Vorstellungen, Fehlvorstellungen und Lernbarrieren

**Forschungsregel:** Vorstellungen werden als prüfbare aktuelle Deutungen behandelt, nicht als feste Eigenschaften von Personen. [CLAIM-LP-002; CLAIM-INF-006] Die folgende Planungsfolge ist eine inferentielle Anwendung mit Status `working`.

| Bereich | Erwartbare Vorstellung oder Barriere | Planungsfolge |
| --- | --- | --- |
| Programmzustand | Zuweisung, Variable, Kontrollfluss oder Aufruf werden statisch statt als Zustandsänderung verstanden. [CLAIM-INF-006] | Vorhersage, Trace, Kontrastfall und Reparatur; kein dauerhaftes Fehlvorstellungslabel |
| Internet und Cloud | Internet wird mit WLAN, Satellit, Sendeturm oder einem zentralen Speicher gleichgesetzt. [CLAIM-INF-010] | eigenes Modell sichtbar machen, Paketweg- und Client-Server-Modell kontrastieren, Modellgrenze sichern |
| Codequalität | „Läuft“ wird mit „verstanden, richtig und robust“ gleichgesetzt. [CLAIM-INF-007] | Testfälle, Gegenbeispiele, Debugginghypothese und Erklärung verlangen |
| Block und Text | Werkzeugform wird mit fachlicher Schwierigkeit oder Altersreife verwechselt. [CLAIM-INF-008] | Syntaxlast und Lernziel getrennt betrachten, Repräsentationen übersetzen |
| Empfehlung und Werbung | Auswahl erscheint zufällig, rein persönlich oder neutral. [CLAIM-MED-005; CLAIM-MED-006] | Daten, Akteur, Auswahlmechanismus, Interesse und Wirkung im Modell verbinden |
| KI und Desinformation | überzeugende Form oder Detektorlabel gilt als Wahrheitsbeleg. [CLAIM-MED-003; CLAIM-MED-004] | Behauptung zerlegen, Primär- und unabhängigen Beleg prüfen, Unsicherheit revidieren |
| sensible Wirkungsfragen | Korrelation wird als individuelle Ursache oder Diagnose gelesen. [CLAIM-MED-008; CLAIM-MED-010] | Studiendesign und alternative Erklärung prüfen; fiktive Fälle statt Personenprofile |

- **Forschungsregel:** Eine einzelne falsche Antwort belegt kein stabiles Fehlkonzept; Vorwissen und Vorstellungen werden lokal, aufgabenbezogen und revidierbar sichtbar gemacht. [CLAIM-LP-002; CLAIM-INF-006]
- **Persönliche Arbeitsannahme · `working`:** Sprachliche, technische und organisatorische Hürden werden als Planungsaufgabe behandelt; Unterstützung erhält den gymnasialen fachlichen Anspruch.

## 12. Scaffolding, Üben, Feedback, Transfer und Sicherung

- **Forschungsregel:** Hilfen benennen die konkrete Hürde und erhalten die zentrale Denkhandlung; Rücknahme folgt sichtbarer fachlicher Bewältigung, nicht Zeit, Klickzahl oder Telemetrie. [CLAIM-LP-006]
- **Forschungsregel:** Beispiele und Hilfen können vom vollständigen Beispiel über Lücken und Modifikation zur Eigenkonstruktion führen; die konkrete Dosierung für 10- bis 13-Jährige bleibt zu pilotieren. [CLAIM-INF-004; CLAIM-LP-004]
- **Forschungsregel:** Wenige fachlich fokussierte Selbsterklärungsprompts dienen Beziehungen, Vorhersagen, Begründungen oder Reparaturen; generische Warum-Fragen sind kein Standard. [CLAIM-LP-005]
- **Forschungsregel:** Aktiver Abruf, verteilte Wiederaufnahme und Transfer werden als getrennte Lernfunktionen geplant. [CLAIM-LP-007; CLAIM-LP-008; CLAIM-LP-009]
- **Forschungsregel:** Feedback liefert nutzbare Information zum Produkt, zur Strategie oder zum nächsten Prüfschritt; Punkte, Lob oder sofortige Lösung ersetzen diese Funktion nicht. [CLAIM-LP-010]
- **Forschungsregel:** Begrenzte Exploration erzeugt Vorläuferwissen und wird durch Vergleich, explizite Erklärung, Übung und gemeinsame Sicherung konsolidiert. [CLAIM-LP-012]
- **Projektentscheidung · `working`:** Jede Sequenz hält fest, welches Modell, welcher Begriff, welches Verfahren oder welches begründete Urteil gilt, welche Grenze oder offene Frage bleibt und wann ein späterer Abruf erfolgt. ([Gesamtdesign, Abschnitt 4.7](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 13. Lehrkraftorchestrierung

- **Projektentscheidung:** Das Lernwerk unterstützt gemeinsamen Einstieg, kurze explizite Erklärung, angeleitete und selbstständige Arbeit, Werkstattphasen, funktionalen Austausch und gemeinsame Sicherung; es ist kein vollständig selbstgesteuerter Onlinekurs. ([Gesamtdesign, Abschnitte 1, 2.3 und 4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Die Lehrkraft orchestriert kognitive Aktivierung, konstruktive Unterstützung und klare Führung; Methode, Sozialform und digitales Medium sind Sichtstruktur, nicht der Lernnachweis. [CLAIM-LP-001]
- **Forschungsregel:** Sie verbindet Explorationsergebnisse mit expliziter Erklärung, insbesondere in Klasse 5, und lässt Fehlwege nicht fachlich ungeklärt stehen. [CLAIM-LP-012]
- **Forschungsregel:** Sie entscheidet anhand sichtbarer Produkte und Gespräche über Hilfen und Fading; ein System inferiert keine Lernstrategie aus Nutzungsdaten. [CLAIM-LP-006; CLAIM-LP-013]
- **Forschungsregel:** Bei sensiblen Themen trennt sie fachliche Fallanalyse von persönlicher Betroffenheit und hält schulische Hilfs- und Eskalationswege bereit. [CLAIM-MED-007; CLAIM-MED-009]
- **Persönliche Arbeitsannahme · `working`:** Ziel, Kriterien, Zeitrahmen und sinnvolle Wahlmöglichkeiten werden transparent; Selbstverantwortung und Peer-Feedback erhalten eine klare Funktion, Verbindlichkeit und Anschlussnutzung.
- **Projektentscheidung · `working`:** Jedes Modulhandbuch nennt erwartbare Vorstellungen, fachlichen Hintergrund, Erklärungspunkte, Hilfen, Gesprächs- und Sicherungspunkte, Sicherheitsgrenzen, Testfälle, Kriterien, Fallbacks und spätere Wiederaufnahme. ([Gesamtdesign, Abschnitt 7.2](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 14. Begründete Analog-/Digitalentscheidung

- **Projektentscheidung:** Digital ist das selbstverständliche Primärmedium; eine analoge parallele Vollfassung wird nicht gepflegt. ([Gesamtdesign, Abschnitt 2.1](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Digital ist fachlich begründet, wenn veränderliche Zustände, tatsächliche Programmausführung, unmittelbare Testfälle, Simulation, Quellenöffnung, Variantenvergleich, Produktion oder Revision die Lernhandlung tragen. [CLAIM-INF-005; CLAIM-LP-003]
- **Forschungsregel:** Analog ist begründet, wenn räumliche Anordnung, freies Skizzieren, haptische Manipulation, Verkörperung, gemeinsame Modellierung oder bildschirmfreie Diskussion die fachliche Beziehung klarer oder störungsärmer macht. [CLAIM-LP-003; CLAIM-INF-009]
- **Forschungsregel:** Unplugged-Material nennt fachliche Zuordnung, Modell- oder Analogiegrenze und eine formale oder digitale Anschlussaufgabe; sein Einsatz belegt keinen pauschalen Transfer. [CLAIM-INF-009]
- **Projektentscheidung · `working`:** Die Medienabnahme fragt: Welche Denkhandlung trägt das Medium? Welche Bedien-, Such- oder Darstellungsbelastung erzeugt es? Welche Modellgrenze ist sichtbar? Welches überprüfbare Produkt oder welche Revision folgt? ([Gesamtdesign, Abschnitte 2.1 und 13.1](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · No-Gate:** Kein Printmaterial ohne eigenständige Lernfunktion und dokumentierte Rückbindung; keine funktionslose Digitalisierung eines analogen Blatts. ([Gesamtdesign, Abschnitte 2.1 und 10.2](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 15. Nicht personenbezogene Diagnosegelegenheiten

**Forschungsregel:** Diagnose bedeutet hier eine aktuelle, aufgabenbezogene Gelegenheit für Anschlussreaktion und Feedback, keine Erhebung eines stabilen Personenmerkmals. [CLAIM-LP-002; CLAIM-LP-010]

- **Projektentscheidung:** Es gibt keine Konten, Namen, zentralen Kompetenzstände, Lernanalyse, automatisierte Bewertung, Tracker oder personenbezogene Telemetrie. ([Gesamtdesign, Abschnitte 2.4 und 11](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Geeignet sind Vorhersage, Trace, Modellskizze, Kontrastfall, Reparatur, Quellencheck, Testfall, Kriterienanwendung und begründete Revision. [CLAIM-INF-005; CLAIM-INF-006; CLAIM-INF-007; CLAIM-INF-010; CLAIM-MED-003; CLAIM-LP-010]
- **Forschungsregel:** Einzelantworten werden nicht zu Fehlvorstellungs-, Selbstregulations-, psychischen oder spielbezogenen Profilen verdichtet. [CLAIM-LP-002; CLAIM-LP-013; CLAIM-MED-008; CLAIM-MED-010]
- **Forschungsregel:** Kontenfreiheit oder lokale Speicherung belegt noch keine Datenschutzkonformität; Datenfluss, Freitext, Export, Löschung und Speicherfehler bleiben zu prüfen. [CLAIM-DLE-004; CLAIM-DLE-005; CLAIM-DLE-006]
- **Persönliche Arbeitsannahme · `working`:** Das Handbuch nennt, wie die Lehrkraft bei ausgefallenem Selbstcheck, fehlendem Produkt oder unklarem Lernstand kurz nachsichert, bevor der Lernweg auf dem Ergebnis aufbaut.

## 16. Quellen, Lizenz, Aktualität und Accessibility

- **Projektentscheidung:** Eigene Lerninhalte stehen unter CC BY-SA 4.0, eigener Code unter MIT; Drittmaterial wird einzeln ausgewiesen und darf offene Nachnutzung des Kerns nicht blockieren. ([Gesamtdesign, Abschnitt 2.5](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** OER umfasst kostenlosen Zugang, Wiederverwendung, Bearbeitung und Weitergabe in bearbeitbaren Quellen; öffentlicher Lesezugriff allein genügt nicht. [CLAIM-DLE-009]
- **Forschungsregel:** Jedes Asset dokumentiert Titel, Urheber, Fundstelle, Lizenzversion und -link, Änderungen, Drittmaterial und eine versions- und richtungsspezifische Kompatibilitätsentscheidung. [CLAIM-MED-013; CLAIM-DLE-010; CLAIM-DLE-011]
- **Forschungsregel:** WCAG 2.2 AA ist das vollständige technische Baseline-Gate; Tastatur-, Touch- und Assistive-Technology-Pfade sowie reale Nutzeraufgaben prüfen zusätzlich gleichwertige Bedienbarkeit, nicht Lernwirksamkeit. [CLAIM-DLE-001; CLAIM-DLE-002; CLAIM-DLE-003]
- **Forschungsregel:** Installation, Offlinekorrektheit, Cache, Lernstandsmigration, Wiederanbindung und reale schulische Browser-/MDM-Konfigurationen werden getrennt und datiert geprüft. [CLAIM-DLE-007; CLAIM-DLE-008; CLAIM-DLE-012; CLAIM-DLE-013]
- **Projektentscheidung · `working`:** Quellen- und Rechtsstand, Plattform- und KI-Beispiele, Accessibility-Standards, Browser-/MDM-Ziele und Lizenzkompatibilität erhalten Datum, Version und Recheck-Trigger. ([Gesamtdesign, Abschnitte 7.1 und 13](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Curriculumregel:** Amtliche Inhalte ohne ausgewiesene offene Lizenz werden nicht stillschweigend als OER vervielfältigt; ihre Kompetenzanker werden über registrierte Quellen-IDs und quellentreue Datensätze nachgewiesen. [SRC-CUR-BMB-2016; SRC-CUR-INF7-2016]

## 17. Reduzierbares Beurteilungsinstrumentarium

**Projektentscheidung · `working`:** Der gesamte Abschnitt ist ein modularer, reduzierbarer Arbeitsbestand und darf weder Kernlernziele noch Modulgrammatik dominieren. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

- **Projektentscheidung:** Das Lernwerk vergibt keine Noten, Punkte oder Kompetenzprofile; die pädagogische Bewertung bleibt bei der Lehrkraft. Instrumente dürfen später entfernt werden, ohne Kernmodule umzubauen. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Forschungsregel:** Beurteilbar sind aktuelle Produkte, Erklärungen, Testfälle, Strategien und dokumentierte Revisionen, nicht aus Telemetrie inferierte Personenmerkmale. [CLAIM-INF-006; CLAIM-LP-010; CLAIM-LP-013; CLAIM-MED-007]
- **Projektentscheidung · `working`:** Der Arbeitsbestand kann kommentierte Programme mit Vorhersage und Tests, Traces oder Modelle mit Modellgrenze, Debuggingprotokolle, Evidenzdossiers, Mechanismuskarten, revidierte Medienprodukte, Kriterienraster, mündliche Erklärungen und praktische Transferaufgaben enthalten. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · `working`:** Lern- und Leistungssituation, Hilfen, erlaubte Werkzeuge, Kriterien, Belegpflicht und Exportentscheidung werden sichtbar unterschieden. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- **Projektentscheidung · `working`:** Ein Instrument bleibt nur, wenn es eine fachlich relevante Leistung valide sichtbar macht, mit vertretbarem Aufwand nutzbar ist und keine personenbezogene Infrastruktur voraussetzt. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 18. No-Gos

### Curriculumregel

- Keine curriculare Norm aus `SRC-CUR-LESEHILFE-2026-27`, `SRC-CUR-KM-FACHSEITE` oder `SRC-CUR-KM-FAQ-REFORM` ableiten.

### Forschungsregeln

- Softwarebedienung, Geräteverfügbarkeit, Interaktivität oder ein Methodenlabel nicht als Lernqualität ausgeben. [CLAIM-LP-001; CLAIM-DLE-014]
- Programmieraufgaben nicht auf „Code läuft“ oder reine Eigenkonstruktion ohne Lesen, Erklären, Testen und Debugging reduzieren. [CLAIM-INF-003; CLAIM-INF-007]
- Medienanalyse nicht auf Warnung, Meinung, Checkliste oder Detektor-Endurteil verkürzen. [CLAIM-MED-002; CLAIM-MED-003; CLAIM-MED-004]
- Keine persönliche Offenlegung, Peerdiagnostik, Rankings, Risiko- oder Kompetenzprofile und zentrale sensible Fallspeicherung verlangen. [CLAIM-MED-007; CLAIM-MED-008; CLAIM-MED-010]
- Kein offenes Entdecken ohne erreichbares Zielwissen, Unterstützung, explizite Konsolidierung und Sicherung einsetzen. [CLAIM-LP-012]

### Projektentscheidungen

- Informatik und Medienbildung nicht zu unscharfer „Digitalkompetenz“ vermischen. ([Gesamtdesign, Abschnitte 5 und 5.4](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- Medienprodukte nicht ohne Zielgruppe, Gestaltungsbegründung, Rechte-/Quellenprüfung, Test und Revision abnehmen. ([Gesamtdesign, Abschnitte 4.5, 4.6 und 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- Analoge und digitale Vollstrukturen nicht parallel pflegen und kein Medium ohne eigene Lernfunktion wählen. ([Gesamtdesign, Abschnitt 2.1](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- Amtliche, fremde oder KI-generierte Inhalte nicht ohne Provenienz-, Lizenz-, Änderungs- und Aktualitätsprüfung veröffentlichen. ([Gesamtdesign, Abschnitte 2.5 und 13](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- Das `working`-Beurteilungsinstrumentarium nicht zur Voraussetzung jedes Moduls machen. ([Gesamtdesign, Abschnitt 8](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))
- Vor Abschluss von Curriculum-Crosswalk, Fachreview und Pilotierung keine Klassenverteilung oder Profilregel als `standard` ausgeben. ([Gesamtdesign, Abschnitte 3, 9.5 und 13.3](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

## 19. Offene Fragen, Recheck-Trigger und Reviewstatus

### Offene Fragen

- Welche jahrgangsgenaue Verteilung folgt aus dem vollständigen Crosswalk von BMB 2016, INF7 2016 und der Lesehilfe als Orientierung?
- Welche PRIMM-, notional-machine-, Worked-Example- und Block-/Text-Ausgestaltung trägt für 10- bis 13-Jährige in realen Klassen? [CLAIM-INF-002; CLAIM-INF-004; CLAIM-INF-005; CLAIM-INF-008]
- Wann ist in Klasse 5 vorbereitete Exploration erreichbar, und wann ist frühe explizite Erklärung günstiger? [CLAIM-LP-012]
- Welche wiederholten Prüfaufgaben unterstützen die Beurteilung von Desinformation und KI-Ausgaben in dieser Altersgruppe? [CLAIM-MED-003; CLAIM-MED-004]
- Welche Bestandteile des Beurteilungsinstrumentariums werden nach Fachreview und Erprobung gestrichen?

### Recheck-Trigger

**Projektentscheidung · `working`:** Ein Recheck wird ausgelöst durch:

- Veröffentlichung, Änderung oder Inkraftsetzung eines amtlichen Fachplans;
- Abschluss des Curriculum-Crosswalks und der Modulroadmap;
- fachliches, didaktisches oder technisches Review eines Goldstandard-Piloten;
- widersprüchliche Unterrichtsbefunde oder wiederholt beobachtete Barrieren;
- neue systematische Evidenz für die Zielaltersgruppe;
- Rechts-, Lizenz-, WCAG-, Browser-, MDM-, Plattform- oder KI-Änderung.

Die Recheck-Logik konkretisiert Qualitätssicherung, Review und Erprobung. ([Gesamtdesign, Abschnitt 13](../superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md))

### Reviewstatus

- Profil: `working`;
- persönliche Arbeitsannahmen: `working`;
- Forschung: Claim-basiert; ihre konkrete Profilanwendung bleibt, sofern nicht anders ausgewiesen, `working`;
- Designprinzipien: zwölf `working`, drei `reviewed`, kein `draft`, kein `standard`;
- curriculare Basis: BMB 2016 und INF7 2016 `enacted`, Lesehilfe 2026/2027 `orientation`;
- nächster Reifeschritt: Task-12-Crosswalk, getrenntes Fach-/Didaktikreview und spätere Pilotierung; keine automatische Statusanhebung durch dieses Profil.
