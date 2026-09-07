# Prüfvertrag – V2-G5-M06

**Version 0.1 · Status review · keine reale Evidenz.** Verbindliche Basis: [MOD-Spezifikation](../reference-module/specification.json), [Annahme](../reference-module/acceptance.json), [TECH-Befunde](../technical/findings.md), [GOV](../../foundations/governance/governance-contract.json) und [LXF-Gates](../../foundations/learning-experience/experience-gates.json).

## 1. Prüfgegenstand und Entscheidung

Geprüft werden soll, ob eine konkrete Umsetzung der „Prüffahrt im Raster“ fachlich korrekt, zugänglich, mit ehrlichen Speicherwegen bedienbar und in den geplanten fünf Terminen unterrichtlich nutzbar ist. Grundlage ist Klasse 5, Gymnasium Baden-Württemberg, Niveau E; M01 bleibt tatsächliche Voraussetzung, deren Durchführung vor Einsatz zu klären ist. Keine reale Lerngruppe, Termine, Geräte, Umsetzung oder Produkte sind bekannt. Die sieben curricularen Zuordnungen bleiben `unassessed`.

Drei Ansätze wurden abgewogen: Ein bloßes Umbenennen des V1-Gate-B-Pakets würde falsche Zeit-, Schema- und Freigabeannahmen bewahren. Eine neue umfassende Pilotplattform würde vor dem ersten Modul unnötige Datenerhebung und Implementierung erzeugen. **Gewählt ist ein kleines Dokumentenpaket mit geschlossenen Beobachtungskategorien, konkreten Prüfaufgaben und lokaler Vertragsprüfung.** Es schafft die Anforderungen für eine spätere Umsetzung, ohne selbst Daten im Lernmodul zu sammeln.

Die Paketannahme entscheidet über diesen Prüfentwurf. Sie ist getrennt von Implementierung, technischer Durchführung, Lernendennutzung, Unterrichtspilot, Hosting und Veröffentlichung. Eine fachliche Entwicklungsentscheidung darf trotz fehlender realer Nachweise getroffen werden; eine positive Einsatzentscheidung darf daraus nicht entstehen.

## 2. Vier getrennte Prüfpfade

| Pfad | Gegenstand und Instrument | Eintritt / Umfang | Zulässiger Befund |
| --- | --- | --- | --- |
| TECH | Semantik, Versionsbindung, Datenverlust, Recovery, Persistenz, Update, Zugang; technischer Leitfaden | Spätere Modulrevision mit vollständigem Git-SHA, Builddigest, Protokoll- und Materialversion. Automatisierte Tests und reale Zielprüfung getrennt protokollieren. | Einzelprüfung bestanden, fehlgeschlagen, nicht durchgeführt oder begründet nicht anwendbar. Kein Lern- oder Unterrichtsurteil. |
| USE | Finden, eigene Eingabe, Erklärung von Zustand/Spur, Hilfe und Rückkehr | Erst interner Walkthrough durch Lehrkraft/Fachprüfende mit synthetischen Produkten; anschließend gesondert erlaubte Lernendennutzung. Für eine erste Problemsuche 4–6 Lernende, bis 20 Minuten je Nutzungssitzung als **Planungsbudget**. | Bedienhindernisse und Verständlichkeit im geprüften Zugang. Keine Repräsentativität oder Sättigungsbehauptung bei dieser Zahl. |
| TEACH | Durchführung aller fünf Termine, P0–P6, eigene Programmierung, Feedback, Sicherung und Transfer | Erst nach geschlossenem Eintrittsbogen. Explorative Klasse, anschließend Überarbeitung und gesonderte Bestätigung in anderer Klasse. Jeweils der vollständige M06-Entwurf, 225 Minuten. | Kontextbezogene Umsetzbarkeit und beobachtete Produkt-/Prozessqualität. Kein Kausalnachweis. |
| REVIEW | Zusammenführen widerspruchsfreier Befunde, Grenzen und Änderungen | Zuständige Fach-, Technik-, Zugangs- und Unterrichtsprüfende; tatsächliche Personenzuordnung vor Durchführung. | Nacharbeit, nicht beurteilbar oder bereit für eine **menschliche Folgeentscheidung**. Keine automatische Freigabe. |

