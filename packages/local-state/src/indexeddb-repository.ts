import type {
  DeleteResult,
  LearningStateEnvelope,
  PlatformError,
  SaveResult,
  StateRepository,
} from '@ium/module-contract';
import { wrap, type DBSchema, type IDBPDatabase } from 'idb';

interface IumLearningDatabase extends DBSchema {
  activeStates: {
    key: string;
    value: LearningStateEnvelope;
  };
}

export type IndexedDbRepositoryOptions = Readonly<{
  indexedDbFactory: IDBFactory;
  databaseName?: string;
}>;

function writeError(error: unknown): PlatformError {
  const name = error instanceof DOMException ? error.name : '';
  if (name === 'QuotaExceededError') {
    return {
      code: 'STORAGE_QUOTA',
      message: 'Der lokale Speicherplatz reicht nicht aus.',
      action: 'Exportiere deinen Arbeitsstand und gib lokalen Speicher frei.',
      technicalDetails: String(error),
    };
  }
  return {
    code: 'STORAGE_WRITE_FAILED',
    message: 'Der Arbeitsstand konnte nicht dauerhaft gespeichert werden.',
    action: 'Exportiere den Arbeitsstand und versuche es erneut.',
    technicalDetails: String(error),
  };
}

export class IndexedDbStateRepository implements StateRepository {
  readonly mode = 'persistent' as const;
  readonly #database: IDBPDatabase<IumLearningDatabase>;

  private constructor(database: IDBPDatabase<IumLearningDatabase>) {
    this.#database = database;
  }

  static async open(
    options: IndexedDbRepositoryOptions,
  ): Promise<IndexedDbStateRepository> {
    const request = options.indexedDbFactory.open(
      options.databaseName ?? 'ium-lernwerk',
      1,
    );
    request.addEventListener('upgradeneeded', () => {
      if (!request.result.objectStoreNames.contains('activeStates')) {
        request.result.createObjectStore('activeStates', { keyPath: 'moduleId' });
      }
    });
    const database = await wrap(request) as IDBPDatabase<IumLearningDatabase> | undefined;
    if (!database) {
      throw new Error('IndexedDB open request returned no database');
    }
    return new IndexedDbStateRepository(database);
  }

  async load(moduleId: string): Promise<LearningStateEnvelope | null> {
    const value = await this.#database.get('activeStates', moduleId);
    return value ? structuredClone(value) : null;
  }

  async save(state: LearningStateEnvelope): Promise<SaveResult> {
    try {
      const transaction = this.#database.transaction('activeStates', 'readwrite');
      await transaction.store.put(structuredClone(state));
      await transaction.done;
      return { ok: true, mode: this.mode };
    } catch (error) {
      return { ok: false, error: writeError(error) };
    }
  }

  async deleteModule(moduleId: string): Promise<DeleteResult> {
    try {
      const transaction = this.#database.transaction('activeStates', 'readwrite');
      const existed = (await transaction.store.getKey(moduleId)) !== undefined;
      await transaction.store.delete(moduleId);
      await transaction.done;
      return { ok: true, deleted: existed };
    } catch (error) {
      return { ok: false, error: writeError(error) };
    }
  }

  async deleteAll(): Promise<DeleteResult> {
    try {
      const transaction = this.#database.transaction('activeStates', 'readwrite');
      const deleted = (await transaction.store.count()) > 0;
      await transaction.store.clear();
      await transaction.done;
      return { ok: true, deleted };
    } catch (error) {
      return { ok: false, error: writeError(error) };
    }
  }
}
