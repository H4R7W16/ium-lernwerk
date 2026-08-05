# IUM5 Learning-Experience-Akzeptanzmatrix

Status: interner `working`-Implementierungsstand am LXP05-Reviewgate. Diese Matrix belegt automatisierte Vertrags- und Regressionsprüfungen, keine Lernwirkung, vollständige WCAG-Konformität, Realgeräteprüfung oder Unterrichtsfreigabe.

## Vertragsstand

- Inhaltsvertrag: `ExperienceContentV1`, `schemaVersion: 1`, Terminologie `lxp04-1`.
- Komponentenvertrag: semantische Komponenten unter `@ium/learning-experience`; IUM5 bleibt Kompositions- und Fachadapter.
- Zustandsvertrag: IUM5 `stateSchemaVersion 2`; ältere valide Stände migrieren explizit von `stateSchemaVersion 1 → 2` und erhalten deterministisch `evidenceCard: null`.
- Speicherung: ausschließlich IndexedDB über `@ium/local-state`, nutzergesteuerter JSON-Export und modulbezogen bestätigtes Löschen.

## Drei Referenzsituationen

| Situation | Implementierung | Automatisierte Evidenz |
| --- | --- | --- |
| Start und Fortsetzen | `StartBoard`, `ResumePrompt`, lokale Recovery | `npm run test:ium5:state`; `ium5-start-resume.spec.ts` |
| Vorhersage, Beleg und Revision | `PredictionForm`, `EvidenceView`, `EvidenceFeedback`, `RevisionCompare` | `ium5-evidence-revision.spec.ts`; `learning-feedback-contract.test.ts` |
| Belegkarte, Transfer und Wiedereinstieg | `EvidenceCardComposer`, `TransferPrompt`, `ReentryRecall` | `ium5-transfer-reentry.spec.ts`; `ium5-payload.test.ts` |

## Qualitätsnachweise

| Bereich | Exakte Prüfung | Aussagegrenze |
| --- | --- | --- |
| Inhaltsverträge | `npm run contracts:check`; `ium5-experience-content.test.ts` | geschlossenes JSON und Referenzen |
| Paketgrenzen | `npm run boundaries:check`; `learning-experience-production.test.ts` | gerichtete Abhängigkeiten, keine DOM-Fachkernkopplung |
| Semantik und Kontrast | `learning-experience-styles.test.ts`; `npm run test:ium5:accessibility` | automatisierbare Baseline, kein vollständiger manueller WCAG-Nachweis |
| Local First und Migration | `ium5-payload.test.ts`; `npm run test:ium5:state`; `npm run test:ium5:offline` | lokale Persistenz, Export/Import, Offlinepfad |
| Lehrkraftorchestrierung | `ium5-teacher-orchestration.test.ts`; `ium5-teacher-orchestration.spec.ts` | lokale Haltepunkte ohne Konto, Fernsteuerung oder Telemetrie |
| Produktionsgate | `npm run verify:experience`; `npm run verify:ium5` | technische Reviewbereitschaft, keine Einsatzfreigabe |

## Nicht-Generalisierungen

Das IUM5-Raster, der grafische Editor, der Befehlskatalog, die Laufspursemantik, die Szenario-IDs und die fachliche Sprache bleiben im IUM5-Kern beziehungsweise Portaladapter. Auch die Checkpoint-Platzierung ist eine IUM5-Kompositionsentscheidung. Das generische Paket stellt dafür nur semantische Rollen und lokale Interaktionsmuster bereit.
