# IuM-Lernwerk – Phase 2: Entwicklungs- und Einsatzgate

**Status:** zur Schriftprüfung nach freigegebener Designentscheidung

**Datum:** 3. August 2026

**Scope:** Start von Phase 2 mit `IUM-5-CORE-05 – Präzise Abläufe ausführbar machen`

**Ausgangsstand:** `main` auf Commit `2caa0c5`

## 1. Entscheidung

Phase 2 wird in zwei voneinander unabhängige Gates getrennt:

1. Das **Entwicklungsgate** erlaubt die fachlich-didaktische Spezifikation, technische Umsetzung und interne Qualitätssicherung des ersten Lernmoduls.
2. Das **Einsatzgate** erlaubt erst nach gesondertem Nachweis die reale Unterrichtspilotierung, LMS-Einbindung und Veröffentlichung als nutzbares Lernwerkmodul.

Das offene Phase-1-Realgerätegate `IUM14` blockiert damit nicht länger die Entwicklung von Phase 2. Es blockiert weiterhin den realen Einsatz und bleibt unverändert `blocked`; `device-verified` bleibt `not-run`.

Diese Trennung nimmt keinen fehlenden Nachweis vorweg. Sie verhindert lediglich, dass externe Geräte-, MDM- und LMS-Voraussetzungen die fachliche Produktentwicklung vollständig anhalten.

## 2. Ausgangslage

Das Plattformfundament ist technisch umgesetzt. Die automatisierten Qualitätsgates sind grün, und alle vorgesehenen iPad-Interaktionspfade wurden am realen Gerät positiv beobachtet. Nicht nachweisbar sind weiterhin:

- das genaue iPad-Modell sowie iPadOS- und Safari-Version;
- MDM-, Web-Clip-, Speicher-, Filter-/Proxy- und Netzrichtlinien;
- ein verwaltetes Chromium-/Firefox-Desktopziel;
- ein realer LMS-Prüfkontext.

Deshalb ist der technische Status `implemented` belegt, der Status `device-verified` jedoch nicht. Die frühere Formulierung „Phase 2 bleibt bis zum bestandenen Gerätegate vollständig gesperrt“ koppelte daran auch Arbeiten, die keine reale Zielumgebung benötigen. Diese Kopplung wird mit der vorliegenden Spezifikation präzise aufgelöst.

## 3. Bindende Grundlagen

Unverändert bindend bleiben:

- das freigegebene Gesamtdesign des modularen digitalen Lernwerks;
- die Phase-0-Forschungs-, Fachprofil-, Curriculum- und Roadmapbestände;
- die freigegebene Phase-1-Spezifikation und ihre Plattformverträge;
- die Statusfolge `draft → working → reviewed → standard`;
- lokale, datensparsame Lernstände ohne Konto, Backend, Telemetrie oder personenbezogene Diagnostik;
- digital als selbstverständliches Primärmedium;
- analoge Materialien nur bei einer eigenständigen fachlichen oder lernpsychologischen Funktion;
- eigener Code unter MIT und eigene Lerninhalte unter CC BY-SA 4.0;
- öffentliche Quelloffenheit über GitHub bei eindeutiger Kennzeichnung unfertiger Arbeitsstände.

## 4. Betrachtete Ansätze

### 4.1 Gewählt: getrenntes Entwicklungs- und Einsatzgate

Die Entwicklung kann auf dem verifizierten Plattformstand beginnen. Reale Einsatzbehauptungen bleiben an ein separates, fail-closed geprüftes Gate gebunden.

Vorteile:

- fachlicher Fortschritt trotz externer Geräteblocker;
- keine Umdeutung automatisierter Tests in reale Evidenz;
- frühe Prüfung des Plattformvertrags an einem echten Lernmodul;
- klare Trennung von Produktentwicklung, Pilotierung und Release.

### 4.2 Verworfen: vollständiger Stillstand bis IUM14

