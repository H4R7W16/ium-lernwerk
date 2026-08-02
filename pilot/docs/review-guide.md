# Reviewanleitung zum IUM11-Pilotinstrument

<!-- IUM11-PUBLICATION-CONTRACT:START -->
<!-- Generiert aus Pilotprotokoll und Zeitmodell; nicht manuell bearbeiten. -->
| Bereich | Verbindliche Fakten |
| --- | --- |
| Vertragsbindung | schemaVersion: 1; id: IUM11-PUBLICATION-CONTRACT; contractVersion: 1.0.0; protocolPath: pilot/pilot-protocol.json; timeModelPath: roadmap/time-model.json; protocolVersion: 1.0.0; toolVersion: 1.0.0; timeModelFingerprintAlgorithm: sha256-canonical-json-v1; timeModelFingerprint: 873774e52b6c9a20e08e5079c898a014493a39305be5efa35a601248ff36a2c1 |
| Kernpfad | variantId: GRADE-7-WORKING-40; targetUnits: 40; clusterCount: 4; moduleCount: 10; pilotStageCount: 5 |
| Clusterbudgets und Rückfälle | id: CLUSTER-7-DATA-CODING; order: 1; budgetUnits: 8; fallbackDeltaUnits: 3; id: CLUSTER-7-PROGRAMMING; order: 2; budgetUnits: 11; fallbackDeltaUnits: 2; id: CLUSTER-7-NET-SECURITY; order: 3; budgetUnits: 11; fallbackDeltaUnits: 3; id: CLUSTER-7-DATA-MEDIA-SOCIETY; order: 4; budgetUnits: 10; fallbackDeltaUnits: 6 |
| Privacygrenze | minimumLearnerResponses: 10; personalDataAllowed: false; realPackagesInRepositoryAllowed: false |
| Aktuelle Urteilachsen | status: working; availabilityStatus: conditional; timeFeasibilityStatus: amber; sequenceEvidenceStatus: covered; pilotStatus: not-started; semanticCoverageStatus: partial |
| Aussagegrenze | statementBoundary: documented-conditions-only |
| Zulässige Empfehlung | allowedRecommendation: eligible-for-working-availability-review |
| Gesperrte Reifegrade | forbiddenMaturityValues: reviewed; forbiddenMaturityValues: standard |
| Spätere Auftraggeberentscheidung | requiresCommissionerDecision: true; secondIndependentAnnualRunRequiredForMaturity: true; allowedChanges: availabilityStatus: available; allowedChanges: timeFeasibilityStatus: green; allowedChanges: pilotStatus: completed; unchangedAxes: status: working; unchangedAxes: semanticCoverageStatus: partial |
| Reale Pilotierung | realPilotCompleted: false; syntheticValidationOnly: true |
| Flexible Module | flexibleModulesOutsideCorePreserved: true; flexibleModuleSubstitution: forbidden; Flexible Vertiefungs-, Transfer- und Projektmodule bleiben sichtbar erhalten. |
<!-- IUM11-PUBLICATION-CONTRACT:END -->

## Aussagegrenze und Prüfgegenstand

Geprüft wird das IUM11-Instrument unter den verbindlichen Bedingungen des automatisch erzeugten Faktenblocks. Ein positiver Minimalpilot ist keine allgemeine Wirksamkeits- oder Reifeaussage. Die folgenden Gates werden personell und protokollarisch getrennt entschieden.

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
- Unterdrückung kleiner Gruppen und die ganzzahlige Warnschwelle;
- harte Clusterbudgets und ausschließlich additive Rückfallbedarfe;
- Privacy-Exportblockade und fail-closed Fehlerwege;
- Tastaturbedienung, Fokus, Fehlerresümee, Live-Status, Reflow, Kontrast und mindestens 44 × 44 CSS-Pixel große Bedienziele;
- die aktuelle Browserbaseline und lokale Dateiabläufe für Import, Prüfung und Download;
- Synchronität von Protokoll, Werkzeug, Schemas, Code und Anleitungen mit dem Faktenblock.

Ein offener Engineering-, Privacy- oder Accessibilitybefund verhindert das Gate.

## Gate 3: Auftraggebergate

Das Auftraggebergate erhält nur validierte Klassenaggregate, das Entscheidungspaket und die getrennten Reviewurteile. Die ausschließlich später und ausdrücklich zu beschließenden Änderungen sowie die unveränderlichen Achsen stehen im Faktenblock.

Das Instrument mutiert diese Werte nicht. Für eine spätere Reifeentscheidung ist mindestens eine zweite unabhängige End-to-End-Jahresdurchführung unter den dann dokumentierten Bedingungen sowie ein erneutes Fachreview, Engineering-/Privacyreview und Auftraggebergate erforderlich.

## Retention und Veröffentlichung nach der Entscheidung

Bis zur Auftraggeberentscheidung bleiben reale Pakete nichtöffentlich und zugriffsbeschränkt außerhalb des Repositorys. Nach der Entscheidung werden sie und lokale Zuordnungen gelöscht, sofern keine abweichende institutionelle Pflicht besteht. Veröffentlicht werden nur Protokoll, Schemas, Instrument, Anleitungen, Reviewurteile ohne personenbezogene Inhalte und ausdrücklich synthetische Beispiele. Eine Veröffentlichung behauptet weder eine reale Pilotdurchführung noch eine automatische Statusänderung.
