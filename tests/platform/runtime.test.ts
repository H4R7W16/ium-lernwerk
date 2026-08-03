import { expect, test } from 'vitest';
import type {
  ExportPort,
  LearningStateEnvelope,
} from '../../packages/module-contract/src/index.js';
import { serializeState } from '../../packages/export-import/src/index.js';
import { MemoryStateRepository } from '../../packages/local-state/src/index.js';
import {
  createModuleRuntime,
  type StateMigration,
} from '../../packages/module-runtime/src/index.js';

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
    payload: { text: 'alt' },
    ...overrides,
  };
}

function createRuntime(
  repository: MemoryStateRepository,
  migrations: readonly StateMigration[] = [],
  exportPort?: ExportPort,
) {
  return createModuleRuntime({
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    targetStateSchemaVersion: migrations.length === 0 ? 1 : 2,
    repository,
    migrations,
    clock: { now: () => new Date('2026-08-03T13:00:00.000Z') },
    createWorkspaceId: () => '223e4567-e89b-42d3-a456-426614174000',
    ...(exportPort === undefined ? {} : { exportPort }),
  });
}

test('wrong-module import leaves repository unchanged', async () => {
  const repository = new MemoryStateRepository();
  const existingState = state();
  await repository.save(existingState);
  const runtime = createRuntime(repository);
  await runtime.start();
  const otherModuleState = state({ moduleId: 'TEST-OTHER-MODULE' });
  const result = runtime.previewImport(serializeState(otherModuleState));
  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_WRONG_MODULE' }),
  });
  expect(await repository.load(existingState.moduleId)).toEqual(existingState);
});

test('future module version import leaves repository unchanged', async () => {
  const repository = new MemoryStateRepository();
  const existingState = state();
  await repository.save(existingState);
  const runtime = createRuntime(repository);
  await runtime.start();
  const futureState = state({ moduleVersion: '2.0.0' });

  const result = runtime.previewImport(serializeState(futureState));

  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_UNSUPPORTED_VERSION' }),
  });
  expect(await repository.load(existingState.moduleId)).toEqual(existingState);
});

test('failed migration preserves the original state byte-for-byte', async () => {
  const original = state({ stateSchemaVersion: 1, payload: { text: 'alt' } });
  const repository = new MemoryStateRepository();
  await repository.save(original);
  const failingMigration: StateMigration = {
    from: 1,
    to: 2,
    migrate() {
      throw new Error('synthetic failure');
    },
  };

  const result = await createRuntime(repository, [failingMigration]).start();

  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'MIGRATION_FAILED' }),
  });
  expect(await repository.load(original.moduleId)).toEqual(original);
});

test('import changes storage only after explicit confirmation', async () => {
  const repository = new MemoryStateRepository();
  const original = state({ payload: { text: 'alt' } });
  const imported = state({
    workspaceId: '323e4567-e89b-42d3-a456-426614174000',
    payload: { text: 'neu' },
  });
  await repository.save(original);
  const runtime = createRuntime(repository);
  await runtime.start();

  expect(runtime.previewImport(serializeState(imported)).ok).toBe(true);
  expect(await repository.load(original.moduleId)).toEqual(original);
  expect(await runtime.confirmImport()).toEqual({
    ok: true,
    state: imported,
    mode: 'volatile-selected',
  });
  expect(await repository.load(original.moduleId)).toEqual(imported);
});

test('blocked download falls back to the same copyable JSON', async () => {
  const repository = new MemoryStateRepository();
  const activeState = state();
  await repository.save(activeState);
  let copiedText = '';
  const exportPort: ExportPort = {
    async download() {
      return false;
    },
    async copyText(text) {
      copiedText = text;
      return true;
    },
  };
  const runtime = createRuntime(repository, [], exportPort);
  await runtime.start();

  expect(await runtime.exportState()).toEqual({
    ok: true,
    method: 'copy',
    filename: 'ium-test-platform-reference-2026-08-03.json',
  });
  expect(copiedText).toBe(new TextDecoder().decode(serializeState(activeState)));
});

test('IUM5 rejects a future state schema without changing active storage', async () => {
  const repository = new MemoryStateRepository();
  const activeState = state({
    moduleId: 'IUM-5-CORE-05',
    moduleVersion: '0.1.0',
    stateSchemaVersion: 1,
    payload: { phaseId: 'ue1-orientation' },
  });
  const futureState = state({
    moduleId: 'IUM-5-CORE-05',
    moduleVersion: '0.1.0',
    stateSchemaVersion: 2,
    payload: { phaseId: 'future-phase' },
  });
  await repository.save(activeState);
  const runtime = createModuleRuntime({
    moduleId: 'IUM-5-CORE-05',
    moduleVersion: '0.1.0',
    targetStateSchemaVersion: 1,
    repository,
    migrations: [],
    clock: { now: () => new Date('2026-08-03T13:00:00.000Z') },
    createWorkspaceId: () => '223e4567-e89b-42d3-a456-426614174000',
  });
  await runtime.start();

  const result = runtime.previewImport(serializeState(futureState));

  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'MIGRATION_FAILED' }),
  });
  expect(await repository.load('IUM-5-CORE-05')).toEqual(activeState);
  expect(await runtime.confirmImport()).toEqual({
    ok: false,
    error: expect.objectContaining({
      technicalDetails: 'No import is waiting for confirmation',
    }),
  });
});
