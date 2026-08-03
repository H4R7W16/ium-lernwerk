import { expect, test } from '@playwright/test';

test('builds an algorithm by buttons and requires a prediction before execution', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Nimm auf einfügen' }).click();
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(
    page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'),
  ).toHaveCount(2);
  await page.getByRole('button', { name: 'Befehl 2 nach oben' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' }))
    .toBeDisabled();
  await page.getByLabel('Erwartete Endposition').selectOption('A3');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('north');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('unsure');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await expect(page.getByRole('button', { name: 'Schritt ausführen' }))
    .toBeEnabled();
  await expect(page.locator('[data-prediction-status]')).toContainText(
    'Vorhersage gespeichert – jetzt prüfen',
  );
});
