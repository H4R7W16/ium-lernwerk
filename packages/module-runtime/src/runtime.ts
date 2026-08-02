import {
  parseImport,
  serializeState,
  stateExportFilename,
  type ImportParseResult,
} from '@ium/export-import';
import type {
  ClockPort,
  ExportPort,
  LearningStateEnvelope,
  PlatformError,
  SaveResult,
  StateRepository,
  StorageMode,
} from '@ium/module-contract';
import {
  migrateStateCopy,
  type StateMigration,
} from './migrations.js';

export type ModuleRuntimeDependencies = Readonly<{
  moduleId: string;
  moduleVersion: string;
  targetStateSchemaVersion: number;
  repository: StateRepository;
  migrations: readonly StateMigration[];
  clock: ClockPort;
  createWorkspaceId: () => string;
  exportPort?: ExportPort;
}>;

type RuntimeFailure = Readonly<{ ok: false; error: PlatformError }>;
type RuntimeStateSuccess = Readonly<{
  ok: true;
  state: LearningStateEnvelope;
  mode: StorageMode;
}>;

function unavailableExportError(detail: string): PlatformError {
  return {
    code: 'STORAGE_WRITE_FAILED',
    message: 'Der Arbeitsstand konnte nicht ausgegeben werden.',
    action: 'Versuche den Export in einem normalen Browserfenster erneut.',
    technicalDetails: detail,
  };
}

function unsupportedModuleVersionError(actual: string, expected: string): PlatformError {
  return {
    code: 'IMPORT_UNSUPPORTED_VERSION',
    message: 'Die Datei gehört zu einer nicht unterstützten Modulversion.',
    action: 'Öffne sie mit der passenden Lernwerkversion.',
    technicalDetails: `expected ${expected}, received ${actual}`,
  };
}

export class ModuleRuntime {
  readonly #dependencies: ModuleRuntimeDependencies;
  #active: LearningStateEnvelope | null = null;
  #pendingImport: LearningStateEnvelope | null = null;

  constructor(dependencies: ModuleRuntimeDependencies) {
    this.#dependencies = dependencies;
  }

  async start(): Promise<RuntimeStateSuccess | RuntimeFailure> {
    const loaded = await this.#dependencies.repository.load(
      this.#dependencies.moduleId,
    );
    if (!loaded) {
      const created: LearningStateEnvelope = {
        format: 'ium-learning-state',
        formatVersion: 1,
        moduleId: this.#dependencies.moduleId,
        moduleVersion: this.#dependencies.moduleVersion,
        stateSchemaVersion: this.#dependencies.targetStateSchemaVersion,
        workspaceId: this.#dependencies.createWorkspaceId(),
        savedAt: this.#dependencies.clock.now().toISOString(),
        payload: {},
      };
      const saved = await this.#dependencies.repository.save(created);
      if (!saved.ok) {
        return saved;
      }
      this.#active = structuredClone(created);
      return { ok: true, state: structuredClone(created), mode: saved.mode };
    }

    const migrated = migrateStateCopy(
      loaded,
      this.#dependencies.targetStateSchemaVersion,
      this.#dependencies.migrations,
    );
    if (!migrated.ok) {
      return { ok: false, error: migrated.error };
    }
    if (migrated.state.stateSchemaVersion !== loaded.stateSchemaVersion) {
      const saved = await this.#dependencies.repository.save(migrated.state);
      if (!saved.ok) {
        return saved;
      }
    }
    this.#active = structuredClone(migrated.state);
    return {
      ok: true,
      state: structuredClone(migrated.state),
      mode: this.#dependencies.repository.mode,
    };
  }

  updatePayload(payload: Readonly<Record<string, unknown>>): LearningStateEnvelope {
    if (!this.#active) {
      throw new Error('Module runtime has not started');
    }
    this.#active = {
      ...structuredClone(this.#active),
      savedAt: this.#dependencies.clock.now().toISOString(),
      payload: structuredClone(payload),
    };
    return structuredClone(this.#active);
  }

  async flush(): Promise<SaveResult> {
    if (!this.#active) {
      return {
        ok: false,
        error: unavailableExportError('Module runtime has not started'),
      };
    }
    return this.#dependencies.repository.save(this.#active);
  }

  async exportState(): Promise<
    | Readonly<{ ok: true; method: 'download' | 'copy'; filename: string }>
    | RuntimeFailure
  > {
    if (!this.#active || !this.#dependencies.exportPort) {
      return {
        ok: false,
        error: unavailableExportError('No active state or export port'),
      };
    }
    const bytes = serializeState(this.#active);
    const filename = stateExportFilename(this.#active);
    if (await this.#dependencies.exportPort.download(
      filename,
      bytes,
      'application/json',
    )) {
      return { ok: true, method: 'download', filename };
    }
    const text = new TextDecoder().decode(bytes);
    if (await this.#dependencies.exportPort.copyText(text)) {
      return { ok: true, method: 'copy', filename };
    }
    return {
      ok: false,
      error: unavailableExportError('Download and copy fallback failed'),
    };
  }

  previewImport(bytes: Uint8Array): ImportParseResult | RuntimeFailure {
    const parsed = parseImport(bytes, this.#dependencies.moduleId);
    if (!parsed.ok) {
      return parsed;
    }
    if (parsed.state.moduleVersion !== this.#dependencies.moduleVersion) {
      return {
        ok: false,
        error: unsupportedModuleVersionError(
          parsed.state.moduleVersion,
          this.#dependencies.moduleVersion,
        ),
      };
    }
    const migrated = migrateStateCopy(
      parsed.state,
      this.#dependencies.targetStateSchemaVersion,
      this.#dependencies.migrations,
    );
    if (!migrated.ok) {
      return { ok: false, error: migrated.error };
    }
    this.#pendingImport = structuredClone(migrated.state);
    return {
      ok: true,
      state: structuredClone(migrated.state),
      preview: {
        ...parsed.preview,
        payloadFields: Object.keys(migrated.state.payload).sort(),
      },
    };
  }

  async confirmImport(): Promise<RuntimeStateSuccess | RuntimeFailure> {
    if (!this.#pendingImport) {
      return {
        ok: false,
        error: unavailableExportError('No import is waiting for confirmation'),
      };
    }
    const next = structuredClone(this.#pendingImport);
    const saved = await this.#dependencies.repository.save(next);
    if (!saved.ok) {
      return saved;
    }
    this.#active = next;
    this.#pendingImport = null;
    return { ok: true, state: structuredClone(next), mode: saved.mode };
  }

  async deleteActive(): Promise<Readonly<{ ok: true }> | RuntimeFailure> {
    const result = await this.#dependencies.repository.deleteModule(
      this.#dependencies.moduleId,
    );
    if (!result.ok) {
      return result;
    }
    if (await this.#dependencies.repository.load(this.#dependencies.moduleId)) {
      return {
        ok: false,
        error: unavailableExportError('Deleted module state is still present'),
      };
    }
    this.#active = null;
    return { ok: true };
  }

  async deleteAll(): Promise<Readonly<{ ok: true }> | RuntimeFailure> {
    const result = await this.#dependencies.repository.deleteAll();
    if (!result.ok) {
      return result;
    }
    if (await this.#dependencies.repository.load(this.#dependencies.moduleId)) {
      return {
        ok: false,
        error: unavailableExportError('Local state is still present after global delete'),
      };
    }
    this.#active = null;
    this.#pendingImport = null;
    return { ok: true };
  }
}

export function createModuleRuntime(
  dependencies: ModuleRuntimeDependencies,
): ModuleRuntime {
  return new ModuleRuntime(dependencies);
}
