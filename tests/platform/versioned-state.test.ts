import { expect, test } from 'vitest';
import { IDBFactory } from 'fake-indexeddb';
import type { LearningStateEnvelope } from '../../packages/module-contract/src/index.js';
import { VersionedIndexedDbStateRepository as Repository }
  from '../../packages/local-state/src/versioned-indexeddb-repository.js';
import { VersionedMemoryStateRepository }
  from '../../packages/local-state/src/versioned-memory-repository.js';
import { sameVersion } from '../../packages/local-state/src/version-token.js';

function syntheticState(
  overrides: Partial<LearningStateEnvelope> = {},
): LearningStateEnvelope {
  return {
    format: 'ium-learning-state',
    formatVersion: 1,
    moduleId: 'V2-G5-M06',
    moduleVersion: '0.1.0',
    stateSchemaVersion: 1,
    workspaceId: '123e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-09-07T12:00:00.000Z',
    payload: { test: 'A' },
    ...overrides,
  };
}

test('stale instance cannot overwrite a newer row or revive deletion', async () => {
  const indexedDbFactory = new IDBFactory();
  const a = await Repository.open({ indexedDbFactory, databaseName: 'synthetic-cas' });
  const b = await Repository.open({ indexedDbFactory, databaseName: 'synthetic-cas' });
  const original = syntheticState();
  await a.load(original.moduleId);
  expect((await a.save(original)).ok).toBe(true);
  await b.load(original.moduleId);
  expect((await a.save({ ...original, payload: { test: 'new' } })).ok).toBe(true);
  expect((await b.save(original)).ok).toBe(false);
  expect((await b.deleteModule(original.moduleId)).ok).toBe(false);
  await b.load(original.moduleId);
  expect((await a.deleteAll()).ok).toBe(true);
  expect((await b.save(original)).ok).toBe(false);
  expect(await a.load(original.moduleId)).toBeNull();
});

test('compares generation and revision together', () => {
  expect(sameVersion({ generation: 2, revision: 4 }, { generation: 2, revision: 4 })).toBe(true);
  expect(sameVersion({ generation: 1, revision: 4 }, { generation: 2, revision: 4 })).toBe(false);
  expect(sameVersion({ generation: 2, revision: 3 }, { generation: 2, revision: 4 })).toBe(false);
});

test('versioned memory instances conflict only through explicit shared test backing', async () => {
  const backing = { states: new Map(), generation: 0 };
  const a = new VersionedMemoryStateRepository('volatile-selected', backing);
  const b = new VersionedMemoryStateRepository('volatile-selected', backing);
  const original = syntheticState();
  await a.load(original.moduleId);
  await b.load(original.moduleId);
  expect((await a.save(original)).ok).toBe(true);
  const stale = await b.save({ ...original, payload: { test: 'stale' } });
  expect(stale).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_CONFLICT' }),
  });
  expect(await a.deleteModule(original.moduleId)).toEqual({ ok: true, deleted: true });
  await b.load(original.moduleId);
  expect(await b.load(original.moduleId)).toBeNull();
});

test('save requires a load token and a failed clone keeps that token usable', async () => {
  const repository = await Repository.open({
    indexedDbFactory: new IDBFactory(),
    databaseName: 'synthetic-token-lifecycle',
  });
  const original = syntheticState();
  expect(await repository.save(original)).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_CONFLICT' }),
  });
  await repository.load(original.moduleId);
  const invalid = {
    ...original,
    payload: { invalid: () => undefined },
  } as unknown as LearningStateEnvelope;
  expect(await repository.save(invalid)).toEqual({
    ok: false,
    error: expect.objectContaining({ code: 'STORAGE_WRITE_FAILED' }),
  });
  expect((await repository.save(original)).ok).toBe(true);
  expect(await repository.load(original.moduleId)).toEqual(original);
});
