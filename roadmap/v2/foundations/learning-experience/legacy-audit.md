# LXF01 Bestandsaudit

**Stand:** 3. September 2026

**Scope:** 13 Lernpsychologie-Claims, 15 Designprinzipien, das Fachprofil IuM Gymnasium 5–7 und LXP01–LXP04

**Maschinenlesbare Entscheidung:** [legacy-audit.json](legacy-audit.json)

**V2-Anforderung:** `V2-REQ-LXF-001`

**Gategrenze:** Bestandsklassifikation, keine Übernahmefreigabe und keine Inhaltsproduktion

Der Bestand ist substanziell, aber nicht unverändert produktionsfähig. Alle 33 Pflichtartefakte wurden einzeln geprüft. Das Ergebnis lautet: 29-mal `adapt`, dreimal `reference-only`, einmal `replace`, kein `retain` und kein `drop`. Dass kein vollständiges Artefakt unverändert übernommen wird, ist kein Urteil gegen seinen fachlichen Gehalt. Es verhindert, dass ältere Status- und Vertragslogiken ohne den neuen Evidenz-zu-Design-Vertrag zu V2-Standards werden.

## Tragfähiger Bestand

Folgende Inhalte sollen weiterverwendet werden, jedoch jeweils innerhalb neu geschlossener V2-Verträge:

- Die 13 Lernpsychologie-Claims besitzen registrierte, primär geprüfte Quellen und dokumentieren ihre wesentlichen Einschränkungen. Besonders tragfähig sind die Trennung von Tiefenstruktur und Methodenlabel, lokale Vorwissensaktivierung, aktive Beispielverarbeitung, fachlich gebundenes Scaffolding, aktiver Abruf, verteilte Wiederaufnahme, getrennte Transferprüfung, informationshaltiges Feedback, strukturierte Autonomie und vorbereitete Exploration mit expliziter Konsolidierung.
- Das Fachprofil beschreibt einen belastbaren Fachkern: eigenständige Lernstränge Informatik und Medienbildung, begründete Integration, fachliche Denkhandlungen, Repräsentationsstandards, typische Lernbarrieren, Programmierpraktiken, Medienanalyse, nicht personenbezogene Diagnosegelegenheiten und die Rolle der Lehrkraft.
- LXP01 setzt einen weiterhin sinnvollen Nordstern: Lernende müssen Zweck, aktuelle fachliche Handlung, Qualitätsmerkmal, nächste sinnvolle Revision und Anschluss an den Unterricht erkennen können. Progressive Offenlegung, lokale Datenhaltung und die klare Unterscheidung von technischer Konformität und Lernwirkung bleiben erhalten.
- LXP02s Trennung von Lernwerk-Kosmos und fokussiertem Lernstudio, kontrollierte Begriffe, sichere Übergänge und Recoverygrenzen sind brauchbare Architekturhypothesen.
- LXP03 liefert wertvolle Fragen und Gegenproben für Wide-/Schmalansicht, Tastatur, Touch, Assistive Technology, Offline-/Recoveryverhalten und Lehrkraftmomente.
- LXP04 enthält weiterhin verwertbare Einzelbefunde: semantische Designrollen, Fokus auf eine fachliche Handlung, Accessibility, Resilienz sowie die ausdrückliche Ablehnung einer vom IUM5-Screen abgeleiteten globalen Pattern Library.

Diese Substanz wird nicht als `retain` klassifiziert, weil jedes Ursprungsartefakt zusätzlich ungesicherte Übersetzungen oder einen für V2 unzureichenden Vertrag enthält. Tragfähige Teile werden über `adapt` neu begrenzt oder über `reference-only` als Prüfevidenz erhalten.

## Anpassungsbedürftiger Bestand

### 13 Lernpsychologie-Claims → LXF02

Alle Claims werden `adapt` zugeordnet. Ihre Aussagen, Quellenbezüge, Evidenzstufen und Einschränkungen sind eine gute Grundlage. Das alte Claimmodell führt aber nicht durchgehend getrennt:

- den angenommenen Wirkmechanismus;
- den konkreten Lernenden- und Aufgabenkontext;
- förderliche und schädliche Randbedingungen;
- die genaue Designentscheidung;
- beobachtbare Lern- oder Prozesskriterien;
- die zur Behauptung passende Prüfart.

LXF02 muss insbesondere verhindern, dass Worked Examples zu passivem Vormachen, Selbsterklärung zu generischen Warum-Fragen, Quizzing zu beliebiger Quizmechanik, Spacing zu bloßem Wiedersehen, Feedback zu einer Ampel und Productive Failure zu unbegleitetem Entdecken verkürzt werden.

