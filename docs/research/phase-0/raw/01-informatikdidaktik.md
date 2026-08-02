---
package: informatikdidaktik
executed: 2026-07-28
status: raw
prompt: ../prompts/01-informatikdidaktik.md
---

# 1. Executive Summary

Für die Zielgruppe von etwa 10 bis 13 Jahren ist die Evidenz am stärksten, wenn Programmieren nicht als unmittelbares freies Produzieren, sondern als schrittweise Entwicklung unterscheidbarer Praktiken organisiert wird: Abläufe vorhersagen und nachvollziehen, vorhandenen Code untersuchen und verändern, gezielt testen und erst danach zunehmend eigenständig entwerfen. K‑8-Lernverlaufsforschung stützt eine Progression für Sequenz, Wiederholung und Bedingungen; die PRIMM-Studie zeigt bei 11- bis 14-Jährigen in realen Schulklassen einen kleinen günstigen Leistungseffekt eines strukturierten Predict–Run–Investigate–Modify–Make-Zyklus. Reviews zu Fehlvorstellungen und „notional machines“ begründen, Programmzustand und Ausführung ausdrücklich sichtbar zu machen.

Blockbasierte Umgebungen können anfängliche Syntaxhürden senken. Eine quasi-experimentelle High-School-Studie fand nach fünf Wochen größere Lernzuwächse mit einer blockbasierten als mit einer isomorphen textbasierten Oberfläche; nach dem späteren Übergang zu Java verschwanden die Gruppenunterschiede. Daraus folgt keine allgemeine Überlegenheit von Blöcken, sondern die begrenzte Heuristik, Darstellungsform, Lernziel und Übergang bewusst aufeinander abzustimmen.

Unplugged-Aktivitäten sind nicht schon deshalb wirksam, weil sie analog, aktiv oder spielerisch sind. Ein K‑12-Review weist auf uneinheitliche Konstrukte, konfundierte Interventionen und schwache Transferbelege hin. Eine kleine quasi-experimentelle Studie mit 10- bis 12-Jährigen liefert gleichwohl positive Evidenz für eng umrissene unplugged Aufgaben zu Sequenzen, Schleifen, Bedingungen und Variablen. Analog ist daher fachlich begründet einzusetzen, wenn Verkörperung, Manipulation oder gemeinsame Modellierung einen unsichtbaren Prozess sichtbar macht; digitale Ausführung ist nötig, wenn präzise Maschinenrückmeldung, Testen oder ein authentischer Systemprozess das Lernziel bildet.

Für Daten, Codierung, Netze, Client–Server und grundlegende Kryptografie ist die direkte Wirksamkeitsevidenz bei 10- bis 13-Jährigen deutlich dünner als für Einführungsprogrammierung. Ein systematisches Review zu Internetvorstellungen von 3- bis 15-Jährigen zeigt jedoch verbreitete fragmentarische Modelle von Wi‑Fi, zentralen Computern, Türmen und Satelliten. Professionelle CSTA-Standards von 2026 liefern eine kohärente Inhalts- und Praxisarchitektur, aber keinen Wirksamkeitsnachweis. Die konkrete baden-württembergische Progression bleibt deshalb eine zu prüfende Projektinferenz.

# 2. Such- und Auswahlbeschreibung

Die Recherche wurde am 28. Juli 2026 quellenfähig durchgeführt. Gesucht wurde in bzw. über Originalseiten von ACM, Taylor & Francis, Springer Nature, Elsevier, CSTA, institutionelle Forschungsportale und Autorenarchive. Suchkombinationen verbanden `K-8 learning trajectory`, `PRIMM`, `programming misconceptions`, `notional machine`, `worked examples programming`, `block text transition`, `unplugged K-12 review`, `internet conceptions children`, `data networks security standards` und die Altersstufen.

Eingeschlossen wurden:

- systematische oder kritische Reviews mit ausgewiesener Such- bzw. Synthesemethode;
- peer-reviewte Primärstudien mit nachvollziehbarer Stichprobe und Intervention;
- Forschungsrahmen mit expliziter Herleitung;
- offizielle professionelle Standards zur Inhaltsprogression.

Ausgeschlossen oder nicht für zentrale Aussagen verwendet wurden:

