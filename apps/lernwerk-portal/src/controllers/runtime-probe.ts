import { createV2StateRepository } from '@ium/local-state';
import type { StateRepository } from '@ium/module-contract';
import { createModuleRuntime } from '@ium/module-runtime';
import { createBrowserExportPort, createWorkspaceId } from './algorithm-workbench/browser-ports.js';
import { chooseStorage } from './storage-choice.js';
import type { ReloadRequestDetail } from './pwa-registration.js';

function requiredElement<T extends Element>(root: ParentNode, selector: string): T {
  const element = root.querySelector<T>(selector);
  if (!element) throw new Error(`Missing runtime probe element: ${selector}`);
  return element;
}

function ensureUpdateProbeUi(root: HTMLElement): void {
  if (document.querySelector('[data-update-prompt]')) return;
  const connection = document.createElement('p');
  connection.dataset.connectionStatus = '';
  connection.dataset.pwaState = 'not-ready';
  connection.setAttribute('aria-live', 'polite');
  connection.textContent = 'Online – Offlinebereitschaft wird geprüft';
  const prompt = document.createElement('section');
  prompt.className = 'update-prompt';
  prompt.dataset.updatePrompt = '';
  prompt.hidden = true;
  prompt.tabIndex = -1;
  prompt.setAttribute('aria-labelledby', 'probe-update-title');
  const heading = document.createElement('h2');
  heading.id = 'probe-update-title';
  heading.textContent = 'Aktualisierung verfügbar';
  const explanation = document.createElement('p');
  explanation.textContent = 'Alle offenen Seiten müssen ihren aktuellen Arbeitsstand zuerst als wiederherstellbar bestätigen.';
  const actions = document.createElement('div');
  actions.className = 'actions';
  const confirm = document.createElement('button');
  confirm.type = 'button';
  confirm.dataset.updateConfirm = '';
  confirm.textContent = 'Speichern und aktualisieren';
  const dismiss = document.createElement('button');
  dismiss.type = 'button';
  dismiss.dataset.updateDismiss = '';
  dismiss.textContent = 'Später aktualisieren';
  actions.append(confirm, dismiss);
  prompt.append(heading, explanation, actions);
  root.before(connection, prompt);
  document.dispatchEvent(new CustomEvent('ium:update-ui-ready'));
}

function quotaRepository(repository: StateRepository): StateRepository {
  return {
    mode: repository.mode,
    load: (moduleId) => repository.load(moduleId),
    save: async () => ({
      ok: false,
      error: {
        code: 'STORAGE_QUOTA',
        message: 'Der lokale Speicherplatz reicht nicht aus.',
        action: 'Exportiere deinen Arbeitsstand und gib lokalen Speicher frei.',
      },
    }),
    deleteModule: (moduleId) => repository.deleteModule(moduleId),
    deleteAll: () => repository.deleteAll(),
  };
}

