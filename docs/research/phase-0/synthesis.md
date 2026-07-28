# Forschungssynthese Phase 0

**Status:** `working`
**Geltungsbereich:** IuM-Lernwerk, Gymnasium Baden-Württemberg, Klassen 5–7, Niveau E
**Evidenzstichtag:** 28. Juli 2026

## 1. Zweck, Scope und Evidenzbasis

Diese Synthese übersetzt die vier kuratierten Forschungspakete in prüfbare Regeln für das IuM-Lernwerk. Sie ist kein fünfter Rohbericht und ersetzt weder das Claim-Ledger noch das Curriculum-Mapping. Ihre Evidenzanker sind ausschließlich die 51 dort registrierten und als `reviewed` geprüften Claims:

- 11 Claims zur Informatikdidaktik;
- 13 Claims zur Medienbildung;
- 13 Claims zu Lernpsychologie und Unterrichtswissenschaft;
- 14 Claims zu digitalen Lernumgebungen und OER.

Die Synthese unterscheidet vier Aussagearten:

1. **empirische Befunde** mit Population, Kontext und Limitation;
2. **normative oder professionelle Standards** ohne behauptete Lernwirkung;
3. **inferentielle Projektfolgen**, die in IuM 5–7 zu erproben sind;
4. **bereits freigegebene Projektentscheidungen**, die durch Forschung geprüft und konkretisiert, aber nicht nachträglich als Forschungsbefund ausgegeben werden.

Zu den freigegebenen Projektentscheidungen gehören das digitale Primärmedium, lehrkraftorchestrierter Unterricht, der Verzicht auf integrierte personenbezogene Diagnostik, die offene Veröffentlichung, der progressive Kernlernweg und die flexible Ergänzungsarchitektur. Der dafür maßgebliche Satz bleibt unverändert:

> Vertiefungs-, Transfer- und Projektmodule können an definierte Voraussetzungen andocken und flexibel eingesetzt werden.

Diese Phase spezifiziert Forschungs- und Curriculumgrundlagen. Sie implementiert weder Portal noch PWA, lokale Speicherung oder ein Pilotmodul.

## 2. Evidenz- und Konfidenzmodell

### 2.1 Leseregel

`reviewed` im Claim-Ledger bedeutet, dass Aussage, Quelle und Limitationen gegen mindestens eine primär geprüfte Quelle kontrolliert wurden. Es bedeutet nicht, dass jede Übertragung auf 10- bis 13-Jährige, auf Informatik und Medienbildung oder auf eine digitale Lernumgebung bereits experimentell abgesichert ist.

| Aussageart | Zulässige Funktion in dieser Synthese | Unzulässige Überdehnung |
| --- | --- | --- |
| Empirischer Befund | begründet eine vorsichtige Designhypothese innerhalb des untersuchten Scopes | universelle Methodenregel, Altersgrenze oder Kausalbehauptung außerhalb des Designs |
| Normativer oder professioneller Standard | setzt eine technische, rechtliche oder professionelle Baseline | empirischer Nachweis für Lernen oder schulische Nutzbarkeit |
| Projektinferenz | übersetzt mehrere Claims in eine prüfbare Regel für IuM 5–7 | als bereits bewährter Standard ausgeben |
| Freigegebene Projektentscheidung | begrenzt Produktarchitektur und Umsetzung | nachträglich als aus Forschung zwingend ableiten |

### 2.2 Konfidenzentscheidungen

- Breite Meta-Analysen zu Abruf, verteiltem Üben, Transfer und Feedback stützen die jeweiligen Lernmechanismen, ihre konkrete IuM-Ausprägung bleibt wegen heterogener Fächer, Altersstufen und Aufgaben eine Projektinferenz. [CLAIM-LP-007; CLAIM-LP-008; CLAIM-LP-009; CLAIM-LP-010]
- Fachnahe Befunde zu PRIMM, Internetvorstellungen und Unplugged-Aktivitäten liegen näher an der Zielgruppe, erlauben aber weder eine feste Unterrichtsfolge noch pauschale Transfer- oder Wirksamkeitsurteile. [CLAIM-INF-002; CLAIM-INF-009; CLAIM-INF-010]
- Worked Examples, notional machines und getrennte Programmierpraktiken sind fachlich tragfähig, stammen jedoch teilweise stark aus Hochschulkontexten; ihre konkrete Form und Dosierung in IuM 5–7 müssen pilotiert werden. [CLAIM-INF-003; CLAIM-INF-004; CLAIM-INF-005; CLAIM-LP-004]
- Die Evidenz zu Desinformation und GenAI ist für 10- bis 13-Jährige begrenzt und schnell veränderlich; sie trägt einen wiederholten Prüfprozess, aber keine altersgesicherte Standardsequenz und kein Detektor-Endurteil. [CLAIM-MED-003; CLAIM-MED-004]
- Beobachtete Zusammenhänge zu Medienwirkungen und Lootboxen begründen Analyseaufgaben, aber keine individuelle Ursache, Gefährdungsdiagnose oder monokausale Warnbotschaft. [CLAIM-MED-008; CLAIM-MED-010]
- WCAG, Datenschutz-, Storage-, PWA- und Lizenzquellen liefern technische oder normative Anforderungen; sie sind keine Belege für Lernwirksamkeit. [CLAIM-DLE-001; CLAIM-DLE-004; CLAIM-DLE-005; CLAIM-DLE-006; CLAIM-DLE-007; CLAIM-DLE-009; CLAIM-DLE-010; CLAIM-DLE-011]

Deskriptive Jugendmedienstudien werden nur für passende Prävalenzfragen verwendet und nicht zu Wirkungsnachweisen umgedeutet. Kleine, heterogene, korrelative oder nicht kausale Befunde werden nicht verallgemeinert. Rechtsbezogene Regeln bleiben datiert und unter Zuständigkeits- sowie Recheck-Vorbehalt.

