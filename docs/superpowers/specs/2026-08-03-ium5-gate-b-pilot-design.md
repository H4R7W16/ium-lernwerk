# IUM-5-CORE-05 Gate-B-Prüfung: Spezifikation

**Stand:** 2026-08-03  
**Version:** 0.1  
**Spezifikationsstatus:** `review`  
**Designstatus:** durch den Auftraggeber freigegeben  
**Produktstatus:** unverändert `working`  
**Gerätestatus:** unverändert `device-verified: not-run`

## 1. Zweck und Entscheidungsgrenze

Diese Spezifikation definiert das modulspezifische Gate-B-Paket für `IUM-5-CORE-05 – Präzise Abläufe ausführbar machen`. Es soll drei bislang fehlende Nachweisarten kontrolliert ermöglichen:

1. eine reale technische Prüfung des tatsächlichen Modulbuilds auf den vorgesehenen Zielkonfigurationen;
2. eine datensparsame, lehrkraftorchestrierte Erprobung des vollständigen Lernwegs in zwei aufeinanderfolgenden Unterrichtskontexten;
3. ein fail-closed Entscheidungsdossier für die spätere Prüfung, ob das Modul zur Freigabeprüfung eines `working`-Releases zugelassen werden kann.

IUM19 spezifiziert und plant nur das dafür benötigte Werkzeug-, Publikations- und Verfahrenspaket. Es erlaubt noch keine reale Pilotierung, keine Erhebung realer Evidenz, keine LMS-Einbindung, keine Produktveröffentlichung und keine Statushochsetzung.

Die folgenden Entscheidungen bleiben getrennt und ausdrücklich menschlich:

- **Pilot-Eintritt:** Darf eine zeitlich und sachlich begrenzte Unterrichtserprobung beginnen?
- **LMS-Nutzung:** Darf die Prüffassung im konkreten schulischen LMS verlinkt oder eingebettet werden?
- **Releaseprüfung:** Ist die Evidenz hinreichend, um eine Freigabeprüfung für einen weiterhin als `working` gekennzeichneten Release zu beginnen?
- **Produktfreigabe:** Darf das Modul öffentlich als unterrichtsgeeignet angeboten werden?

Keine Softwarekomponente darf diese Entscheidungen automatisch treffen oder Produktmetadaten verändern.

## 2. Normative Ausgangsbasis

Die Spezifikation bindet folgende bestehende Verträge, ohne sie zu überschreiben:

- `docs/superpowers/specs/2026-08-03-ium-phase2-entwicklungs-und-einsatzgate-design.md` trennt Gate A und Gate B.
- `docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md` definiert Lernweg, Zeitmodell, Daten-, Accessibility-, Offline- und Statusvertrag.
- `docs/fachprofil/ium-gymnasium-5-7.md` bindet Informatik- und Medienbildungsdidaktik, lehrkraftorchestrierte Nutzung, digitalen Primärmodus und Datenschutzgrenzen.
- `docs/platform/device-verification.md` hält das reale Phase-1-Gerätegate fail-closed.
- `docs/superpowers/specs/2026-08-01-ium11-grade7-working-40-pilot-design.md` liefert wiederverwendbare Datenschutz-, Unterdrückungs-, Evidenz- und Entscheidungsprinzipien.
- `modules/IUM-5-CORE-05/module.yaml` definiert den aktuellen Modulvertrag `0.1.0`, fünf reguläre beziehungsweise sechs erweiterte Unterrichtseinheiten und den Status `working`.

Das IUM11-Offlinesystem ist kein technischer oder fachlicher Unterbau von IUM19. Wiederverwendet werden ausschließlich die bewährten Prinzipien der Datenminimierung, Aggregation, Unterdrückung kleiner Rückmeldezahlen, getrennten Reviews und fail-closed Entscheidung. Es entsteht kein zweites Cockpit.

Die IBBW-WU-Bände 1, 5 und 9 dienen als theoriegeleitete Planungsfolie für lernförderliches Klima, formatives Feedback und funktionsgerechten digitalen Medieneinsatz. Sie sind Entwurfsgrundlage, kein empirischer Wirksamkeitsnachweis für dieses Modul. Der Pilot prüft Umsetzbarkeit und Lernprozessqualität, nicht kausale Wirksamkeit.

## 3. Geltungsbereich

### 3.1 Im Umfang