- Blogbeiträge, Marketingseiten und reine Materialsammlungen;
- nur sekundär auffindbare Zitate ohne überprüfbare Metadaten;
- Wirkversprechen, deren zugrunde liegende Intervention mehrere Medien und Methoden untrennbar vermischte;
- Generalisierungen von Hochschulstudierenden auf die Klassen 5–7 ohne ausdrücklichen Transferhinweis.

Die wichtigsten Aussagen wurden gegen DOI-, Publisher-, Autoren- oder Institutionsseiten geprüft. Wo eine Originalpublikation überwiegend Hochschulanfänger untersuchte, wird sie nur als plausible didaktische Heuristik für 10- bis 13-Jährige verwendet. Professionelle Standards werden als fachliche Orientierungen, nicht als empirische Wirksamkeitsbelege behandelt.

# 3. Evidenzmatrix

| Befund | Quelle und Publikationsart | Alter/Stufe | Reichweite | Einschränkungen | Konsequenz |
| --- | --- | --- | --- | --- | --- |
| Lernziele für Sequenz, Wiederholung und Bedingungen lassen sich als K‑8-Lernpfade ordnen; Kontext und Sprache beeinflussen die Pfade. | Rich et al. 2017, literaturbasierte Forschungssynthese, DOI 10.1145/3105726.3106166 | K‑8 | Progressionshypothesen für zentrale Kontrollstrukturen | Forschungsliteratur war lückenhaft; keine Wirksamkeitsstudie eines vollständigen Curriculums | Lernziele nicht nur nach Begriffen, sondern nach steigenden Operationen und Repräsentationen staffeln. |
| Debugging umfasst Strategien zum Finden und Beheben, Fehlertypen und die Rolle von Fehlern im Problemlösen. | Rich et al. 2019, literaturbasierte K‑8-Lerntrajektorie, DOI 10.1145/3287324.3287396 | K‑8 | Mehrdimensionale Ordnung von Debuggingzielen | Hergeleitete Trajektorie, keine kausale Interventionsstudie | Fehler lokalisieren, klassifizieren, Hypothesen bilden, testen und begründen getrennt üben. |
| PRIMM war in 13 Schulen mit 11- bis 14-Jährigen mit höheren Posttestwerten verbunden. | Sentance, Waite & Kallia 2019, Mixed-Methods-Studie, DOI 10.1080/08993408.2019.1608781 | 11–14; 493 Intervention, 180 Kontrolle | Schulische Einführung in Programmierung | Keine durchgängige Randomisierung; Schulen und Umsetzung variierten; Effekt klein (r=.13) | Vorhersagen, Ausführen, Untersuchen, Verändern und Erstellen als wiederkehrende Modulfolge nutzen. |
| Tracing, Syntaxproduktion, Templateverständnis und Codeproduktion können explizit und inkrementell getrennt werden. | Xie et al. 2019, Theorie plus explorative Mixed-Methods-Studie, DOI 10.1080/08993408.2019.1565235 | neun überwiegend erwachsene Hochschulneulinge | Detaillierte Hypothese zur Programmierinstruktion | Sehr kleine Stichprobe; keine statistisch belastbare Wirkung; Altersübertragung offen | Die vier Praktiken als Designheuristik verwenden, aber an 10- bis 13-Jährigen pilotieren. |
| Worked examples sind vor allem für Code-Tracing und Code-Generierung erforscht; hilfreich erscheinen aktive Verarbeitung, Subgoals, Lücken und Parsons-Probleme. | Muldner, Jennings & Chiarelli 2023, Review, DOI 10.1145/3560266 | überwiegend tertiäre Einführungskurse | Synthese zu Programmierbeispielen | Altersgruppe 10–13 unterrepräsentiert; heterogene Aufgaben und Maße | Beispiele mit Vorhersage, Selbsterklärung und schrittweisem Ausblenden koppeln, nicht passiv anzeigen. |
| Fehlvorstellungen betreffen unter anderem Variablen, Zuweisung, Kontrollfluss, Schleifen und Aufrufe; die Literatur ist stark CS1-geprägt. | Qian & Lehman 2017, Literaturreview, DOI 10.1145/3077618 | überwiegend Hochschule, einzelne K‑12-Bezüge | Katalog und Einordnung wiederkehrender Schwierigkeiten | Uneinheitliche Definition von „misconception“; nicht alle Befunde entwicklungspsychologisch geprüft | Kurze Diagnoseaufgaben in den Lernprozess einbauen; keine dauerhaften Personenprofile erzeugen. |
| Ein explizites „notional machine“-Modell kann statischen Code, Laufzeitprozess und Zustand verbinden; Visualisierung ist kein Selbstzweck. | Sorva 2013, theoretisch-kritischer Review, DOI 10.1145/2483710.2483713 | überwiegend CS1 | Synthese zu mentalen Modellen und Programmausführung | Hauptsächlich Hochschulkontexte; Modell muss sprach- und werkzeugspezifisch sein | Zustandstabellen, Ablaufspuren und Laufzeitvisualisierungen konsistent verwenden und aktiv bearbeiten lassen. |
| Blockbasierte Oberflächen können in einer anfänglichen Phase bessere Lernzuwächse als eine isomorphe Textoberfläche ermöglichen. | Weintrop & Wilensky 2017, 5‑wöchige Quasi-Experimentalstudie, DOI 10.1145/3089799 | High School, n=60 | Variablen, Bedingungen, Schleifen und Prozeduren | Selektive Schule, Wahlkurs, nur zwei Klassen, CoffeeScript/Pencil-Code-Kontext | Blöcke als niedrigschwellige Repräsentation anbieten, nicht als generelle Entwicklungsstufe festschreiben. |
| Nach zehn Wochen Java waren frühere Unterschiede zwischen Block- und Textgruppe nicht mehr nachweisbar. | Weintrop & Wilensky 2019, 15‑wöchige Quasi-Experimentalstudie, DOI 10.1016/j.compedu.2019.103646 | High School, dieselben zwei Klassen | Übergang in professionelle Textsprache | Kleines, selektives Sample; ein Lehrer; spezifischer Übergang zu Java | Übergang explizit gestalten; weder „Blöcke verhindern Transfer“ noch „Blöcke garantieren Transfer“ behaupten. |
| Unplugged-Pädagogik kann fachliches Lernen unterstützen, doch Studien verwechseln teils CT mit Programmierleistung und vermischen Methoden. | Huang & Looi 2021, kritischer K‑12-Review von 40 Publikationen, DOI 10.1080/08993408.2020.1789411 | K‑12 | Überblick zu Lernen, Zugang und Teilhabe | Heterogene Konstrukte, wenige robuste Vergleiche, schwache Equity-Evidenz | Für jede analoge Aktivität Lernmechanismus, Rückbindung und digitales Anschlussprodukt angeben. |
| Eine kurze unplugged Intervention erhöhte in zwei spanischen Schulen CT-Testwerte stärker als Unterricht ohne diese Sequenz. | Brackmann et al. 2017, Quasi-Experiment, DOI 10.1145/3137065.3137069 | 10–12, n=73 | Sequenzen, Schleifen, Bedingungen, Funktionen, Variablen | Keine Individualrandomisierung; kleine Stichprobe; Test und Aktivität inhaltlich ähnlich | Eng umrissene analoge Modellierungsphasen sind vertretbar; keine allgemeine Überlegenheit ableiten. |
| Kinder und Jugendliche verfügen häufig über fragmentarische Internetmodelle; Wi‑Fi, Internet, zentrale Speicherung, Türme und Satelliten werden verwechselt. | Brom, Yaghobová, Drobná & Urban 2023, systematisches Review von 27 Studien, DOI 10.1007/s10639-023-11775-9 | 3–15, N=2.214 | 60 Konzeptionen zu Internet, Infrastruktur und Datenfluss | Überwiegend qualitative und Mixed-Methods-Studien; Technikstand 2002–2022; fehlender Befund ist kein Altersnachweis | Präkonzepte mit Zeichnungen/Erklärungen sichtbar machen und mit Paketweg-, Router- und Client–Server-Modellen kontrastieren. |
| Zeitgemäße Standards ordnen Algorithmen, Programmierung, Daten, Systeme/Sicherheit und gesellschaftliche Folgen zusammen mit Praktiken wie Abstrahieren, Erstellen und Testen. | CSTA 2026 PK–12 Standards, professioneller Standard, DOI 10.1145/3820482 | PK–12, Middle School Grades 6–8 | Fachliche Inhalts- und Praxisarchitektur | US-amerikanischer Standard; kein Wirksamkeitsbeleg und nicht normativ für Baden-Württemberg | Daten, Netze und Sicherheit als eigenständige fachliche Stränge führen und mit Praktiken verbinden. |