Dieser Ansatz wäre formal streng, würde aber auch Didaktik, Inhalte und lokal prüfbare Technik von derzeit nicht beschaffbaren MDM- und LMS-Nachweisen abhängig machen. Er erzeugt keinen zusätzlichen Schutz für Lernendendaten, solange Entwicklung und Tests ausschließlich mit synthetischen Daten erfolgen.

### 4.3 Verworfen: IUM14 aufgrund der positiven iPad-Runden als bestanden werten

Die funktionalen iPad-Beobachtungen ersetzen weder die unbekannten Policy- und Versionsdaten noch die fehlende Desktop-/LMS-Matrix. Eine solche Hochstufung wäre eine unbelegte Qualitätsbehauptung.

## 5. Gate A – Entwicklung

### 5.1 Voraussetzungen

Das Entwicklungsgate gilt als geöffnet, weil:

- Phase 1 den technischen Status `implemented` erreicht hat;
- der Hauptstand reproduzierbar gebaut und automatisch geprüft wird;
- die zentralen iPad-Interaktionspfade ohne gemeldete Abweichung durchlaufen wurden;
- Entwicklung, Review und Tests ohne reale Lernendendaten möglich sind;
- der Nutzer die Gate-Trennung ausdrücklich freigegeben hat.

### 5.2 Erlaubte Arbeiten

Gate A erlaubt:

- eine detaillierte fachlich-didaktische Modulspezifikation;
- ein vollständiges digitales Lernendenmodul;
- das zugehörige Lehrkräftehandbuch;
- curriculare Zuordnung sowie Quellen- und Lizenznachweise;
- lokale und CI-basierte Builds, Tests und interne Reviews;
- Speicherung unfertiger Quellen im öffentlichen GitHub-Repository mit dem Modulstatus `working`;
- eine lokale oder CI-interne Vorschau, die eindeutig als Entwicklungsstand gekennzeichnet ist.

### 5.3 Nicht erlaubte Arbeiten

Gate A erlaubt ausdrücklich nicht:

- reale Unterrichtspilotierung;
- Einsatz mit realen Lernendendaten;
- Verknüpfung oder Veröffentlichung in einem LMS;
- Aufnahme des Moduls in den öffentlich nutzbaren Produktkatalog oder ein stabiles Lernwerk-Release;
- ein Pages-Deployment, das das fachliche Modul als einsatzbereites Angebot ausliefert;
- Hochstufung auf `reviewed` oder `standard` allein aufgrund automatisierter Tests;
- die Kennzeichnung von Phase 1 oder Phase 2 als `device-verified`;
- integrierte Individualdiagnostik, automatische Benotung oder Personenprofile.

Die öffentliche Sichtbarkeit von Quelltexten und Arbeitsinhalten im Repository ist OER-Entwicklung, aber keine Produktfreigabe. README, Manifest und Oberfläche müssen den Arbeitsstatus eindeutig ausweisen.

## 6. Gate B – Einsatz, Pilotierung und Release

Gate B bleibt geschlossen. Es wird erst durch einen eigenen Auftrag und einen dokumentierten Nachweis geöffnet.

### 6.1 Mindestvoraussetzungen

Vor realer Pilotierung oder LMS-/Produktveröffentlichung müssen mindestens vorliegen:

- ein bestandener oder ausdrücklich begrenzt akzeptierter IUM14-Nachweis für die tatsächlich verwendete Zielumgebung;
- dokumentierte Browser-, Betriebssystem-, Policy- und LMS-Rahmenbedingungen, soweit sie für den Einsatz relevant und zugänglich sind;
- eine modulspezifische reale Geräteprüfung des vollständigen Lernpfads einschließlich Tastatur- oder Touchbedienung, Screenreaderpfad, Speicherung, Offlineverhalten und Update;
- abgeschlossene fachliche, didaktische, technische, Accessibility-, Datenschutz- und Lizenzreviews;
- ein separates Pilotierungsprotokoll mit synthetischer Vorbereitung und datensparsamer realer Durchführung;
- ausdrückliche Nutzerfreigabe für Pilot oder Release.

### 6.2 Ausnahmeentscheidung

