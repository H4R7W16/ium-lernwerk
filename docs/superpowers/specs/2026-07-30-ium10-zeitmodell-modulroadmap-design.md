# IUM10 – Zeitmodell der Modulroadmap überarbeiten

**Status:** `approved` – am 30. Juli 2026 schriftlich als Gesamtspezifikation freigegeben
**Stand:** 30. Juli 2026

**Scope:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E

**Voraussetzung:** IUM09-Endbilanz 164 `covered` / 7 `partial` durch den Auftraggeber angenommen

**Implementierungsgrenze:** Diese Spezifikation entwirft IUM10. Sie implementiert weder das Zeitmodell noch Phase 1.

## 1. Zweck und Entscheidungszusammenfassung

IUM10 ersetzt das bisherige starre Referenzmodell von 30 Kern- plus 6 Puffereinheiten durch ein gestuftes, prüfbares Jahreszeitmodell. Es soll die reale Unsicherheit eines einstündigen Schulfachs abbilden, ohne fachliche Lernhandlungen durch rechnerische Kürzungen verschwinden zu lassen.

Die abschnittsweise freigegebenen Leitentscheidungen lauten:

1. Eine Unterrichtseinheit umfasst 45 Minuten.
2. `30 + 6` ist keine amtliche Vorgabe, sondern bleibt nur eine Vergleichsheuristik.
3. Das Lernwerk unterscheidet:
   - 30 Unterrichtseinheiten Basispfad,
   - 34 Unterrichtseinheiten Regelpfad,
   - 38 Unterrichtseinheiten Erweiterungspfad.
4. Der Basispfad enthält bereits Einführung, Erklärung, Übung, Produktarbeit, Feedback beziehungsweise Selbstkontrolle, Revision, Sicherung und mindestens einen Transfer- oder Abrufpunkt.
5. Kalenderpuffer ist ausschließlich die Differenz zwischen lokal tatsächlich erwartbarer Kapazität und gewähltem Jahrespfad.
6. Jeder Kernkandidat erhält einen maschinenprüfbaren Zeitvertrag.
7. Alle 60 IUM09-Zeitübergaben werden recordgenau entschieden.
8. Zeitgewinne durch Integration benötigen explizite Integrationsverträge.
9. Klasse 5 soll mit 30/34/38 Einheiten planbar werden.
10. Klasse 6 soll mit 30/34/38 Einheiten planbar werden, bleibt bis zum Detailaudit `amber`.
11. Klasse 7 benötigt unter unveränderter Roadmapstruktur nach aktuellem Entwurf mindestens 40 Einheiten und bleibt deshalb `red`.
12. Ein roter Zeitbefund wird nicht durch unbelegte Selbstlernzeit, Hausaufgaben, Überschriftenkürzung oder verdeckte Stoffstreichung geschlossen.

## 2. Baseline und unveränderliche Grenzen

### 2.1 Technische Baseline

IUM10 baut auf dem nach IUM09 veröffentlichten Repository-Stand `e53bad7` auf.

Die Baseline umfasst:

- 31 Modulkandidaten;
- 24 Kernmodule;
- 7 flexible Kandidaten;
- 171 Curriculumrecords;
- 164 `covered`;
- 7 `partial`;
- 60 IUM09-Zeitübergaben in 15 Kernmodulen;
- davon 56 `review-required`;
- davon 4 `roadmap-dependent`;
- Klasse 5: bisherige Kernsumme 31–44;
- Klasse 6: bisherige Kernsumme 35–50;
- Klasse 7: bisherige Kernsumme 54–78.

### 2.2 Unveränderliche Struktur

IUM10 verändert ohne neues Auftraggebergate nicht:

- Modul-IDs;
- Jahrgänge;
- Modularten;
- Voraussetzungskanten;
- Reihenfolgezwänge des Graphen;
- zentrale Lernhandlungen;
- zentrale Lernprodukte;
- das Hybridmodell aus Kern-, Vertiefungs-, Transfer- und Projektmodulen;
- Datenschutz- und Privatsphäregrenzen;
- die Trennung von semantischer Coverage und zeitlicher Durchführbarkeit.

Der Graph bleibt azyklisch. Kernmodule hängen weiterhin nicht von flexiblen Modulen ab.