# 4. Progression 5–7

Die folgende Progression ist eine Projektinferenz für Baden-Württemberg, keine direkt evaluierte Sequenz.

## Klasse 5: Handlungen präzisieren und Ausführung sichtbar machen

- Endliche Folgen ausführen, ordnen, vorhersagen und in mehreren Darstellungen beschreiben.
- Kurze gegebene Programme lesen und ausführen; Zustand und Ausgabe mit Tabelle, Spur oder konkreten Objekten festhalten.
- Programme zunächst nutzen und klein verändern; Veränderungen vor dem Lauf begründen.
- Daten als Zeichen, Zahlen und binäre Entscheidungen unterscheiden; einfache Codierungen darstellen und zurückübersetzen.
- Eigene Vorstellungen von Internet, Wi‑Fi und Speicherung durch Skizzen oder kurze Erklärungen erheben, ohne personenbezogene Speicherung.
- Analoge Aktivitäten nur dort einsetzen, wo körperliche Ausführung oder manipulierbare Zustände den Maschinenprozess klären; danach immer formal oder digital rückbinden.

## Klasse 6: Kontrollstrukturen, Variablen und systematische Tests

- Sequenz, Bedingung und Wiederholung vergleichen; Bedingungen und Schleifengrenzen vorhersagen.
- Variablen als veränderlichen Zustand in einem expliziten Maschinenmodell verwenden; Zuweisung von Gleichheit unterscheiden.
- Den Zyklus Predict–Run–Investigate–Modify–Make mehrfach in überschaubaren Kontexten durchlaufen.
- Normalfälle, Randfälle und gezielt fehlerhafte Beispiele testen; Fehlerort, Fehlerart und Reparaturhypothese trennen.
- Block- und Textdarstellungen punktuell isomorph gegenüberstellen; Syntaxlast und semantisches Ziel sichtbar auseinanderhalten.
- Datenübertragung als Weg zwischen Endgerät, lokalem Netz, Vermittlung und Dienst modellieren; Client und Server über Rollen und Nachrichten erklären.

