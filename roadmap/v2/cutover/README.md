# IUM-V2-CUT – Entscheidung über die V2-Baseline

Stand: 6. September 2026 · **Zur Nutzerentscheidung** · V1 aktiv · V2 `building`.

## Empfehlung und Entscheidungsgegenstand

**V2 als Planungs- und Entwicklungsbaseline annehmen**, unter ausdrücklicher Fortführung der unten aufgeführten Grenzen. Die 17 Vorgängergates einschließlich DASH sind einzeln fachlich angenommen. Curriculum, Quellen, Lern-Experience, Governance, Übernahmeaudit und Jahrgangsplanung sind ausreichend bestimmt, um die weitere Entwicklung daran auszurichten. Es gibt keinen nachgewiesenen V2-Produkt- oder Unterrichtsstand.

Die bisherige DASH-Freigabe und der CUT-Auftrag eröffnen diese Entscheidungsvorbereitung. Die konkrete Auswahl ist noch nicht getroffen. Bis dahin bleiben V1 aktiv, V2 `building` und die Inhalte eingefroren. CUT ist Gate 18, im Review; kein achtzehntes angenommenes Gate.

| Option | Konsequenz |
|---|---|
| **Annehmen – empfohlen** | V2 nach kontrollierter Aktivierung als maßgebliche Planungs-/Entwicklungsbaseline führen. V1 als historische Referenz und bestehender Produktstand erhalten. Die offenen Einsatzbedingungen ausdrücklich weiterführen. |
| Vertagen | V1 aktiv und V2 im Aufbau lassen; fehlende Entscheidungsgrundlage konkret benennen. |
| Nacharbeiten | V1 aktiv lassen und betroffene Kriterien benennen. Bereits erteilte Teilfreigaben nicht pauschal rückwirkend aufheben. |

**Keine Option beinhaltet:** neue Lernmaterialproduktion, LXP05-Integration, Pilotierung, Schul-/Betreiberfreigabe, Hosting, Veröffentlichung, Merge oder Push. FU-TECH, FU-MOD und FU-PILOT bleiben eigene, noch gesperrte Folgeaufträge mit ihren Abhängigkeiten.

## Prüfbasis und Aussagegrenzen

Der angenommene Kandidatenstand vor den CUT-Ergänzungen ist DASH-Commit `85ccc94b1dc9c5cc60fc48470bd6346cac3b3e50`. Die Entscheidungsvorlage ergänzt diesen Stand im selben isolierten Branch `feat/ium-v2-rebaseline`; ihren eigenen Abschlusscommit nennt der Session-Handoff. Der Kandidatencommit ist **nicht** der Commit der neu hinzugefügten CUT-Prüfung.

[review.json](review.json) bindet jedes Vorgängergate an eine tatsächliche Nutzerfreigabe, einen vollständigen Git-Commit und SHA-256-Digests ausgewählter Artefakte **aus diesem historischen Commit**. Zusätzlich schützen 104 aktuelle Inputdigests die Kriterien, Statusgrenzen, Dashboardquellen und Validatoren vor Drift. Historische Git-Blob-Digests verwenden exakte Bytes. Aktuelle Textdigests normalisieren CRLF zu LF entsprechend den bestehenden V2-Prüfsiegeln; gleiche Inhalte bleiben dadurch über Git-Checkouts hinweg gültig. Eine Arbeitskopie oder ein Testlauf erteilt keine Freigabe.

Die Prüfung ist ein KI-gestützter Dokumenten- und Vertragsreview mit technischen Regressionen. Sie ist keine unabhängige fachliche Doppelprüfung, keine erneute Onlineprüfung aller Quellen und keine Beobachtung von Lernenden. Schulrechtliche, datenschutzfachliche und organisatorische Einsatzentscheidungen werden nicht vorweggenommen.

## Alle 17 angenommenen Vorgängergates

