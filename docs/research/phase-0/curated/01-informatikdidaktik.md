---
package: informatikdidaktik
status: curated
curated: 2026-07-28
source: ../raw/01-informatikdidaktik.md
---

# Informatikdidaktik Klassen 5–7

## Scope und Quellenqualität

Dieses Paket kuratiert Informatikdidaktik für einen gymnasialen Lernweg im Alter von etwa 10 bis 13 Jahren. Es deckt Progression, Programmierpraktiken, Fehlvorstellungen, externe Repräsentationen, Beispiele und Anleitung, Block/Text-Übergänge, Daten, Netze, Sicherheit sowie begründete analoge und digitale Aktivitäten ab.

Die Quellen wurden am 28. Juli 2026 gegen DOI-, Publisher-, Autoren- oder Institutionsseiten geprüft. Die höchste Zielgruppennähe haben:

- PRIMM mit 11- bis 14-Jährigen;
- die K‑8-Lerntrajektorien;
- das Unplugged-Quasi-Experiment mit 10- bis 12-Jährigen;
- das systematische Review zu Internetvorstellungen von 3- bis 15-Jährigen.

Die Quellen zu notional machines, worked examples, Fehlvorstellungen und expliziter Skill-Sequenz beruhen stark oder ausschließlich auf Hochschulkontexten. Sie begründen deshalb didaktische Heuristiken, keine altersbezogenen Standards. Die CSTA-Standards sind eine professionelle fachliche Orientierung; sie belegen keine Methodenwirkung und sind für Baden-Württemberg nicht normativ.

Alle retained Claims stehen im `claim-ledger.json` auf `reviewed`. Keiner wird als projektweiter `standard` gesetzt.

## Retained Claims

### CLAIM-INF-001 – Kontrollstrukturen als Lerntrajektorien

**Befund.** Literaturbasierte K‑8-Lerntrajektorien ordnen Sequenz, Wiederholung und Bedingungen als Netze zunehmend anspruchsvoller Lernziele. Die konkrete Ordnung hängt von Kontext, Aufgabe und Sprache ab.