- modulspezifisches Gate-B-Protokoll mit geschlossenen Kategorien;
- synthetische Pass-, Revisions- und Nicht-auswertbar-Beispiele;
- Schema- und Validatorvertrag für technische Evidenz, Pilotaggregate und Entscheidungspaket;
- manuell ausgelöste, zeitlich begrenzte HTTPS-Prüffassung auf GitHub Pages;
- eindeutige Prüffassungskennzeichnung auf jeder Seite und in den Buildmetadaten;
- technische Prüfläufe für iPad/Safari/VoiceOver, verwaltete Desktopbrowser, Schulnetz, Offline/Update und LMS-Routing;
- zwei gestufte, datensparsame Unterrichtsläufe;
- kompakter analoger Beobachtungsbogen für die unterrichtsbegleitende Fremdbeobachtung;
- Leitfäden für Durchführung, Datenschutz, Aggregation, Review, Abbruch und Löschung;
- automatische Qualitätsgates für die Implementierung des Pakets.

### 3.2 Nicht im Umfang

- integrierte Diagnostik, Lernstandsprofile oder automatische Leistungsbeurteilung;
- Namen, Konten, Kennnummern, Freitextantworten, Lernprodukte, Bildschirmaufnahmen oder Telemetrie;
- allgemeine Pilotplattform oder Wiederverwendung des IUM11-Cockpits;
- Authentifizierung oder Zugriffsschutz für GitHub Pages;
- automatische Erhebung aus dem Lernmodul;
- dauerhafter Produktbetrieb, öffentlicher Katalogeintrag oder Suchmaschinenindexierung;
- Statusänderung an `module.yaml` oder `docs/platform/device-verification.md`;
- Durchführung des realen Piloten;
- Nachweis kausaler Lernwirksamkeit, Repräsentativität oder curriculare Vollabdeckung anderer Module;
- Niveaudifferenzierung oder zusätzliche analoge Lernendenmaterialien.

## 4. Leitprinzipien

### 4.1 Digitaler Primärmodus

Der vollständige Lernweg bleibt digital. Das Gate-B-Paket erzeugt keine parallele Druckfassung des Moduls. Der einzige analoge Bestandteil ist der Beobachtungsbogen: Er hält die beobachtende Person von einer zweiten digitalen Bedienaufgabe frei, unterstützt den Blick auf Unterrichtsprozesse und bleibt unabhängig von Netz- oder Appstörungen. Nach der strukturierten Übertragung wird er vernichtet.

### 4.2 Lehrkraftorchestrierung

Die Erprobung ist kein selbstgesteuerter Onlinekurs. Die Lehrkraft eröffnet, rhythmisiert und sichert die Lernphasen, entscheidet über Hilfen und analoge Fallbacks und verantwortet den Abbruch bei technischen, pädagogischen oder datenschutzbezogenen Problemen.

### 4.3 Prozessqualität statt Punktwert

Beobachtet wird auf Klassenebene, ob der fachliche Zyklus sichtbar zustande kommt:

`Vorhersagen → ausführen → Laufspur deuten → erste Abweichung lokalisieren → Reparaturhypothese formulieren → minimal revidieren → erneut prüfen → Schleifenentscheidung begründen`

Es gibt keine Punkte, Noten, Kompetenzstufen, Rangfolgen oder individuellen Urteile.

### 4.4 Datenminimierung und Zweckbindung

Das Modul selbst erzeugt für den Piloten keine zusätzlichen Daten. Das Gate-B-Paket akzeptiert ausschließlich die in Abschnitt 10 definierten Klassenaggregate und technischen Kategorien. Reale Rohnotizen bleiben außerhalb des Repositorys, werden nur für die Gate-B-Entscheidung genutzt und anschließend fristgerecht gelöscht.

### 4.5 Fail closed

Fehlende, widersprüchliche oder nicht interpretierbare Pflichtnachweise führen zu `not-evaluable`, nicht zu einer positiven Annahme. Datenschutzverletzungen oder ungelöste kritische technische Befunde führen zu `revise-required`. Kein Teilresultat hebt `device-verified` oder den Modulstatus automatisch an.

## 5. Publikationsarchitektur der Prüffassung

### 5.1 Eigenständiger Veröffentlichungsmodus

Der bestehende Registry-Vertrag bleibt unverändert:

```ts
type BuildProfile = 'production' | 'fixture';
```

Zusätzlich wird ein orthogonaler Veröffentlichungsmodus eingeführt:

```ts
type PublicationMode = 'development' | 'device-fixture' | 'gate-b-preview';
```

Zulässige Kombinationen:

| Buildprofil | Veröffentlichungsmodus | Zulässig | Zweck |
|---|---|---:|---|
| `production` | `development` | ja | lokale Entwicklung und CI |
| `production` | `gate-b-preview` | ja | zeitlich begrenzte IUM5-Prüffassung |
| `fixture` | `device-fixture` | ja | bestehende synthetische Phase-1-Geräteprüfung |
| `production` | `device-fixture` | nein | verhindert Fachmodul im Fixture-Vertrag |
| `fixture` | `development` | nein | verhindert mehrdeutige Fixture-Builds |
| `fixture` | `gate-b-preview` | nein | verhindert synthetische Daten im Fachpilot |

