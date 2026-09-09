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
  acceptState,
  resolveStatePolicy,
  type RuntimeFailure,
  type StatePolicy,
} from './accept-state.js';
import type { StateMigration } from './migrations.js';

export type ModuleRuntimeDependencies = Readonly<{
  moduleId: string;
  moduleVersion: string;
  targetStateSchemaVersion: number;
  repository: StateRepository;
  migrations: readonly StateMigration[];
  clock: ClockPort;
  createWorkspaceId: () => string;
  exportPort?: ExportPort;
  statePolicy?: StatePolicy;
}>;

type RuntimeStateSuccess = Readonly<{
  ok: true;
  state: LearningStateEnvelope;
  mode: StorageMode;
}>;

export type ExportResult =
  | Readonly<{ ok: true; method: 'download' | 'copy'; filename: string }>
  | RuntimeFailure;

export type ReloadReadiness =
  | Readonly<{
    safe: true;
    reason: 'persisted-readback' | 'no-work' | 'explicit-discard';
    revision: number;
  }>
  | Readonly<{
    safe: false;
    reason: 'volatile' | 'write-failed' | 'conflict' | 'readback-failed' | 'unknown-client';
  }>;

type RecoverySnapshot =
  | Readonly<{ source: 'local'; value: unknown }>
  | Readonly<{ source: 'import'; bytes: Uint8Array }>;

function unavailableExportError(detail: string): PlatformError {
  return {
    code: 'STORAGE_WRITE_FAILED',
    message: 'Der Arbeitsstand konnte nicht ausgegeben werden.',
    action: 'Versuche den Export in einem normalen Browserfenster erneut.',
    technicalDetails: detail,
  };
}

function storageFailure(error: unknown): RuntimeFailure {
  return {
    ok: false,
    error: {
      code: 'STORAGE_UNAVAILABLE',
      message: 'Der lokale Arbeitsstand konnte nicht gelesen werden.',
      action: 'Versuche den Start erneut oder verwende eine bereits extern gesicherte Datei.',
      technicalDetails: String(error),
    },
  };
}

function writeFailure(error: unknown): RuntimeFailure {
  return {
    ok: false,
    error: {
      code: 'STORAGE_WRITE_FAILED',
      message: 'Der geprüfte Arbeitsstand konnte nicht gespeichert werden.',
      action: 'Sichere bei Bedarf das Original und versuche das Speichern erneut.',
      technicalDetails: String(error),
    },
  };
}

function invalidPayloadError(detail: string): RuntimeFailure {
  return {
    ok: false,
    error: {
      code: 'IMPORT_INVALID',
      message: 'Der Arbeitsstand enthält keine gültigen Moduldaten.',
      action: 'Behalte den letzten gültigen Stand und korrigiere die Eingabe.',
      technicalDetails: detail,
    },
  };
}

export class ModuleRuntime {
  readonly #dependencies: ModuleRuntimeDependencies;
  #active: LearningStateEnvelope | null = null;
  #pendingImport: LearningStateEnvelope | null = null;
  #recovery: RecoverySnapshot | null = null;
  #revision = 0;
  #reloadFrozen = false;
  #discardRevision: number | null = null;

  constructor(dependencies: ModuleRuntimeDependencies) {
    this.#dependencies = dependencies;
  }