| Nr. | Gate | Nutzerfreigabe | Angenommener Commit |
|---|---|---|---|
| 1 | IUM-V2-00 | 2026-09-03 | `59df1385d69e79ed90616de8d32d790c10b796e9` |
| 2 | IUM-V2-01 | 2026-09-03 | `fac45a9cad671ba5194e4ed778580f824ecb3b65` |
| 3 | IUM-V2-CUR | 2026-09-03 | `e0171a2d0f522b18989b3a6bae3b54caa5e1a827` |
| 4 | IUM-V2-SRC | 2026-09-03 | `1ff08e50197b3cd58ae3654a9bea5e4ea90eea16` |
| 5 | LXF01 | 2026-09-03 | `3a3d4c0d3efbaf7cc9db70f9493298636b7345e8` |
| 6 | LXF02 | 2026-09-03 | `be77fe1b1297ec048b3fee3783dc97657568deb7` |
| 7 | LXF03 | 2026-09-03 | `370193bff9d9e0040478b72a70166cca8b42d435` |
| 8 | LXF04 | 2026-09-03 | `1b8c0f3d7b99a42cd12b4ae8dcbe5923103e0b74` |
| 9 | LXF05 | 2026-09-05 | `22e9978e86fe5a0fc61e1d5de8072c7a94e18eeb` |
| 10 | LXF06 | 2026-09-05 | `beaba6d3382d60ef31b1171368e4580b2e1432b3` |
| 11 | LXF07 | 2026-09-05 | `d11a8bc69775525ec0162516275bb39f5dc9c441` |
| 12 | IUM-V2-GOV | 2026-09-06 | `9f52cdc6f5e36b72b7a3fd9e64501ccfc4af2135` |
| 13 | IUM-V2-AUD | 2026-09-06 | `dc059cffcb2866c6e0d7df3c83dbc0410d14d680` |
| 14 | IUM-V2-R5 | 2026-09-06 | `5146310ae855636d3529e8d31b079b5ca265da6e` |
| 15 | IUM-V2-R6 | 2026-09-06 | `c38ff9b0b037539b37d6964091c38dc3c323344a` |
| 16 | IUM-V2-R7 | 2026-09-06 | `60c7d0a195bc6f3e6803bdc2a97e4a7479e28a24` |
| 17 | IUM-V2-DASH | 2026-09-06 | `85ccc94b1dc9c5cc60fc48470bd6346cac3b3e50` |

Die exakten Freigabeauszüge und Pfade der Task-Notizen stehen in `gates[].approvalEvidence`; `--vault` prüft sie gegen den tatsächlichen Vault. Für 00, CUR und LXF02 sind die abschließenden Korrektur-/Archivstände verwendet. Bei SRC liegen die Nachweise in `inventory.json` und `traceability.json` des angenommenen Commits; spätere Registerdateien werden ihm nicht rückwirkend zugeschrieben. Die LXF05-Musterfreigabe am 5. September wird vom später im LXF06-Commit dokumentierten Statuswechsel getrennt.

## Kriterienmatrix

Die acht Anforderungen sind als **Planungsvertrag geprüft**. Ihr Feld `coverage` bleibt `unassessed`: Annahme des Plans ersetzt keinen ausgeführten Curriculum- oder Nutzungsnachweis.

| Anforderung | Gegenstand | Tragende Gates |
|---|---|---|
| V2-REQ-SYS-001 | V1 und V2 bis zum Cutover strikt trennen | IUM-V2-00 |
| V2-REQ-SYS-002 | Inhaltsproduktion während der Grundlagenarbeit geschlossen halten | IUM-V2-01, IUM-V2-AUD |
| V2-REQ-CUR-001 | Curriculumquellen nach Bindungsgrad unterscheiden | IUM-V2-CUR |
| V2-REQ-CUR-002 | Drei Formen der Curriculumabdeckung zulassen | IUM-V2-CUR, IUM-V2-R5, IUM-V2-R6, IUM-V2-R7 |
| V2-REQ-SRC-001 | Quellen, Claims und Gestaltungsentscheidungen rückverfolgbar machen | IUM-V2-SRC, LXF02 |
| V2-REQ-LXF-001 | Die vollständige Lernarchitektur vor der Inhaltsproduktion fundieren | LXF07 |
| V2-REQ-GOV-001 | Öffentliche Aussagen an Mindestnachweise binden | IUM-V2-GOV |
| V2-REQ-DASH-001 | Dashboard auf die V1/V2-Steuerung ausrichten | IUM-V2-DASH |

