import { describe, expect, test } from 'vitest';
import {
  createInitialPayload,
  parseWorkbenchPayload,
  projectPersistentPayload,
} from '../../packages/ium-5-core-05/src/index.js';

const allowed = [
  'phaseId',
  'scenarioId',
  'initialAlgorithm',
  'prediction',
  'evidenceTrace',
  'repairSource',
  'repairHypothesis',
  'revisedAlgorithm',
  'loopDecision',
  'systemClassifications',
  'selfCheck',
].sort();

describe('workbench payload', () => {
  test('starts with only the agreed product fields', () => {
    expect(Object.keys(createInitialPayload()).sort()).toEqual(allowed);
    expect(createInitialPayload()).toMatchObject({
      phaseId: 'ue1-orientation',
      scenarioId: 'worked-sequence',
      initialAlgorithm: [],
      prediction: null,
      evidenceTrace: null,
      repairSource: null,
      repairHypothesis: '',
      revisedAlgorithm: null,
      loopDecision: '',
      systemClassifications: [],
      selfCheck: {
        unambiguous: 'review',
        traceMatches: 'review',
        repairJustified: 'review',
        loopAppropriate: 'review',
      },
    });
  });

  test.each([
    'elapsedMs',
    'attemptCount',
    'clicks',
    'hintUsage',
    'playbackSpeed',
    'name',
  ])('rejects forbidden field %s', (field) => {
    const payload = { ...createInitialPayload(), [field]: 1 };
    expect(parseWorkbenchPayload(payload).ok).toBe(false);
  });

  test('limits explanations by Unicode code point instead of UTF-16 unit', () => {
    const valid = {
      ...createInitialPayload(),
      repairHypothesis: '🧭'.repeat(500),
    };
    const invalid = {
      ...createInitialPayload(),
      repairHypothesis: '🧭'.repeat(501),
    };
    expect(parseWorkbenchPayload(valid).ok).toBe(true);
    expect(parseWorkbenchPayload(invalid).ok).toBe(false);
  });

  test('returns a deep copy and never carries transient execution state', () => {
    const source = {
      ...createInitialPayload(),
      initialAlgorithm: [{ id: 'cmd-1', kind: 'move' }],
      transientTrace: [{ step: 1 }],
    };
    const projected = projectPersistentPayload(source);

    expect(Object.keys(projected).sort()).toEqual(allowed);
    expect(projected).not.toBe(source);
    expect(projected.initialAlgorithm).not.toBe(source.initialAlgorithm);
    expect(projected).not.toHaveProperty('transientTrace');
  });

  test('rejects a future or malformed module payload without coercion', () => {
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      phaseId: 'future-phase',
    }).ok).toBe(false);
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      initialAlgorithm: 'move',
    }).ok).toBe(false);
  });

  test('rejects identifiers outside the closed content contract', () => {
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      scenarioId: 'unknown',
    }).ok).toBe(false);
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      systemClassifications: [{
        caseId: 'unknown',
        classification: 'algorithmic',
        rationale: 'Begründung',
      }],
    }).ok).toBe(false);
  });

  test('rejects unknown nested fields and duplicate transfer cases', () => {
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      prediction: {
        position: { column: 1, row: 1 },
        direction: 'east',
        success: 'yes',
        confidence: 1,
      },
    }).ok).toBe(false);
    const classification = {
      caseId: 'navigation',
      classification: 'algorithmic',
      rationale: 'Feste Verarbeitungsschritte',
    };
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      systemClassifications: [classification, classification],
    }).ok).toBe(false);
  });

  test('rejects evidence beyond the hard execution limit', () => {
    const worldState = {
      position: { column: 1, row: 1 },
      direction: 'east' as const,
      carrying: false,
      itemPosition: { column: 1, row: 1 },
      delivered: false,
    };
    const evidenceTrace = {
      scenarioId: 'worked-sequence',
      entries: Array.from({ length: 102 }, (_, index) => ({
        step: index + 1,
        sourceCommandId: 'cmd-1',
        commandKind: 'turn-left',
        loop: null,
        before: worldState,
        after: worldState,
        outcome: 'ok',
        error: null,
      })),
      finalState: worldState,
      missionSucceeded: false,
    };
    expect(parseWorkbenchPayload({
      ...createInitialPayload(),
      evidenceTrace,
    }).ok).toBe(false);
  });

  test('accepts a closed populated product trace', () => {
    const worldState = {
      position: { column: 1, row: 1 },
      direction: 'east',
      carrying: false,
      itemPosition: { column: 1, row: 1 },
      delivered: false,
    };
    const result = parseWorkbenchPayload({
      ...createInitialPayload(),
      prediction: {
        position: { column: 1, row: 1 },
        direction: 'east',
        success: 'unsure',
      },
      evidenceTrace: {
        scenarioId: 'worked-sequence',
        entries: [{
          step: 1,
          sourceCommandId: 'cmd-1',
          commandKind: 'turn-left',
          loop: null,
          before: worldState,
          after: { ...worldState, direction: 'north' },
          outcome: 'ok',
          error: null,
        }],
        finalState: { ...worldState, direction: 'north' },
        missionSucceeded: false,
      },
      repairSource: 'own-draft',
      repairHypothesis: 'Die erste Drehung zeigt in die falsche Richtung.',
      revisedAlgorithm: [{ id: 'cmd-1', kind: 'turn-right' }],
      loopDecision: 'Keine feste Wiederholung nötig.',
      systemClassifications: [{
        caseId: 'navigation',
        classification: 'algorithmic',
        rationale: 'Die Eingabe wird nach festgelegten Schritten verarbeitet.',
      }],
      selfCheck: {
        unambiguous: 'yes',
        traceMatches: 'yes',
        repairJustified: 'yes',
        loopAppropriate: 'not-applicable',
      },
    });

    expect(result.ok).toBe(true);
  });
});