Sind einzelne Konfigurationsnachweise trotz angemessener Beschaffungsversuche nicht verfügbar, kann der Nutzer später eine begrenzte Risikoakzeptanz aussprechen. Diese Entscheidung muss:

- die fehlenden Nachweise einzeln benennen;
- Zielgruppe, Gerät, Browser, LMS und Zeitraum des erlaubten Einsatzes begrenzen;
- verbleibende Risiken und Rückfallmaßnahmen dokumentieren;
- `device-verified` weiterhin als `not-run` oder nicht bestanden ausweisen, sofern die ursprünglichen Kriterien nicht erfüllt sind;
- Pilot- und Produktfreigabe getrennt entscheiden.

Eine Risikoakzeptanz entsteht niemals automatisch aus Zeitablauf, grünem CI oder positiven Einzelbeobachtungen.

## 7. Erster Phase-2-Arbeitsauftrag

Phase 2 beginnt mit dem bereits ausgewählten Goldstandard-Modul:

`IUM-5-CORE-05 – Präzise Abläufe ausführbar machen`

Verbindliche curriculare Eckdaten:

| Feld | Vertrag |
|---|---|
| Jahrgang | Gymnasium, Klasse 5 |
| Art | Kernmodul |
| Lernstrang | `STRAND-A` |
| Kompetenzen | `LH26-E-PROG-002`, `LH26-E-ALG-001` bis `LH26-E-ALG-004` |
| Voraussetzung | `IUM-5-CORE-01` |
| Leitfrage | Wie genau muss eine Vorschrift sein, damit Mensch und digitales System denselben Ablauf ausführen? |
| Zentrale Lernhandlung | Alltagshandlungen präzisieren, grafische Algorithmen ausführen, Abweichungen erklären und eine konstante Wiederholung als Grundbaustein modellieren. |
| Lernprodukt | Ausführbarer grafischer Algorithmus mit Vorhersage, Laufprotokoll, reparierter Fassung und begründeter Schleifenentscheidung. |
| Modulstatus | `working` |

## 8. Zeitvertrag

Der reguläre und der Basispfad umfassen jeweils **5 Unterrichtseinheiten beziehungsweise 225 Minuten**. Der Erweiterungspfad umfasst **6 Unterrichtseinheiten beziehungsweise 270 Minuten**.

| Lernphase | regulär | erweitert |
|---|---:|---:|
| Orientierung und Herausforderung | 15 min | 15 min |
| Vorwissen aktivieren | 20 min | 20 min |
| Begriffe und Konzept aufbauen | 35 min | 35 min |
| Angeleitet üben | 45 min | 60 min |
| Eigenständiges Lernprodukt | 55 min | 75 min |
| Prüfen, überarbeiten und transferieren | 35 min | 40 min |
| Gemeinsam sichern | 20 min | 25 min |

Der historische Korridor von fünf bis sieben Unterrichtseinheiten bleibt als Herkunftsangabe erhalten. Für das erste Produkt werden jedoch nur die bereits auditierten Varianten mit fünf und sechs Unterrichtseinheiten umgesetzt. Eine siebte Einheit ist kein verdeckter Produktumfang und benötigt bei späterem Bedarf eine eigene Begründung.

Der Erweiterungspfad muss zusätzliche reale Algorithmusausführung und Fehlerkorrektur enthalten. Mehr Demonstration oder zusätzliche Produktanforderungen ohne Lernfunktion gelten nicht als Erweiterung.

## 9. Inhaltlicher und medialer Umfang

Die detaillierte Modulspezifikation muss mindestens gestalten:

1. eine altersangemessene Orientierungssituation mit einem erkennbar mehrdeutigen Ablauf;
2. Aktivierung relevanten Vorwissens ohne Ersatz des vorausgesetzten Moduls `IUM-5-CORE-01`;
3. Aufbau der Begriffe Anweisung, Algorithmus, Ausführung, Zustand, Abweichung und Schleife mit konstanter Wiederholungszahl;
4. angeleitete Ausführung und Vergleich von Vorhersage und tatsächlicher Laufspur;
5. ein eigenständig erstelltes oder vervollständigtes grafisches Algorithmusprodukt;
6. gezielte Fehlersuche, Reparatur und begründete Revision;
7. integrierte Klassifikation digitaler Systeme, deren Funktion wesentlich algorithmisch bestimmt ist;
8. gemeinsame Sicherung und einen nahen Transferfall.

