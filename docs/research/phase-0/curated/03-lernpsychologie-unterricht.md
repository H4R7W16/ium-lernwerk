---
package: lernpsychologie-unterricht
status: curated
curated: 2026-07-28
source: ../raw/03-lernpsychologie-unterricht.md
---

# Lernpsychologie und Unterrichtswissenschaft für IuM 5–7

## Scope und Quellenqualität

Dieses Paket kuratiert Lernpsychologie und Unterrichtswissenschaft für ein digitales, lehrkraftorchestriertes Lernwerk am Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E, und damit für Lernende im Alter von etwa 10 bis 13 Jahren. Es leitet keine allgemeine Rangliste von Methoden ab. Unmittelbarer Lernerfolg, verzögertes Behalten und Transfer bleiben getrennte Outcomes; Effektangaben werden nur zusammen mit Design, Population, Vergleich, Messung, Moderatoren und Grenzen verwendet.

Der feste Quellenkern umfasst dreizehn wissenschaftliche Original-/Publisherquellen und die offizielle IBBW-Publikationsreihe als einen professionellen lokalen Syntheserahmen. Die IBBW-Bände 1, 3, 6 und 9 strukturieren das Zusammenspiel von Tiefenstrukturen, konstruktiver Unterstützung, Aufgabenqualität und digitaler Medienfunktion. Sie werden nicht als zusätzliche unabhängige kausale Wirksamkeitsnachweise gezählt.

Die Meta-Analysen zu Vorwissen, worked examples, Selbsterklärung, Scaffolding, Abruf, Spacing, Transfer, Feedback und Problem Solving before Instruction mischen Fächer und Altersgruppen. Nur Teilmengen liegen nahe an der Zielgruppe. Jede Übertragung auf Informatik und Medienbildung ist deshalb eine zu prüfende Projektinferenz. Der feste Kern enthält keine belastbare Synthese zu einer bestimmten Selbstregulationsintervention in IuM 5–7; diese Lücke wird nicht durch Motivations- oder Feedbackforschung verdeckt.

Die ergänzte Selbstregulationsmeta-Analyse untersucht explizite Trainings in realen Grundschulklassen, schließt computerbasierte Interventionen aber aus. Sie schließt damit eine allgemeine Evidenzlücke für jüngere Lernende, nicht die spezifische Lücke für digitale IuM-Settings der Klassen 5–7.

Alle dreizehn retained Claims stehen im `claim-ledger.json` auf `reviewed`; keiner ist `standard`.

## Errata zum versiegelten Rohbericht

Der Rohbericht bleibt als Provenienzartefakt bytegenau unverändert. Für die Kuration gelten folgende Korrekturen:

