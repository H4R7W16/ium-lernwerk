# IuM-Lernwerk

Offenes, digitales Lernwerk für Informatik und Medienbildung am Gymnasium in Baden-Württemberg, Klassen 5 bis 7. Der Lernwerk-Kosmos verbindet verbindliche Kernpfade mit ausdrücklich erhaltenen Vertiefungs-, Transfer- und Projektmodulen.

## Phase 0: validierte Grundlage

Phase 0 umfasst Forschungsbasis, Curriculumdaten, Fachprofil, Modulverträge, Coverageaudit und das IUM10-Zeitmodell. Eine Lernendenanwendung und die Planung von Phase 1 gehören noch nicht zu diesem Stand.

Das IUM10-Zeitmodell hat den Status `working`. [roadmap/time-model.json](roadmap/time-model.json) ist die kanonische Quelle mit Schema 3; [roadmap/module-roadmap.md](roadmap/module-roadmap.md) ist die daraus abgeleitete Lesefassung. Die vollständigen Jahresvarianten und Referenzrechnungen sind daraus projiziert:

### Zeitmodell in Zahlen

| Klasse | Verfügbare Pfade (UE) | Bedarf ohne Angebot (UE) | Zeiturteil |
| --- | --- | --- | --- |
| 5 | 30/34/38 | — | green |
| 6 | 30/34/38/38/38 | — | green |
| 7 | — | 46/54 | amber |

Die drei 38-UE-Pfade der Klasse 6 bilden unterschiedliche Erweiterungen ab. Für Klasse 7 ist `GRADE-7-WORKING-40` ein `working`-Arbeitsziel mit `conditional`-Verfügbarkeit und `amber`-Zeitmachbarkeit; die 46- und 54-UE-Pfade sind `unavailable`/`red` und ausschließlich Referenzrechnungen, keine Ersatzangebote.

Status: **Auftraggeber-Zeitfreigabe ausstehend**. `working` ist der Status der 40-UE-Jahresvariante und bedeutet weder `available` noch `reviewed` oder zeitlich freigegeben. Die fünf Urteilachsen werden in dieser Reihenfolge ausgewiesen: Verfügbarkeit, Zeitmachbarkeit, Sequenznachweis, Pilotstatus, semantische Coverage.

- Klasse 5: available / green / covered / not-started / partial
- Klasse 6: available / green / covered / not-started / covered
- Klasse 7: conditional / amber / covered / not-started / partial

Klasse 7 bleibt nur unter dem Working-40-Vertrag bedingt: fünf Gates (`capacity`, `integration`, `technical`, `privacy`, `pilot`) sowie vier Integrationspiloten und ein Jahrespfadpilot sind noch nicht abgeschlossen. Ein gescheitertes erforderliches Gate führt fail-closed zu `unavailable`/`red`. Die additive Rückfallrechnung lautet `40 + 3 + 2 + 3 + 6 = 54`; 38 UE sind lediglich eine nichtnormative Vergleichsgrenze, keine Klasse-7-Jahresvariante.

Die 36 privacy-sicheren Pilotaufträge bleiben aggregiert: 31 Modulaufträge, vier Integrationsaufträge und ein Jahrespfadauftrag. Private Reflexion, persönliche Telemetrie und Schülerprodukte als Zeitnachweis sind ausgeschlossen; `handoffProductPresent` ist nur ein aggregierter Ja/Nein-Befund und allein kein positiver Zeitnachweis.

Die übrigen IUM10-Achsen bleiben ebenfalls getrennt beurteilt:

- aktuelle IUM10-Coverage: 166 `covered` / 5 `partial`;
- historische IUM09-Projektion: 164 `covered` / 7 `partial`;
- 60/60 Zeitreviews und 4/4 Sequenznachweise sind dokumentiert;
- Pilotaufträge bleiben auf Modul-, Integrations- oder Jahrespfadebene aggregiert und nichtpersonal, ohne persönliche Diagnostik oder Telemetrie.

