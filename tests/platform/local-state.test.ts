import 'fake-indexeddb/auto';
import { IDBFactory } from 'fake-indexeddb';
import { expect, test } from 'vitest';
import type { LearningStateEnvelope } from '../../packages/module-contract/src/index.js';
import {
  createStateRepository,
  createV2StateRepository,
  IndexedDbStateRepository,
  MemoryStateRepository,
  VersionedIndexedDbStateRepository,
  VersionedMemoryStateRepository,
} from '../../packages/local-state/src/index.js';

const firstId = '123e4567-e89b-42d3-a456-426614174000';
const secondId = '223e4567-e89b-42d3-a456-426614174000';

function state(
  overrides: Partial<LearningStateEnvelope> = {},
): LearningStateEnvelope {
  return {
    format: 'ium-learning-state',
    formatVersion: 1,
    moduleId: 'TEST-PLATFORM-REFERENCE',
    moduleVersion: '1.0.0',
    stateSchemaVersion: 1,
    workspaceId: firstId,
    savedAt: '2026-08-03T12:00:00.000Z',
    payload: {},
    ...overrides,
  };
}

test('stores exactly one active state per module', async () => {
  const repository = new MemoryStateRepository();
  await repository.save(state({ workspaceId: firstId, payload: { text: 'eins' } }));
  await repository.save(state({ workspaceId: secondId, payload: { text: 'zwei' } }));
  expect(await repository.load('TEST-PLATFORM-REFERENCE')).toMatchObject({
    workspaceId: secondId,
    payload: { text: 'zwei' },
  });
});

test('reports saved only after the IndexedDB transaction completes', async () => {
  const repository = await IndexedDbStateRepository.open({
    indexedDbFactory: new IDBFactory(),
    databaseName: 'ium-local-state-confirmed',
  });
  const savedState = state();
  const result = await repository.save(savedState);
  expect(result).toEqual({ ok: true, mode: 'persistent' });
  expect(await repository.load('TEST-PLATFORM-REFERENCE')).toEqual(savedState);
});

test('falls back visibly when IndexedDB opening fails', async () => {
  const rejectingIndexedDbFactory = {
    open() {
      throw new Error('blocked by policy');
    },
  } as unknown as IDBFactory;
  const selection = await createStateRepository({
    indexedDbFactory: rejectingIndexedDbFactory,
    preferredMode: 'persistent',
  });
  expect(selection.mode).toBe('volatile-fallback');
  expect(selection.warning?.code).toBe('STORAGE_UNAVAILABLE');
});

test('failed write leaves the previous committed state unchanged', async () => {
  const repository = await IndexedDbStateRepository.open({
    indexedDbFactory: new IDBFactory(),
    databaseName: 'ium-local-state-atomic-write',
  });
  const committed = state({ payload: { text: 'bestehend' } });
  expect(await repository.save(committed)).toEqual({
    ok: true,
    mode: 'persistent',
  });
  const invalid = state({ payload: { uncloneable: () => 'not serializable' } });

  const result = await repository.save(invalid);

  expect(result).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_WRITE_FAILED' }),
  });
  expect(await repository.load(committed.moduleId)).toEqual(committed);
});

test('selects isolated V2 adapters without touching the V1 factory', async () => {
  const volatile = await createV2StateRepository({ preferredMode: 'volatile-selected' });
  expect(volatile.repository).toBeInstanceOf(VersionedMemoryStateRepository);
  expect(volatile.mode).toBe('volatile-selected');

  const persistent = await createV2StateRepository({
    preferredMode: 'persistent',
    indexedDbFactory: new IDBFactory(),
    databaseName: 'ium-v2-factory-selection',
  });
  expect(persistent.repository).toBeInstanceOf(VersionedIndexedDbStateRepository);
  expect(persistent.mode).toBe('persistent');
});

test('V2 persistent selection falls back visibly when opening fails', async () => {
  const rejectingIndexedDbFactory = {
    open() {
      throw new Error('blocked by policy');
    },
  } as unknown as IDBFactory;
  const selection = await createV2StateRepository({
    indexedDbFactory: rejectingIndexedDbFactory,
    preferredMode: 'persistent',
  });
  expect(selection.mode).toBe('volatile-fallback');
  expect(selection.warning).toEqual(expect.objectContaining({ code: 'STORAGE_UNAVAILABLE' }));
});
