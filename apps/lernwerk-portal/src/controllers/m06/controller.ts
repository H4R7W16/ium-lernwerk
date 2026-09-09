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
  previewImport(bytes: Uint8Array): Readonly<{ ok: true; payload: unknown }> | Failure;
  confirmImport(): Promise<Readonly<{ ok: true; payload: unknown }> | Failure>;
  startNew(): Promise<Readonly<{ ok: true; payload: unknown }> | Failure>;
  hasRecovery?(): boolean;
  cancelImport(): void;
  deleteActive(): Promise<Readonly<{ ok: true }> | (Failure & Readonly<{ cleared?: true }>)>;
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
    startupError?: string;
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
  #preview: Dossier | null = null;
  #ready = true;
  #replacing = false;
  #disposed = false;
  #revision = 0;
  #syncedRevision = -1;
  #reloadPreparing = false;
  #preparation = 0;
  #operations = 0;
  #listeners = new Set<(replacement: boolean) => void>();

  constructor(dossier: Dossier, runtime: M06RuntimePort, startupError?: string) {
    const parsed = parseDossier(dossier);
    if (!parsed.ok) throw new TypeError(parsed.issues.join('; '));
    this.#dossier = cloneDossier(parsed.value);
    this.#runtime = runtime;
    if (startupError !== undefined) {
      this.#ready = false;
      this.#save = { state: 'unsaved', message: startupError };
    }
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

  workspaceReady(): boolean { return this.#ready; }
  replacingWork(): boolean { return this.#replacing; }
  importPreview(): Dossier | null { return this.#preview === null ? null : cloneDossier(this.#preview); }
  hasRecovery(): boolean { return this.#runtime.hasRecovery?.() ?? false; }

  #editable(): boolean { return this.#ready && !this.#reloadPreparing && !this.#replacing; }

  #acceptReplacement(payload: unknown, message: string): boolean {
    const parsed = parseDossier(payload);
    if (!parsed.ok) {
      this.#ready = false;
      this.#save = { state: 'unsaved', message: 'Der neue Stand enthält kein gültiges Prüfdossier.' };
      return false;
    }
    this.#dossier = cloneDossier(parsed.value);
    this.#revision += 1;
    this.#syncedRevision = this.#revision;
    this.#transient = { prediction: '', retrievalReason: '' };
    this.#ready = true;
    this.#save = { state: 'saved', message };
    return true;
  }

  #syncCurrent(): boolean {
    if (!this.#ready) return false;
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
    if (!this.#editable()) return;
    this.#transient = { ...this.#transient, ...next };
    this.#notify();
  }

  updateReturnNote(value: Dossier['returnNote']): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, returnNote: structuredClone(value) };
    this.#changed();
  }

  updateDiagram(program: Program, explanation: string): void {
    if (!this.#editable()) return;
    this.#dossier = {
      ...this.#dossier,
      p3: { ...this.#dossier.p3, diagram: { program: structuredClone(program), explanation } },
    };
    this.#changed('Die eigene Ablaufgrafik wurde geändert; der Code bleibt unverändert.');
  }

  updateDraftProgram(program: Program): void {
    if (!this.#editable()) return;
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
    if (!this.#editable()) return;
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
    if (!this.#editable()) return;
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
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, p2: { ...this.#dossier.p2, firstDeviation: step } };
    this.#changed();
  }

  updateTransfer(sequence: Dossier['p5']['sequence'], rationale: string): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, p5: { sequence: [...sequence], rationale } };
    this.#changed();
  }

  updateSystems(value: Dossier['p6']): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, p6: structuredClone(value) };
    this.#changed();
  }

  updateP1Diagram(program: Program, explanation: string): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, p1: { diagram: { program: structuredClone(program), explanation } } };
    this.#changed();
  }

  updateP3Rationale(rationale: string): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier,
      p3: { ...this.#dossier.p3, evidence: { ...this.#dossier.p3.evidence, rationale } } };
    this.#changed();
  }

  updateRevisionRationale(phase: 'before' | 'after', rationale: string): void {
    if (!this.#editable()) return;
    this.#dossier = { ...this.#dossier, p2: { ...this.#dossier.p2,
      [phase]: { ...this.#dossier.p2[phase], rationale } } };
    this.#changed();
  }

  cancelImport(message?: string): void {
    if (this.#replacing) return;
    this.#runtime.cancelImport();
    this.#pendingImport = false;
    this.#preview = null;
    if (message) this.#save = { state: 'unsaved', message };
    this.#notify();
  }

  async previewImport(bytes: Uint8Array): Promise<boolean> {
    if (this.#reloadPreparing || this.#operations > 0) return false;
    this.cancelImport();
    try {
      const result = this.#runtime.previewImport(bytes);
      const parsed = result.ok ? parseDossier(result.payload) : null;
      if (!result.ok || !parsed?.ok) {
        this.#runtime.cancelImport();
        this.#save = { state: 'unsaved', message: result.ok
          ? 'Import enthält kein gültiges Prüfdossier.' : result.error.message };
        this.#notify();
        return false;
      }
      this.#pendingImport = true;
      this.#preview = cloneDossier(parsed.value);
      this.#notify();
      return true;
    } catch {
      this.cancelImport();
      this.#save = { state: 'unsaved', message: 'Die Datei konnte nicht geprüft werden.' };
      this.#notify();
      return false;
    }
  }

  async confirmImport(): Promise<boolean> {
    if (this.#reloadPreparing || this.#operations > 0 || !this.#pendingImport) return false;
    this.#operations += 1;
    this.#replacing = true;
    this.#pendingImport = false;
    this.#preview = null;
    this.#notify();
    let replacement = false;
    try {
      const result = await this.#runtime.confirmImport();
      if (!result.ok) {
        this.#save = { state: 'unsaved', message: result.error.message };
        return false;
      }
      replacement = this.#acceptReplacement(result.payload, 'Importierter Arbeitsstand gespeichert.');
      return replacement;
    } catch {
      this.#save = { state: 'unsaved', message: 'Import fehlgeschlagen. Dein bisheriger Stand bleibt erhalten.' };
      return false;
    } finally {
      this.#runtime.cancelImport();
      this.#operations -= 1;
      this.#replacing = false;
      this.#notify(replacement);
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
    this.cancelImport();
    this.#operations += 1;
    this.#replacing = true;
    this.#notify();
    let deleted = false;
    try {
      const result = await this.#runtime.deleteActive();
      if (result.ok || result.cleared) {
        deleted = true;
        this.#dossier = createInitialDossier();
        this.#revision += 1;
        this.#syncedRevision = -1;
        this.#ready = false;
        this.#transient = { prediction: '', retrievalReason: '' };
      }
      if (!result.ok) {
        this.#save = { state: 'unsaved', message: deleted
          ? `Die Löschung wurde ausgeführt, konnte aber nicht nachgeprüft werden. ${result.error.message}`
          : result.error.message };
        return false;
      }
      const next = await this.#runtime.startNew();
      if (!next.ok) {
        this.#save = { state: 'unsaved', message: `Arbeitsstand gelöscht. Neuer Anfang noch nicht gespeichert: ${next.error.message}` };
        return false;
      }
      return this.#acceptReplacement(next.payload, 'Arbeitsstand gelöscht.');
    } catch {
      this.#save = { state: 'unsaved', message: deleted
        ? 'Arbeitsstand gelöscht. Der neue Anfang konnte noch nicht gespeichert werden.'
        : 'Löschen fehlgeschlagen. Prüfe den lokalen Stand erneut.' };
      return false;
    } finally {
      this.#operations -= 1;
      this.#replacing = false;
      this.#notify(deleted);
    }
  }

  async startNew(): Promise<boolean> {
    if (this.#ready || this.#reloadPreparing || this.#operations > 0) return false;
    this.cancelImport();
    this.#operations += 1;
    this.#replacing = true;
    this.#notify();
    let replacement = false;
    try {
      const result = await this.#runtime.startNew();
      if (!result.ok) {
        this.#save = { state: 'unsaved', message: result.error.message };
        return false;
      }
      replacement = this.#acceptReplacement(result.payload, 'Neuer Arbeitsstand gespeichert.');
      return replacement;
    } catch {
      this.#save = { state: 'unsaved', message: 'Ein neuer Anfang konnte nicht gespeichert werden. Das gesicherte Original bleibt erhalten.' };
      return false;
    } finally {
      this.#operations -= 1;
      this.#replacing = false;
      this.#notify(replacement);
    }
  }

  async exportWork(recovery = false): Promise<boolean> {
    if (!recovery && (this.#replacing || !this.#syncCurrent())) return false;
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
    if (this.#operations > 0 || (!this.#ready && !this.#reloadPreparing)) return { safe: false, reason: 'write-failed' };
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

export function createM06Controller(dossier: Dossier, runtime: M06RuntimePort, startupError?: string): M06Controller {
  return new M06Controller(dossier, runtime, startupError);
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
  const controller = createM06Controller(session.dossier, session.runtime, session.startupError);
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
        : controller.replacingWork() ? 'Der Arbeitsstand wird ersetzt. Bitte warte kurz.' : controller.saveState().message;
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
      const parsed = parseDossier(started.ok ? started.state.payload : createInitialDossier());
      if (!parsed.ok) throw new Error(parsed.issues.join('; '));
      const port: M06RuntimePort = {
        replacePayload: (payload) => runtime.updatePayload(payload),
        flush: () => runtime.flush(),
        previewImport(bytes) {
          const result = runtime.previewImport(bytes);
          return result.ok ? { ok: true, payload: result.state.payload } : result;
        },
        async startNew() {
          const result = await runtime.startNew();
          return result.ok ? { ok: true, payload: result.state.payload } : result;
        },
        hasRecovery: () => runtime.hasRecovery(),
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
        ...(!started.ok ? { startupError: started.error.message } : {}),
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
