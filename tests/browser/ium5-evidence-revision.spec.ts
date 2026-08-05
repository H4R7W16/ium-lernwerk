import { expect, test, type Page } from '@playwright/test';

async function openWorkbench(page: Page): Promise<void> {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: /Mit der Vermutung beginnen|Weiterarbeiten/ }).click();
}

async function confirmPrediction(page: Page, position: string, direction: string, success: string): Promise<void> {
  await page.getByLabel('Erwartete Endposition').selectOption(position);
  await page.getByLabel('Erwartete Blickrichtung').selectOption(direction);
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption(success);
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
}

test('completes the evidence-led revision cycle with keyboard-operable stages', async ({ page }) => {
  await openWorkbench(page);
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem')).toHaveCount(1);

  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await expect(page.getByRole('button', { name: 'Vollständig ausführen' })).toBeDisabled();
  await page.locator('[data-run-all]').evaluate((button) => {
    (button as HTMLButtonElement).disabled = false;
    (button as HTMLButtonElement).click();
  });
  await expect(page.locator('[data-prediction-status]')).toContainText('Vorhersage erforderlich');

  await confirmPrediction(page, 'E2', 'east', 'no');
  await expect(page.locator('#workbench-title')).toBeFocused();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.locator('#workbench-title')).toBeFocused();
  await expect(page.getByRole('table', { name: 'Laufspur' })).toContainText('Vorherzustand');
  const feedback = page.locator('[data-evidence-feedback]');
  await expect(feedback).toContainText('Beleg');
  await expect(feedback).toContainText('Kriterium');
  await expect(feedback).toContainText('Deute');
  await expect(feedback).toContainText('Prüfe als Nächstes');

  const evidence = page.getByRole('radio', { name: /erster abweichender Schritt/i }).first();
  await evidence.check();
  await page.getByLabel('Reparaturhypothese').fill('Die Wiederholungszahl ist zu klein.');
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await expect(page.locator('#workbench-title')).toBeFocused();
  await expect(page.locator('[data-trace-table] tbody tr[aria-current="step"]')).toContainText('cmd-');

  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  const comparison = page.locator('[data-revision-compare]');
  await expect(comparison.getByRole('heading', { name: 'Vorher' })).toBeVisible();
  await expect(comparison.getByRole('heading', { name: 'Nachher' })).toBeVisible();
  await expect(comparison.locator('[data-revision-summary]')).not.toBeEmpty();

  await confirmPrediction(page, 'F2', 'east', 'yes');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' })).not.toHaveText('Noch keine Ausführung.');
});

test('keeps support escalation explicit and user controlled', async ({ page }) => {
  await openWorkbench(page);
  const operation = page.getByRole('button', { name: /Bedienung klären öffnen/i });
  await operation.click();
  await expect(operation).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('[data-support-panel="SUP-OPERATION"]')
    .getByText(/Denkhandlung bleibt unverändert/i)).toBeVisible();
  await operation.click();
  await expect(operation).toBeFocused();
});
