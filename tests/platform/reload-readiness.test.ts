import { expect, test } from 'vitest';
import {
  allReady,
  collectReadiness,
  isCurrentReadiness,
} from '../../apps/lernwerk-portal/src/controllers/reload-readiness.js';
import type { StateRepository } from '../../packages/module-contract/src/index.js';
import {
  MemoryStateRepository,
  VersionedMemoryStateRepository,
  type VersionedMemoryBacking,
} from '../../packages/local-state/src/index.js';
import { createModuleRuntime } from '../../packages/module-runtime/src/index.js';
import {
  coordinateUpdate,
  type UpdateBridge,
} from '../../apps/lernwerk-portal/src/controllers/update-coordinator.js';

function persistentRepository(backing = new MemoryStateRepository()): StateRepository {
  return {
    mode: 'persistent',
    load: (moduleId) => backing.load(moduleId),
    save: (state) => backing.save(state).then((result) => result.ok
      ? { ok: true as const, mode: 'persistent' as const }
      : result),
    deleteModule: (moduleId) => backing.deleteModule(moduleId),
    deleteAll: () => backing.deleteAll(),
  };
}

function persistentVersioned(backing: VersionedMemoryBacking): StateRepository {
  const repository = new VersionedMemoryStateRepository('volatile-selected', backing);
  return {
    mode: 'persistent',
    load: (moduleId) => repository.load(moduleId),
    save: (state) => repository.save(state).then((result) => result.ok
      ? { ok: true as const, mode: 'persistent' as const }
      : result),
    deleteModule: (moduleId) => repository.deleteModule(moduleId),
    deleteAll: () => repository.deleteAll(),
  };
}

function runtime(repository: StateRepository) {
  return createModuleRuntime({
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    targetStateSchemaVersion: 1,
    repository,
    migrations: [],
    clock: { now: () => new Date('2026-09-08T10:00:00.000Z') },
    createWorkspaceId: () => '123e4567-e89b-42d3-a456-426614174000',
  });
}

test('one volatile client prevents reload even if another persisted', () => {
  expect(allReady([
    { safe: true, reason: 'persisted-readback', revision: 1 },
    { safe: false, reason: 'volatile' },
  ])).toBe(false);
});

test('a rejected client readiness becomes a visible veto', async () => {
  const result = await collectReadiness([
    Promise.resolve({ safe: true, reason: 'no-work', revision: 0 } as const),
    Promise.reject(new Error('client disappeared')),
  ]);

  expect(result).toEqual({
    safe: false,
    values: [
      { safe: true, reason: 'no-work', revision: 0 },
      { safe: false, reason: 'unknown-client' },
    ],
    errors: ['client disappeared'],
  });
});

test('a later edit invalidates a persisted readback', () => {
  const readiness = { safe: true, reason: 'persisted-readback', revision: 4 } as const;

  expect(isCurrentReadiness(readiness, 4)).toBe(true);
  expect(isCurrentReadiness(readiness, 5)).toBe(false);
});

test('persistent readiness is bound to the current runtime revision and freezes edits', async () => {
  const active = runtime(persistentRepository());
  expect((await active.start()).ok).toBe(true);
  expect(active.updatePayload({ text: 'A' })).toEqual(expect.objectContaining({ payload: { text: 'A' } }));

  const readiness = await active.prepareForReload();

  expect(readiness).toEqual({ safe: true, reason: 'persisted-readback', revision: 1 });
  expect(active.updatePayload({ text: 'B' })).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_WRITE_FAILED' }),
  });
  active.releaseReloadPreparation();
  expect(active.updatePayload({ text: 'B' })).toEqual(expect.objectContaining({ payload: { text: 'B' } }));
  expect(isCurrentReadiness(readiness, active.currentRevision())).toBe(false);
});

test('volatile work vetoes reload until its exact revision is explicitly discarded', async () => {
  const active = runtime(new MemoryStateRepository());
  expect((await active.start()).ok).toBe(true);
  active.updatePayload({ text: 'ungesichert' });

  expect(await active.prepareForReload()).toEqual({ safe: false, reason: 'volatile' });
  active.releaseReloadPreparation();
  expect(active.approveDiscardForReload()).toEqual({
    safe: true,
    reason: 'explicit-discard',
    revision: 1,
  });
  expect(await active.prepareForReload()).toEqual({
    safe: true,
    reason: 'explicit-discard',
    revision: 1,
  });
});