  async start(): Promise<RuntimeStateSuccess | RuntimeFailure> {
    this.#reloadFrozen = false;
    this.#discardRevision = null;
    this.#revision = 0;
    this.#pendingImport = null;
    this.#recovery = null;
    this.#active = null;
    let loaded: unknown;
    try {
      loaded = await this.#dependencies.repository.load(this.#dependencies.moduleId);
    } catch (error) {
      return storageFailure(error);
    }
    if (loaded === null) {
      const policy = resolveStatePolicy(this.#dependencies);
      let payload: Record<string, unknown>;
      try {
        payload = policy.createInitialPayload();
      } catch (error) {
        return invalidPayloadError(`Initial payload creation failed: ${String(error)}`);
      }
      const candidate = {
        format: 'ium-learning-state',
        formatVersion: 1,
        moduleId: this.#dependencies.moduleId,
        moduleVersion: this.#dependencies.moduleVersion,
        stateSchemaVersion: this.#dependencies.targetStateSchemaVersion,
        workspaceId: this.#dependencies.createWorkspaceId(),
        savedAt: this.#dependencies.clock.now().toISOString(),
        payload,
      };
      const accepted = acceptState(candidate, this.#dependencies);
      if (!accepted.ok) return accepted;
      let saved: SaveResult;
      try {
        saved = await this.#dependencies.repository.save(accepted.state);
      } catch (error) {
        return writeFailure(error);
      }
      if (!saved.ok) {
        return saved;
      }
      this.#active = structuredClone(accepted.state);
      return { ok: true, state: structuredClone(accepted.state), mode: saved.mode };
    }

    this.#recovery = { source: 'local', value: structuredClone(loaded) };
    const accepted = acceptState(loaded, this.#dependencies);
    if (!accepted.ok) return accepted;
    const loadedState = loaded as LearningStateEnvelope;
    if (
      accepted.state.stateSchemaVersion !== loadedState.stateSchemaVersion
      || accepted.state.moduleVersion !== loadedState.moduleVersion
    ) {
      let saved: SaveResult;
      try {
        saved = await this.#dependencies.repository.save(accepted.state);
      } catch (error) {
        return writeFailure(error);
      }
      if (!saved.ok) {
        return saved;
      }
    }
    this.#active = structuredClone(accepted.state);
    this.#recovery = null;
    return {
      ok: true,
      state: structuredClone(accepted.state),
      mode: this.#dependencies.repository.mode,
    };
  }

  /** Explicitly replace the current/recovery state only after validating and saving a new dossier. */
  async startNew(): Promise<RuntimeStateSuccess | RuntimeFailure> {
    if (this.#reloadFrozen) return writeFailure('Reload preparation has frozen this runtime');
    this.#pendingImport = null;
    const policy = resolveStatePolicy(this.#dependencies);
    let payload: Record<string, unknown>;
    try {
      payload = policy.createInitialPayload();
    } catch (error) {
      return invalidPayloadError(`Initial payload creation failed: ${String(error)}`);
    }
    const accepted = acceptState({
      format: 'ium-learning-state', formatVersion: 1,
      moduleId: this.#dependencies.moduleId, moduleVersion: this.#dependencies.moduleVersion,
      stateSchemaVersion: this.#dependencies.targetStateSchemaVersion,
      workspaceId: this.#dependencies.createWorkspaceId(),
      savedAt: this.#dependencies.clock.now().toISOString(), payload,
    }, this.#dependencies);
    if (!accepted.ok) return accepted;
    let saved: SaveResult;
    try {
      saved = await this.#dependencies.repository.save(accepted.state);
    } catch (error) {
      return writeFailure(error);
    }
    if (!saved.ok) return saved;
    this.#active = structuredClone(accepted.state);
    this.#recovery = null;
    this.#revision += 1;
    this.#discardRevision = null;
    return { ok: true, state: structuredClone(accepted.state), mode: saved.mode };
  }

  updatePayload(
    payload: Readonly<Record<string, unknown>>,
  ): LearningStateEnvelope | RuntimeFailure {
    if (!this.#active) {
      throw new Error('Module runtime has not started');
    }
    if (this.#reloadFrozen) {
      return writeFailure('Reload preparation has frozen this runtime');
    }
    const candidate = {
      ...structuredClone(this.#active),
      savedAt: this.#dependencies.clock.now().toISOString(),
      payload: structuredClone(payload),
    };
    const accepted = acceptState(candidate, this.#dependencies);
    if (!accepted.ok) return accepted;
    this.#active = structuredClone(accepted.state);
    this.#revision += 1;
    this.#discardRevision = null;
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

  async exportState(): Promise<ExportResult> {
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
    if (this.#reloadFrozen) {
      return writeFailure('Reload preparation has frozen this runtime');
    }
    this.#pendingImport = null;
    if (!this.#recovery) {
      this.#recovery = { source: 'import', bytes: new Uint8Array(bytes) };
    }
    const parsed = parseImport(bytes, this.#dependencies.moduleId);
    if (!parsed.ok) {
      return parsed;
    }
    const accepted = acceptState(parsed.state, this.#dependencies);
    if (!accepted.ok) return accepted;
    this.#pendingImport = structuredClone(accepted.state);
    this.#revision += 1;
    this.#discardRevision = null;
    return {
      ok: true,
      state: structuredClone(accepted.state),
      preview: {
        ...parsed.preview,
        moduleVersion: accepted.state.moduleVersion,
        payloadFields: Object.keys(accepted.state.payload).sort(),
      },
    };
  }

  cancelImport(): void {
    this.#pendingImport = null;
  }

  hasRecovery(): boolean {
    return this.#recovery !== null;
  }

  async exportRecovery(): Promise<ExportResult> {
    if (!this.#recovery || !this.#dependencies.exportPort) {
      return {
        ok: false,
        error: unavailableExportError('No recovery snapshot or export port'),
      };
    }
    let bytes: Uint8Array;
    try {
      bytes = this.#recovery.source === 'import'
        ? new Uint8Array(this.#recovery.bytes)
        : new TextEncoder().encode(`${JSON.stringify(this.#recovery.value, null, 2)}\n`);
    } catch (error) {
      return invalidPayloadError(`Recovery serialization failed: ${String(error)}`);
    }
    const date = this.#dependencies.clock.now().toISOString().slice(0, 10);
    const filename = `ium-recovery-original-${date}.json`;
    if (await this.#dependencies.exportPort.download(filename, bytes, 'application/json')) {
      return { ok: true, method: 'download', filename };
    }
    let text: string;
    try {
      text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    } catch (error) {
      return invalidPayloadError(`Recovery bytes are not UTF-8: ${String(error)}`);
    }
    if (await this.#dependencies.exportPort.copyText(text)) {
      return { ok: true, method: 'copy', filename };
    }
    return {
      ok: false,
      error: unavailableExportError('Recovery download and copy fallback failed'),
    };
  }

  async confirmImport(): Promise<RuntimeStateSuccess | RuntimeFailure> {
    if (this.#reloadFrozen) {
      return writeFailure('Reload preparation has frozen this runtime');
    }
    if (!this.#pendingImport) {
      return {
        ok: false,
        error: unavailableExportError('No import is waiting for confirmation'),
      };
    }
    const next = structuredClone(this.#pendingImport);
    this.#pendingImport = null;
    let saved: SaveResult;
    try {
      saved = await this.#dependencies.repository.save(next);
    } catch (error) {
      return writeFailure(error);
    }
    if (!saved.ok) {
      return saved;
    }
    this.#active = next;
    this.#recovery = null;
    this.#revision += 1;
    this.#discardRevision = null;
    return { ok: true, state: structuredClone(next), mode: saved.mode };
  }

  async deleteActive(): Promise<Readonly<{ ok: true }> | (RuntimeFailure & Readonly<{ cleared?: true }>)> {
    if (this.#reloadFrozen) {
      return writeFailure('Reload preparation has frozen this runtime');
    }
    this.#pendingImport = null;
    const result = await this.#dependencies.repository.deleteModule(
      this.#dependencies.moduleId,
    );
    if (!result.ok) {
      return result;
    }
    // The delete has committed. Never retain a writable copy while checking its result.
    this.#active = null;
    this.#recovery = null;
    this.#revision += 1;
    this.#discardRevision = null;
    try {
      if (await this.#dependencies.repository.load(this.#dependencies.moduleId) !== null) {
        return { ok: false, cleared: true, error: unavailableExportError('Deleted module state is still present') };
      }
    } catch (error) {
      return { ...storageFailure(error), cleared: true };
    }
    return { ok: true };
  }

  async deleteAll(): Promise<Readonly<{ ok: true }> | RuntimeFailure> {
    if (this.#reloadFrozen) {
      return writeFailure('Reload preparation has frozen this runtime');
    }
    this.#pendingImport = null;
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
    this.#recovery = null;
    this.#revision += 1;
    this.#discardRevision = null;
    return { ok: true };
  }

  currentRevision(): number {
    return this.#revision;
  }

  approveDiscardForReload(): ReloadReadiness {
    this.#reloadFrozen = true;
    this.#discardRevision = this.#revision;
    return { safe: true, reason: 'explicit-discard', revision: this.#revision };
  }

  releaseReloadPreparation(): void {
    this.#reloadFrozen = false;
    this.#discardRevision = null;
  }

  async prepareForReload(): Promise<ReloadReadiness> {
    const revision = this.#revision;
    this.#reloadFrozen = true;
    if (this.#discardRevision === revision) {
      return { safe: true, reason: 'explicit-discard', revision };
    }
    if (this.#active === null) {
      return { safe: true, reason: 'no-work', revision };
    }
    if (this.#pendingImport !== null || this.#dependencies.repository.mode !== 'persistent') {
      return { safe: false, reason: 'volatile' };
    }

    let saved: SaveResult;
    try {
      saved = await this.#dependencies.repository.save(this.#active);
    } catch {
      return { safe: false, reason: 'write-failed' };
    }
    if (!saved.ok) {
      return {
        safe: false,
        reason: saved.error.code === 'STORAGE_CONFLICT' ? 'conflict' : 'write-failed',
      };
    }
    if (revision !== this.#revision) {
      return { safe: false, reason: 'readback-failed' };
    }

    let stored: LearningStateEnvelope | null;
    try {
      stored = await this.#dependencies.repository.load(this.#dependencies.moduleId);
    } catch {
      return { safe: false, reason: 'readback-failed' };
    }
    if (
      revision !== this.#revision
      || stored === null
      || JSON.stringify(stored) !== JSON.stringify(this.#active)
    ) {
      return { safe: false, reason: 'readback-failed' };
    }
    return { safe: true, reason: 'persisted-readback', revision };
  }
}

export function createModuleRuntime(
  dependencies: ModuleRuntimeDependencies,
): ModuleRuntime {
  return new ModuleRuntime(dependencies);
}