## Klasse 7: Eigenständiger entwerfen, abstrahieren und Systeme verbinden

- Größere Programme planen, Funktionen oder Prozeduren verwenden und von Vorlagen zu eigenen Lösungen übergehen.
- Code erklären, testen, refaktorieren und dokumentieren; mehrere mögliche Lösungen nach Korrektheit, Verständlichkeit und Aufwand vergleichen.
- Den Übergang zu textuellen Darstellungen durch parallele Beispiele, strukturierte Editoren oder kleine Übersetzungsaufgaben stützen.
- Datenrepräsentationen im Kontext von Übertragung, Kompression oder Fehlererkennung untersuchen.
- Client–Server, Routing und verteilte Speicherung an echten, aber didaktisch reduzierten Protokollspuren nachvollziehen.
- Grundlegende Kryptografie als Zusammenhang von Klartext, Verfahren, Schlüssel, Geheimtext und Angriffsannahme behandeln; einfache Handverfahren dienen der Modellbildung, digitale Werkzeuge der skalierbaren Anwendung und Prüfung.

Für Netze, Datenrepräsentation und Kryptografie muss die konkrete Reihenfolge zusätzlich mit dem baden-württembergischen Curriculum-Mapping geprüft werden. Die Forschungslage rechtfertigt hier nicht dieselbe Sicherheit wie bei den Programmierpraktiken.

# 5. Fehlvorstellungen

## Programmierung

Wiederkehrende Schwierigkeiten betreffen die Annahme, eine Variable speichere eine algebraische Gleichung, ein sprechender Variablenname vermittle dem Computer Bedeutung, mehrere Zuweisungen gälten gleichzeitig oder eine Schleife „wisse“ die beabsichtigte Anzahl von Wiederholungen. Hinzu kommen Verwechslungen von statischem Programmtext, aktueller Ausführungsposition und veränderlichem Zustand.

Diagnostische Gelegenheiten:

- Ausgabe und Zustandsfolge eines sehr kurzen Programms vorhersagen;
- zwei fast gleiche Programme mit einem kritischen Unterschied vergleichen;
- einen falschen Trace reparieren;
- in eigenen Worten erklären, was eine Zeile jetzt bewirkt und was sie nicht bewirkt;
- Randfälle für eine Schleife oder Bedingung wählen;
- einen Fehler erst lokalisieren, dann klassifizieren, dann beheben.

Antworten sollen für unmittelbares Feedback genutzt werden. Es ist weder erforderlich noch datenschutzgerecht, dauerhafte individuelle Fehlvorstellungsprofile anzulegen.

## Netze

Typische Präkonzepte setzen Internet mit Wi‑Fi, einem Gerät, einer „Cloud“, einem zentralen Computer, einem Turm oder Satelliten gleich. Häufig fehlt ein mehrstufiges Modell von Datenfluss und verteilter Infrastruktur.

Diagnostische Gelegenheiten:

- „Zeichne und erkläre den Weg einer Nachricht“;
- Karten mit Client, Router, Provider, Server und Datenpaket ordnen;
- zwei Modelle vergleichen: direkter Funkweg versus mehrstufiger Paketweg;
- erklären, wo Daten während einer Anfrage und dauerhaft gespeichert sein können.

Die Auswertung bleibt auf Aufgabenebene; das Lernwerk speichert keine personenbezogenen Diagnosedaten.

## Codierung und Kryptografie

Für diese Altersgruppe wurden in der gesichteten Evidenz keine vergleichbar robusten Fehlvorstellungskataloge gefunden. Plausible Risiken sind die Gleichsetzung von Codierung und Verschlüsselung, die Annahme, Geheimhaltung des Verfahrens ersetze einen Schlüssel, und die Verwechslung von Darstellung, Kompression, Fehlererkennung und Schutz. Diese Punkte sind fachliche Hypothesen für Pilotaufgaben, keine gesicherten altersbezogenen Forschungsbefunde.

# 6. Aufgaben- und Repräsentationsdesign

## Worked examples und explizite Anleitung

Ein Beispiel soll nicht bloß fertigen Code zeigen. Es enthält Problem, Ziel, relevante Zustände, begründete Schritte und ein sichtbares Ergebnis. Lernende müssen vorhersagen, einzelne Schritte erklären, kritische Stellen markieren oder eine ausgelassene Zeile ergänzen. Danach wird Unterstützung reduziert: vollständig ausgearbeitetes Beispiel → Beispiel mit Teilentscheidungen → unvollständiges Beispiel oder Parsons-Problem → Modifikation → eigenständige Lösung.

Da der Worked-example-Review überwiegend tertiäre Kontexte umfasst, ist diese Abfolge in Klasse 5–7 als prüfbare Designheuristik zu behandeln. Kurze Aufgaben, geringe Syntaxlast und unmittelbare Anschlussprobleme sind wichtiger als lange Musterlösungen.

## Repräsentationen

- Ablaufspuren verbinden Codezeile, Ausführungsposition, Variablenzustand und Ausgabe.
- Zustandstabellen eignen sich für Variablen, Schleifen und Verzweigungen, wenn ihre Spalten stabil bleiben.
- Block- und Textcode werden nur parallel gezeigt, wenn semantische Korrespondenzen markiert und aktiv übersetzt werden.
- Netzdiagramme zeigen Rollen, Knoten, Verbindungen, Nachrichtenrichtung und Speicherung; dekorative Cloud-Symbole ohne erklärten Mechanismus sind zu vermeiden.
- Codiertabellen, Bitmuster und Schlüsselräume werden mit konkreten Datenobjekten verknüpft.

Visualisierung ist dann lernwirksam plausibel, wenn Lernende mit ihr vorhersagen, erklären, ergänzen oder korrigieren. Reines Abspielen einer Animation reicht nicht.

## Exploration und selbstständiges Problemlösen

Offene Exploration folgt nicht automatisch auf eine Erklärung, sondern auf gesicherte Mindestvoraussetzungen. Eine Aufgabe benennt invarianten fachlichen Kern, verfügbare Werkzeuge, Erfolgskriterien und Reflexionsprodukt. Wahlmöglichkeiten können Kontext, Darstellung oder Erweiterung betreffen, ohne das Kernziel zu verdecken. Selbstständige Projekte werden durch Zwischenprodukte strukturiert: Problemformulierung, Beispiel, Plan, Testfälle, lauffähiges Minimum, Überarbeitung und Erklärung.