## 3. Paketübergreifend konvergierende Prinzipien

### 3.1 Lernprozessqualität statt Medien- oder Gerätewirkung

Unterrichtsqualität wird über kognitive Aktivierung, konstruktive Unterstützung, klare Führung und fachliche Lernhandlungen beschrieben, nicht über Methode oder Medium allein. [CLAIM-LP-001] Der systematische Review zu Mobilgeräten erlaubt weder einen kausalen Lernvorteil noch einen pauschalen Nulleffekt; Geräteverfügbarkeit ist damit kein eigenständiges Qualitätskriterium. [CLAIM-DLE-014]

**Projektfolge:** Jede Aktivität nennt Ziel, fachliche Denkhandlung, Unterstützung, Rückmeldung und Sicherung. Interaktivität ohne Entscheidung, Prüfung, Erklärung oder Revision besteht das didaktische Gate nicht. Diese Regel ist als `PRIN-001` operationalisiert.

### 3.2 Vorwissen und Fehlvorstellungen ohne Defizitdeterminismus

Vorwissen sagt spätere Wissensstände voraus, legt den Wissenszuwachs aber nicht fest; eine einzelne falsche Antwort belegt kein stabiles Fehlkonzept. [CLAIM-LP-002] Fachliche Schwierigkeiten beim Programmieren und fragmentarische Internetmodelle sind geeignete Ausgangspunkte für Vorhersage-, Modellvergleichs- und Reparaturaufgaben, nicht für dauerhafte Etiketten. [CLAIM-INF-006; CLAIM-INF-010] Zielgruppennahe Algorithmusvorstellungen zeigen zudem nutzbare vorhandene Erklärungsansätze, ohne Kompetenzverteilungen oder Unterrichtswirkung zu belegen. [CLAIM-MED-005]

**Projektfolge:** Vorwissen wird lokal und aufgabenbezogen sichtbar gemacht. Antworten steuern den aktuellen Lernschritt oder das Unterrichtsgespräch, nicht ein personenbezogenes Profil. Diese Regel ist als `PRIN-002` operationalisiert.

### 3.3 Vorbereitete Exploration und explizite Instruktion

Problem Solving before Instruction kann unter den Bedingungen von Productive Failure günstig sein; der Befund gilt nicht für offenes Entdecken, und bei jüngeren Lernenden kann frühe Instruktion günstiger sein. [CLAIM-LP-012] PRIMM zeigt zugleich einen schulnahen Zyklus aus Vorhersage, Ausführung, Untersuchung, Modifikation und Eigenkonstruktion, ohne jede Phase isoliert als Ursache auszuweisen. [CLAIM-INF-002]

**Projektfolge:** Exploration verwendet Kontrastfälle, kontrollierte Simulationen oder begrenzte Lösungsräume und endet in expliziter Erklärung und gemeinsamer Sicherung. Klasse 5 erhält ein eigenes Überforderungsgate. Diese Regel ist als `PRIN-003` operationalisiert.

### 3.4 Aktive Worked Examples, Selbsterklärung, Scaffolding und Fading

Worked Examples sind besonders dann anschlussfähig, wenn Lernende vorhersagen, erklären, ergänzen, vergleichen oder korrigieren; passives Betrachten ist keine abgeleitete Regel. [CLAIM-INF-004; CLAIM-LP-004] Ein notional-machine-Modell kann Code, Ausführung und Zustand verbinden, wenn Lernende die Darstellung aktiv bearbeiten. [CLAIM-INF-005] Selbsterklärung ist aufgaben- und promptabhängig und rechtfertigt keine Folge generischer Warum-Fragen. [CLAIM-LP-005] Computerbasiertes Scaffolding kann Lernen unterstützen, belegt aber keine universell überlegene Anpassungs- oder Fadinglogik. [CLAIM-LP-006]

**Projektfolge:** Hilfen sind an konkrete Hürden gebunden, erhalten die zentrale Denkhandlung und werden nach sichtbarer fachlicher Bewältigung reduziert. Zeit, Klickzahl oder Telemetrie lösen kein automatisches Fading aus. Diese Regel ist als `PRIN-004` operationalisiert.

### 3.5 Abruf, verteiltes Üben, Feedback und entworfener Transfer

Aktiver Abruf kann Lernen fördern, ist aber nicht mit Wiederlesen oder Wiederanschauen gleichzusetzen. [CLAIM-LP-007] Verteilte Wiederaufnahme ist für verzögertes Behalten im Mittel günstiger als massiertes Üben, ohne eine universelle Terminierung vorzugeben. [CLAIM-LP-008] Transfer muss nach Zielbeziehung und Transferart gestaltet werden; Oberflächenvariation allein genügt nicht. [CLAIM-LP-009] Feedback ist stark heterogen und muss als nutzbare Information zu Produkt, Strategie oder nächstem Prüfschritt entworfen werden. [CLAIM-LP-010]

**Projektfolge:** Unmittelbare Anwendung, verzögerter Abruf und Transfer erhalten getrennte Aufgaben und Kriterien. Feedbackzeitpunkt und -inhalt folgen der Lernfunktion. Diese Regel ist als `PRIN-005` operationalisiert.

### 3.6 Autonomieunterstützung, Struktur und Selbstregulation

Autonomieunterstützung und Struktur sind nicht grundsätzlich gegensätzlich, doch ihre Zusammenhänge sind heterogen und überwiegend korrelativ. [CLAIM-LP-011] Explizite Selbstregulationstrainings bei jüngeren Lernenden zeigen günstige unmittelbare Outcomes in nicht randomisierten Vergleichen, belegen aber weder digitale IuM-Wirkung noch eine universelle Sequenz. [CLAIM-LP-013]

**Projektfolge:** Lernende entscheiden innerhalb klarer Ziele, Kriterien, Zeitrahmen und Hilfen. Planen, Strategie wählen, überwachen, prüfen und revidieren werden als sichtbare fachliche Handlungen aufgebaut. Diese Regel ist als `PRIN-006` operationalisiert.