### 2.3 Bedeutung der bisherigen `lessonRange`

Die vorhandene `lessonRange` bleibt als historische, eigenständige Kandidatenschätzung erhalten. Sie ist nach IUM10 nicht mehr die autoritative Jahreszuweisung.

Das neue Zeitmodell:

- referenziert jede vorhandene Kandidatenschätzung;
- dokumentiert jede Abweichung;
- unterscheidet eigenständige Kandidatenzeit von integrierter Jahreszeit;
- verändert die alte Schätzung nicht stillschweigend;
- macht im Validator eindeutig, welches Artefakt für die Jahresfreigabe maßgeblich ist.

## 3. Herleitung der Jahreskapazität

### 3.1 Amtlicher Ausgangspunkt

Die FAQ zur Bildungsreform des Kultusministeriums Baden-Württemberg weist in der G9-Stundentafel für Informatik und Medienbildung je eine Wochenstunde in den Klassen 5 bis 11 aus:

<https://km.baden-wuerttemberg.de/de/schule/schulartuebergreifend/faq-bildungsreform>

Die amtlichen Ferientermine für 2026/2027 nennen die landesweiten Ferien, vier bewegliche Ferientage sowie den Hinweis auf drei weitere unterrichtsfreie Tage für Lehrkräfte:

<https://km.baden-wuerttemberg.de/de/service/ferien>

Beide Quellen wurden am 30. Juli 2026 geprüft. Die Angaben sind administrativer Kontext, keine didaktische Zeitnorm.

### 3.2 Reproduzierbare Kalenderabschätzung 2026/2027

Eine eigene Kalenderauswertung zwischen erstem möglichem Schultag nach den Sommerferien 2026 und letztem Schultag vor den Sommerferien 2027 ergibt nach landesweit festen Ferien und Feiertagen, aber vor lokalen beweglichen Tagen und schulischen Ausfällen, je nach Wochentag ungefähr:

| Wochentag der Fachstunde | mögliche Termine vor lokalen Ausfällen |
|---|---:|
| Montag | 40 |
| Dienstag | 40 |
| Mittwoch | 39 |
| Donnerstag | 36 |
| Freitag | 37 |

Diese Zahlen sind eine datierte Projektberechnung für den Belastungstest. Sie sind weder dauerhaft noch für jede Schule garantiert.

### 3.3 Kapazitätsebenen

Das Modell unterscheidet drei Kapazitätsebenen:

1. **Kalenderkapazität**

   Rechnerisch mögliche Fachstunden nach landesweit festen Ferien und Feiertagen.

2. **Lokale Kapazität**

   Erwartbare Stunden nach beweglichen Ferientagen, pädagogischen Tagen, Praktika, Veranstaltungen und bekannten schulischen Besonderheiten.

3. **Planungskapazität**

   Der vom Lernwerk angebotene und von der Lehrkraft gewählte Jahrespfad.

### 3.4 Drei Jahrespfade

| Pfad | Umfang | Funktion |
|---|---:|---|
| `baseline` | 30 UE | curricular tragfähiger Kern mit allen unverzichtbaren Lernfunktionen |
| `regular` | 34 UE | empfohlener Jahrespfad mit zusätzlicher Übung, Revision und verteilter Wiederaufnahme |
| `extended` | 38 UE | Vertiefung, Transfer, kurze Projekte oder gezielte zusätzliche Modultiefe |

Die drei Werte besitzen zunächst Status `working`. Reale Pilotdaten können sie bestätigen oder verändern.

### 3.5 Pufferregel

Puffer ist kein Unterrichtsinhalt und keine versteckte Lernphase.

```text
Kalenderpuffer = lokale Kapazität – gewählter Jahrespfad
```

Ausfall, organisatorische Unterbrechung oder ungeplante Wiederaufnahme verbrauchen diesen Kalenderpuffer. Unverzichtbare Übung, Feedback, Sicherung und Transfer gehören bereits in den gewählten Jahrespfad.

## 4. Zeitvertrag eines Moduls

### 4.1 Vertragszweck

Jedes der 24 Kernmodule erhält genau einen autoritativen Zeitvertrag. Flexible Module erhalten ebenfalls einen Vertrag, werden aber nicht automatisch in die Kernjahressumme aufgenommen.

