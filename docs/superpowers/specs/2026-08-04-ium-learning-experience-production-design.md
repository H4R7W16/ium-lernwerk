# IuM-Lernwerk – Forschungsbasis und Experience-Strategie

- **Task:** LXP01 Learning-UX-Forschungsbasis und Experience-Strategie entwickeln
- **Status:** zur schriftlichen Nutzerprüfung nach freigegebenem Gesamtdesign
- **Fassung:** 1.0
- **Datum:** 4. August 2026
- **Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
- **Ausgangsstand:** main auf Commit 3498838
- **Arbeitsgrenze:** Strategie und Spezifikation; kein Produktcode, keine reale Pilotierung, kein Preview-Deployment

## 1. Entscheidung

Das IuM-Lernwerk erhält eine zweistufige Experience-Architektur:

1. Der **Lernwerk-Kosmos** macht Module, Progression, Voraussetzungen, Wahlmöglichkeiten und spätere Wiederaufnahmen verständlich.
2. Das **lehrkraftorchestrierte Lernstudio** führt innerhalb eines Moduls durch eine fokussierte Folge fachlicher Lernhandlungen.

Der Kosmos ist die Umgebung für Überblick, Auswahl und Zusammenhang. Das Lernstudio ist die Umgebung für konzentriertes Lernen. Innerhalb eines Lernstudios werden nicht alle Inhalte, Werkzeuge, Hilfen, Statusmeldungen und Folgehandlungen gleichzeitig angeboten. Die Oberfläche zeigt vorrangig:

- den aktuellen fachlichen Zweck;
- die aktuelle Lernhandlung;
- die dafür notwendigen Repräsentationen und Werkzeuge;
- ein erkennbares Qualitätskriterium;
- den nächsten sinnvollen Schritt;
- den Anschluss an gemeinsame Unterrichtsphasen.

Die grundlegende Experience-Grammatik lautet:

~~~text
orientieren
→ Vorwissen oder Erwartung aktivieren
→ denken und entscheiden
→ fachlich handeln
→ Wirkung oder Ergebnis beobachten
→ Rückmeldung interpretieren
→ prüfen und revidieren
→ sichern und übertragen
→ später wiederanknüpfen
~~~

Die bestehende siebenphasige Modulgrammatik bleibt fachlich gültig. Die Experience-Strategie übersetzt sie in verständliche, fokussierte und wiederaufnehmbare Nutzungssituationen.

## 2. Ziel

Das IuM-Lernwerk soll jederzeit fünf Fragen beantworten:

1. **Warum bin ich hier?**
2. **Was ist jetzt meine fachliche Handlung?**
3. **Woran erkenne ich Qualität oder eine relevante Abweichung?**
4. **Wie kann ich sinnvoll weiterarbeiten, Hilfe nutzen oder revidieren?**
5. **Wie verbindet sich mein aktueller Schritt mit dem gemeinsamen Unterricht und dem späteren Lernweg?**

Eine gute Experience ist daher nicht mit einer attraktiven Oberfläche gleichzusetzen. Sie verbindet:

- fachliche Kohärenz;
- verständliche Orientierung;
- kognitive Zugänglichkeit;
- sinnvolle Autonomie;
- informationshaltige Rückmeldung;
- sichtbare Produktverbesserung;
- barrierearme Interaktion;
- Lehrkraftorchestrierung;
- Local First, Offlinefähigkeit und Datenschutz;
- eine ästhetisch sorgfältige, aber lernfunktionale Gestaltung.

## 3. Status- und Gategrenze

Mit dieser Spezifikation werden ausschließlich Forschungsbasis, Experience-Ziel, Qualitätsmodell und drei vertikale Referenzsituationen festgelegt.

Nicht freigegeben werden:

- Produktarchitektur im technischen Sinn;
- konkrete Seitentypen und Navigationskomponenten;
- visuelle Stilrichtung, Typografie, Farbe oder Illustration;
- Komponentenbibliothek oder Design Tokens;
- Produktcode;
- Neufassung von IUM-5-CORE-05;
- Preview-Deployment;
- reale Geräte-, Unterrichts- oder LMS-Prüfung;
- Pilotierung;
- Produktrelease oder Statushochsetzung.

Die spätere Folge bleibt:

~~~text
LXP01 Forschungsbasis und Experience-Strategie
→ LXP02 Produktarchitektur, Navigation und Lernreise
→ LXP03 drei vertikale Experience-Entwürfe
→ LXP04 Design- und Interaktionssystem
→ LXP05 IUM5-Neufassung
→ LXP06 interne Produktvalidierung
→ LXP07 Produktions- und Ausrollsystem
~~~

LXP02 darf erst nach schriftlicher Freigabe dieser Spezifikation präzisiert werden.

## 4. Evidenzregel

Die Spezifikation unterscheidet:

| Status | Bedeutung | Zulässige Verwendung |
|---|---|---|
| bestehender geprüfter Claim | im Phase-0-Claim-Ledger als reviewed kontrolliert | tragende Designheuristik innerhalb der dokumentierten Grenzen |
| ergänzende Meta-Analyse oder systematischer Review | für LXP01 primär oder über Originalpublikation geprüft | Lücke schärfen und vorsichtige Experience-Hypothese begründen |
| professioneller oder normativer Standard | offizielle Quelle, aber kein Wirksamkeitsnachweis | Accessibility-, Prozess- oder Designbaseline |
| lokaler Produktaudit | reproduzierbare Sichtung des aktuellen Stands | konkreten Handlungsbedarf beschreiben, nicht Lernwirkung behaupten |
| Projektentscheidung | schriftlich freigegebene Produktprämisse | Architektur und Scope verbindlich begrenzen |
| Designhypothese | begründete Übertragung auf IuM 5–7 | in LXP03 und LXP06 gezielt prüfen |

Keine Quelle wird über ihren Geltungsbereich hinaus als Beweis ausgegeben. Insbesondere folgen aus:

- WCAG-Konformität keine schulische Usability und keine Lernwirkung;
- positiven Motivationseffekten keine Pflicht zu Gamification;
- Segmentierung keine universelle Zahl von Seiten, Schritten oder Minuten;
- Classroom-Orchestration-Forschung kein Auftrag zu personenbezogener Lernanalyse;
- UDL-Leitlinien kein domänenspezifischer Wirksamkeitsnachweis für IuM 5–7;
- einem lokalen Oberflächenbefund keine Aussage über reale Schülerinnen und Schüler.

## 5. Bestehende Forschungsbasis

### 5.1 Bereits belastbar abgedeckt

Die Phase-0-Forschung trägt bereits:

- Unterrichtsqualität über kognitive Aktivierung, konstruktive Unterstützung und Führung statt über Medienlabels: CLAIM-LP-001;
- Vorwissen und Vorstellungen als aufgabenbezogene Anschlussinformation ohne Defizitprofil: CLAIM-LP-002, CLAIM-INF-006 und CLAIM-INF-010;
- Cognitive Load als Verhältnis von Aufgabe, Vorwissen, Darstellung und Umgebung: CLAIM-LP-003;
- aktive Worked Examples, Selbsterklärung und Scaffolding: CLAIM-INF-004, CLAIM-INF-005, CLAIM-LP-004, CLAIM-LP-005 und CLAIM-LP-006;
- Abruf, Verteilung, Transfer und informationshaltiges Feedback: CLAIM-LP-007 bis CLAIM-LP-010;
- Autonomieunterstützung mit Struktur und sichtbaren Selbstregulationshandlungen: CLAIM-LP-011 und CLAIM-LP-013;
- vorbereitete Exploration mit expliziter Konsolidierung: CLAIM-LP-012 und CLAIM-INF-002;
- fachliche Programmierpraktiken, PRIMM und begründetes Debugging: CLAIM-INF-002, CLAIM-INF-003 und CLAIM-INF-007;
- aktive, mehrschrittige Medienanalyse: CLAIM-MED-001 bis CLAIM-MED-006;
- sensible Themen ohne persönliche Offenlegung oder Risikoprofil: CLAIM-MED-007 bis CLAIM-MED-010;
- begründete Digital-/Analogwahl: CLAIM-LP-001, CLAIM-LP-003, CLAIM-INF-009 und CLAIM-DLE-014;
- Local First, Datenminimierung und ausfalltolerantes Speichern: CLAIM-DLE-004 bis CLAIM-DLE-006;
- WCAG 2.2, gleichwertige Bedienpfade und Nutzerbeteiligung: CLAIM-DLE-001 bis CLAIM-DLE-003;
- Offline-, Browser- und Updateverträge: CLAIM-DLE-007, CLAIM-DLE-008, CLAIM-DLE-012 und CLAIM-DLE-013;
- offene Lizenzen und bearbeitbare OER-Rechteketten: CLAIM-MED-013 und CLAIM-DLE-009 bis CLAIM-DLE-011.

Die 15 vorhandenen Designprinzipien bleiben gültig. LXP01 ersetzt sie nicht, sondern ordnet sie zu einer zusammenhängenden Experience.

### 5.2 Vor LXP01 nicht ausreichend operationalisiert

Die vorhandene Forschungsbasis beantwortet noch nicht hinreichend:

1. Wie Lernende einen mehrstündigen digitalen Lernweg schnell verstehen und sicher wiederaufnehmen.
2. Wie komplexe Lernhandlungen schrittweise offengelegt werden, ohne fachliche Zusammenhänge zu zerlegen.
3. Wie Fortschritt als wachsende fachliche Handlungsfähigkeit und Produktverbesserung erlebbar wird.
4. Wie Motivation aus Relevanz, Kompetenz, Autonomie, Zugehörigkeit und sorgfältiger Gestaltung entsteht, ohne Belohnungsschicht.
5. Wie die Lehrkraft gemeinsame Phasen, Einzelarbeit, Partnererklärung und Sicherung steuert, ohne Konten oder Live-Telemetrie.
6. Wie technische Accessibility um kognitive Zugänglichkeit, verständliche Kontrollbeziehungen und kurze kritische Pfade ergänzt wird.
7. Wie Infrastrukturstatus, Speicherung und Offlinefähigkeit vorhanden bleiben, ohne die Lernhandlung permanent zu überlagern.
8. Wie das Portal Überblick und Wahl ermöglicht, ohne innerhalb eines Moduls eine offene Gesamtoberfläche zu erzwingen.

## 6. Ergänzende LXP01-Forschungsbasis

### 6.1 LXP-SRC-SDT-2024 – Motivation und psychologische Grundbedürfnisse

- **Quelle:** Wang, Y., Wang, H., Wang, S., Wind, S. A. und Gill, C. (2024). A systematic review and meta-analysis of self-determination-theory-based interventions in the education context. Learning and Motivation, 87, 102015.
- **DOI:** https://doi.org/10.1016/j.lmot.2024.102015
- **Art:** systematischer Review und Meta-Analyse
- **Umfang:** 36 Interventionen im Review; 31 Artikel, 137 Effektgrößen und 9.433 Teilnehmende in der Meta-Analyse

**Befund für LXP01:**

- Interventionen können intrinsische Motivation und Autonomieunterstützung verbessern.
- Kompetenzunterstützung zeigt teilweise positive, aber weniger konsistente Effekte.
- Für Zugehörigkeit ergab sich kein stabiler Gesamteffekt.
- Wirkungen hängen von Kontext, Umsetzung und Zielgruppe ab.

**Grenzen:**

- sehr hohe Heterogenität;
- Hinweise auf Publikationsbias;
- gemischte Altersgruppen, Fächer und Interventionstypen;
- überwiegend kurze Wirkungszeiträume;
- begrenzte Langzeit- und Verhaltensmaße;
- keine direkte Prüfung eines offenen Local-First-Lernwerks für IuM 5–7.

**Zulässige Designhypothese:**

Motivation wird über relevante Ziele, passende Herausforderung, echte begrenzte Wahl, verständliche Kriterien, handlungsorientierte Rückmeldung, Produktverbesserung und soziale Einbettung unterstützt. Punkte, Badges, Ranglisten, Streaks oder künstliche Verknappung folgen daraus nicht.

### 6.2 LXP-SRC-SEGMENT-2019 – Segmentierung

- **Quelle:** Rey, G. D., Beege, M., Nebel, S., Wirzberger, M., Schmitt, T. H. und Schneider, S. (2019). A Meta-analysis of the Segmenting Effect. Educational Psychology Review, 31, 389–419.
- **DOI:** https://doi.org/10.1007/s10648-018-9456-4
- **Art:** Meta-Analyse

**Befund für LXP01:**

- sinnvolle Segmentierung kann Behalten und Transfer unterstützen;
- Segmentierung kann kognitive Belastung senken;
- lernendengesteuerte oder klar gegliederte Abschnitte können Verarbeitungspausen ermöglichen;
- die Lernzeit kann steigen.

**Grenzen:**

- Schwerpunkt auf multimedialem Instruktionsmaterial, nicht auf mehrstündigen interaktiven Lernwerken;
- heterogene Inhalte, Altersgruppen und Segmentierungsarten;
- kein universeller optimaler Umfang eines Schritts;
- Segmentierung kann fachliche Zusammenhänge zerstückeln, wenn sie nur nach Bildschirmgröße erfolgt.

**Zulässige Designhypothese:**

Ein Lernstudio zeigt einen fachlich vollständigen Handlungsschritt und hält dessen Kontext sichtbar. Es schaltet nicht bloß nach Zeit oder Klickzahl weiter und versteckt keine für die aktuelle Entscheidung notwendige Information.

### 6.3 LXP-SRC-SIGNAL-2016 – Signaling zwischen Repräsentationen

- **Quelle:** Richter, J., Scheiter, K. und Eitel, A. (2016). Signaling text-picture relations in multimedia learning: A comprehensive meta-analysis. Educational Research Review, 17, 19–36.
- **DOI:** https://doi.org/10.1016/j.edurev.2015.12.003
- **Art:** Meta-Analyse
- **Umfang:** 27 Studien, 45 Paarvergleiche, 2.464 Teilnehmende

**Befund für LXP01:**

- Signale, die zusammengehörige Informationen in Text und Bild erkennbar verbinden, zeigen im Mittel einen kleinen bis mittleren positiven Effekt auf Verstehen und Transfer;
- der Nutzen ist bei geringerem Vorwissen tendenziell größer;
- Signale unterstützen die Integration mehrerer Repräsentationen.

**Grenzen:**

- Signaling ist kein allgemeiner Auftrag zu mehr Farbe, Animation oder Hervorhebung;
- bei hohem Vorwissen kann zusätzliche Führung unnötig werden;
- Befunde gelten nicht automatisch für jede dynamische Bedienoberfläche.

**Zulässige Designhypothese:**

Aktueller Befehl, betroffene Darstellung, Zustandsänderung, Rückmeldung und relevante Laufspur werden semantisch und visuell korrespondenztreu markiert. Dekorative Akzente dürfen nicht mit fachlichen Signalen konkurrieren.

### 6.4 LXP-SRC-W3C-COGA-2021 – kognitive Accessibility

- **Quelle:** W3C Web Accessibility Initiative. Supplemental Guidance to WCAG 2: Cognitive Accessibility Guidance.
- **URL:** https://www.w3.org/WAI/WCAG2/supplemental/
- **Art:** offizielle ergänzende Accessibility Guidance
- **Status:** professionelle Guidance, nicht Bestandteil der normativen WCAG-Konformitätsanforderungen

**Für LXP01 relevante Muster:**

- Zweck von Seite, Abschnitt und Kontrolle klar machen;
- vertraute Hierarchie und konsistente Gestaltung;
- jeden Schritt und die wichtigste Aktion verständlich anzeigen;
- Beziehungen zwischen Kontrolle und betroffener Information eindeutig machen;
- kurze kritische Pfade;
- zu viel gleichzeitig sichtbaren Inhalt vermeiden;
- Hilfen auffindbar und kontextnah anbieten;
- Prozesse nicht unnötig auf Erinnerung stützen;
- Fehlerkorrektur, Rückkehr und Datenverlustschutz unterstützen.

**Grenzen:**

- kein domänenspezifischer Lernwirkungsnachweis;
- ersetzt weder WCAG 2.2 noch Tests mit Lernenden und Menschen mit Behinderungen.

**Zulässige Designfolge:**

Kognitive Accessibility wird zu einem eigenen Reviewstrang neben technischer WCAG-Konformität, fachlicher Richtigkeit und Lernwirksamkeit.

### 6.5 LXP-SRC-UDL30-2024 – UDL als professionelles Prüfraster

- **Quelle:** CAST (2024). Universal Design for Learning Guidelines 3.0.
- **URL:** https://udlguidelines.cast.org/
- **Art:** professionelles Designframework

**Für LXP01 relevante Prüffragen:**

- Sind Wahl und Autonomie fachlich sinnvoll?
- Sind Relevanz, Wert und Authentizität erkennbar?
- Sind Ziel und Zweck verständlich?
- Passen Herausforderung und Unterstützung zusammen?
- Ist Rückmeldung handlungsorientiert?
- Können Lernende Fortschritt überwachen?
- Gibt es mehrere zugängliche Wahrnehmungs-, Interaktions- und Ausdruckswege?

**Grenzen:**

- die Guidelines werden nicht als kausaler Wirksamkeitsnachweis behandelt;
- einzelne Optionen werden nicht als Pflichtkomponenten umgesetzt;
- mehr Wahl ist nicht automatisch besser;
- verschiedene Ausdruckswege müssen dasselbe fachliche Ziel tragen.

### 6.6 LXP-SRC-COS-2023 – Classroom Orchestration

- **Quelle:** Feng, S., Zhang, L., Wang, S. und Cai, Z. (2023). Effectiveness of the functions of classroom orchestration systems: A systematic review and meta-analysis. Computers & Education, 203, 104864.
- **DOI:** https://doi.org/10.1016/j.compedu.2023.104864
- **Art:** systematischer Review und Meta-Analyse
- **Umfang:** 67 Systeme; 22 empirische Publikationen mit 57 Studien und Effektgrößen

**Befund für LXP01:**

Die Forschung unterscheidet drei nützliche Funktionsfamilien:

1. Lehrkraftorientierung und Awareness;
2. Unterrichtssteuerung;
3. Koordination von Lernenden und Sozialformen.