- **Curriculum:** Amtliche Anforderungen und orientierende Lesehilfe bleiben getrennt; die drei Erfüllungsmodi werden auf die geplante Handlung bezogen. Alte V1-Coverage wird nicht auf V2 übertragen.
- **Quellen und Lern-Experience:** Quellen-/Claimgrenzen, Lernendenprofil, 18 Architekturprinzipien, zehn Materialmuster und die Lehrkraftorchestrierung liegen als angenommene Planung vor. LXF07 ist `reviewed`, kein durch einen Unterrichtspilot belegter Standard.
- **Governance:** Verantwortlichkeiten, Aussagearten, Rechte und Recheck-Auslöser sind benannt. Offene Besetzung und Einsatzentscheidungen bleiben sichtbar.
- **Übernahmeaudit:** 25 Artefaktfamilien: 1 beibehalten, 15 anpassen, 5 ersetzen, 4 nur Referenz. Historischer Bestand und LXP05 sind Referenzen, keine fertigen V2-Bausteine. Drei Folgeaufträge bleiben außerhalb der ursprünglichen 18 Gate-Tasks.
- **Klasse 5:** Sechs Kernmodule mit 1.260 Minuten/28 UE; 32/36/40-UE-Varianten. Von 144 Records sind 62 Klasse 5 zugeordnet, 17 an R6 übergeben, sechs Eigenbezugsnachweise offen und 59 Kontext. „Zugeordnet“ bedeutet geplant.
- **Klasse 6:** Sieben Kernmodule mit 1.215 Minuten/27 UE; 32/36/40-UE-Varianten und sechs Eintrittsklärungen. 85 Lesehilfe-Records: 17 Erstzuordnungen, 39 Wiederaufnahmen, vier Lesehilfe-Eigenbezugsfragen, 25 Kontext. Zusammen mit zwei übernommenen amtlichen BMB-Fragen bleiben die sechs bisherigen Nachweisfragen offen.
- **Klasse 7:** Fünf Kernmodule mit 1.260 Minuten/28 UE, zwei curriculare Erweiterungen und separat budgetierte Jahresposten. 134 Records: 51 amtliche Kompetenzen, 31 orientierende Kompetenzen, 52 Kontext. Sieben Progressionsstränge und zugehörige Eintrittsklärungen sind geplant, nicht mit einer realen Lerngruppe ausgeführt.
- **Dashboard:** Acht lokale Ansichten mit getrennten Reifeachsen, allen 18 Gates, Commitbezügen und sichtbarer Offenheit. Der fehlende historische Dashboardcommit und zwei fehlende optionale alte Task-Notizen bleiben als Quellenlücken dokumentiert. Sie sind kein Nachweis für erledigte Arbeit.

## Zeit, Eigenbezug und tatsächliche Eingangslage

| R7-Pfad | Bedarf | Geplante Kompetenzen | Zeitbedingt offene Orientierung | Offene neue Reflexionsnachweise |
|---|---|---|---|---|
| CORE36 | 36 UE | 71 = 51 amtlich + 20 orientierend | 8 | 3 |
| MEDIA40 | 40 UE | 76 = 51 amtlich + 25 orientierend | 3 | 3 |
| DEMAND43 | 43 UE | 79 = 51 amtlich + 28 orientierend | 0 | 3 |

Alle lokalen Verfügbarkeiten sind **ungeprüft**. 43 UE sind ein Bedarf, keine vorhandene Kapazität. Die neun Vergleiche der drei Pfade mit 32/36/40 Netto-UE sind Rechenfälle. Vor Einsatz sind Nettozeit, verfügbare Werkzeuge und tatsächliche Eingangslage zu bestimmen. Freigegebene R5-/R6-Pläne beweisen keine Durchführung oder vorhandenes Vorwissen.

Sechs übernommene Eigenbezugsfragen: `BMB16-GYM-IK-MG-001`, `BMB16-GYM-PK-RK-001`, `LH26-E-DP-002`, `LH26-E-DP-003`, `LH26-E-DP-009`, `LH26-E-KS-011`. Drei zusätzliche R7-Reflexionsfragen: `LH26-E-DP-013`, `LH26-E-DP-014`, `LH26-E-DP-018`.

