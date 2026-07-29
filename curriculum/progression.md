# Begründete Progression Informatik und Medienbildung 5–7

- **Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Niveau E
- **Stand:** 29. Juli 2026
- **Artefaktstatus:** `working`
- **Curriculumstatus:** Basiskurs Medienbildung 2016 und Aufbaukurs Informatik Klasse 7 sind `enacted`; die Lesehilfe 2026/2027 ist `orientation`.

## 1. Zweck und Statusgrenze

Diese Progression begründet einen Arbeitsstand für Kernlernweg, Modulvoraussetzungen und spätere Abdeckungsplanung. Sie führt drei quellentreu extrahierte Curriculumdatensätze, das Fachprofil und den vollständigen Crosswalk zusammen. Sie ist kein neuer Bildungsplan und erklärt insbesondere die kombinierte Vorgabe „Klassen 5/6“ nicht nachträglich zu einer amtlichen jahrgangsgenauen Verteilung.

Für jede Aussage gilt daher eine von zwei Kategorien:

- **Normative beziehungsweise orientierende Anforderung:** Sie ist durch einen Record aus `competencies.json` belegt. Geltungsstatus, Klassenband und Wortlaut bleiben unverändert.
- **Didaktische Sequenzierungsentscheidung · `working`:** Sie ordnet Voraussetzungen, Wiederaufnahme, Komplexitätszuwachs oder einen vorläufigen Jahrgang zu. Sie ist eine Projektentscheidung und muss durch Fachreview, Pilotierung sowie einen späteren Fachplan revidierbar bleiben.

Der Crosswalk in `crosswalk.json` löst 278 Records vollständig auf: fachliche Beziehungen stehen in 56 Relationsgruppen; 107 nicht verbindliche Beispiele beziehungsweise quellenspezifische Operatorrecords werden mit Grund und Folgeaktion separat geführt. Neun Relationsgruppen bleiben wegen Klassenverteilung oder veränderter Gewichtung `open`.

## 2. Quellen- und Entscheidungslogik

1. Die `enacted` Bildungspläne bleiben verbindlich, solange sie nicht amtlich ersetzt oder aufgehoben sind.
2. Die Lesehilfe steuert als `orientation` die Vorbereitung auf Informatik und Medienbildung, setzt die Bildungspläne aber nicht außer Kraft.
3. Fachlich gleichartige Anforderungen werden über `equivalent`, `overlaps`, `extends` oder `reframes` verbunden; ihre Quell-IDs bleiben erhalten.
4. `new` markiert eine Lesehilfe-Anforderung ohne quellentreues Einzelgegenstück.
5. `not-comparable` markiert eine geltende Anforderung ohne ausdrückliches Lesehilfe-Gegenstück. Solche Anforderungen dürfen nicht stillschweigend entfallen.
6. Nicht verbindliche Beispiele sind mögliche Kontexte, keine zusätzlichen Pflichtkompetenzen.
7. Operatoren und Prozesskompetenzen werden in `operators.json` quellengebunden erhalten. Das dortige Komplexitätsband ist eine Aufgabenheuristik und keine universelle Operatorenhierarchie.

Die acht direkten Brücken `XW-045` bis `XW-052` machen fachliche Überschneidungen zwischen Basiskurs Medienbildung und Aufbaukurs Informatik explizit. Ihre Richtung vom früheren Basiskurs zum späteren Aufbaukurs dient nur der konsistenten Datenmodellierung; sie behauptet keine zusätzliche normative Jahrgangsprogression.

## 3. Fünf wiederkehrende Stränge

