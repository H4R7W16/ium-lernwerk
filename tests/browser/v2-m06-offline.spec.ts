import { expect, test, type Page } from '@playwright/test';
import { openPersistent, reloadPersistent } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';

async function waitForOfflineReady(page: Page): Promise<void> {
  await expect(page.locator('[data-connection-status]')).toHaveAttribute('data-pwa-state', 'ready', {
    timeout: 20_000,
  });
  await reloadPersistent(page);
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
}

test('reopens the persistent M06 route offline with its dossier', async ({ context, page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByLabel('Begründung der Prüffahrt').fill('OFFLINE-P3');
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await waitForOfflineReady(page);
  await context.setOffline(true);
  await reloadPersistent(page);
  await expect(page.getByRole('heading', { name: 'Präzise Abläufe entwickeln und prüfen' })).toBeVisible();
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('OFFLINE-P3');
  await context.setOffline(false);
});

test('does not claim an uncached first visit works offline', async ({ browser }) => {
  const context = await browser.newContext({ baseURL: 'http://127.0.0.1:4324', offline: true });
  try {
    const page = await context.newPage();
    await expect(page.goto(moduleUrl, { waitUntil: 'domcontentloaded', timeout: 5_000 })).rejects.toThrow();
  } finally {
    await context.close();
  }
});

test('loads no third-party runtime resources', async ({ page }) => {
  const external: string[] = [];
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.origin !== 'http://127.0.0.1:4324') external.push(request.url());
  });
  await openPersistent(page, moduleUrl);
  expect(external).toEqual([]);
});