Damit bestehen **neun unterschiedliche Nachweisfragen**, keine neun neuen amtlichen Klasse-7-Anforderungen. Fallanalysen ersetzen nicht automatisch eigenen Reflexionsbezug. Datensparsame eigene Unterrichtsreflexion kann geeignet sein; eine konkrete tragfähige Nachweisregel ist noch zu prüfen. Private Offenlegung wird nicht zur Voraussetzung gemacht.

## Fortgeführte Bedingungen

46 Einträge: 16 Grundlagenfragen, 18 Jahrgangsgates, neun konkrete Nachweisfragen und drei gesperrte Folgeaufträge. **Zwei Planungsbedingungen sind inzwischen erfüllt; 44 Einträge sind offen oder gesperrt.** Die Einträge überschneiden sich und bilden keine Zahl unabhängiger Risiken.

`R6-R7-TRANSITION` ist als Anschlussplanung erfüllt, ohne bestätigtes Vorwissen; `R7-DASH` ist durch die ausdrückliche DASH-Abnahme erfüllt. Die historischen R6-/R7-Dateien bleiben unverändert. Bei `CUR-Q-003` liefert R7 inzwischen Planungsnachweise für Fachbalance und Progression; die reale Bewährung bleibt offen. Die aktuelle Einordnung steht jeweils neben der ursprünglichen Bedingung.

Die offenen Einträge verhindern eine pauschale Einsatz-/Erfüllungsbehauptung. Sie können bei einer ausdrücklich auf Planung begrenzten Baseline-Annahme als benannte Folgepflichten weitergeführt werden. Verantwortlichkeiten, Risikowortlaut, Auslöser und Quellen stehen vollständig in `conditions[]` des JSON-Pakets; die folgende Liste dient der Entscheidungssichtung.

