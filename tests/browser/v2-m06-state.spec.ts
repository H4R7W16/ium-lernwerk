import { expect, test, type Page } from '@playwright/test';
import { choosePersistent, openPersistent, reloadPersistent } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';

async function saveP3(page: Page, text: string): Promise<void> {
  await page.getByLabel('Begründung der Prüffahrt').fill(text);
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gespeichert.');
}

test('P4 is not restored from the dossier and P3 remains editable', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('SYNTHETIC-P4-SENTINEL');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).click();
  await saveP3(page, 'SYNTHETIC-P3-SENTINEL');
  await reloadPersistent(page);
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('SYNTHETIC-P3-SENTINEL');
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await expect(page.getByLabel('Deine Abrufbegründung')).toHaveValue('');
});

test('keeps P0 and P4 sentinels out of the stored envelope and conscious export', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByLabel('Meine Vorhersage vor dem Ausführen').fill('SYNTHETIC-P0-SENTINEL');
  await page.getByRole('button', { name: 'Abruf öffnen' }).click();
  await page.getByLabel('Deine Abrufbegründung').fill('SYNTHETIC-P4-SENTINEL');
  await saveP3(page, 'SYNTHETIC-P3-SENTINEL');
  const stored = await page.evaluate(async () => {
    const request = indexedDB.open('ium-lernwerk-v2');
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    const names = [...database.objectStoreNames];
    const rows: unknown[] = [];
    for (const name of names) {
      const transaction = database.transaction(name, 'readonly');
      const values = await new Promise<unknown[]>((resolve, reject) => {
        const query = transaction.objectStore(name).getAll();
        query.onsuccess = () => resolve(query.result);
        query.onerror = () => reject(query.error);
      });
      rows.push(...values);
    }
    database.close();
    return JSON.stringify(rows);
  });
  expect(stored).toContain('SYNTHETIC-P3-SENTINEL');
  expect(stored).not.toContain('SYNTHETIC-P0-SENTINEL');
  expect(stored).not.toContain('SYNTHETIC-P4-SENTINEL');

  await page.getByText('Daten verwalten').click();
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const path = await (await download).path();
  expect(path).not.toBeNull();
  const exported = await (await import('node:fs/promises')).readFile(path!, 'utf8');
  expect(exported).toContain('SYNTHETIC-P3-SENTINEL');
  expect(exported).not.toContain('SYNTHETIC-P0-SENTINEL');
  expect(exported).not.toContain('SYNTHETIC-P4-SENTINEL');
});

test('rejects a damaged import without replacing a valid active dossier', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await saveP3(page, 'VALID-ACTIVE-DOSSIER');
  await page.getByText('Daten verwalten').click();
  await page.getByLabel('Arbeitsstand importieren').setInputFiles({
    name: 'damaged.json',
    mimeType: 'application/json',
    buffer: Buffer.from('{"schemaVersion":999,"payload":{"p3":"broken"}}'),
  });
  await expect(page.locator('[data-m06-save-status]')).not.toHaveText('Importierter Arbeitsstand gespeichert.');
  await reloadPersistent(page);
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('VALID-ACTIVE-DOSSIER');
});

test('reports a conflict between two pages and prevents revival after deletion', async ({ context, page }) => {
  await openPersistent(page, moduleUrl);
  const sibling = await context.newPage();
  await sibling.goto(moduleUrl);
  await choosePersistent(sibling);
  await saveP3(page, 'PAGE-A');
  await sibling.getByLabel('Begründung der Prüffahrt').fill('PAGE-B');
  await sibling.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(sibling.locator('[data-m06-save-status]')).toContainText(/geändert|gelöscht/);

  page.on('dialog', (dialog) => dialog.accept());
  await page.getByText('Daten verwalten').click();
  await page.getByRole('button', { name: 'Arbeitsstand dieses Moduls löschen' }).click();
  await expect(page.locator('[data-m06-save-status]')).toHaveText('Arbeitsstand gelöscht.');
  await sibling.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await expect(sibling.locator('[data-m06-save-status]')).toContainText(/geändert|gelöscht/);
});