Unbekannte oder unzulässige Kombinationen brechen den Build ab.

### 5.2 Sichtbare und maschinenlesbare Kennzeichnung

Jede HTML-Seite der Gate-B-Prüffassung enthält:

- ein dauerhaft sichtbares Banner: `Gate-B-Prüffassung – keine Unterrichts- oder Produktfreigabe`;
- `meta name="robots" content="noindex,nofollow,noarchive"`;
- Buildprofil `production`;
- Veröffentlichungsmodus `gate-b-preview`;
- den vollständigen Git-Commit-SHA des gebauten Stands;
- eine nichtpersonenbezogene Preview-Kennung;
- den Modulstatus `working` und den Gerätestatus `not-run`.

Eine zusätzlich ausgelieferte `robots.txt` sperrt alle Crawler. `noindex` ist eine Indexierungsbitte, kein Zugriffsschutz. Die URL gilt als öffentlich und potenziell weitergebbar. Deshalb enthält die Prüffassung weder Geheimnisse noch reale Pilotdaten.

### 5.3 Technischer Datenschutz

Die Prüffassung verwendet:

- keine Analytics, Pixel, Telemetrie oder Fehlertrackingdienste;
- keine externen Laufzeitressourcen oder Drittanbieterrequests;
- keine Accounts, Cookies oder Serverdatenbank;
- nur die bereits freigegebene Local-First-Speicherung des Lernprodukts;
- keine zusätzlichen `localStorage`-, `IndexedDB`- oder Cachefelder für Gate-B-Beobachtung;
- keine Buildsecrets außer den von GitHub Pages technisch bereitgestellten Deploymentrechten.

### 5.4 Manuelle Veröffentlichung und Rückbau

Der Workflow `.github/workflows/ium5-gate-b-preview.yml` darf ausschließlich über `workflow_dispatch` auf `main` starten. Er verlangt eine explizite Bestätigung, dass es sich nicht um einen Release handelt. Er baut exakt `github.sha`, führt `npm run verify:ium5` und das Gate-B-Preview-Gate aus und deployed nur bei vollständig grünem Ergebnis.

Der bestehende Workflow `.github/workflows/device-fixture-pages.yml` bleibt in Inhalt und Semantik unverändert. Er ist zugleich der technische Rückbaupfad: Nach Ende des Prüffensters wird die synthetische Fixture erneut veröffentlicht. Der reale Start und der Rückbau werden jeweils durch eine verantwortliche Person ausgelöst und im privaten Durchführungsprotokoll dokumentiert.

## 6. Gate-B-Phasen

### Phase B0: Paket implementieren und intern prüfen

Erlaubt sind Code, Schemata, synthetische Beispiele, lokale Builds, automatisierte Tests und interne Reviews. Reale Zielgeräte können technisch geprüft werden, sofern dafür eine eigene ausdrückliche Durchführungserlaubnis vorliegt. Unterrichtserprobung ist nicht erlaubt.

Ergebnis: implementiertes, reviewtes Gate-B-Paket; Status weiterhin `working`, `device-verified: not-run`.

### Phase B1: Technische Eintrittsprüfung

Die exakte Prüffassung wird auf den Zielkonfigurationen vollständig durchlaufen. Jede Matrixzeile bezieht sich auf denselben Commit-SHA und dieselbe Preview-Kennung.

Pflichtmatrix:

| ID | Zielkonfiguration | Kernprüfung |
|---|---|---|
| `TECH-IPAD-TOUCH` | verwaltetes iPad, Safari, Touch | vollständiger regulärer Lernpfad, Local First, Export/Import/Löschen |
| `TECH-IPAD-VO` | dasselbe Zielprofil, VoiceOver | Überschriften, Landmarken, Fokus, Status, Textszene, Laufspur, Fehlermeldungen |
| `TECH-DESKTOP-CHROMIUM` | verwalteter Desktop, Chromium, Tastatur | vollständiger Kernpfad, Reflow/Zoom, Dateidialoge |
| `TECH-DESKTOP-FIREFOX` | verwalteter Desktop, Firefox, Tastatur | vollständiger Kernpfad, Reflow/Zoom, Dateidialoge |
| `TECH-NET-OFFLINE-UPDATE` | Schulnetz und installierte Prüffassung | Erstaufruf, Offlinewiederaufruf, kontrolliertes Update, fehlerhaftes Update |
| `TECH-LMS-ROUTE` | reales schulisches LMS | Link oder iframe; bei Blockade verständlicher Weg `in eigenem Tab öffnen` |