Teacher Awareness war ein relevanter Moderator; der Gesamtbefund wird als mittlerer Effekt berichtet.

**Grenzen:**

- eingeschlossene Systeme, Designs, Fächer und Messungen sind heterogen;
- der Suchstand endet 2021;
- viele Systeme nutzen Datenanalyse oder Dashboards, die mit der IuM-Datenprämisse nicht vereinbar sind;
- aus einem mittleren Gesamteffekt folgt kein Auftrag zu Live-Tracking.

**Zulässige Designhypothese:**

IuM übernimmt die Funktionsfamilien, nicht die Datentechnik. Lehrkraftorientierung entsteht durch vorbereitete fachliche Hinweise, sichtbare gemeinsame Haltepunkte, frische Kurzfälle, Rollen- und Zeitoptionen sowie lokal oder analog wahrnehmbare Lernprodukte. Es entsteht kein personenbezogenes Lehrkräftedashboard.

## 7. Audit der aktuellen Produkterfahrung

### 7.1 Auditmethode

Geprüft wurden:

- das freigegebene Gesamtdesign;
- die IUM-5-CORE-05-Modulspezifikation;
- die Phase-0-Forschungssynthese und Designprinzipien;
- der lokale Produktionsbuild auf main/3498838;
- Portalstart und IUM5-Modulpfad im Browser;
- semantischer DOM-Pfad;
- Desktopansicht bei 1280 × 720;
- schmale Ansicht bei 390 × 844;
- sichtbare Zustände vor und nach Auswahl einer Produktkarte.

Es wurden keine Nutzerstudie, keine Wirksamkeitsprüfung und kein Realgerätetest durchgeführt.

### 7.2 Stärken des Bestands

Der aktuelle Stand besitzt:

- klare semantische Regionen, Überschriften, Formulare und Statusmeldungen;
- beschriftete Schaltflächen und Textalternativen;
- Tastatur-, Touch- und textbasierte Bedienkonzepte;
- Local-First-, Export-, Import- und Löschpfade;
- explizite Gate- und Arbeitsstandskennzeichnung;
- einen fachlich tragfähigen Predict–Run–Compare–Repair-Zyklus;
- transparente Lernziele und Qualitätskriterien;
- eine echte Revision statt bloßer Richtig-/Falsch-Rückmeldung;
- datensparsame Hilfen ohne Profilbildung;
- funktionierenden Reflow ohne horizontalen Dokumentüberlauf in der geprüften schmalen Ansicht.

Diese Substanz wird bewahrt.

### 7.3 Experience-Probleme des Bestands

In der geprüften Ausgangslage zeigte der Modulpfad:

- ungefähr 8.399 Pixel Dokumenthöhe bei 1280 × 720;
- ungefähr 11.275 Pixel Dokumenthöhe bei 390 × 844;
- 55 sicht- oder fokussierbare Schaltflächen;
- 23 Eingabefelder;
- Lernphasennavigation, Arbeitsauftrag, Aufgabenfamilien, Kartenwahl, Fehlerfälle, Werkstatt, Vorhersage, Ausführung, Laufspur, Revision, Hilfen, Transfer, Selbstcheck und Datenverwaltung in einem zusammenhängenden Dokument;
- zwei prominente Arbeitsstandsbereiche vor dem eigentlichen Lernauftrag;
- technische Speicher- und Verbindungsinformation vor der fachlichen Handlung;
- Navigation über Unterrichtseinheiten und Abschnittsnamen, ohne den aktuellen fachlichen Handlungsschritt ausreichend zu priorisieren;
- viele noch nicht relevante Bedienelemente, bevor die nötigen Voraussetzungen oder Ergebnisse vorliegen;
- eine lange räumliche Distanz zwischen Ursache, Handlung, Rückmeldung und späterer Revision.

### 7.4 Diagnose

Der Bestand ist kein fachlich leerer UI-Prototyp. Das Problem ist vielmehr eine **unzureichende Experience-Komposition**:

- Verträge und Funktionen wurden vollständig sichtbar gemacht, statt als fokussierte Lernreise angeordnet zu werden.
- Technische Ehrlichkeit konkurriert mit dem fachlichen Einstieg.
- Die Oberfläche bildet den Gesamtumfang des Moduls ab, nicht die aktuelle Lernhandlung.
- Fortschritt erscheint überwiegend als Position in einem langen Dokument, nicht als fachlich erkennbare Entwicklung.
- Die Lehrkraftrolle steht im Handbuch, ist aber in der Produkterfahrung nicht als Orchestrierungsrhythmus sichtbar.

Eine reine visuelle Überarbeitung würde diese Diagnose nicht lösen.

## 8. Ansatzvergleich

### 8.1 Ansatz A – orchestriertes Lernstudio

**Kern:** Ein stabiler Arbeitsraum zeigt pro Zustand die aktuelle Lernhandlung, relevante Repräsentationen, Kriterien, Hilfe und nächsten Schritt. Gemeinsame Haltepunkte sind Teil des Lernwegs.

**Stärken:**

- hohe fachliche Fokussierung;
- gute Passung zu Klassen 5–7;
- kompatibel mit Segmentierung, Scaffolding und lehrkraftorchestriertem Unterricht;
- erleichtert kognitive Accessibility;
- kann Local First und Offline ohne Konten tragen;
- unterstützt Revision und Wiedereinstieg.

**Risiken:**

- zu starre Führung;
- künstlich kleinteilige Schritte;
- verdeckte lineare Zwangsführung;
- Gefahr, Wahl und Überblick zu schwächen.

**Gegenmittel:**

- fachlich vollständige Handlungsschritte;
- sichtbare Gesamtkarte;
- begrenzte echte Wahl;
- flexible Lehrkraftpfade;
- nachvollziehbare Rückkehr und Wiederaufnahme.

### 8.2 Ansatz B – narrativer Missionspfad

**Kern:** Module werden als Missionen mit Kontext, Ziel, Etappen und Abschluss erzählt.

**Stärken:**

- klare Relevanz;
- situativer Spannungsbogen;
- gute Anschlussfähigkeit für konkrete Problem- und Gestaltungsaufträge.

**Risiken:**

- Kontext kann das Fachmodell verdecken;
- Mission, Avatar, Punkte oder Level können zum Selbstzweck werden;
- wiederkehrende Narration skaliert schlecht auf heterogene Fachbereiche;
- Transfer aus dem Kontext wird erschwert.

**Urteil:**

Narrative Rahmung bleibt als lokale Aufgabenform möglich, wird aber nicht zur globalen Produktarchitektur.

### 8.3 Ansatz C – offener Lernwerk-Kosmos

**Kern:** Lernende bewegen sich frei zwischen Modulen, Materialien, Werkzeugen und Vertiefungen.

**Stärken:**

- guter Gesamtüberblick;
- echte Modularität;
- flexible Nachnutzung;
- geeignete Portallogik für Lehrkräfte und erfahrene Lernende.

**Risiken:**

- hohe Navigations- und Entscheidungslast;
- Voraussetzungen und Progression werden leicht unsichtbar;
- offene Oberflächen konkurrieren mit fokussierter Begriffsbildung;
- Lernende können Aktivität mit Lernfortschritt verwechseln.

**Urteil:**

Der Kosmos ist die richtige Außenarchitektur, aber nicht die Innenarchitektur eines komplexen Moduls.

### 8.4 Entscheidung

Gewählt wird eine Kombination mit klarer Zuständigkeit:

| Ebene | Primärfunktion | Experience-Modell |
|---|---|---|
| Lernwerk-Kosmos | Überblick, Zusammenhang, Modulwahl, Voraussetzungen, spätere Wiederaufnahme | offen und modular |
| Modulstart | Zweck, Lernprodukt, Zeit, Voraussetzung, gemeinsamer Auftakt | orientierend |
| Lernstudio | fokussierte fachliche Lernhandlung und Revision | geführt mit begrenzter Wahl |
| Sicherung und Transfer | Beleg, Produktverbesserung, Gespräch, Transfer, nächster Anschluss | reflektierend und orchestriert |
| Rückkehr zum Kosmos | Einordnung, nächster Lernweg, Wiedervorlage | anschlussfähig |

## 9. Experience-Nordstern

Das Lernwerk erzeugt eine **ruhige fachliche Handlungsfähigkeit**:

- Lernende wissen, worum es geht.
- Sie sehen nur, was sie für den aktuellen Schritt benötigen.
- Sie treffen echte fachliche Entscheidungen.
- Das System macht Folgen, Zustände und Qualitätskriterien verständlich.
- Rückmeldung führt zu einer nächsten Denkhandlung.
- Fortschritt wird an Verständnis, Beleg und Revision sichtbar.
- Die Lehrkraft kann gemeinsame und individuelle Lernphasen ohne Datendashboard orchestrieren.
- Technische Schutzfunktionen bleiben zuverlässig, aber treten bei störungsfreiem Betrieb hinter das Lernen zurück.

Die Experience darf anspruchsvoll sein. Sie darf nicht unnötig kompliziert sein.

## 10. Experience-Grammatik

### 10.1 Orientieren

Jeder neue oder wiederaufgenommene Lernabschnitt zeigt:

- fachliche Frage oder Auftrag;
- Funktion im Lernweg;
- erwartbares Lernprodukt;
- aktuellen Schritt;
- benötigte Zeit als realistischen Korridor;
- gemeinsame oder individuelle Arbeitsform;
- vorhandenen Arbeitsstand;
- nächsten primären Handlungsaufruf.

Technische Zustände erscheinen nach Dringlichkeit:

- unauffällig bei störungsfreiem Betrieb;
- kontextnah, wenn eine Entscheidung nötig ist;
- prominent, wenn Datenverlust, Offlineunvollständigkeit oder inkompatibler Stand droht.

### 10.2 Denken und entscheiden

Vor Interaktion wird die relevante Erwartung, Vorhersage, Einordnung, Strategie oder Qualitätsentscheidung aktiviert. Die Denkhandlung darf:

- nicht durch eine Animation vorweggenommen werden;
- nicht durch sofort sichtbare Lösungshinweise entwertet werden;
- nicht unnötig als Freitext verlangt werden;
- nicht als stabiles Personenmerkmal gespeichert werden.

### 10.3 Fachlich handeln

Der Arbeitsraum enthält nur Werkzeuge, die die aktuelle Lernhandlung tragen. Jede Kontrolle beantwortet:

- Was verändert sie?
- Welche fachliche Bedeutung hat die Veränderung?
- Wo wird die Wirkung sichtbar?
- Wie kann die Handlung rückgängig gemacht oder geprüft werden?

### 10.4 Wirkung beobachten

Relevante Veränderungen werden:

- im betroffenen Modell sichtbar;
- textlich verfügbar;
- semantisch angekündigt;
- mit der auslösenden Handlung verknüpft;
- bei Bedarf schrittweise steuerbar;
- nicht allein durch Farbe oder Bewegung codiert.

### 10.5 Rückmeldung interpretieren

Rückmeldung folgt der fachlichen Funktion:

1. Ergebnis oder relevante Abweichung benennen.
2. betroffene Stelle, Zustand oder Kriterium sichtbar machen.
3. Vergleich mit Erwartung, Modell oder Qualitätskriterium anregen.
4. einen nächsten Prüfschritt anbieten.
5. auf Wunsch einen strategischen Hinweis öffnen.
6. vollständiges Beispiel erst dann zugänglich machen, wenn es didaktisch vertretbar ist.

### 10.6 Revidieren

Revision ist eine sichtbare Veränderung zwischen mindestens zwei fachlich bedeutsamen Zuständen:

- Ausgangsidee oder Ausgangsprodukt;
- Beleg oder Rückmeldung;
- Reparatur- oder Verbesserungsentscheidung;
- revidierte Fassung;
- kurze Begründung oder Qualitätsprüfung.

Trial-and-error ohne Erwartung, Vergleich oder Begründung gilt nicht als hinreichende Revision.

### 10.7 Sichern und übertragen

Ein Lernabschnitt endet nicht mit einem grünen Zustand. Er erzeugt:

- eine fachliche Kernaussage;
- ein Beispiel oder Lernprodukt;
- ein benanntes Qualitätskriterium;
- eine Modellgrenze oder typische Abweichung;
- einen Transfer auf eine veränderte Beziehung;
- einen späteren Wiedervorlagepunkt.

### 10.8 Wiederanknüpfen

Beim Wiedereinstieg werden nicht alle gespeicherten Daten gezeigt. Sichtbar sind:

- zuletzt sinnvoll abgeschlossener Schritt;
- aktuelles Produkt oder Beleg;
- offene fachliche Handlung;
- kurze Erinnerung an Ziel und Kontext;
- nächster primärer Schritt;
- optional die Gesamtkarte.

## 11. Informationsarchitektur auf Experience-Ebene

Diese Spezifikation legt noch keine konkrete Navigation fest. Sie definiert jedoch fünf notwendige Informationsräume:

### 11.1 Kosmos

- Lernstränge und Jahrgänge;
- Kern-, Vertiefungs-, Transfer- und Projektmodule;
- Voraussetzungen und Anschlüsse;
- empfohlene und flexible Wege;
- Arbeitsstatus und Lizenzinformation;
- Wiederaufnahmen.

### 11.2 Startboard

- fachliche Leitfrage;
- Relevanz und Lernprodukt;
- Voraussetzung;
- Zeitkorridor;
- gemeinsamer Einstieg;
- Start oder Wiederaufnahme;
- verfügbare Fallbacks.

### 11.3 Lernstudio

- aktueller Auftrag;
- Repräsentationen und Werkzeuge;
- aktuelle Denkhandlung;
- Kriterien;
- kontextuelle Hilfe;
- fachliche Rückmeldung;
- Revision.

### 11.4 Sicherungsraum

- Beleg und Produktentwicklung;
- Kernaussage und Modellgrenze;
- Transfer;
- Gesprächsimpuls;
- bewusster Export;
- spätere Wiedervorlage.

### 11.5 Lehrkraftspur

- Unterrichtsziel und fachlicher Hintergrund;
- erwartbare Vorstellungen und Fehler;
- gemeinsame Haltepunkte;
- Zeit- und Sozialformoptionen;
- Fragen, Hilfen und frische Kurzfälle;
- technische Fallbacks;
- nächste Wiederaufnahme.

Die Lehrkraftspur ist kein getrennter Lerninhalt und kein personenbezogenes Dashboard. Sie orchestriert dieselben Lernhandlungen aus einer anderen Rolle.

## 12. Rollenmodell

### 12.1 Lernende

Lernende:

- verstehen Ziel und aktuellen Schritt;
- treffen begrenzte fachliche Wahl;
- erzeugen Vorhersage, Produkt, Beleg oder Revision;
- nutzen Hilfen bewusst;
- können zurückkehren und den eigenen Stand löschen oder exportieren;
- erhalten keine Note, Kompetenzampel oder Rangposition.

### 12.2 Lehrkraft

Die Lehrkraft:

- startet und rahmt Lernphasen;
- wählt Zeit-, Sozialform- und Hilfepfade;
- setzt gemeinsame Haltepunkte;
- beobachtet Produkte, Erklärungen und Gespräche;
- nutzt frische Kurzfälle bei fehlender Evidenz;
- führt Begriffe und Modellgrenzen zusammen;
- plant Wiedervorlagen;
- erhält keine personenbezogene Telemetrie.

### 12.3 Partnerarbeit bei 1:2

Partnerarbeit benötigt fachlich symmetrische Rollen, zum Beispiel:

- steuern;
- vorhersagen und prüfen.

Rollenwechsel erfolgt an fachlich sinnvollen Punkten. Beide Rollen müssen sichtbare Denkhandlungen enthalten. Das Produkt darf nicht dauerhaft einer Person gehören, während die andere nur zusieht.

### 12.4 Produkt- und Plattformsystem

Das System:

- hält Verträge und lokale Zustände zuverlässig;
- zeigt den aktuellen fachlichen Zustand;
- bietet gleichwertige Bedienpfade;
- gibt informationshaltige Rückmeldung;
- bewahrt Datenminimierung;
- entscheidet nicht über Personen, Noten oder Kompetenzstatus.

## 13. Motivationsstrategie

Motivation entsteht aus sechs Produktmechanismen:

### 13.1 Relevanz

Ein Auftrag zeigt ein glaubwürdiges Problem, Phänomen, Gestaltungsziel oder Urteil. Relevanz wird nicht durch künstliche Dramatik behauptet.

### 13.2 Kompetenzerfahrung

Lernende erleben Fortschritt, wenn sie:

- eine bessere Vorhersage treffen;
- eine Zustandsänderung erklären;
- eine Abweichung lokalisieren;
- ein Produkt gezielt verbessern;
- ein Kriterium selbstständig anwenden;
- ein Konzept übertragen.

Kompetenz wird nicht durch Konfetti, Punkte oder pauschales Lob simuliert.

### 13.3 Begrenzte Autonomie

Wahl ist sinnvoll, wenn Alternativen:

- dasselbe Lernziel tragen;
- echte fachliche Entscheidung erlauben;
- in Umfang und Schwierigkeit transparent sind;
- nicht als verdeckte Niveaustufe wirken;
- durch die Lehrkraft begrenzt oder freigegeben werden können.

### 13.4 Zugehörigkeit und gemeinsames Lernen

Das Lernwerk unterstützt:

- Partnererklärung;
- geteilte Modelle;
- anonymisierte Fehlerfälle;
- gemeinsame Sicherung;
- produktbezogenes Peerfeedback;
- kollektive Fragen ohne personenbezogene Offenlegung.

### 13.5 Fortschrittsklarheit

Fortschritt wird primär als fachlicher Zustand angezeigt:

- begonnen;
- Erwartung formuliert;
- erprobt;
- geprüft;
- revidiert;
- gesichert;
- für spätere Wiederaufnahme markiert.

Eine Prozentanzeige ist nur zulässig, wenn der Nenner sachlich stabil und für die Handlung nützlich ist. Klick- oder Seitenfortschritt darf nicht mit Kompetenz verwechselt werden.

### 13.6 Ästhetische Sorgfalt

Gestalterische Qualität soll:

- Ruhe und Wertigkeit vermitteln;
- fachliche Beziehungen hervorheben;
- Schülerarbeiten ernst nehmen;
- Klarheit und Wiedererkennbarkeit erzeugen;
- altersangemessen sein, ohne zu verniedlichen.

Eine konkrete visuelle Sprache wird erst in LXP04 entschieden.

## 14. Inhaltsrhythmus

### 14.1 Mikro-Rhythmus

Ein fokussierter Experience-Schritt enthält typischerweise:

~~~text
kurze Orientierung
→ eine zentrale Denkhandlung
→ eine fachliche Aktion oder Entscheidung
→ eine beobachtbare Wirkung
→ eine Rückmeldung oder Prüfung
→ einen klaren Abschluss oder Übergang
~~~

Nicht jeder Schritt benötigt Freitext, Animation oder explizite Bestätigung.

### 14.2 Meso-Rhythmus

Eine Unterrichtseinheit verbindet:

- gemeinsamen oder angeleiteten Auftakt;
- fokussierte Studioarbeit;
- kurze Partner- oder Austauschfunktion;
- mindestens einen sichtbaren Zwischenstand;
- gemeinsamen oder individuellen Abschluss.

### 14.3 Makro-Rhythmus

Ein mehrstündiges Modul macht sichtbar:

- was bereits begrifflich aufgebaut wurde;
- welche Lernhandlung heute im Zentrum steht;
- welches Produkt weiterentwickelt wird;
- wann Transfer und Sicherung folgen;
- wo später wieder angeknüpft wird.

## 15. Progressive Offenlegung

### 15.1 Grundregel

Nur Inhalte und Kontrollen, die für die aktuelle Lernhandlung oder eine notwendige Entscheidung relevant sind, stehen im primären Arbeitsraum.

### 15.2 Immer erreichbar

Trotz Fokussierung bleiben jederzeit erreichbar:

- Ziel und aktueller Schritt;
- Gesamtkarte des Lernwegs;
- Hilfe;
- Accessibility- und Anzeigeoptionen;
- Speicherstatus in angemessener Priorität;
- Export und Löschen über einen stabilen Datenbereich;
- Rückkehr zum Kosmos.

### 15.3 Nicht zulässig

Progressive Offenlegung darf nicht:

- Voraussetzungen verbergen;
- notwendige Kriterien erst nach einer Entscheidung zeigen;
- eine irreversible Aktion ohne Folgenhinweis auslösen;
- fachliche Zusammenhänge auseinanderreißen;
- Tastatur- oder Screenreaderpfade verlängern, ohne Orientierung zu erhalten;
- einen offenen Hilfepfad durch Telemetrie ersetzen.

## 16. Rückmeldung und Revision

### 16.1 Rückmeldungsarten

| Art | Funktion | Beispiel |
|---|---|---|
| Ergebnisrückmeldung | beobachtbaren Zustand benennen | Auftrag noch nicht erfüllt |
| Prozessrückmeldung | relevante Stelle oder Beziehung zeigen | erste Abweichung in Schritt 4 |
| Strategierückmeldung | nächsten Prüfschritt anbieten | vergleiche Blickrichtung vor und nach der Drehung |
| Kriterienrückmeldung | Produkt gegen Qualitätsmerkmal prüfen | Begründung nennt noch keinen Beleg |
| Modellrückmeldung | Modellgrenze oder Begriff klären | digital ist nicht automatisch algorithmisch |

### 16.2 Unzulässige Rückmeldung

- pauschales Personenlob;
- beschämende oder defizitorientierte Sprache;
- Punkte oder Sterne ohne fachliche Information;
- Lösung vor Vergleich und Denkhandlung;
- wiederholtes „falsch“ ohne lokalisierbaren Bezug;
- automatisierte Diagnose;
- eine grüne Oberfläche als Freigabe- oder Kompetenzurteil.

### 16.3 Revisionsvertrag

Jede zentrale Lernhandlung muss später beantworten können:

- Was war der Ausgangsstand?
- Welche Beobachtung oder welches Kriterium war relevant?
- Welche Änderung wurde vorgenommen?
- Was ist jetzt besser, präziser oder tragfähiger?
- Wie wird dies an einem neuen Fall geprüft?

## 17. Fortschritt, Persistenz und Wiedereinstieg

### 17.1 Progressionsachsen

Fortschritt wird auf drei getrennten Ebenen beschrieben:

1. **Lernwegfortschritt:** Position und Funktion im Modul oder Lernstrang.
2. **Produktfortschritt:** relevante Entwicklung zwischen Ausgangs- und Revisionsstand.
3. **Konzeptfortschritt:** zunehmend anspruchsvolle Anwendung, Erklärung oder Übertragung.

Keine Achse wird aus Klickzeit, Fehlversuchen oder Hilfenutzung abgeleitet.

### 17.2 Minimaler Wiedereinstiegsstand

Der lokale Zustand enthält nur, was für fachliche Kontinuität erforderlich ist:

- aktueller Lernabschnitt;
- letzter sinnvoll abgeschlossener Schritt;
- relevantes Ausgangsprodukt;
- bestätigter Beleg;
- revidiertes Produkt;
- notwendige Begründung;
- Transfer- oder Sicherungsstand;
- Schemaversion.

### 17.3 Wiedereinstiegsdarstellung

Nach Rückkehr sieht die lernende Person:

- „Darum geht es“;
- „Hier warst du“;
- „Das ist dein letzter relevanter Stand“;
- „Das ist jetzt der nächste Schritt“;
- optional „Gesamten Lernweg ansehen“.

Das System rekonstruiert keine Lernendenbiografie.

## 18. Lehrkraftorchestrierung

### 18.1 Drei Funktionsfamilien

Die Experience unterstützt:

1. **Orientierung:** Ziel, Zeit, Voraussetzungen, erwartbare Wege und aktuelle Unterrichtsphase verstehen.
2. **Steuerung:** gemeinsame Haltepunkte, Erklärungen, Sozialformwechsel, Hilfen und Sicherung auslösen.
3. **Koordination:** Einzelarbeit, Partnerrollen, Gruppenvergleich und gemeinsame Produkte funktional organisieren.

### 18.2 Orchestrierung ohne Telemetrie

Nicht verwendet werden:

- Konten;
- Klassenlisten;
- Liveansichten einzelner Geräte;
- zentrale Fortschrittsdaten;
- Klick-, Zeit- oder Fehlerstatistiken;
- automatisierte Gruppierung;
- Kompetenzprognosen.

Stattdessen verwendet das Lernwerk:

- sichtbare Haltepunktsymbole im Lernweg;
- gemeinsame Kurzfälle;
- projizierbare Modelle oder Aufgaben;
- Rollenhinweise;
- Produkt- und Gesprächskriterien;
- lokale Selbstauskunft;
- Handzeichen, Partnervergleich und Lehrkraftbeobachtung;
- bewusst exportierte Produkte, wenn dies für den Unterricht nötig ist.

### 18.3 Lehrkraftspur pro Lernabschnitt

Jeder zentrale Abschnitt dokumentiert:

- Lernfunktion;
- erwartbaren Zeitkorridor;
- Sozialform;
- notwendige Erklärung;
- typische Vorstellungen oder Abweichungen;
- beobachtbares Lernprodukt;
- geeignete Rückfrage;
- verfügbare Hilfe;
- gemeinsamen Haltepunkt;
- Fallback und nächste Wiederaufnahme.

## 19. Accessibility und kognitive Zugänglichkeit

### 19.1 Technische Baseline

WCAG 2.2 AA bleibt vollständig verbindlich. Zentrale Pfade funktionieren:

- mit Tastatur;
- mit Touch;
- ohne Drag-and-drop;
- ohne Farberkennung;
- ohne Animation;
- bei reduziertem Bewegungswunsch;
- bei 320 CSS-Pixeln Reflow;
- bei 200 Prozent Zoom;
- mit Text- und Assistive-Technology-Pfad.

### 19.2 Kognitive Accessibility

Zusätzlich werden geprüft:

- klarer Zweck jeder Seite und Region;
- eine erkennbare primäre Handlung;
- konsistente Hierarchie und Position wiederkehrender Funktionen;
- verständliche Labels;
- eindeutige Beziehungen zwischen Kontrolle und Wirkung;
- kurze kritische Pfade;
- begrenzte gleichzeitige Auswahl;
- Rückkehr, Undo und Fehlerkorrektur;
- kontextnahe Hilfe;
- keine unnötige Gedächtnisbelastung;
- verständlicher Wiedereinstieg;
- kein Informationsverlust durch progressive Offenlegung.

### 19.3 Gleichwertigkeit

Alternative Darstellungen sind gleichwertig, wenn sie:

- dasselbe fachliche Ziel tragen;
- dieselbe zentrale Entscheidung oder Erklärung verlangen;
- vergleichbare Rückmeldung ermöglichen;
- denselben Produkt- oder Revisionsvertrag erfüllen.

Eine reine Beschreibung eines visuellen Ergebnisses ist nicht automatisch gleichwertig mit einer interaktiven Modellhandlung.

## 20. Local First, Offline und Datenschutz in der Experience

### 20.1 Ruhemodus