### 13 Experience-relevante Prinzipien → LXF04

`PRIN-001` bis `PRIN-012` sowie `PRIN-015` werden `adapt` zugeordnet. Ihre Richtungen sind überwiegend plausibel, ihre heutige Struktur aus Statement, Claims, Anwendungsfeldern, Implikationen und Risiken ist aber noch kein geschlossener Evidence-to-Design-Vertrag. Mehrere Prinzipien bündeln zudem unterschiedliche Mechanismen:

- `PRIN-004` verbindet Worked Examples, Selbsterklärung, Repräsentationen, Scaffolding und Fading;
- `PRIN-005` verbindet Retrieval, Spacing, Feedback und Transfer;
- `PRIN-006` verbindet Autonomieunterstützung und explizite Selbstregulation.

LXF04 muss solche Bündel in prüfbare Entscheidungen zerlegen und je Entscheidung Mechanismus, Geltungsgrenzen, Positiv-/Negativmuster, beobachtbare Kriterien und Prüfverfahren angeben.

### Fachprofil → LXF03

Das Fachprofil wird `adapt` zugeordnet. Seine fachliche Substanz bleibt leitend. Die jahrgangsgenaue Aufteilung des gemeinsamen Bands 5/6 sowie Annahmen zur vorbereiteten Exploration, Hilfedosierung, Wiederholung, Selbstregulation und Materialerfahrung sind im Dokument selbst als `working` oder pilotierungsbedürftig markiert. LXF03 muss deshalb ein explizites Lernenden- und Stufenprofil für Klassen 5 bis 7 ergänzen: Vorwissen, Heterogenität, Lese- und Sprachlast, Aufmerksamkeit, Bedienerfahrung, Unterstützungsbedarf, soziale Arbeitsformen und Überforderungsgrenzen.

### LXP01 und LXP02 → LXF02/LXF04

LXP01 wird `adapt` zugeordnet. Seine sechs zusätzlichen Quellen sind nach IUM-V2-SRC maschinenlesbar registriert, aber erst LXF02 darf aus ihnen geprüfte V2-Claims bilden. LXP02 wird `adapt` zugeordnet: Seine Räume und Sicherheitsgrenzen bleiben Kandidaten, die elf Zustände und die hohe Objektdichte müssen jedoch aus dem neuen Evidenz- und Lernendenvertrag neu abgeleitet und vereinfacht werden.

## Zu ersetzende Annahmen

LXP04 wird als vollständiger normativer Produktionsvertrag `replace` zugeordnet. Das betrifft nicht jede Einzelregel, sondern seinen Anspruch, bereits eine hinreichende und produktionsreife Experience-Grammatik zu bilden.

Die entscheidende Gegenprobe ist der ungemergte LXP05-Kandidat. Trotz Contract-first-Ansatz und ausdrücklicher Portabilitätsregeln entstand eine sehr lange Werkstattoberfläche. Elf Inhaltsphasen und acht Experience-Zustände blieben als parallele Modelle sichtbar. Die Sicherung wurde formal und formularlastig, die Belegkarte drohte das eigentliche Lernprodukt zu dominieren, und die Lehrkraftspur beschrieb Orchestrierung stärker, als sie reale Unterrichtshandlungen ausführbar machte.

LXF05 ersetzt LXP04 deshalb durch eine schlankere Material- und Experience-Grammatik. Diese muss zunächst an unterschiedlichen fachlichen Lernhandlungen, Belastungsgrenzen und realen Unterrichtsmomenten tragen. Erst danach dürfen Komponenten, Pattern und Inhaltsverträge daraus entstehen.

## Nur historische Referenz

- `PRIN-013` bleibt als technische Randbedingung für Plattform- und Releasearbeit erhalten. Installierbarkeit, Offlinekorrektheit, Migration und Schulbrowserprüfung sind wichtig, belegen aber keine Lernqualität.
- `PRIN-014` bleibt als Quellen- und Governance-Randbedingung erhalten. Eine offene Rechtekette ist notwendig, belegt aber keine lernpsychologische Qualität.
- LXP03 bleibt eine konkrete historische Entwurfsevidenz. Die drei IUM5-Referenzsituationen helfen bei Gegenproben, wurden jedoch nicht mit Lernenden oder Lehrkräften erprobt und dürfen nicht zur allgemeinen Vorlage werden.