Die 4–6 Nutzungsfälle dienen dazu, mehrere unterschiedliche Zugänge und Hürden zu suchen. Sind die geplanten Eingabe-/Assistenzwege damit nicht vertreten, wird gezielt ergänzt oder der Geltungsbereich eingegrenzt. Ein erfolgreicher Erwachsenenlauf ist keine Lernendennutzung. Ergebnisse aus Nutzungssitzungen mit vorgeführter S3-Lösung dürfen nicht als unbeeinflusste Unterrichtsleistung derselben Personen gelten; deshalb getrennte Teilnehmende für die explorative Klasse vorsehen.

Die explorative Klasse wird nach tatsächlicher Einsatzabsicht gewählt: Klasse 5 mit bestätigtem M01-Stand und den vorgesehenen Zugängen. Die zweite Klasse prüft die Übertragbarkeit auf einen weiteren konkret beschriebenen Kontext; dieselbe Lehrkraft ist zulässig, wird aber nicht als unabhängige Bestätigung ausgegeben. Keine Auswahl nach erwünschtem Ergebnis oder nach vermeintlich besonders geeigneten Lernenden. Falls nur eine Klasse verfügbar ist, bleibt die Bestätigung offen, statt Wiederholung als zweite Klasse auszugeben.

Nach einer Änderung erhalten Build und Materialien neue Kennungen. TECH wird für betroffene Prüfungen erneut ausgeführt; die Auswirkung auf andere Prüfungen wird begründet. Exploration an Revision A wird nicht als Nachweis für die unverändert funktionierende Revision B ausgegeben. Die Bestätigung untersucht die überarbeitete Fassung und erhält eigene Kontextdaten. Abweichende Zeit-/Materialvarianten brauchen eine neue Protokollfassung vor der Bestätigung.

## 3. Zeit- und Aufgabenbindung

Die [22 MOD-Segmente](../reference-module/specification.json) werden unverändert in `protocol.json` referenziert und kopiert. Summen: Orientierung/Erklärung 35, angeleitete Übung 55, eigene Anwendung 60, Feedback/Revision 40, Sicherung/Transfer 35 Minuten. Alle fünf Termine dauern je 45 Minuten. Die gleiche Summe wie im Altmodul ist keine Übernahme seines Lernwegs.

| Termin | Prüfanker im bestehenden Budget | Unterrichtliche Entscheidung |
| --- | --- | --- |
| T1 | S0/P0, S1/P1; bei Minute 40 eigener Ergänzungsschritt, anschließend angeleiteter Vergleich | Fehlt Verständnis von Drehung/Körper: am Beispiel nachklären, keinen Bedienfehler als Fachdefizit werten. |
| T2 | S2/P2; fachliche Abweichung Aktion 2, technische Grenze Aktion 3; Revision und Körperregel bis Minute 45 | Nur verkleinerte Wiederholungszahl reicht nicht. Fehlt eigener Vergleich: nächste Sitzung mit Ersatzdiagnose beginnen. |
| T3 | P4 in den ersten 5 Minuten vor alter Lösung; S3/P3 und Partnerprüfung | Nach Abruflücke nachsichern. Bei Peerprüfung beide Erklärungen, gemeinsames Kriterium und eigene Revision beobachten. |
| T4 | S3/P3 mit eigener ausführbarer Schleife und Spur; Revision und Sicherung | Kein ALG-005-Nachweis bei Papier, vorgeführtem Code oder bloßer Animation. Fehlender digitaler Beitrag bleibt offen. |
| T5 | S4/P5 in 10 + 15 Minuten; S5/P6 in 15 Minuten; Dossier/Rückkehr in 5 Minuten | Neue Zustandsbedingung und Erkenntnisgrenze sichern. Unfertige Produkte als solche festhalten, kein stiller sechster Termin. |

