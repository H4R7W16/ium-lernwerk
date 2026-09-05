# LXF05 Material- und Experience-Grammatik

**Status der LXF05-Muster:** `reviewed` (Nutzerfreigabe 2026-09-05)

**Status des Gesamtfundaments:** `working` bis zum gesonderten LXF07-Review

**Stichtag:** 2026-09-05

**Geltung:** Gymnasium Baden-Württemberg, Niveau E, Klassen 5–7  
**Voraussetzung:** freigegebener LXF04-Lernarchitektur-Vertrag  
**Produktbindung:** `product-neutral`  
**Inhaltsproduktion:** `frozen`

## Vertragsgrenzen

LXF05 übersetzt die freigegebenen LXF04-Prinzipien in wiederverwendbare Material- und Interaktionsmuster. Der Vertrag beschreibt Lernfunktionen, notwendige Informationen, Handlungen, Rückmeldung, Barrieren und Prüfwege. Er schreibt weder eine Oberfläche noch eine feste Seitenfolge, Elementzahl, Dauer oder visuelle Stilwelt vor.

Es entstehen ausdrücklich:

- keine Lernendentexte und kein fachlicher Modulinhalt;
- keine App-, Portal-, PWA-, Routing- oder Navigationskomponente;
- keine universelle Seiten-, Element-, Minuten- oder Altersgrenze;
- kein Produktentscheid und keine Übernahme von LXP05;
- kein Pilot-, Wirksamkeits-, Release- oder Cutover-Nachweis.

Die zehn Muster wurden nach ihrem fachlichen Abschlussreview am 5. September 2026 ausdrücklich vom Nutzer freigegeben und stehen auf `reviewed`. Die Freigabe gilt für LXF05 als Grundlage von LXF06. Das Gesamtfundament bleibt bis zum gesonderten LXF07-Review `working`. Technische Prüfbarkeit ersetzt weder fachlichen Review noch Nutzungserprobung.

## Globale Gestaltungsregeln

### Kohärenz und Informationshierarchie

Zielzustand, zentrale Lernhandlung, Material, Qualitätskriterium und erwartetes Produkt bilden eine sichtbare Kette. Die wichtigste fachliche Beziehung erhält Vorrang vor Bedienhinweisen, Metadaten und Zusatzangeboten. Ein Ausspielkanal darf diese Hierarchie darstellen, aber nicht neu definieren.

Information wird nach fachlichen Einheiten gegliedert. Chunking bedeutet nicht pauschale Kürze: Ein Abschnitt endet dort, wo eine Beziehung verstanden, vorhergesagt, ausgeführt, verglichen oder gesichert werden kann. Zusammengehörige Informationen bleiben auffindbar beieinander.

### Signaling und Korrespondenz

Jedes Signal markiert eine benennbare fachliche Beziehung, einen Status oder eine nächste Handlung. Farbe, Kontrast, Pfeil, Position, Bewegung oder Typografie sind kein Selbstzweck. Zusammengehörige Texte, Bilder, Codes, Modelle, Tabellen und Zustände werden räumlich verbunden; zeitliche Veränderungen bleiben schrittweise oder statisch rekonstruierbar.

Signaling darf keine zusätzliche Symbolsprache erzeugen, die erst gelernt werden muss. Dieselbe Beziehung und derselbe Zustand erhalten konsistente Bezeichner. Bedeutung ist nie ausschließlich farblich, auditiv oder durch Bewegung codiert.

### Segmentierung und progressive Offenlegung

Segmentierung folgt fachlichen Einheiten und sinnvollen Haltepunkten. Progressive Offenlegung ist zulässig, wenn sie Nebenlast reduziert und die nächste fachliche Handlung erreichbar hält. Sie ist unzulässig, wenn relevante Informationen über versteckte Ansichten verteilt werden oder zusätzliche Klicks das gedankliche Zusammenführen erschweren.

Es gibt keine universelle maximale Anzahl von Abschnitten, Elementen oder Minuten. Quantifizierte Regeln benötigen eine direkt ausgewiesene Claimgrundlage und einen beschriebenen Geltungsbereich; LXF05 legt keine solche Regel fest.

### Sprache und Lesbarkeit

Aufträge benennen Handlung, Produkt und Qualitätsbezug. Fachbegriffe werden konsistent eingesetzt und dort erläutert, wo ihr Verständnis für den nächsten Schritt nötig ist. Kurze Sätze, Listen oder Zwischenüberschriften dienen der Lesbarkeit, ersetzen aber keine fachlich vollständige Beziehung.

