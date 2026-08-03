import { createStateRepository } from '@ium/local-state';
import type { ExportPort, PlatformError } from '@ium/module-contract';
import { createModuleRuntime } from '@ium/module-runtime';
import {
  announceDataChanged,
  announceError,
  announceState,
  type StateStatusDetail,
} from '@ium/ui-components/controllers/status-announcer';

const SAVE_DELAY_MS = 250;

function browserExportPort(workspace: HTMLElement): ExportPort {
  return {
    async download(filename, bytes, mediaType) {
      const frame = window.frameElement;
      const blockedBySandbox =
        frame instanceof HTMLIFrameElement
        && frame.hasAttribute('sandbox')
        && !frame.sandbox.contains('allow-downloads');
      if (window.origin === 'null' || window.self !== window.top || blockedBySandbox) {
        return false;
      }
      const blobBytes = new Uint8Array(bytes.byteLength);
      blobBytes.set(bytes);
      const url = URL.createObjectURL(new Blob([blobBytes.buffer], { type: mediaType }));
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.hidden = true;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 0);
      return true;
    },
    async copyText(text) {
      const fallback = workspace.querySelector<HTMLElement>('[data-copy-fallback]');
      const field = workspace.querySelector<HTMLTextAreaElement>('[data-copy-fallback-text]');
      if (fallback && field) {
        fallback.hidden = false;
        field.value = text;
        field.focus();
        field.select();
      }
      try {
        await navigator.clipboard.writeText(text);
      } catch {
        // The visible read-only field remains the manual fallback.
      }
      return fallback !== null && field !== null;
    },
  };
}

