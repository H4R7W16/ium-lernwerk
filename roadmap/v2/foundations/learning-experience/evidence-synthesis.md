# LXF02 Evidenzsynthese

Stand: 2026-09-03

Status: `reviewed` auf Quellen- und Claimebene, noch kein `standard`

Maschinenlesbare Grundlage: [`evidence-register.json`](./evidence-register.json)
Quellenregister: [`../sources/source-register.json`](../sources/source-register.json)

Diese Synthese beantwortet eine engere Frage als ein Material- oder Designsystem: Welche Aussagen tragen die geprüften Quellen, über welche angenommenen Mechanismen, für welchen Lernendenkontext und mit welchen Grenzen? Sie erzeugt noch keine fertigen Gestaltungsregeln. Diese Übersetzung erfolgt erst in LXF04 und muss dann beobachtbare Kriterien sowie passende Prüfarten benennen.

Die Evidenzstufe bezeichnet die Tragfähigkeit des jeweiligen Quellen- und Aussagepakets, nicht die Reife des IuM-Lernwerks. `normative` kennzeichnet einen technischen Standard. `high` kennzeichnet eine starke, aber weiterhin begrenzte Forschungssynthese. `medium` kennzeichnet eine belastbare Orientierung mit relevanten Übertragungs- oder Quellenbegrenzungen. Kein Claim belegt bereits eine konkrete Implementierung, schulische Nutzbarkeit, Pilotbewährung oder Lernwirkung des Produkts.

## Lernarchitektur

Tragfähig ist die Grundannahme, dass das Lernwerk nicht von Seiten, Widgets oder Medienformaten her aufgebaut werden darf. Ausgangspunkt sind fachliche Lernhandlungen, die kognitive Aktivierung auslösen, durch passende Unterstützung aufrechterhalten und von der Lehrkraft realistisch orchestriert werden. Technik ist Mittel dieser Lernprozesse und kein eigenständiges Qualitätsmerkmal (`CLAIM-LP-001`).

Vorwissen verändert, was eine Aufgabe für eine konkrete Lerngruppe schwierig macht. Eine kurze Vorwissensaktivierung kann deshalb für die Planung relevant sein, sie darf aber nicht aus einer Einzelantwort ein stabiles Fehlkonzept oder Personenprofil ableiten (`CLAIM-LP-002`). Cognitive Load Theory ergänzt diese Perspektive: Aufgabe, Darstellung, Vorwissen und Lernumgebung sind gemeinsam zu betrachten; weder Bearbeitungszeit noch subjektive Leichtigkeit darf mit Lernen gleichgesetzt werden (`CLAIM-LP-003`).

Für die weitere Architektur folgt als Arbeitsrichtung: Lernziel, Lernhandlung, Repräsentation, Unterstützung und Lernnachweis müssen als zusammenhängende Einheit spezifiziert werden. Ob und in welcher Reihenfolge diese Einheit später in Materialzustände übersetzt wird, ist noch eine Projektentscheidung von LXF04 und LXF05.

## Kognitive Belastung und Multimedia

CTML bietet einen geeigneten Mechanismenrahmen für Material aus Texten, Bildern, Animationen und Simulationen: Lernende wählen relevante Information aus, organisieren sie und verbinden sie miteinander sowie mit Vorwissen. Begrenzte Verarbeitungskapazität begründet, vermeidbare Nebenlast zu reduzieren. Der Theorieüberblick selbst beweist aber keinen generellen Vorteil digitaler oder multimedialer Darstellung (`CLAIM-V2-LXF-MAYER-001`).

Zwei Designrichtungen sind stärker empirisch abgesichert, bleiben aber bedingt:

- Bedeutungsvolle Segmentierung kann informationsdichte Multimediaerklärungen besser verarbeitbar machen. Sie muss fachlich kohärente Einheiten schaffen und darf nicht mit einer bloßen Vermehrung von Klickschritten verwechselt werden. Lernenden- und Systemsteuerung, Vorwissen und verfügbare Zeit bleiben relevante Grenzen (`CLAIM-V2-LXF-SEGMENT-001`).
- Signale können die Integration korrespondierender Text- und Bildelemente unterstützen. Sie müssen eine fachliche Beziehung markieren; dekorative Salienz, unpassende Hinweise oder Farbe als einziger Informationsträger erfüllen diesen Zweck nicht (`CLAIM-V2-LXF-SIGNAL-001`).

Damit ist eine zurückhaltende Multimediaregel gut begründbar: Repräsentationen nur dann kombinieren, wenn ihre Beziehung lernrelevant und auffindbar ist. Ob eine konkrete Darstellung diese Funktion erfüllt, muss später in einem fachlichen Walkthrough und mit der Zielgruppe geprüft werden.

## Aktivierung und Aufgabenqualität

