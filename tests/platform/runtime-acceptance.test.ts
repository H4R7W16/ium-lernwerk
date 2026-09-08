import { expect, test } from 'vitest';
import type {
  ExportPort,
  LearningStateEnvelope,
  SaveResult,
  StateRepository,
  StorageMode,
} from '../../packages/module-contract/src/index.js';
import { serializeState } from '../../packages/export-import/src/index.js';
import {
  acceptState,
  createModuleRuntime,
  type StateMigration,
  type StatePolicy,
} from '../../packages/module-runtime/src/index.js';

function state(overrides: Partial<LearningStateEnvelope> = {}): LearningStateEnvelope {
  return {
    format: 'ium-learning-state',
    formatVersion: 1,
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    stateSchemaVersion: 1,
    workspaceId: '123e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-08-03T12:00:00.000Z',
    payload: { text: 'original' },
    ...overrides,
  };
}

class ControlledRepository implements StateRepository {
  readonly mode: StorageMode = 'volatile-selected';
  value: unknown;
  failSave = false;
  throwOnSave = false;
  throwOnLoad = false;
  saves = 0;

  constructor(value: unknown = null) {
    this.value = structuredClone(value);
  }

  async load(): Promise<LearningStateEnvelope | null> {
    if (this.throwOnLoad) throw new Error('synthetic load failure');
    return structuredClone(this.value) as LearningStateEnvelope | null;
  }

  async save(next: LearningStateEnvelope): Promise<SaveResult> {
    this.saves += 1;
    if (this.throwOnSave) throw new Error('synthetic save exception');
    if (this.failSave) {
      return {
        ok: false,
        error: {
          code: 'STORAGE_WRITE_FAILED',
          message: 'synthetic save failure',
          action: 'retry',
        },
      };
    }
    this.value = structuredClone(next);
    return { ok: true, mode: this.mode };
  }

  async deleteModule() {
    const deleted = this.value !== null;
    this.value = null;
    return { ok: true as const, deleted };
  }

  async deleteAll() {
    return this.deleteModule();
  }
}

class CaptureExportPort implements ExportPort {
  bytes: Uint8Array | null = null;
  filename = '';
  downloadSucceeds = true;

  async download(filename: string, bytes: Uint8Array) {
    this.filename = filename;
    this.bytes = new Uint8Array(bytes);
    return this.downloadSucceeds;
  }

  async copyText(text: string) {
    this.bytes = new TextEncoder().encode(text);
    return true;
  }
}

const textPolicy: StatePolicy = {
  supportedModuleVersions: ['0.9.0', '1.0.0'],
  createInitialPayload: () => ({ text: 'initial' }),
  validatePayload: (value) => (
    value !== null
    && typeof value === 'object'
    && typeof (value as { text?: unknown }).text === 'string'
  ),
};

function runtime(
  repository: ControlledRepository,
  options: Readonly<{
    migrations?: readonly StateMigration[];
    policy?: StatePolicy;
    exportPort?: ExportPort;
    targetSchema?: number;
  }> = {},
) {
  return createModuleRuntime({
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    targetStateSchemaVersion: options.targetSchema ?? 1,
    repository,
    migrations: options.migrations ?? [],
    clock: { now: () => new Date('2026-08-03T13:00:00.000Z') },
    createWorkspaceId: () => '223e4567-e89b-42d3-a456-426614174000',
    statePolicy: options.policy ?? textPolicy,
    ...(options.exportPort === undefined ? {} : { exportPort: options.exportPort }),
  });
}