Für jede Zeile werden nur folgende Kontextdaten gespeichert:

- Zieltyp und verwalteter Status;
- Betriebssystemfamilie und Version;
- Browserfamilie und Version;
- MDM-/Policy-Status als `documented`, `unavailable` oder `limited-accepted`;
- Netzkontext als geschlossene Kategorie;
- Ergebnis `pass`, `fail` oder `blocked`;
- Fehlercode, Schweregrad und reproduzierbare, bereinigte Schritte;
- Verweis auf einen privaten Evidenzpfad ohne Geheimnisse oder Personenbezug.

Seriennummern, MAC-/IP-Adressen, eindeutige Gerätenamen, Nutzerkonten, Policyinhalte mit Geheimnissen und Netzwerkkennungen sind verboten.

### Phase B1a: Begrenzte Ausnahmeentscheidung

Ist eine Pflichtkonfiguration nachweislich nicht verfügbar, kann der Auftraggeber eine enge Ausnahme für genau einen explorativen Pilotlauf entscheiden. Der Datensatz muss benennen:

- fehlende Matrixzeile und Grund der Nichtverfügbarkeit;
- akzeptierende Rolle;
- konkrete Zielgruppe, Laufart und Gültigkeitszeitraum;
- kompensierende Maßnahmen und Abbruchkriterien;
- ausdrücklich ausgeschlossene Behauptungen.

Eine Ausnahme setzt die fehlende Zeile nicht auf `pass`, ändert `device-verified: not-run` nicht und erlaubt weder LMS- noch Produktrelease. Ohne ausdrückliche Ausnahme bleibt der Pilot-Eintritt geschlossen.

### Phase B2: Explorative Unterrichtserprobung

Der erste Lauf verwendet den regulären 225-Minuten-Pfad in genau einer Klasse. Ziel ist das frühe Erkennen von Zeit-, Orchestrierungs-, Verständlichkeits-, Accessibility- und Technikproblemen. Der Lauf ist nicht dazu bestimmt, eine positive Releaseentscheidung zu tragen.

Ein Abbruch erfolgt bei:

- Datenschutzverletzung oder verbotener Datenerhebung;
- nicht kontrollierbarem Datenverlust;
- kritischem Accessibilityproblem im Kernpfad;
- technischem Ausfall ohne tragfähigen Fallback;
- pädagogisch nicht vertretbarer Überforderung oder Unterrichtsstörung;
- falschem Build, fehlender Prüffassungskennzeichnung oder abweichendem SHA.

Nach B2 werden Befunde korrigiert, intern regressionstestet und der technische Eintritt für betroffene Matrixzeilen erneut geprüft.

### Phase B3: Bestätigungslauf

Der zweite Lauf verwendet den erweiterten 270-Minuten-Pfad in einer anderen Klasse. Die Beziehung der Kontexte wird ausschließlich als `different-class-same-teacher` oder `different-class-different-teacher` dokumentiert. Namen, Schule, Klasse oder exakte Kalenderdaten werden nicht gespeichert.

Der Lauf prüft, ob die in B2 behobenen Probleme nicht wiederkehren und ob der vollständige Lernzyklus einschließlich Transfer- und Erweiterungsphase unter realen Bedingungen umsetzbar ist. Er ist weiterhin kein Wirksamkeitsnachweis.

### Phase B4: Review und Empfehlung

Nach B1 bis B3 prüfen getrennte Rollen:

1. Pilotlehrkraft: Durchführbarkeit und Orchestrierung;
2. fachlich-didaktisches Review: fachlicher Lernzyklus, Aufgaben- und Feedbackqualität;
3. Engineering-/Accessibility-/Privacy-Review: Technik, Barrierefreiheit, Datenvertrag, Löschung;
4. Koordination: Vollständigkeit, Buildidentität und Widerspruchsfreiheit;
5. Auftraggeber: Pilot-, LMS- und Releaseentscheidungen.

Die stärkste maschinenlesbare Empfehlung lautet `eligible-for-working-release-review`. Sie ist keine Freigabe und ändert keinen Status.

## 7. Fachlich-didaktischer Pilotvertrag

### 7.1 Verbindlicher Lernweg

Beide Läufe müssen die in Modul und Handbuch festgelegten Phasen in der vorgesehenen Reihenfolge abbilden. B2 deckt die fünf regulären Unterrichtseinheiten ab; B3 ergänzt die sechste Erweiterungseinheit. Verkürzte Demo-, Freiarbeits- oder reine Techniknutzung zählt nicht als Pilotlauf.