ICAP ist als Analyse- und Planungsrahmen nützlich, weil es oberflächliche Bedienaktivität von kognitiver Beteiligung trennt. Entscheidend ist, ob Lernende fachlich relevante Information nur aufnehmen, bearbeiten, eigene Inferenzen erzeugen oder auf Beiträgen anderer aufbauen. Klicken, Ziehen oder Gruppenarbeit allein beweist keine konstruktive oder interaktive Lernhandlung (`CLAIM-V2-LXF-ICAP-001`).

Productive Failure eröffnet eine weitere mögliche Architektur: Ein vorbereiteter Lösungsversuch kann Vorwissen aktivieren und Kontrastmaterial für nachfolgende explizite Instruktion erzeugen. Diese Richtung ist für Klasse 5 besonders vorsichtig zu behandeln. Unbegleitetes Entdecken, ein zu großer Lösungsraum oder fehlende anschließende Instruktion werden durch die Evidenz nicht getragen (`CLAIM-LP-012`).

Für V2 ist deshalb verwendbar: Aufgaben müssen einen fachlichen Output oder eine begründete Entscheidung sichtbar machen. Noch offen bleibt, welche Aufgabenformen in IuM 5, 6 und 7 ohne Überforderung konstruktive Verarbeitung auslösen. Diese Alters- und Stufengrenze gehört in LXF03 und später in Pilotfragen.

## Unterstützung und Erklärung

Worked Examples sind ein starker Kandidat für Einstiege in neue, mehrschrittige Handlungen. Ihr möglicher Nutzen entsteht durch reduzierte Suche und sichtbare Lösungsrelationen, nicht durch passive Betrachtung. Die vorliegende Meta-Analyse stammt aus Mathematik; Übertragungen auf Informatik- oder Medienproduktionsaufgaben benötigen eigene fachliche Begründung und Prüfung (`CLAIM-LP-004`).

Selbsterklärung kann eigene Inferenzen und die Verbindung mit Vorwissen fördern. Der Prompt muss jedoch zu Aufgabe und gewünschtem Denkprozess passen. Häufige generische Warum-Fragen oder ungenutzte Texteingaben sind keine belastbare Umsetzung (`CLAIM-LP-005`).

Scaffolding ist als temporäre Unterstützung tragfähig, sofern es eine identifizierte Hürde adressiert und die fachliche Kernhandlung erhält. Die Evidenz legt keine universelle adaptive oder automatische Fadinglogik fest. Rücknahme benötigt beobachtbare Bewältigungskriterien und einen sicheren Rückfallpfad (`CLAIM-LP-006`).

Verwendbar ist damit ein abgestufter Unterstützungsraum aus Modell, Hinweis, Teilstruktur und erneuter selbstständiger Anwendung. Definitiv nachzubessern ist jede alte Annahme, nach der mehr Hilfen, automatische Anpassung oder eine feste Fadingsequenz von sich aus lernwirksam wären.

## Übung und Transfer

Aktiver Abruf ist gut belegt, darf aber nicht mit Wiedersehen, Multiple-Choice-Erkennen oder einem Quizdesign gleichgesetzt werden. Die konkrete Abrufhandlung, Vergleichsbedingung, Wiederholung, Rückmeldung und Passung zum Lernziel müssen benannt sein (`CLAIM-LP-007`).

Verteilte Wiederaufnahme ist für verzögertes Behalten plausibel. Die Forschung gibt für komplexe IuM-Inhalte und 10- bis 13-Jährige jedoch weder einen universellen Abstand noch eine bestimmte Wiederholungsoberfläche vor (`CLAIM-LP-008`).

Transfer entsteht nicht durch kosmetische Variation. Eine Transferaufgabe muss eine veränderte Situation mit einem erhaltenen fachlichen Prinzip verbinden und dessen erneuten Abruf und Anwendung verlangen. Unmittelbare Anwendung, verzögertes Behalten und Transfer bleiben getrennte Outcomes (`CLAIM-LP-009`).

Für die spätere Roadmap folgt: Wiederaufnahme und Transfer müssen curricular über Stunden und Module hinweg geplant werden. Sie benötigen keine künstliche Zusatzstunde; der bestehende Unterrichtsverlauf kann diese Funktion tragen. Ob die geplanten Wiederaufnahmen tatsächlich abruf- und transferwirksam sind, ist an den Aufgaben zu prüfen.

## Feedback und Metakognition

Feedback ist relevant, aber in seiner Wirkung stark heterogen. Tragfähig ist keine pauschale Feedbackregel, sondern ein vollständiger Revisionszyklus: Ein Kriterium und der aktuelle Stand werden verständlich in Beziehung gesetzt, anschließend besteht eine reale Möglichkeit zur fachlichen Überarbeitung (`CLAIM-LP-010`). Sicherheitskritische Fehler können eine unmittelbare Korrektur erfordern.

