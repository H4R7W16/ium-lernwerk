import type {
  DeleteResult,
  LearningStateEnvelope,
  PlatformError,
  SaveResult,
  StateRepository,
  StorageMode,
} from '@ium/module-contract';
import { sameVersion, type StoredRow, type VersionToken } from './version-token.js';

export type VersionedMemoryBacking = {
  states: Map<string, StoredRow>;
  generation: number;
};

function conflictError(): PlatformError {
  return {
    code: 'STORAGE_CONFLICT',
    message: 'Dieser Arbeitsstand wurde inzwischen an anderer Stelle geändert oder gelöscht.',
    action: 'Exportiere deine Sitzung oder öffne den aktuellen Stand erneut.',
  };
}

function writeError(error: unknown): PlatformError {
  return {
    code: 'STORAGE_WRITE_FAILED',
    message: 'Der Arbeitsstand konnte in dieser Sitzung nicht gespeichert werden.',
    action: 'Exportiere den Arbeitsstand und versuche es erneut.',
    technicalDetails: String(error),
  };
}

export class VersionedMemoryStateRepository implements StateRepository {
  readonly mode: Extract<StorageMode, 'volatile-selected' | 'volatile-fallback'>;
  readonly #backing: VersionedMemoryBacking;
  readonly #tokens = new Map<string, VersionToken>();

  constructor(
    mode: Extract<StorageMode, 'volatile-selected' | 'volatile-fallback'> = 'volatile-selected',
    backing?: VersionedMemoryBacking,
  ) {
    this.mode = mode;
    this.#backing = backing ?? { states: new Map(), generation: 0 };
  }

  async load(moduleId: string): Promise<LearningStateEnvelope | null> {
    const row = this.#backing.states.get(moduleId);
    this.#tokens.set(moduleId, {
      generation: this.#backing.generation,
      revision: row?.revision ?? 0,
    });
    return row?.state ? structuredClone(row.state) : null;
  }

  async save(state: LearningStateEnvelope): Promise<SaveResult> {
    const expected = this.#tokens.get(state.moduleId);
    const currentRow = this.#backing.states.get(state.moduleId);
    const current = {
      generation: this.#backing.generation,
      revision: currentRow?.revision ?? 0,
    };
    if (!expected || !sameVersion(expected, current)) {
      return { ok: false, error: conflictError() };
    }
    try {
      const revision = current.revision + 1;
      const cloned = structuredClone(state);
      this.#backing.states.set(state.moduleId, {
        moduleId: state.moduleId,
        revision,
        state: cloned,
      });
      this.#tokens.set(state.moduleId, { generation: current.generation, revision });
      return { ok: true, mode: this.mode };
    } catch (error) {
      return { ok: false, error: writeError(error) };
    }
  }

  async deleteModule(moduleId: string): Promise<DeleteResult> {
    const expected = this.#tokens.get(moduleId);
    const currentRow = this.#backing.states.get(moduleId);
    const current = {
      generation: this.#backing.generation,
      revision: currentRow?.revision ?? 0,
    };
    if (!expected || !sameVersion(expected, current)) {
      return { ok: false, error: conflictError() };
    }
    const deleted = currentRow?.state !== null && currentRow !== undefined;
    const revision = (currentRow?.revision ?? 0) + 1;
    this.#backing.states.set(moduleId, { moduleId, revision, state: null });
    this.#tokens.set(moduleId, { generation: current.generation, revision });
    return { ok: true, deleted };
  }

  async deleteAll(): Promise<DeleteResult> {
    const deleted = [...this.#backing.states.values()].some((row) => row.state !== null);
    this.#backing.generation += 1;
    this.#backing.states.clear();
    this.#tokens.clear();
    return { ok: true, deleted };
  }
}