Bei funktionierendem Speichern und vollständig verfügbarem Offlinebestand bleibt Infrastrukturstatus zurückhaltend. Er ist erreichbar, aber nicht vor jeder fachlichen Handlung dominant.

### 20.2 Handlungsmodus

Wenn eine Nutzerentscheidung nötig ist, zeigt die Experience:

- was nicht verfügbar oder gefährdet ist;
- welche Arbeit betroffen ist;
- welche sichere Handlung möglich ist;
- ob ein Export empfohlen wird;
- wie später wiederaufgenommen werden kann.

### 20.3 Alarmmodus

Prominente Unterbrechung ist nur zulässig bei:

- drohendem Datenverlust;
- inkompatiblem Import;
- nicht sicher migrierbarem Stand;
- unvollständigem Kern-Offlinebestand;
- blockierter Kernfunktion;
- expliziter Löschhandlung.

### 20.4 Datenprinzip

Experience-Fortschritt darf keine neue Datensammlung erzeugen. Insbesondere bleiben ausgeschlossen:

- Nutzungsdauer;
- Klickfolge;
- Anzahl von Versuchen;
- Hilfenutzung;
- Scrolltiefe;
- Aufmerksamkeitssignale;
- automatisch abgeleitete Motivation oder Kompetenz.

## 21. Vertikale Referenzsituation 1 – Einstieg und Orientierung

### 21.1 Zweck

Ein neuer oder wiederaufgenommener Lernweg wird so eröffnet, dass Lernende und Lehrkraft ohne lange Vorlektüre handlungsfähig werden.

### 21.2 Ausgangslage

- Klasse 5 bis 7;
- gemeinsamer Unterrichtsbeginn;
- unterschiedliche Geräte- und Vorwissensstände;
- Modul kann neu sein oder fortgesetzt werden;
- lokale Speicherung kann funktionieren oder im flüchtigen Modus stehen.

### 21.3 Lernendenperspektive

Die lernende Person sieht:

1. eine verständliche Leitfrage oder Herausforderung;
2. das erwartete Lernprodukt;
3. den aktuellen Schritt;
4. einen realistischen Zeitkorridor;
5. „neu beginnen“ oder „weiterarbeiten“;
6. einen primären Handlungsaufruf;
7. bei Bedarf eine knappe technische Warnung mit sicherer Handlung.

Die gesamte Modulkarte ist erreichbar, aber nicht der primäre Arbeitsraum.

### 21.4 Lehrkraftperspektive

Die Lehrkraft sieht:

- Lernziel und Stellenwert;
- Voraussetzungen;
- gemeinsamen Einstieg;
- erwartbare Ausgangsvorstellungen;
- Geräte- und Sozialformoption;
- ersten Haltepunkt;
- technische Fallbacks;
- Entscheidung zwischen regulärem und erweitertem Zeitpfad.

### 21.5 Experience-Ablauf

~~~text
Kosmos oder Direktlink
→ Startboard
→ neu beginnen oder wiederaufnehmen
→ gemeinsamer Impuls
→ kurze Vorwissens- oder Erwartungshandlung
→ erster fokussierter Studiozustand
~~~

### 21.6 Qualitätskriterien

- Zweck, Produkt und nächster Schritt sind ohne Scrollsuche erkennbar.
- Nur eine primäre Startentscheidung konkurriert um Aufmerksamkeit.
- Wiederaufnahme zeigt den letzten fachlich sinnvollen Zustand.
- Technische Information ist ehrlich, aber nach Dringlichkeit priorisiert.
- Tastatur-, Touch- und Screenreaderpfad besitzen dieselbe Orientierung.
- Lehrkraft und Lernende beziehen sich auf dieselben Phasenbezeichnungen.

### 21.7 Initiale Validierungsziele

Diese Werte sind Projektbenchmarks, keine Forschungsgrenzwerte:

- neue Lernende können den ersten fachlichen Schritt nach höchstens 90 Sekunden Orientierung beginnen;
- wiederkehrende Lernende finden den nächsten Schritt nach höchstens 30 Sekunden;
- Testpersonen können Ziel, aktuelles Produkt und nächsten Schritt korrekt benennen;
- keine Person muss Daten- oder Offlineeinstellungen öffnen, wenn kein Handlungsbedarf besteht.

### 21.8 Anti-Patterns

- mehrere gleichgewichtige Startknöpfe;
- Technikstatus vor Lernziel;
- vollständige fünf- oder sechsstündige Aufgabenliste als Einstiegsoberfläche;
- kryptische UE-Navigation ohne Lernfunktion;
- Fortschrittsprozent ohne fachliche Bedeutung;
- Willkommensanimation ohne Denkhandlung.

## 22. Vertikale Referenzsituation 2 – interaktive Kernlernhandlung mit Feedback und Revision

### 22.1 Zweck

Eine anspruchsvolle digitale Lernhandlung koppelt fachliche Erwartung, Interaktion, Zustandsbeobachtung, Rückmeldung und Revision so eng, dass Trial-and-error nicht die tragende Strategie wird.

### 22.2 Referenzkern

IUM-5-CORE-05 dient als fachlicher Prüfgegenstand:

~~~text
Entwurf
→ Vorhersage
→ Ausführung
→ Laufspur
→ Vergleich
→ Reparaturhypothese
→ Revision
→ Begründung
~~~

Die Situation ist dennoch abstrakt genug, um später auch Datenmodelle, Quellenprüfung, Sicherheitsentscheidungen und Medienproduktion zu prüfen.

### 22.3 Lernendenperspektive

Der Lernende sieht einen fokussierten Arbeitsraum mit:

- aktuellem Auftrag;
- relevanter Szene oder Darstellung;
- Werkzeugen für den aktuellen Handlungstyp;
- Erwartungs- oder Vorhersagefeld;
- schrittweiser Ausführung oder Prüfung;
- korrespondenztreuer Zustands- und Belegdarstellung;
- Rückmeldung mit nächstem Prüfschritt;
- kontextueller Hilfe;
- Ausgangs- und Revisionsstand.

Nicht relevante Transfer-, Export-, Selbstcheck- und Folgeaufgaben bleiben außerhalb des primären Arbeitsraums.

### 22.4 Lehrkraftperspektive

Die Lehrkraft erhält:

- Zeitpunkt für gemeinsame Modellbildung;
- erwartbare Fehler und Fehlvorstellungen;
- anonymisierten Fehlerfall;
- Hinweise für Geräteverhältnis 1:2;
- Partnerrollen;
- Rückfragen zur ersten Abweichung;
- frischen Kurzfall bei fehlender Evidenz;
- gemeinsamen Haltepunkt vor Transfer.

### 22.5 Experience-Ablauf

~~~text
Auftrag verstehen
→ Entwurf oder Fall auswählen
→ Ergebnis und Zustand vorhersagen
→ schrittweise ausführen oder prüfen
→ relevante Abweichung markieren
→ Hypothese formulieren
→ gezielt ändern
→ erneut prüfen
→ Qualitätskriterium anwenden
~~~

### 22.6 Rückmeldungsbeispiel

Ungeeignet:

> Falsch. Versuche es noch einmal.

Geeignet:

> Der Auftrag endet in Schritt 4 vor dem Hindernis. Vergleiche die Blickrichtung nach Schritt 3 mit deiner Vorhersage. Welche einzelne Änderung möchtest du zuerst prüfen?

Die geeignete Rückmeldung:

- benennt das Ergebnis;
- lokalisiert den relevanten Zustand;
- erhält die Denkhandlung;
- erzwingt keine lange Freitexterklärung;
- verrät nicht sofort die Lösung.

### 22.7 Accessibility-Vertrag

- grafische und textliche Szene stammen aus derselben semantischen Quelle;
- aktuelle Aktion und betroffene Zustandsänderung sind verbunden;
- Editor funktioniert ohne Drag-and-drop;
- Rückmeldung ist programmatisch dem relevanten Zustand zugeordnet;
- Animation ist stoppbar oder schrittweise;
- Fokus folgt der Lernhandlung, nicht jeder dekorativen Änderung;
- bei schmaler Ansicht bleibt die Ursache–Wirkung-Beziehung verständlich.

### 22.8 Qualitätskriterien

- Lernende können sagen, was sie prüfen und warum.
- Erwartung und Beobachtung bleiben unterscheidbar.
- Rückmeldung erzeugt einen nächsten fachlichen Prüfschritt.
- Hilfe übernimmt nicht die Kernhandlung.
- Ausgangs- und Revisionsstand sind vergleichbar.
- Produktfortschritt ist fachlich, nicht über Versuchszahl, sichtbar.
- Lehrkraft kann einen gemeinsamen Vergleich auslösen, ohne Gerätedaten einzusehen.

### 22.9 Anti-Patterns

- alle Werkzeuge und Folgephasen gleichzeitig;
- Ausführung ohne Erwartung;
- Animation ohne textliche Zustandsdarstellung;
- Fehlerfarbe ohne lokalisierbaren Schritt;
- Lösung nach erstem Fehler;
- unendliche Versuchshistorie;
- Punkte für schnelles oder häufiges Ausführen;
- Lehrkraftdashboard mit Fehlerranking.

## 23. Vertikale Referenzsituation 3 – Sicherung, Transfer und anschlussfähiger Wiedereinstieg

