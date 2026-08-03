import {
  announceDataChanged,
  announceError,
  announceState,
} from './status-announcer.js';

type DataControlDependencies = Readonly<{
  mode: 'persistent' | 'volatile-selected' | 'volatile-fallback';
  warning?: ErrorDetail;
  deleteAll(): Promise<
    | Readonly<{ ok: true; deleted: boolean }>
    | Readonly<{ ok: false; error: ErrorDetail }>
  >;
}>;

export async function connectGlobalDataControls(
  dependencies: DataControlDependencies,
  root: ParentNode = document,
): Promise<void> {
  const deleteButton = root.querySelector<HTMLButtonElement>('[data-delete-all]');
  const dialog = root.querySelector<HTMLDialogElement>('[data-delete-all-dialog]');
  const confirm = root.querySelector<HTMLButtonElement>('[data-delete-all-confirm]');
  const cancel = root.querySelector<HTMLButtonElement>('[data-delete-all-cancel]');
  if (!deleteButton || !dialog || !confirm || !cancel) {
    return;
  }
  if (dependencies.warning) {
    announceError(document, dependencies.warning);
  }
  announceState(document, {
    state: dependencies.mode === 'persistent' ? 'saved' : 'volatile',
    mode: dependencies.mode,
    message: dependencies.mode === 'persistent'
      ? 'Dauerhafter lokaler Speicher verfügbar'
      : 'Nur diese Sitzung',
  });

  deleteButton.addEventListener('click', () => dialog.showModal());
  cancel.addEventListener('click', () => {
    dialog.close();
    deleteButton.focus();
  });
  confirm.addEventListener('click', async () => {
    const result = await dependencies.deleteAll();
    if (!result.ok) {
      announceError(document, result.error);
      return;
    }
    dialog.close();
    announceDataChanged(document, { scope: 'all', operation: 'delete' });
    announceState(document, {
      state: 'deleted',
      mode: dependencies.mode,
      message: 'Alle lokalen Lernwerkdaten wurden gelöscht',
    });
    document.querySelector<HTMLElement>('h1')?.focus();
  });
}