### 7.2 Klassenbezogene Beobachtungskriterien

Für jede Pflichtphase wird genau eine Kategorie erfasst:

- `met`: der überwiegende Teil der Lerngruppe konnte die geforderte Handlung im vorgesehenen Arrangement sichtbar vollziehen;
- `partly`: die Handlung war erkennbar, benötigte aber substanzielle Zusatzsteuerung oder blieb bei einem erheblichen Teil lückenhaft;
- `not-met`: die Handlung kam trotz vorgesehener Unterstützung nicht tragfähig zustande;
- `not-observable`: die Durchführung erlaubte keine belastbare Beobachtung.

Pflichtkriterien:

1. Vorhersagen werden vor der Ausführung fachlich genutzt.
2. Laufspuren werden zur Erklärung von Zustandsänderungen herangezogen.
3. Die erste Abweichung wird lokalisiert statt nur das Endergebnis zu beurteilen.
4. Reparaturen folgen einer benannten Hypothese.
5. Revisionen sind minimal und werden erneut ausgeführt.
6. Eine feste Wiederholung wird begründet eingesetzt oder begründet verworfen.
7. Algorithmische und nichtalgorithmische Systeme werden im Transfer unterschieden.
8. Hilfen unterstützen die Lernhandlung, ohne sie zu ersetzen.
9. Gemeinsame Sicherung macht zentrale Begriffe und Strategien explizit.

Diese Kategorien sind keine Beurteilung einzelner Schülerinnen oder Schüler.

### 7.3 Zeit- und Unterrichtsqualität

Pro Unterrichtseinheit werden nur geplantes Zeitfenster, tatsächliches grobes Zeitband und Abweichungsgrund als Code erfasst. Minutengenaue Lernendenzeiten oder Klickzeiten sind verboten.

Die Lernumgebung gilt nur dann als zeitlich tragfähig, wenn alle Pflichtphasen stattfinden konnten, die Sicherung nicht regelmäßig entfiel und keine Phase durch technische Wartezeit substanziell verdrängt wurde.

### 7.4 Lernendenimpuls

Der Lernendenimpuls ist optional, ergänzend und exakt dreiteilig:

1. `Ich wusste, was ich als Nächstes tun sollte.`
2. `Vorhersage und Laufspur haben mich zum Nachdenken über den Ablauf gebracht.`
3. `Die Hilfen haben mir weitergeholfen, ohne mir die Lösung abzunehmen.`

Antwortkategorien: `agree`, `partly`, `disagree`, `no-answer`.

Es werden nur Klassensummen übertragen. Bei weniger als zehn gültigen Antworten pro Frage wird die gesamte Frage als `suppressed` gespeichert; Einzelwerte oder kleine Summen dürfen nicht exportiert werden. Der Impuls kann eine negative Entscheidung stützen, aber niemals allein eine positive Gate-B-Empfehlung erzeugen.

## 8. Analoger Beobachtungsbogen

Der druckbare Bogen umfasst genau:

- Preview-Kennung und Commit-SHA;
- Laufart `exploratory` oder `confirmation`;
- grobe Kontextkategorien;
- neun Pflichtkriterien mit `met`, `partly`, `not-met`, `not-observable`;
- sechs Unterrichtsphasen mit grobem Zeitband und Abweichungscode;
- technische Störungscodes und Unterstützungsbedarf als Kategorien;
- Abbruchentscheidung und Grundcode;
- Erinnerung an verbotene Daten und Vernichtung nach Übertragung.

Er enthält keine Felder für Namen, Sitzplan, exakte Klasse, Schule, Datum, Freitext über Lernende, Leistungsurteile, Lernprodukte, Gerätekennungen oder offene Beobachtungsprosa. Kurze technische Reproduktionsschritte werden getrennt und bereinigt im privaten technischen Befund erfasst, nicht auf dem Unterrichtsbogen.

## 9. Evidenzklassen

### 9.1 Technische Evidenz

Belegt Buildidentität, Zielkonfiguration, Kernpfad, Accessibility, Schulnetz, Offline/Update und LMS-Routing. Ergebnis pro Matrixzeile: `pass`, `fail`, `blocked`.

### 9.2 Durchführungs- und Zeitevidenz

Belegt, welche Phasen tatsächlich stattfanden, ob der reguläre beziehungsweise erweiterte Zeitvertrag tragfähig war und welche Fallbacks benötigt wurden.

### 9.3 Fachlich-didaktische Prozessevidenz

Belegt auf Klassenebene den Zyklus aus Vorhersage, Laufspur, Fehlerlokalisierung, Hypothese, Revision und Begründung. Sie belegt keine individuellen Kompetenzen und keine kausale Wirkung.