Ein Zeitvertrag weist für jeden einschlägigen Pfad aus:

- Gesamtzeit in Unterrichtseinheiten;
- Gesamtzeit in Minuten;
- direkte Modulzeit;
- gemeinsam genutzte Zeit über Integrationsverträge;
- Phasenbudgets;
- zentrale Lernhandlungen und Produkte;
- betroffene Curriculumrecords;
- IUM09-Zeitreviews;
- schulabhängige Ausführungsschritte;
- Voraussetzungen und spätere Wiederaufnahme;
- Status, Risiko und Pilotbedarf.

### 4.2 Phasenbudgets

Die sieben Phasen der freigegebenen Modulgrammatik bleiben erhalten:

1. `orientation-challenge`
2. `activate-prior-knowledge`
3. `build-concept`
4. `guided-practice`
5. `independent-action-product`
6. `review-revise-transfer`
7. `shared-consolidation`

Der Basispfad eines Moduls darf keine erforderliche Lernfunktion nur benennen und mit null Minuten ausweisen.

Mehrere Phasen dürfen innerhalb derselben 45-Minuten-Einheit stattfinden. Deshalb führt der Vertrag Minutenbudgets, während die Jahresplanung in ganzen Unterrichtseinheiten summiert wird.

### 4.3 Direkte und gemeinsam genutzte Zeit

Gemeinsam genutzte Phasen werden über einen Integrationsvertrag referenziert. Jeder Integrationsvertrag benennt genau ein `countedInModuleId`. Dadurch zählt die gemeinsame Zeit in der Jahressumme genau einmal.

Für jedes beteiligte Modul wird dennoch geprüft, ob seine fachliche Funktion durch die gemeinsame Phase tatsächlich erfüllt wird.

### 4.4 Mindestanforderungen an den Basispfad

Jeder Basispfad enthält:

- Ziel- und Produktklarheit;
- mindestens eine fachlich gehaltvolle Aktivierung oder Vorwissensaufnahme;
- expliziten Begriffs-, Modell- oder Verfahrensaufbau;
- angeleitete Übung;
- eigenständige Lernhandlung;
- beobachtbare Produkt- oder Nachweisspur;
- Feedback, Selbstkontrolle oder kriterielle Rückmeldung;
- anschließende Revision oder Weiterarbeit;
- gemeinsame Sicherung;
- Transfer oder späteren aktiven Abruf.

## 5. Recordgenauer Review der 60 Zeitübergaben

### 5.1 Vollständigkeitsregel

Jeder Eintrag aus `coverage-remediation.json` erhält genau einen IUM10-Zeitreview. Die Identität der 60 Ausgangsrecords bleibt unverändert.

### 5.2 Entscheidungsarten

| Entscheidung | Bedeutung | Zusatzzeit |
|---|---|---:|
| `absorbed` | dieselbe fachliche Lernhandlung und dasselbe Produkt tragen die Anforderung bereits | 0 zusätzliche Minuten; Bindung an eine positive vorhandene Phase |
| `integrated` | eigene Lernzeit ist nötig, kann aber fachlich mit einer anderen Handlung verbunden werden | positive Zeit oder gemeinsame Integrationszeit |
| `additional-time` | eigenständige Erklärung, Übung, Ausführung, Revision oder Sicherung ist nötig | positive zusätzliche Minuten |
| `unresolved` | Verortung oder Zeitbedarf ist noch nicht belastbar | keine fingierte Präzision; Risiko und Folgeauftrag verpflichtend |

### 5.3 Pflichtfelder

Jeder Zeitreview enthält mindestens:

- `id`;
- `competencyId`;
- `moduleId`;
- `sourceTimeImpactLevel`;
- `decision`;
- `rationale`;
- `phaseIds`;
- `additionalMinutes`;
- gegebenenfalls `integrationContractIds`;
- `pathAvailability`;
- `coverageConsequence`;
- `risk`;
- `followUp`;
- `status`.

### 5.4 Roadmapabhängige Records

Die vier Records `LH26-E-PROG-001` bis `LH26-E-PROG-004` erhalten keinen fingierten Einzelmodulnachweis. Sie werden über Sequenznachweise geprüft.

Ein Sequenznachweis enthält:

- betroffene Module und Jahrgänge;
- fachliche Progression;
- zunehmende Operator- und Produkttiefe;
- Perspektivengewichtung;
- Zeitgewichtung;
- verfügbaren Jahrespfad;
- verbleibende Grenze;
- Coverageentscheidung.

## 6. Integrationsverträge

### 6.1 Zulässige Integrationen

Zeit darf eingespart werden durch:

- gemeinsame Aktivierung an Modulübergängen;
- Wiederaufnahme eines früheren Produkts statt vollständigem Neueinstieg;
- ein gemeinsames Produkt mit mehreren fachlich zusammenhängenden Nachweisspuren;
- Verbindung von Feedback und unmittelbar anschließender Revision;
- Verzicht auf redundante Bedienübungen;
- Verzicht auf redundante Beispiele oder Darstellungsvarianten;
- gemeinsame Sicherung tatsächlich verbundener Konzepte.

### 6.2 Unzulässige Scheinkürzungen

Nicht zulässig sind:

- Operatoren nur erwähnen statt ausführen;
- selbstständige Anwendung durch Demonstration ersetzen;
- Übung, Feedback, Revision oder Transfer in Hausaufgaben verschieben;
- fachlich getrennte Produkte nur sprachlich zusammenziehen;
- Werkzeugkompetenz ohne Lern- oder Prüfzeit voraussetzen;
- unbeaufsichtigte digitale Selbstlernzeit als garantierte Unterrichtszeit anrechnen;
- ein Kernmodul faktisch entfernen, ohne Coverage recordgenau neu zuzuordnen;
- private Reflexion zur öffentlichen Nachweisspur machen;
- flexible Module als verdeckte Voraussetzung der Kernabdeckung nutzen.

### 6.3 Pflichtfelder eines Integrationsvertrags

Ein Integrationsvertrag enthält:

- `id`;
- beteiligte Modul-IDs;
- beteiligte Pfade;
- gemeinsame Phase oder Produktspur;
- `countedInModuleId`;
- eingesparte Minuten gegenüber eigenständiger Durchführung;
- erhaltene modulbezogene Lernhandlungen;
- erhaltene Produkt- und Curriculumnachweise;
- Voraussetzungen;
- Risiko;
- Rückfalloption;
- Status.

Scheitert ein Integrationsvertrag, gilt wieder die Summe der eigenständigen Modulzeiten.

## 7. Jahrgangsmodelle

### 7.1 Klasse 5

| Modul | Basispfad | Regelpfad | Erweiterungspfad |
|---|---:|---:|---:|
| `IUM-5-CORE-01` Arbeitsfähigkeit | 5 | 6 | 6 |
| `IUM-5-CORE-02` Recherche | 4 | 5 | 5 |
| `IUM-5-CORE-03` Kommunikation | 4 | 5 | 5 |
| `IUM-5-CORE-04` Datenweg | 3 | 3 | 3 |
| `IUM-5-CORE-05` Algorithmen | 5 | 5 | 6 |
| `IUM-5-CORE-06` Medienprodukt | 5 | 5 | 7 |
| `IUM-5-CORE-07` Medienwirkung | 4 | 5 | 6 |
| **Gesamt** | **30** | **34** | **38** |

Die Reduktion gegenüber dem bisherigen Minimum von 31 Einheiten beruht primär auf gemeinsam genutzten Quellen- und Belegspuren zwischen Recherche und Medienproduktion.

Der ausgewiesene 38er-Pfad vertieft:

- Algorithmusübung;
- Medienproduktion;
- Medienreflexion.

Für Klasse 5 gibt es weiterhin bewusst kein separates flexibles Modul.

### 7.2 Klasse 6

| Modul | Basispfad | Regelpfad |
|---|---:|---:|
| `IUM-6-CORE-01` Suche, Akteure und KI | 5 | 6 |
| `IUM-6-CORE-02` Datenfluss und Auswahl | 4 | 5 |
| `IUM-6-CORE-03` Codierungen | 4 | 4 |
| `IUM-6-CORE-04` Programme und Schleifen | 4 | 5 |
| `IUM-6-CORE-05` Netze und Speicher | 4 | 4 |
| `IUM-6-CORE-06` soziale Konflikte | 4 | 4 |
| `IUM-6-CORE-07` Wirkung, Rechte und Revision | 5 | 6 |
| **Gesamt** | **30** | **34** |

