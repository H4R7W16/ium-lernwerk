# LXF07 Validierungsbericht

## Prüfgegenstand und Commit

Prüfdatum: 5. September 2026. Gegenstand ist das produktneutrale Lern- und Experience-Fundament LXF01–LXF06 für Gymnasium Baden-Württemberg, Niveau E, Klassen 5–7. LXF06 wurde vom Nutzer ausdrücklich fachlich freigegeben; zugleich wurde LXF07 beauftragt.

Basiscommit: `beaba6d3382d60ef31b1171368e4580b2e1432b3`, Branch `feat/ium-v2-rebaseline`. Der exakte geprüfte Änderungsstand ist über `review.inputDigests` in [status.json](status.json) an sämtliche Pflichtartefakte, die Spezifikation und diesen Bericht gebunden. SHA-256 wird auf UTF-8-Dateiinhalten mit LF-Zeilenenden gebildet; reine Git-Zeilenendenkonvertierung verändert den Nachweis nicht. Der Commit, der Bericht und Status gemeinsam einführt, versioniert die Gesamtentscheidung. Der endgültige Hash wird im Vault-Handoff dokumentiert.

**Prüfart:** KI-gestützter Dokumentenselbstreview durch Codex. Quellenprüfung, Inhaltswalkthroughs und Prüfung der Accessibility-Anforderungen sind von automatisierten Vertrags- und Regressionstests getrennt. Die Rollen im Gateprotokoll bezeichnen die jeweils geprüfte Verantwortung; sie behaupten weder mehrere Personen noch eine unabhängige Fach-, Lehrkraft- oder Rechtsprüfung. Perspektivübernahmen sind keine Beobachtungen realer Lernender oder Lehrkräfte. Die abschließende Nutzerabnahme von LXF07 bleibt eine eigene Entscheidung.

### Spec-Coverage

| Vorgabe der freigegebenen Spezifikation | Implementierender Nachweis | Ergebnis im Fundamentumfang |
|---|---|---|
| 10.1 Vollständige Lernarchitektur einschließlich Lehrkraft | LXF04 `principleGroups`, LXF05 zehn Muster, LXF06 Orchestrierungsleitfaden | Material, Handlung, Repräsentation, Hilfe, Feedback, Zugang und Führung zusammengeführt. |
| 10.2 Quelle → Claim → Entscheidung → Prinzip | LXF02 23 Claims; LXF04 18 Prinzipien mit `claimIds`, `decisionBasis`, Kriterien und Methoden | Empirie und Projektentscheidung getrennt; Rückverfolgung vollständig. |
| 10.3 Quellenfamilien und begrenzte Übernahme | LXF01 33 Auditentscheidungen; LXF02 Synthese und Quellenregister | Keine pauschale Übernahme alter Standards; professionelle Guidance und normative Standards erkennbar. |
| 10.4 Varianz in Klassen 5–7 | LXF03 acht Dimensionen mit 16 Arbeitsannahmen, Curriculum-/Projektbezügen und offenen Fragen | Jahrgang ist Scope, kein Diagnosemerkmal; Annahmen bleiben `working`. |
| 10.5 Acht Qualitätsdimensionen | Acht LXF04-Prinzipiengruppen; Gatebezüge aus LXF06 | Jede Dimension besitzt operationalisierte Entscheidungen. |
| 10.6 Flexible Lernfunktionen und Interaktionszweck | Acht Funktionen, elf Übergänge, fünf Varianten, acht Interaktionsverträge; zehn LXF05-Muster | Kein universeller Seitenablauf; Handlung und Eigenleistung begründen Interaktion. |
| 10.7 Methodenspezifische Qualitätsgates | Zwölf LXF06-Definitionen, drei Walkthrough-Zuordnungen, ausgeführtes Protokoll unten | Pflichtnachweise dokumentiert; technische Prüfung ersetzt keinen fachlichen Befund. |
| 6 / 11 / 16 Getrennte Reife, öffentliche Aussagen und Pilotgrenze | Zentraler LXF07-Status, offene Fragen und Statusentscheidung | Höchstens Dokumentenreife `reviewed`; Produktfreigabe, Standard, Pilot und Wirkung bleiben ausgeschlossen. |

## Quellen- und Claim-Konsistenz