Selbstregulation wird in V2 als erlernbare Folge fachlicher Handlungen behandelt: planen, eine Strategie wählen, überwachen, prüfen und revidieren. Die ältere Primarschulevidenz unterstützt diese Richtung nur begrenzt und rechtfertigt keine Diagnose stabiler Personeneigenschaften oder Ableitungen aus Klickdauer (`CLAIM-LP-013`).

Die zweite EEF-Guidance bestätigt die fachliche Einbettung, explizite Vermittlung, Lehrkraftmodellierung und abgestufte Unterstützung als sinnvolle Umsetzungsrichtung. Sie ist eine professionelle Evidenzübersetzung, keine einzelne kausale Studie und kein Ersatz für die IuM-spezifische Erprobung (`CLAIM-V2-LXF-EEF-META-001`).

## Motivation und Agency

Autonomieunterstützung und klare Struktur sind keine Gegensätze. Bedeutsame Wahlmöglichkeiten können Autonomieerleben unterstützen, während verständliche Ziele, Grenzen, Kriterien und Hilfen Orientierung und Kompetenzerleben ermöglichen. Die zugrunde liegende Evidenz erlaubt keine pauschale Synergie- oder Leistungsbehauptung (`CLAIM-LP-011`).

Die SDT-Interventionssynthese erweitert die Grundlage um gezielte Bildungsinterventionen. Sie trägt eine vorsichtige Aussage zu autonomer Motivation sowie Autonomie- und Kompetenzerleben; Ergebnisse zu sozialer Eingebundenheit und unterschiedlichen Kontexten sind weniger einheitlich. Daraus folgt weder eine generelle Gamificationregel noch, dass jede Auswahl motivierend wirkt (`CLAIM-V2-LXF-SDT-001`).

Für V2 ist Agency daher als nachvollziehbarer fachlicher Handlungsspielraum zu behandeln, nicht als maximale Freiheit. Motivation, Engagement, Zufriedenheit und fachliches Lernen müssen separat beobachtet werden.

## Inklusion und Accessibility

WCAG 2.2 bildet die normative technische Baseline für Web-Accessibility. Die prüfbaren Erfolgskriterien sind für Konformität relevant; selbst vollständige Konformität adressiert aber nicht alle Bedürfnisse, insbesondere nicht alle kognitiven, sprachlichen und lernbezogenen Barrieren. Sie belegt weder schulische Usability noch Lernwirkung (`CLAIM-V2-LXF-WCAG-001`).

Die ergänzende COGA-Guidance macht zusätzliche Barrieren sichtbar: unklare Zwecke und Schritte, hohe Gedächtnisanforderungen, schwer auffindbare Hilfe, unerwartete Zustandswechsel oder schwer korrigierbare Fehler. Diese Patterns sind informativ und müssen in konkreten IuM-Aufgaben fachlich und mit Nutzenden geprüft werden (`CLAIM-V2-LXF-COGA-001`).

UDL 3.0 ist als Planungsrahmen für Engagement, Repräsentation sowie Handlung und Ausdruck brauchbar. Es ist keine universelle Methode und keine kausale Wirksamkeitsstudie. Mehrere Zugänge sind nur dann gleichwertig, wenn sie dasselbe Lernziel und die notwendige fachliche Kernhandlung erhalten (`CLAIM-V2-LXF-UDL-001`).

Definitiv nachzubessern ist deshalb eine zu enge Gleichsetzung von Accessibility mit automatisierbarer WCAG-Prüfung. Technische Konformität, kognitive Zugänglichkeit, fachliche Gleichwertigkeit und reale Nutzbarkeit erhalten getrennte Gates.

## Digitale Interaktion

Die Evidenz stützt keine Interaktion um ihrer selbst willen. Digitale Bedienhandlungen sind nur gerechtfertigt, wenn sie einen fachlichen Denk-, Darstellungs-, Prüf- oder Revisionsprozess ermöglichen. Das betrifft insbesondere Drag-and-drop, Schrittfolgen, Animationen, Simulationen und spielerische Elemente.

ICAP begrenzt die Interpretation beobachtbarer Bedienung (`CLAIM-V2-LXF-ICAP-001`), CTML und die Signaling-Evidenz begrenzen die Kombination von Repräsentationen (`CLAIM-V2-LXF-MAYER-001`, `CLAIM-V2-LXF-SIGNAL-001`), WCAG und UDL begrenzen Bedien- und Ausdruckswege (`CLAIM-V2-LXF-WCAG-001`, `CLAIM-V2-LXF-UDL-001`). Eine Interaktion braucht daher später mindestens Lernfunktion, gleichwertigen Zugangsweg, erwarteten Output und passende Prüfung. Diese vier Felder sind noch kein fertiges UI-Muster und werden erst in LXF05 normativ formuliert.