Die Reduktion gegenüber dem bisherigen Minimum von 35 Einheiten beruht auf drei zu prüfenden Integrationslinien:

1. Suchmaschinen/KI und personalisierte Auswahl teilen Akteurs-, Interessen- und Evidenzmodelle.
2. Konfliktanalyse und Medienproduktion teilen Zielgruppen-, Wirkungs-, Rechte- und Revisionsarbeit.
3. Programmierarbeit baut unmittelbar auf dem Algorithmusprodukt aus Klasse 5 auf.

Die Referenzvariante des 38er-Pfads ergänzt den 34er-Regelpfad um `IUM-6-EXT-01` mit vier Einheiten.

Gleichwertige Alternativvarianten dürfen nach eigenem Zeit- und Coveragecheck verwenden:

- `IUM-6-TRANSFER-01` mit vier Einheiten;
- `IUM-6-EXT-02` mit drei Einheiten plus eine gezielte Kernvertiefung;
- eine andere geprüfte Kombination, deren Jahressumme exakt 38 Einheiten beträgt.

`IUM-6-PROJECT-01` benötigt mit 8–12 Einheiten zusätzliche Projekt- oder Schwerpunktzeit und gehört nicht in den normalen 38er-Pfad.

### 7.3 Klasse 7

Die zehn Kernmodule werden in vier Orchestrierungscluster gegliedert:

| Cluster | Module | optimierte Untergrenze |
|---|---|---:|
| Daten und Codierung | `IUM-7-CORE-01`, `IUM-7-CORE-02` | 8 |
| Programmieren | `IUM-7-CORE-03`, `IUM-7-CORE-04` | 11 |
| Netze und Sicherheit | `IUM-7-CORE-05`, `IUM-7-CORE-06`, `IUM-7-CORE-07` | 11 |
| Daten, Medien und Gesellschaft | `IUM-7-CORE-08`, `IUM-7-CORE-09`, `IUM-7-CORE-10` | 10 |
| **Gesamt** |  | **40** |

Die Modulmatrix lautet:

| Modul | optimierte Untergrenze | robuster Bedarf | bisheriges Minimum |
|---|---:|---:|---:|
| `IUM-7-CORE-01` Zeichen, Zahlen und Bits | 5 | 5 | 6 |
| `IUM-7-CORE-02` Bilder als Daten | 3 | 4 | 5 |
| `IUM-7-CORE-03` Kontrollfluss und Zustände | 5 | 5 | 6 |
| `IUM-7-CORE-04` Implementieren, Testen, Debuggen | 6 | 6 | 7 |
| `IUM-7-CORE-05` Netze, Speicher, Schutz | 4 | 4 | 5 |
| `IUM-7-CORE-06` Verschlüsselungsmodelle | 3 | 3 | 4 |
| `IUM-7-CORE-07` Verschlüsselung angreifen | 4 | 4 | 5 |
| `IUM-7-CORE-08` Daten, Akteure, Desinformation | 4 | 6 | 6 |
| `IUM-7-CORE-09` Gamingmechanismen | 2 | 3 | 4 |
| `IUM-7-CORE-10` Medienbilder und Revision | 4 | 6 | 6 |
| **Gesamt** | **40** | **46** | **54** |

Die optimierte Untergrenze setzt starke Integration voraus und ist noch kein freigegebener Kurzpfad. Selbst sie überschreitet:

- den 30er-Basispfad um 10 Einheiten;
- den 34er-Regelpfad um 6 Einheiten;
- den 38er-Erweiterungspfad um 2 Einheiten.

Klasse 7 bleibt deshalb `red`. Flexible Module werden nicht eingeplant, solange der Kernzeitkonflikt ungelöst ist.

IUM10 weist als getrennte Folgeoptionen aus:

- zusätzliche schulische Zeit;
- strukturelle Integration oder Reklassifikation einzelner Kernmodule;
- curriculare Neupriorisierung nach Inkrafttreten des neuen Fachplans;
- Verschiebung geeigneter vorbereitender Anteile in frühere Jahrgänge;
- ausdrücklich unvollständiger 30er-Pfad mit recordgenau offengelegter Coverage-Lücke.

