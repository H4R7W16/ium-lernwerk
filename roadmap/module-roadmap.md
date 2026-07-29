# IuM-Lernwerk - erste Modulroadmap für Gymnasium 5-7

Status: `working`
Stand: 29. Juli 2026
Geltungsbereich: Baden-Württemberg, Gymnasium, Niveau E

Diese Roadmap ordnet die 31 geprüften Modulkandidaten zu einem reviewfähigen Lernwerk-Kosmos. Sie ist weder Stundentafel noch fertiges Schulcurriculum. Insbesondere trennt sie drei Aussagen:

1. **Semantischer Coverage-Audit:** Alle 171 Curriculumrecords sind einem Kernkandidaten zugeordnet und einzeln gegen Operator, Gegenstand, zentrale Lernhandlung und Produktnachweis geprüft. 111 Records besitzen einen expliziten Match; bei 60 Records ist die noch zu schließende Lücke dokumentiert.
2. **Abhängigkeit:** Der Kandidatengraph ist fachlich progressiv, azyklisch und jahrgangskonsistent.
3. **Zeitliche Umsetzbarkeit:** Eine vollständige Kandidatenfolge muss zusätzlich in die reale Unterrichtszeit passen. Dieser Nachweis ist für die Klassen 6 und 7 noch nicht erbracht.

## Planungsannahmen und Zeitmodell