Eine beobachtende Person erfasst Segmentgrenzen mit einer Uhr **auf Unterrichtsebene**, ohne Schülerzeitmessung. Ist sie nicht verfügbar, notiert die Lehrkraft nach dem Termin nur sicher rekonstruierbare Zeiten und markiert übrige Segmente als unbekannt. Die Auswertung wird entsprechend enger. Beobachtung liegt innerhalb bestehender Handlungen; keine zusätzliche Befragung wird in die 225 Minuten hineingerechnet. Besprechung der Erwachsenen vor/nach Unterricht wird separat geplant: 20 Minuten Vorbereitung, bis 10 Minuten Nachbesprechung je Termin und 30 Minuten Abschlussreview als eigene Organisationsbudgets.

P4-Prüfimpuls: Start `(2,3)`, Ost; `wiederhole 2 [vor; links]`. Vor Wiederanzeige der alten Lösung den Körper entfalten und Zustand nach vier Aktionen begründen: `(3,2)`, West. Die vertraute Legende ist erlaubt, fertige Spur nicht. Das ist eine Konkretisierung der schon vorgesehenen Abrufhandlung, kein zusätzlicher Test. Tatsächlichen Abstand zu T2 lokal erfassen. Erst ein späterer Unterrichtstag wird hier als zeitversetzter Abruf bezeichnet; bei unmittelbar anschließenden Stunden nur unmittelbare Anwendung. Keine Mindestdauer wird als wissenschaftliche Behaltensschwelle behauptet. Ein fehlender späterer Abruf bleibt eine Grenze; zusätzliche Zeit muss ausdrücklich geplant werden.

## 4. Beobachtung und Schwellen

Alle Schwellen sind **projektdefinierte Entscheidungsregeln**, keine Normwerte, Noten oder empirisch validierten Effektgrenzen. Die Kriterien stehen im [Beobachtungspaket](observation-kit.md). Es gibt keine Gesamtpunktzahl und keinen Prozentwert „Kompetenz erreicht“.

| Auslöser | Regel und Begründung | Folge |
| --- | --- | --- |
| Einzelner schwerer Fehler | Datenverlust ohne kontrollierbare Sicherung, fremder Arbeitsstand, unerwartete Datenübertragung, unzugängliche Kernhandlung oder erhebliche Belastung | Betroffenen technischen oder Lernendenpfad sofort stoppen; keine Mehrheits- oder Quotenabwägung. Sichere fachliche Alternative anbieten, Ereignis zuständig klären. |
| Wiederholtes Bedienhindernis | Dasselbe reproduzierbare Hindernis in zwei getrennten Nutzungssituationen, trotz geplanter Bedienhilfe | Gestaltungsnacharbeit. Zwei Vorkommnisse schützen vor dem Übersehen eines wiederkehrenden Problems; sie schätzen keine Häufigkeit in der Klasse. Ein einzelnes plausibles Hindernis bleibt ein offener Befund. |
| Produkt-/Prozesskriterium | Je Kriterium zwei verschiedene eigene Beiträge im vorgesehenen Fenster sichten, Auswahl im Raum wechseln; keine Personenkennungen notieren | `beobachtet`, wenn beide die beschriebenen Anker zeigen; `teilweise`, wenn nur einer oder Teilanker; `nicht-beobachtet`, wenn beide trotz Gelegenheit fehlen; `nicht-beurteilbar`, wenn weniger als zwei geeignete Gelegenheiten. Die Kategorie beschreibt nur diese Sichtung. |
| Fachliche Fehlvorstellung | Falsche Körpergrenze, Endzustand statt Fahrt, Grafik ohne Anweisungsbezug oder Hilfe ersetzt Eigenleistung | Sofort produktbezogen nachklären; vor positiver Umsetzbarkeitsaussage erneute eigene Anwendung sichten. Keine automatische individuelle Kompetenzdiagnose. |
| Zeitabweichung | Segmentabweichung über 5 Minuten löst einen Ursachenvermerk aus; Grenze ist Arbeitsheuristik. Jede Überschreitung von 45 Minuten oder ausgelassene Kernhandlung widerlegt den unveränderten Terminplan. | Tatsächliche Mehrzeit und entfallene Funktion nennen, Entwurf nacharbeiten. Zeit durch gestrichene Revision/Sicherung zu sparen gilt nicht als Zeitpassung. |
| Fehlender Beleg / Widerspruch | Nicht durchgeführter Test, nicht beobachtbarer Prozess, unpassender Build oder ungeklärte Hilfesituation | `nicht-beurteilbar`; nicht als null Fehler, Misserfolg der Person oder positives Ergebnis behandeln. |

