import type {
  DeleteResult,
  LearningStateEnvelope,
  SaveResult,
  StateRepository,
  StorageMode,
} from '@ium/module-contract';

export class MemoryStateRepository implements StateRepository {
  readonly mode: StorageMode;
  readonly #states = new Map<string, LearningStateEnvelope>();

  constructor(mode: Extract<StorageMode, 'volatile-selected' | 'volatile-fallback'> = 'volatile-selected') {
    this.mode = mode;
  }

  async load(moduleId: string): Promise<LearningStateEnvelope | null> {
    const state = this.#states.get(moduleId);
    return state ? structuredClone(state) : null;
  }

  async save(state: LearningStateEnvelope): Promise<SaveResult> {
    this.#states.set(state.moduleId, structuredClone(state));
    return { ok: true, mode: this.mode };
  }

  async deleteModule(moduleId: string): Promise<DeleteResult> {
    return { ok: true, deleted: this.#states.delete(moduleId) };
  }

  async deleteAll(): Promise<DeleteResult> {
    const deleted = this.#states.size > 0;
    this.#states.clear();
    return { ok: true, deleted };
  }
}