### 3.7 Fachliche Programmierpraktiken und Repräsentationsübergänge

Kontrollstrukturen lassen sich als kontextabhängige Lerntrajektorien ordnen, nicht als starre Stoffliste. [CLAIM-INF-001] Tracing, Syntaxarbeit, Musterverständnis und Eigenkonstruktion sind unterscheidbare Praktiken, deren konkrete Reihenfolge für die Zielgruppe noch zu prüfen ist. [CLAIM-INF-003] Debugging umfasst Bemerken, Lokalisieren, Hypothese, gezielten Test, Reparatur und Begründung. [CLAIM-INF-007] Block- und Textdarstellungen besitzen keinen evidenzbasierten festen Alterswechsel; die Entscheidung hängt von Lernziel, Syntaxlast und Anschlussweg ab. [CLAIM-INF-008]

**Projektfolge:** Programmiermodule verbinden Predict–Run–Investigate–Modify–Make mit notional machine, Testfällen und begründetem Debugging. Block-/Textübergänge werden durch isomorphe Beispiele oder Übersetzungsaufgaben gestützt. Diese Regel ist als `PRIN-007` operationalisiert.

### 3.8 Aktive, mehrschrittige Medienanalyse

Medienbildungsinterventionen zeigen im Mittel kleine positive, aber stark kontext- und outcomeabhängige Effekte; daraus folgt eine aktive Lernhandlung, nicht die Überlegenheit eines Mediums oder einer festen Sequenz. [CLAIM-MED-002] Informationsprüfung profitiert in überwiegend erwachsenen Stichproben eher von mehrteiligen als einmaligen Interventionen, während die Übertragung auf 10- bis 13-Jährige offen bleibt. [CLAIM-MED-003] Privatsphäre, Empfehlung und eingebettete Werbung müssen Datenarten, Akteure, Interessen und Gestaltungsmechanismen sichtbar machen. [CLAIM-MED-001; CLAIM-MED-005; CLAIM-MED-006] KI-Ausgaben werden als ungesicherte Behauptungen geprüft; ein Modell- oder Detektorlabel ersetzt keine Evidenzprüfung. [CLAIM-MED-004]

**Projektfolge:** Mechanismus, Akteur, Interesse, Beleg, Gegenbeleg, Unsicherheit und Revision bilden einen wiederkehrenden Analysezyklus. Diese Regel ist als `PRIN-008` operationalisiert.

### 3.9 Sensible Themen ohne personenbezogene Diagnose oder Monokausalität

Cybermobbingprogramme zeigen im Mittel moderate Reduktionen, ohne wirksame Einzelkomponenten oder Schutz im Einzelfall zu garantieren. [CLAIM-MED-007] Zusammenhänge zwischen sozialer Mediennutzung und internalisierenden Symptomen sind in beobachtenden Studien im Mittel klein und erlauben keine kausale Individualaussage. [CLAIM-MED-008] Körperbildinterventionen zeigen kleine und teilweise nicht fortbestehende Outcomes; Exposition und Zielgruppenabdeckung begrenzen die Übertragung. [CLAIM-MED-009] Lootbox-Ausgaben korrelieren mit problematischem Glücksspiel und Gaming, doch überwiegend querschnittliche Daten erlauben keine individuelle Risikodiagnose. [CLAIM-MED-010]

**Projektfolge:** Fiktive Fälle, kuratierte Beispiele, geldfreie Modelle und mechanismusbezogene Produkte ersetzen persönliche Offenlegung, Peerdiagnostik und Risikoscores. Diese Regel ist als `PRIN-009` operationalisiert.

### 3.10 Digitale und analoge Lernfunktionen

Medium und Methode erhalten ihren Wert durch die ausgelösten Lernprozesse. [CLAIM-LP-001] Kognitive Last wird durch Aufgabe, Vorwissen, Darstellung und Umgebung gemeinsam geprägt; digitale Zustände und synchrone Repräsentationen sowie analoge räumliche Übersicht können je eigene Funktionen erfüllen. [CLAIM-LP-003] Unplugged-Aktivitäten tragen eng umrissene Ziele, rechtfertigen aber keine pauschale Transfer- oder Wirksamkeitsannahme. [CLAIM-INF-009] Bloße Mobilgerätenutzung ist kein Lernwirkungsnachweis. [CLAIM-DLE-014]

**Projektfolge:** Digital bleibt Primärmedium. Analog wird nur mit fachlicher oder lernpsychologischer Funktion, Analogiegrenze und Anschlussprodukt vorgesehen; es gibt keine parallele Vollstruktur. Diese Regel ist als `PRIN-010` operationalisiert.

### 3.11 Datenschutz, Accessibility, Offlinequalität und OER

Datenminimierung und Datenschutz durch Technikgestaltung verlangen einen dokumentierten Datenfluss; Konto- und Backendfreiheit belegen allein keine Compliance. [CLAIM-DLE-004] Endgerätespeicherung bleibt rechtlich einzelfallabhängig, und Browserstorage bietet keine universelle Verfügbarkeits- oder Persistenzgarantie. [CLAIM-DLE-005; CLAIM-DLE-006] Diese Anforderungen sind in `PRIN-011` operationalisiert.

WCAG 2.2 AA ist eine technische Baseline, keine Aussage über schulische Usability oder Lernen. [CLAIM-DLE-001] Gleichwertige Bedienpfade und die Verbindung technischer Prüfung mit echten Nutzeraufgaben sind gesondert erforderlich. [CLAIM-DLE-002; CLAIM-DLE-003] Diese Anforderungen sind in `PRIN-012` operationalisiert.

