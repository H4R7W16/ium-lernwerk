import { expect, test, type Page } from '@playwright/test';

async function enterExperience(page: Page): Promise<void> {
  await page.getByRole('button', { name: /Mit der Vermutung beginnen|Weiterarbeiten/ }).click();
}

async function activePayload(page: Page): Promise<unknown> {
  return page.evaluate(async () => {
    const database = await new Promise<IDBDatabase>((resolve, reject) => {
      const request = indexedDB.open('ium-lernwerk', 1);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    return new Promise((resolve, reject) => {
      const transaction = database.transaction('activeStates', 'readonly');
      const request = transaction.objectStore('activeStates').get('IUM-5-CORE-05');
      request.onsuccess = () => resolve(request.result?.payload ?? null);
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => database.close();
    });
  });
}

test('supports local checkpoints, keyboard role exchange and either release path without persistence', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await enterExperience(page);
  await expect(page.locator('[data-teacher-checkpoint]')).toHaveCount(2);
  await expect(page.getByText(/ohne Lernendenkonto, Fernsteuerung oder Datenübertragung/i).first()).toBeVisible();

  const roleExchange = page.locator('[data-role-exchange]').first();
  await expect(roleExchange.locator('[data-role-primary]')).toHaveText('Erklären');
  await expect(roleExchange.locator('[data-role-secondary]')).toHaveText('Prüfen');
  const swap = roleExchange.getByRole('button', { name: /Rollen tauschen/i });
  await swap.focus();
  await page.keyboard.press('Enter');
  await expect(swap).toBeFocused();
  await expect(roleExchange.locator('[data-role-primary]')).toHaveText('Prüfen');
  await expect(roleExchange.locator('[data-role-secondary]')).toHaveText('Erklären');

  const before = await activePayload(page);
  const forbiddenRequests: string[] = [];
  page.on('request', (request) => {
    if (/analytics|telemetry|teacher|checkpoint/i.test(request.url())) forbiddenRequests.push(request.url());
  });
  const sharedHold = page.locator('[data-shared-hold]').first();
  await sharedHold.getByRole('button', { name: 'Gemeinsam besprechen' }).click();
  await expect(sharedHold.getByRole('status')).toContainText('gemeinsame Besprechung');
  expect(await activePayload(page)).toEqual(before);
  await sharedHold.getByRole('button', { name: 'Ohne gemeinsame Besprechung fortfahren' }).click();
  await expect(sharedHold.getByRole('status')).toContainText('selbstständig');
  expect(await activePayload(page)).toEqual(before);
  expect(forbiddenRequests).toEqual([]);

  await expect(page.locator('[data-connection-status]')).toHaveAttribute('data-pwa-state', 'ready', { timeout: 20_000 });
  await page.reload();
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
  await context.setOffline(true);
  await page.reload();
  await enterExperience(page);
  const offlineHold = page.locator('[data-shared-hold]').last();
  await offlineHold.getByRole('button', { name: 'Ohne gemeinsame Besprechung fortfahren' }).click();
  await expect(offlineHold.getByRole('status')).toContainText('selbstständig');
  expect(await activePayload(page)).toEqual(before);
  await context.setOffline(false);
});
