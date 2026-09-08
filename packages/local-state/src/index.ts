import type { PlatformError, StateRepository, StorageMode } from '@ium/module-contract';
import {
  IndexedDbStateRepository,
  type IndexedDbRepositoryOptions,
} from './indexeddb-repository.js';
import { MemoryStateRepository } from './memory-repository.js';
import {
  VersionedIndexedDbStateRepository,
  type VersionedIndexedDbRepositoryOptions,
} from './versioned-indexeddb-repository.js';
import { VersionedMemoryStateRepository } from './versioned-memory-repository.js';

export type StateRepositorySelection = Readonly<{
  repository: StateRepository;
  mode: StorageMode;
  warning?: PlatformError;
}>;

export type CreateStateRepositoryOptions = Readonly<{
  preferredMode: 'persistent' | 'volatile-selected';
  indexedDbFactory?: IDBFactory;
  databaseName?: string;
}>;

export async function createStateRepository(
  options: CreateStateRepositoryOptions,
): Promise<StateRepositorySelection> {
  if (options.preferredMode === 'volatile-selected') {
    const repository = new MemoryStateRepository('volatile-selected');
    return { repository, mode: repository.mode };
  }

  try {
    const indexedDbFactory = options.indexedDbFactory ?? globalThis.indexedDB;
    if (!indexedDbFactory) {
      throw new Error('IndexedDB is unavailable');
    }
    const openOptions: IndexedDbRepositoryOptions = {
      indexedDbFactory,
      ...(options.databaseName === undefined
        ? {}
        : { databaseName: options.databaseName }),
    };
    const repository = await IndexedDbStateRepository.open(openOptions);
    return { repository, mode: repository.mode };
  } catch (error) {
    const repository = new MemoryStateRepository('volatile-fallback');
    return {
      repository,
      mode: repository.mode,
      warning: {
        code: 'STORAGE_UNAVAILABLE',
        message: 'Dauerhaftes lokales Speichern ist nicht verfügbar.',
        action: 'Arbeite in dieser Sitzung weiter und exportiere deinen Arbeitsstand.',
        technicalDetails: String(error),
      },
    };
  }
}

export async function createV2StateRepository(
  options: CreateStateRepositoryOptions,
): Promise<StateRepositorySelection> {
  if (options.preferredMode === 'volatile-selected') {
    const repository = new VersionedMemoryStateRepository('volatile-selected');
    return { repository, mode: repository.mode };
  }

  try {
    const indexedDbFactory = options.indexedDbFactory ?? globalThis.indexedDB;
    if (!indexedDbFactory) {
      throw new Error('IndexedDB is unavailable');
    }
    const openOptions: VersionedIndexedDbRepositoryOptions = {
      indexedDbFactory,
      ...(options.databaseName === undefined
        ? {}
        : { databaseName: options.databaseName }),
    };
    const repository = await VersionedIndexedDbStateRepository.open(openOptions);
    return { repository, mode: repository.mode };
  } catch (error) {
    const repository = new VersionedMemoryStateRepository('volatile-fallback');
    return {
      repository,
      mode: repository.mode,
      warning: {
        code: 'STORAGE_UNAVAILABLE',
        message: 'Dauerhaftes lokales Speichern ist nicht verfügbar.',
        action: 'Arbeite in dieser Sitzung weiter und exportiere deinen Arbeitsstand.',
        technicalDetails: String(error),
      },
    };
  }
}

export {
  IndexedDbStateRepository,
  MemoryStateRepository,
  VersionedIndexedDbStateRepository,
  VersionedMemoryStateRepository,
};
export { sameVersion } from './version-token.js';
export type { IndexedDbRepositoryOptions, VersionedIndexedDbRepositoryOptions };
export type { VersionedMemoryBacking } from './versioned-memory-repository.js';
export type { StoredRow, VersionToken } from './version-token.js';