test('acceptState migrates a supported source version before normalizing the module version', () => {
  const migration: StateMigration = {
    from: 1,
    to: 2,
    migrate: (payload) => ({ ...payload, migrated: true }),
  };
  const result = acceptState(
    state({ moduleVersion: '0.9.0' }),
    {
      moduleId: 'TEST-PLATFORM-REFERENCE',
      moduleVersion: '1.0.0',
      targetStateSchemaVersion: 2,
      migrations: [migration],
      statePolicy: {
        ...textPolicy,
        validatePayload: (value) => (
          textPolicy.validatePayload(value)
          && (value as { migrated?: unknown }).migrated === true
        ),
      },
    },
  );

  expect(result).toEqual({
    ok: true,
    state: expect.objectContaining({
      moduleVersion: '1.0.0',
      stateSchemaVersion: 2,
      payload: { text: 'original', migrated: true },
    }),
  });
});

test('invalid initial and updated payloads never replace the last accepted state', async () => {
  const invalidInitial = runtime(new ControlledRepository(), {
    policy: { ...textPolicy, createInitialPayload: () => ({ nope: true }) },
  });
  expect(await invalidInitial.start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_INVALID' }),
  });

  const repository = new ControlledRepository(state());
  const port = new CaptureExportPort();
  const active = runtime(repository, { exportPort: port });
  expect((await active.start()).ok).toBe(true);
  expect(active.updatePayload({ nope: true })).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_INVALID' }),
  });
  expect((await active.exportState()).ok).toBe(true);
  expect(JSON.parse(new TextDecoder().decode(port.bytes!)).payload).toEqual({ text: 'original' });
});

test('a migration failure preserves and exports the local original', async () => {
  const original = state();
  const repository = new ControlledRepository(original);
  const port = new CaptureExportPort();
  const instance = runtime(repository, {
    targetSchema: 2,
    migrations: [{ from: 1, to: 2, migrate: () => { throw new Error('broken'); } }],
    exportPort: port,
  });

  expect(await instance.start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'MIGRATION_FAILED' }),
  });
  expect(instance.hasRecovery()).toBe(true);
  expect(await instance.exportRecovery()).toEqual({
    ok: true,
    method: 'download',
    filename: expect.stringContaining('recovery-original'),
  });
  expect(JSON.parse(new TextDecoder().decode(port.bytes!))).toEqual(original);
  expect(repository.value).toEqual(original);
});

test('an earlier import original stays recoverable while a failed preview invalidates its candidate', async () => {
  const repository = new ControlledRepository(state());
  const port = new CaptureExportPort();
  const instance = runtime(repository, { exportPort: port });
  await instance.start();
  const originalImport = serializeState(state({ payload: { text: 'candidate' } }));
  expect(instance.previewImport(originalImport).ok).toBe(true);
  const invalid = new TextEncoder().encode('{not-json');

  expect(instance.previewImport(invalid).ok).toBe(false);
  expect((await instance.confirmImport()).ok).toBe(false);
  expect(await instance.exportRecovery()).toEqual({
    ok: true,
    method: 'download',
    filename: expect.stringContaining('recovery-original'),
  });
  expect(port.bytes).toEqual(originalImport);
  expect(repository.value).toEqual(state());
});

test('cancel, delete and a second confirmation all consume the current preview', async () => {
  const repository = new ControlledRepository(state());
  const instance = runtime(repository);
  await instance.start();
  expect(instance.previewImport(serializeState(state({ payload: { text: 'A' } }))).ok).toBe(true);
  instance.cancelImport();
  expect((await instance.confirmImport()).ok).toBe(false);

  expect(instance.previewImport(serializeState(state({ payload: { text: 'B' } }))).ok).toBe(true);
  expect((await instance.deleteActive()).ok).toBe(true);
  expect((await instance.confirmImport()).ok).toBe(false);

  await instance.start();
  expect(instance.previewImport(serializeState(state({ payload: { text: 'C' } }))).ok).toBe(true);
  expect((await instance.confirmImport()).ok).toBe(true);
  expect((await instance.confirmImport()).ok).toBe(false);
});