| Strang | Wiederkehrender fachlicher Kern | Curriculare Anker | Didaktische Funktion |
|---|---|---|---|
| **A. Modellieren, Algorithmen und Programmieren** | präzise Abläufe, externe Darstellungen, Grundbausteine, Ausführung, Werte, Implementieren, Analysieren, Testen und Bewerten | `LH26-E-ALG-*`; `INF7-16-GYM-PK-SV-*`; `INF7-16-GYM-PK-MI-*`; `INF7-16-GYM-PK-AB-001`; `INF7-16-GYM-IK-ALG-*` | Von ausführbaren Handlungen und Codeverständnis zu selbstständiger Implementation; Testen und Bewerten bleiben als enacted Anforderungen erhalten. |
| **B. Information, Daten und Codierung** | Recherche, Quellenqualität, Akteure und Motive, Informationsverarbeitung, Codierung, Bitfolgen, Datenmengen und Ressourcenbezug | `LH26-E-ID-*`; `BMB16-GYM-PK-HK-001`; `BMB16-GYM-IK-IW-*`; `INF7-16-GYM-IK-DC-*` | Information und Daten begrifflich trennen; von Nutzung und Prüfung zu formaler Repräsentation und begründeter Codierungsentscheidung führen. |
| **C. Rechner, Netze, Kommunikation und Sicherheit** | Gerät und Betriebssystem, Dateien und Speicherorte, Netzmodelle, Client–Server, digitale Kommunikation, Zugangsschutz, Recht und Verschlüsselung | `LH26-E-KS-*`; `LH26-E-DA-001` bis `-004`; `BMB16-GYM-IK-KK-*`; `BMB16-GYM-IK-GM-*`; `INF7-16-GYM-IK-RN-*`; `INF7-16-GYM-IK-IGD-*` | Bedienhandlung mit Systemmodell verbinden; von sicherer schulischer Nutzung zu Netz- und Verschlüsselungsmodellen sowie begründeten Sicherheitsurteilen entwickeln. |
| **D. Digitalität, Medienanalyse und Partizipation** | Mediennutzung, Akteure und Interessen, Werbung, Datenerhebung, Einfluss, Desinformation, Rollenbilder, Gaming und gesellschaftliche Folgen | `LH26-E-DP-*`; `BMB16-GYM-PK-RK-*`; `BMB16-GYM-IK-MG-*`; `INF7-16-GYM-PK-AB-004` bis `-006` | Von beschreibbarer Nutzung zu Mechanismus–Akteur–Interesse–Evidenz-Analysen und revidierbaren Urteilen führen, ohne persönliche Offenlegung oder Diagnostik zu verlangen. |
| **E. Digitales Arbeiten, Produktion und Kooperation** | Strukturieren, gestalten, Wirkungsabsicht, Medienprodukt, Zusammenarbeit, Quellen und Rechte, Teilen, Prüfen und Überarbeiten | `LH26-E-DA-005` bis `-017`; `BMB16-GYM-PK-HK-002` bis `-003`; `BMB16-GYM-IK-PP-*`; `INF7-16-GYM-PK-KK-*` | Bedienkompetenz in fachlich begründete Produktion überführen; Zielgruppe, Zweck, Gestaltung, Rechte, Feedback, Test und Revision sichtbar machen. |

Die Stränge sind wiederkehrend, aber keine fünf isolierten Lehrgangsfächer. Ein integriertes Modul ist nur dann gerechtfertigt, wenn es den informatischen Erkenntnisgewinn, den medienbildnerischen Erkenntnisgewinn und ihre notwendige Beziehung getrennt benennen kann.

## 4. Voraussetzungskonzepte

Die folgenden Abhängigkeiten sind **didaktische Sequenzierungsentscheidungen · `working`**. Sie beschreiben keine amtliche Reihenfolge.

### A. Modellieren, Algorithmen und Programmieren

```text
präzise Handlung und Reihenfolge
→ endliche Folge in externer Darstellung
→ Anweisung und Sequenz
→ konstante Wiederholung
→ Code schrittweise ausführen und Wirkung erklären
→ bedingte Wiederholung, Verzweigung und Ausdrücke
→ Werteübergabe, Rückgabe und Datentypen
→ zielorientiert implementieren
→ gezielt testen, überarbeiten und Lösung bewerten
```

Die letzten beiden Schritte sichern die weiterhin geltenden Records `INF7-16-GYM-PK-MI-009` und `INF7-16-GYM-PK-MI-010`, obwohl die Lesehilfe dafür keine eigenen Gegenrecords enthält (`XW-055`).

### B. Information, Daten und Codierung