Installationsmetadaten, Offlinekorrektheit, Cache- und Updatezustände sowie schulische Browserrestriktionen sind getrennte Verträge. [CLAIM-DLE-007; CLAIM-DLE-008; CLAIM-DLE-012] Performance- und Transfergrößen sind messbar, begründen aber kein pauschales Nachhaltigkeitslabel. [CLAIM-DLE-013] Diese Anforderungen sind in `PRIN-013` operationalisiert.

OER verlangt rechtlichen und praktischen Bearbeitungs- und Weitergaberaum, nicht nur kostenlosen Zugriff. [CLAIM-DLE-009] Attribution, Änderungen und ShareAlike-Kompatibilität sind asset-, versions- und richtungsspezifisch zu dokumentieren. [CLAIM-MED-013; CLAIM-DLE-010; CLAIM-DLE-011] Diese Anforderungen sind in `PRIN-014` operationalisiert.

### 3.12 Produktbezogene und reduzierbare Lernnachweise

Aufgabenbezogene Fehler, aktuelle Produkte und sichtbare Strategien bieten Feedbackgelegenheiten, ohne ein stabiles Personenmerkmal zu diagnostizieren. [CLAIM-INF-006; CLAIM-LP-010; CLAIM-LP-013] Sensible Fälle dürfen dabei keine persönliche Offenlegung oder zentrale Fallspeicherung verlangen. [CLAIM-MED-007]

**Projektfolge:** Das Beurteilungsinstrumentarium bleibt ein `working`-Bestand aus Produkten, Erklärungen, Testfällen, Kriterien und Revisionen. Es kann später reduziert werden, ohne Kernlernziele oder Module umzubauen. Diese Regel ist als `PRIN-015` operationalisiert.

## 4. Spannungen und begründete Auflösungsregeln

| Spannung | Auflösungsregel | Evidenz- und Entscheidungsgrundlage |
| --- | --- | --- |
| Exploration ↔ explizite Führung | Begrenzte Exploration vorsehen, wenn Aufgabe und Vorwissen passen; danach Lösungswege vergleichen, Zielkonzept explizit erklären und gemeinsam sichern. Klasse 5 vorsichtig pilotieren. | Productive Failure gilt nicht für offenes Entdecken und zeigt bei Jüngeren Grenzen. [CLAIM-LP-012] |
| Autonomie ↔ Struktur | Echte Entscheidungen innerhalb klarer Ziele, Kriterien, Zeitrahmen und Hilfen anbieten; Autonomie nicht als Freiheit von Führung definieren. | Der Zusammenhang beider Konstrukte ist positiv, aber heterogen und nicht generell kausal. [CLAIM-LP-011] |
| Hilfen ↔ eigenständige Denkhandlung | Hilfe muss Hürde und erhaltene Kernhandlung benennen; Rücknahme folgt sichtbarer Bewältigung, nicht Zeit, Klickzahl oder automatischem Profil. | Keine robuste Überlegenheit einer Fadinglogik; Selbstregulation bleibt konkrete Handlung. [CLAIM-LP-006; CLAIM-LP-013] |
| digitales Primärmedium ↔ begründete Analogwahl | Digital ist Standard; analog nur bei eigener epistemischer oder lernpsychologischer Funktion mit Anschlussprodukt, nicht als Doppelstruktur. | Medienwert folgt Lernfunktion; Unplugged belegt keine pauschale Wirkung. [CLAIM-LP-001; CLAIM-INF-009; CLAIM-DLE-014] |
| lokale Speicherung ↔ fehlende Persistenzgarantie und Rechtsprüfung | Realen Speicher probeweise prüfen, flüchtigen Modus und Export anbieten und lokale Speicherung rechtlich vor Betrieb rechecken. | Browserstorage ist best-effort; TDDDG-Anwendung bleibt einzelfallabhängig. [CLAIM-DLE-005; CLAIM-DLE-006] |
| offene Nachnutzung ↔ Drittmaterial- und Lizenzgrenzen | Bearbeitbare Quellen plus assetgenaue Rechtekette ausliefern; Kompatibilität nach Version, Richtung und Werkart entscheiden. | OER-Nachnutzung und CC-Bedingungen sind normativ, aber keine Freigabe aller sonstigen Rechte. [CLAIM-MED-013; CLAIM-DLE-009; CLAIM-DLE-010; CLAIM-DLE-011] |
| WCAG-Konformität ↔ tatsächliche schulische Nutzbarkeit | Vollständiges AA-Gate mit Tastatur-, Touch- und Assistive-Technology-Pfaden durchführen und durch echte Nutzeraufgaben ergänzen; Lernoutcomes getrennt prüfen. | WCAG deckt nicht alle Bedürfnisse und keine Lernwirkung ab; Nutzerbeteiligung ergänzt die Konformitätsprüfung. [CLAIM-DLE-001; CLAIM-DLE-002; CLAIM-DLE-003] |
| PWA-Installierbarkeit ↔ reale Offlinekorrektheit | Installation, Kernressourcen, Lernstand, externe Ressourcen, Netzverlust, Wiederanbindung und Updates getrennt abnehmen. | Manifest und Service Worker sind Mechanismen, kein Offlinebeweis. [CLAIM-DLE-007; CLAIM-DLE-008] |
| vollständiges Arbeitsinstrumentarium ↔ spätere begründete Reduktion | Lernnachweise von Kernmodulen entkoppeln und ausschließlich produkt-, erklärungs-, test- und revisionsbezogen halten; Auswahl bleibt `working`. | Feedback- und Selbstregulationsbefunde tragen aktuelle Handlungen, keine automatische Bewertung. [CLAIM-LP-010; CLAIM-LP-013] Die Reduzierbarkeit ist eine freigegebene Projektentscheidung. |

## 5. Alters-, domänen- und settingspezifische Grenzen

### 5.1 Altersgrenzen

