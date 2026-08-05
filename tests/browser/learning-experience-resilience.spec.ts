import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/fixtures/learning-experience-resilience/');
});

test('announces offline once without moving focus', async ({ page }) => {
  const trigger = page.getByRole('button', { name: 'Offline simulieren' });
  await trigger.focus();
  await trigger.click();

  await expect(page.getByRole('status')).toContainText('Offline');
  await expect(trigger).toBeFocused();
  await expect(page.getByText('Offline – du kannst lokal weiterarbeiten')).toHaveCount(1);
});

test('makes a user-triggered save failure discoverable and preserves work', async ({ page }) => {
  const work = page.getByLabel('Arbeitsnotiz');
  await work.fill('Meine noch nicht gespeicherte Vermutung');
  await page.getByRole('button', { name: 'Speicherfehler simulieren' }).click();

  await expect(page.getByRole('alert')).toContainText('Speichern nicht möglich');
  await expect(work).toHaveValue('Meine noch nicht gespeicherte Vermutung');
});

test('starts reset confirmation on cancel and returns focus for Escape', async ({ page }) => {
  const reset = page.getByRole('button', { name: 'Arbeitsstand zurücksetzen' });
  await reset.click();

  await expect(page.getByRole('dialog', { name: 'Arbeitsstand zurücksetzen?' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Abbrechen' })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog', { name: 'Arbeitsstand zurücksetzen?' })).toBeHidden();
  await expect(reset).toBeFocused();
});

test('keeps local export available offline', async ({ page }) => {
  await page.getByRole('button', { name: 'Offline simulieren' }).click();
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Arbeitsstand lokal exportieren' }).click();
  expect(await (await download).path()).not.toBeNull();
});

test('contains no learning correctness in live regions', async ({ page }) => {
  await page.getByRole('button', { name: 'Offline simulieren' }).click();
  await page.getByRole('button', { name: 'Speicherfehler simulieren' }).click();

  const liveText = await page.locator('[aria-live], [role="status"], [role="alert"]')
    .allTextContents();
  expect(liveText.join(' ')).not.toMatch(/richtig|falsch|korrekt|lösung/i);
});