```text
Fragestellung und Informationsbedarf
→ digitale Recherche und Auswahl
→ Kriterien, Beleg und widersprüchliche Quellen
→ Akteur, Interesse und Veröffentlichungsmechanismus
→ Information, Zeichen und vereinbarte Codierung
→ Umkehrbarkeit und Codieren/Decodieren
→ Text/Bild als Bitfolge
→ Datenmenge, Bit/Byte und Präfixe
→ Ressourcenbezug und begründete Repräsentationsentscheidung
```

Binärdarstellung natürlicher Zahlen sowie der Zusammenhang von Zeichenvorrat, Codelänge und Codewörtern bleiben als `enacted` Inhalte zusätzlich erhalten (`INF7-16-GYM-IK-DC-005`, `INF7-16-GYM-IK-DC-008`; `XW-056`).

### C. Rechner, Netze, Kommunikation und Sicherheit

```text
Gerät, Ein-/Ausgabe und Betriebssystem
→ Datei, Verzeichnis und Speicherort
→ Kommunikationsregel und geschützter Zugang
→ Knoten, Verbindung und Weiterleitung
→ Client, Server, Anfrage und Antwort
→ Datenweg, Speicherort und Schutzbedarf
→ Codierung versus Verschlüsselung
→ Schlüssel, Klartext und Geheimtext
→ Verfahren ausführen, angreifen und Sicherheit bewerten
→ Transport- und Ende-zu-Ende-Verschlüsselung unterscheiden
```

### D. Digitalität, Medienanalyse und Partizipation

```text
Nutzung und beobachtbare Situation
→ Regel, Konflikt und Handlungsoption
→ Akteur und Interesse
→ Datenerhebung, Auswahl oder Gestaltung als Mechanismus
→ mögliche Wirkung und Gegenperspektive
→ Beleg, Gegenbeleg und Unsicherheit
→ begründetes Urteil
→ dokumentierte Revision
```

Persönliche Mediennutzung darf durch fiktive Fälle, vorgegebene Datensätze oder freiwillige Distanzierungsoptionen ersetzt werden. Die Progression begründet keine personenbezogene Diagnose.

### E. Digitales Arbeiten, Produktion und Kooperation

```text
Werkzeugfunktion und Struktur
→ Zielgruppe, Zweck und Wirkungsabsicht
→ Inhalt–Form-Entscheidung
→ Quellen-, Lizenz- und Rechteprüfung
→ eigenständiges Produkt
→ Kriterienprüfung oder Feedback
→ sichtbare Überarbeitung
→ kontrolliertes Teilen beziehungsweise Exportieren
```

## 5. Vorläufige Arbeitsverteilung 5–7

Die folgende Tabelle ist vollständig **didaktisch · `working`**. Für die Klassen 5 und 6 nennt die Lesehilfe nur ein gemeinsames Band. Ein Modulmanifest muss deshalb jede konkrete Zuordnung als Projektentscheidung kennzeichnen.

| Jahrgang | Vorläufige Leitidee | Schwerpunkt A–E | Zunehmende Selbstständigkeit |
|---|---|---|---|
| **5** | In der schulischen digitalen Umgebung sicher handeln, Informationen und Medienhandlungen präzise beschreiben und erste Modelle aufbauen. | A: präzise Folgen, Anweisung, grafische Darstellung; B: recherchieren, auswählen, erste Qualitätskriterien; C: Gerät, Betriebssystem, Datei, Kommunikationsregel, Zugangsschutz; D: Nutzung, Regeln, Konflikte, Werbung identifizieren; E: strukturiertes einfaches Produkt mit Ziel und Quellenangabe. | Stark modellierte Beispiele, gemeinsame Begriffsbildung, kurze fokussierte Übung; Produktentscheidungen mit vorgegebenen Kriterien. |
| **6** | Hinter Bedienoberflächen liegende Mechanismen erklären, Modelle vergleichen und bekannte Praktiken auf neue Kontexte übertragen. | A: konstante Schleife, einfache Implementation, Code schrittweise analysieren; B: indexbasierte Suche, Akteure/Motive, widersprüchliche Quellen, Codierung von Text; C: Netz, Weiterleitung, Client–Server, Speicherorte; D: Datenerhebung, Werbeauswahl, informationelle Selbstbestimmung, verletzendes Verhalten; E: Wirkungsabsicht, Inhalt–Form, Lizenzmodell, Revision und Teilen. | Hilfen werden sichtbar ausgeblendet; Lernende begründen Auswahl, prüfen Ergebnisse und dokumentieren mindestens eine Revision. |
| **7** | Fachliche Modelle formalisieren, technische und gesellschaftliche Perspektiven verbinden und eigenständige Lösungen prüfen. | A: bedingte Schleife, Verzweigung, Ausdrücke, Werte, Datentypen, Implementieren, Tracing, Testen; B: eigene Codierung, ASCII, Pixel, Bit/Byte, Ressourcenbezug; C: Verschlüsselungsbegriffe, Caesar/Substitution, Angriffe und Sicherheitsurteil; D: Akteure, Einfluss, Desinformation, Rollenbilder, Gaming; E: Medienmanipulation, wirkungsverändertes Produkt, Rechte- und Evidenzprüfung. | Eigenständigere Modell-, Code-, Analyse- und Produktionsentscheidungen; Testfälle, Gegenbelege, Feedback und Überarbeitung werden Teil des Lernprodukts. |