| ID | Stand | Verantwortlich | Auslöser und Bedingung |
|---|---|---|---|
| `CUR-Q-002` | Offen | IUM-V2-CUR / IUM-V2-GOV | Vor einer Modulspezifikation, die eigene Mediennutzung zum Gegenstand hat. — Wie wird curricular geforderter Eigenbezug ohne erzwungene persönliche Offenlegung bearbeitet? |
| `CUR-Q-003` | Offen | IUM-V2-R7 | Jahrgangsroadmap nach Freigabe der vorgeschalteten Gates. — Wie werden Fachbalance und Progression in Klasse 7 jahrgangsweit nachgewiesen? |
| `GOV-Q-OPERATOR` | Offen | project-decision | Vor Hosting oder öffentlicher V2-Prüffassung — Betreiber, rechtlich Verantwortliche, Kontakt-/Impressum-/Datenschutzhinweise und anwendbare Accessibility-Regeln konkret bestimmen. |
| `GOV-Q-REVIEWERS` | Offen | project-decision | Vor konkreter Material-, Produkt- oder öffentlicher Aussagefreigabe — Erforderliche menschliche Fachprüfende benennen; Autorenschaft, Selbstreview und externe Prüfung offenlegen. |
| `GOV-Q-RIGHTS` | Offen | project-decision | Vor Einbindung oder Veröffentlichung konkreter Assets, Logos und externer Angebote — Rechteketten und Materiallizenzen einzeln nachweisen; institutionelle Namens-/Logonutzung benötigt eigene belegte Berechtigung. |
| `GOV-Q-SCHOOL` | Offen | project-decision | Vor Nutzungsprüfung mit Lernenden oder Pilot — Schule, zuständige Stelle, Datenschutzberatung, Rechtsgrundlage, Datenfluss, Löschfristen und ggf. Auftragsverarbeitung/DSFA prüfen. |
| `LXF03-Q-001` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche aufgabenbezogenen Vorwissenszugänge zeigen in Klasse 5, 6 und 7 ausreichend früh, ob ein Modell, Begriff oder Verfahren erklärt werden muss? |
| `LXF03-Q-002` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Fachbegriffe, Operatoren und Darstellungswechsel benötigen je Jahrgang Modellierung, mündliche Vorformen oder optionale Sprachgerüste? |
| `LXF03-Q-003` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Informationsdichte, Segmentierungsart und Zahl paralleler Repräsentationen bleiben je Jahrgang bei unterschiedlichen Vorkenntnissen fachlich produktiv? |
| `LXF03-Q-004` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Bedienroutinen können in den Klassen 5, 6 und 7 vorausgesetzt werden und welche müssen aufgabenbezogen vorbereitet oder technisch umgangen werden? |
| `LXF03-Q-005` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Strategien und Hilfewege müssen je Jahrgang zunächst modelliert werden, und an welchem fachlichen Produkt kann wachsende Selbstständigkeit verantwortbar erkannt werden? |
| `LXF03-Q-006` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Formen von Zweckklärung, Wahl und sichtbarer fachlicher Bewältigung tragen in den drei Jahrgängen, ohne private Offenlegung oder dekorative Motivationselemente zu verlangen? |
| `LXF03-Q-007` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Barrieren und gleichwertigen Ausdruckswege treten in den drei Jahrgängen bei den vorgesehenen Fachhandlungen, Geräten und Unterrichtsroutinen tatsächlich auf? |
| `LXF03-Q-008` | Offen | subject-didactics-reviewer / teacher-reviewer | Konkretisierung in IUM-V2-R5/R6/R7 und reale Prüfung erst nach gesonderter Pilotfreigabe. — Welche Kooperationsrollen, Haltepunkte, Zeitvarianten und Fallbacks ermöglichen je Jahrgang fachlich gehaltvollen Austausch bei vertretbarem Orchestrierungsaufwand? |
| `LXF07-Q-PILOT` | Offen | teacher-reviewer / subject-didactics-reviewer | Gesondertes Pilotierungsdesign und ausdrückliche Durchführungserlaubnis. — Trägt der Lernbogen wiederholt im Unterricht einschließlich verzögertem Abruf und Transfer? |
| `LXF07-Q-TECH` | Offen | accessibility-reviewer / integration-reviewer | Implementiertes, gesondert zur Technik- und Nutzungsprüfung freigegebenes V2-Referenzmaterial. — Funktionieren Zugang, Offlineverhalten und Wiederaufnahme am konkreten V2-Produkt? |
| `R5-ACCESS` | Offen | IUM-V2-FU-TECH / Schule / Betreiber | Vor konkreter Modulproduktion und schulischer Erprobung — Freigegebene Geräte, realer schulischer Login, zugängliche Werkzeuge und geschlossener Kommunikationsweg; Datenschutz-/Rechteentscheidung und Barrieren prüfen. |
| `R5-BUDGET` | Offen | Auftraggeber / planende Lehrkraft | Vor Verwendung einer Jahresvariante — Tatsächlich verfügbare 45-Minuten-Einheiten, Unterrichtstakt, Lerngruppe und zusätzliche Hilfen bestimmen; bei weniger als 32 Einheiten neue Teilplanung. |
| `R5-PRIVACY` | Offen | IUM-V2-CUR / Governance / zuständige Schule | Vor Nachweisbehauptung für sechs Eigenbezugsrecords — CUR-Q-002 auf alle einschlägigen Records beziehen; weder private Abgabe noch künstliche Erfüllung durch fiktive Fälle. Bis zur tragfähigen Entscheidung bleibt der Nachweis offen. |
| `R5-PILOT` | Offen | IUM-V2-FU-PILOT / fachliche Prüfende | Nach neuer Modulspezifikation und gesonderter Erprobungsfreigabe — Zeitannahmen, Zugänglichkeit, Nutzung von Hilfen/Feedback und fachliche Produkte prüfen; keine Wirksamkeitsbehauptung aus Tests. |
| `R6-ENTRY` | Offen | Planende Lehrkraft / Auftraggeber | Vor dem jeweiligen abhängigen Lernbogen — Sechs aufgabenbezogene Einstiegsprodukte sichten, Hürden unterscheiden und Unterstützung begründen. Bei breiten Lücken erst neu planen; keine private Nutzungserhebung. |
| `R6-ACCESS` | Offen | IUM-V2-FU-TECH / Schule / Betreiber | Vor Materialproduktion und schulischer Erprobung — Zugängliche Geräte, realer Schulzugang, Suchwerkzeug, geschlossener Kanal und Interpreter samt Datenschutz-/Rechtefragen prüfen. Nicht ausführbare Zielhandlungen bleiben offen. |
| `R6-BUDGET` | Offen | Auftraggeber / planende Lehrkraft | Vor Auswahl der Jahresvariante und bei Überbrückungsbedarf über 45 Minuten — Nettozeit, Unterrichtstakt und Eingangslage erheben; bei weniger als 32 UE oder breiten Lücken neue transparente Teilplanung. Kern nicht zugunsten Flex kürzen. |
| `R6-PRIVACY` | Offen | IUM-V2-CUR / Governance / zuständige Schule | Vor Nachweisbehauptungen mit eigenem Nutzungs-/Erfahrungsbezug — Alle sechs aus R5 offenen Records samt CUR-Q-002 erhalten; datenschutzfachlich tragfähige Nachweisentscheidung separat beauftragen. Zwei amtliche BMB-Lücken bleiben Klasse-5-Altlast, kein neuer R6-Pflichtkatalog. |
| `R6-PILOT` | Offen | IUM-V2-FU-PILOT / fachliche Prüfende | Nach späterer Modulspezifikation und gesonderter Erprobungsfreigabe — Zeit, Zugänglichkeit, Nutzung von Hilfen/Feedback und fachliche Produkte im freigegebenen Verfahren untersuchen; Risiken je Modul prüfen. |
| `R6-R7-TRANSITION` | Planerisch erfüllt | IUM-V2-R7 / fachliche Prüfende / Auftraggeber | Nach ausdrücklicher R6-Planungsabnahme, vor Klasse-7-Planung — R7-Anschluss aus geplanten Produkten und tatsächlicher späterer Eingangslage unterscheiden; eigenes R7-Review. R6-Abnahme öffnet keinen Pilot, keine Produktion und keinen Cutover. |
| `R7-ENTRY` | Offen | Planende Lehrkraft / Auftraggeber | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Sieben aufgabenbezogene Eingangsprodukte sichten; Sprache/Bedienung klären und bei breiten Lücken vor abhängigen Modulen neu planen. |
| `R7-ACCESS` | Offen | IUM-V2-FU-TECH / Schule / Betreiber | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Reale zugängliche und freigegebene Zielwerkzeuge samt Rechten bereitstellen; fehlende digitale Handlungen bleiben ohne Nachweis. |
| `R7-BUDGET` | Offen | Auftraggeber / planende Lehrkraft | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Lokale Nettozeit und Eingangslage prüfen. Unter 36 UE oder bei Bedarf über 45 Minuten Überbrückung neuer Teilplan mit sichtbaren amtlichen Lücken; 43 UE nicht voraussetzen. |
| `R7-SCOPE` | Offen | Auftraggeber / Curriculumprüfung / Schule | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Pfad mit acht/drei offenen Orientierungsrecords ausdrücklich wählen oder zusätzliche reale Kapazität sichern; keine stille Verschiebung nach Klasse 8 oder Flex. |
| `R7-REFLECTION` | Offen | Curriculumprüfung / Governance / Schule | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — LH26-E-DP-013/014/018 mit datensparsamer Aufgaben-/Nachweisregel klären. Unterrichtsbezogene eigene Reflexion kann möglich sein; erst konkrete Prüfung, bis dahin offen. |
| `R7-PRIVACY` | Offen | IUM-V2-CUR / Governance / Schule | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Alle sechs R5/R6-Fragen samt CUR-Q-002 erhalten; keine private Abgabe, keine künstliche Schließung durch Fremdfälle. |
| `R7-PILOT` | Offen | IUM-V2-FU-PILOT / fachliche Prüfende | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Nach späterer Spezifikation und eigener Erprobungsfreigabe Modulzeiten, Integration, Zugänglichkeit sowie Nutzung von Hilfen/Feedback tatsächlich prüfen. |
| `R7-DASH` | Planerisch erfüllt | IUM-V2-DASH / Auftraggeber | Vor jeweiliger Einsatz-, Nachweis- oder Folgeentscheidung — Erst nach R7-Nutzerabnahme Dashboardmigration separat ausführen; V1/V2, pfadabhängige Offenheit, Reifeachsen und spätere Gates erhalten. |
| `BMB16-GYM-IK-MG-001` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `BMB16-GYM-PK-RK-001` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-002` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-003` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-009` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-KS-011` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-013` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-014` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `LH26-E-DP-018` | Offen | Curriculumprüfung / Governance / zuständige Schule | Vor Modulen mit betroffenem Eigenbezug oder Reflexionsnachweis — Datensparsame, fachlich tragfähige Nachweisform operationalisieren; bis dahin keine Erfüllung behaupten. |
| `IUM-V2-FU-TECH` | Gesperrt | Auftraggeber / Codex nach eigenem Auftrag | Nach den dokumentierten Abhängigkeiten und eigenem Nutzerauftrag — Technische V1-Bausteine gegen V2 prüfen |
| `IUM-V2-FU-MOD` | Gesperrt | Auftraggeber / Codex nach eigenem Auftrag | Nach den dokumentierten Abhängigkeiten und eigenem Nutzerauftrag — Erstes V2-Referenzmodul spezifizieren |
| `IUM-V2-FU-PILOT` | Gesperrt | Auftraggeber / Codex nach eigenem Auftrag | Nach den dokumentierten Abhängigkeiten und eigenem Nutzerauftrag — Prüf- und Pilotinstrumente an V2 binden |