# 7. Analog versus digital

## Analog fachlich begründet

- Lernende spielen eine eindeutige Maschine oder ein Netzwerkprotokoll, wenn die Rollen und Regeln präzise sind.
- Karten, Seile, Kästchen oder Körperpositionen repräsentieren Zustand, Reihenfolge, Verbindung oder Schlüsselraum.
- Gemeinsame Manipulation ermöglicht Sprache und Aushandlung über einen sonst unsichtbaren Prozess.
- Papier eignet sich für Trace, Vergleich und Fehlersuche, wenn Ablenkung durch Editorbedienung das Ziel überlagern würde.

Jede analoge Aktivität braucht eine Korrespondenztabelle: Was repräsentiert was? Welche Maschinenregel gilt? Wo bricht die Analogie? Welches digitale oder formale Anschlussprodukt prüft die Übertragung?

## Digital fachlich begründet

- Ausführung liefert präzise Rückmeldung über Semantik und Zustand.
- Tests lassen sich wiederholen, variieren und mit Randfällen prüfen.
- Netzverkehr, Datenrepräsentation und Verschlüsselung können in skalierbarer oder authentischer Form untersucht werden.
- Programme sind veränderbare Artefakte; Versionen, Eingaben und Ausgaben können verglichen werden.

Die Schlussfolgerung lautet nicht „zuerst immer analog“ oder „digital ist immer authentischer“. Das Medium folgt der epistemischen Funktion. Eine Doppelstruktur ohne zusätzlichen Lerngewinn ist zu vermeiden.

# 8. Kontroverse oder schwache Evidenz

1. **Block versus Text:** Zwei Studien derselben High-School-Kohorte zeigen zunächst Vorteile der Blockdarstellung, später aber keine Unterschiede nach dem Java-Übergang. Werkzeug, Curriculum, Schule und Lehrkraft begrenzen die Übertragung. Ein dogmatischer Alterswechsel ist nicht begründet.
2. **Worked examples:** Der Review bietet eine gute Programmierdidaktik-Synthese, doch die Evidenz stammt überwiegend aus Hochschulkontexten. Dosierung, Fading und Selbsterklärung müssen für 10- bis 13-Jährige pilotiert werden.
3. **Explizite Skill-Sequenz:** Xie et al. formulieren eine starke Theorie, prüfen sie jedoch nur mit neun überwiegend erwachsenen Lernenden. Sie stützt eine Heuristik, keinen verbindlichen Klassenstufenplan.
4. **Unplugged-Wirkung:** Positive Einzelstudien stehen neben erheblichen Validitäts- und Transferproblemen. Besonders ungesichert ist die Behauptung, unplugged Aktivitäten erhöhten automatisch Interesse oder Teilhabe.
5. **Kryptografie und Daten:** In der gesichteten Literatur fehlen starke, direkt altersbezogene Vergleichsstudien zu einer Progression 5–7. Professionelle Standards und fachliche Analyse müssen durch Pilotierung ergänzt werden.
6. **Standards:** CSTA 2026 ist aktuell und fachlich strukturiert, aber US-amerikanisch und nicht normativ für Baden-Württemberg. Es begründet Inhaltsbreite, nicht Methodenwirksamkeit.
7. **Fehlvorstellungen:** Viele Programmierbefunde stammen aus CS1. Begriffe und Schwierigkeiten dürfen nicht ungeprüft als stabile kindliche Fehlkonzepte etikettiert werden.

# 9. Priorisierte Designfolgen

