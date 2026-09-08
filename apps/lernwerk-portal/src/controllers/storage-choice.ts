export type StorageChoice = 'persistent' | 'volatile-selected';

export function chooseStorage(root: HTMLElement): Promise<StorageChoice> {
  const container = document.createElement('section');
  container.dataset.storageChoice = '';
  container.setAttribute('aria-labelledby', 'storage-choice-title');
  container.innerHTML = `
    <h2 id="storage-choice-title">Wie möchtest du deinen Arbeitsstand speichern?</h2>
    <p>Du entscheidest bei jedem Besuch neu. Ein bestehender Stand in diesem Browserprofil wird erst nach deiner Wahl geöffnet.</p>
    <div class="actions">
      <button type="button" data-storage-persistent>Auf diesem Gerät speichern</button>
      <button type="button" data-storage-volatile>Nur in dieser Sitzung arbeiten</button>
    </div>
  `;
  root.parentElement?.insertBefore(container, root);
  const persistent = container.querySelector<HTMLButtonElement>('[data-storage-persistent]');
  const volatile = container.querySelector<HTMLButtonElement>('[data-storage-volatile]');
  if (!persistent || !volatile) {
    container.remove();
    throw new Error('Storage choice controls could not be created');
  }
  persistent.focus();
  return new Promise((resolve) => {
    const finish = (choice: StorageChoice) => {
      container.remove();
      resolve(choice);
    };
    persistent.addEventListener('click', () => finish('persistent'), { once: true });
    volatile.addEventListener('click', () => finish('volatile-selected'), { once: true });
  });
}
