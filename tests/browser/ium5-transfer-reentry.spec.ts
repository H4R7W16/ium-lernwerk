import { readFile } from 'node:fs/promises';
import { expect, test, type Page } from '@playwright/test';

async function enterExperience(page: Page): Promise<void> {
  await page.getByRole('button', { name: /Mit der Vermutung beginnen|Weiterarbeiten/ }).click();
}

async function waitForOfflineReady(page: Page): Promise<void> {
  await expect(page.locator('[data-connection-status]')).toHaveAttribute(
    'data-pwa-state',
    'ready',
    { timeout: 20_000 },
  );
  await page.reload();
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
}

test('persists a minimal evidence card and requires free recall before comparison', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await enterExperience(page);
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill('Die Wiederholungszahl ist zu klein.');
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('F2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('yes');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();

  const keyStatement = 'Eine gezielte Revision folgt aus der ersten belegten Abweichung.';
  await page.getByLabel('Quelle', { exact: true }).selectOption('error-repeat-count');
  await page.getByLabel('Beleg', { exact: true }).selectOption('trace:first-deviation');
  await page.getByLabel('Deutung', { exact: true }).fill('Die Spur endet zu früh, weil ein Wiederholungsschritt fehlt.');
  await page.getByLabel('Überarbeitung', { exact: true }).fill('Die Wiederholungszahl wird von vier auf fünf erhöht.');
  await page.getByLabel('Kernaussage', { exact: true }).fill(keyStatement);
  await page.getByLabel('Modellgrenze', { exact: true }).fill('Die Laufspur belegt nur den ausgeführten deterministischen Ablauf.');
  await page.getByRole('button', { name: 'Belegkarte bestätigen' }).click();
  await expect(page.locator('[data-evidence-card-status]')).toContainText('vorgemerkt');
  await expect(page.locator('[data-transfer-card-link]')).toContainText(keyStatement);

  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Eine eindeutige Folge von Anweisungen verarbeitet die Wegdaten.',
  );
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'reentry');
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');

  await waitForOfflineReady(page);
  await context.setOffline(true);
  await page.reload();
  await enterExperience(page);
  await expect(page.locator('[data-reentry-recall]')).toBeVisible();
  await expect(page.locator('[data-reentry-key-statement]')).toBeEmpty();
  await expect(page.locator('[data-reentry-card]')).toBeHidden();
  await page.getByLabel('Was weißt du noch?').fill('Abweichung lokalisieren und die Änderung daran begründen.');
  await page.getByRole('button', { name: 'Eigene Erinnerung festhalten' }).click();
  await expect(page.locator('[data-reentry-key-statement]')).toBeEmpty();
  await page.getByRole('button', { name: 'Mit der gespeicherten Kernaussage vergleichen' }).click();
  await expect(page.locator('[data-reentry-card]')).toContainText(keyStatement);
  await context.setOffline(false);

  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const exportedPath = await (await download).path();
  expect(exportedPath).not.toBeNull();
  const exported = JSON.parse(await readFile(exportedPath!, 'utf8')) as {
    stateSchemaVersion: number;
    payload: Record<string, unknown> & { evidenceCard: Record<string, unknown> };
  };
  expect(exported.stateSchemaVersion).toBe(2);
  expect(Object.keys(exported.payload.evidenceCard).sort()).toEqual([
    'evidenceRef',
    'interpretation',
    'keyStatement',
    'modelBoundary',
    'revision',
    'sourceRef',
  ]);
  expect(JSON.stringify(exported.payload.evidenceCard)).not.toMatch(
    /traceEntries|timestamp|user|name|elapsed|attempt|click|hint|score|metric/i,
  );
  expect(JSON.stringify(exported.payload)).not.toMatch(/user|name|elapsed|attempt|click|hint|score|metric/i);

  await page.getByRole('button', { name: 'Arbeitsstand löschen' }).click();
  await page.getByRole('button', { name: 'Löschen bestätigen' }).click();
  await expect(page.getByLabel('Quelle', { exact: true })).toHaveValue('');
  await expect(page.locator('[data-reentry-recall]')).toBeHidden();
  await page.setInputFiles('input[type=file]', exportedPath!);
  await page.getByRole('button', { name: 'Import übernehmen' }).click();
  await expect(page.locator('[data-reentry-recall]')).toBeVisible();
  await expect(page.locator('[data-reentry-key-statement]')).toBeEmpty();

  await page.setViewportSize({ width: 320, height: 900 });
  expect(await page.evaluate(
    () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
  )).toBe(true);
  await page.setViewportSize({ width: 640, height: 900 });
  await page.evaluate(() => document.documentElement.style.setProperty('zoom', '2'));
  expect(await page.evaluate(
    () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
  )).toBe(true);
});
