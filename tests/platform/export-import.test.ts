import { expect, test } from 'vitest';
import type { LearningStateEnvelope } from '../../packages/module-contract/src/index.js';
import {
  parseImport,
  serializeState,
  stateExportFilename,
} from '../../packages/export-import/src/index.js';

function state(
  overrides: Partial<LearningStateEnvelope> = {},
): LearningStateEnvelope {
  return {
    format: 'ium-learning-state',
    formatVersion: 1,
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    stateSchemaVersion: 1,
    workspaceId: '123e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-08-03T12:00:00.000Z',
    payload: { choice: 'a', text: 'Probe' },
    ...overrides,
  };
}

test('rejects input over exactly 5 MiB without parsing', () => {
  const bytes = new Uint8Array(5 * 1024 * 1024 + 1);
  expect(parseImport(bytes, 'TEST-PLATFORM-REFERENCE')).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_TOO_LARGE' }),
  });
});

test('serializes deterministic UTF-8 JSON with one final LF', () => {
  const text = new TextDecoder().decode(serializeState(state()));
  expect(text).toBe(`${JSON.stringify(state(), null, 2)}\n`);
  expect(text.endsWith('\n\n')).toBe(false);
});

test('export filename contains no workspace identity', () => {
  const filename = stateExportFilename(state());
  expect(filename).toBe('ium-test-platform-reference-2026-08-03.json');
  expect(filename).not.toContain('123e4567');
});

test('parses a valid state into a non-HTML preview', () => {
  const result = parseImport(
    serializeState(state()),
    'TEST-PLATFORM-REFERENCE',
  );
  expect(result).toEqual({
    ok: true,
    state: state(),
    preview: {
      moduleId: 'TEST-PLATFORM-REFERENCE',
      moduleVersion: '1.0.0',
      savedAt: '2026-08-03T12:00:00.000Z',
      payloadFields: ['choice', 'text'],
    },
  });
});
