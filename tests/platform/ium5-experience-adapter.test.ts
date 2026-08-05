import { describe, expect, test } from 'vitest';
import {
  createInitialPayload,
  projectPersistentPayload,
  type WorkbenchPayload,
} from '@ium/ium-5-core-05';
import { deriveIum5ExperienceState } from '../../apps/lernwerk-portal/src/controllers/algorithm-workbench/experience-adapter.js';

const algorithm = [{ id: 'cmd-1', kind: 'move' }] as const;
const prediction = {
  position: { column: 1, row: 2 },
  direction: 'north',
  success: 'unsure',
} as const;
const worldState = {
  position: { column: 1, row: 1 },
  direction: 'north',
  carrying: false,
  itemPosition: { column: 2, row: 2 },
  delivered: false,
} as const;
const trace = {
  scenarioId: 'worked-sequence',
  entries: [{
    step: 1,
    sourceCommandId: 'cmd-1',
    commandKind: 'move',
    loop: null,
    before: worldState,
    after: { ...worldState, position: { column: 1, row: 2 } },
    outcome: 'ok',
    error: null,
  }],
  finalState: { ...worldState, position: { column: 1, row: 2 } },
  missionSucceeded: false,
} as const;
const evidenceCard = {
  sourceRef: 'worked-sequence',
  evidenceRef: 'trace:first-deviation',
  interpretation: 'Die erste Abweichung zeigt die Ursache.',
  revision: 'Der fehlerhafte Schritt wird gezielt geändert.',
  keyStatement: 'Laufspuren begründen gezielte Revisionen.',
  modelBoundary: 'Die Aussage gilt für den geprüften deterministischen Ablauf.',
} as const;

function payload(overrides: Partial<WorkbenchPayload>): WorkbenchPayload {
  return projectPersistentPayload({ ...createInitialPayload(), ...overrides });
}

describe('IUM5 experience stage truth table', () => {
  test.each([
    ['start', payload({})],
    ['prediction', payload({ initialAlgorithm: algorithm })],
    ['run', payload({ initialAlgorithm: algorithm, prediction })],
    ['evidence', payload({ initialAlgorithm: algorithm, prediction, evidenceTrace: trace })],
    ['revision', payload({ initialAlgorithm: algorithm, prediction, evidenceTrace: trace, repairSource: 'own-draft', repairHypothesis: 'Der erste Schritt weicht ab.' })],
    ['transfer', payload({ initialAlgorithm: algorithm, prediction, evidenceTrace: trace, repairSource: 'own-draft', repairHypothesis: 'Der erste Schritt weicht ab.', revisedAlgorithm: algorithm })],
    ['reentry', payload({ initialAlgorithm: algorithm, prediction, evidenceTrace: trace, repairSource: 'own-draft', repairHypothesis: 'Der erste Schritt weicht ab.', revisedAlgorithm: algorithm, evidenceCard, systemClassifications: [{ caseId: 'navigation', classification: 'algorithmic', rationale: 'Feste Schritte verarbeiten die Eingabe.' }] })],
  ] as const)('derives %s without a persisted stage field', (expected, value) => {
    expect(deriveIum5ExperienceState(value).stage).toBe(expected);
    expect(value).not.toHaveProperty('stage');
  });

  test('represents resume, persistence, validation and import facts separately', () => {
    const value = payload({ initialAlgorithm: algorithm });

    expect(deriveIum5ExperienceState(value, { hasStoredState: true }).canResume).toBe(true);
    expect(deriveIum5ExperienceState(value, { persistenceAvailable: false }).recovery).toBe('storage');
    expect(deriveIum5ExperienceState(value, { validationFailed: true }).recovery).toBe('validation');
    expect(deriveIum5ExperienceState(value, { importFailed: true }).recovery).toBe('import');
    expect(deriveIum5ExperienceState(value, { connectivity: 'offline' }).connectivity).toBe('offline');
  });

  test('does not mutate the core payload', () => {
    const value = payload({ initialAlgorithm: algorithm, prediction });
    const before = structuredClone(value);

    deriveIum5ExperienceState(value, { hasStoredState: true, saveState: 'saving' });

    expect(value).toEqual(before);
  });
});