In der historischen IUM09-Projektion gilt weiterhin: 164 sind auf Kandidatenebene `covered`, 7 bleiben `partial`. Von 60 Ausgangslücken wurden 53 geschlossen; 7 bleiben im Ledger offen. Trotz der verbesserten semantischen Coverage ist das Lernwerk weiterhin zeitlich nicht freigegeben.

Flexible Vertiefungs-, Transfer- und Projektmodule bleiben zusätzlich außerhalb der 40 UE sichtbar und ersetzen weder fehlende Kernzeit noch gescheiterte Kernintegrationen. Digital ist das selbstverständliche Unterrichtsmedium; analoge Materialien werden nur eingesetzt, wenn die Lernhandlung ihre Verwendung didaktisch begründet. Eine zwanghafte Doppelstruktur ist nicht vorgesehen.

## IUM11-Pilotinstrument

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

IUM11 veröffentlicht ein lokales, privacy-sicheres Entwicklungsinstrument für den Klasse-7-Kernpfad. Die verbindlichen, automatisch erzeugten Fakten stehen im vorstehenden Faktenblock. Das Instrument und seine Beispiele sind synthetisch geprüft; dies ist keine reale Pilotierung und keine Statushochsetzung.

- [Pilotprotokoll](pilot/pilot-protocol.json)
- [Lokales Offline-Cockpit](pilot/cockpit/index.html)
- [Lehrkräfteanleitung](pilot/docs/teacher-guide.md)
- [Reviewanleitung](pilot/docs/review-guide.md)
- [IUM11-Validator](scripts/validate_ium11.py)

Das Cockpit wird direkt lokal geöffnet, verarbeitet nur Klassenaggregate im Arbeitsspeicher und speichert erst durch einen bewussten JSON-Download. Kleine Gruppen werden unterdrückt und exportieren keine Lernendenzählwerte. Reale Evidenz- und Entscheidungspakete bleiben außerhalb dieses öffentlichen Repositorys. Die verbindlichen Urteilachsen werden nicht durch das Instrument verändert.

<!-- IUM11-PUBLICATION-SCOPE:END -->

## Zentrale Einstiege

- [Validierte Modulroadmap](roadmap/module-roadmap.md)
- [Autoritatives IUM10-Zeitmodell](roadmap/time-model.json)
- [Recordgenauer Abdeckungsplan](roadmap/coverage-plan.json)
- [IUM10-Validator](scripts/validate_ium10.py)
- [IUM09-Validator](scripts/validate_ium09.py)
- [Gesamtvalidator Phase 0](scripts/validate_phase0.py)
- [Fachprofil Gymnasium 5–7](docs/fachprofil/ium-gymnasium-5-7.md)
- [Curriculum-Crosswalk](curriculum/crosswalk.json) und [begründete Progression](curriculum/progression.md)
- [Forschungsarchitektur](docs/research/phase-0/README.md) und [Forschungssynthese](docs/research/phase-0/synthesis.md)
- [Verbindliche Gesamtspezifikation](docs/superpowers/specs/2026-07-27-ium-lernwerk-gesamtdesign.md)

IUM10 ist nicht `reviewed`; eine Zeitfreigabe ist nicht erteilt. Phase 1 bleibt bis zu einem gesonderten Nutzerentscheid ungeplant.

## Validierung

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
python -B scripts/build_ium11_cockpit.py --check
node --check pilot/cockpit/assets/app.js
python -B scripts/build_ium11_publication_contract.py --check
python -B scripts/validate_ium11.py
python -B scripts/validate_ium10.py
python -B scripts/validate_ium09.py
python -B scripts/validate_phase0.py
```

## Lizenzen

Eigener Validierungscode steht unter der [MIT-Lizenz](LICENSE). Eigene inhaltliche Repository-Beiträge stehen unter [CC BY-SA 4.0](LICENSE-CONTENT.md), sofern eine Datei nicht ausdrücklich etwas anderes festlegt. Material Dritter behält seine jeweils ausgewiesene Lizenz.
