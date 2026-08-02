import { describe, expect, test } from 'vitest';
import {
  validateLearningState,
  validateModuleManifest,
} from '../../packages/module-contract/src/index.js';

function validManifest() {
  return {
    schemaVersion: 1,
    id: 'TEST-PLATFORM-REFERENCE',
    version: '1.0.0',
    title: 'Technische Referenz',
    status: 'draft',
    grade: 5,
    kind: 'core',
    strands: ['TEST-STRAND'],
    time: {
      minLessons: 1,
      maxLessons: 1,
      contractId: 'TEST-TIME-001',
    },
    prerequisites: [],
    curriculum: {
      competencyIds: ['TEST-COMP-001'],
      coverageEvidenceIds: ['TEST-COV-001'],
    },
    learningDesign: {
      centralQuestion: 'Technische Frage',
      goals: ['Technischen Zustand prüfen'],
      actions: ['Synthetische Eingabe ändern'],
      product: 'Synthetischer Zustand',
      misconceptions: [],
      scaffolds: [],
    },
    components: ['fixture-workspace'],
    media: {
      digitalFunction: 'Technischen Zustandsfluss prüfen',
      analogMaterials: [],
    },
    data: {
      stateSchemaVersion: 1,
      fields: ['text', 'choice'],
      exportable: true,
      deletable: true,
    },
    offline: { core: true, externalResources: [] },
    accessibility: {
      alternatives: [],
      manualChecks: ['keyboard', 'screenreader'],
    },
    licenses: {
      content: 'CC-BY-SA-4.0',
      code: 'MIT',
      assetEvidencePath: 'assets/licenses.json',
    },
    quality: { evidenceRefs: [] },
  };
}

describe('closed Phase-1 contracts', () => {
  test('rejects unknown manifest fields', () => {
    const result = validateModuleManifest({
      ...validManifest(),
      unexpected: true,
    });
    expect(result.ok).toBe(false);
  });

  test('rejects a maximum below the minimum lesson count', () => {
    const manifest = validManifest();
    manifest.time = { ...manifest.time, minLessons: 2, maxLessons: 1 };
    const result = validateModuleManifest(manifest);
    expect(result).toEqual({
      ok: false,
      issues: [
        {
          path: '/time/maxLessons',
          keyword: 'semantic',
          message: 'muss mindestens minLessons entsprechen',
        },
      ],
    });
  });

  test('rejects a state with identity fields', () => {
    const result = validateLearningState({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'TEST-PLATFORM-REFERENCE',
      moduleVersion: '1.0.0',
      stateSchemaVersion: 1,
      workspaceId: '123e4567-e89b-42d3-a456-426614174000',
      savedAt: '2026-08-03T12:00:00.000Z',
      payload: {},
      learnerName: 'Nicht erlaubt',
    });
    expect(result.ok).toBe(false);
  });
});