### 9.4 Optionaler Lernendenimpuls

Belegt nur die aggregierte Wahrnehmung von Klarheit, kognitiver Aktivierung und Hilfenutzen unter der Unterdrückungsregel.

### 9.5 Privacy- und Verfahrensevidenz

Belegt Datenminimierung, Aufbewahrung, Löschung, Rollenreviews, Buildidentität, Abbruch- und Ausnahmeentscheidungen.

Die Klassen bleiben getrennt. Eine fehlende Evidenzklasse darf nicht durch eine andere ersetzt werden.

## 10. Geschlossener Datenvertrag

### 10.1 Erlaubte Kontextfelder

- `moduleId`: immer `IUM-5-CORE-05`;
- `moduleVersion`: immer die geprüfte Modulversion;
- `buildRevision`: vollständiger Git-SHA;
- `previewId`: nichtpersonenbezogene Kennung;
- `runKind`: `technical`, `exploratory` oder `confirmation`;
- `pathKind`: `regular-225` oder `extended-270`;
- `gradeBand`: immer `grade-5`;
- `groupSizeBand`: `10-19`, `20-29`, `30-plus` oder `not-recorded`;
- `contextRelation`: nur beim Bestätigungslauf;
- `seasonWindow`: `school-year-start`, `autumn`, `winter`, `spring`, `summer` oder `not-recorded`;
- geschlossene Ergebnis-, Zeit-, Störungs-, Unterstützungs- und Reviewkategorien.

### 10.2 Verbotene Felder und Inhalte

- Namen, Initialen, Konten, E-Mail-Adressen und Rollenbezeichnungen mit Identifikationswirkung;
- Schule, Ort, Klassencode, Kursname oder exaktes Datum;
- Freitext von oder über Lernende;
- Lernprodukte, Algorithmen, Exporte, Bilder, Video, Audio oder Bildschirmaufnahmen;
- Einzelantworten, Einzelzeiten, Einzelbeobachtungen oder Sitzpositionen;
- IP-, MAC-, Serien-, Inventar-, MDM-, Benutzer- oder Netzwerkkennungen;
- Klick-, Fokus-, Navigations-, Hilfe-, Versuchszahl- oder Performance-Telemetrie;
- Punkte, Noten, Kompetenzstufen oder individuelle Profile;
- Geheimnisse, Tokens, interne URLs oder Policyinhalte.

Der Validator weist unbekannte Felder rekursiv zurück.

### 10.3 Speicherorte und Löschung

Schemata, Validator, Leitfäden, Druckvorlage und rein synthetische Beispiele sind öffentlich im Repository. Reale technische und Pilotpakete bleiben in einem freigegebenen, nichtöffentlichen Speicher außerhalb des Repositorys. Sie dürfen weder committed noch als GitHub-Artefakt hochgeladen werden.

Analoge Bögen werden nach geprüfter Aggregation vernichtet. Digitale Realpakete werden spätestens 30 Tage nach der abschließenden Gate-B-Entscheidung gelöscht, sofern keine kürzere lokale Vorgabe gilt. Im öffentlichen Repository darf nur ein nach Privacy-Review ausdrücklich freigegebenes, vollständig aggregiertes Entscheidungsfaktum ohne Kontextidentifikatoren erscheinen.

## 11. Ergebnislogik

### 11.1 Technisches Eintrittsurteil

`technical-entry = pass` nur wenn:

- alle sechs Matrixzeilen `pass` sind;
- Build-SHA und Preview-Kennung in allen Nachweisen übereinstimmen;
- keine kritischen oder hohen ungelösten Befunde bestehen;
- Datenschutz- und Drittanbieterrequestprüfung bestanden sind.

`technical-entry = limited-accepted` nur bei einer ausdrücklich dokumentierten Ausnahme nach 6/B1a. `device-verified` bleibt dabei `not-run` beziehungsweise unverändert.

`technical-entry = fail` bei Fehler oder Privacyverletzung. `technical-entry = not-evaluable` bei fehlender, blockierter oder widersprüchlicher Evidenz ohne gültige Ausnahme.

### 11.2 Laufurteil

Ein einzelner Lauf ist `pass`, wenn:

- alle vorgesehenen Unterrichtsphasen stattgefunden haben;
- die Kriterien 1 bis 6 jeweils `met` oder höchstens einmal `partly` sind;
- kein Pflichtkriterium `not-met` oder `not-observable` ist;
- kein ungelöster kritischer Technik-, Accessibility- oder Privacybefund besteht;
- die gemeinsame Sicherung stattgefunden hat;
- Zeit- und Fallbackvertrag tragfähig waren.