1. Eine wiederkehrende Modulgrammatik aus Aktivierung/Diagnose, modelliertem Beispiel, Predict–Run–Explain, fokussierter Übung, Modify/Test, Make/Transfer und Reflexion entwickeln.
2. Code lesen, vorhersagen, erklären, verändern, testen und erstellen als getrennte, kumulativ verknüpfte Lernhandlungen ausweisen.
3. Für jedes Programmiermodul ein konsistentes notional-machine-Modell mit Zustand, Ausführungsposition und Ausgabe festlegen.
4. Fehlersuche als eigene Progression planen: bemerken → lokalisieren → klassifizieren → Hypothese → gezielter Test → Reparatur → Begründung.
5. Block/Text nicht als Lagerfrage behandeln; für jedes Modul die gewählte Repräsentation und den Übergang begründen.
6. Worked examples aktiv verarbeiten lassen und Unterstützung sichtbar ausblenden.
7. Analoge Aktivitäten nur mit expliziter Repräsentationsfunktion, Analogiegrenze und digitalem/formalem Anschluss verwenden.
8. Internet-Präkonzepte in anonymen Aufgaben sichtbar machen und schrittweise zu Client–Server-, Paketweg- und Verteilungsmodellen entwickeln.
9. Daten, Codierung, Netze und Sicherheit als eigenständige Stränge führen, nicht als Nebenprodukte des Programmierens.
10. Bei Daten- und Kryptografieprogression Unsicherheit dokumentieren und frühe Module gezielt mit Beobachtung, Artefaktanalyse und datensparsamen Klassenauswertungen pilotieren.

# 10. Vollständiges Quellenverzeichnis mit stabilen Links

- Brackmann, C. P., Román-González, M., Robles, G., Moreno-León, J., Casali, A. & Barone, D. (2017). *Development of Computational Thinking Skills through Unplugged Activities in Primary School.* Proceedings of WiPSCE ’17. https://doi.org/10.1145/3137065.3137069
- Brom, C., Yaghobová, A., Drobná, A. & Urban, M. (2023). *‘The internet is in the satellites!’: A systematic review of 3–15-year-olds’ conceptions about the internet.* Education and Information Technologies, 28, 14639–14668. https://doi.org/10.1007/s10639-023-11775-9
- Computer Science Teachers Association. (2026). *2026 CSTA PK–12 Computer Science Standards.* https://doi.org/10.1145/3820482 und https://csteachers.org/pk12standards/
- Huang, W. & Looi, C.-K. (2021). *A critical review of literature on “unplugged” pedagogies in K-12 computer science and computational thinking education.* Computer Science Education, 31(1), 83–111. https://doi.org/10.1080/08993408.2020.1789411
- Muldner, K., Jennings, J. & Chiarelli, V. S. (2023). *A Review of Worked Examples in Programming Activities.* ACM Transactions on Computing Education, 23(1), Article 13. https://doi.org/10.1145/3560266
- Qian, Y. & Lehman, J. D. (2017). *Students’ Misconceptions and Other Difficulties in Introductory Programming: A Literature Review.* ACM Transactions on Computing Education, 18(1), Article 1. https://doi.org/10.1145/3077618
- Rich, K. M., Strickland, C., Binkowski, T. A., Moran, C. & Franklin, D. (2017). *K-8 Learning Trajectories Derived from Research Literature: Sequence, Repetition, Conditionals.* Proceedings of ICER ’17, 182–190. https://doi.org/10.1145/3105726.3106166
- Rich, K. M., Strickland, C., Binkowski, T. A. & Franklin, D. (2019). *A K-8 Debugging Learning Trajectory Derived from Research Literature.* Proceedings of SIGCSE ’19, 745–751. https://doi.org/10.1145/3287324.3287396
- Sentance, S., Waite, J. & Kallia, M. (2019). *Teaching computer programming with PRIMM: a sociocultural perspective.* Computer Science Education, 29(2–3), 136–176. https://doi.org/10.1080/08993408.2019.1608781
- Sorva, J. (2013). *Notional Machines and Introductory Programming Education.* ACM Transactions on Computing Education, 13(2), Article 8. https://doi.org/10.1145/2483710.2483713
- Weintrop, D. & Wilensky, U. (2017). *Comparing Block-Based and Text-Based Programming in High School Computer Science Classrooms.* ACM Transactions on Computing Education, 18(1), Article 3. https://doi.org/10.1145/3089799
- Weintrop, D. & Wilensky, U. (2019). *Transitioning from introductory block-based and text-based environments to professional programming languages in high school computer science classrooms.* Computers & Education, 142, 103646. https://doi.org/10.1016/j.compedu.2019.103646
- Xie, B., Loksa, D., Nelson, G. L., Davidson, M. J., Dong, D., Kwik, H., Tan, A. H., Hwa, L., Li, M. & Ko, A. J. (2019). *A theory of instruction for introductory programming skills.* Computer Science Education, 29(2–3), 205–253. https://doi.org/10.1080/08993408.2019.1565235