### 23.1 Zweck

Ein Lernweg endet in einer fachlich belastbaren Sicherung und bereitet zugleich spätere Wiederaufnahme vor. Abschluss bedeutet weder Seitenende noch Vollständigkeitsbadge.

### 23.2 Lernendenperspektive

Die lernende Person erhält eine knappe Belegkarte:

- Leitfrage;
- eigene Kernaussage;
- relevantes Ausgangsprodukt;
- bestätigter Beleg oder Test;
- wichtigste Revision;
- angewendetes Qualitätskriterium;
- Transferantwort;
- nächster Wiedervorlagepunkt.

Die Belegkarte wird aus bereits erzeugten Produktspuren zusammengestellt. Sie verlangt keine zweite Vollverschriftlichung des Lernwegs.

### 23.3 Lehrkraftperspektive

Die Lehrkraft erhält:

- fachliche Sicherungsaussage;
- kontrastierbare Beispiele und typische Abweichungen;
- Gesprächs- oder Tafelbildstruktur;
- Kriterien für ein tragfähiges Produkt;
- frischen Transferfall;
- Hinweise für späteren Abruf;
- Entscheidung, ob bewusster Export erforderlich ist.

### 23.4 Experience-Ablauf

~~~text
Produkt und Revision vergleichen
→ Kernaussage sichern
→ Modellgrenze benennen
→ Transferfall bearbeiten
→ gemeinsame Sicherung
→ Belegkarte bestätigen
→ lokalen Wiedereinstieg setzen
→ zum Kosmos oder nächsten Modul zurückkehren
~~~

### 23.5 Fortschrittsdarstellung

Die Experience zeigt:

- welche Lernhandlung abgeschlossen wurde;
- welches Produkt jetzt tragfähiger ist;
- welche Frage im Transfer geklärt wurde;
- wann und in welchem Modul das Konzept wiederkehrt.

Sie zeigt nicht:

- Kompetenzniveau;
- Klassendurchschnitt;
- Rang;
- Fehlerquote;
- Nutzungsdauer;
- prognostizierten Lernerfolg.

### 23.6 Wiedereinstieg

Bei späterer Rückkehr:

- wird die Belegkarte in Kurzform gezeigt;
- wird die relevante Kernaussage aktiv abgerufen, nicht nur wieder angezeigt;
- folgt eine neue, veränderte Lernhandlung;
- bleibt die alte Vollseite geschlossen;
- kann der bisherige Stand bewusst geöffnet werden.

### 23.7 Qualitätskriterien

- Sicherung und Transfer sind getrennte Lernhandlungen.
- Die Belegkarte beruht auf tatsächlichem Produkt und tatsächlicher Revision.
- Die Lehrkraft kann eine gemeinsame fachliche Konsolidierung durchführen.
- Wiedervorlage fordert aktiven Abruf.
- Export ist bewusst und datensensibel.
- Der nächste Lernweg ist nachvollziehbar, aber nicht automatisch erzwungen.

### 23.8 Anti-Patterns

- bloße Zusammenfassung ohne Lernhandlung;
- Konfetti oder Badge als Abschluss;
- Selbstcheck als Kompetenzdiagnose;
- vollständige Versuchschronik;
- Exportzwang;
- Transfer nur durch anderes Oberflächendekor;
- Wiedereinstieg als lange Liste alter Eingaben.

## 24. Gemeinsamer Vertrag der drei Referenzsituationen

Jede spätere Produktarchitektur muss über alle drei Situationen hinweg dieselben Verträge erfüllen:

| Vertrag | Einstieg | Kernhandlung | Sicherung |
|---|---|---|---|
| fachlicher Zweck | Leitfrage und Produkt | aktuelle Denkhandlung | Kernaussage und Transfer |
| primäre Aktion | beginnen oder fortsetzen | prüfen, handeln oder revidieren | sichern, übertragen oder wiederaufnehmen |
| Fortschritt | aktueller Lernwegzustand | Produkt- und Revisionszustand | Konzept- und Anschlusszustand |
| Lehrkraft | Auftakt und Haltepunkt | Modellierung, Rückfrage, Rollen | Konsolidierung und Wiedervorlage |
| Accessibility | Orientierung | gleichwertige Interaktion | verständliche Beleg- und Transferwege |
| Local First | vorhandenen Stand erkennen | relevante Produktspuren sichern | bewusster Export und Wiedereinstieg |
| Motivation | Relevanz und erreichbarer Start | Kompetenzerfahrung und begrenzte Wahl | sichtbare Verbesserung und Anschluss |

## 25. Qualitätsmodell Learning Experience

### 25.1 Q1 – Lernhandlungs-Klarheit

**Prüffragen:**

- Ist die aktuelle fachliche Handlung eindeutig?
- Sind Ziel, Produkt und Kriterium verständlich?
- Ist der nächste Schritt erkennbar?

**Gate:**

Eine Testperson kann in eigenen Worten Ziel, aktuelle Handlung und Qualitätskriterium benennen.

### 25.2 Q2 – kognitive Ökonomie

**Prüffragen:**

- Sind nur relevante Werkzeuge und Informationen primär sichtbar?
- Bleiben notwendige Zusammenhänge erhalten?
- Sind Ursache und Wirkung räumlich und semantisch verbunden?

**Gate:**

Keine konkurrierende Kontrolle besitzt ohne aktuelle Funktion visuelles oder semantisches Primat.

### 25.3 Q3 – sinnvolle Agency und Motivation

**Prüffragen:**

- Gibt es relevante, begrenzte Wahl?
- Ist Herausforderung mit Unterstützung ausbalanciert?
- Wird Kompetenz an einer echten Verbesserung sichtbar?

**Gate:**

Keine Motivation hängt von Punkten, Rang, Streak, künstlicher Knappheit oder pauschalem Lob ab.

### 25.4 Q4 – Feedback und Revision

**Prüffragen:**

- Ist Rückmeldung informationshaltig?
- Erzeugt sie einen nächsten Prüfschritt?
- Bleiben Ausgangs- und Revisionsstand unterscheidbar?

**Gate:**

Jede zentrale Aufgabe besitzt mindestens einen nachvollziehbaren Revisionspfad.

### 25.5 Q5 – Fortschritt und Kontinuität

**Prüffragen:**

- Ist Fortschritt fachlich und nicht klickbasiert?
- Ist der Wiedereinstieg verständlich?
- Gibt es spätere Wiedervorlagen?

**Gate:**

Ein lokaler Wiedereinstieg benötigt keine vollständige Wiederholung der bereits gesicherten Orientierung.

### 25.6 Q6 – Lehrkraftorchestrierung

**Prüffragen:**

- Sind gemeinsame Haltepunkte sichtbar?
- Gibt es geeignete Sozialform- und Zeitoptionen?
- Sind Rückfragen, Hilfen und Sicherung vorbereitet?

**Gate:**

Die Lehrkraft kann eine Lernphase ohne personenbezogene Systemdaten beginnen, begleiten und sichern.

### 25.7 Q7 – Accessibility und Gleichwertigkeit

**Prüffragen:**

- Sind WCAG 2.2 AA und kognitive Accessibility getrennt geprüft?
- Tragen alternative Pfade dasselbe Lernziel?
- Sind Kontrolle, Wirkung und Rückmeldung eindeutig verbunden?

**Gate:**

Die zentrale Lernhandlung funktioniert fachlich gleichwertig mit Tastatur, Touch und Text-/Assistive-Technology-Pfad.

### 25.8 Q8 – Resilienz, Datenschutz und Offenheit

**Prüffragen:**

- Bleibt die Lernhandlung offline und local first?
- Sind technische Warnungen nach Dringlichkeit priorisiert?
- Werden nur erforderliche Produktspuren gespeichert?
- Bleiben Quellen und Assets offen nachnutzbar?

**Gate:**

Keine Experience-Funktion benötigt Konto, Backend, Telemetrie oder personenbezogene Analyse.

## 26. Globale Anti-Patterns

Spätere Entwürfe fallen durch, wenn sie eines der folgenden Muster als Grundarchitektur verwenden:

- **Mega-Seite:** alle Phasen, Werkzeuge, Hilfen und Datenfunktionen gleichzeitig.
- **Infrastruktur-First:** Speicher-, Update- oder Gatezustand dominiert ohne Handlungsbedarf den Einstieg.
- **Pseudo-Fortschritt:** Prozent, Badge oder Level bildet Seitenbesuch statt Lernen ab.
- **Dekorative Gamification:** Punkte, Streaks, Ranglisten, künstliche Zeitknappheit oder Belohnungsschleifen.
- **Offene Wahl ohne Struktur:** viele Optionen ohne Ziel-, Kriterien- und Voraussetzungenklärung.
- **Wizard ohne Überblick:** strikte Einzelschritte ohne Gesamtkarte, Rückkehr oder fachlichen Zusammenhang.
- **Feedback als Urteil:** richtig/falsch, Lob oder Ampel ohne fachliche Information.
- **Adaptive Blackbox:** Weg oder Hilfe wird aus Klicks, Zeit oder Fehlerhistorie personalisiert.
- **Lehrkraft als Nachtrag:** Unterrichtsführung steht nur im Handbuch und besitzt keine sichtbaren Haltepunkte.
- **Accessibility als Parallelprodukt:** textliche oder assistive Pfade tragen eine andere Lernhandlung.
- **Narration als Lernersatz:** Mission, Illustration oder Animation ersetzt Modell, Entscheidung und Revision.
- **Export als Abschluss:** Dateidownload wird mit Sicherung oder Lernnachweis verwechselt.

