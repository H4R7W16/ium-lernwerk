export function connectDataActionDialogs(root: ParentNode = document): void {
  const invokers = new WeakMap<HTMLDialogElement, HTMLElement>();

  for (const trigger of root.querySelectorAll<HTMLElement>('[data-data-action-open]')) {
    trigger.addEventListener('click', () => {
      const id = trigger.dataset.dataActionOpen;
      const dialog = id ? root.querySelector<HTMLDialogElement>(`#${CSS.escape(id)}`) : null;
      if (!dialog) {
        return;
      }
      invokers.set(dialog, trigger);
      dialog.showModal();
      dialog.querySelector<HTMLButtonElement>('[data-data-action-cancel]')?.focus();
    });
  }

  for (const dialog of root.querySelectorAll<HTMLDialogElement>('[data-data-action-dialog]')) {
    dialog.querySelector<HTMLButtonElement>('[data-data-action-cancel]')
      ?.addEventListener('click', () => dialog.close('cancel'));
    dialog.querySelector<HTMLButtonElement>('[data-data-action-confirm]')
      ?.addEventListener('click', () => dialog.close('confirm'));
    dialog.addEventListener('close', () => invokers.get(dialog)?.focus());
  }
}