Er ist `revise-required`, sobald ein Pflichtkriterium `not-met`, eine Datenschutzverletzung oder ein ungelöster kritischer Befund vorliegt. Er ist `not-evaluable`, wenn Pflichtphasen, Buildidentität oder notwendige Aggregate fehlen beziehungsweise widersprüchlich sind.

### 11.3 Gesamtempfehlung

`eligible-for-working-release-review` darf nur entstehen, wenn:

- technische Eintrittsprüfung `pass` ist;
- explorativer Lauf nach etwaiger Nacharbeit abschließend `pass` ist;
- Bestätigungslauf in einer anderen Klasse `pass` ist;
- beide internen Reviews zustimmen;
- Privacy-, Lösch- und Evidenzprüfung abgeschlossen sind;
- keine Ausnahmeentscheidung mehr für die beanspruchte Zielkonfiguration nötig ist.

Andernfalls lautet das Ergebnis `revise-required` oder `not-evaluable`. Die Empfehlung öffnet lediglich ein menschliches Release-Review. Sie setzt weder `status` noch `device-verified` und erlaubt keinen Katalogeintrag.

## 12. Rollen und Vier-Augen-Prinzip

| Rolle | Verantwortung | Darf nicht allein |
|---|---|---|
| Engineering | Previewbuild, Validator, technische Befunde | Pilot- oder Releasefreigabe erteilen |
| Pilotlehrkraft | Unterricht durchführen, Abbruch entscheiden, Aggregate bestätigen | sich selbst fachlich und technisch freigeben |
| Beobachtung | Bogen ausfüllen, ohne Lernende zu identifizieren | offene personenbezogene Notizen führen |
| Fach-/Didaktikreview | Lernzyklus, Aufgaben, Feedback, Zeitvertrag prüfen | Technik-/Privacyurteil ersetzen |
| Accessibility-/Privacyreview | Zugänglichkeit, Datenvertrag, Löschung prüfen | fachliche Prozessqualität ersetzen |
| Koordination | Evidenzpaket auf Vollständigkeit und Buildidentität prüfen | fehlende Nachweise positiv annehmen |
| Auftraggeber | Ausnahme, Pilot-Eintritt, LMS und Release getrennt entscheiden | Softwareurteil als automatische Freigabe behandeln |

Pilotlehrkraft und Beobachtung dürfen dieselbe Person sein, wenn keine zweite Person verfügbar ist. Die abschließende fachlich-didaktische und technisch-datenschutzbezogene Prüfung muss dennoch durch andere Reviewrollen erfolgen.

## 13. Fehler-, Abbruch- und Nacharbeitsvertrag

Störungen werden mit geschlossenen Codes erfasst:

- `wrong-build`
- `preview-label-missing`
- `startup-failure`
- `interaction-loss`
- `state-loss`
- `import-export-failure`
- `offline-failure`
- `update-failure`
- `screenreader-blocker`
- `keyboard-blocker`
- `touch-blocker`
- `layout-blocker`
- `network-policy-blocker`
- `lms-routing-blocker`
- `unexpected-third-party-request`
- `privacy-contract-breach`
- `instructional-time-collapse`
- `other-closed-review-required`

`other-closed-review-required` darf nur die Existenz eines nicht abgebildeten Problems markieren; sein Inhalt wird außerhalb des exportierten Pakets bereinigt analysiert und vor einer positiven Entscheidung als neuer geschlossener Code in Protokoll und Schema aufgenommen.

Nach jeder Produktänderung, die fachliches Verhalten, Persistenz, Offline, Accessibility, Routing oder Buildkennzeichnung berührt, sind alle betroffenen technischen Matrixzeilen erneut auszuführen. Ein neuer Commit-SHA invalidiert die Pilot-Eintrittsevidenz des alten Builds.

## 14. Implementierungsartefakte

Das spätere Implementierungspaket umfasst mindestens:

```text
pilot/ium5-gate-b/protocol.json
pilot/ium5-gate-b/schemas/technical-evidence.schema.json
pilot/ium5-gate-b/schemas/pilot-evidence.schema.json
pilot/ium5-gate-b/schemas/decision-package.schema.json
pilot/ium5-gate-b/examples/technical-pass.synthetic.json
pilot/ium5-gate-b/examples/pilot-pass.synthetic.json
pilot/ium5-gate-b/examples/decision-pass.synthetic.json
pilot/ium5-gate-b/examples/decision-revise.synthetic.json
pilot/ium5-gate-b/examples/decision-not-evaluable.synthetic.json
pilot/ium5-gate-b/docs/technical-runbook.md
pilot/ium5-gate-b/docs/pilot-guide.md
pilot/ium5-gate-b/docs/review-guide.md
pilot/ium5-gate-b/print/observation-sheet.html
scripts/validate_ium5_gate_b.py
scripts/verify-ium5-gate-b.ts
.github/workflows/ium5-gate-b-preview.yml
```