Diese Arbeitsverteilung bewahrt die offene Frage, **welche** 5/6-Anforderung in Klasse 5 oder 6 liegt. Sie legt nur eine lernlogische Hypothese für die Roadmap vor.

## 6. Übergang 5 → 6

| Strang | Ende Klasse 5 · Arbeitsannahme | Übergangshandlung | Beginn Klasse 6 · erwartete Anschlussfähigkeit |
|---|---|---|---|
| A | präzise Folge ausführen und darstellen | Darstellung wechseln, Wirkung vorhersagen, Abweichung erklären | konstante Schleife verstehen, einfachen Code ausführen und verändern |
| B | digitale Recherche nutzen und Informationen auswählen | Kriterien auf zwei widersprüchliche Quellen anwenden | Mechanismen der Suche sowie Akteure, Motive und automatisierte Inhalte untersuchen |
| C | Gerät, Datei, Zugang und Kommunikationsregel sicher nutzen | sichtbare Oberfläche mit einfachem System- oder Datenwegmodell verbinden | Netz, Weiterleitung, Client–Server und Speicherorte erklären und vergleichen |
| D | eigene Nutzung und Konflikte beschreiben, Werbung erkennen | vom persönlichen Beispiel auf fiktiven Fall und Akteursinteresse abstrahieren | Datenerhebung, Werbeauswahl und informationelle Selbstbestimmung mechanismisch analysieren |
| E | einfaches Produkt mit Zweck und Grundstruktur erstellen | Kriterien und Quellenregel auf eigenes Produkt anwenden | Wirkungsabsicht begründen, Lizenz beachten, Feedback nutzen und überarbeiten |

## 7. Übergang 6 → 7

| Strang | Ende Klasse 6 · Arbeitsannahme | Übergangshandlung | Klasse 7 · erwartete Anschlussfähigkeit |
|---|---|---|---|
| A | konstante Schleife und einfache Codewirkung erklären | Zustand, übergebenen Wert und Ausführungsposition explizit verfolgen | Verzweigung, bedingte Schleife, Ausdrücke, Typen und Werte zielorientiert implementieren und testen |
| B | Zweck und Umkehrbarkeit einfacher Codierungen erklären | dieselbe Information in Text-, Bild- und Bitdarstellung überführen | ASCII, Pixelcodierung, Datenmengen und formale Codierungsentscheidungen bearbeiten |
| C | Netz-, Client–Server- und Speicherortmodell verwenden | Datenweg, Zugriff und Schutzbedarf in einem Fall verbinden | Verschlüsselung von Codierung trennen, Verfahren angreifen und Sicherheit begründet bewerten |
| D | Akteur, Interesse und Auswahlmechanismus untersuchen | Behauptung, Beleg, Gegenbeleg und Unsicherheit trennen | Desinformation, Rollenbilder und Gaming ohne monokausale Wirkbehauptung analysieren und Urteil revidieren |
| E | Medienprodukt zielbezogen gestalten, Rechte prüfen und überarbeiten | technische Veränderung mit beabsichtigter Wirkung begründen | manipulierte Medienprodukte entwerfen, Wirkung analysieren und Evidenz-/Rechteprüfung dokumentieren |