export async function connectRuntimeProbe(parent: ParentNode = document): Promise<void> {
  const root = parent.querySelector<HTMLElement>('[data-runtime-probe]');
  if (!root || root.dataset.connected === 'true') return;
  root.dataset.connected = 'true';
  root.dataset.reloadClient = 'true';
  ensureUpdateProbeUi(root);
  const params = new URLSearchParams(location.search);
  root.dataset.forceDownloadFallback = String(params.get('download') === 'blocked');
  const text = requiredElement<HTMLTextAreaElement>(root, '[data-probe-text]');
  const status = requiredElement<HTMLElement>(root, '[data-probe-status]');
  const error = requiredElement<HTMLElement>(root, '[data-probe-error]');
  const moduleId = root.dataset.moduleId!;
  const moduleVersion = root.dataset.moduleVersion!;
  const preferredMode = params.get('storage') === 'volatile'
    ? 'volatile-selected'
    : await chooseStorage(root);
  const blockedFactory = {
    open() {
      throw new DOMException('IndexedDB durch die Prüfhülle blockiert', 'InvalidStateError');
    },
  } as unknown as IDBFactory;
  const selection = await createV2StateRepository({
    preferredMode,
    ...(params.get('idb') === 'blocked' ? { indexedDbFactory: blockedFactory } : {}),
  });
  const repository = params.get('save') === 'quota'
    ? quotaRepository(selection.repository)
    : selection.repository;
  const runtime = createModuleRuntime({
    moduleId,
    moduleVersion,
    targetStateSchemaVersion: 1,
    repository,
    migrations: [],
    clock: { now: () => new Date() },
    createWorkspaceId,
    exportPort: createBrowserExportPort(root),
  });
  const showError = (message: string) => {
    error.hidden = false;
    error.textContent = message;
  };
  const started = await runtime.start();
  if (!started.ok) {
    showError(`${started.error.message} ${started.error.action}`);
    status.textContent = 'Kein lokaler Stand gespeichert';
    return;
  }
  text.value = typeof started.state.payload.text === 'string'
    ? started.state.payload.text
    : '';
  status.textContent = selection.mode === 'persistent'
    ? 'V2-Profilstand geöffnet'
    : 'Flüchtige V2-Sitzung geöffnet';
  if (selection.warning) {
    showError(`${selection.warning.message} ${selection.warning.action}`);
  }
  requiredElement<HTMLButtonElement>(root, '[data-probe-save]').addEventListener('click', async () => {
    runtime.updatePayload({ text: text.value });
    const result = await runtime.flush();
    if (!result.ok) {
      showError(`${result.error.message} ${result.error.action}`);
      status.textContent = 'Eigene Sitzung unverändert erhalten';
      return;
    }
    error.hidden = true;
    status.textContent = result.mode === 'persistent'
      ? 'Lokal gespeichert'
      : 'Nur für diese Sitzung gespeichert';
  });
  requiredElement<HTMLButtonElement>(root, '[data-probe-reopen]').addEventListener('click', () => {
    location.reload();
  });
  requiredElement<HTMLButtonElement>(root, '[data-probe-export]').addEventListener('click', async () => {
    runtime.updatePayload({ text: text.value });
    const result = await runtime.exportState();
    if (!result.ok) {
      showError(`${result.error.message} ${result.error.action}`);
      return;
    }
    status.textContent = result.method === 'download'
      ? 'Download angefordert. Prüfe die Datei in deiner Ablage.'
      : 'Exporttext steht zur bewussten Ausgabe bereit.';
  });
  requiredElement<HTMLButtonElement>(root, '[data-probe-delete]').addEventListener('click', async () => {
    const result = await runtime.deleteActive();
    if (!result.ok) {
      showError(`${result.error.message} ${result.error.action}`);
      return;
    }
    text.value = '';
    status.textContent = 'Synthetischer Modulstand gelöscht';
  });

  const setReloadPreparing = (blocked: boolean) => {
    for (const control of root.querySelectorAll<HTMLButtonElement | HTMLTextAreaElement>('button, textarea')) {
      if (!control.matches('[data-probe-export], [data-copy-fallback-text]')) control.disabled = blocked;
    }
    root.dataset.reloadPreparing = String(blocked);
  };
  let discardForReload = false;
  document.addEventListener('ium:reload-request', ((event: CustomEvent<ReloadRequestDetail>) => {
    setReloadPreparing(true);
    event.detail.add((async () => {
      if (!discardForReload) {
        const updated = runtime.updatePayload({ text: text.value });
        if ('ok' in updated && !updated.ok) return { safe: false, reason: 'write-failed' } as const;
      }
      return runtime.prepareForReload();
    })());
  }) as EventListener);
  document.addEventListener('ium:reload-release', () => {
    discardForReload = false;
    runtime.releaseReloadPreparation();
    setReloadPreparing(false);
  });
  document.addEventListener('ium:reload-discard', () => {
    if (selection.mode === 'persistent') return;
    discardForReload = true;
    setReloadPreparing(true);
    runtime.releaseReloadPreparation();
    runtime.approveDiscardForReload();
  });

  const clientId = createWorkspaceId();
  const channel = typeof BroadcastChannel === 'undefined' || params.get('broadcast') === 'off'
    ? null
    : new BroadcastChannel('ium-local-data-v2');
  channel?.addEventListener('message', (event: MessageEvent<unknown>) => {
    const value = event.data as { type?: string; requestId?: string };
    if (value.type !== 'invalidate' || typeof value.requestId !== 'string') return;
    runtime.cancelImport();
    for (const control of root.querySelectorAll<HTMLButtonElement | HTMLTextAreaElement>('button, textarea')) {
      control.disabled = true;
    }
    status.textContent = 'Lokale Profildaten gelöscht';
    showError('Diese offene Sitzung speichert nicht weiter. Lade die Seite neu.');
    channel.postMessage({ type: 'invalidated', requestId: value.requestId, clientId });
  });
}