Es gibt keine produktive Erfassungsoberfläche. Reale Pakete werden aus kopierten, lokal gespeicherten JSON-Vorlagen erstellt und durch den Validator geprüft. Diese bewusste Einfachheit verhindert eine zweite Plattform und hält alle Verarbeitungsschritte sichtbar.

## 15. Automatische Qualitätsgates

Die Implementierung muss mindestens automatisch belegen:

- rekursive Ablehnung unbekannter oder verbotener Felder;
- korrekte Unterdrückung des Lernendenimpulses unter zehn gültigen Antworten;
- fail-closed Ergebnislogik für `pass`, `revise-required` und `not-evaluable`;
- zwei unterschiedliche Klassenkontexte für eine positive Gesamtempfehlung;
- vollständige technische Matrix und identische Buildrevision;
- unveränderten Status `working` und unverändertes `device-verified: not-run`;
- erlaubte Kombinationen aus Buildprofil und Veröffentlichungsmodus;
- Prüffassungsbanner, `noindex,nofollow,noarchive`, `robots.txt` und Build-SHA auf jeder Route;
- keine externen Laufzeitrequests, Analytics oder Gate-B-Speicherung im Modul;
- manuellen, `main`-gebundenen, fail-closed Pages-Workflow;
- unveränderten bestehenden Fixture-Workflow;
- druckbaren Beobachtungsbogen ohne verbotene Felder;
- vollständigen bisherigen IUM5-Regressionslauf.

## 16. Akzeptanzkriterien der Spezifikation

Die Spezifikation ist schriftlich freigabefähig, wenn:

- die Grenze zwischen Paketimplementierung, technischer Prüfung, Pilot, LMS und Release eindeutig ist;
- IUM14 und `device-verified: not-run` unverändert bleiben;
- der Previewmodus öffentlichkeits- und datenschutzrealistisch beschrieben ist;
- der vollständige reguläre und erweiterte Lernweg abgedeckt ist;
- keine integrierte Diagnostik oder zweite Pilotplattform entsteht;
- Datenfelder, Verbote, Unterdrückung, Löschung und Rollen vollständig bestimmt sind;
- positive, negative und nicht auswertbare Ergebniswege geschlossen sind;
- der analoge Beobachtungsbogen fachlich und medial begründet ist;
- automatische und reale Nachweise sauber getrennt sind;
- keine Platzhalter oder offenen Designentscheidungen verbleiben.

## 17. Nichtfreigaben nach schriftlicher Annahme

Auch eine schriftliche Freigabe dieser Spezifikation erlaubt ausschließlich die Erstellung und Ausführung des Implementierungsplans. Weiterhin nicht freigegeben sind:

- Veröffentlichung der realen Prüffassung;
- reale technische Prüfung, sofern sie nicht separat beauftragt wird;
- Unterrichtspilot oder Erhebung realer Aggregate;
- LMS-Verlinkung oder -Einbettung;
- Veröffentlichung realer Evidenz;
- Änderung von `working` oder `device-verified`;
- Release oder Produktkatalogeintrag.

## 18. Abdeckung des freigegebenen Designs

| Freigegebener Designpunkt | Normative Stelle |
|---|---|
| schlankes modulspezifisches Paket statt IUM11-Cockpit | 2, 3.2, 14 |
| manuelle zeitlich begrenzte HTTPS-Prüffassung | 5.4 |
| sichtbare Nichtfreigabe und `noindex` | 5.2 |
| keine Analytics, Drittanbieter oder Zusatzspeicherung | 5.3 |
| iPad, VoiceOver, Desktop, Schulnetz, Offline, Update, LMS | 6/B1 |
| explorativer und anschließender Bestätigungslauf | 6/B2–B3 |
| keine Diagnostik oder Personendaten | 4.4, 10 |
| analoger Beobachtungsbogen nur aus Medienfunktion | 4.1, 8 |
| technische Störungen, Zeitfenster, Hilfe, Klassenaggregate | 7–10 |
| `pass`, `revise-required`, `not-evaluable` | 11 |
| keine automatische Statushochsetzung | 1, 11.3 |
| IUM14-Evidenz und IUM11-Prinzipien, keine zweite Plattform | 2, 6/B1a |

Diese Tabelle ist zugleich die Freigabecheckliste. Alle Designpunkte sind normativ aufgelöst.
