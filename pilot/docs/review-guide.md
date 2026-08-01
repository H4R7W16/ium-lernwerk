# Reviewanleitung zum IUM11-Pilotinstrument

## Aussagegrenze und Prüfgegenstand

Geprüft wird das IUM11-Instrument für 40 UE, 4 Cluster, 10 Module und 5 Pilotstufen mit Protokollversion `1.0.0` und Werkzeugversion `1.0.0`. Ein positiver Minimalpilot trägt ausschließlich die Aussage `documented-conditions-only` und höchstens die Empfehlung `eligible-for-working-availability-review`. Die drei folgenden Gates werden personell und protokollarisch getrennt entschieden.

## Gate 1: Fachreview

Das Fachreview beantwortet für jeden Cluster, jedes Modul und den Jahreslauf:

- Bleiben Curriculumstatus und normative Gewichtung sichtbar, ohne Orientierungstexte aufzuwerten?
- Entspricht die Operatorentiefe der geforderten Lernhandlung?
- Ist die Ankerhandlung fachlich zentral und im vorgesehenen Zeitbudget beobachtbar?
- Verkörpert das Lernprodukt die geforderte Leistung, ohne selbst als personenbezogener Zeitnachweis exportiert zu werden?
- Sind Übung und fachliches Feedback so angelegt, dass eine begründete Revision folgt?
- Gibt es eine fachlich tragfähige Sicherung und einen eigenständigen Transfer?
- Bleibt die Übergabekontinuität zwischen Produkt, nächstem Cluster und Jahreslauf funktional erhalten?
- Sind flexible Vertiefungs-, Transfer- und Projektmodule sichtbar erhalten, ohne Kernzeit oder eine gescheiterte Integration zu kompensieren?

Das Fachreview prüft keine Einzelpersonen und erhält keine Rohprodukte oder Lernendenantworten. Offene fachliche Muss-Befunde verhindern das Gate.

## Gate 2: Engineering-/Privacyreview

Das Engineering-/Privacyreview prüft gemeinsam, aber getrennt dokumentiert:

- rekursiv geschlossene Evidenz- und Entscheidungsschemas;
- Protokoll-, Werkzeug- und Zeitmodellfingerprints sowie versionsgleiche Imports;
- Offlinebetrieb und No-Persistence ohne Backend, Konto, Netzwerk, Cookie, Telemetrie oder Browserspeicher;
- Abwesenheit verbotener Felder, Rohprodukte, Links, Freitexte und Einzelantworten;
- Unterdrückung unter der Privacy-Schwelle 10 und die ganzzahlige Warnschwelle;
- harte Clusterbudgets und ausschließlich additive Rückfallbedarfe;
- Privacy-Exportblockade und fail-closed Fehlerwege;
- Tastaturbedienung, Fokus, Fehlerresümee, Live-Status, Reflow, Kontrast und mindestens 44 × 44 CSS-Pixel große Bedienziele;
- die aktuelle Browserbaseline und lokale Dateiabläufe für Import, Prüfung und Download;
- Synchronität von Protokoll `1.0.0`, Werkzeug `1.0.0`, Schemas, Code, Anleitungen, 40 UE, 4 Clustern, 10 Modulen und 5 Stufen.

Ein offener Engineering-, Privacy- oder Accessibilitybefund verhindert das Gate.

## Gate 3: Auftraggebergate

Das Auftraggebergate erhält nur validierte Klassenaggregate, das Entscheidungspaket und die getrennten Reviewurteile. Bei positivem Minimalpilot sind als spätere, ausdrücklich zu beschließende Änderungen genau zulässig:

- `availabilityStatus: available`
- `timeFeasibilityStatus: green`
- `pilotStatus: completed`

Das Instrument mutiert diese Werte nicht. Die Achsen `status: working` und `semanticCoverageStatus: partial` bleiben unverändert. Die Minimalpilotaussage bleibt `documented-conditions-only`; sie ist keine allgemeine Wirksamkeits- oder Reifeaussage.

`reviewed` und `standard` bleiben gesperrt. Für eine spätere Reifeentscheidung ist mindestens eine zweite unabhängige End-to-End-Jahresdurchführung unter den dann dokumentierten Bedingungen sowie ein erneutes Fachreview, Engineering-/Privacyreview und Auftraggebergate erforderlich.

## Retention und Veröffentlichung nach der Entscheidung

Bis zur Auftraggeberentscheidung bleiben reale Pakete nichtöffentlich und zugriffsbeschränkt außerhalb des Repositorys. Nach der Entscheidung werden sie und lokale Zuordnungen gelöscht, sofern keine abweichende institutionelle Pflicht besteht. Veröffentlicht werden nur Protokoll, Schemas, Instrument, Anleitungen, Reviewurteile ohne personenbezogene Inhalte und ausdrücklich synthetische Beispiele. Eine Veröffentlichung behauptet weder eine reale Pilotdurchführung noch eine automatische Statusänderung.
