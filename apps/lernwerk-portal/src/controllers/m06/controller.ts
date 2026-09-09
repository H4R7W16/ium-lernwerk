import {
  createInitialDossier,
  evidenceBelongsToProgram,
  parseDossier,
  type Dossier,
  type Program,
} from '@ium/v2-g5-m06';
import { createV2StateRepository } from '@ium/local-state';
import { createModuleRuntime } from '@ium/module-runtime';
import type { ReloadReadiness } from '@ium/module-runtime';
import { createBrowserExportPort, createWorkspaceId } from '../algorithm-workbench/browser-ports.js';
import { chooseStorage } from '../storage-choice.js';
import type { ReloadRequestDetail } from '../update-coordinator.js';

type Failure = Readonly<{ ok: false; error: Readonly<{ message: string }> }>;

export type M06RuntimePort = Readonly<{
  replacePayload(payload: Dossier): unknown | Failure;
  flush(): Promise<Readonly<{ ok: true; mode?: string }> | Failure>;
  previewImport(bytes: Uint8Array): Readonly<{ ok: true }> | Failure;
  confirmImport(): Promise<Readonly<{ ok: true; payload?: unknown }> | Failure>;
  cancelImport(): void;
  deleteActive(): Promise<Readonly<{ ok: true }> | Failure>;
  exportState?(): Promise<Readonly<{ ok: true }> | Failure>;
  exportRecovery?(): Promise<Readonly<{ ok: true }> | Failure>;
  prepareForReload(): Promise<ReloadReadiness>;
  releaseReloadPreparation?(): void;
  approveDiscardForReload?(): unknown;
}>;

export type M06Resources = Readonly<{ content: unknown; cases: unknown }>;

export type M06Dependencies = Readonly<{
  chooseStorage(root: HTMLElement): Promise<'persistent' | 'volatile-selected'>;
  createRuntime(
    choice: 'persistent' | 'volatile-selected',
    resources: M06Resources,
  ): Promise<Readonly<{
    runtime: M06RuntimePort;
    dossier: Dossier;
    mode: 'persistent' | 'volatile-selected' | 'volatile-fallback';
    warning?: string;
  }>>;
  registerReload?(controller: M06Controller): () => void;
}>;

export type M06SaveState =
  | Readonly<{ state: 'saved'; message: string }>
  | Readonly<{ state: 'changed'; message: string }>
  | Readonly<{ state: 'unsaved'; message: string }>;

function cloneDossier(value: Dossier): Dossier {
  return structuredClone(value);
}

export class M06Controller {
  #dossier: Dossier;
  #runtime: M06RuntimePort;
  #transient = { prediction: '', retrievalReason: '' };
  #save: M06SaveState = { state: 'saved', message: 'Arbeitsstand geladen.' };
  #pendingImport = false;
  #disposed = false;
  #revision = 0;
  #syncedRevision = -1;
  #reloadPreparing = false;
  #preparation = 0;
  #operations = 0;
  #listeners = new Set<(replacement: boolean) => void>();

  constructor(dossier: Dossier, runtime: M06RuntimePort) {
    const parsed = parseDossier(dossier);
    if (!parsed.ok) throw new TypeError(parsed.issues.join('; '));
    this.#dossier = cloneDossier(parsed.value);
    this.#runtime = runtime;
  }

  dossier(): Dossier {
    return cloneDossier(this.#dossier);
  }

  transient(): Readonly<{ prediction: string; retrievalReason: string }> {
    return { ...this.#transient };
  }

  saveState(): M06SaveState {
    return this.#save;
  }

  subscribe(listener: (replacement: boolean) => void): () => void {
    this.#listeners.add(listener);
    return () => this.#listeners.delete(listener);
  }

  #changed(message = 'Änderungen sind noch nicht gespeichert.'): void {
    this.#revision += 1;
    this.#save = { state: 'changed', message };
    this.#notify();
  }

  #notify(replacement = false): void {
    this.#listeners.forEach((listener) => listener(replacement));
  }

  reloadPreparing(): boolean {
    return this.#reloadPreparing;
  }

  #syncCurrent(): boolean {
    if (this.#syncedRevision === this.#revision) return true;
    try {
      const result = this.#runtime.replacePayload(cloneDossier(this.#dossier));
      if (result && typeof result === 'object' && 'ok' in result && result.ok === false) {
        this.#save = { state: 'unsaved', message: (result as Failure).error.message };
        this.#notify();
        return false;
      }
      this.#syncedRevision = this.#revision;
      return true;
    } catch {
      this.#save = { state: 'unsaved', message: 'Der aktuelle Entwurf konnte nicht übernommen werden.' };
      this.#notify();
      return false;
    }
  }

