import {
  IndexedDbStateRepository,
  VersionedIndexedDbStateRepository,
} from '@ium/local-state';

export type LocalDataDeletionResult = Readonly<{
  ok: boolean;
  v1: 'deleted' | 'failed';
  v2: 'deleted' | 'failed';
}>;

export type InvalidationSummary = Readonly<{
  confirmations: number;
}>;

let lastInvalidationSummary: InvalidationSummary = { confirmations: 0 };

async function invalidateOpenClients(): Promise<InvalidationSummary> {
  if (typeof BroadcastChannel === 'undefined') {
    return { confirmations: 0 };
  }
  const requestId = crypto.randomUUID();
  const channel = new BroadcastChannel('ium-local-data-v2');
  const clients = new Set<string>();
  channel.addEventListener('message', (event: MessageEvent<unknown>) => {
    const value = event.data as { type?: string; requestId?: string; clientId?: string };
    if (
      value.type === 'invalidated'
      && value.requestId === requestId
      && typeof value.clientId === 'string'
    ) {
      clients.add(value.clientId);
    }
  });
  channel.postMessage({ type: 'invalidate', requestId });
  await new Promise((resolve) => setTimeout(resolve, 250));
  channel.close();
  return { confirmations: clients.size };
}

export function getLastInvalidationSummary(): InvalidationSummary {
  return lastInvalidationSummary;
}

export async function deleteAllLocalLearningData(): Promise<LocalDataDeletionResult> {
  const indexedDbFactory = globalThis.indexedDB;
  const deleteV1 = async (): Promise<'deleted' | 'failed'> => {
    try {
      const repository = await IndexedDbStateRepository.open({ indexedDbFactory });
      return (await repository.deleteAll()).ok ? 'deleted' : 'failed';
    } catch {
      return 'failed';
    }
  };
  const deleteV2 = async (): Promise<'deleted' | 'failed'> => {
    try {
      const repository = await VersionedIndexedDbStateRepository.open({ indexedDbFactory });
      return (await repository.deleteAll()).ok ? 'deleted' : 'failed';
    } catch {
      return 'failed';
    }
  };
  const [v1, v2] = await Promise.all([deleteV1(), deleteV2()]);
  lastInvalidationSummary = await invalidateOpenClients();
  return { ok: v1 === 'deleted' && v2 === 'deleted', v1, v2 };
}

export async function connectLocalDataV2(root: ParentNode = document): Promise<void> {
  const deleteButton = root.querySelector<HTMLButtonElement>('[data-delete-all]');
  const dialog = root.querySelector<HTMLDialogElement>('[data-delete-all-dialog]');
  const confirm = root.querySelector<HTMLButtonElement>('[data-delete-all-confirm]');
  const cancel = root.querySelector<HTMLButtonElement>('[data-delete-all-cancel]');
  const resultText = root.querySelector<HTMLElement>('[data-delete-all-result]');
  const invalidationText = root.querySelector<HTMLElement>('[data-invalidation-result]');
  if (!deleteButton || !dialog || !confirm || !cancel || !resultText || !invalidationText) {
    return;
  }
  deleteButton.addEventListener('click', () => dialog.showModal());
  cancel.addEventListener('click', () => {
    dialog.close();
    deleteButton.focus();
  });
  confirm.addEventListener('click', async () => {
    confirm.disabled = true;
    const result = await deleteAllLocalLearningData();
    confirm.disabled = false;
    dialog.close();
    const resultLabel = (value: 'deleted' | 'failed') => value === 'deleted'
      ? 'gelöscht'
      : 'fehlgeschlagen';
    resultText.textContent = result.ok
      ? 'Die lokalen V1- und V2-Arbeitsstände dieses Browserprofils und dieser Origin wurden gelöscht.'
      : `Löschung nur teilweise abgeschlossen: V1 ${resultLabel(result.v1)}, V2 ${resultLabel(result.v2)}. Wiederhole die Aktion.`;
    const { confirmations } = getLastInvalidationSummary();
    invalidationText.textContent = confirmations > 0
      ? `${confirmations} offene Lernseite(n) haben die Löschung bestätigt.`
      : 'Keine Bestätigung anderer offener Lernseiten empfangen. Offene Seiten müssen neu geladen werden.';
    document.querySelector<HTMLElement>('h1')?.focus();
  });
}