Alle 23 LXF02-Claims sind `reviewed`, referenzieren registrierte Quellen und trennen Aussage, Mechanismus, Lernendenkontext, Evidenzstufe und Grenzen. Alle 18 LXF04-Prinzipien sind `reviewed` und besitzen Claimbezüge; sämtliche 23 Claims werden mindestens einmal verwendet. Alle zehn freigegebenen Muster besitzen bekannte Prinzipienbezüge. Die zwölf Gates referenzieren zusammen alle 18 Prinzipien und zehn Muster. Der Validator prüft die Referenzketten und erkennt Änderungen am geprüften Bestand; die inhaltliche Tragfähigkeit wurde zusätzlich anhand der Entscheidungen und ihrer Gegenfälle geprüft.

Die entscheidenden Grenzen bleiben erhalten: Mathematikevidenz zu Worked Examples begründet keinen ungeprüften IuM-Effekt (`CLAIM-LP-004` → `LXF04-PR-007`); Hinweise auf Vorwissen erzeugen keine stabilen Personenprofile (`CLAIM-LP-002` → `LXF04-PR-003`); vorbereitete Exploration verlangt Anschlusswissen und Konsolidierung (`CLAIM-LP-012` → `LXF04-PR-009`). Segmentierung wird fachlich begründet statt durch Klickzahl; ICAP wird nicht zur Rangliste von Bedienaktivitäten. Rückmeldung verlangt Nutzung, Abruf unterscheidet sich von Wiederlesen, Transfer von kosmetischer Variation. Motivation und fachliches Lernen bleiben verschiedene Gegenstände.

### Aktualitätsprüfung der fortschreibbaren Quellen

Die in LXF02 ausdrücklich vor LXF07 verlangte Nachprüfung wurde am 5. September 2026 an den offiziellen Seiten durchgeführt. Sie betrifft Identität, Versionsstand und die für die Einordnung entscheidenden Aussagen; sie ist keine erneute vollständige Extraktion aller Primärstudien und keine neue Rechtefreigabe.