function randomWorkspaceId(): string {
  if (typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6]! & 0x0f) | 0x40;
  bytes[8] = (bytes[8]! & 0x3f) | 0x80;
  const hex = [...bytes].map((value) => value.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

function showError(error: PlatformError): void {
  announceError(document, error);
}

export async function connectFixtureWorkspace(
  root: ParentNode = document,
): Promise<void> {
  const workspace = root.querySelector<HTMLElement>('[data-fixture-workspace]');
  if (!workspace || workspace.dataset.connected === 'true') {
    return;
  }
  workspace.dataset.connected = 'true';
  const moduleId = workspace.dataset.moduleId;
  const moduleVersion = workspace.dataset.moduleVersion;
  const textInput = workspace.querySelector<HTMLInputElement>('#fixture-text');
  const choiceInput = workspace.querySelector<HTMLSelectElement>('#fixture-choice');
  const status = workspace.querySelector<HTMLElement>('[data-save-status]');
  const exportButton = workspace.querySelector<HTMLButtonElement>('[data-fixture-export]');
  const importInput = workspace.querySelector<HTMLInputElement>('[data-fixture-import]');
  const importDialog = workspace.querySelector<HTMLDialogElement>('[data-import-dialog]');
  const deleteDialog = workspace.querySelector<HTMLDialogElement>('[data-delete-dialog]');
  const deleteButton = workspace.querySelector<HTMLButtonElement>('[data-fixture-delete]');
  if (
    !moduleId || !moduleVersion || !textInput || !choiceInput || !status
    || !exportButton || !importInput || !importDialog || !deleteDialog || !deleteButton
  ) {
    return;
  }

  const selectedVolatile = new URLSearchParams(location.search).get('storage') === 'volatile';
  const selection = await createStateRepository({
    preferredMode: selectedVolatile ? 'volatile-selected' : 'persistent',
  });
  const runtime = createModuleRuntime({
    moduleId,
    moduleVersion,
    targetStateSchemaVersion: 1,
    repository: selection.repository,
    migrations: [],
    clock: { now: () => new Date() },
    createWorkspaceId: randomWorkspaceId,
    exportPort: browserExportPort(workspace),
  });
  if (selection.warning) {
    showError(selection.warning);
  }
  const started = await runtime.start();
  if (!started.ok) {
    showError(started.error);
    return;
  }

  const renderPayload = (payload: Readonly<Record<string, unknown>>) => {
    textInput.value = typeof payload.text === 'string' ? payload.text : '';
    choiceInput.value = typeof payload.choice === 'string' ? payload.choice : '';
  };
  renderPayload(started.state.payload);

  const setStatus = (detail: StateStatusDetail) => {
    status.textContent = detail.message;
    announceState(document, detail);
  };
  let saveTimer: ReturnType<typeof setTimeout> | undefined;
  const updateRuntimePayload = () => runtime.updatePayload({
    text: textInput.value,
    choice: choiceInput.value,
  });
  const flush = async () => {
    if (saveTimer !== undefined) {
      clearTimeout(saveTimer);
      saveTimer = undefined;
    }
    updateRuntimePayload();
    setStatus({ state: 'saving', mode: selection.mode, message: 'Wird lokal gespeichert' });
    const result = await runtime.flush();
    if (!result.ok) {
      showError(result.error);
      return false;
    }
    setStatus({
      state: 'saved',
      mode: selection.mode,
      message: selection.mode === 'persistent'
        ? 'Lokal gespeichert'
        : 'Nur für diese Sitzung gespeichert',
    });
    announceDataChanged(document, { scope: 'module', operation: 'save' });
    return true;
  };
  const scheduleSave = () => {
    if (saveTimer !== undefined) {
      clearTimeout(saveTimer);
    }
    saveTimer = setTimeout(() => void flush(), SAVE_DELAY_MS);
  };
  textInput.addEventListener('input', scheduleSave);
  choiceInput.addEventListener('input', scheduleSave);
  textInput.addEventListener('change', () => void flush());
  choiceInput.addEventListener('change', () => void flush());
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      void flush();
    }
  });

  exportButton.addEventListener('click', async () => {
    if (await flush()) {
      const result = await runtime.exportState();
      if (!result.ok) {
        showError(result.error);
      }
    }
  });

  importInput.addEventListener('change', async () => {
    const file = importInput.files?.[0];
    if (!file) {
      return;
    }
    const preview = runtime.previewImport(new Uint8Array(await file.arrayBuffer()));
    if (!preview.ok) {
      showError(preview.error);
      importInput.value = '';
      return;
    }
    workspace.querySelector<HTMLElement>('[data-preview-module]')!.textContent = preview.preview.moduleId;
    workspace.querySelector<HTMLElement>('[data-preview-version]')!.textContent = preview.preview.moduleVersion;
    workspace.querySelector<HTMLElement>('[data-preview-saved]')!.textContent = preview.preview.savedAt;
    workspace.querySelector<HTMLElement>('[data-preview-fields]')!.textContent = preview.preview.payloadFields.join(', ');
    importDialog.showModal();
  });
  workspace.querySelector<HTMLButtonElement>('[data-import-cancel]')?.addEventListener('click', () => {
    importDialog.close();
    importInput.value = '';
    importInput.focus();
  });
  workspace.querySelector<HTMLButtonElement>('[data-import-confirm]')?.addEventListener('click', async () => {
    const result = await runtime.confirmImport();
    if (!result.ok) {
      showError(result.error);
      return;
    }
    renderPayload(result.state.payload);
    importDialog.close();
    importInput.value = '';
    setStatus({ state: 'imported', mode: selection.mode, message: 'Import lokal gespeichert' });
    announceDataChanged(document, { scope: 'module', operation: 'import' });
    workspace.querySelector<HTMLElement>('#fixture-title')?.focus();
  });

  deleteButton.addEventListener('click', () => deleteDialog.showModal());
  workspace.querySelector<HTMLButtonElement>('[data-delete-cancel]')?.addEventListener('click', () => {
    deleteDialog.close();
    deleteButton.focus();
  });
  workspace.querySelector<HTMLButtonElement>('[data-delete-confirm]')?.addEventListener('click', async () => {
    const deleted = await runtime.deleteActive();
    if (!deleted.ok) {
      showError(deleted.error);
      return;
    }
    const restarted = await runtime.start();
    if (!restarted.ok) {
      showError(restarted.error);
      return;
    }
    renderPayload(restarted.state.payload);
    deleteDialog.close();
    setStatus({ state: 'deleted', mode: selection.mode, message: 'Arbeitsstand gelöscht' });
    announceDataChanged(document, { scope: 'module', operation: 'delete' });
    workspace.querySelector<HTMLElement>('#fixture-title')?.focus();
  });

  setStatus({
    state: selection.mode === 'persistent' ? 'saved' : 'volatile',
    mode: selection.mode,
    message: selection.mode === 'persistent'
      ? 'Lokal gespeichert'
      : 'Nur für diese Sitzung gespeichert',
  });
}
