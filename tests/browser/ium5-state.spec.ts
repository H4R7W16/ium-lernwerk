import { readFile } from 'node:fs/promises';
import { expect, test } from '@playwright/test';

test('reload, export, delete and import preserve only the learning product', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.reload();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);

  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand exportieren' }).click();
  const path = await (await download).path();
  expect(path).not.toBeNull();
  const exported = JSON.parse(await readFile(path!, 'utf8'));
  expect(Object.keys(exported.payload).sort()).toEqual([
    'evidenceTrace', 'initialAlgorithm', 'loopDecision', 'phaseId', 'prediction',
    'repairHypothesis', 'repairSource', 'revisedAlgorithm', 'scenarioId',
    'selfCheck', 'systemClassifications',
  ]);
  expect(JSON.stringify(exported.payload)).not.toMatch(
    /elapsed|attempt|click|hint|playback|focus|navigation/i,
  );

  await page.getByRole('button', { name: 'Arbeitsstand löschen' }).click();
  await page.getByRole('button', { name: 'Löschen bestätigen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(0);
  await page.setInputFiles('input[type=file]', path!);
  await page.getByRole('button', { name: 'Import übernehmen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});

test('rejects a malformed module payload without changing active work', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await page.setInputFiles('input[type=file]', {
    name: 'invalid.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'IUM-5-CORE-05',
      moduleVersion: '0.1.0',
      stateSchemaVersion: 1,
      workspaceId: '11111111-1111-4111-8111-111111111111',
      savedAt: '2026-08-03T00:00:00.000Z',
      payload: { name: 'Person' },
    })),
  });
  await expect(page.getByRole('heading', { name: 'Import prüfen' })).toBeHidden();
  await expect(page.getByRole('alert')).toContainText('nicht übernommen');
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});

test('rejects a future module schema without changing active work', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await page.setInputFiles('input[type=file]', {
    name: 'future.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'IUM-5-CORE-05',
      moduleVersion: '0.1.0',
      stateSchemaVersion: 2,
      workspaceId: '11111111-1111-4111-8111-111111111111',
      savedAt: '2026-08-03T00:00:00.000Z',
      payload: {},
    })),
  });
  await expect(page.getByRole('heading', { name: 'Import prüfen' })).toBeHidden();
  await expect(page.getByRole('alert')).toContainText('nicht übernommen');
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});