| Quelle | Befund der aktuellen Primärseite | Folge |
|---|---|---|
| [IBBW: Wirksamer Unterricht](https://ibbw-bw.de/,Lde/Startseite/Bildungsforschung/Publikationsreihe%2B_Wirksamer%2BUnterricht_) | Die Reihe ist erreichbar; Bände 1–12 einschließlich der verwendeten Themen werden aufgeführt. | Einordnung als praxisbezogene Forschungssynthese bleibt passend. |
| [W3C: Supplemental Guidance](https://www.w3.org/WAI/WCAG2/supplemental/) | Zusätzliche kognitive Accessibility-Guidance, ausdrücklich über die WCAG-Konformitätsanforderungen hinaus. | Guidance und normative Konformität bleiben getrennt. |
| [CAST: UDL Guidelines](https://udlguidelines.cast.org/) | Version 3.0 und Veröffentlichung am 30. Juli 2024 werden weiterhin ausgewiesen. | Planungsrahmen; keine behauptete IuM-Wirkungsprüfung. |
| [EEF: Metacognition and Self-Regulated Learning](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition) | Zweite Auflage vom 13. November 2025; fachliche und curriculare Einbettung wird hervorgehoben. | Die registrierte Ausgabe und begrenzte Einordnung bleiben passend. |
| [W3C: WCAG](https://www.w3.org/TR/wcag/) | Die aktuelle Fundstelle weist WCAG 2.2, Recommendation vom 12. Dezember 2024, aus. | Normative technische Baseline; keine Konformitätsaussage für ein noch nicht implementiertes V2-Produkt. |

Im geprüften Umfang ergibt sich kein Änderungsbedarf an den Claims. Vor öffentlicher Wiedergabe bleiben Locator-, Rechte- und Aktualitätsprüfungen erforderlich. Historische Zugriffszeitpunkte im Quellenregister werden durch diesen getrennt dokumentierten Recheck nicht als vollständige neue Quellenextraktion umgeschrieben.

## Fach- und Stufenpassung

LXF03 unterscheidet in allen acht Dimensionen evidenzgestützte Annahmen, curriculare oder projektbezogene Erwartungen und offene Jahrgangsfragen. Die 16 Annahmen bleiben `working`: Die Prüfung bestätigt ihre vorsichtige Planungsfunktion, nicht eine empirische Absicherung aller Übertragungen. Vorwissen, Sprache, Bedienung und Selbststeuerung werden aufgabenbezogen betrachtet. Die Lesehilfe für das Band 5/6 wird nicht in erfundene jahrgangsscharfe Kompetenzerwartungen übersetzt. Klasse 7 erhält kein pauschales Vorwissen allein aufgrund des Alters.

Die prüfbaren Verbindungen betreffen sowohl informatische Handlungen als auch Medienbildung: Beziehungen modellieren und ausführen, Repräsentationen vergleichen, Aussagen und Entscheidungen begründen, Ergebnisse überarbeiten. Ein technischer Output reicht nicht als Nachweis eines begründeten Urteils; ein beschreibender Text ersetzt nicht jede verlangte digitale Handlung. V2-Curriculumabdeckung bleibt `unassessed`.

**Befund LXF07-F01, geschlossen:** Die bisherige Datenschutz-Gatebedingung konnte einen fiktiven Ersatzfall pauschal als lernzielgleich erscheinen lassen. Das widerspricht `CUR-Q-002`, wenn der Eigenbezug selbst gefordert ist. `privacy-and-emotional-safety` und der Orchestrierungsfallback benennen nun ausdrücklich: Schutz zuerst, betroffener Eigenbezugsnachweis offen, kein behauptetes `covered`. CUR-Q-002 bleibt an Curriculum und Governance gebunden; hier wird keine Rechts- oder Erhebungsentscheidung getroffen.

## Lernarchitektur

Die acht Qualitätsdimensionen sind in 18 prüfbare Prinzipien übersetzt. Die fünf Varianten erlauben unterstützte Problemöffnung, frühe Erklärung, direkte Modellierung, verzögerten Abruf und Rückkehr zur Unterstützung. Ein neutraler Lernbogen kann Funktionen zusammenfassen oder begründet auslassen; die Liste verlangt keine acht nacheinander sichtbaren Oberflächenzustände.

Die Gegenprüfung bestätigt drei entscheidende Trennungen: Modellierung kann den gesamten Kernschritt zeigen, während die nachfolgende eigene Anwendung dessen Nachweis trägt. Eine Lernaufgabe erlaubt Hilfen, deren Einsatz eine Leistungsaufgabe unter anderen Bedingungen verändern würde. Unmittelbare Anwendung, späterer Abruf und Transfer benötigen unterschiedliche Produkte und Vergleichsbedingungen. Keine unbelegte universelle Alters-, Gruppen-, Seiten-, Element- oder Minutenregel wurde im aktiven Vertrag gefunden. Zahlen in IDs, Versionsangaben, Curriculumjahrgängen und gezählten Vertragsbestandteilen sind davon zu unterscheiden.

## Material- und Interaktionsmuster

Die zehn Muster führen Prinzipienbezug, Einsatzgrenzen, Pflicht-/Verbotelemente, beobachtbare Kriterien und fachliche Prüfmethoden zusammen. Die drei Gerüste sind keine verpflichtenden Gesamtkompositionen. Der Durchgang prüft jeweils die benötigte Funktion, damit die formale Vollständigkeit der Bibliothek nicht erneut eine überladene Gesamtoberfläche erzeugt.

Die Prüfung eines abstrakten Modulauftrags ist möglich: Anforderung und Zielbeziehung auswählen, erforderliches Produkt und Kriterium festlegen, passende Lernfunktionsvariante begründen, Muster bedarfsbezogen wählen, Hilfe und Zugang auf die Kernhandlung beziehen, Orchestrierung und Nachweise vorsehen. Ein daraus später entstehender Modulentwurf müsste seine eigene Curriculum-, Quellen-, Accessibility- und Nutzungsprüfung durchlaufen. Dieser Durchgang erzeugt weder Lernendentexte noch ein Referenzmodul und öffnet die Inhaltsproduktion nicht.

## Lehrkraftorchestrierung

Vorbereitung und Haltepunkte verbinden Produktlage, Beobachtungsfrage und Anschlussentscheidung. Kooperation verlangt individuellen Beitrag, Austauschfunktion, gemeinsames Minimalprodukt, Zwischenkontrolle, Zusammenführung und eigene Anschlussleistung. Verkürzte Zeit führt zu einer begründeten Reduktion oder Verteilung; eine entfallene Sicherung wird nicht als abgeschlossene Einheit gezählt.

**Befund LXF07-F02, geschlossen:** Die bisherige Orchestrierungs-Gatebedingung verlangte für jeden Ausfall pauschal eine gleichwertige Reaktion, obwohl der Leitfaden digitale oder kooperative Kernhandlungen im Ersatzpfad ausdrücklich als offen behandelt. Die Bedingung stimmt nun mit dieser Grenze überein: fachlich begründete Umsteuerung und späterer Nachweis statt fiktiv gleichwertigem Abschluss. Der Anspruch des betroffenen Lernziels bleibt erhalten.

Der WU-Abgleich folgt den bereits dokumentierten Exzerpten und Claims: Kognitive Aktivierung über Eigenleistung, Unterstützung an konkreten Hürden, Klassenführung über Anschlussentscheidungen, Feedback über Revision, Kooperation über fachlich verantwortete Beiträge. Reale Führbarkeit und Zeitbedarf sind weiterhin Pilotfragen.

## Accessibility, Datenschutz und Sicherheit

### Barriere-Funktions-Matrix

| Barriere oder Pfad | Erhaltene Funktion und Prüfgegenstand | Späterer fehlender Nachweis |
|---|---|---|
| Tastatur | Ziel, Material, Hilfe, Zustandswechsel und Revision sind ohne Zeigehandlung erreichbar; semantische Reihenfolge und Fokus bleiben nachvollziehbar. | Implementierte Fokusführung und vollständige Tastaturbedienung. |
| Touch | Auswahl und Änderung verlangen weder Mauspräzision noch Hoverwissen; gleicher Kernschritt und gleiche Kriterien. | Reale Zielgrößen, Gestenalternativen und Bedienbarkeit auf Schulgeräten. |
| Text / Assistive Technology | Bezeichner, Zustände und Beziehungen sind sprachlich oder strukturell zugänglich; Farbe trägt keine alleinige Fachinformation. | Semantik und tatsächliche Ausgabe mit Assistive Technology. |
| Print / kein JavaScript | Erklärung, Vergleich und begründete Revision bleiben soweit fachlich möglich erreichbar. | Digitale Ausführung oder Speicherung wird durch Papier nicht technisch nachgewiesen. |
| Alternative Ausdrucksform | Gemeinsame Kernleistung und Belegpflicht bleiben erhalten. | Reale Nutzbarkeit; ein anderes Lernziel ist kein gleichwertiger Pfad. |
| Fehlender Eigenbezug | Sachbezogener Schutzweg erlaubt Weiterarbeit ohne erzwungene Offenlegung. | Curricular erforderliche eigene Reflexion bleibt CUR-Q-002; keine fingierte Abdeckung. |

Der Dokumentenaudit bestätigt geplante Barrieren- und Funktionsbehandlung. Er beansprucht keine technische WCAG-Konformität und keine Rechtskonformität. Der Reviewbogen erfasst Aufgaben- und Artefaktmerkmale; Lernendenkennungen, Klickverläufe, Hilfenutzungsprofile, Rankings und private Medienbiografien werden nicht vorausgesetzt. IUM-V2-GOV muss Betrieb, Rechte, öffentliche Aussagen und die offenen Schutzfragen gesondert prüfen.

## Neutrale Walkthroughs

Die folgenden Gegenproben wurden am Entwurf durchgeführt. Sie verwenden symbolische Zielbeziehungen, keine fertigen Aufgaben oder hypothetischen Nutzerbeobachtungen.

### entry

**Regelfall:** Eine aufgabenbezogene Darstellung legt eine Zielbeziehung und den ersten eigenen Schritt fest. Aus Lernendensicht ist erkennbar, welches kleine Ausgangsprodukt benötigt wird; aus Lehrkraftsicht liefert dieses Produkt eine begründbare Entscheidung über Problemöffnung oder Modellierung. Belege: `LXF05-PT-001`, `LXF04-PR-003`, LXF06 „Auftakt und Wahl des fachlichen Wegs“.

**Gegenfall:** Das Ausgangsprodukt fehlt oder ist mehrdeutig. Die Lehrkraft darf daraus weder eine passende Voraussetzung noch ein Defizit ableiten. Die vorgesehene Ersatzsichtung beziehungsweise frühe Modellierung stellt den Anschluss her; aus Lernendensicht bleibt der nächste eigene Schritt erreichbar. Eine verlangte private Aussage wird unterbrochen; sachbezogene Weiterarbeit schreibt einen curricular nötigen Eigenbezug nicht als erfüllt fort. Ergebnis: `pass` im Dokumentenumfang nach F01.

### central-learning-action

**Regelfall:** Ein symbolischer Ausgangszustand, eine fachlich begründete Änderung und der Folgezustand werden vergleichbar gehalten. Die lernende Person erzeugt oder begründet die Änderung; ein Kriterium macht den Unterschied zwischen Ausführung und bloßem Kopieren sichtbar. Bei einer medienbezogenen Beurteilung entspricht dies einer begründeten Aussage mit tragendem Beleg, nicht bloß einer ausgewählten Option. Lehrkraft und Feedback adressieren dieselbe Produktstelle. Belege: `LXF04-PR-005` bis `-008`, `LXF05-PT-003`, `-004`, `-006`.

**Gegenfall:** Hilfe liefert die vollständige Lösung oder eine Person übernimmt den Beitrag der anderen. Der Vertrag verlangt Wechsel zur Modellierung oder reduzierte Hilfe, gefolgt von eigener Anwendung. Kooperation wird neu gerahmt; ein Partnerausfall hält einen eigenen Kernschritt offen erreichbar, ersetzt aber keine ausdrücklich kooperative Kompetenz. Eine nur farblich erkennbare Zustandsänderung fällt im Dokumentenaudit durch und verlangt zusätzliche Bezeichner. Ergebnis: `pass` für die vorgesehene Fehlerreaktion nach F02; keine Behauptung tatsächlich gelungener Eigenleistung.

### securing-and-reentry

**Regelfall:** Gesicherte Zielbeziehung, offener Punkt und nächste Handlung bleiben unterscheidbar. Aus Lernendensicht lässt sich nach einer Unterbrechung anschließen; die Lehrkraft kann einen späteren aktiven Abruf vor vollständiger Wiederanzeige ermöglichen. Belege: `LXF05-PT-007` bis `-009`, `LXF04-PR-014`, LXF06 Sicherung und Fallbacks.

**Gegenfall:** Das Produkt ist verloren oder die Wiederanzeige wird als Abruf gewertet. Der Entwurf benennt Verlust und begrenzte Rekonstruktion beziehungsweise Nachsicherung. Anschließend wird ein tatsächlicher Abruf separat geplant. Ein kosmetisch veränderter Gegenstand zählt nicht als Transfer; veränderte Bedingung und erhaltenes Prinzip müssen benannt sein. Ergebnis: `pass` im Dokumentenumfang. Wiederherstellung auf Geräten und tatsächliches Behalten bleiben offen. Die bei LXF05 genannte spätere Methode `usability-test` wird durch diesen Inhaltswalkthrough nicht als ausgeführt verbucht.

### Ausgeführtes Vorproduktions-Gateprotokoll

Alle Ergebnisse betreffen den abgegrenzten Dokumentenstand. „Pass“ bewertet die konkrete Entwurfslogik mit Beleg und Gegenfall. Es ist keine Freigabe aus Testergebnissen. Die vollständigen Einträge mit Rolle, Fundstelle, Beobachtung, Methode und Aussagegrenze stehen zusätzlich in `status.json`.

| Gate | Methode und verantwortliche Prüffunktion durch Codex | Befund / tragender Beleg | Ergebnis |
|---|---|---|---|
| evidence-integrity | Quellenreview; source-reviewer | 23 Claims mit Grenzen; vollständige Kette zu 18 Prinzipien und zehn Mustern; fünf aktuelle institutionelle Seiten nachgeprüft. | pass |
| goal-action-evidence-alignment | Inhaltswalkthrough; subject-didactics-reviewer | Einstieg und zentrale Handlung verbinden Zielbeziehung, eigenes Produkt und Kriterium; Produktabweichung steuert Anschluss. | pass |
| cognitive-economy | Inhaltswalkthrough; subject-didactics-reviewer | Fachliche Segmente und benötigte Funktionen; keine Pflicht zur vollständigen Musterfolge und keine unbelegte Universalmenge. | pass |
| disciplinary-learning-action | Inhaltswalkthrough; subject-didactics-reviewer | Eigene Ausführung, Erklärung oder Revision; Kopieren und Auswahl allein bestehen die Gegenprobe nicht. | pass |
| representation-coherence | Inhaltswalkthrough; subject-didactics-reviewer | Ausgangs-/Folgezustände, konsistente Bezeichner und lernrelevante Zuordnung; Farballeinigkeit fällt durch. | pass |
| support-without-task-removal | Inhaltswalkthrough; subject-didactics-reviewer | Hürde, Rücknahmepunkt und neue Eigenleistung; vollständige Lösung wird als Modellierung getrennt. | pass |
| feedback-and-next-action | Inhaltswalkthrough; subject-didactics-reviewer | Kriterium, Produktstelle und nutzbare Revision; Abruf und Transfer besitzen eigene Nachweisbedingungen. | pass |
| orientation-and-recovery | Inhaltswalkthrough; teacher-reviewer | Erhaltener und verlorener Stand führen zu unterschiedlicher Wiederaufnahme; keine verlustfreie Funktion behauptet. | pass |
| accessibility-and-equivalence | Anforderungs-/Äquivalenzaudit und Inhaltswalkthrough; accessibility-reviewer | Barriere-Funktions-Matrix oben; Pflichtfunktion bleibt erhalten oder ihr Nachweis offen. | pass |
| teacher-orchestration | Inhaltswalkthrough; teacher-reviewer | Produktbezogene Haltepunkte, Zeitvarianten, individuelle Beiträge und ehrliche Ausfallfolge nach F02. | pass |
| privacy-and-emotional-safety | Inhaltswalkthrough; privacy-reviewer | Keine Telemetrie oder öffentliche Labels; Eigenbezugsgrenze nach F01 erhält CUR-Q-002 ausdrücklich offen. | pass |
| pilot-boundary | Inhaltswalkthrough; integration-reviewer | Versioniertes Protokoll, offen ausgewiesener Selbstreview und zugeordnete reale Folgeprüfungen. | pass |

## Offene Pilotfragen

| Frage / Bezug | Zuständigkeit und Auslöser | Risiko und aktuelle Folge |
|---|---|---|
| LXF03-Q-001 / -002: Vorwissen, Sprache und Modellierung je Jahrgang | Fachplanung in IUM-V2-R5/R6/R7; Beobachtung erst im gesondert freigegebenen Pilot | Keine festen Eingangsniveaus oder Sprachmengen ableiten. |
| LXF03-Q-003: Informationsdichte und Segmentierung | Materialreview am späteren konkreten Referenzmaterial, danach Nutzungsprüfung | Muster enthalten keine erwiesenen Alterslimits. |
| LXF03-Q-004: Bedienroutinen | Technik-/Accessibility-Verantwortung am implementierten Produkt | Gerätefunktion und technischer Fallback bleiben ungetestet. |
| LXF03-Q-005 / -006: Strategien, Hilfen und sinnvolle Wahl | Fach-/Lehrkraftreview des späteren Lernbogens, anschließend Pilot | Keine Wirkung oder stabile Selbstregulation aus dem Entwurf ableiten. |
| LXF03-Q-007: Barrieren und gleichwertige Ausdruckswege | Accessibility- und Nutzungsprüfung am konkreten Produkt | Geplante Äquivalenz ist keine reale Zugänglichkeit. |
| LXF03-Q-008: Kooperation, Haltepunkte und Aufwand | Verantwortliche Lehrkraft im gesondert freigegebenen Unterrichtspilot | Führbarkeit, Wechselzeiten und Rollennutzung noch unbekannt. |
| CUR-Q-002: Persönliche Reflexion ohne erzwungene Offenlegung | IUM-V2-CUR mit IUM-V2-GOV vor betroffener Modulspezifikation | Kein fiktiver Ersatz als Nachweis des Eigenbezugs; Abdeckung offen. |
| CUR-Q-003: Fachliche Balance und Progression in Klasse 7 | IUM-V2-R7 nach den vorgeschalteten Gates | Ein Einzelmodul belegt keine Jahrgangsprogression. |
| Wiederholte Bewährung, verzögerter Abruf und Transfer | Spätere Pilotverantwortung nach gesondertem Design und Freigabe | Kein Standard- oder Lernwirkungsnachweis vorhanden. |

Diese Fragen verhindern unzulässige weitergehende Aussagen. Sie verschieben keine fehlende aktuelle Pflichtfunktion: F01/F02 wurden jetzt korrigiert, anstatt die widersprüchlichen Gatebedingungen nur als Pilotfrage zu vertagen. Für ein konkretes Modul mit curricular nötigem Eigenbezug bleibt CUR-Q-002 ein eigenständiger Blocker.

## Statusentscheidung

Die fachliche Dokumentenprüfung ist abgeschlossen; alle zwölf Vorproduktionsgates bestehen im angegebenen Umfang. Zwei Widersprüche der Gateformulierungen wurden nachgearbeitet und erneut gegen die neutralen Gegenfälle geprüft. Es bleibt kein struktureller Blocker des allgemeinen Fundamentvertrags. Eine unabhängige Gegenprüfung und die abschließende fachliche Nutzerabnahme von LXF07 werden nicht behauptet.

Die vollständig bestandene technische Verifikation erlaubt die atomare Statusentscheidung im selben Commit wie dieser Bericht: `concept: reviewed` und `workStatus: done` bezeichnen den abgeschlossenen Fundament-Dokumentenreview. Sie bedeutet keine Produktfreigabe. `pilot: not-started`, `standardization: not-eligible`, `contentProduction: frozen` und `release: closed` bleiben verbindlich. Die LXF06-Datei hält weiterhin Gatedefinitionen mit `executionStatus: not-run`; die tatsächlich ausgeführte Gesamtprüfung wird ausschließlich im getrennten LXF07-Protokoll geführt.

Der operative Vault-Task bleibt bis zur Nutzerabnahme in `review`. IUM-V2-GOV darf erst nach ausdrücklicher LXF07-Nutzerfreigabe beginnen. V2 bleibt `building`, aktive Baseline V1; Inhaltsproduktion, LXP05, Pilot, Veröffentlichung und Cutover werden nicht geöffnet.

### Technische Verifikation

Alle verlangten Prüfungen sind am geprüften Änderungsstand bestanden:

| Prüfung | Ergebnis |
|---|---|
| Fokussierte V2-Vertragstests | 167 bestanden, darunter 18 LXF07-Tests. |
| Gesamte Python-Regression | 842 bestanden, zuletzt innerhalb beider vollständigen Prüfketten. |
| Typecheck und Astro-Check | Bestanden, keine Typecheck-/Astro-Fehler. |
| Plattformtests | 132 Tests in 25 Dateien bestanden. |
| `npm run verify:phase1` | 19/19 Schritte bestanden, einschließlich Browser-, Offline- und Accessibility-Prüfungen. |
| `npm run verify:ium5` | 24/24 Schritte bestanden; modulspezifisch 39 Browser-, vier Zustands-, drei Offline- und zwölf Accessibility-Tests. |
| `npm run verify:v2` | Bestanden; Statusentscheidung und Berichtbindung werden vor Commit erneut geprüft. |
| LXF06-Schema-Instanzprüfung | Geänderte Gates mit AJV Draft 2020-12 unabhängig vom Python-Validator geprüft. |
| `git diff --check` | Bestanden. |

Die ersten 15 LXF07-Tests scheiterten vor Implementierung am fehlenden Releasevalidator beziehungsweise fehlender Repositoryanbindung; danach bestanden sie. Drei zusätzliche Negativ-/Portabilitätsprüfungen sichern nicht freigegebene Claims/Prinzipien/Muster trotz erneuerter Hashes, Pflichtmethoden und reine Git-Zeilenendenkonvertierung.

Anfangs wurden Plattformläufe ohne abschließendes Ergebnis unterbrochen. Ein isolierter Vertragstest, ein direkter Astro-Build und ein isolierter Buildtest bestanden; danach bestanden der komplette Plattformlauf und beide unveränderten vollständigen Prüfketten. Ein fortbestehender Produktfehler wurde nicht reproduziert; die anfängliche Verzögerung ist nicht als geklärter Codefehler ausgewiesen. Es wurde keine Testkonfiguration oder V1-Produktion geändert.

Vollständige lokale Logs liegen außerhalb des Repositorys und Vaults unter `_Transfer/IuM-LXF07/verify-phase1.log` und `verify-ium5.log`. Automatisierung prüft Verträge, Statusgrenzen und Regressionen; sie bewertet weder die Wahrheit von Freitextbefunden noch Lernwirksamkeit. Die Produktregressionen betreffen den bestehenden V1/IUM5-Code und sind keine Ausführung eines V2-Unterrichtspiloten.