- Ein erheblicher Teil der Forschung zu Programmierpraktiken, notional machines und Worked Examples stammt aus Hochschul- oder breiten Bildungssettings; für 10- bis 13-Jährige sind Form, Umfang und Fading nicht direkt abgesichert. [CLAIM-INF-003; CLAIM-INF-004; CLAIM-INF-005; CLAIM-LP-004]
- Productive-Failure-Befunde stammen überwiegend aus Mathematik, Klassen 6–10 und Hochschule; für Klasse 5 kann frühe Instruktion geeigneter sein. [CLAIM-LP-012]
- Desinformations- und GenAI-Interventionen untersuchen überwiegend Erwachsene, Studierende oder gemischte Bildungsstufen. [CLAIM-MED-003; CLAIM-MED-004]
- Normative Referenzrahmen mit Altersbändern sind keine empirischen Entwicklungsnormen und nicht curricular verbindlich für Baden-Württemberg. [CLAIM-MED-011; CLAIM-MED-012; CLAIM-INF-011]

### 5.2 Domänengrenzen

- Allgemeine Lernmechanismen werden nicht ohne fachliche Übersetzung übernommen: Abruf in IuM bedeutet etwa Trace rekonstruieren, Systemweg erklären, Beleg prüfen oder Entwurfsentscheidung begründen. [CLAIM-LP-007]
- Mathematikbefunde zu Worked Examples bestimmen nicht automatisch Programmier- oder Medienproduktionsaufgaben. [CLAIM-LP-004]
- Ein notional-machine-Modell ist sprach-, paradigm- und zweckabhängig; eine Visualisierung allein ist keine Lernhandlung. [CLAIM-INF-005]
- Medienanalyse verlangt technische, ökonomische, gestalterische und gesellschaftliche Beziehungen, ohne in jedem Modul alle Perspektiven künstlich zu verbinden. Die Evidenz zu einzelnen Plattformen ist zeit- und kontextgebunden. [CLAIM-MED-001; CLAIM-MED-005; CLAIM-MED-006]

### 5.3 Settinggrenzen

- Das Lernwerk ist lehrkraftorchestriert. Studien zu digitalen Einzelscaffolds oder Selbstregulation begründen keinen vollautomatischen Lernpfad. [CLAIM-LP-006; CLAIM-LP-013]
- Schulische iPads, Browser, MDM- und Filterkonfigurationen sind lokale und datierte Zielbedingungen, keine universelle Plattformgarantie. [CLAIM-DLE-012]
- Rechts-, Lizenz- und Standardstände benötigen vor Betrieb und bei relevanten Änderungen einen Recheck; diese Synthese ist keine Rechtsberatung. [CLAIM-DLE-004; CLAIM-DLE-005; CLAIM-DLE-011]

## 6. Konsequenzen für alle sieben Modulphasen

| Modulphase | Verbindliche Lernfunktion | Forschungsbasierte Ausgestaltung | Prüffrage |
| --- | --- | --- | --- |
| **1. Orientierung und Herausforderung** | relevante fachliche Frage, Ziel, Produkt und Funktion klären | Eine vorbereitete Herausforderung darf Exploration eröffnen; klare Struktur und begrenzte Wahl bleiben sichtbar. [CLAIM-LP-011; CLAIM-LP-012] | Ist die Herausforderung fachlich gehaltvoll und so begrenzt, dass sie anschließende Konzeptbildung vorbereitet? |
| **2. Vorwissen aktivieren** | vorhandene Kenntnisse und Modelle aufgabenbezogen sichtbar machen | Vorhersage, Skizze, Abruf, Modellvergleich oder Fallentscheidung werden lokal genutzt und nicht als stabiles Defizit profiliert. [CLAIM-LP-002; CLAIM-LP-007; CLAIM-INF-006; CLAIM-INF-010; CLAIM-MED-005] | Erzeugt die Aufgabe eine nutzbare Anschlussinformation ohne persönliche Offenlegung oder Profilbildung? |
| **3. Konzept aufbauen** | tragfähiges fachliches Modell entwickeln | Exploration wird explizit konsolidiert; aktive Beispiele, fokussierte Selbsterklärung und konsistente Repräsentationen verbinden relevante Beziehungen. [CLAIM-LP-003; CLAIM-LP-004; CLAIM-LP-005; CLAIM-LP-012; CLAIM-INF-005] | Können Lernende das Modell erklären und auf eine Vorhersage oder Abweichung beziehen? |
| **4. angeleitet erproben** | Konzept in überschaubaren Fällen anwenden | Hilfen adressieren Hürden, erhalten Entscheidungen und werden nicht telemetrisch ausgeblendet; PRIMM, Varianten und Testfälle geben eine mögliche fachliche Struktur. [CLAIM-LP-006; CLAIM-INF-002] | Welche Denkhandlung bleibt bei jeder Hilfe ausdrücklich bei den Lernenden? |
| **5. eigenständig handeln oder produzieren** | fachlich aussagekräftiges Produkt unter klaren Kriterien erstellen | Autonomie wird mit Struktur verbunden; Programm, Modell, Analyse, Sicherheitsentscheidung oder Medienprodukt zeigt eine eigene fachliche Entscheidung. [CLAIM-LP-011; CLAIM-LP-013; CLAIM-INF-003; CLAIM-MED-002] | Belegt das Produkt mehr als Bedienung oder bloße Reproduktion? |
| **6. prüfen, überarbeiten und übertragen** | Produkt und Strategie testen, Feedback nutzen, revidieren und transferieren | Testfälle, Gegenbelege, Quellenchecks, Kriterien und gezielte Feedbackinformation erzwingen dokumentierte Revision; Transfer wird eigens entworfen. [CLAIM-LP-009; CLAIM-LP-010; CLAIM-INF-007; CLAIM-MED-003; CLAIM-MED-004] | Ist eine Revision sichtbar, und prüft die Transferaufgabe dasselbe Prinzip in neuer Beziehung? |
| **7. gemeinsam sichern** | Begriffe, Modelle, Begründungen, Fehlwege und spätere Wiedervorlage konsolidieren | Die Lehrkraft verbindet Exploration und Instruktion, kontrastiert Modelle und plant verteilte Wiederaufnahme statt bloßer Abschlusszusammenfassung. [CLAIM-LP-008; CLAIM-LP-012; CLAIM-INF-010] | Ist geklärt, was fachlich gilt, welche Modellgrenze bleibt und wann das Konzept erneut abgerufen wird? |