Keine dieser Folgeoptionen wird ohne neues Auftraggebergate umgesetzt.

## 8. Coverage- und Progressionsfolgen

### 8.1 Trennung der Status

IUM10 führt getrennte Status:

- `semanticCoverageStatus`;
- `timeFeasibilityStatus`;
- `sequenceEvidenceStatus`;
- `pilotStatus`.

Ein semantisch `covered`-Record kann zeitlich noch nicht freigegeben sein. Ein grüner Zeitpfad darf umgekehrt keine semantische Lücke verdecken.

### 8.2 Statuswechsel bei Roadmaprecords

Ein `roadmap-dependent`-Record darf nur von `partial` zu `covered` wechseln, wenn:

- ein vollständiger Sequenznachweis vorliegt;
- Progression und Zeitgewichtung nachgewiesen sind;
- mindestens ein tatsächlich verfügbarer Jahrespfad die Sequenz trägt;
- der Nachweis nicht auf einem Einzelmodulvertrag beruht;
- der Fachaudit den Statuswechsel ausdrücklich bestätigt.

Voraussichtliche Arbeitsannahme:

- `LH26-E-PROG-001` kann nach bestandenem Klasse-5/6-Review geschlossen werden.
- `LH26-E-PROG-002` kann nach bestandenem jahrgangsübergreifendem Algorithmenreview geschlossen werden.
- `LH26-E-PROG-003` bleibt mindestens solange `partial`, wie Klasse 7 keinen verfügbaren Jahrespfad besitzt.
- `LH26-E-PROG-004` bleibt mindestens solange `partial`, wie Klasse 7 keinen verfügbaren Jahrespfad besitzt.

Die Spezifikation nimmt keinen Statuswechsel vorweg.

### 8.3 Übrige `partial`-Records

Die Records:

- `BMB16-GYM-IK-GM-003`;
- `BMB16-GYM-PK-RK-003`;
- `LH26-E-DP-003`

bleiben ohne neuen fachlich tragfähigen Nachweis `partial`. Zeitzuweisung allein schließt keine semantische Lücke.

## 9. Artefaktarchitektur

### 9.1 Neues autoritatives Artefakt

IUM10 führt ein:

```text
roadmap/time-model.json
```

Es enthält:

- Zeiteinheit;
- Kapazitätsbänder;
- Modulzeitverträge;
- Integrationsverträge;
- Jahresvarianten;
- 60 Zeitreviews;
- vier Sequenznachweise;
- Jahrgangsurteile;
- Risiken und Pilotaufträge.

### 9.2 Bestehende Artefakte

`roadmap/module-candidates.json`

- behält den Strukturgraphen;
- behält die historische `lessonRange`;
- erhält eindeutige Referenzen auf Zeitverträge;
- erklärt die neue Bedeutung der Zeitfelder in `modelNotes`.

`roadmap/coverage-remediation.json`

- behält die 60 Ausgangsübergaben;
- erhält für jeden Eintrag genau eine Referenz auf den IUM10-Zeitreview;
- verliert keine IUM09-Begründung.

`roadmap/coverage-plan.json`

- bleibt Quelle der semantischen Coverage;
- referenziert Zeit- und Sequenznachweise;
- ändert Coverage nur nach explizitem Fachentscheid.

`roadmap/module-roadmap.md`

- dokumentiert die drei Jahrespfade;
- zeigt Modulmatrizen und Integrationen;
- weist Klasse 7 `red` aus;
- enthält die lesbare 60/60-Zeitbilanz;
- trennt Projektannahme, Rechenergebnis und Freigabeurteil.

### 9.3 Validator und Tests

Neu entstehen:

```text
scripts/validate_ium10.py
tests/test_validate_ium10.py
```

Der gemeinsame Repository-Einstieg ruft Phase 0, IUM09 und IUM10 zusammen auf.

## 10. Validierungsregeln

Der IUM10-Validator prüft mindestens:

1. genau einen Zeitvertrag für jedes der 31 Module;
2. genau einen IUM10-Zeitreview für jeden der 60 IUM09-Übergaberecords;
3. genau einen Sequenznachweis für jeden der vier `roadmap-dependent`-Records;
4. korrekte 45-Minuten-Einheit;
5. Phasenbudgets ergeben exakt die jeweilige Modulzeit;
6. erforderliche Lernfunktionen sind im Basispfad größer als null;
7. gemeinsam genutzte Zeit wird nur einmal gezählt;
8. jeder Integrationsvertrag nennt `countedInModuleId`;
9. kein Modul verschwindet durch Integration;
10. kein Curriculumrecord verschwindet durch Integration;
11. Klasse 5 summiert sich auf 30/34/38;
12. Klasse 6 summiert sich auf 30/34/38;
13. Klasse 7 ist mit 40/46/54 und `red` konsistent;
14. `covered` auf Roadmapebene setzt einen tragfähigen Sequenznachweis und einen verfügbaren Jahrespfad voraus;
15. Modul-IDs, Jahrgänge, Arten und Voraussetzungen bleiben gegenüber der IUM09-Baseline unverändert;
16. flexible Module ersetzen keine Kernabdeckung;
17. die historische `lessonRange` bleibt zur Baseline nachvollziehbar;
18. Coverage-, IUM09- und Phase-0-Validatoren bleiben grün;
19. alle JSON-Dateien sind UTF-8 und deterministisch serialisierbar;
20. menschenlesbare Roadmap und maschinenlesbare Bilanz widersprechen sich nicht.

## 11. Review- und Freigabegates

### Gate 1 – Baseline

Graph, Modulstruktur, Coveragebilanz und 60 Zeitübergaben werden maschinell gegen IUM09 gesichert.

### Gate 2 – Zeitverträge

Alle Module erhalten vollständige Phasenbudgets. Eine rechnerisch passende Summe genügt nicht.

### Gate 3 – Integration

Jede Zeitersparnis wird fachlich und technisch geprüft. Scheitert eine Integration, fällt das Modell auf die eigenständigen Zeiten zurück.

### Gate 4 – Jahrgänge

- Klasse 5: Ziel `green`;
- Klasse 6: Ziel `green`, andernfalls begründetes `amber`;
- Klasse 7: dokumentiertes `red` mit entscheidungsreifen Folgeoptionen.

### Gate 5 – getrenntes Fach- und Engineeringreview

Geprüft werden:

- fachliche Tragfähigkeit;
- Lernhandlungs- und Produktrealismus;
- Datenschutz- und Privatsphäregrenzen;
- Zeitrealismus;
- Datenschema;
- Validatoren;
- Konsistenz der Dokumentation.

### Gate 6 – gesondertes Auftraggebergate

IUM10 wird nicht automatisch freigegeben. Vorgelegt werden:

- Modulzeitmatrix;
- 60/60-Zeitbilanz;
- Jahresvarianten;
- Coverage- und Progressionsfolgen;
- verbleibende Risiken;
- Klasse-7-Kapazitätsentscheidung.

## 12. Pilot- und Statuslogik

Ein rechnerisch grüner Pfad bleibt zunächst `working`.

Im späteren Goldstandard-Piloten werden ausschließlich auf Modulebene dokumentiert:

- tatsächlich verwendete Unterrichtszeit;
- technische Anlaufzeit;
- Unterstützungsbedarf;
- Übungs- und Revisionsbedarf;
- Unterbrechungen;
- notwendige Wiederaufnahme;
- erreichte beziehungsweise nicht erreichte Lernprodukte.

Es entstehen keine personenbezogenen Lernprofile und keine personenbezogene Telemetrie.

Erst nach Pilotierung darf ein Zeitvertrag auf `reviewed` angehoben werden.

## 13. Abbruch- und Rückfallregeln

Wenn ein Zeitvertrag nur durch Wegfall einer unverzichtbaren Lernhandlung passt:

- wird die Modulzeit erhöht;
- wird der Jahrespfad herabgestuft;
- bleibt der Curriculumrecord gegebenenfalls `partial`;
- wird keine Ausnahme in den Validator eingebaut.

Wenn technische Anlaufzeit im Schulkontext die Lernzeit substanziell verdrängt:

- wird sie im Vertrag sichtbar;
- erhält das Modul eine lokale Fallbackroute;
- wird der Jahrespfad nicht aufgrund idealisierter Technikzeit freigegeben.

Wenn eine Integration inhaltlich nicht trägt:

- wird der Vertrag auf `failed` gesetzt;
- gilt wieder die Summe der eigenständigen Modulzeiten;
- wird das Jahrgangsurteil neu berechnet.

## 14. WU-Check

- **Kognitive Aktivierung:** Operatoren bleiben tatsächliche Denkhandlungen.
- **Konstruktive Unterstützung:** Unterstützungs- und Scaffoldingzeit wird im Basispfad eingeplant.
- **Klassenführung / Struktur:** Drei benannte Jahrespfade ersetzen einen scheinbar universellen Stundenplan.
- **Aufgabenqualität:** Zeit wird von Lernhandlung und Produkt, nicht von Themenüberschriften abgeleitet.
- **Feedback / Diagnose:** Jeder Basispfad enthält sichtbare Rückmeldung und Anschlussrevision.
- **Kooperation / Verantwortlichkeit:** Kooperative Zeitgewinne benötigen gemeinsame und modulbezogene Nachweisspuren.
- **Diagnose-Fallback:** Ausgefallene Produkte oder Selbstchecks lösen Nachsicherung aus.
- **Sprachsensibilität / Zugänglichkeit:** Erklärungs- und Unterstützungszeit darf nicht zugunsten reiner Stoffabdeckung verschwinden.
- **Wichtigste Verbesserung:** Reale Pilotdaten müssen die modellierten Zeitwerte bestätigen oder ersetzen.
- **WU-Quellenbasis:** IBBW Wirksamer Unterricht, Band 1 Grundlagen, Band 3 Konstruktive Unterstützung, Band 5 Formatives Feedback, Band 6 Aufgaben im Fachunterricht; Fachprofil IuM Gymnasium 5–7; Curriculum-Mapping; IUM09-Zeitübergaben.

## 15. Akzeptanzkriterien für die spätere Implementierung

- [ ] `roadmap/time-model.json` ist vollständig und schemafest.
- [ ] Alle 31 Module besitzen einen Zeitvertrag.
- [ ] Alle 24 Kernmodule besitzen nachvollziehbare Basispfad- und Regelpfadbudgets.
- [ ] Alle 7 flexiblen Module besitzen einen zusätzlichen Zeitkorridor und klare Andockbedingungen.
- [ ] Alle 60 IUM09-Zeitübergaben sind genau einmal entschieden.
- [ ] Alle 4 roadmapabhängigen Records besitzen einen Sequenznachweis.
- [ ] Übung, Feedback, Revision, Sicherung und Transfer sind nicht Nullzeit.
- [ ] Klasse 5 besitzt konsistente 30/34/38-Varianten.
- [ ] Klasse 6 besitzt konsistente 30/34/38-Varianten.
- [ ] Klasse 7 besitzt eine belastbare 40/46/54-Bedarfsrechnung und bleibt ohne neue Entscheidung `red`.
- [ ] Curriculumabdeckung, Progression und Hybridmodell bleiben erhalten oder Abweichungen werden recordgenau ausgewiesen.
- [ ] Graph und Strukturgrenzen bleiben unverändert.
- [ ] Phase-0-, IUM09- und IUM10-Validatoren sowie alle Tests sind grün.
- [ ] Ein getrenntes Fach- und Engineeringreview ist dokumentiert.
- [ ] Das neue Zeitmodell wird dem Auftraggeber als eigenes Freigabegate vorgelegt.

## 16. Nichtziele

IUM10:

- implementiert keine Lernmodule;
- baut keine Plattform;
- plant keine Phase 1;
- verändert keine Datenschutzarchitektur;
- erstellt keine personenbezogene Diagnostik;
- entscheidet keine neue curriculare Norm;
- macht aus der Lesehilfe keine in Kraft gesetzte Vorgabe;
- löst den Klasse-7-Konflikt nicht ohne neues Auftraggebergate;
- erhebt Zeitannahmen nicht ohne Pilotierung zu `reviewed` oder `standard`.

## 17. Nächster Schritt nach schriftlicher Freigabe

Die schriftliche Freigabe erfolgte am 30. Juli 2026. Als nächster Schritt wird mit dem Skill `superpowers:writing-plans` ein ausführbarer, testgetriebener IUM10-Implementierungsplan erstellt.

Die Freigabe dieser Spezifikation erlaubt die Planung, nicht die automatische Implementierung oder Phase-1-Planung.