test('requesting an export never turns volatile work into a recoverable readback', async () => {
  const repository = new MemoryStateRepository();
  const active = createModuleRuntime({
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    targetStateSchemaVersion: 1,
    repository,
    migrations: [],
    clock: { now: () => new Date('2026-09-08T10:00:00.000Z') },
    createWorkspaceId: () => '123e4567-e89b-42d3-a456-426614174000',
    exportPort: {
      async download() { return true; },
      async copyText() { return true; },
    },
  });
  expect((await active.start()).ok).toBe(true);
  active.updatePayload({ text: 'export requested' });
  expect((await active.exportState()).ok).toBe(true);

  expect(await active.prepareForReload()).toEqual({ safe: false, reason: 'volatile' });
});

test('quota and stale-client conflicts remain visible readiness vetoes', async () => {
  let failWrites = false;
  const base = persistentRepository();
  const quota: StateRepository = {
    ...base,
    save: async (state) => failWrites
      ? {
        ok: false,
        error: {
          code: 'STORAGE_QUOTA',
          message: 'synthetic quota',
          action: 'keep working',
        },
      }
      : base.save(state),
  };
  const quotaRuntime = runtime(quota);
  expect((await quotaRuntime.start()).ok).toBe(true);
  quotaRuntime.updatePayload({ text: 'too large' });
  failWrites = true;
  expect(await quotaRuntime.prepareForReload()).toEqual({ safe: false, reason: 'write-failed' });

  const backing: VersionedMemoryBacking = { states: new Map(), generation: 0 };
  const newer = runtime(persistentVersioned(backing));
  const stale = runtime(persistentVersioned(backing));
  expect((await newer.start()).ok).toBe(true);
  expect((await stale.start()).ok).toBe(true);
  newer.updatePayload({ text: 'newer' });
  expect((await newer.flush()).ok).toBe(true);
  stale.updatePayload({ text: 'stale' });
  expect(await stale.prepareForReload()).toEqual({ safe: false, reason: 'conflict' });
});

test('a mismatching persistent readback is never treated as recoverable', async () => {
  const base = persistentRepository();
  let corruptReadback = false;
  const repository: StateRepository = {
    ...base,
    async load(moduleId) {
      const value = await base.load(moduleId);
      return corruptReadback && value
        ? { ...value, payload: { text: 'older value' } }
        : value;
    },
  };
  const active = runtime(repository);
  expect((await active.start()).ok).toBe(true);
  active.updatePayload({ text: 'current value' });
  corruptReadback = true;

  expect(await active.prepareForReload()).toEqual({ safe: false, reason: 'readback-failed' });
});

test('a client veto releases every prepared client and never activates', async () => {
  const calls: string[] = [];
  const bridge: UpdateBridge = {
    async prepare() {
      calls.push('prepare');
      return {
        clientIds: ['a', 'b'],
        values: [
          { safe: true, reason: 'persisted-readback', revision: 2 },
          { safe: false, reason: 'volatile' },
        ],
      };
    },
    async commit() {
      calls.push('commit');
      return true;
    },
    async release() {
      calls.push('release');
    },
    async activate() {
      calls.push('activate');
    },
  };

  expect(await coordinateUpdate(bridge, 'request-1')).toEqual({
    activated: false,
    reason: 'volatile',
  });
  expect(calls).toEqual(['prepare', 'release']);
});

test('a changed client inventory aborts before candidate activation', async () => {
  const calls: string[] = [];
  const bridge: UpdateBridge = {
    async prepare() {
      calls.push('prepare');
      return {
        clientIds: ['a'],
        values: [{ safe: true, reason: 'no-work', revision: 0 }],
      };
    },
    async commit() {
      calls.push('commit');
      return false;
    },
    async release() {
      calls.push('release');
    },
    async activate() {
      calls.push('activate');
    },
  };

  expect(await coordinateUpdate(bridge, 'request-2')).toEqual({
    activated: false,
    reason: 'unknown-client',
  });
  expect(calls).toEqual(['prepare', 'commit', 'release']);
});

test('activation follows prepare and unchanged-inventory commit', async () => {
  const calls: string[] = [];
  const bridge: UpdateBridge = {
    async prepare() {
      calls.push('prepare');
      return {
        clientIds: ['a'],
        values: [{ safe: true, reason: 'persisted-readback', revision: 3 }],
      };
    },
    async commit() {
      calls.push('commit');
      return true;
    },
    async release() {
      calls.push('release');
    },
    async activate() {
      calls.push('activate');
    },
  };

  expect(await coordinateUpdate(bridge, 'request-3')).toEqual({
    activated: true,
    reason: 'activated',
  });
  expect(calls).toEqual(['prepare', 'commit', 'activate']);
});