Die Phasen sind funktional verbindlich, nicht zeitlich gleich lang. Flexible Module können an ausgewiesene Voraussetzungen andocken; Kernmodule sichern Progression und Curriculum-Abdeckung.

## 7. Konsequenzen für Lehrkraftorchestrierung

Die Lehrkraft ist nicht Ausfallhilfe eines Selbstlernkurses, sondern Teil des Designs:

- Sie klärt Ziel, Kriterien, Zeitrahmen und sinnvolle Wahlmöglichkeiten und beobachtet aktuelle Handlungen statt verborgene Kompetenzprofile. [CLAIM-LP-011; CLAIM-LP-013]
- Sie entscheidet anhand sichtbarer Produkte und Gespräche, welche fachliche Hilfe benötigt wird; das System automatisiert kein Fading aus Nutzungsdaten. [CLAIM-LP-006]
- Sie moderiert Predict–Run–Investigate–Modify–Make, Modellvergleiche und Debuggingbegründungen, statt nur fertige Programme abzunehmen. [CLAIM-INF-002; CLAIM-INF-007]
- Sie konsolidiert vorbereitete Exploration explizit und prüft in Klasse 5 besonders sorgfältig, ob die Herausforderung erreichbar war. [CLAIM-LP-012]
- Sie trennt bei sensiblen Themen fachliche Fallanalyse von persönlicher Betroffenheit und hält schulische Hilfe- und Eskalationswege bereit. [CLAIM-MED-007; CLAIM-MED-009]
- Sie nutzt Feedback als Information zum Produkt, zur Strategie oder zum nächsten Prüfschritt; Lob, Punkte oder Ranglisten ersetzen diese Information nicht. [CLAIM-LP-010]
- Sie plant gemeinsame Sicherung und spätere Wiedervorlage, weil Abruf und verteiltes Üben modulübergreifend organisiert werden müssen. [CLAIM-LP-007; CLAIM-LP-008]

Das Lehrkräftehandbuch muss dafür erwartbare Vorstellungen, fachlichen Hintergrund, Erklär- und Gesprächspunkte, Hilfen, Sicherheitsgrenzen, Testfälle, Qualitätskriterien und spätere Wiederaufnahmen bereitstellen.

## 8. Konsequenzen für die Analog-/Digitalwahl

### 8.1 Digital begründet

Digital ist fachlich stark, wenn tatsächliche Programmausführung, veränderliche Zustände, unmittelbare Testfälle, Simulation, Quellenöffnung, kontrollierter Variantenvergleich, Produktion oder Revision den Gegenstand tragen. [CLAIM-INF-005; CLAIM-LP-003] Digitalität allein belegt jedoch keine Lernwirkung. [CLAIM-DLE-014]

### 8.2 Analog begründet

Analog ist sinnvoll, wenn räumliche Anordnung, freies Skizzieren, haptische Manipulation, Verkörperung, gemeinsame Modellierung oder bildschirmfreie Diskussion die fachliche Beziehung klarer oder störungsärmer macht. Unplugged-Aktivitäten benötigen dafür eine ausgewiesene Zuordnung, Analogiegrenze und formale oder digitale Anschlussaufgabe. [CLAIM-INF-009]

### 8.3 Abnahmeregel

Jede Medienentscheidung beantwortet:

1. Welche fachliche Denkhandlung trägt das Medium?
2. Welche zusätzliche Bedien-, Such- oder Darstellungsbelastung entsteht?
3. Welche Modellgrenze oder Fehlerquelle ist zu markieren?
4. Welches überprüfbare Produkt oder welche Revision folgt?

Eine analoge Doppelstruktur wird nicht gepflegt. Ein Printmaterial ist nur dann Bestandteil eines Moduls, wenn seine eigene Lernfunktion dokumentiert ist. `PRIN-010` macht diese Entscheidung für Phase 1 prüfbar.

## 9. Konsequenzen für nicht personenbezogene Diagnosegelegenheiten

Diagnose bezeichnet hier eine aktuelle, aufgabenbezogene Gelegenheit für Anschlussreaktion und Feedback, keine integrierte Datensammlung.

Geeignete Formate sind:

- Ausgabe oder nächsten Zustand vorhersagen, Trace ergänzen, zwei Programme vergleichen oder einen Fehler gezielt reparieren. [CLAIM-INF-005; CLAIM-INF-006; CLAIM-INF-007]
- Internet-, Datenfluss- oder Empfehlungsmodell zeichnen, ordnen, kontrastieren und an einem kontrollierten Fall revidieren. [CLAIM-INF-010; CLAIM-MED-001; CLAIM-MED-005]
- Behauptung und Quelle zuordnen, Gegenbeleg prüfen und ein Unsicherheitsurteil formulieren. [CLAIM-MED-003; CLAIM-MED-004]
- Testfall, Kriterienraster, Muster- oder Gegenbeispiel auf ein aktuelles Produkt anwenden. [CLAIM-LP-009; CLAIM-LP-010]
- Eigenes Vorgehen planen, Zwischenstand prüfen und Revision begründen. [CLAIM-LP-013]

Ausgeschlossen sind Konten, Kompetenzprofile, Rankings, Telemetrie, dauerhafte Fehlvorstellungsetiketten, psychische oder spielbezogene Risikoscores, private Nutzungsverläufe und zentrale Konfliktakten. [CLAIM-INF-006; CLAIM-MED-007; CLAIM-MED-008; CLAIM-MED-010; CLAIM-DLE-004]