- **Selbstregulation.** Der Raw nennt fälschlich DOI `10.1007/s10648-008-9088-4` und leitet daraus eine allgemeine Forschungslücke ab. Richtig ist Dignath, Büttner und Langfeldt (2008), *How can primary school students learn self-regulated learning strategies most effectively? A meta-analysis on self-regulation training programmes*, DOI [`10.1016/j.edurev.2008.02.003`](https://doi.org/10.1016/j.edurev.2008.02.003). Die falsche Lückenfolgerung wird durch CLAIM-LP-013 ersetzt; offen bleibt nur die Übertragung auf digitale IuM-Settings und Klasse 7.
- **Raw-Bibliografie.** Der exakte Belland-Titel lautet *Synthesizing Results From Empirical Research on Computer-Based Scaffolding in STEM Education: A Meta-Analysis*. Beim Signaling-Beitrag ist der Erstautor vollständig als Sascha V. Schneider zu führen; Titel und Reihenfolge lauten *A meta-analysis of how signaling affects learning with media*, Sascha V. Schneider, Maik Beege, Steve Nebel und Günter Daniel Rey. Die weiteren im Review festgestellten Namens- und Titelabweichungen lagen im Quellenregister und sind dort gegen DOI-/Publishermetadaten korrigiert.

## Retained Claims

### CLAIM-LP-001 – Unterricht über Lernhandlungen und Tiefenstrukturen orchestrieren

**Befund.** Der offizielle IBBW-Syntheserahmen ordnet Unterrichtsqualität nicht primär nach Methode oder Medium, sondern nach der Qualität von kognitiver Aktivierung, konstruktiver Unterstützung und Klassenführung; Aufgaben und digitale Medien erhalten ihren Wert erst über die dadurch ermöglichten Lernprozesse.

**Evidenz.** Die offizielle Publikationsseite bestätigt den Wissenschaftstransfercharakter und die Bände 1, 3, 6 und 9. [Offizielle Quelle](https://ibbw-bw.de/%2CLde/Startseite/Bildungsforschung/Publikationsreihe%2B_Wirksamer%2BUnterricht_)

**Scope und Einschränkungen.** Professioneller Syntheserahmen für Unterrichtspraxis aller Schularten. Er ist weder eine einheitliche Interventionsmeta-Analyse noch ein domänenspezifischer Wirksamkeitsnachweis für IuM 5–7.

**IBBW-Abgleich.** Direkt abgedeckt durch Band 1, 3, 6 und 9. Die Aussage beschreibt die IBBW-Synthese; kausale Einzelmechanismen werden in den folgenden Claims an Originalforschung geprüft.

**Betroffene Modulphasen.** 4.1 Orientierung und Herausforderung; 4.2 Vorwissen aktivieren; 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Jede Aktivität benennt Ziel, fachliche Lernhandlung, Unterstützung, Rückmeldung und Sicherung. Digital bleibt Primärmedium, wird aber nur eingesetzt, wenn es eine dieser Funktionen besser erfüllt. Eine analoge Variante entsteht nur bei eigener Lernfunktion.

### CLAIM-LP-002 – Vorwissen aufgabenbezogen aktivieren, nicht als Schicksal behandeln

**Befund.** Domänenspezifisches Vorwissen sagt spätere Wissensstände deutlich voraus, den normalisierten Wissenszuwachs im Mittel jedoch kaum; die Beziehung zwischen Vorwissen und Lernen variiert stark.

**Evidenz.** Simonsmeier und Kolleginnen und Kollegen meta-analysierten 8.776 Effektgrößen. Die Stabilität individueller Unterschiede lag bei `r = .534`, die Beziehung von Vorwissen zu normalisiertem Wissenszuwachs bei `r = -.059` mit breitem Vorhersageintervall. [Originalquelle](https://doi.org/10.1080/00461520.2021.1939700)

**Scope und Einschränkungen.** Verschiedene Altersgruppen und Domänen; überwiegend Zusammenhänge, keine direkte Evaluation einer Vorwissensphase für IuM 5–7. Eine falsche Antwort belegt kein stabiles Fehlkonzept.

**IBBW-Abgleich.** Band 1 und Band 3 unterstützen die Berücksichtigung von Lernvoraussetzungen als professionellen Syntheserahmen. Der quantitative Befund stammt aus der Originalmeta-Analyse, nicht aus IBBW.

**Betroffene Modulphasen.** 4.2 Vorwissen aktivieren; 4.3 Konzept aufbauen; 4.4 Angeleitet erproben.

**Designfolge und Medium.** Kurze Vorhersagen, Skizzen, Code- oder Medienbeispiele und Modellvergleiche aktivieren Vorwissen lokal. Ergebnisse werden nicht zentral gespeichert und erzeugen keine dauerhaften Fehlvorstellungsprofile. Analog ist sinnvoll, wenn freies Skizzieren oder räumliches Ordnen die Vorstellung unverstellter sichtbar macht.

### CLAIM-LP-003 – Kognitive Last als Gestaltungsrahmen, nicht als Lernwert verwenden

**Befund.** Cognitive Load Theory begründet, warum Aufgabe, Vorwissen, Darstellung und Lernumgebung gemeinsam betrachtet werden müssen: unnötige Verarbeitung soll reduziert und verfügbare Verarbeitung auf lernrelevante Beziehungen gelenkt werden; Unterstützung kann mit wachsender Expertise redundant werden.

**Evidenz.** Paas und van Merriënboer fassen Cognitive Load Theory und Methoden zur Steuerung von Arbeitsgedächtnisbelastung bei komplexen Aufgaben zusammen. [Originalquelle](https://doi.org/10.1177/0963721420922183)

**Scope und Einschränkungen.** Forschungsüberblick, keine Meta-Effektzahl für ein bestimmtes Design. Subjektive mentale Anstrengung, Bearbeitungszeit oder Bedienleichtigkeit sind keine Lernoutcomes. Die IuM-Übertragung ist inferenziell.

**IBBW-Abgleich.** Band 6 stützt die Prüfung von Zieltreffer und Nebenlast, Band 9 die Funktionsprüfung digitaler Medien. CLT liefert den theoretischen Originalrahmen; IBBW operationalisiert ihn nicht als eigenständigen Effektbeleg.

**Betroffene Modulphasen.** 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren.

**Designfolge und Medium.** Zusammengehörige Informationen werden integriert, Bedien- und Suchlast reduziert und Repräsentationen konsistent gehalten. Digital ist besonders begründet für veränderliche Zustände, Testfälle und synchrone Repräsentationen; Papier kann bei komplexen Skizzen oder räumlicher Übersicht entlasten.

### CLAIM-LP-004 – Worked examples aktiv verarbeiten und domänennah ausblenden

**Befund.** Worked examples verbesserten in einer Mathematikmeta-Analyse die Leistung gegenüber Vergleichsbedingungen im Mittel; daraus folgt weder passive Beispielbetrachtung noch ein universelles Fadingrezept.

**Evidenz.** Barbieri und Kolleginnen und Kollegen integrierten 43 Artikel mit 55 Studien und 181 Effekten von Primarstufe bis Hochschule und berichteten `g = 0.48`. [Originalquelle](https://doi.org/10.1007/s10648-023-09745-1)

**Scope und Einschränkungen.** Mathematik, heterogene Altersgruppen, Beispieltypen und Outcomes. Korrekte Beispiele waren im Mittel günstiger; Selbsterklärung war in dieser Synthese kein pauschal positiver Zusatzmoderator. Die Effektzahl ist nicht auf Programmier- oder Medienproduktionsaufgaben übertragbar.

**IBBW-Abgleich.** Band 6 unterstützt Beispiele als Aufgaben mit klarer fachlicher Handlung, Band 3 die dosierte Unterstützung. Die Wirksamkeitsaussage stammt aus der Mathematikmeta-Analyse.

**Betroffene Modulphasen.** 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren.

**Designfolge und Medium.** Lernende sagen Beispielschritte voraus, markieren Begründungen, vergleichen Varianten, ergänzen Lücken und testen Änderungen. Fading führt von vollständigem Beispiel über gezielte Lücken und Modifikation zur Eigenkonstruktion und wird im IuM-Pilot geprüft.

### CLAIM-LP-005 – Selbsterklärung gezielt prompten und fachlich prüfbar machen

**Befund.** Induzierte Selbsterklärung zeigt über unterschiedliche Aufgaben und Bildungsstufen im Mittel positive Lernoutcomes, ist aber kein automatischer Zusatznutzen unabhängig von Prompt und Aufgabe.

**Evidenz.** Bisra und Kolleginnen und Kollegen integrierten 69 Effekte aus 64 Berichten und berichteten `g = 0.55`; sie kodierten unter anderem Aufgabe, Fach, Bildungsstufe, Promptart und Dauer als Moderatoren. [Originalquelle](https://doi.org/10.1007/s10648-018-9434-x)

**Scope und Einschränkungen.** Heterogene Fächer, Altersgruppen und Promptformen. Die worked-example-Meta-Analyse zeigt, dass zusätzliche Selbsterklärungsprompts in einem engeren Kontext auch ungünstig moderieren können. Häufige generische „Warum?“-Fragen sind nicht belegt.

**IBBW-Abgleich.** Band 6 deckt Erklären und Begründen als fachliche Lernhandlungen ab, Band 3 die passende Unterstützung. Der quantitative Befund stammt aus Originalforschung.

**Betroffene Modulphasen.** 4.2 Vorwissen aktivieren; 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Wenige fachlich fokussierte Prompts verlangen kausale Beziehung, Vorhersage, Begründung oder Reparatur. Digitale Antworten werden lokal verarbeitet oder im Gespräch genutzt; es entsteht kein automatisches Persönlichkeits- oder Kompetenzprofil.

### CLAIM-LP-006 – Scaffolds an Hürden koppeln; Fading nicht automatisieren

**Befund.** Computerbasiertes Scaffolding unterstützt in problemzentrierten STEM-Settings kognitive Outcomes im Mittel; die Evidenz zeigt jedoch keine robuste Überlegenheit einer bestimmten Anpassungs- oder Fadinglogik.

**Evidenz.** Belland und Kolleginnen und Kollegen meta-analysierten 144 experimentelle Studien mit 333 Outcomes von Primarstufe bis Erwachsenenbildung und berichteten `g = 0.46`. [Originalquelle](https://doi.org/10.3102/0034654316670999)

**Scope und Einschränkungen.** Heterogene STEM-Domänen und Bildungsstufen; der stärkste Effekt trat bei Erwachsenen auf. Kontextbezug sowie Vorhandensein und Logik von Veränderung/Fading moderierten den Effekt nicht robust. Keine spezifische Evidenz für IuM 5–7.

**IBBW-Abgleich.** Band 3 deckt Scaffolding, Lernhürden und Rücknahme von Hilfen als professionelle Synthese ab; Band 6 schützt die anspruchsvolle Kernhandlung. Die Effektgröße stammt aus der Originalmeta-Analyse.

**Betroffene Modulphasen.** 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen.

**Designfolge und Medium.** Hilfen klären Ziel, lenken Aufmerksamkeit, bieten Teilbeispiele oder Prüffragen und erhalten die zentrale Entscheidung. Fading folgt sichtbarer fachlicher Bewältigung, nicht Zeit, Klickzahl oder zentraler Telemetrie. Lehrkräfte orchestrieren zusätzliche Hilfen über Beobachtung und Produkte.

### CLAIM-LP-007 – Retrieval Practice als Abruf mit Rückmeldung gestalten

**Befund.** Classroom Quizzing verbessert gegenüber Wiederlernen und anderen Vergleichsstrategien akademische Leistung im Mittel; Nutzen hängt von Aufgabe, Vergleich, Wiederholung, Feedback und Testpassung ab.

**Evidenz.** Yang und Kolleginnen und Kollegen integrierten 222 unabhängige Studien mit 48.478 Lernenden und berichteten `g = 0.499`. [Originalquelle](https://doi.org/10.1037/bul0000309)

**Scope und Einschränkungen.** Viele Bildungsstufen, Fächer, Formate und Messzeitpunkte. Der Gesamtwert sagt nichts über eine konkrete IuM-Aufgabe aus. Retrieval ist aktiver Abruf, nicht Wiederlesen, Wiederanschauen oder bloßes Wiederholen eines bereits sichtbaren Schritts.

**IBBW-Abgleich.** Band 9 nennt digitale Abrufübungen als mögliche Medienfunktion; Band 6 verlangt Zielpassung. Die Wirksamkeitsaussage stammt aus der Originalmeta-Analyse.

**Betroffene Modulphasen.** 4.2 Vorwissen aktivieren; 4.4 Angeleitet erproben; 4.6 Prüfen, überarbeiten und übertragen; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Kurze, niedrigschwellige Abrufe verlangen Rekonstruktion, Vorhersage, Erklärung oder Anwendung und erhalten korrigierendes Feedback. Digital ermöglicht unmittelbare Testfälle und Varianten; Antworten bleiben lokal und werden nicht bewertet oder profiliert.

### CLAIM-LP-008 – Übung über relevante Zeitabstände verteilen

**Befund.** In curriculumsnahen Klassenzimmerstudien war verteiltes Üben massiertem Üben im Mittel überlegen, besonders für verzögerte Messungen; die genaue Terminierung bleibt kontextabhängig.

**Evidenz.** Mawson und Kang integrierten 22 Berichte mit 31 Effekten und mehr als 3.000 Lernenden und berichteten `d = 0.54`, 95%-KI `[0.31, 0.77]`. [Originalquelle](https://doi.org/10.3390/bs15060771)

**Scope und Einschränkungen.** Die Zahl der Studien begrenzte Moderatoranalysen. Größere Effekte waren tendenziell mit höherer Bildungsstufe, längerem Behaltensintervall und weniger Wiederexpositionen verbunden. Komplexe IuM-Inhalte und 10- bis 13-Jährige sind nicht separat abgesichert.

**IBBW-Abgleich.** Band 6 ordnet Üben als Aufgabenfunktion ein; Band 9 kann digitale Organisation begründen. Der quantitative Spacing-Befund stammt aus Originalforschung.

**Betroffene Modulphasen.** 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Zentrale Konzepte kehren in späteren Modulen mit Abstand und veränderter Lernhandlung wieder. Digital organisiert curriculare Wiedervorlagen, ohne personenbezogene Erinnerungsprofile; eine analoge Wiederaufnahme ist sinnvoll, wenn sie dieselbe fachliche Rekonstruktion besser trägt.

### CLAIM-LP-009 – Transfer eigens entwerfen und prüfen

**Befund.** Retrieval Practice kann Transfer gegenüber nicht-testender Wiederexposition unterstützen; positiver Transfer ist aber stark von Elaboriertheit, Antwortbeziehung und initialem Abruf abhängig und nicht automatisch.

**Evidenz.** Pan und Rickard integrierten 192 Transfereffekte aus 122 Experimenten mit `N = 10.382` und berichteten `d = 0.40`, 95%-KI `[0.31, 0.50]`. [Originalquelle](https://doi.org/10.1037/bul0000151)

**Scope und Einschränkungen.** Mehr als 40 Jahre heterogener Forschung. Bias-Modelle reduzierten Intercepts teils bis auf keinen positiven Transfer, wenn relevante Moderatoren fehlten. Die Transferart muss benannt werden; Oberflächenvariation genügt nicht.

**IBBW-Abgleich.** Band 6 stützt Anwenden und Überprüfen als Aufgabenfunktionen. Der spezifische Retrieval-Transfer-Befund stammt aus Originalforschung und ist in IBBW nicht eigenständig quantifiziert.

**Betroffene Modulphasen.** 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Transferaufgaben variieren Repräsentation, Oberfläche oder Anwendungskontext, verlangen aber dasselbe fachliche Prinzip. Unmittelbarer Lernerfolg, späteres Behalten und Transfer erhalten getrennte Kriterien und Messzeitpunkte.

### CLAIM-LP-010 – Feedback nach Informationsfunktion und Aufgabe differenzieren

**Befund.** Feedback zeigt im Mittel positive, aber extrem heterogene Lernoutcomes; Informationsgehalt, Outcome, Design und Kontext unterscheiden die Effekte, und ein relevanter Anteil ist negativ.

**Evidenz.** Wisniewski, Zierer und Hattie integrierten 994 Effekte aus 435 Studien mit etwa 61.000 Personen. Der unbereinigte gewichtete Mittelwert lag bei `d = 0.55`; 17 % der Effekte waren negativ und die Heterogenität betrug `I² = 86.47 %`. Nach Ausschluss von 35 extremen Effekten lag der gewichtete Mittelwert bei `d = 0.48`, 95%-KI `[0.44, 0.51]`. [Originalquelle](https://doi.org/10.3389/fpsyg.2019.03087)

**Scope und Einschränkungen.** Viele Fächer, Altersstufen, Designs und Feedbackarten; Median des Publikationsjahrs 1985, asymmetrische Effektverteilung. Ein Gesamtwert erlaubt keine universelle Regel zu Timing, Kanal oder Form.

**IBBW-Abgleich.** Band 3 deckt formatives Feedback und nächste Lernschritte ab, Band 6 die Passung zur Aufgabe. Die heterogene Effektverteilung stammt aus der Originalmeta-Analyse.

**Betroffene Modulphasen.** 4.2 Vorwissen aktivieren; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Rückmeldung benennt am Produkt, an der Strategie oder am nächsten Prüfschritt nutzbare Information. Sicherheitsrelevante Fehlentscheidungen werden rasch korrigiert; reversible Lösungswege können vor Feedback erst erklärt und verglichen werden. Lob, Punkte und Ranglisten ersetzen keine Information.

### CLAIM-LP-011 – Autonomieunterstützung mit klarer Struktur verbinden

**Befund.** Autonomieunterstützung und Struktur sind keine Gegensätze: Sie treten positiv miteinander auf und sind beide mit Motivation, Engagement und Bedürfnisbefriedigung verbunden.

**Evidenz.** Patzak und Zhang synthetisierten 94 Studien und 110 Effektgrößen zur Beziehung von Autonomieunterstützung und Struktur. Der mittlere Zusammenhang war positiv, aber extrem heterogen (`I² = 98.94 %`); acht Studien berichteten negative Beziehungen. [Originalquelle](https://doi.org/10.1007/s10648-025-09994-2)

**Scope und Einschränkungen.** Überwiegend korrelative Daten, eine sehr große PISA-Stichprobe, verschiedene Schulstufen, Fächer, Kulturen und Erhebungsmethoden. Die Beziehung war in der Primarstufe kleiner (`r = .29`) als in der Sekundarstufe (`r = .56`) und variierte nach Erhebungsmethode: Schülerberichte, Lehrkraftberichte und Beobachtungen ergaben unterschiedlich starke Zusammenhänge. Nach Kontrolle des jeweils anderen Konstrukts wurden die Beziehungen zu Lernoutcomes kleiner. Daraus folgen weder eine robuste Synergie noch eine generelle kausale Leistungswirkung oder eine Begründung für Gamification beziehungsweise freie Wahl ohne Leitplanken.

**IBBW-Abgleich.** Band 3 deckt motivational-emotionale und methodisch-didaktische Unterstützung ab, Band 1 klare Klassenführung. Die statistischen Zusammenhänge stammen aus der Originalmeta-Analyse.

**Betroffene Modulphasen.** 4.1 Orientierung und Herausforderung; 4.4 Angeleitet erproben; 4.5 Eigenständig handeln oder produzieren; 4.6 Prüfen, überarbeiten und übertragen.

**Designfolge und Medium.** Lernende erhalten sinnvolle Entscheidungen über Beispiel, Strategie oder Produkt innerhalb klarer Ziele, Kriterien, Zeitrahmen und Hilfemöglichkeiten. Selbstregulation wird als Planen, Prüfen und Revidieren sichtbar, nicht als angenommene Eigenschaft einer angenehmen Oberfläche.

### CLAIM-LP-012 – Vorbereitete Exploration nur mit anschließender Instruktion einsetzen

**Befund.** Problem Solving before Instruction war Instruction before Problem Solving im Mittel überlegen, wenn die Exploration die Bedingungen von Productive Failure erfüllte; für jüngere Lernende und domänenübergreifende Fähigkeiten zeigte sich teils die Gegenrichtung.

**Evidenz.** Sinha und Kapur integrierten 53 Studien mit 166 Vergleichen und berichteten `g = 0.36`, 95%-KI `[0.20, 0.51]`. [Originalquelle](https://doi.org/10.3102/00346543211019105)

**Scope und Einschränkungen.** Überwiegend Mathematik, Klassen 6–10 und Hochschule. Bei Klassen 2–5 sowie domänenübergreifenden Fähigkeiten tendierten Effekte zugunsten I-PS. Der Befund gilt nicht für unbegleitetes Entdecken und nicht ohne anschließende konsolidierende Instruktion.

**IBBW-Abgleich.** Band 1 und Band 6 stützen Herausforderung und kognitive Aktivierung, Band 3 die Erreichbarkeit durch Unterstützung. Die spezifische PS-I-Wirkung stammt aus der Originalmeta-Analyse; die vier betrachteten IBBW-Bände decken Productive Failure nicht als eigene Effektquelle ab.

**Betroffene Modulphasen.** 4.1 Orientierung und Herausforderung; 4.2 Vorwissen aktivieren; 4.3 Konzept aufbauen; 4.4 Angeleitet erproben; 4.7 Gemeinsam sichern.

**Designfolge und Medium.** Exploration verwendet vorbereitete Kontrastfälle, kontrollierte Simulationen oder begrenzte Lösungsräume. Anschließend vergleicht und erklärt die Lehrkraft Lösungswege, führt das Zielkonzept ein und sichert es gemeinsam. Für Klasse 5 wird der Ansatz besonders vorsichtig pilotiert.

### CLAIM-LP-013 – Selbstregulation als explizite Lernhandlung aufbauen

**Befund.** Explizite Selbstregulationstrainings in realen Grundschulklassen verbesserten im Mittel akademische Leistung, Strategiegebrauch und Motivation; daraus folgt keine einzelne universelle Trainingssequenz.

**Evidenz.** Dignath, Büttner und Langfeldt integrierten 30 Artikel mit 48 Vergleichen und 263 Effektgrößen. Der gewichtete Gesamtmittelwert lag bei `d = 0.69`; gruppierte Mittelwerte lagen für akademische Leistung bei `d = 0.62`, für kognitiven und metakognitiven Strategiegebrauch bei `d = 0.73` und für Motivation bei `d = 0.76`. [Originalquelle](https://doi.org/10.1016/j.edurev.2008.02.003)

**Scope und Einschränkungen.** Klassen 1–6 beziehungsweise Lernende im Durchschnitt bis etwa 12 Jahre in realen Klassenräumen. Computerbasierte Interventionen waren ausgeschlossen. Die Evidenz stammt von 2008; Programme, Messungen und Implementationen waren heterogen, die Zielgruppe überlappt nur teilweise mit Klasse 5–7, und weder ein digitales noch ein IuM-spezifisches Setting wurde untersucht. Die Mittelwerte garantieren keine einzelne Abfolge; Unterschiede zwischen forschungs- und lehrkraftgeleiteter Implementation begrenzen die Übertragung.

**IBBW-Abgleich.** Band 3 stützt explizite, lernprozessbezogene Unterstützung und nutzbare Rückmeldung; Band 1 stützt klare Orientierung und Rahmung. Die quantitativen Interventionsbefunde stammen ausschließlich aus der Originalmeta-Analyse und werden durch IBBW nicht als eigener Effektbeleg dupliziert.

**Betroffene Modulphasen.** 4.2 Vorwissen aktivieren; 4.4 Angeleitet erproben; 4.6 Prüfen, überarbeiten und übertragen.

**Designfolge und Medium.** Selbstregulation wird als konkrete Folge fachlicher Lernhandlungen angelegt: planen, eine Strategie wählen, den Zwischenstand überwachen sowie prüfen und revidieren. Rückmeldung knüpft an aktuelle Handlungen und Produkte an; das Lernwerk diagnostiziert keine stabile persönliche Eigenschaft und erzeugt keine personenbezogene Telemetrie. Die digitale Umsetzung dieser Lernhandlungen bleibt eine zu pilotierende Übertragung, nicht Teil des Originalnachweises.

## Kompakte Phasenmatrix

| Modulphase | Tragende Claims | Verbindliche Lernfunktion |
| --- | --- | --- |
| 4.1 Orientierung und Herausforderung | CLAIM-LP-001, CLAIM-LP-011, CLAIM-LP-012 | relevante Frage, klare Ziele, begrenzte Wahl und vorbereitete Herausforderung |
| 4.2 Vorwissen aktivieren | CLAIM-LP-001, CLAIM-LP-002, CLAIM-LP-005, CLAIM-LP-007, CLAIM-LP-010, CLAIM-LP-012, CLAIM-LP-013 | vorhandene Modelle, Kenntnisse, Abrufwege und Planung ohne Profilbildung sichtbar machen |
| 4.3 Konzept aufbauen | CLAIM-LP-001, CLAIM-LP-002, CLAIM-LP-003, CLAIM-LP-004, CLAIM-LP-005, CLAIM-LP-006, CLAIM-LP-012 | Repräsentationen integrieren, Beispiele aktiv verarbeiten, Exploration explizit konsolidieren |
| 4.4 Angeleitet erproben | CLAIM-LP-001 bis CLAIM-LP-008, CLAIM-LP-010 bis CLAIM-LP-013 | Beispiele variieren, Scaffolds hürdenbezogen nutzen, Strategien überwachen, abrufen und informativ rückmelden |
| 4.5 Eigenständig handeln oder produzieren | CLAIM-LP-001, CLAIM-LP-003, CLAIM-LP-004, CLAIM-LP-006, CLAIM-LP-008 bis CLAIM-LP-011 | eigenständige fachliche Entscheidung und prüfbares Produkt innerhalb klarer Struktur |
| 4.6 Prüfen, überarbeiten und übertragen | CLAIM-LP-001, CLAIM-LP-006 bis CLAIM-LP-011, CLAIM-LP-013 | testen, Feedback nutzen, zeitversetzt abrufen, Strategien prüfen, revidieren und Transfer getrennt prüfen |
| 4.7 Gemeinsam sichern | CLAIM-LP-001, CLAIM-LP-005, CLAIM-LP-007 bis CLAIM-LP-010, CLAIM-LP-012 | Begriffe, Modelle, Begründungen, Fehlwege und spätere Wiederaufnahme konsolidieren |

## Übungs- und Festigungsarchitektur

Ein Kernkonzept durchläuft drei getrennte Evidenzpunkte:

1. **unmittelbare Anwendung** nach Konzeptaufbau mit Beispielvariation und gestufter Hilfe;
2. **verzögerter Abruf** nach einem für die Unterrichtsfolge relevanten Abstand, möglichst ohne erneute Darbietung;
3. **Transfer** in einer veränderten Repräsentation, Oberfläche oder Anwendungssituation.

Abruf, Feedback und Spacing werden verbunden, aber nicht verwechselt. Ein digitales Modul kann Testfälle, Varianten und spätere Wiedervorlagen zuverlässig bereitstellen. Es speichert keine personenbezogene Historie und berechnet keinen Kompetenzstand. Lehrkräfte nutzen sichtbare Produkte, Gespräch und aktuelle Bearbeitung für die Orchestrierung.

## Feedback und Selbstregulation ohne zentrale Diagnostik

Feedback wird nach Aufgabe, Strategie und nächstem Prüfschritt differenziert. Timing folgt der Lernfunktion: sofort bei sicherheitsrelevanten oder voraussetzungsnotwendigen Fehlern, gegebenenfalls verzögert bei begründbaren Lösungswegen, wenn zunächst Selbsterklärung oder Vergleich produktiv ist.

Selbstregulation wird als Handlung gestaltet: Ziel klären, Vorgehen planen, eine Strategie wählen, den Zwischenstand überwachen sowie Ergebnis und Strategie prüfen und revidieren. CLAIM-LP-013 stützt explizite Strategiearbeit für jüngere Lernende, aber nicht ihre digitale Umsetzung; CLAIM-LP-011 begründet ergänzend und nur korrelativ die Verbindung von Autonomieunterstützung und Struktur.

Datensparsame Gelegenheiten sind lokale Selbstchecks, Testfälle, Muster- und Gegenbeispiele, Produktkriterien, Peer-Rückmeldung und kurze Lehrkraftgespräche. Konten, Profile, Rankings, zentrale Antwortspeicherung und Telemetrie sind ausgeschlossen.

## Multimedia, Interaktivität und Mediumwahl

- Digitale Funktionen benennen ihren Mechanismus: Aufmerksamkeit lenken, Repräsentationen verbinden, Zustand verändern, Hypothese testen, Abruf auslösen, Feedback geben oder Produkt revidieren.
- Signale markieren relevante Beziehungen oder Bearbeitungsschritte. Sie sind keine Dekoration.
- Interaktivität wird verworfen, wenn Klicken, Ziehen oder Animation keine fachliche Entscheidung, Prüfung oder Erklärung auslöst.
- Digitale worked examples verlangen Vorhersage, Erklärung, Vergleich, Ergänzung oder Korrektur; bloßes Abspielen ist nicht hinreichend.
- Analog ist begründet, wenn freies Skizzieren, räumliche Anordnung, haptische Manipulation, Verkörperung oder bildschirmfreie Diskussion die Lernfunktion klarer oder störungsärmer erfüllt.
- Es gibt keine parallele analoge Vollstruktur. Digital bleibt das selbstverständliche Primärmedium.

## Verworfen oder herabgestuft

- **„Vorwissen hilft immer.“** Verworfen: Die Meta-Analyse zeigt hohe Stabilität, aber stark variable Beziehung zum Wissenszuwachs.
- **„Worked examples sind passives Vormachen.“** Verworfen: Die Projektfolge verlangt aktive Verarbeitung; die Mathematikeffektzahl ist nicht auf IuM übertragbar.
- **„Fading ist als feste digitale Hilfelogik erwiesen.“** Verworfen: Anpassung und Fading moderierten den Belland-Effekt nicht robust.
- **„Retrieval Practice ist Wiederholen.“** Verworfen: Der Mechanismus ist aktiver Abruf; Wiederexposition ist eine andere Vergleichsbedingung.
- **„Spacing bedeutet möglichst häufig wiederholen.“** Verworfen: Zeitverteilung, Retentionsziel, Wiederexposition und Bildungsstufe moderieren die Befundlage.
- **„Feedback wirkt allgemein mit `d = 0.55`.“** Verworfen: `d = 0.55` ist der unbereinigte Mittelwert; nach Ausschluss von 35 extremen Effekten lag er bei `d = 0.48`. 17 % negative Effekte und sehr hohe Heterogenität schließen eine pauschale Regel aus.
- **„Autonomie bedeutet wenig Struktur.“** Verworfen: Die Konstrukte waren im Mittel positiv verbunden, aber die Beziehung war extrem heterogen, methoden- und schulstufenabhängig und in acht Studien negativ. Daraus folgt keine robuste Synergie.
- **„Produktives Scheitern rechtfertigt offenes Entdecken.“** Verworfen: Positive Befunde setzen passende Aufgaben, Vorwissen und anschließende Instruktion voraus.
- **„Mehr Interaktivität verbessert Lernen.“** Verworfen: Weder IBBW noch der geprüfte Evidenzkern stützen Interaktivität ohne benannten Lernmechanismus.
- **Signaling-Effektzahl.** Herabgestuft: Schneider et al. (2018) wurde bibliografisch am Original geprüft, der Primärvolltext war im Prüfpfad nicht direkt zugänglich. Die Quelle bleibt im Register `metadata-checked`; numerische Effekte und ein eigener retained Claim werden nicht übernommen.

## Offene Forschungsfragen

- Wie wirken worked examples, Selbsterklärung und Fading bei Codeverständnis, Datenmodellen und Medienanalyse für 10- bis 13-Jährige?
- Welche Abstände und Rückkehrformate sichern IuM-Konzepte über Module hinweg, ohne den Lernweg zu überfrachten?
- Welche Transferaufgaben prüfen strukturelles Verständnis statt Oberflächenähnlichkeit?
- Welche vorbereiteten Explorationsformen sind in Klasse 5 tragfähig, und wann ist Instruction before Problem Solving besser?
- Wie unterstützen lokale Selbstchecks Selbstregulation, ohne personenbezogene Profile oder Telemetrie?
- Welche Signaling-, Animations- und Interaktivitätsmerkmale verbessern Behalten und Transfer in fachtypischen IuM-Repräsentationen?

## Quellen

Die vierzehn registrierten Quellen `SRC-LP-*` stehen im `source-register.json`. Prüf- und Effektgrenzen sind im unveränderten Rohbericht `../raw/03-lernpsychologie-unterricht.md` sowie für die Fixrunde in den Errata und CLAIM-LP-013 dieses Curated-Berichts dokumentiert.