## 27. Validierungsstrategie

### 27.1 LXP01-Dokumentprüfung

Vor schriftlicher Freigabe werden geprüft:

- Forschungsbestand und neue Quellen sind getrennt;
- Quellenart, Population, Umfang und Grenzen sind benannt;
- Forschungsbefund und Projektinferenz sind unterscheidbar;
- alle drei Referenzsituationen enthalten Lernenden- und Lehrkraftperspektive;
- Local First, Offline, Datenschutz und Accessibility sind integriert;
- Qualitätskriterien und Anti-Patterns sind prüfbar;
- spätere Etappen werden nicht vorweg implementiert.

### 27.2 LXP02-Strukturprüfung

Die spätere Produktarchitektur muss:

- alle fünf Informationsräume abbilden;
- Start, Studio, Sicherung und Kosmos unterscheiden;
- Zustände, Navigation und Wiedereinstieg definieren;
- dieselben Bezeichnungen für Lernende und Lehrkraft verwenden;
- progressive Offenlegung ohne Informationsverlust nachweisen.

### 27.3 LXP03-Referenzprüfung

Jede der drei Referenzsituationen wird mindestens geprüft durch:

- Desktop- und schmale Ansicht;
- Tastatur-, Touch- und Textpfad;
- Neu- und Wiedereinstieg;
- störungsfreien und fehlerhaften Local-First-Zustand;
- Einzel- und 1:2-Arbeit;
- Lehrkraftablauf;
- kognitive Walkthroughs;
- fachliche und didaktische Reviews.

### 27.4 LXP06-interne Produktvalidierung

Vor Pilotierung werden getrennt geprüft:

- fachliche Richtigkeit;
- Lernhandlungs-Klarheit;
- Usability;
- kognitive Accessibility;
- WCAG 2.2 AA;
- Lehrkraftorchestrierung;
- Local First, Offline und Datenschutz;
- Motivation ohne Gamification;
- Produkt- und Revisionsqualität.

Ein grüner technischer Test ersetzt keine dieser Prüfungen.

## 28. Mess- und Beobachtungsfragen

Spätere Tests untersuchen ohne zentrale Telemetrie:

### Einstieg

- Können Lernende Ziel, Produkt und nächsten Schritt benennen?
- Finden sie Neu- und Wiedereinstieg?
- Verstehen sie die Gesamtkarte, ohne sie ständig offen zu benötigen?

### Kernhandlung

- Können Lernende Erwartung und Beobachtung unterscheiden?
- Lokalisieren sie eine relevante Abweichung?
- Nutzen sie Rückmeldung für eine begründete Revision?
- Bleibt Trial-and-error begrenzt?

### Sicherung

- Können Lernende Kernaussage, Beleg und Revision verbinden?
- Übertragen sie das Konzept auf eine veränderte Beziehung?
- Unterstützt die Belegkarte späteren aktiven Abruf?

### Lehrkraft

- Sind Haltepunkte, Rückfragen und Fallbacks ausreichend?
- Funktioniert 1:2-Arbeit fachlich symmetrisch?
- Kann die Lehrkraft ohne Systemdaten handlungsfähig entscheiden?

### Accessibility

- Bleibt die Lernhandlung in allen Bedienpfaden gleichwertig?
- Sind aktuelle Aktion, Wirkung und Rückmeldung verständlich verbunden?
- Entsteht durch Segmentierung neue Orientierungs- oder Gedächtnislast?

## 29. Bekannte Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| Segmentierung wird zum kleinteiligen Wizard | fachlich vollständige Schritte, Gesamtkarte, Rückkehr und transparente Übergänge |
| Kosmos erzeugt Wahlüberlastung | Voraussetzungen, empfohlener Kernweg und begrenzte Filter |
| Lernstudio wird zu starr | echte Varianten, Lehrkraftoptionen und sichtbare Wahlräume |
| Fortschritt wird zum versteckten Scoring | fachliche Zustände statt Prozent, Punkte oder Vergleich |
| Motivation wird als Dekoration behandelt | Relevanz, Kompetenzerfahrung, Agency, Zugehörigkeit und Revision prüfen |
| Lehrkraftspur wird zweites Produkt | dieselben Lernhandlungen und Begriffe, nur rollenbezogene Orchestrierungsinformation |
| kognitive Accessibility senkt Fachanspruch | Bedien- und Darstellungsbarrieren reduzieren, Kernhandlung erhalten |
| technische Warnungen werden versteckt | dreistufige Dringlichkeitslogik mit prominentem Alarmmodus |
| Quellen werden zu universellen Regeln überdehnt | Evidenzstatus, Grenzen und Designhypothesen sichtbar halten |
| IUM5 wird zu früh kosmetisch überarbeitet | Produktcode und konkrete UI bis LXP04/LXP05 gesperrt |

## 30. Konsequenzen für LXP02

Nach Freigabe muss LXP02 spezifizieren:

1. Informationsarchitektur des Kosmos;
2. Modulstart und Startboard;
3. Zustandsmodell des Lernstudios;
4. Navigation zwischen Lernphasen und Unterrichtseinheiten;
5. Gesamtkarte und progressive Offenlegung;
6. Neu-, Fortsetzungs- und Wiedereinstieg;
7. Sicherungsraum und Belegkarte;
8. Lehrkraftspur;
9. Local-First-, Offline- und Fehlerzustände auf Experience-Ebene;
10. Rollen- und Sozialformwechsel;
11. Begriffe und Beschriftungsvertrag;
12. Abgrenzung zu LXP03 und LXP04.

LXP02 erstellt noch keinen Produktcode.

## 31. Konsequenzen für LXP03

LXP03 entwickelt aus den hier definierten Verträgen drei konkrete, vergleichbare Experience-Entwürfe:

1. Einstieg und Orientierung;
2. interaktive Kernlernhandlung mit Feedback und Revision;
3. Sicherung, Transfer und Wiedereinstieg.

Die Entwürfe müssen:

- denselben Experience-Nordstern erfüllen;
- unterschiedliche fachliche Zustände abbilden;
- Lernenden- und Lehrkraftspur verbinden;
- Accessibility, Local First und Offline sichtbar lösen;
- gegen Qualitätsmodell und Anti-Patterns geprüft werden;
- vor Systemableitung gemeinsam bewertet werden.

## 32. Nicht-Ziele

Diese Spezifikation enthält bewusst nicht:

- konkrete Wireframes;
- visuelle Moodboards;
- Markenentwicklung;
- CSS- oder Komponentenentscheidungen;
- eine technische Router- oder Zustandsbibliothek;
- eine vollständige Designsystemtaxonomie;
- neue Curriculumzuordnung;
- Niveaudifferenzierung;
- automatische Personalisierung;
- Lernanalyse;
- Konten oder Klassenverwaltung;
- Pilotierungsinstrumente;
- Produktimplementierung.

## 33. Akzeptanzkriterien

- Bestand und Forschungslücken sind quellenkritisch getrennt.
- Bestehende und ergänzende Quellen sind mit Grenzen dokumentiert.
- Lernwirksame Gestaltung ist über Mechanismen und Lernhandlungen operationalisiert.
- Drei Experience-Ansätze sind verglichen und einer ist begründet gewählt.
- Kosmos und Lernstudio besitzen getrennte, komplementäre Funktionen.
- Motivation wird ohne aufgesetzte Gamification beschrieben.
- Fortschritt ist fachlich, nicht klick- oder personenbezogen.
- Einstieg, Kernhandlung und Sicherung/Transfer sind als vertikale Referenzsituationen festgelegt.
- Lernenden- und Lehrkraftperspektive sind integriert.
- Accessibility umfasst WCAG und kognitive Zugänglichkeit.
- Local First, Offline und Datenschutz bleiben Produktgrundlagen.
- Qualitätskriterien und Anti-Patterns ermöglichen spätere Reviews.
- LXP02 und LXP03 erhalten klare Folgeaufträge, aber keine vorweggenommene Implementierung.
- Kein Produktcode, Deployment, Pilot oder Release wurde begonnen.

## 34. Schriftliches Freigabegate

Mit der schriftlichen Freigabe werden verbindlich:

- die zweistufige Kosmos-/Lernstudio-Strategie;
- der Experience-Nordstern;
- die Experience-Grammatik;
- Rollen-, Motivations-, Fortschritts- und Orchestrierungsmodell;
- die drei vertikalen Referenzsituationen;
- das achtteilige Qualitätsmodell;
- die globalen Anti-Patterns;
- die Abgrenzung von LXP02, LXP03 und späterer Implementierung.

Die Freigabe erlaubt anschließend ausschließlich die Präzisierung und Planung von LXP02. Sie erlaubt noch keinen Produktcode, keine IUM5-Neufassung, keine reale Erprobung und keine Produktfreigabe.