Das digitale Medium ist fachlich notwendig, weil es Schrittfolge, Position, Zustand, Wiederholung und reproduzierbare Abweichungen unmittelbar koppeln kann. Für den ersten Arbeitsauftrag sind keine analogen Materialien vorgesehen. Eine spätere analoge Ergänzung ist nur über eine dokumentierte eigenständige Lernfunktion zulässig; eine parallele Druckkopie der digitalen Struktur bleibt ausgeschlossen.

## 10. Lieferumfang

Der erste Phase-2-Arbeitsstrang liefert:

- ein produktionsnahes Modulmanifest und alle fachlichen Modulquellen;
- die vollständige Lernendenoberfläche für den regulären Fünf-UE-Pfad;
- die klar abgrenzbare Erweiterung auf sechs UE;
- eine barrierearme Alternative für jede Zeiger-, Drag-, Canvas- oder räumliche Interaktion;
- lokale Speicherung, Export, Import und Löschung über die bestehenden Plattformverträge;
- ein Lehrkräftehandbuch mit Lernzielen, fachlichem Hintergrund, Fehlvorstellungen, Scaffolds, Unterrichtsorganisation, Zeitvarianten, Beobachtungskriterien und Rückfalloptionen;
- transparente Kriterien für Produkt, Erklärung und Revision ohne automatische Punktzahl oder Personenprofil;
- Curriculum-, Quellen-, Asset- und Lizenzmapping;
- automatische fachliche Vertrags-, Unit-, Browser-, Offline-, Accessibility-, Lizenz- und Isolationsprüfungen.

## 11. Architekturgrenzen

Das fachliche Modul nutzt die bestehenden Phase-1-Verträge. Es darf das Plattformfundament nur erweitern, wenn ein konkreter Lernbedarf dies erfordert und ein neuer Plattformvertrag separat getestet wird.

Verbindlich sind:

- fachliche Modulquellen unter dem regulären `modules/`-Pfad;
- keine Vermischung mit `TEST-PLATFORM-REFERENCE` oder synthetischen Curriculum-Fixtures;
- keine fachlichen Daten im Portal- oder Speicherpaket;
- kein Konto, Backend, Tracking, Telemetrie oder externe Laufzeitabhängigkeit im Kernpfad;
- keine dynamische Codeausführung aus Lernstands- oder Importdaten;
- deterministische Ausführung der grafischen Algorithmen;
- ein explizites, versioniertes Zustandsschema;
- Systemschrift und bestehende UI-Grundbausteine, solange kein nachgewiesener Lernbedarf eine Erweiterung erfordert;
- kein automatisches Deployment des Arbeitsstands als Produktrelease.

## 12. Daten- und Beurteilungsgrenze

Das Modul speichert nur den für die Lernhandlung notwendigen lokalen Arbeitsstand. Namen, E-Mail-Adressen, Klassenkennungen, Gerätekennungen und personenbezogene Diagnosedaten werden weder verlangt noch erzeugt.

Beurteilbar sind das sichtbare Lernprodukt, die fachliche Erklärung und die dokumentierte Revision. Die Kriterien unterstützen Rückmeldung und Unterrichtsbeobachtung. Sie erzeugen keine automatischen Punkte, keine Rangfolge, keine verdeckte Kompetenzdiagnose und kein dauerhaftes Personenprofil.

## 13. Qualitätssicherung

Vor einem technischen Implementierungsabschluss müssen mindestens bestehen:

- Schema- und Referenzprüfung des Modulmanifests;
- exakte Zuordnung der fünf Kompetenzrecords und des Zeitvertrags;
- Tests für Schrittfolge, Zustand, konstante Wiederholung, Vorhersage, Laufprotokoll, Fehler und Reparatur;
- Verlustfreiheit von Speichern, Neuladen, Export, Löschen und Import;
- vollständige Tastaturbedienung und bedienbare Nicht-Drag-Alternative;
- Screenreader-kompatible Struktur, Status- und Fehlermeldungen;
- Reflow, Zoom, Touchziele, Kontrast und reduzierte Bewegung;
- Offline-Kernpfad und kontrolliertes Update ohne Zustandsverlust;
- keine Drittanbieterrequests, Telemetrie oder Fixture-Kontamination;
- vollständige Lizenz- und Quellenmetadaten;
- getrenntes fachliches, didaktisches und technisches Review.

Automatisierte Nachweise dürfen den Modulstatus nicht über `working` anheben und öffnen Gate B nicht.

## 14. Arbeitsfolge

Die verbindliche Reihenfolge lautet:

```text
vorliegende Gate-Spezifikation schriftlich freigeben
→ detailliertes didaktisches und interaktives Moduldesign erarbeiten
→ Modulspezifikation schriftlich freigeben
→ testgetriebenen Implementierungsplan erstellen
→ Modul sequenziell implementieren
→ fachliches, didaktisches und technisches Review
→ Gate B mit realer Zielumgebung prüfen oder begrenzt entscheiden
→ erst danach Pilotierung, LMS-Einbindung oder Produktrelease
```

Die Phase-2-Entwicklung wird zunächst sequenziell geführt. Subagenten oder parallele Branches werden nur eingesetzt, wenn ein freigegebener Plan voneinander unabhängige Schreibbereiche und einen eindeutigen Integrationspunkt ausweist.

## 15. Supersession und Statuswirkung

Diese Spezifikation ersetzt ausschließlich frühere Aussagen, nach denen IUM14 **jede** Arbeit an Phase 2 blockiert. Künftig gilt:

| Bereich | Wirkung von IUM14 |
|---|---|
| fachlich-didaktische Konzeption | blockiert nicht |
| technische Implementierung mit synthetischen Daten | blockiert nicht |
| automatische QA und internes Review | blockiert nicht |
| reale Unterrichtspilotierung | blockiert |
| LMS-Einbindung | blockiert |
| Veröffentlichung als einsatzbereites Modul | blockiert |
| Status `device-verified` | bleibt `not-run` |

Alle übrigen Anforderungen und Definition-of-Done-Kriterien der Phase-1-Spezifikation bleiben unverändert. Die Phase-1-Initiative und IUM14 dürfen deshalb weiterhin `blocked` bleiben, während die neue Phase-2-Entwicklungsinitiative `in_progress` ist.

## 16. Akzeptanzkriterien dieser Spezifikation

- Entwicklungs- und Einsatzgate sind begrifflich und operativ getrennt.
- IUM14 wird weder geschlossen noch stillschweigend abgeschwächt.
- Öffentliche GitHub-Quellen werden klar von Produktveröffentlichung unterschieden.
- Umfang, Zeitvarianten, Kompetenzbezug und Lieferobjekte des ersten Moduls sind festgelegt.
- Diagnostik-, Datenschutz-, OER-, Accessibility- und Analoggrenzen bleiben erhalten.
- Die ältere vollständige Phase-2-Sperre ist nur in ihrem Entwicklungsanteil ersetzt.
- Der nächste zulässige Schritt ist das detaillierte Moduldesign, nicht bereits Unterrichtseinsatz oder Release.

## 17. Schriftliches Freigabegate

Mit Freigabe dieser Spezifikation werden die Gate-Trennung, der erste Phase-2-Arbeitsauftrag und seine Scopegrenzen verbindlich.

Die Freigabe startet noch keine Modulimplementierung. Der nächste Schritt ist die zusammenhängende fachlich-didaktische und interaktive Ausgestaltung von `IUM-5-CORE-05`. Erst deren schriftlich freigegebene Spezifikation darf mit `superpowers:writing-plans` in einen testgetriebenen Implementierungsplan überführt werden.