## Orchestrierung

Orchestrierung ist kein nachträglicher Lehrkräftehinweis, sondern Teil der Lernarchitektur. Die Forschung zu Classroom-Orchestration-Systemen unterscheidet insbesondere Lehrkraftwahrnehmung, Klasseninstruktion und Koordination zwischen Lernenden. Die Systeme und Outcomes sind heterogen; eine konkrete Dashboard- oder Telemetriearchitektur lässt sich daraus nicht ableiten (`CLAIM-V2-LXF-ORCHESTRATION-001`).

Für das IuM-Lernwerk ist als Richtung verwendbar: Lehrkräfte benötigen sichtbare Phasen, realistische Zeitannahmen, Übergänge zwischen Sozialformen, analoge oder technische Fallbacks und aufgabenbezogene Beobachtungspunkte. Personenbezogene Telemetrie, verdeckte Profilbildung und die Deutung von Klickdauer als Lernstand bleiben ausgeschlossen. Die konkreten Orchestrierungsverträge und Gates sind Aufgabe von LXF06.

## Fachspezifische Grenzen

Die Evidenzbasis ist breit, aber nicht IuM-spezifisch. Viele Befunde stammen aus Mathematik, STEM, allgemeinpsychologischen Lernsettings oder fachübergreifenden Synthesen. Die professionelle Guidance zu Unterricht, Metakognition, UDL und Accessibility übersetzt Forschung oder Standards, prüft aber nicht das konkrete Lernwerk. Für 10- bis 13-Jährige liegen nur teilweise getrennte Analysen vor.

Mit dieser Basis kann weitergearbeitet werden, wenn drei Grenzen verbindlich bleiben:

1. Ein Claim wird erst in LXF04 zu einer Designentscheidung und muss dort eine explizite Entscheidungsbasis, Anwendungsgrenze und beobachtbare Prüfung erhalten.
2. Alters-, Sprach-, Vorwissens- und Bedienannahmen werden in LXF03 als variable Planungsannahmen formuliert, nicht als durchschnittliches oder defizitäres Lernendenprofil.
3. Fachliche Aufgabenqualität, kognitive Zugänglichkeit, technische Konformität, Usability und Lernwirkung werden nicht zusammengezogen. Automatisierte Prüfungen können nur den jeweils geprüften Vertrag bestätigen.

Der Bestand ist damit nicht als fertiges Materialsystem freigegeben. Verwendbar sind die begrenzten Claims und ihre Mechanismen. Zweifel bleiben bei der IuM- und Altersübertragung, der konkreten Aufgabengestaltung, der Hilferücknahme, der Orchestrierung und der Wirksamkeit im realen Unterricht. Definitiv nachzubessern sind pauschale Wirkungsannahmen, Interaktivität ohne Lernfunktion, Accessibility nur als Technikcheck und Selbststeuerung ohne explizite Vermittlung.

## Quellenentscheidungen und Aktualitätsrisiko

Das neue V2-Quellenregister ist bewusst enger als der vollständige Phase-0-Bestand: Es enthält die 13 Quellen der adaptierten Lernpsychologie-Claims sowie die zehn in LXF02 geprüften Ergänzungen. Die alte Phase-0-Datei bleibt unverändert und versiegelt. Alle LXF02-Claims referenzieren ausschließlich registrierte, primär geprüfte Quellen.

Die optionale Phase-0-Quelle `SRC-LP-SIGNALING-2018` wird nicht migriert. Sie war nur metadatengeprüft und trug keinen Claim. Für die in V2 tatsächlich benötigte, enger begrenzte Aussage zu Text-Bild-Beziehungen wurde stattdessen die Originalpublikation `SRC-V2-LXF-SIGNAL-2016` primär geprüft und registriert. Damit bleibt der historische Eintrag erhalten, ohne eine unnötige oder ungeprüfte Claimgrundlage fortzuschreiben.

Die DOI-Publikationen besitzen ein geringes inhaltliches Aktualitätsrisiko, verlangen aber vor öffentlicher Wiedergabe eine erneute Rechte- und Locatorprüfung. IBBW, EEF, COGA, UDL und die jeweils aktuelle WCAG-Fundstelle können fortgeschrieben werden und besitzen deshalb ein mittleres Aktualitätsrisiko. Vor LXF07 und vor jeder Veröffentlichung sind diese fünf lebenden oder institutionell fortschreibbaren Fundstellen erneut zu prüfen.

Es wurden keine Effektzahlen in das V2-Register übernommen. Wo die Originalquellen quantitative Synthesen enthalten, bleibt die Aussage qualitativ und mit Population, Vergleichs- und Übertragungsgrenzen versehen. Eine spätere quantitative Nutzung setzt einen eigenen, vollständigen Extraktionsdatensatz voraus.
