import { expect, test, type Page } from '@playwright/test';

async function fillAndConfirmPersistentSave(page: Page, value: string): Promise<void> {
  const input = page.getByLabel('Synthetischer Text');
  await input.fill(value);
  await input.dispatchEvent('change');
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
}

test('edit, reload, export, delete and import is lossless', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await page.getByLabel('Synthetischer Text').fill('Zustand A');
  await page.getByLabel('Synthetische Auswahl').selectOption('beta');
  await expect(page.getByRole('status')).toContainText('Lokal gespeichert');
  await page.reload();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Zustand A');
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Exportieren' }).click();
  const exportFile = await download;
  const exportPath = await exportFile.path();
  expect(exportPath).not.toBeNull();
  await page.getByRole('button', { name: 'Arbeitsstand löschen' }).click();
  await page.getByRole('button', { name: 'Löschen bestätigen' }).click();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('');
  await page.setInputFiles('input[type=file]', exportPath!);
  await page.getByRole('button', { name: 'Import übernehmen' }).click();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Zustand A');
  await expect(page.getByLabel('Synthetische Auswahl')).toHaveValue('beta');
});

test('selected volatile mode remains explicit', async ({ page }) => {
  await page.goto('/module/test-platform-reference/?storage=volatile');
  await page.getByLabel('Synthetischer Text').fill('Nur Sitzung');
  await expect(page.getByRole('status')).toContainText('Nur für diese Sitzung');
  await page.reload();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('');
});

test('wrong-module import is visible and leaves the active state unchanged', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await fillAndConfirmPersistentSave(page, 'Bleibt erhalten');
  const wrongModuleState = {
    format: 'ium-learning-state',
    formatVersion: 1,
    moduleId: 'TEST-OTHER-MODULE',
    moduleVersion: '1.0.0',
    stateSchemaVersion: 1,
    workspaceId: '423e4567-e89b-42d3-a456-426614174000',
    savedAt: '2026-08-03T12:00:00.000Z',
    payload: { text: 'Darf nicht hinein' },
  };
  await page.setInputFiles('input[type=file]', {
    name: 'wrong-module.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify(wrongModuleState)),
  });
  const errorSummary = page.getByRole('alert');
  await expect(errorSummary).toContainText(
    'Die Datei gehört zu einem anderen Lernmodul',
  );
  await expect(errorSummary).toBeFocused();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Bleibt erhalten');
});

test('global delete is confirmed and reread on the module route', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await fillAndConfirmPersistentSave(page, 'Global löschen');
  await page.goto('/daten/');
  await page.getByRole('button', { name: 'Alle lokalen Daten löschen' }).click();
  await page.getByRole('button', { name: 'Alle Daten löschen' }).click();
  await expect(page.locator('[data-storage-status]')).toContainText(
    'Alle lokalen Lernwerkdaten wurden gelöscht',
  );
  await page.goto('/module/test-platform-reference/');
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('');
});

test('sandboxed iframe exposes volatile mode and copy fallback', async ({ page }) => {
  const pageErrors: string[] = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  await page.setContent(
    '<iframe title="Eingebettetes Lernwerk" sandbox="allow-scripts allow-same-origin" '
      + 'src="http://127.0.0.1:4321/module/test-platform-reference/?storage=volatile"></iframe>',
  );
  const frame = page.frameLocator('iframe');
  await frame.getByLabel('Synthetischer Text').fill('Sandbox');
  await expect.poll(() => pageErrors).toEqual([]);
  await expect(frame.getByRole('status')).toContainText('Nur für diese Sitzung');
  await frame.getByRole('button', { name: 'Exportieren' }).click();
  await expect(frame.getByLabel('Export zum Kopieren')).toHaveValue(
    /"text": "Sandbox"/,
  );
});

test('fixture remains operable with keyboard only', async ({ page, browserName }) => {
  await page.goto('/module/test-platform-reference/');
  const skipLink = page.getByRole('link', { name: 'Zum Hauptinhalt' });
  if (browserName === 'webkit') {
    await expect(skipLink).toHaveAttribute('href', '#hauptinhalt');
    await page.locator('main').focus();
  } else {
    await page.keyboard.press('Tab');
    await expect(skipLink).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('main')).toBeFocused();
  }

  for (let index = 0; index < 20; index += 1) {
    if (await page.evaluate(() => document.activeElement?.id === 'fixture-text')) break;
    await page.keyboard.press('Tab');
  }
  await expect(page.getByLabel('Synthetischer Text')).toBeFocused();
  await page.keyboard.type('Tastatur');
  await page.keyboard.press('Tab');
  await expect(page.getByLabel('Synthetische Auswahl')).toBeFocused();
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('status')).toContainText('Lokal gespeichert');
});
