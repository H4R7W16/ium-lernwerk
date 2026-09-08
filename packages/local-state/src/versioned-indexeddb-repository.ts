import type {
  DeleteResult,
  LearningStateEnvelope,
  PlatformError,
  SaveResult,
  StateRepository,
} from '@ium/module-contract';
import { sameVersion, type StoredRow, type VersionToken } from './version-token.js';

function requestResult<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.addEventListener('success', () => resolve(request.result), { once: true });
    request.addEventListener('error', () => reject(request.error), { once: true });
  });
}

function transactionDone(transaction: IDBTransaction): Promise<void> {
  return new Promise((resolve, reject) => {
    transaction.addEventListener('complete', () => resolve(), { once: true });
    transaction.addEventListener(
      'abort',
      () => reject(transaction.error ?? new DOMException('Transaction aborted', 'AbortError')),
      { once: true },
    );
    transaction.addEventListener('error', () => reject(transaction.error), { once: true });
  });
}

export type VersionedIndexedDbRepositoryOptions = Readonly<{
  indexedDbFactory: IDBFactory;
  databaseName?: string;
}>;

function conflictError(): PlatformError {
  return {
    code: 'STORAGE_CONFLICT',
    message: 'Dieser Arbeitsstand wurde inzwischen an anderer Stelle geändert oder gelöscht.',
    action: 'Exportiere deine Sitzung oder öffne den aktuellen Stand erneut.',
  };
}

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

export class VersionedIndexedDbStateRepository implements StateRepository {
  readonly mode = 'persistent' as const;
  readonly #database: IDBDatabase;
  readonly #tokens = new Map<string, VersionToken>();

  private constructor(database: IDBDatabase) {
    this.#database = database;
  }

  static async open(
    options: VersionedIndexedDbRepositoryOptions,
  ): Promise<VersionedIndexedDbStateRepository> {
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      let settled = false;
      const request = options.indexedDbFactory.open(
        options.databaseName ?? 'ium-lernwerk-v2',
        1,
      );
      request.addEventListener('upgradeneeded', () => {
        const opened = request.result;
        if (!opened.objectStoreNames.contains('states')) {
          opened.createObjectStore('states', { keyPath: 'moduleId' });
        }
        if (!opened.objectStoreNames.contains('meta')) {
          const meta = opened.createObjectStore('meta');
          meta.put(0, 'generation');
        }
      });
      request.addEventListener('success', () => {
        if (settled) {
          request.result.close();
          return;
        }
        settled = true;
        resolve(request.result);
      }, { once: true });
      request.addEventListener('error', () => {
        if (settled) return;
        settled = true;
        reject(request.error);
      }, { once: true });
      request.addEventListener(
        'blocked',
        () => {
          if (settled) return;
          settled = true;
          reject(new DOMException('IndexedDB open request was blocked', 'InvalidStateError'));
        },
        { once: true },
      );
    });
    return new VersionedIndexedDbStateRepository(database);
  }

  async load(moduleId: string): Promise<LearningStateEnvelope | null> {
    const transaction = this.#database.transaction(['meta', 'states'], 'readonly');
    const done = transactionDone(transaction);
    const [generationValue, row] = await Promise.all([
      requestResult(transaction.objectStore('meta').get('generation') as IDBRequest<number | undefined>),
      requestResult(transaction.objectStore('states').get(moduleId) as IDBRequest<StoredRow | undefined>),
    ]);
    await done;
    const generation = generationValue ?? 0;
    this.#tokens.set(moduleId, { generation, revision: row?.revision ?? 0 });
    return row?.state ? structuredClone(row.state) : null;
  }

  async save(state: LearningStateEnvelope): Promise<SaveResult> {
    const expected = this.#tokens.get(state.moduleId);
    if (!expected) {
      return { ok: false, error: conflictError() };
    }
    const transaction = this.#database.transaction(['meta', 'states'], 'readwrite');
    const done = transactionDone(transaction);
    try {
      const meta = transaction.objectStore('meta');
      const states = transaction.objectStore('states');
      const [generationValue, row] = await Promise.all([
        requestResult(meta.get('generation') as IDBRequest<number | undefined>),
        requestResult(states.get(state.moduleId) as IDBRequest<StoredRow | undefined>),
      ]);
      const generation = generationValue ?? 0;
      const current = { generation, revision: row?.revision ?? 0 };
      if (!sameVersion(expected, current)) {
        transaction.abort();
        try {
          await done;
        } catch {
          // Expected abort keeps the transaction free of writes.
        }
        return { ok: false, error: conflictError() };
      }
      const revision = current.revision + 1;
      await requestResult(states.put({
        moduleId: state.moduleId,
        revision,
        state: structuredClone(state),
      }));
      await done;
      this.#tokens.set(state.moduleId, { generation, revision });
      return { ok: true, mode: this.mode };
    } catch (error) {
      try {
        transaction.abort();
      } catch {
        // The transaction may already have aborted or committed.
      }
      try {
        await done;
      } catch {
        // The failed write is reported through the repository result.
      }
      return { ok: false, error: writeError(error) };
    }
  }

  async deleteModule(moduleId: string): Promise<DeleteResult> {
    const expected = this.#tokens.get(moduleId);
    if (!expected) {
      return { ok: false, error: conflictError() };
    }
    const transaction = this.#database.transaction(['meta', 'states'], 'readwrite');
    const done = transactionDone(transaction);
    try {
      const meta = transaction.objectStore('meta');
      const states = transaction.objectStore('states');
      const [generationValue, row] = await Promise.all([
        requestResult(meta.get('generation') as IDBRequest<number | undefined>),
        requestResult(states.get(moduleId) as IDBRequest<StoredRow | undefined>),
      ]);
      const generation = generationValue ?? 0;
      const current = { generation, revision: row?.revision ?? 0 };
      if (!sameVersion(expected, current)) {
        transaction.abort();
        try {
          await done;
        } catch {
          // Expected abort keeps the transaction free of writes.
        }
        return { ok: false, error: conflictError() };
      }
      const deleted = row?.state !== null && row !== undefined;
      const revision = current.revision + 1;
      await requestResult(states.put({ moduleId, revision, state: null }));
      await done;
      this.#tokens.set(moduleId, { generation: current.generation, revision });
      return { ok: true, deleted };
    } catch (error) {
      try {
        transaction.abort();
      } catch {
        // The transaction may already have aborted or committed.
      }
      try {
        await done;
      } catch {
        // The failed delete is reported through the repository result.
      }
      return { ok: false, error: writeError(error) };
    }
  }

  async deleteAll(): Promise<DeleteResult> {
    const transaction = this.#database.transaction(['meta', 'states'], 'readwrite');
    const done = transactionDone(transaction);
    try {
      const meta = transaction.objectStore('meta');
      const states = transaction.objectStore('states');
      const [generationValue, rows] = await Promise.all([
        requestResult(meta.get('generation') as IDBRequest<number | undefined>),
        requestResult(states.getAll() as IDBRequest<StoredRow[]>),
      ]);
      const generation = generationValue ?? 0;
      const deleted = rows.some((row) => row.state !== null);
      await Promise.all([
        requestResult(states.clear()),
        requestResult(meta.put(generation + 1, 'generation')),
      ]);
      await done;
      this.#tokens.clear();
      return { ok: true, deleted };
    } catch (error) {
      try {
        transaction.abort();
      } catch {
        // The transaction may already have aborted or committed.
      }
      try {
        await done;
      } catch {
        // The failed global delete is reported through the repository result.
      }
      return { ok: false, error: writeError(error) };
    }
  }
}