Antworten bleiben flüchtig oder lokal, werden bewusst exportiert und können vollständig gelöscht werden. Lokale Speicherung ist dennoch technisch und rechtlich zu prüfen und darf nicht als garantiert dargestellt werden. [CLAIM-DLE-005; CLAIM-DLE-006]

## 10. Konsequenzen für das später reduzierbare Beurteilungsinstrumentarium

Das Instrumentarium bleibt `working`. Es darf vollständig genug sein, um Lernprodukte, Erklärungen, Tests und Revisionen zu beurteilen, aber weder die Modulgrammatik noch das Curriculum dominieren.

Tragfähige Bestandteile sind:

- kommentierte Programme mit Vorhersage, Tests, Debugginghypothese und Begründung. [CLAIM-INF-002; CLAIM-INF-007]
- Daten-, Internet- oder notional-machine-Modelle mit ausgewiesenen Modellgrenzen. [CLAIM-INF-005; CLAIM-INF-010]
- Evidenzdossiers, Mechanismuskarten, Sicherheitsentscheidungen und revidierte Medienprodukte ohne Personenscore. [CLAIM-MED-003; CLAIM-MED-007; CLAIM-MED-010]
- Kriterienraster, Vergleichsbeispiele und Feedback, die Produkt, Strategie oder nächsten Prüfschritt adressieren. [CLAIM-LP-010]
- sichtbare Planung, Zwischenprüfung und Revision, ohne Selbstregulation als Eigenschaft zu bewerten. [CLAIM-LP-013]

Die Lernendenanwendung vergibt keine Noten, Punkte oder Kompetenzprofile. Die pädagogische Bewertung bleibt bei der Lehrkraft. Bewertungsinstrumente werden technisch und inhaltlich von Kernlernzielen und Modulen entkoppelt, sodass einzelne Instrumente später ohne Umbau des Lernwegs gestrichen werden können. `PRIN-015` operationalisiert diese Reduzierbarkeit.

## 11. Phase-1-Inputs und Abnahmekriterien

| Input für das Plattformfundament | Abnahmekriterium | Prinzipien |
| --- | --- | --- |
| Lernfunktionsvertrag für Aktivitäten und Komponenten | Jede Komponente nennt Ziel, fachliche Handlung, Input, prüfbaren Output, Feedback und Sicherungsbezug; funktionslose Interaktivität fällt durch. | `PRIN-001` |
| Lokale Vorwissens- und Selbstcheckformate | Ohne Konto und zentrale Speicherung nutzbar; keine stabile Diagnose aus Einzelantworten; Lehrkraftreaktion dokumentiert. | `PRIN-002` |
| Explorations- und Instruktionsfelder im Modulmanifest | Aufgabe, Begrenzung, erwartete Wege, Konsolidierungs- und Sicherungspunkt sind getrennt erfasst. | `PRIN-003` |
| Aufgaben- und Hilfeschema | Vollständiges Beispiel, Lücke, Modifikation, Eigenkonstruktion, fachliche Hürde und erhaltene Kernhandlung sind modellierbar; kein automatisches Fading. | `PRIN-004` |
| Wiederaufnahme-, Abruf- und Transferschema | Unmittelbare Anwendung, verzögerter Abruf und Transfer besitzen getrennte Kennzeichen und Kriterien. | `PRIN-005` |
| Strukturierte Wahl und Selbstregulationshandlung | Ziel, Kriterien, Zeitrahmen, Wahlraum, Planung, Zwischenprüfung und Revision sind sichtbar; keine Telemetrieinferenz. | `PRIN-006` |
| Fachtypische Programmieraufgaben | Tracing, Erklären, Modifizieren, Testen, Debugging und Eigenkonstruktion sind unterscheidbar; Block/Text nicht altersautomatisch. | `PRIN-007` |
| Mehrschrittige Medienanalyse | Mechanismus, Akteur, Interesse, Beleg, Gegenbeleg, Unsicherheit und Revision sind darstellbar; kein Detektor-Endurteil. | `PRIN-008` |
| Schutzvertrag für sensible Inhalte | Fiktive oder kuratierte Fälle, Offenlegungsgrenze, Hilfsweg, Aktualitätsreview und sichere Produkte sind dokumentiert. | `PRIN-009` |
| Medienbegründung und optionales Printmaterial | Digitalfunktion oder analoge Eigenfunktion ist benannt; Analogmaterial hat Analogiegrenze und Anschlussprodukt; kein Parallelbestand. | `PRIN-010` |
| Dateninventar und lokaler Speichervertrag | Datenart, Zweck, Speicherort, Löschung, Export und Hostingfluss dokumentiert; reale Speicherprobe, flüchtiger Modus und Rechtsrecheck vorhanden. | `PRIN-011` |
| Accessibility-Vertrag | Vollständiges WCAG-2.2-AA-Gate plus gleichwertige Tastatur-, Touch- und Assistive-Technology-Pfade; Nutzeraufgaben getrennt ausgewertet. | `PRIN-012` |
| Offline-, Release- und Browservertrag | Installation, Erstladung, Netzverlust, Teilcache, Altclient, Update, Rollback, Wiederanbindung, MDM und Browsermatrix getrennt getestet. | `PRIN-013` |
| OER- und Assetvertrag | Bearbeitbare Quellen und assetgenaue Urheber-, Quellen-, Lizenz-, Änderungs-, Drittmaterial- und Kompatibilitätsdaten vorhanden. | `PRIN-014` |
| Exportierbare Lernprodukte und reduzierbare Kriterien | Produkte und Kriterien funktionieren ohne zentrale Bewertung; Lern- und Leistungssituation getrennt; Instrumente vom Kernmodul entkoppelt. | `PRIN-015` |

Phase 1 darf diese Inputs in Architektur und Schemata übersetzen. Eine Lernwirkung ist erst nach fachlichem, didaktischem und technischem Review sowie Unterrichtserprobung zu beurteilen.