  setTransient(next: Partial<{ prediction: string; retrievalReason: string }>): void {
    if (this.#reloadPreparing) return;
    this.#transient = { ...this.#transient, ...next };
    this.#notify();
  }

  updateReturnNote(value: Dossier['returnNote']): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, returnNote: structuredClone(value) };
    this.#changed();
  }

  updateDiagram(program: Program, explanation: string): void {
    if (this.#reloadPreparing) return;
    this.#dossier = {
      ...this.#dossier,
      p3: { ...this.#dossier.p3, diagram: { program: structuredClone(program), explanation } },
    };
    this.#changed('Die eigene Ablaufgrafik wurde geändert; der Code bleibt unverändert.');
  }

  updateDraftProgram(program: Program): void {
    if (this.#reloadPreparing) return;
    const evidence = evidenceBelongsToProgram(this.#dossier.p3.evidence, program)
      ? this.#dossier.p3.evidence
      : { program: [], predicted: null, steps: [], rationale: '' } as const;
    this.#dossier = {
      ...this.#dossier,
      p3: { ...this.#dossier.p3, draftProgram: structuredClone(program), evidence },
    };
    this.#changed(evidence.steps.length === 0
      ? 'Der Code wurde geändert. Wähle danach eine neue passende Spur.'
      : undefined);
  }

  recordP3Evidence(
    predicted: Dossier['p3']['evidence']['predicted'],
    steps: readonly number[],
    rationale: string,
  ): void {
    if (this.#reloadPreparing) return;
    this.#dossier = {
      ...this.#dossier,
      p3: {
        ...this.#dossier.p3,
        evidence: {
          program: structuredClone(this.#dossier.p3.draftProgram),
          predicted: predicted === null ? null : structuredClone(predicted),
          steps: [...steps],
          rationale,
        },
      },
    };
    this.#changed('Der ausgewählte Spurbeleg wurde geändert.');
  }

  recordRevisionEvidence(
    phase: 'before' | 'after',
    program: Program,
    steps: readonly number[],
    rationale: string,
  ): void {
    if (this.#reloadPreparing) return;
    this.#dossier = {
      ...this.#dossier,
      p2: {
        ...this.#dossier.p2,
        [phase]: { program: structuredClone(program), predicted: null, steps: [...steps], rationale },
      },
    };
    this.#changed('Der Revisionsvergleich wurde geändert.');
  }

  setFirstDeviation(step: number | null): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, p2: { ...this.#dossier.p2, firstDeviation: step } };
    this.#changed();
  }

  updateTransfer(sequence: Dossier['p5']['sequence'], rationale: string): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, p5: { sequence: [...sequence], rationale } };
    this.#changed();
  }

  updateSystems(value: Dossier['p6']): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, p6: structuredClone(value) };
    this.#changed();
  }

  updateP1Diagram(program: Program, explanation: string): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, p1: { diagram: { program: structuredClone(program), explanation } } };
    this.#changed();
  }

  updateP3Rationale(rationale: string): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier,
      p3: { ...this.#dossier.p3, evidence: { ...this.#dossier.p3.evidence, rationale } } };
    this.#changed();
  }

  updateRevisionRationale(phase: 'before' | 'after', rationale: string): void {
    if (this.#reloadPreparing) return;
    this.#dossier = { ...this.#dossier, p2: { ...this.#dossier.p2,
      [phase]: { ...this.#dossier.p2[phase], rationale } } };
    this.#changed();
  }

  async previewImport(bytes: Uint8Array): Promise<boolean> {
    if (this.#reloadPreparing || this.#operations > 0) return false;
    const result = this.#runtime.previewImport(bytes);
    this.#pendingImport = result.ok;
    if (!result.ok) {
      this.#runtime.cancelImport();
      this.#save = { state: 'unsaved', message: result.error.message };
      this.#notify();
    }
    return result.ok;
  }

  async importBytes(bytes: Uint8Array): Promise<boolean> {
    if (!(await this.previewImport(bytes))) return false;
    if (this.#reloadPreparing) return false;
    this.#operations += 1;
    try {
      const result = await this.#runtime.confirmImport();
      this.#pendingImport = false;
      if (!result.ok) {
        this.#runtime.cancelImport();
        this.#save = { state: 'unsaved', message: result.error.message };
        this.#notify();
        return false;
      }
      if (result.payload !== undefined) {
        const parsed = parseDossier(result.payload);
        if (!parsed.ok) {
          this.#runtime.cancelImport();
          this.#save = { state: 'unsaved', message: 'Import enthält kein gültiges Prüfdossier.' };
          return false;
        }
        this.#dossier = parsed.value;
      }
      this.#revision += 1;
      this.#syncedRevision = this.#revision;
      this.#transient = { prediction: '', retrievalReason: '' };
      this.#save = { state: 'saved', message: 'Importierter Arbeitsstand gespeichert.' };
      this.#notify(true);
      return true;
    } finally {
      this.#operations -= 1;
    }
  }

  async flush(): Promise<boolean> {
    if (this.#reloadPreparing || this.#operations > 0 || !this.#syncCurrent()) return false;
    const revision = this.#revision;
    this.#operations += 1;
    try {
      const result = await this.#runtime.flush();
      this.#save = !result.ok
        ? { state: 'unsaved', message: result.error.message }
        : revision === this.#revision
          ? { state: 'saved', message: 'Arbeitsstand gespeichert.' }
          : { state: 'changed', message: 'Weitere Änderungen sind noch nicht gespeichert.' };
      this.#notify();
      return result.ok;
    } catch {
      this.#save = { state: 'unsaved', message: 'Speichern fehlgeschlagen. Exportiere deinen aktuellen Entwurf.' };
      this.#notify();
      return false;
    } finally {
      this.#operations -= 1;
    }
  }

  async deleteAllWork(): Promise<boolean> {
    if (this.#reloadPreparing || this.#operations > 0) return false;
    this.#operations += 1;
    try {
      this.#runtime.cancelImport();
      this.#pendingImport = false;
      const result = await this.#runtime.deleteActive();
      if (!result.ok) {
        this.#save = { state: 'unsaved', message: result.error.message };
        return false;
      }
      this.#dossier = createInitialDossier();
      this.#revision += 1;
      this.#syncedRevision = -1;
      this.#transient = { prediction: '', retrievalReason: '' };
      this.#save = { state: 'saved', message: 'Arbeitsstand gelöscht.' };
      this.#notify(true);
      return true;
    } finally {
      this.#operations -= 1;
    }
  }

  async exportWork(recovery = false): Promise<boolean> {
    if (!recovery && !this.#syncCurrent()) return false;
    const action = recovery ? this.#runtime.exportRecovery : this.#runtime.exportState;
    if (!action) return false;
    const result = await action();
    if (!result.ok) {
      this.#save = { state: 'unsaved', message: result.error.message };
      this.#notify();
    }
    return result.ok;
  }

  async prepareForReload(): Promise<ReloadReadiness> {
    if (this.#operations > 0) return { safe: false, reason: 'write-failed' };
    if (!this.#reloadPreparing && !this.#syncCurrent()) return { safe: false, reason: 'write-failed' };
    this.#reloadPreparing = true;
    const preparation = this.#preparation;
    this.#notify();
    const result = await this.#runtime.prepareForReload();
    return preparation === this.#preparation ? result : { safe: false, reason: 'readback-failed' };
  }

  releaseReloadPreparation(): void {
    this.#preparation += 1;
    this.#runtime.releaseReloadPreparation?.();
    this.#reloadPreparing = false;
    this.#notify();
  }

  approveDiscardForReload(): void {
    if (this.#operations > 0) return;
    if (!this.#reloadPreparing) this.#syncCurrent();
    this.#runtime.approveDiscardForReload?.();
    this.#reloadPreparing = true;
    this.#notify();
  }

  dispose(): void {
    if (this.#disposed) return;
    this.#disposed = true;
    if (this.#pendingImport) this.#runtime.cancelImport();
    this.#listeners.clear();
  }
}

export function createM06Controller(dossier: Dossier, runtime: M06RuntimePort): M06Controller {
  return new M06Controller(dossier, runtime);
}

export async function connectM06(
  root: HTMLElement,
  resources: M06Resources,
  dependencies: M06Dependencies,
): Promise<M06Controller> {
  const choice = await dependencies.chooseStorage(root);
  const session = await dependencies.createRuntime(choice, resources);
  const storageCard = document.querySelector<HTMLElement>('[data-storage-mode]');
  const storageText = document.querySelector<HTMLElement>('[data-storage-status]');
  if (storageCard) storageCard.dataset.storageMode = session.mode;
  if (storageText) {
    storageText.textContent = session.warning ?? (session.mode === 'persistent'
      ? 'Auf diesem Gerät gespeichert'
      : session.mode === 'volatile-selected'
        ? 'Nur für diese Sitzung'
        : 'Dauerhaftes Speichern nicht verfügbar; nur diese Sitzung');
  }
  const controller = createM06Controller(session.dossier, session.runtime);
  const unregister = dependencies.registerReload?.(controller);
  const status = root.querySelector<HTMLElement>('[data-m06-save-status]');
  const save = root.querySelector<HTMLButtonElement>('[data-m06-save]');
  const retrieval = root.querySelector<HTMLTextAreaElement>('[data-m06-retrieval]');
  const openRetrieval = root.querySelector<HTMLButtonElement>('[data-m06-open-retrieval]');
  const retrievalPanel = root.querySelector<HTMLElement>('[data-m06-retrieval-panel]');
  const ownDraft = root.querySelector<HTMLButtonElement>('[data-m06-own-draft]');
  const dossierPanel = root.querySelector<HTMLElement>('#mein-pruefdossier');
  const render = () => {
    if (status) {
      status.textContent = controller.reloadPreparing()
        ? 'Arbeitsstand wird für die Aktualisierung gesichert. Die Bearbeitung ist kurz gesperrt.'
        : controller.saveState().message;
      status.dataset.saveState = controller.saveState().state;
    }
  };
  const unsubscribe = controller.subscribe(render);
  save?.addEventListener('click', () => void controller.flush());
  retrieval?.addEventListener('input', () => controller.setTransient({ retrievalReason: retrieval.value }));
  openRetrieval?.addEventListener('click', () => {
    if (retrievalPanel) retrievalPanel.hidden = false;
    retrieval?.focus();
  });
  ownDraft?.addEventListener('click', () => dossierPanel?.focus());
  render();
  const dispose = controller.dispose.bind(controller);
  controller.dispose = () => {
    unsubscribe();
    unregister?.();
    dispose();
  };
  return controller;
}

export function createBrowserM06Dependencies(root: HTMLElement): M06Dependencies {
  return {
    chooseStorage,
    async createRuntime(choice) {
      const selection = await createV2StateRepository({
        preferredMode: choice,
        databaseName: 'ium-lernwerk-v2',
      });
      const runtime = createModuleRuntime({
        moduleId: 'V2-G5-M06',
        moduleVersion: '0.1.0',
        targetStateSchemaVersion: 1,
        repository: selection.repository,
        migrations: [],
        clock: { now: () => new Date() },
        createWorkspaceId,
        exportPort: createBrowserExportPort(root),
        statePolicy: {
          supportedModuleVersions: ['0.1.0'],
          createInitialPayload: createInitialDossier,
          validatePayload: (payload) => parseDossier(payload).ok,
        },
      });
      const started = await runtime.start();
      if (!started.ok) throw new Error(started.error.message);
      const parsed = parseDossier(started.state.payload);
      if (!parsed.ok) throw new Error(parsed.issues.join('; '));
      const port: M06RuntimePort = {
        replacePayload: (payload) => runtime.updatePayload(payload),
        flush: () => runtime.flush(),
        previewImport: (bytes) => runtime.previewImport(bytes),
        async confirmImport() {
          const result = await runtime.confirmImport();
          return result.ok
            ? { ok: true, payload: result.state.payload }
            : result;
        },
        cancelImport: () => runtime.cancelImport(),
        deleteActive: () => runtime.deleteActive(),
        exportState: () => runtime.exportState(),
        exportRecovery: () => runtime.exportRecovery(),
        prepareForReload: () => runtime.prepareForReload(),
        releaseReloadPreparation: () => runtime.releaseReloadPreparation(),
        approveDiscardForReload: () => runtime.approveDiscardForReload(),
      };
      return {
        runtime: port,
        dossier: parsed.value,
        mode: selection.mode,
        ...(selection.warning === undefined ? {} : { warning: selection.warning.message }),
      };
    },
    registerReload(controller) {
      const request = ((event: CustomEvent<ReloadRequestDetail>) => {
        event.detail.add(controller.prepareForReload());
      }) as EventListener;
      const release = () => controller.releaseReloadPreparation();
      const discard = () => controller.approveDiscardForReload();
      document.addEventListener('ium:reload-request', request);
      document.addEventListener('ium:reload-release', release);
      document.addEventListener('ium:reload-discard', discard);
      return () => {
        document.removeEventListener('ium:reload-request', request);
        document.removeEventListener('ium:reload-release', release);
        document.removeEventListener('ium:reload-discard', discard);
      };
    },
  };
}
