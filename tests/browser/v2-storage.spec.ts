import { expect, test } from '@playwright/test';
import { choosePersistent, chooseVolatile } from './helpers/storage-choice.js';

const probeUrl = '/tests/v2-runtime/';

test('does not open learning storage before a visible choice and asks again on reload', async ({ page }) => {
  await page.goto(probeUrl);
  await expect(page.getByRole('button', { name: 'Auf diesem Gerät speichern' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Nur in dieser Sitzung arbeiten' })).toBeVisible();
  const beforeChoice = await page.evaluate(async () => (
    await indexedDB.databases()
  ).map(({ name }) => name));
  expect(beforeChoice).not.toContain('ium-lernwerk-v2');

  await choosePersistent(page);
  await expect(page.locator('[data-probe-status]')).toHaveText('V2-Profilstand geöffnet');
  await page.reload();
  await expect(page.getByRole('button', { name: 'Auf diesem Gerät speichern' })).toBeVisible();
});

test('opens both database spaces on the management page only after confirmation', async ({ page }) => {
  await page.goto('/daten/');
  const beforeDialog = await page.evaluate(async () => (
    await indexedDB.databases()
  ).map(({ name }) => name));
  expect(beforeDialog).not.toContain('ium-lernwerk');
  expect(beforeDialog).not.toContain('ium-lernwerk-v2');
  await page.getByRole('button', { name: 'Alle lokalen Daten löschen' }).first().click();
  const beforeConfirmation = await page.evaluate(async () => (
    await indexedDB.databases()
  ).map(({ name }) => name));
  expect(beforeConfirmation).not.toContain('ium-lernwerk');
  expect(beforeConfirmation).not.toContain('ium-lernwerk-v2');
  await page.getByRole('button', { name: 'Alle Daten löschen' }).click();
  await expect(page.locator('[data-delete-all-result]')).toContainText('V1- und V2-Arbeitsstände');
  expect(await page.evaluate(async () => (
    await indexedDB.databases()
  ).map(({ name }) => name))).toEqual(expect.arrayContaining([
    'ium-lernwerk',
    'ium-lernwerk-v2',
  ]));
});

test('invalidates an open volatile client and reports its confirmation', async ({ context, page }) => {
  await page.goto(probeUrl);
  await chooseVolatile(page);
  await page.getByLabel('Synthetischer Text').fill('flüchtig geöffnet');
  await page.getByRole('button', { name: 'Speichern' }).click();

  const management = await context.newPage();
  await management.goto('/daten/');
  await management.getByRole('button', { name: 'Alle lokalen Daten löschen' }).first().click();
  await management.getByRole('button', { name: 'Alle Daten löschen' }).click();
  await expect(management.locator('[data-invalidation-result]')).toContainText('1 offene Lernseite');
  await expect(page.locator('[data-probe-status]')).toHaveText('Lokale Profildaten gelöscht');
  await expect(page.getByLabel('Synthetischer Text')).toBeDisabled();
  await expect(page.getByRole('alert')).toContainText('speichert nicht weiter');
});

test('protects two pages in one profile and separates another browser profile', async ({ browser, context, page }) => {
  const sibling = await context.newPage();
  await page.goto(probeUrl);
  await choosePersistent(page);
  await sibling.goto(probeUrl);
  await choosePersistent(sibling);

  await page.getByLabel('Synthetischer Text').fill('Seite A');
  await page.getByRole('button', { name: 'Speichern' }).click();
  await expect(page.locator('[data-probe-status]')).toHaveText('Lokal gespeichert');
  await sibling.getByLabel('Synthetischer Text').fill('Seite B bleibt erhalten');
  await sibling.getByRole('button', { name: 'Speichern' }).click();
  await expect(sibling.getByRole('alert')).toContainText('inzwischen an anderer Stelle geändert');
  await expect(sibling.getByLabel('Synthetischer Text')).toHaveValue('Seite B bleibt erhalten');

  const reopened = await context.newPage();
  await reopened.goto(probeUrl);
  await choosePersistent(reopened);
  await expect(reopened.getByLabel('Synthetischer Text')).toHaveValue('Seite A');

  const isolatedContext = await browser.newContext({ baseURL: 'http://127.0.0.1:4321' });
  try {
    const isolated = await isolatedContext.newPage();
    await isolated.goto(probeUrl);
    await choosePersistent(isolated);
    await expect(isolated.getByLabel('Synthetischer Text')).toHaveValue('');
  } finally {
    await isolatedContext.close();
  }
});

test('keeps volatile work out of IndexedDB and clears it on reload', async ({ page }) => {
  await page.goto(probeUrl);
  await chooseVolatile(page);
  await page.getByLabel('Synthetischer Text').fill('nur Sitzung');
  await page.getByRole('button', { name: 'Speichern' }).click();
  await expect(page.locator('[data-probe-status]')).toHaveText('Nur für diese Sitzung gespeichert');
  const databases = await page.evaluate(async () => (
    await indexedDB.databases()
  ).map(({ name }) => name));
  expect(databases).not.toContain('ium-lernwerk-v2');
  await page.reload();
  await chooseVolatile(page);
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('');
});

test('global deletion advances the generation and a stale page cannot revive data', async ({ context, page }) => {
  await page.goto(`${probeUrl}?broadcast=off`);
  await choosePersistent(page);
  await page.getByLabel('Synthetischer Text').fill('vor Löschung');
  await page.getByRole('button', { name: 'Speichern' }).click();

  const stale = await context.newPage();
  await stale.goto(`${probeUrl}?broadcast=off`);
  await choosePersistent(stale);
  await expect(stale.getByLabel('Synthetischer Text')).toHaveValue('vor Löschung');

  const management = await context.newPage();
  await management.goto('/daten/');
  await management.getByRole('button', { name: 'Alle lokalen Daten löschen' }).first().click();
  await management.getByRole('button', { name: 'Alle Daten löschen' }).click();
  await expect(management.locator('[data-delete-all-result]')).toContainText('V1- und V2-Arbeitsstände');
  await expect(management.locator('[data-invalidation-result]')).toContainText('Keine Bestätigung');

  await stale.getByLabel('Synthetischer Text').fill('Wiederbelebungsversuch');
  await stale.getByRole('button', { name: 'Speichern' }).click();
  await expect(stale.getByRole('alert')).toContainText('inzwischen an anderer Stelle geändert oder gelöscht');
  await expect(stale.getByLabel('Synthetischer Text')).toHaveValue('Wiederbelebungsversuch');

  const reopened = await context.newPage();
  await reopened.goto(probeUrl);
  await choosePersistent(reopened);
  await expect(reopened.getByLabel('Synthetischer Text')).toHaveValue('');
});

test('reports blocked IndexedDB and quota failures without claiming persistence', async ({ page }) => {
  await page.goto(`${probeUrl}?idb=blocked`);
  await choosePersistent(page);
  await expect(page.getByRole('alert')).toContainText('Dauerhaftes lokales Speichern ist nicht verfügbar');
  await expect(page.locator('[data-probe-status]')).toHaveText('Flüchtige V2-Sitzung geöffnet');

  await page.goto(`${probeUrl}?save=quota`);
  await choosePersistent(page);
  await page.getByLabel('Synthetischer Text').fill('zu groß');
  await page.getByRole('button', { name: 'Speichern' }).click();
  await expect(page.getByRole('alert')).toContainText('Speicherplatz reicht nicht aus');
  await expect(page.locator('[data-probe-status]')).toHaveText('Kein lokaler Stand gespeichert');
});

test('writes to the clipboard only after the dedicated button and makes no external request', async ({ context, page }) => {
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: {
        writeText: async () => {
          const scope = window as typeof window & { __clipboardCalls?: number };
          scope.__clipboardCalls = (scope.__clipboardCalls ?? 0) + 1;
        },
      },
    });
    (window as typeof window & { __clipboardCalls?: number }).__clipboardCalls = 0;
  });
  const externalRequests: string[] = [];
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.origin !== 'http://127.0.0.1:4321') externalRequests.push(request.url());
  });
  await page.goto(`${probeUrl}?download=blocked`);
  await choosePersistent(page);
  await page.getByLabel('Synthetischer Text').fill('bewusste Ausgabe');
  await page.getByRole('button', { name: 'Export anfordern' }).click();
  await expect(page.locator('[data-copy-fallback]')).toBeVisible();
  expect(await page.evaluate(() => (
    window as typeof window & { __clipboardCalls?: number }
  ).__clipboardCalls)).toBe(0);
  await page.getByRole('button', { name: 'In Zwischenablage kopieren' }).click();
  expect(await page.evaluate(() => (
    window as typeof window & { __clipboardCalls?: number }
  ).__clipboardCalls)).toBe(1);
  expect(externalRequests).toEqual([]);
});