## 12. Ungelöste Fragen und Recheck-Trigger

### 12.1 Empirische Rechecks

- Welche PRIMM- und notional-machine-Ausgestaltung unterstützt 10- bis 13-Jährige in Block- und Textdarstellungen? [CLAIM-INF-002; CLAIM-INF-005; CLAIM-INF-008]
- Welche Form und Dosierung von Worked Examples, Selbsterklärung und Fading trägt Codeverständnis, Datenmodelle und Medienanalyse? [CLAIM-INF-004; CLAIM-LP-004; CLAIM-LP-005; CLAIM-LP-006]
- Welche vorbereitete Exploration ist in Klasse 5 erreichbar, und wann ist Instruction before Problem Solving günstiger? [CLAIM-LP-012]
- Welche Abstände und Transferformate sichern komplexe IuM-Konzepte, ohne bloße Wiederexposition zu erzeugen? [CLAIM-LP-007; CLAIM-LP-008; CLAIM-LP-009]
- Welche wiederholte Prüfsequenz verbessert bei 10- bis 13-Jährigen nachhaltig die Bewertung von KI-Ausgaben und Desinformation? [CLAIM-MED-003; CLAIM-MED-004]
- Welche sensiblen Medienbildungsaufgaben fördern Analyse und Handlungsfähigkeit, ohne Betroffenheit zu verlangen oder problematische Darstellungen zu verstärken? [CLAIM-MED-007; CLAIM-MED-009; CLAIM-MED-010]

**Trigger:** Pilotierung jedes zentralen Aufgabentyps; widersprüchliche Unterrichtsbefunde; neue systematische Evidenz; Übertragung auf andere Alters- oder Niveaustufen.

### 12.2 Curriculare Rechecks

- Die endgültige Progression, Klassenverteilung und Verbindlichkeit folgen dem vollständigen Crosswalk aus Lesehilfe, Basiskurs Medienbildung und Aufbaukurs Informatik, nicht der Forschungssynthese.
- Professionelle Referenzrahmen dienen nur als Kontrollperspektive und ersetzen keine baden-württembergische Vorgabe. [CLAIM-INF-011; CLAIM-MED-011; CLAIM-MED-012]

**Trigger:** Veröffentlichung oder Inkraftsetzung eines neuen Fachplans; Änderung amtlicher Quellen; Curriculum-Crosswalk und Phase-0-Abschlussreview.

### 12.3 Rechtliche und technische Rechecks

- Betreiber, Hosting, Logs, Freitext, Export und Endgerätespeicherung benötigen vor öffentlichem Betrieb eine zuständige Datenschutz- und Rechtsprüfung. [CLAIM-DLE-004; CLAIM-DLE-005]
- WCAG-Errata, Browser- und MDM-Hauptversionen, Storage-Verhalten, App-Manifest- und Service-Worker-Reifegrad sowie schulische Filter können die Abnahme verändern. [CLAIM-DLE-001; CLAIM-DLE-006; CLAIM-DLE-007; CLAIM-DLE-012]
- CC-Kompatibilitätsliste und Drittmaterialstatus sind bei jedem Import oder Lizenzwechsel erneut zu prüfen. [CLAIM-DLE-010; CLAIM-DLE-011]

**Trigger:** Phase-1-Freeze; jedes öffentliche Release; Datenfluss-, Schema-, Cache- oder Lizenzänderung; Browser-/iPadOS-/MDM-Hauptupdate.

## 13. Index der Designprinzipien

| ID | Titel | Status | Tragende Claimpakete |
| --- | --- | --- | --- |
| `PRIN-001` | Lernprozessqualität vor Medien- oder Methodenlabel | `working` | LP, DLE |
| `PRIN-002` | Vorwissen und Vorstellungen lokal aktivieren | `working` | LP, INF, MED |
| `PRIN-003` | Exploration vorbereiten und explizit konsolidieren | `working` | LP, INF |
| `PRIN-004` | Beispiele aktiv verarbeiten und Hilfen fachlich dosieren | `working` | INF, LP |
| `PRIN-005` | Abruf, Verteilung, Feedback und Transfer getrennt entwerfen | `working` | LP |
| `PRIN-006` | Autonomie durch Struktur und explizite Selbstregulation ermöglichen | `working` | LP |
| `PRIN-007` | Programmierpraktiken sichtbar progressiv verbinden | `working` | INF |
| `PRIN-008` | Medienmechanismen aktiv und mehrschrittig analysieren | `working` | MED |
| `PRIN-009` | Sensible Medienthemen fall- und mechanismusbezogen bearbeiten | `working` | MED |
| `PRIN-010` | Digitales Primärmedium und begründete Analogwahl | `working` | LP, INF, DLE |
| `PRIN-011` | Datenminimierung und fehlertolerante lokale Arbeit | `reviewed` | DLE |
| `PRIN-012` | WCAG-Baseline durch reale Nutzeraufgaben ergänzen | `reviewed` | DLE |
| `PRIN-013` | Installation, Offlinebetrieb, Updates und Schulbrowser getrennt abnehmen | `working` | DLE |
| `PRIN-014` | OER als bearbeitbare Rechte- und Quellenkette ausliefern | `reviewed` | MED, DLE |
| `PRIN-015` | Lernnachweise produktbezogen und reduzierbar halten | `working` | INF, LP, MED |

Die drei `reviewed` Prinzipien bilden unmittelbar geprüfte technische oder normative Anforderungen mit konkret geprüfter Projektanwendung ab. Die zwölf `working` Prinzipien enthalten mindestens eine inferentielle Übertragung auf IuM 5–7, die in Phase 1 spezifiziert und im Goldstandard-Pilot fachlich, didaktisch und technisch geprüft werden muss. Kein Prinzip erhält vor diesem Review- und Erprobungsweg den Status `standard`.