LXP05 selbst ist kein Pflichtartefakt des 33-teiligen Audits und wird nicht in die V2-Basis übernommen. Der Branch `origin/feat/lxp05-ium5-experience` bleibt eingefrorene, ungemergte Implementierungs- und Regressionsevidenz.

## Entfallende Regeln

Kein vollständiges Pflichtartefakt erhält die Entscheidung `drop`. Folgende implizite Regeln entfallen dennoch verbindlich:

- Eine schriftlich freigegebene Spezifikation ist noch kein Nachweis für Nutzbarkeit oder Lernwirkung.
- Schema-, Type-, Build-, Accessibility- oder Contract-Vollständigkeit erhöht keinen fachlichen, didaktischen oder Pilot-Reifegrad.
- Ein Methodenname wie Retrieval, Scaffolding, Productive Failure oder Selbsterklärung genügt nicht ohne Mechanismus, Randbedingungen und passende Prüfung.
- Eine einzige IUM5-Komposition begründet weder elf globale Lernzustände noch eine globale Patternbibliothek.
- Das Evidenzprodukt darf nicht automatisch zum Lernprodukt werden.
- Eine lange Lehrkraftbeschreibung ersetzt keine zeitlich, organisatorisch und fachlich ausführbare Orchestrierung.
- Lernende der Klassen 5 bis 7 werden nicht als homogene Gruppe mit gleicher Lese-, Bedien-, Selbstregulations- oder Explorationserfahrung modelliert.

## Querschnittliche Ursachen des LXP05-Fehlschlags

| Ebene | Befund | Konsequenz |
|---|---|---|
| Evidenzschwäche | Die 13 Claims sind quellengeprüft, aber ihre Übertragung auf IuM 5–7 bleibt teilweise inferenziell. Die sechs LXP01-Ergänzungen sind registriert, jedoch noch keine geprüften V2-Claims. | LXF02 schließt Quellen-, Claim-, Mechanismus- und Geltungsgrenzen vor jeder neuen Designnorm. |
| Übersetzungsschwäche | Aus vorsichtigen Claims wurden umfangreiche Prinzipien, Zustände und Produktionsverträge, ohne jede Entscheidung mit Mechanismus, Randbedingung, beobachtbarem Kriterium und eigener Prüfart zu schließen. | LXF04 leitet einen prüfbaren Evidence-to-Design-Vertrag erst nach LXF02 und LXF03 ab. |
| Implementierungsschwäche | Der Kandidat materialisierte Vertragsvollständigkeit als Gesamtoberfläche: parallele Phasenmodelle, hohe Informations- und Formularlast, dominantes Evidenzprodukt und beschreibende Lehrkraftspur. | LXF05/LXF06 begrenzen Informationsbudget, Komposition, Lernprodukt und reale Lehrkraftaktionen vor neuer Implementierung. |
| Fehlende Pilotevidenz | Weder die Referenzentwürfe noch der Kandidat wurden im realen Unterricht mit Lernenden und Lehrkräften der Zielstufen belastbar geprüft. | Technische Tests bleiben technisch. LXF06 definiert getrennte Beobachtungs-, Usability-, Accessibility- und Unterrichtsgates; Pilotierung braucht eine spätere Freigabe. |

Der Fehlschlag liegt damit nicht in einer einzigen falschen Farbe, Komponente oder Methode. Er entstand an der Kette zwischen Evidenz, Übersetzung, Komposition und fehlender Erprobung. V2 muss diese vier Ebenen getrennt schließen.

## Übergabe an LXF02

LXF02 erhält ausschließlich den Auftrag, den Evidenzvertrag zu konsolidieren:

1. die 13 bestehenden Lernpsychologie-Claims mit ihren primär geprüften Quellen in das V2-Claimmodell überführen;
2. die sechs in IUM-V2-SRC registrierten LXP01-Quellen inhaltlich prüfen und nur bei tragfähiger Aussage als V2-Claims aufnehmen;
3. je Claim Mechanismus, Lernendenkontext, Randbedingungen, Designimplikation, beobachtbare Kriterien, Outcome und geeignete Prüfart trennen;
4. schwache Alters- oder IuM-Übertragungen sichtbar lassen und an LXF03 oder spätere Pilotgates binden;
5. keine Prinzipien, Komponenten, Materialien oder Inhalte produzieren.

Bis zur ausdrücklichen Abnahme dieses Audits bleiben LXF02, LXF03–LXF07, Inhaltsproduktion, LXP05-Integration, Pilotierung, Veröffentlichung und V2-Cutover geschlossen.