**Evidenz.** Rich et al. synthetisierten mehr als 100 Forschungsarbeiten und über 600 Lernziele zu K‑8. Die Arbeit ist eine Forschungssynthese, keine Curriculum-Intervention. [Originalquelle](https://doi.org/10.1145/3105726.3106166)

**Einschränkung und Transfer.** Die Literaturbasis war lückenhaft und kontextspezifisch. Eine Zuordnung zu Klassen 5, 6 und 7 in Baden-Württemberg ist Projektinferenz.

**Designfolge.** Kontrollstrukturen werden über Handlungen gestaffelt: erkennen/ausführen → vorhersagen/erklären → verändern/testen → selbst entwerfen und vergleichen.

### CLAIM-INF-002 – PRIMM als schulnaher Programmierzyklus

**Befund.** In 13 Schulen erzielte eine PRIMM-Interventionsgruppe von 493 Lernenden im Alter von 11 bis 14 Jahren höhere Posttestwerte als 180 Lernende in Kontrollgruppen.

**Evidenz.** Die Mixed-Methods-Studie prüfte Predict, Run, Investigate, Modify und Make im verpflichtenden Unterricht und berichtete einen kleinen günstigen Effekt (r=.13). [Originalquelle](https://doi.org/10.1080/08993408.2019.1608781)

**Einschränkung und Transfer.** Die Gruppen waren nicht durchgängig randomisiert und die Umsetzung variierte zwischen Schulen. PRIMM ist ein belastbarer Kandidat für die Modulgrammatik, aber keine Garantie für Lernerfolg.

**Designfolge.** Programmiereinheiten verwenden wiederkehrend Vorhersagen, tatsächliche Ausführung, gemeinsame Untersuchung, gezielte Modifikation und zunehmend eigenständige Konstruktion.

### CLAIM-INF-003 – Programmierpraktiken getrennt und inkrementell lehren

**Befund.** Tracing, Syntaxproduktion, Templateverständnis und Codeproduktion sind unterscheidbare Praktiken, die explizit und inkrementell unterrichtet werden können.

**Evidenz.** Xie et al. formulierten eine Theorie und prüften passende Materialien explorativ. [Originalquelle](https://doi.org/10.1080/08993408.2019.1565235)

**Einschränkung und Transfer.** Die empirische Studie hatte nur neun überwiegend erwachsene Teilnehmende und erlaubte keine belastbaren Effektangaben. Der Claim bleibt `low`.

**Designfolge.** Die Praktiken werden in Aufgaben und Lernzielen separat ausgewiesen. Ihre Reihenfolge für 10- bis 13-Jährige wird pilotiert und nicht dogmatisch festgeschrieben.

### CLAIM-INF-004 – Worked examples aktiv verarbeiten

**Befund.** Die Programmierforschung zu worked examples stützt vor allem aktiv zu verarbeitende Code-Tracing- und Code-Generierungsbeispiele, darunter Subgoal-Hinweise, Lücken und Parsons-Probleme.

**Evidenz.** Der Review von Muldner, Jennings und Chiarelli bündelt die einschlägige Forschung und weist zugleich Lücken aus. [Originalquelle](https://doi.org/10.1145/3560266)

**Einschränkung und Transfer.** 10- bis 13-Jährige sind unterrepräsentiert; Aufgaben, Medien und Maße sind heterogen.

**Designfolge.** Beispiele verlangen Vorhersage, Selbsterklärung, Ergänzung oder Korrektur. Unterstützung wird von vollständigen Beispielen über Lücken und Modifikationen zur Eigenkonstruktion ausgeblendet.

### CLAIM-INF-005 – Programmausführung durch ein notional-machine-Modell erklären

**Befund.** Ein explizites notional-machine-Modell verbindet statischen Code, Ausführungsprozess und veränderlichen Zustand. Der Lernwert einer Visualisierung hängt von aktiver Auseinandersetzung ab.

**Evidenz.** Sorva synthetisiert Forschung zu Fehlvorstellungen, mentalen Modellen, Programmausführung und Visualisierung. [Originalquelle](https://doi.org/10.1145/2483710.2483713)

**Einschränkung und Transfer.** Die Forschung stammt überwiegend aus CS1. Das Modell muss zu Sprache, Paradigma, Werkzeug und Lernziel passen.

**Designfolge.** Lernmodule verwenden konsistente Spuren mit Codezeile, Ausführungsposition, Zustand und Ausgabe. Lernende ergänzen, erklären und korrigieren sie; Animation allein genügt nicht.

### CLAIM-INF-006 – Fehlvorstellungen aufgabenbezogen diagnostizieren

**Befund.** Wiederkehrende Schwierigkeiten betreffen Variablen und Zuweisung, Kontrollfluss, Schleifen, Aufrufe sowie das Verhältnis von Syntax, Semantik und Programmplan.

**Evidenz.** Qian und Lehman kuratieren die Literatur zu Einführungsprogrammierung; Sorva ordnet Schwierigkeiten im Verhältnis zur Programmausführung ein. [Qian & Lehman](https://doi.org/10.1145/3077618), [Sorva](https://doi.org/10.1145/2483710.2483713)

**Einschränkung und Transfer.** Viele Befunde sind hochschulspezifisch. Ein Fehler ist nicht automatisch ein stabiles Fehlkonzept.

**Designfolge.** Kurze Vorhersage-, Erklär-, Vergleichs- und Reparaturaufgaben erzeugen unmittelbares Feedback. Das Lernwerk speichert keine personenbezogenen Diagnoseprofile.

### CLAIM-INF-007 – Debugging mehrdimensional entwickeln

**Befund.** Eine K‑8-Synthese ordnet Debugging entlang von Strategien zum Finden und Beheben, Fehlertypen und der Rolle von Fehlern im Problemlösen.

**Evidenz.** Rich et al. leiteten die Trajektorie aus Forschungsliteratur ab. [Originalquelle](https://doi.org/10.1145/3287324.3287396)

**Einschränkung und Transfer.** Die Arbeit evaluiert keine vollständige Unterrichtssequenz und kein bestimmtes Werkzeug.

**Designfolge.** Die Progression trennt bemerken → lokalisieren → klassifizieren → Hypothese bilden → gezielt testen → reparieren → begründen. Fehler werden als erwartbarer Teil des Problemlösens gerahmt.

### CLAIM-INF-008 – Block/Text als kontextabhängige Übergangsentscheidung

**Befund.** In zwei Klassen einer selektiven High School zeigte die Blockgruppe nach fünf Wochen größere Lernzuwächse als die Gruppe mit isomorpher Textoberfläche. Nach zehn weiteren Wochen Java waren Unterschiede in Leistung, Haltung und Programmierpraktiken nicht mehr nachweisbar.

**Evidenz.** Zwei Berichte derselben quasi-experimentellen Langzeituntersuchung: [Anfangsphase](https://doi.org/10.1145/3089799), [Übergang zu Java](https://doi.org/10.1016/j.compedu.2019.103646)

**Einschränkung und Transfer.** Das Sample umfasste 60 Lernende in einem Wahlkurs, zwei nicht randomisierte Klassen, einen Lehrer und spezifische Werkzeuge.

**Designfolge.** Es gibt keinen festen Alterswechsel. Die Darstellung folgt Lernziel und Syntaxlast; Übergänge werden mit isomorphen Beispielen, Übersetzungsaufgaben oder strukturierten Editoren gestützt.

### CLAIM-INF-009 – Unplugged nur mit ausgewiesener fachlicher Funktion

**Befund.** Unplugged-Aktivitäten können eng umrissene CS/CT-Ziele unterstützen. Die Forschung rechtfertigt keine pauschale Wirksamkeits-, Interessens- oder Transferbehauptung.

**Evidenz.** Huang und Looi sichteten 40 K‑12-Publikationen und dokumentierten Konstrukt-, Konfundierungs- und Equity-Probleme. Brackmann et al. fanden in einem Quasi-Experiment mit 73 Lernenden im Alter von 10 bis 12 Jahren positive CT-Testeffekte. [Review](https://doi.org/10.1080/08993408.2020.1789411), [Primärstudie](https://doi.org/10.1145/3137065.3137069)

**Einschränkung und Transfer.** Konstrukte und Interventionen sind heterogen; im Quasi-Experiment ähnelten sich Aufgaben und Testformat, und es gab keine Individualrandomisierung.

**Designfolge.** Analog wird nur gewählt, wenn Manipulation, Verkörperung oder gemeinsames Modellieren einen unsichtbaren fachlichen Prozess klärt. Jede Aktivität benennt Zuordnung, Analogiegrenze und digitales oder formales Anschlussprodukt.

### CLAIM-INF-010 – Internetmodelle schrittweise rekonstruieren

**Befund.** Kinder und Jugendliche verfügen häufig über fragmentarische und widersprüchliche Vorstellungen von Internet, Wi‑Fi, Infrastruktur, zentraler Speicherung, Türmen, Satelliten und Datenfluss.

**Evidenz.** Brom et al. synthetisierten 27 qualitative und Mixed-Methods-Studien mit 2.214 Teilnehmenden im Alter von 3 bis 15 Jahren und ordneten 60 Konzeptionen. [Originalquelle](https://doi.org/10.1007/s10639-023-11775-9)

**Einschränkung und Transfer.** Länder, Altersgruppen und Technikstände von 2002 bis 2022 unterscheiden sich. Das früheste dokumentierte Auftreten ist kein Entwicklungsgrenzwert.

**Designfolge.** Lernende erklären oder zeichnen zunächst einen Nachrichtenweg. Modellvergleiche führen von Geräte-/Wi‑Fi-Vorstellungen zu mehrstufigen Paketweg-, Router-, Client–Server- und Speicherungsmodellen, ohne personenbezogene Speicherung.

### CLAIM-INF-011 – Informatik als verbundene Inhaltsbereiche und Praktiken

**Befund.** Die CSTA-Standards 2026 führen Algorithmen und Design, Programmierung, Daten und Analyse, Systeme und Sicherheit sowie Computing und Gesellschaft als Inhaltsbereiche und kombinieren sie mit fachlichen Praktiken.

**Evidenz.** Der professionelle PK‑12-Standard hat ein Middle-School-Band für Grades 6 bis 8 und ist unter CC BY-NC-SA veröffentlicht. [Originalquelle](https://csteachers.org/pk12standards/)

**Einschränkung und Transfer.** Der US-Standard ist weder Wirkungsstudie noch Norm für Baden-Württemberg. Die Klassenbänder sind nicht deckungsgleich.

**Designfolge.** Daten, Netze und Sicherheit werden als eigenständige Stränge mit Erstellen, Abstrahieren, Testen und gesellschaftlicher Reflexion verbunden. Verbindliche Inhalte folgen ausschließlich dem amtlichen Curriculum-Mapping.

## Empfohlene Progression 5–7

Die Sequenz ist eine Projektinferenz aus den Claims und muss mit dem Curriculum-Mapping sowie Pilotierungen geprüft werden.

| Klasse | Algorithmen und Programmierung | Daten, Netze und Sicherheit | Leitende Lernhandlungen |
| --- | --- | --- | --- |
| 5 | Folgen präzisieren; kurze gegebene Programme lesen, vorhersagen und klein verändern; Zustand und Ausgabe sichtbar machen | Zeichen, Zahlen und einfache Codierungen; eigene Internetvorstellungen; Rollen von Gerät, Verbindung und Dienst | ausführen, ordnen, vorhersagen, erklären, vergleichen |
| 6 | Bedingungen, Wiederholungen und Variablen; PRIMM-Zyklen; Normal- und Randfälle; erste systematische Fehlersuche | Datenübertragung als mehrstufiger Weg; Client und Server über Rollen und Nachrichten; einfache Codier- und Übertragungsmodelle | untersuchen, modifizieren, testen, Fehler lokalisieren und begründen |
| 7 | größere Programme planen; Funktionen/Prozeduren; Textübergänge; Lösungen vergleichen, dokumentieren und überarbeiten | Datenrepräsentation im Übertragungskontext; Routing und verteilte Speicherung; Klartext–Verfahren–Schlüssel–Geheimtext | entwerfen, abstrahieren, gezielt testen, erklären, transferieren |

Für Datenrepräsentation und grundlegende Kryptografie ist die direkt altersbezogene Evidenz dünn. Die vorgeschlagene Abfolge ist fachlich plausibel, aber nicht empirisch gleich stark abgesichert wie die Programmierprogression.

## Fehlvorstellungen und datensparsame Diagnosegelegenheiten

### Programmierung

- Variable als algebraische Gleichung statt veränderlicher Zustand;
- Bedeutung eines Variablennamens als vermeintliches Maschinenwissen;
- Schleife als absichtsgeleitete Wiederholung statt bedingter Ausführung;
- Verwechslung von statischem Code, aktueller Ausführungsposition und Zustand;
- Reparatur durch unsystematisches Ändern statt Hypothese und Test.

Geeignete Aufgaben: Ausgabe vorhersagen, Zustandstabelle ergänzen, zwei fast gleiche Programme vergleichen, falschen Trace reparieren, Randfall wählen, Fehlerort und Fehlerart trennen.

### Netze

- Internet gleich Wi‑Fi oder gleich Endgerät;
- ein zentraler Speicher, Turm oder Satellit als vollständiges Infrastrukturmodell;
- direkter Weg vom Absender zum Empfänger ohne Zwischenstationen;
- fehlende Trennung zwischen Übertragung und dauerhafter Speicherung.

Geeignete Aufgaben: Nachrichtenweg zeichnen und erklären, Rollen-/Paketkarten ordnen, Modelle kontrastieren, mögliche Speicherorte im Verlauf markieren.

### Datenschutzgrenze

Diagnoseantworten dienen dem unmittelbaren Feedback, der Aufgabenauswahl im aktuellen Lernschritt oder einer anonymen Klassenauswertung. Das Lernwerk erzeugt keine dauerhaften Personenprofile, speichert keine Fehlvorstellungsetiketten und integriert keine personenbezogene Diagnostik.

## Konsequenzen für die Modulgrammatik

Ein Kernmodul folgt in adaptierbarer Form dieser Grammatik:

1. **Aktivieren und sichtbar machen:** kurze Vorhersage, Erklärung oder Modellskizze ohne personenbezogene Speicherung.
2. **Modellieren:** worked example mit explizitem Ziel, Zustand, Schrittfolge und Ergebnis.
3. **Predict–Run–Explain:** Vorhersage vor digitaler Ausführung, anschließend Abweichung erklären.
4. **Fokussiert üben:** Vergleich, Trace, Parsons-Problem oder Teilergänzung mit unmittelbarem Feedback.
5. **Modify und Test:** gezielte Änderung, erwartetes Ergebnis, Normal- und Randfall.
6. **Make und Transfer:** zunehmend eigenständiges Produkt mit Erfolgskriterien.
7. **Debug und Überarbeiten:** Fehlerhypothese, Test, Reparatur und Begründung.
8. **Reflektieren:** fachliche Erklärung, Modellgrenze und nächster Transfer.

Nicht jedes Modul benötigt jede Phase in gleicher Länge. Vertiefungs-, Transfer- und Projektmodule können an definierte Voraussetzungen andocken und flexibel eingesetzt werden.

## Begründete Analog-/Digital-Entscheidungen

| Lernfunktion | Analog sinnvoll, wenn … | Digital sinnvoll, wenn … |
| --- | --- | --- |
| Programmausführung | ein stabil definiertes Rollen- oder Zustandsmodell gemeinsam manipuliert wird | tatsächliche Semantik, Ausführungsreihenfolge und unmittelbare Rückmeldung geprüft werden |
| Netzkommunikation | Rollen, Knoten, Paketwege und Engpässe körperlich oder mit Karten modelliert werden | reale oder simulierte Protokollspuren, Zeitverläufe und Paketvariation untersucht werden |
| Codierung/Kryptografie | kleine Alphabete, Bitkarten oder Schlüsselräume sichtbar und handhabbar werden | Skalierung, wiederholte Anwendung, Testfälle oder Angriffsversuche relevant sind |
| Debugging | Trace und Hypothese ohne Editorlast fokussiert werden | Fehler reproduziert, Eingaben variiert und Reparaturen ausgeführt werden |

Entscheidend ist die epistemische Funktion. Es gibt keine zwanghafte Doppelstruktur und kein pauschales „analog zuerst“. Digital ist selbstverständliches Unterrichtsmedium; analog wird genutzt, wenn es den fachlichen Gegenstand besser zugänglich macht.

## Verworfen oder herabgestuft

- **„Blockbasiert ist für Jüngere grundsätzlich besser.“** Verworfen: Die Evidenz ist kontextabhängig, stammt aus einer kleinen High-School-Studie und zeigt nach dem Java-Übergang keine bleibenden Gruppenunterschiede.
- **„Ein fester Klassenstufenwechsel von Blöcken zu Text ist evidenzbasiert.“** Verworfen: Kein belastbarer Altersgrenzwert.
- **„Unplugged erhöht automatisch Motivation, Teilhabe oder Transfer.“** Verworfen: Der Review dokumentiert schwache und teils gegenläufige Befunde sowie unzureichende Equity-Analysen.
- **„Worked examples sind für Klasse 5–7 robust belegt.“** Herabgestuft: Der programmierdidaktische Review ist relevant, aber stark hochschulgeprägt.
- **„Tracing → Syntax → Templates → Schreiben ist eine geprüfte K‑12-Sequenz.“** Herabgestuft auf `low`: Theorie plausibel, empirische Studie zu klein und zu altfern.
- **„CSTA 2026 bestimmt die baden-württembergische Progression.“** Verworfen: professioneller US-Standard ohne normative Geltung oder Wirksamkeitsbeleg.
- **„Codierung, Kompression und Verschlüsselung erzeugen bei 10- bis 13-Jährigen gesicherte typische Fehlvorstellungen.“** Nicht retained: In der gesichteten Evidenz fehlt ein hinreichend belastbarer altersbezogener Katalog.

## Offene Forschungsfragen

1. Welche PRIMM-Phasen tragen bei 10- bis 13-Jährigen unter digitalen Selbstlernanteilen besonders zum Verständnis bei?
2. Wie viel und welche Art von worked-example-Fading ist in Klassen 5–7 wirksam?
3. Welche notional-machine-Repräsentation bleibt über Block- und Textdarstellungen hinweg anschlussfähig?
4. Wie können Block/Text-Übergänge für heterogene Vorerfahrung flexibel angeboten werden, ohne Lernwege zu stigmatisieren?
5. Welche unplugged Aktivitäten zeigen nach einer digitalen Anschlussaufgabe tatsächlich Transfer?
6. Wie entwickeln sich Vorstellungen von Router, Client, Server, Paketweg und verteilter Speicherung zwischen Klasse 5 und 7?
7. Welche Progression verbindet Codierung, Datenrepräsentation, Kompression, Fehlererkennung und Kryptografie fachlich korrekt und altersangemessen?
8. Welche aufgabenbezogenen Diagnoseformate liefern nützliches Feedback, ohne personenbezogene Daten zu speichern?
9. Welche Lernprodukte belegen nicht nur lauffähigen Code, sondern auch Erklären, Testen, Debugging und Modellverständnis?

## Quellen

Die vollständigen Metadaten, Prüfstatus und Nutzungsangaben stehen im `source-register.json`; die Claim-Quelle-Zuordnung steht im `claim-ledger.json`. Der Rohbericht bleibt separat unter `../raw/01-informatikdidaktik.md` erhalten.