test('a failed import save consumes the preview and leaves active storage unchanged', async () => {
  const original = state();
  const repository = new ControlledRepository(original);
  const instance = runtime(repository);
  await instance.start();
  expect(instance.previewImport(serializeState(state({ payload: { text: 'candidate' } }))).ok).toBe(true);
  repository.failSave = true;

  expect((await instance.confirmImport()).ok).toBe(false);
  expect((await instance.confirmImport()).ok).toBe(false);
  expect(repository.value).toEqual(original);
  expect(instance.hasRecovery()).toBe(true);
});

test('load failures do not invent a recovery snapshot', async () => {
  const repository = new ControlledRepository();
  repository.throwOnLoad = true;
  const instance = runtime(repository);

  expect(await instance.start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_UNAVAILABLE' }),
  });
  expect(instance.hasRecovery()).toBe(false);
});

test('a falsy damaged repository value is rejected instead of replaced', async () => {
  const repository = new ControlledRepository(0);
  const instance = runtime(repository);

  expect(await instance.start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_INVALID' }),
  });
  expect(repository.value).toBe(0);
  expect(repository.saves).toBe(0);
  expect(instance.hasRecovery()).toBe(true);
});

test('missing and payload-breaking migrations reject without changing the original', async () => {
  const original = state();
  const missing = new ControlledRepository(original);
  expect((await runtime(missing, { targetSchema: 2 }).start()).ok).toBe(false);
  expect(missing.value).toEqual(original);

  const invalid = new ControlledRepository(original);
  const result = await runtime(invalid, {
    targetSchema: 2,
    migrations: [{ from: 1, to: 2, migrate: () => ({ nope: true }) }],
  }).start();
  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'IMPORT_INVALID' }),
  });
  expect(invalid.value).toEqual(original);
});

test('a save failure after successful migration keeps the original recoverable', async () => {
  const original = state();
  const repository = new ControlledRepository(original);
  repository.failSave = true;
  const port = new CaptureExportPort();
  const instance = runtime(repository, {
    targetSchema: 2,
    migrations: [{ from: 1, to: 2, migrate: (payload) => ({ ...payload, migrated: true }) }],
    policy: {
      ...textPolicy,
      validatePayload: (value) => (
        textPolicy.validatePayload(value)
        && (value as { migrated?: unknown }).migrated === true
      ),
    },
    exportPort: port,
  });

  expect(await instance.start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_WRITE_FAILED' }),
  });
  expect(repository.value).toEqual(original);
  expect(instance.hasRecovery()).toBe(true);
  expect((await instance.exportRecovery()).ok).toBe(true);
  expect(JSON.parse(new TextDecoder().decode(port.bytes!))).toEqual(original);
});

test('a thrown initial save is reported as a write failure', async () => {
  const repository = new ControlledRepository();
  repository.throwOnSave = true;

  expect(await runtime(repository).start()).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_WRITE_FAILED' }),
  });
  expect(repository.value).toBeNull();
});

test('a non-serializable damaged local value reports recovery failure', async () => {
  const damaged: Record<string, unknown> = {
    ...state(),
    payload: { text: 'original', unsupported: 1n },
  };
  const repository = new ControlledRepository(damaged);
  const port = new CaptureExportPort();
  const instance = runtime(repository, { exportPort: port });

  expect((await instance.start()).ok).toBe(false);
  expect(instance.hasRecovery()).toBe(true);
  expect(await instance.exportRecovery()).toEqual({
    ok: false,
    error: expect.objectContaining({
      code: 'IMPORT_INVALID',
      technicalDetails: expect.stringContaining('Recovery serialization failed'),
    }),
  });
});

test('invalid first import remains available as its exact original bytes', async () => {
  const repository = new ControlledRepository(state());
  const port = new CaptureExportPort();
  const instance = runtime(repository, { exportPort: port });
  await instance.start();
  const invalid = new TextEncoder().encode('{broken');

  expect(instance.previewImport(invalid).ok).toBe(false);
  expect((await instance.exportRecovery()).ok).toBe(true);
  expect(port.bytes).toEqual(invalid);
});