## Kontrollierte Aktivierung nach Auswahl

`roadmap/v2/status.json` ist selbst ein Input mehrerer historischer LXF07-, GOV- und Jahrgangsprüfungen. Ein direktes Umschreiben auf V2 würde diese Nachweise beschädigen. Deshalb beschreibt die empfohlene Option folgende konkrete Umsetzung:

1. Ausdrückliche Nutzerentscheidung an den geprüften CUT-Abschlusscommit und die hier genannten Grenzen binden.
2. Commit und aktuelle Inputdigests erneut prüfen; bei zwischenzeitlicher Änderung nicht blind aktivieren.
3. Einen **zusätzlichen** angenommenen Entscheidungsbeleg und `roadmap/v2/cutover/active-baseline.json` erstellen. Den historischen V1/building-Snapshot und V1-Archivstand erhalten.
4. Aktuelle Statusleser und Validatoren auf diesen entscheidungsgebundenen Zeiger umstellen; Annahme, Vertagung, Nacharbeit und Drift prüfen. Historische Vertragsprüfungen weiter auf ihre damaligen Inputs beziehen.
5. Cockpit und Vault synchronisieren. V2 erst danach als aktive Planungs-/Entwicklungsbaseline ausweisen; bestehender V1-Produktstand, LXP05 und alle Einsatzgrenzen separat erhalten.