## 8. Wiederaufnahme mit steigender Komplexität

| Konzept | Erste Begegnung | Wiederaufnahme | Vertiefung |
|---|---|---|---|
| **Algorithmus** | präzise endliche Handlung und grafische Folge | konstante Schleife, einfache Programmiersprache, Tracing | bedingte Schleife, Verzweigung, Ausdrücke, Werte, Typen, Implementieren und Testen |
| **Information und Vertrauenswürdigkeit** | recherchieren, auswählen, einfache Kriterien | widersprüchliche Quellen, Akteure, Motive, indexbasierte Suche und automatisierter Content | Desinformation, Einflussnahme, Beleg/Gegenbeleg, Unsicherheit und Revision |
| **Daten und Codierung** | verschiedene Zwecke und Codierung von Text | Umkehrbarkeit, Codieren/Decodieren und Darstellungswechsel | eigene Vorschrift, ASCII, Pixel, Bitfolge, Datenmenge und Ressourcenbezug |
| **Netz und Kommunikation** | schulischer Kanal, Regel und Zugang | Knoten, Verbindung, Weiterleitung, Client–Server und Speicherorte | Datenweg, Schutzmodell, Transport-/Ende-zu-Ende-Verschlüsselung und Sicherheitsurteil |
| **Akteure, Interessen und Wirkung** | Nutzung, Werbung und Konflikt | Datenerhebung, Werbeauswahl, Selbstdarstellung und Plattforminteresse | Desinformation, Rollenbilder, Monetarisierung und gesellschaftliche Perspektiven |
| **Medienproduktion** | einfaches strukturiertes Produkt | Zielgruppe, Wirkungsabsicht, Quellen, Lizenz, Feedback und Revision | technische Manipulation, intendierte Wirkungsveränderung und begründete Evidenz-/Rechteentscheidung |

Wiederholung zählt nur dann als Progression, wenn mindestens eine Dimension steigt: fachliche Beziehungen, Repräsentationswechsel, Selbstständigkeit, Begründungstiefe, Unsicherheit, Prüfhandlung oder Transfer.

## 9. Drei Perspektiven in jedem Strang

Die Quellen verlangen keine einheitliche Dreischritt-Methode. Für die Roadmap gilt dennoch als **Projektentscheidung · `working`**:

- **Technische Perspektive:** Welche Daten, Regeln, Komponenten, Zustände, Verfahren oder Algorithmen bewirken etwas?
- **Anwendungsbezogene Perspektive:** Welche Handlung, welches Werkzeug, welches Produkt oder welche Entscheidung löst eine konkrete Aufgabe?
- **Gesellschaftlich-mediale Perspektive:** Welche Akteure, Interessen, Rechte, Wirkungen, Werte, Unsicherheiten und Handlungsfolgen sind beteiligt?

Nicht jedes Einzelmodul muss alle drei Perspektiven gleichgewichtig behandeln. Über einen Strang und über einen Jahrgang hinweg müssen sie jedoch verbunden werden. Eine Integration ist nur fachlich, wenn die Beziehung selbst gelernt wird.

## 10. Operatoren und sichtbare Lernhandlungen

`operators.json` bewahrt 41 amtliche Operatorrecords und 37 Prozesskompetenzrecords einzeln. Für Aufgaben gelten folgende Regeln:

1. Der exakte amtliche Term, seine Definition und der Quellen-AFB dürfen nicht vereinheitlicht oder stillschweigend umgedeutet werden.
2. Gleichnamige Operatoren aus Basiskurs und Aufbaukurs bleiben getrennt, wenn Definition oder AFB abweichen.
3. Prozesskompetenzen werden nicht als Operatoren ausgegeben.
4. Das Feld `expectedObservableAction` beschreibt ein prüfbares Verhalten oder Produkt; es ersetzt keine personenbezogene Kompetenzmessung.
5. `likelyComplexityBand` dient nur dem Aufgabenreview. Materialmenge, Neuigkeit, Hilfen, Selbstständigkeit, Begründung und Produkt können die tatsächliche Komplexität verändern.
6. Über die Progression steigt nicht bloß das Operatorwort, sondern die fachliche Relation: von benennen/bedienen über strukturiert anwenden und erklären zu entwerfen, testen, analysieren, begründen und bewerten.