- Die Lesehilfe 2026/2027 ist eine Orientierung und kein in Kraft gesetzter Bildungsplan. Sie erlaubt auf Seite 3 ausdrücklich eine Gewichtung nach Lerngruppe, schulischen Gegebenheiten und verfügbarer Unterrichtszeit.
- Der Basiskurs Medienbildung und der Aufbaukurs Informatik bleiben im Übergang `enacted`. Ähnliche Records werden deshalb nicht stillschweigend zusammengezogen.
- Die [amtliche FAQ zur Bildungsreform](https://km-baden-wuerttemberg.de/de/schule/schulartuebergreifend/faq-bildungsreform) weist für Informatik und Medienbildung am Gymnasium eine Wochenstunde je Jahrgang aus. Abgerufen am 29. Juli 2026.
- Für die erste Belastungsprobe werden 36 nominelle Unterrichtseinheiten pro Schuljahr angesetzt. Das ist eine Projektannahme, keine amtliche Zahl.
- Der realistische Referenzkorridor reserviert **30 Unterrichtseinheiten Kern** und **6 Unterrichtseinheiten Puffer** für Ausfall, Einstieg, Diagnosegelegenheiten, Sicherung und notwendige Wiederaufnahme.
- Flexible Module werden nicht in den 30-Stunden-Kern hineingerechnet. Sie benötigen zusätzliche Zeit, eine begründete schulische Schwerpunktsetzung oder später eine geprüfte Austauschlogik ohne Verlust verbindlicher Abdeckung.
- Hausaufgaben, Vertretungsstunden und fachfremde Projektzeit werden nicht als garantierte Unterrichtszeit eingerechnet.

## Kernfolge Klasse 5

Die Reihenfolge beginnt mit sicherer Arbeitsfähigkeit. Danach können Recherche, Kommunikation, erster Systemblick und Algorithmen teilweise parallelisiert werden. Medienproduktion baut auf Arbeitsfähigkeit und Recherche auf; Medienreflexion folgt auf die Quellenarbeit.

| Pos. | Modul | Zentrale Funktion | Voraussetzung | Kandidatenkorridor |
|---:|---|---|---|---:|
| 1 | `IUM-5-CORE-01` - Im Schulnetz sicher arbeitsfähig werden | Geräte-, Datei-, Zugangs- und Arbeitsroutinen | - | 5-7 |
| 2 | `IUM-5-CORE-02` - Eine Suchfrage mit Belegen beantworten | Recherche, Auswahl, Beleg und Revision | `IUM-5-CORE-01` | 5-7 |
| 3 | `IUM-5-CORE-03` - Digital verständlich, sicher und fair kommunizieren | Kommunikationsregeln und Schutzhandlungen | `IUM-5-CORE-01` | 4-6 |
| 4 | `IUM-5-CORE-04` - Einen schulischen Datenweg sichtbar machen | stark gestützte Systemeinführung | `IUM-5-CORE-01` | 3-4 |
| 5 | `IUM-5-CORE-05` - Präzise Abläufe ausführbar machen | erste Algorithmen, Laufprotokoll und Schleifenidee | `IUM-5-CORE-01` | 5-7 |
| 6 | `IUM-5-CORE-06` - Ein Medienprodukt zielgerichtet gestalten | Produkt, Quelle, Zweck und Revision | `IUM-5-CORE-01`, `IUM-5-CORE-02` | 5-7 |
| 7 | `IUM-5-CORE-07` - Mediennutzung und Werbung an Fällen untersuchen | Wirkung, Werbung und private Selbstreflexion | `IUM-5-CORE-02` | 4-6 |

Planungsurteil: Die Summe von **31-44** Einheiten liegt am unteren Rand nahe am Referenzkorridor. Ein vollständiger Durchlauf ist nur mit belastbaren Kurzfassungen aller sieben Module möglich; die fünf verbleibenden Einheiten bis 36 bilden dann einen knappen, aber sichtbaren Puffer. Klasse 5 ist deshalb `amber`, nicht uneingeschränkt freigegeben.

## Kernfolge Klasse 6

Klasse 6 hebt die in Klasse 5 aufgebauten Praktiken auf Mechanismen, Modelle und begründete Entscheidungen. Recherche und Akteursanalyse stehen früh, weil Datenfluss, Konfliktfälle und Medienproduktion darauf aufbauen.

| Pos. | Modul | Zentrale Funktion | Voraussetzung | Kandidatenkorridor |
|---:|---|---|---|---:|
| 1 | `IUM-6-CORE-01` - Suchmaschinen, Akteure und KI-Ergebnisse prüfen | Suche, Akteure, Motive, KI und Evidenz | `IUM-5-CORE-02` | 6-8 |
| 2 | `IUM-6-CORE-02` - Datenfluss und personalisierte Auswahl modellieren | Datenerhebung, Auswahlmechanismus und Selbstbestimmung | `IUM-5-CORE-07`, `IUM-6-CORE-01` | 5-7 |
| 3 | `IUM-6-CORE-03` - Codierungen entwerfen und auf Umkehrbarkeit prüfen | Codieren, Decodieren und Darstellungswechsel | `IUM-5-CORE-05` | 4-6 |
| 4 | `IUM-6-CORE-04` - Programme mit festen Schleifen lesen und verändern | Tracing, feste Schleife, Änderung und Test | `IUM-5-CORE-05` | 5-7 |
| 5 | `IUM-6-CORE-05` - Netz- und Speicherentscheidungen mit Modellen begründen | Netz, Client-Server und Speichervergleich | `IUM-5-CORE-04` | 4-6 |
| 6 | `IUM-6-CORE-06` - Konflikte in sozialen Räumen fallbezogen bearbeiten | Selbstdarstellung, Pro/Contra, Recht und Hilfswege | `IUM-5-CORE-03`, `IUM-5-CORE-07` | 5-7 |
| 7 | `IUM-6-CORE-07` - Wirkungsabsicht, Rechte und Revision verbinden | Medienprodukt, Lizenz, Feedback und Revision | `IUM-5-CORE-06`, `IUM-6-CORE-01` | 6-9 |

Planungsurteil: Die Summe von **35-50** Einheiten lässt am Minimum nur eine von 36 Einheiten als Puffer. Das unterschreitet die Referenzannahme um fünf Kernstunden und ist für einen robusten Jahresplan nicht ausreichend. Klasse 6 ist **zeitlich nicht freigegeben**, bis Integration, Kürzung oder zusätzliche Zeit fachlich geprüft sind.

## Kernfolge Klasse 7

Die Folge verbindet drei Pfade: Daten/Codierung, Programmieren sowie Netze/Sicherheit. Der gesellschaftlich-mediale Pfad baut auf der Recherche- und Datenflussarbeit aus Klasse 6 auf. Innerhalb eines Pfades ist die Reihenfolge verbindlich; Pfade können im Schuljahr verzahnt werden.

| Pos. | Modul | Zentrale Funktion | Voraussetzung | Kandidatenkorridor |
|---:|---|---|---|---:|
| 1 | `IUM-7-CORE-01` - Codierungen zwischen Zeichen, Zahlen und Bits entwerfen | Zeichen, Zahl, Bit und eigene Codierung | `IUM-6-CORE-03` | 6-9 |
| 2 | `IUM-7-CORE-02` - Bilder als Daten modellieren und Ressourcenfolgen prüfen | Pixel, Datenmenge und Ressourcenbezug | `IUM-7-CORE-01` | 5-7 |
| 3 | `IUM-7-CORE-03` - Kontrollfluss, Werte und Zustände tracen | Verzweigung, Schleife, Ausdruck, Wert und Typ | `IUM-6-CORE-04` | 6-8 |
| 4 | `IUM-7-CORE-04` - Programme entwerfen, testen und debuggen | Implementation, Test, Fehlerhypothese und Revision | `IUM-7-CORE-03` | 7-10 |
| 5 | `IUM-7-CORE-05` - Netze, Speicher und Geräteschutz modellieren | Datenweg, Speicher, Gerät und Schutzbedarf | `IUM-6-CORE-05` | 5-7 |
| 6 | `IUM-7-CORE-06` - Verschlüsselung erklären und passend auswählen | Codierung versus Verschlüsselung, Modell und Auswahl | `IUM-7-CORE-01`, `IUM-7-CORE-05` | 4-6 |
| 7 | `IUM-7-CORE-07` - Einfache Verschlüsselung angreifen und bewerten | Caesar/Substitution, Angriff und Sicherheitsurteil | `IUM-7-CORE-06` | 5-7 |
| 8 | `IUM-7-CORE-08` - Daten, Akteure und Desinformation beurteilen | Behauptung, Beleg, Interesse, Einfluss und Revision | `IUM-6-CORE-01`, `IUM-6-CORE-02` | 6-9 |
| 9 | `IUM-7-CORE-09` - Gamingmechanismen ohne Personendiagnose analysieren | Spielgestaltung, soziale Lage, Monetarisierung und private Reflexion | `IUM-6-CORE-02`, `IUM-7-CORE-08` | 4-6 |
| 10 | `IUM-7-CORE-10` - Medienbilder analysieren und wirkungsbewusst verändern | Manipulation, Rollenbild, Wirkung, Rechte und Gegenprodukt | `IUM-6-CORE-07`, `IUM-7-CORE-08` | 6-9 |

Planungsurteil: Die Summe von **54-78** Einheiten überschreitet bereits am Minimum das nominelle Ein-Stunden-Jahr um 18 und den 30-Stunden-Kernkorridor um 24 Einheiten. Eine vollständige Durchführung mit fachlicher Tiefe ist unter der Referenzannahme unmöglich. Klasse 7 ist **zeitlich nicht freigegeben**. Die Lücke darf nicht durch bloße Umbenennung von Modulen oder durch unbelegte Selbstlernzeit geschlossen werden.

## Flexible Kandidaten

Flexible Kandidaten bleiben Teil des freigegebenen Hybridmodells, werden aber nicht pro Jahrgang erzwungen. In Klasse 5 gibt es derzeit bewusst keinen flexiblen Kandidaten, weil schon der Kernkorridor knapp ist.

| Modul | Art | Andockpunkt | Nutzen | Zusätzlicher Korridor |
|---|---|---|---|---:|
| `IUM-6-EXT-01` - KI-Antworten im Quellenlabor vertiefen | extension | `IUM-6-CORE-01` | Gegenbelege und Unsicherheit vertiefen | 3-4 |
| `IUM-6-EXT-02` - Paketpost im Klassennetz vertiefen | extension | `IUM-6-CORE-05` | Störfälle und alternative Wege modellieren | 2-3 |
| `IUM-6-TRANSFER-01` - Einen Speicherort für ein Schulprojekt entscheiden | transfer | `IUM-5-CORE-01`, `IUM-6-CORE-05` | Systemmodell auf eine reale Schulentscheidung übertragen | 2-4 |
| `IUM-6-PROJECT-01` - Eine offene Informationskampagne gestalten | project | `IUM-6-CORE-01`, `IUM-6-CORE-07` | Recherche, Rechte, Wirkung und Revision integrieren | 8-12 |
| `IUM-7-EXT-01` - Codewortgrenzen formal untersuchen | extension | `IUM-7-CORE-01` | Präfixfreiheit und formale Codierung vertiefen | 3-5 |
| `IUM-7-TRANSFER-01` - Einen sicheren Kommunikationsweg begründen | transfer | `IUM-6-CORE-06`, `IUM-7-CORE-05`, `IUM-7-CORE-06` | Technik, Schutzbedarf und soziale Lage verbinden | 3-5 |
| `IUM-7-PROJECT-01` - Täuschung sichtbar machen und verantwortbar redesignen | project | `IUM-7-CORE-08`, `IUM-7-CORE-10` | Desinformation, Gestaltung, Rechte und Wirkung integrieren | 8-12 |

Ein flexibles Modul darf nur eingesetzt werden, wenn seine Voraussetzungen tatsächlich bearbeitet wurden. Es ist kein Ersatz für einen fehlenden Kernbaustein, solange keine recordgenaue Austauschprüfung vorliegt.

## Begründung der Abhängigkeiten

| Progressionskette | Begründung |
|---|---|
| Arbeitsfähigkeit -> Recherche -> Medienproduktion | Quellen, Dateien und Export müssen beherrscht werden, bevor ein Produkt nachvollziehbar belegt und revidiert werden kann. |
| präziser Ablauf -> feste Schleife -> Kontrollfluss -> Implementation | Ausführen und Darstellen gehen dem Tracing voraus; Tracing und Zustandsmodell gehen eigenständigem Implementieren, Testen und Debuggen voraus. |
| schulischer Datenweg -> Netz/Client-Server/Speicher -> Schutzmodell -> Verschlüsselung/Angriff | Klasse 5 benennt Rollen stark gestützt, Klasse 6 erklärt Systembeziehungen, Klasse 7 verbindet Datenweg und Schutzbedarf mit Verfahren und Sicherheitsurteil. |
| Mediennutzung/Werbung -> Datenfluss/Personalisierung -> Akteure/Desinformation/Gaming | Beobachtung und private Reflexion werden erst danach zu Mechanismus-, Interessen- und Evidenzanalysen vertieft. |
| einfaches Medienprodukt -> Wirkungsabsicht/Rechte/Revision -> Manipulation/Gegenprodukt | Technische Produktion wird schrittweise um Zielgruppe, Lizenz, Feedback, Wirkungsveränderung und ethische Begründung erweitert. |

Jahrgangsrücksprünge sind im Validator verboten. Kernmodule dürfen nicht von flexiblen Modulen abhängen; flexible Kandidaten dürfen ausschließlich an Kernmodule andocken.

## Curriculare Abdeckung

`coverage-plan.json` enthält 171 Einträge:

| Quellengewicht | Records | Status im Coverage-Plan |
|---|---:|---|
| `enacted` - Basiskurs Medienbildung und Aufbaukurs Informatik | 76 | 45 `covered`, 31 `partial` |
| `orientation` - Lesehilfe 2026/2027 | 95 | 66 `covered`, 29 `partial` |
| Gesamt | 171 | 111 `covered`, 60 `partial`, 0 `deferred` |

`covered` bedeutet hier ausschließlich, dass Operator und Gegenstand in einer zentralen Lernhandlung ausgeführt und in einem passenden Lernprodukt sichtbar werden. `partial` bedeutet nicht „unzugeordnet“: Der Record besitzt einen Kern-Andockpunkt, aber der explizite Operator-Produkt-Nachweis ist noch unvollständig. Für jeden dieser 60 Records nennt `coverage-plan.json` eine konkrete Begründung, das Risiko einer Überbehauptung und eine Nacharbeit.

Jeder Eintrag enthält den exakten Anforderungstext, einen ausgewählten Evidenz-Kernkandidaten und ein recordgenaues `matchRationale` mit dessen unveränderter Lernhandlung und Produktbeschreibung. Der Validator erzwingt diese Nachweiskette und verhindert fachfremde oder veraltete Verweise. Er entscheidet jedoch keine natürlichsprachliche Fachsemantik; die Einstufung `covered` oder `partial` bleibt Ergebnis des dokumentierten manuellen Fachaudits.

Der Status ist **keine** Aussage, dass die 171 Records im Ein-Wochenstunden-Jahr mit der erforderlichen Tiefe unterrichtet werden können. Die semantische und die zeitliche Lücke bleiben getrennt sichtbar; eine formal grüne ID-Menge darf keine von beiden verdecken.

Quellenüberlappungen bleiben über `curriculum/crosswalk.json` nachvollziehbar. Ein Record wird nicht gelöscht, nur weil ein anderer Record einen ähnlichen Handlungskern besitzt.

## Jahreskorridore und Puffer

| Klasse | Kernkandidaten | Kandidatensumme | Referenz: Kern + Puffer | Abweichung zum 30er-Kern | Urteil |
|---:|---:|---:|---:|---:|---|
| 5 | 7 | 31-44 | 30 + 6 | mindestens +1 | `amber`: nur am unteren Rand annähernd belastbar |
| 6 | 7 | 35-50 | 30 + 6 | mindestens +5 | `red`: zeitlich nicht freigegeben |
| 7 | 10 | 54-78 | 30 + 6 | mindestens +24 | `red`: zeitlich nicht freigegeben |

Vor einer Phase-1-Modulspezifikation sind vier Arbeiten nötig:

1. Modulübergänge auf gemeinsame Aktivierung, Übung und Sicherung prüfen, damit Wiederaufnahme nicht zu doppeltem Stundenbedarf führt.
2. Für Klasse 6 besonders `IUM-6-CORE-01`/`02` und `IUM-6-CORE-06`/`07` auf fachlich tragfähige Integration prüfen.
3. Für Klasse 7 die Pfade Daten/Codierung, Programmieren, Sicherheit und Medienreflexion gegen 30 Kernstunden neu schneiden. Kein Pfad darf allein durch Überschriftenkürzung als abgedeckt gelten.
4. In einem Goldstandard-Pilot reale Lernzeit, Unterbrechungen, Unterstützungsbedarf und Sicherungszeit anonym auf Modulebene protokollieren.

Mögliche schulische Zusatzstunden oder fächerverbindende Projekte sind Chancen, aber keine Basisannahme. Eine Roadmapvariante mit zusätzlicher Zeit darf erst nach lokaler Entscheidung ausgewiesen werden.

## Analoge Materialien

| Modul | Analoges Element | Eigenständiger didaktischer Mehrwert | Digitale Rückbindung |
|---|---|---|---|
| `IUM-5-CORE-04` | Rollen- und Datenwegkarten | trennt Gerät, Anmeldung, lokales Netz und Ablage körperlich sichtbar; entlastet die erste Begriffsbildung | Folge in der digitalen Schulumgebung rekonstruieren und als unvollständiges Modell markieren |
| `IUM-6-EXT-02` | Störfallkarten für das Paketnetz | zwingt zu lokalen Weiterleitungsentscheidungen, ohne den Lösungsweg vorzugeben | Störfall digital reproduzieren und alternative Pfade vergleichen |
| `IUM-7-CORE-07` | Caesar-Scheibe beziehungsweise manuelles Angriffsprotokoll | macht Schlüsselraum, Regelmäßigkeit und Angriffshandlung ohne Blackbox greifbar | Angriff anschließend in der digitalen Kryptografieumgebung wiederholen und skalieren |

Es gibt keine analoge Doppelstruktur zu jedem Modul. Ausdrucke entstehen nur, wenn Materialität, Verteilung, Körperhandlung oder gemeinsame Sichtbarkeit einen eigenen Lernbeitrag leisten.

## Erhöhter Prüfbedarf

| Module | Prüfbedarf | Release-Regel |
|---|---|---|
| `IUM-5-CORE-03`, `IUM-6-CORE-06` | verletzende Kommunikation, Hilfs- und Meldewege | nur fiktive Fälle; keine Offenlegungspflicht; aktuelle schulische Hilfswege prüfen |
| `IUM-5-CORE-07`, `IUM-7-CORE-09` | eigene Medien- beziehungsweise Spielnutzung | private Reflexion wird nicht erhoben, gespeichert oder bewertet |
| `IUM-6-CORE-01`, `IUM-7-CORE-08` | KI-Ergebnisse, Suche, Desinformation und aktuelle Beispiele | Quellen und Beispiele vor jedem Release auf Aktualität, Herkunft und Gegenbelege prüfen |
| `IUM-6-CORE-02`, `IUM-7-CORE-05` | Datenerhebung, Personalisierung, Geräte- und Zugriffsschutz | keine realen Konten oder Nutzungsprofile; Bedrohungsmodelle altersangemessen begrenzen |
| `IUM-6-CORE-07`, `IUM-7-CORE-10`, `IUM-6-PROJECT-01`, `IUM-7-PROJECT-01` | Urheberrecht, Lizenzen, Persönlichkeitsrechte und manipulative Medien | Rechts- und Lizenzhinweise mit Standdatum; nur geklärte Assets; keine täuschende Veröffentlichung |
| `IUM-7-CORE-06`, `IUM-7-CORE-07`, `IUM-7-TRANSFER-01` | Sicherheitsbegriffe und Kryptografie | Modellgrenzen ausdrücklich machen; keine Scheinsicherheit oder operative Angriffsanleitung gegen reale Systeme |

## Empfehlung für den ersten Goldstandard-Pilot

Empfohlen wird `IUM-5-CORE-05` - **Präzise Abläufe ausführbar machen**.

Auswahlkriterien:

- hohe Progressionswirkung: Voraussetzung für Programmieren in Klasse 6 und 7;
- genuine digitale Funktion: Schritt, Position, Zustand und Wiederholung können ausführbar gekoppelt werden;
- sichtbares Lernprodukt: Algorithmus, Vorhersage, Laufprotokoll, Reparatur und Schleifenbegründung;
- niedriger Datenschutz-, Rechte- und Aktualitätsdruck;
- mehrere Repräsentationen und gestuftes Ausblenden sind ohne künstliche Medienverdopplung möglich;
- der Kandidatenkorridor von 5-7 Einheiten ist klein genug, um den 30-Stunden-Kern real zu testen;
- Fehlvorstellungen und Unterstützungsbedarf lassen sich an anonymisierten Aufgabenereignissen beziehungsweise Lehrkraftbeobachtungen untersuchen, ohne Personenprofil.

Der Pilot soll die Modulgrammatik, Accessibility, Offlinefähigkeit, lokale Speicherung, Exportierbarkeit und reale Lernzeit prüfen. Diese Empfehlung ist ausdrücklich **keine Phase-2-Implementierungsplanung** und legt weder Plattformarchitektur noch Produktionsmeilensteine fest.

## Offene Entscheidungen und Risiken

1. **Zeitmodell:** Klasse 6 und besonders Klasse 7 passen noch nicht in den Referenzkorridor. Vor einer Implementierungsfreigabe ist ein neuer, recordgenau geprüfter Zuschnitt nötig.
2. **Quellenstand:** Die Lesehilfe ist `orientation`; der angekündigte Fachplan kann Wortlaut, Schwerpunkt und Verteilung verändern. Ein Source-Refresh-Gate bleibt verpflichtend.
3. **Gleichzeitige Geltung:** Für das Übergangsjahr werden Lesehilfe und bestehende Bildungspläne getrennt abgedeckt. Ob und wann einzelne alte Anforderungen entfallen, darf nur amtlich entschieden werden.
4. **Klassen 5/6:** Die konkrete Aufteilung des gemeinsamen Lesehilfebands bleibt eine didaktische Arbeitsentscheidung.
5. **Flexible Module:** Im Ein-Wochenstunden-Modell ist derzeit kein verlässlicher Zusatzkorridor vorhanden. Austausch- oder Integrationsvarianten brauchen einen eigenen Coverage-Nachweis.
6. **Beurteilungsinstrumentarium:** `assessmentWorkingNotes` bleibt reduzierbar. Private Reflexion, automatische Punkte und personenbezogene Kompetenzprofile sind ausgeschlossen.
7. **Goldstandard-Pilot:** `IUM-5-CORE-05` ist eine begründete Empfehlung, aber noch keine Nutzerfreigabe zur Implementierung.
8. **Semantische Lücken:** 60 Records sind curricular verortet, aber noch nicht vollständig durch Lernhandlung und Produkt eingelöst. Sie müssen vor einer Vollabdeckungsbehauptung einzeln geschlossen oder begründet `partial` bleiben.
9. **Vollständigkeitsbehauptung:** 171/171 zugeordnete Records dürfen weder als 171/171 semantisch abgedeckte noch als zeitlich gesicherte Unterrichtsabdeckung kommuniziert werden.

## Freigabestatus

- Fachlicher Kandidatengraph: reviewfähig.
- Coverage-Audit: 171/171 zugeordnet und geprüft; 111 `covered`, 60 `partial`, 0 `deferred`.
- Jahresroadmap Klasse 5: `amber`.
- Jahresroadmap Klassen 6 und 7: `red`.
- Phase-1-Modulspezifikation: für den Goldstandard-Pilot nach Task-15-Abschlussreview und Nutzerentscheidung; eine Vollabdeckungsfreigabe setzt zusätzlich die recordgenaue Bearbeitung der 60 `partial`-Lücken voraus.