Schmale und breite Darstellungen bewahren dieselbe Informationsreihenfolge. In einer breiten Komposition dürfen zusammengehörige Darstellungen nebeneinanderstehen; in einer schmalen Komposition folgt die erklärende oder bedienende Information unmittelbar auf ihren Referenten. Keine Variante verlangt horizontales Suchen oder verändert die Lernhandlung.

### Hilfe, Wahl und Anspruch

Hilfe liegt nahe an der erkennbaren Hürde und führt zum eigenständigen Kernschritt zurück. Sie kann als Hinweis, Kontrollfrage, Sprachgerüst, Teilmodell, Alternativdarstellung oder Lehrkraftimpuls erscheinen. Eine Musterlösung, die den Kernschritt vorwegnimmt, ist keine Hilfe im Sinn dieses Vertrags.

Wahl ist nur sinnvoll, wenn alle Optionen dasselbe Ziel, dieselbe fachliche Kernhandlung und dieselben Qualitätskriterien tragen. Dekorative Themenwahl, Punkte, Badges, Streaks oder Ranglisten gelten weder als Autonomie noch als Lernnachweis. Dekorative Gamification ist kein Default.

### Mediensemantik und Interaktionsrolle

Ein Medium oder eine Interaktion wird durch seine Lernfunktion begründet: orientieren, Vorwissen sichtbar machen, ein fachliches Problem eröffnen, erklären oder modellieren, angeleitet handeln, selbstständig anwenden, Rückmeldung nutzen oder sichern und übertragen. Klicken, Ziehen, Abspielen, Speichern oder Abgeben ist ohne fachlich interpretierbares Produkt keine Lernhandlung.

Digitale Umsetzung ist nur dann fachlich begründet, wenn sie eine zentrale Lernhandlung, kohärente Repräsentation, Rückmeldung, Zugänglichkeit oder Orchestrierung besser ermöglicht. Der gleiche Patternvertrag kann in HTML, Papier, Präsentation, LMS, Tafelarbeit oder Gespräch realisiert werden, sofern die Lernfunktion erhalten bleibt.

### Feedbackhierarchie

Formatives Feedback verbindet zuerst Ziel oder Kriterium, dann eine konkrete Produktstelle und schließlich die nächste fachliche Handlung. Aufgaben- und Prozessrückmeldung haben Vorrang vor Personenlob, Punkten oder sozialem Vergleich. Eine richtige oder falsche Markierung reicht nur dort, wo sie unmittelbar in eine verständliche Prüfung oder Revision führt.

Feedback ist erst lernfunktional, wenn Lernende es verstehen, nutzen und am Produkt weiterarbeiten können. Ausgangs- und Revisionsstand bleiben vergleichbar. Lern- und Leistungsaufgabe werden nicht vermischt.

### Status, Fehlerbehebung und Wiedereinstieg

Bearbeitet, fachlich geprüft, offen, blockiert und nicht anwendbar sind unterschiedliche Zustände. Der Arbeitsstand zeigt niemals pauschal Kompetenz oder Lernerfolg an. Ein Prozentwert, eine Anzahl erledigter Elemente oder Bearbeitungszeit ist kein Lernnachweis.

Fehlerbehebung bewahrt Eingabe, fachlichen Kontext und nächste Handlung oder erklärt transparent, was nicht erhalten werden konnte. Nach Abbruch, Gerätewechsel oder Unterrichtsunterbrechung sind letzter fachlicher Stand, offene Entscheidung, nächster Schritt und erreichbarer Fallback rekonstruierbar.

### Zugänglichkeit, Print und Nicht-JavaScript

Technische Konformität, funktionaler Zugang und Lernen werden getrennt geprüft. Tastatur-, Touch- und Textpfade müssen die gleiche fachliche Kernhandlung ermöglichen. Status, Fokus, Fehler und Rückmeldung sind semantisch und textlich verständlich. Alternative Darstellungen bewahren Ziel und Qualitätskriterium.

Wenn eine Lernfunktion ohne Laufzeit fortsetzbar sein muss, existiert ein druckbarer oder Nicht-JavaScript-Fallback. Ein Fallback darf eine nicht abbildbare Funktion transparent markieren; er darf sie nicht stillschweigend durch eine fachlich leichtere Aufgabe ersetzen. Druckansichten erhalten Lesereihenfolge, Referenzen, Arbeitsraum und Lehrkrafthinweise, ohne interaktive Zustände vorzutäuschen.