## 11. Offene curriculare und didaktische Fragen

### 11.1 Klassen 5 und 6

Offen bleibt:

- welche kombinierte 5/6-Anforderung in Klasse 5 oder 6 liegt;
- welche Inhalte innerhalb eines Schuljahres wiederaufgenommen werden;
- wie viel Programmier- und Netzwerktiefe die Jahrgänge 5 und 6 unter realen Zeitbedingungen tragen;
- welche schulischen Geräte-, Browser- und Netzvoraussetzungen vorausgesetzt werden können.

Bis zur Klärung werden Module über explizite Voraussetzungen verbunden. Eine Roadmap darf die oben vorgeschlagene Arbeitsverteilung ändern, wenn Curriculumabdeckung und Lernlogik erhalten bleiben.

### 11.2 Verhältnis Lesehilfe zu geltenden Plänen

Die Lesehilfe beschreibt für Klasse 7 weniger Informatikanteile und mehr Medienbildung. Sie hebt den Aufbaukurs nicht auf. Deshalb bleiben insbesondere folgende enacted Anforderungen erhalten:

- Abstraktion (`INF7-16-GYM-PK-MI-003`);
- Adaptieren fremder Codebausteine (`INF7-16-GYM-PK-MI-008`);
- Programme gezielt testen und Lösungen bewerten (`INF7-16-GYM-PK-MI-009`, `-010`);
- Binärdarstellung natürlicher Zahlen und formaler Codewortzusammenhang (`INF7-16-GYM-IK-DC-005`, `-008`).

Der spätere Abdeckungsplan muss dafür Zeit ausweisen oder die curriculare Konfliktlage ausdrücklich eskalieren. Ein stilles Streichen ist ausgeschlossen.

### 11.3 Neue Lesehilfe-Gegenstände

Als `new` geführt werden:

- die Erklärung, wie eine spezifisch ausgewählte Werbebotschaft zustande kommt (`XW-008`);
- automatisierte Content-Erzeugung und -Verbreitung sowie Chancen und Fehlerrisiken KI-generierter Rechercheergebnisse (`XW-014`);
- soziale Aspekte und Monetarisierungsmodelle digitaler Spiele (`XW-033`).

Diese Gegenstände benötigen eigenständige Modulabdeckung, dürfen aber nicht als Beleg dafür dienen, enacted Informatik- oder Medienbildungsanforderungen zu verdrängen.

Eingebettete Werbung, indexbasierte Suche, Akteurs- und Motivlagen, psychologische Aspekte sowie die Reflexion eigener Spielnutzung und technische Medienmanipulation sind dagegen spezifische Erweiterungen oder Neurahmungen vorhandener Anforderungen. Der Crosswalk behandelt sie deshalb nicht mehr pauschal als `new`.

## 12. Review- und Revisionsregeln

Die Progression wird erneut geprüft, wenn:

- ein neuer Fachplan veröffentlicht, geändert oder in Kraft gesetzt wird;
- eine amtliche Quelle ihren Geltungsstatus ändert;
- Task 13–15 Zeit- oder Abdeckungskonflikte nachweisen;
- ein Fachreview eine unhaltbare Voraussetzung oder fachliche Verkürzung findet;
- Pilotierungen wiederholt zeigen, dass eine Übergangshandlung nicht trägt;
- schulische Technikbedingungen einen zentralen digitalen Lernweg verhindern.

Eine Statusanhebung von `working` auf `reviewed` verlangt mindestens:

1. vollständigen Abdeckungsplan gegen alle `enacted` Records;
2. Informatik- und Medienbildungsfachreview;
3. Prüfung der offenen 5/6-Verteilung;
4. Prüfung der Zeitkorridore;
5. dokumentierte Pilotbefunde zu den zentralen Übergängen;
6. erneuten Abgleich mit dem dann aktuellen amtlichen Stand.