Die zwei Beiträge je Kriterium begrenzen Beobachtungsaufwand und verhindern ein Urteil aus nur einer Vorführung. Sie repräsentieren die Klasse nicht. Kritische Gegenbefunde an anderen Stellen werden zusätzlich erfasst und haben Vorrang. Eine Lehrkraft braucht keine vollständige Beobachtungsabdeckung zu simulieren: Unterricht unterstützen hat Vorrang, fehlende Abdeckung wird offen dokumentiert.

## 5. Schutz vor falschen Schlussfolgerungen

Die vorliegende Semantikprobe bestätigt V1-Bewegungen und die entfaltete S3-Fahrt. Sie bestätigt **nicht** den neuen Editor, den Schleifenkörper mit fünf Anweisungen oder die V2-Laufzeit. Die acht TECH-Befunde bleiben bis zu konkreter Nacharbeit und Prüfung offen. Eine Gerätezeile wird nur für einen wirklich geprüften Zielzugang als bestanden geführt; ausgeschlossene Profile bleiben ausgeschlossen, ungetestete bleiben ungetestet.

Lernendenrückmeldung erfolgt optional im Nutzungsgespräch mit zwei Fragen: „War klar, was du als Nächstes tun konntest?“ und „Konntest du mit der Hilfe selbst weiterarbeiten?“ Antworten können passen / teilweise / nicht passen / keine Antwort lauten. Sie werden unmittelbar für Nachfragen genutzt und **nicht als einzelne Antworten, Häufigkeiten oder Zitate gespeichert**. Ein sachliches Bedienproblem wird ohne Personenbezug als Problemkategorie notiert. Damit entfallen numerische Zufriedenheitsauswertung, Mindestzahl zehn und Kleingruppen-Rückschluss aus Antworttabellen. Kein Ersatz für P1/P2/P3/P5/P6.

Für die Unterrichtsauswertung bleiben nur die beschriebenen Kategorien der gezielten Sichtung. Kein dauerhaftes P0/P4-Archiv, keine Lernproduktkopien, keine Ranglisten, Telemetrie oder privaten Mediennutzungsfragen. Schulisch zulässige Arbeit am eigenen Dossier und seine Rückgabe sind von Pilotdaten getrennt. Reale Umsetzung dieses Datenwegs ist noch zu prüfen.

## 6. Eintritt und offene Übergaben

Vor TECH an echten Geräten: Arbeitsauftrag, konkrete Zielkonfiguration, synthetische Testdaten und zuständige Technikrolle. Vor Hosting: GOV-Q-OPERATOR und zutreffende Rechteprüfung. Vor jeder Nutzung mit Lernenden: GOV-Q-SCHOOL, betroffene Fach-/Zugangsprüfung, passende Information, Daten-/Löschentscheidung, verfügbare sichere Ersatzhandlung und ausdrückliche Durchführungserlaubnis. Vor TEACH zusätzlich realer M01-Stand, fünf Termine, Geräteverteilung, Materialversionen MAT-01–10 und zuständige Lehr-/Beobachtungsrollen.

GOV-Q-REVIEWERS bleibt offen, bis tatsächliche Personen und Prüfumfänge benannt sind. Jan entscheidet über das Projekt; er wird nicht automatisch Betreiber, schulischer Verantwortlicher oder unabhängiger Prüfer. CUR-Q-002 bleibt außerhalb dieses Moduls offen. Papierfallback erhält Diagnose, Grafik, Revision und Transfer, aber nicht die tatsächlich ausgeführte eigene Programmierung.

Für den aktuellen Auftrag sind alle realen Pfade `not-run`, der Pilot `not-started`, Veröffentlichung `closed`. Die Designarbeit ist prüfbar abgeschlossen, sobald Paket, Bindung und Prüfbericht vollständig vorliegen. Es entsteht noch kein neuer Implementierungsplan für das Lernmodul.