## Zehn Patternfamilien

| ID | Patternfamilie | Kernfunktion | Nicht einsetzen, wenn … |
|---|---|---|---|
| `LXF05-PT-001` | `entry-and-orientation` | Ziel, Zweck, erster Schritt und Ausgangsprodukt verbinden | nur Begrüßung oder persönliche Selbstauskunft entsteht |
| `LXF05-PT-002` | `worked-example-with-active-processing` | Modellierung durch Vorhersage, Begründung und nahe Anwendung aktiv verarbeiten | nur kopiert oder passiv abgespielt wird |
| `LXF05-PT-003` | `linked-representations-and-signaling` | Darstellungen fachlich zuordnen und relevante Beziehungen signalisieren | zusätzliche Darstellung oder Hervorhebung nur dekoriert |
| `LXF05-PT-004` | `prediction-execution-comparison` | Erwartung, Ausführung und Revision an sichtbaren Zuständen verbinden | Überraschung oder richtig-falsch den fachlichen Vergleich ersetzt |
| `LXF05-PT-005` | `guided-practice-and-help` | Hilfe an Hürde und Produktstelle koppeln und wieder zurücknehmen | Hilfe die Kernhandlung löst oder Anspruch senkt |
| `LXF05-PT-006` | `feedback-and-revision` | Kriterium, Produktstelle, nächste Handlung und Revision verbinden | nur Punkte, Lob, Rang oder Abschlussbewertung entstehen |
| `LXF05-PT-007` | `retrieval-and-return` | frühere Sicherung nach Unterbrechung aktiv abrufen | bloße Wiederexposition oder eine erfundene Universalfrist vorliegt |
| `LXF05-PT-008` | `transfer` | relevante Beziehung an veränderte fachliche Bedingungen anpassen | nur Oberfläche oder Werte ausgetauscht werden |
| `LXF05-PT-009` | `progress-and-reentry` | Arbeitsstand und nächste Handlung ohne Kompetenzbehauptung sichern | Erledigung, Zeit oder Prozent als Lernstand erscheinen |
| `LXF05-PT-010` | `accessible-alternative` | gleichwertige Zugangs-, Ausdrucks- und Fallbackpfade sichern | Alternative oder Technikcheck die Lernfunktion abschwächt |

Die verbindlichen Details stehen in `material-patterns.json`. Jede Patternfamilie enthält Lernenden- und Lehrkraftzweck, LXF04-Prinzipien, Lernfunktionen, Einsatz- und Nicht-Einsatzbedingungen, Pflicht- und Verbotelemente, beobachtbare Prüfmerkmale, Prüfmethode und Accessibility-Anforderungen. `productDependencies` bleibt leer.

## Neutrale Walkthroughs

Die folgenden Gerüste prüfen Beziehungen, nicht Layouts. Sie enthalten keine echte Aufgabe, keinen Lernendentext, keine Navigationsbezeichnung und kein visuelles Design. Die Zeile „Barriere“ verlangt eine Funktionsprüfung; sie weist keiner Person ein Merkmal zu.

### Walkthrough 1: Einstieg und Orientierung

| Prüffeld | Abstrakte Ausprägung |
|---|---|
| Lernendenfrage | Was ist das fachliche Ziel, wofür wird mein Produkt gebraucht und womit beginne ich? |
| Erforderliche Information | Zielzustand, Zweck, Kernhandlung, Arbeitsstand, erster Schritt und Fallback |
| Handlung | aufgabenbezogenes Ausgangsprodukt erzeugen oder gesicherten Stand aufnehmen |
| Rückmeldung | Produktlage unterscheiden und nächste fachliche Handlung sichtbar machen |
| Lehrkraftrolle | Ausgangsprodukt lesen, Barrieren beobachten und Übergang entscheiden |
| Barriere | Orientierung darf nicht von Navigationserfahrung oder persönlicher Offenlegung abhängen |
| Prüfmethode | `content-walkthrough` |

Verwendete Muster: `LXF05-PT-001`, `LXF05-PT-009`, `LXF05-PT-010`.

### Walkthrough 2: Zentrale Lernhandlung

