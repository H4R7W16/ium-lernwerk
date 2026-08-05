import { expect, test, type Page } from '@playwright/test';

async function openModule(page: Page): Promise<void> {
  await page.goto('/module/ium-5-core-05/');
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute(
    'data-initialization-state',
    /ready|blocked/,
  );
}

async function seedMeaningfulState(page: Page): Promise<void> {
  await openModule(page);
  await page.getByRole('button', { name: 'Mit der Vermutung beginnen' }).click();
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.reload();
}

test('starts with purpose and exactly one primary action', async ({ page }) => {
  await openModule(page);

  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Algorithmen untersuchen');
  await expect(page.getByRole('button', { name: 'Mit der Vermutung beginnen' })).toHaveCount(1);
  await expect(page.getByRole('main').getByRole('button')).toHaveCount(1);

  await page.getByRole('button', { name: 'Mit der Vermutung beginnen' }).click();
  await expect(page.locator('[data-experience-content]')).toBeVisible();
  await expect(page.locator('#workbench-title')).toBeFocused();
});

test('offers resume before reset without exposing stored answers', async ({ page }) => {
  await seedMeaningfulState(page);

  await expect(page.getByRole('button', { name: 'Weiterarbeiten' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Neu beginnen' })).toBeVisible();
  await expect(page.locator('[data-resume-prompt]')).not.toContainText(/Versuch|Prozent|Punkt/i);
  await expect(page.getByText('Vorhersage bilden')).toBeVisible();
});

test('cancels reset without changing work and returns focus', async ({ page }) => {
  await seedMeaningfulState(page);
  const reset = page.getByRole('button', { name: 'Neu beginnen' });
  await reset.click();

  await expect(page.getByRole('dialog', { name: 'Diesen Modulstand neu beginnen?' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Abbrechen' })).toBeFocused();
  await page.getByRole('button', { name: 'Abbrechen' }).click();
  await expect(reset).toBeFocused();

  await page.getByRole('button', { name: 'Weiterarbeiten' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem')).toHaveCount(1);
});

test('confirmed reset clears only IUM5 and returns to the clean start', async ({ page }) => {
  await seedMeaningfulState(page);
  await page.evaluate(async () => {
    const request = indexedDB.open('ium-lernwerk', 1);
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    const transaction = database.transaction('activeStates', 'readwrite');
    transaction.objectStore('activeStates').put({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'TEST-SENTINEL',
      moduleVersion: '1.0.0',
      stateSchemaVersion: 1,
      workspaceId: '11111111-1111-4111-8111-111111111111',
      savedAt: new Date(0).toISOString(),
      payload: { sentinel: true },
    });
    await new Promise<void>((resolve, reject) => {
      transaction.oncomplete = () => resolve();
      transaction.onerror = () => reject(transaction.error);
    });
    database.close();
  });

  await page.getByRole('button', { name: 'Neu beginnen' }).click();
  await page.getByRole('button', { name: 'Modulstand endgültig zurücksetzen' }).click();

  await expect(page.getByRole('button', { name: 'Mit der Vermutung beginnen' })).toBeFocused();
  const records = await page.evaluate(async () => {
    const request = indexedDB.open('ium-lernwerk', 1);
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    const transaction = database.transaction('activeStates', 'readonly');
    const store = transaction.objectStore('activeStates');
    const read = (key: string) => new Promise<any>((resolve, reject) => {
      const item = store.get(key);
      item.onsuccess = () => resolve(item.result);
      item.onerror = () => reject(item.error);
    });
    const result = {
      ium5: await read('IUM-5-CORE-05'),
      sentinel: await read('TEST-SENTINEL'),
    };
    database.close();
    return result;
  });
  expect(records.ium5.payload.initialAlgorithm).toEqual([]);
  expect(records.sentinel.payload).toEqual({ sentinel: true });
});