Das Aktivierungsartefakt existiert in diesem Review absichtlich noch nicht. Der konkrete Aktivierungsschritt gehört zur Umsetzung der anschließenden Auswahlentscheidung; er benötigt keinen neuen fachlichen Entwurf. Die Folgeaufträge werden dadurch nicht automatisch übernommen.

## Technische Prüfung und Reproduktion

Aktuelle Resultate stehen im [CUT-Prüfbericht](validation-report.md) und in `verification` des JSON-Pakets. Solange dort `pending` steht, ist keine abgeschlossene Gesamtverifikation behauptet.

- `npm run verify:v2:cutover`: bestehendes V2-Gate und additive CUT-Prüfung.
- `python -B scripts/validate_v2_cutover.py --vault <Vault-Verzeichnis> --require-verified`: zusätzlich tatsächliche Task-Freigaben und vollständige aktuelle Prüflaufdokumentation.
- `python -B -m unittest discover -s tests -p test_validate_v2_cutover.py`: Positiv-/Negativtests gegen verlorene Nachweise, Drift und vorweggenommene Entscheidungen.
- `npm run test:dashboard`: Dashboardverträge und Projektion.
- `IUM_DASHBOARD_TEST_PORT=4327 npm run test:dashboard:browser`: Syntax für POSIX; in PowerShell die Variable mit `$env:IUM_DASHBOARD_TEST_PORT='4327'` setzen. Der Runner startet und beendet ausschließlich seinen eigenen Vorschauprozess.
- `npm run verify:ium5`: 24-Schritte-Regression einschließlich aller 19 Phase-1-Prüfschritte, vollständiger Python- und Plattformtests sowie IUM5-Browser-, Zustands-, Offline- und Accessibilityprüfungen.

Tests wurden mit Node 22/npm 10 geplant; der genaue verwendete Runtime-Stand und Ergebnisse stehen im Prüfbericht. Die bestehende Lernmodulvorschau wird durch den separaten Dashboard-Testport nicht ersetzt.