| Prüffeld | Abstrakte Ausprägung |
|---|---|
| Lernendenfrage | Welche Beziehung soll ich erklären, ausführen, vergleichen oder revidieren? |
| Erforderliche Information | Auftrag, kohärente Repräsentationen, Kriterium, Hilfe und Revisionsweg |
| Handlung | vorhersagen, modellieren, ausführen, vergleichen, begründen und revidieren |
| Rückmeldung | Kriterium, Produktstelle und nächsten Schritt verbinden |
| Lehrkraftrolle | Kernhandlung beobachten, Hilfe dosieren, Haltepunkt und Klärung rahmen |
| Barriere | Bedienung, Sprache und Darstellungswechsel dürfen die Denkhandlung nicht verdecken |
| Prüfmethode | `expert-review` |

Verwendete Muster: `LXF05-PT-002`, `LXF05-PT-003`, `LXF05-PT-004`, `LXF05-PT-005`, `LXF05-PT-006`, `LXF05-PT-010`.

### Walkthrough 3: Sicherung und Wiedereinstieg

| Prüffeld | Abstrakte Ausprägung |
|---|---|
| Lernendenfrage | Welche Beziehung ist gesichert, was bleibt offen und wie rufe ich sie später ab oder übertrage sie? |
| Erforderliche Information | gesichertes Produkt, Kernbeziehung, offener Stand, Rückkehrpunkt, Transferänderung und Fallback |
| Handlung | sichern, nach Unterbrechung rekonstruieren oder an veränderte Bedingungen anpassen |
| Rückmeldung | Bearbeitung, Prüfung und offene Handlung unterscheiden und Weiterarbeit auslösen |
| Lehrkraftrolle | Sicherung prüfen, Abruf ermöglichen, Transfer rahmen und Anschluss entscheiden |
| Barriere | Arbeitsstatus darf weder Prozentfortschritt noch Lernstandsdiagnose vortäuschen |
| Prüfmethode | `usability-test` |

Verwendete Muster: `LXF05-PT-007`, `LXF05-PT-008`, `LXF05-PT-009`, `LXF05-PT-010`.

## Lehrkraftvarianten

Ein Pattern kann in der Orchestrierung drei neutrale Varianten annehmen:

| Variante | Einsatz | Erhaltene Vertragsanteile |
|---|---|---|
| gemeinsam modelliert | neue, mehrschrittige oder sprachlich anspruchsvolle Beziehung | Ziel, aktive Verarbeitung, sichtbares Produkt, Haltepunkt |
| begleitet individuell oder im Tandem | Kernhandlung ist erreichbar, Hürden variieren | gleiches Ziel und Kriterium, hürdenbezogene Hilfe, Beobachtungsfrage |
| eigenständig mit Rückkehrpunkt | Beziehung wurde aufgebaut; Anwendung, Abruf oder Transfer steht an | Kernhandlung, gespeicherter Stand, Fallback, anschließende Auswertung |

Diese Varianten definieren keine Sozialform als universal wirksam. Kooperation ist nur dann fachlich begründet, wenn individuelle Verantwortlichkeit, gemeinsames Minimalprodukt, Zwischenkontrolle, Zusammenführung und Fallback später in der konkreten Orchestrierung sichtbar werden. Die verbindliche Orchestrierungsprüfung folgt erst in LXF06.

## Prüf- und Statuslogik

Die Prüfung hat drei ausdrücklich getrennte Ebenen. Das JSON-Schema prüft ausschließlich Struktur, Pflichtfelder, Typen und geschlossene Wertebereiche. Der Python-Validator ergänzt einen konservativen Hinweisfilter für häufige Zahlen-, Produkt-, Darstellungs- und Lernendentextformulierungen. Dieser Filter ist kein semantischer Beweis: natürliche Sprache lässt sich mit Wortlisten weder vollständig noch ohne Fehlalarme klassifizieren. Verbindlich entscheidet deshalb für jedes Pattern ein `expert-review` oder `content-walkthrough` anhand der folgenden Kriterien. Accessibility-Audit, Usability-Test und Unterrichtspilot beantworten zusätzliche Fragen und dürfen diesen Neutralitätsreview nicht ersetzen.

`x-iumSemanticValidation` im Schema dokumentiert diese Zuständigkeitsgrenze maschinenlesbar. Formulierungen in `forbiddenElements` und `doNotUseWhen` dürfen konkrete Negativbeispiele nennen; der Hinweisfilter wertet nur vorschreibende Felder aus. So bleibt ein Verbot wie „kein verpflichtender Weiter-Button“ formulierbar, ohne eine solche Komponente selbst vorzuschreiben.

Ein Pattern besteht den LXF05-Review nur, wenn:

1. sein Lernenden- und Lehrkraftzweck zu mindestens einer LXF04-Lernfunktion passt;
2. alle referenzierten LXF04-Prinzipien `reviewed` sind;
3. Einsatz- und Nicht-Einsatzbedingungen den Geltungsbereich begrenzen;
4. Pflicht- und Verbotelemente sowie beobachtbare Kriterien eine reale Prüfung erlauben;
5. Zugänglichkeit die fachliche Kernhandlung erhält;
6. keine Produktabhängigkeit, Lernendentext oder universelle Mengen- und Zeitregel eingeführt wird;
7. `expert-review` oder `content-walkthrough` als fachlicher Neutralitätsreview vorgesehen ist; ausschließlich technische oder nutzungsbezogene Prüfungen reichen nicht.

`working` bedeutet hier: als prüfbare Arbeitsgrundlage angelegt, aber noch nicht als Fundament freigegeben. `reviewed` darf erst nach dem eigenen LXF05-Review vergeben werden. `standard` ist in diesem Vertrag nicht zulässig und würde reale wiederholte Nutzung voraussetzen.

## WU-Abgleich

Der Abgleich dient der Reflexion, nicht als zusätzlicher empirischer Claim:

- Band 3, Konstruktive Unterstützung: `guided-practice-and-help` bindet Hilfe an eine erkennbare Hürde, erhält die Kernhandlung und sieht Rücknahme vor.
- Band 5, Formatives Feedback: `feedback-and-revision` verbindet Lernstand, Ziel oder Kriterium und nächsten Schritt; Personenlob und sozialer Vergleich tragen die Schleife nicht.
- Band 6, Aufgaben im Fachunterricht: alle Muster benennen eine fachliche Handlung und ein interpretierbares Produkt; Organisation und Oberfläche gelten nicht als Aufgabenqualität.
- Band 9, Digitale Medien: digitale Interaktion ist nur über ihre Lernfunktion begründet; Klick, Abgabe und Dashboardstatus sind kein Lernnachweis.

Für IuM 5–7 liegt kein separates fertiges allgemeines Workspace-Fachprofil vor. Stufenspezifische Aussagen stammen deshalb ausschließlich aus dem freigegebenen LXF03-Profil; offene Alters- und Pilotfragen bleiben offen und werden nicht durch Patternregeln geschlossen.

WU-Check

- Kognitive Aktivierung: Jede Patternfamilie verlangt eine fachliche Handlung oder ein fachlich interpretierbares Produkt.
- Konstruktive Unterstützung: Hilfe ist hürdenbezogen, begrenzt und führt zur Eigenleistung zurück.
- Klassenführung / Struktur: Ziel, Zustand, nächster Schritt, Haltepunkt und Fallback sind sichtbar; die konkrete Orchestrierung folgt in LXF06.
- Aufgabenqualität: Ziel, Lernhandlung, Produkt und Kriterium bleiben kohärent; Lern- und Leistungsaufgabe werden getrennt.
- Feedback / Diagnose: Rückmeldung muss eine nächste fachliche Handlung und Revision ermöglichen.
- Kooperation / Verantwortlichkeit: noch kein Universalpattern; konkrete kooperative Varianten benötigen in LXF06 individuelle Verantwortlichkeit und Zusammenführung.
- Diagnose-Fallback: Ausgangs-, Zwischen- und Rückkehrprodukte dürfen nicht in Personenprofile verdichtet werden.
- Sprachsensibilität / Zugänglichkeit: Begriffe, Bezeichner, Status und Alternativpfade bleiben konsistent und funktional gleichwertig.
- Wichtigste Verbesserung: LXF06 muss die Patterns in einen belastbaren Lehrkraftworkflow und methodenspezifische Experience-Gates überführen.
- WU-Quellenbasis: lokale Exzerpte der IBBW-Reihe „Wirksamer Unterricht“, Bände 3, 5, 6 und 9; Unterrichtsplanung – Manifest; keine neue Wirksamkeitsbehauptung.

## Übergabegrenze

LXF05 liefert einen Patternvertrag und drei neutrale Walkthroughs. Die ausdrückliche Nutzerfreigabe vom 5. September 2026 öffnet LXF06 als nächsten einzelnen Umsetzungsschritt für Orchestrierungsstandard und Experience-Gates. Ein neutraler Referenzslice, konkrete Module, visuelles Design, Produktkomponenten, LXP05-Integration, Pilotierung, Veröffentlichung und Cutover bleiben geschlossen.
