import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { openPersistent } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';

test('has no automatically detectable accessibility violations', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  const result = await new AxeBuilder({ page }).analyze();
  expect(result.violations, JSON.stringify(result.violations, null, 2)).toEqual([]);
});

test('supports the core path and focus transitions by keyboard', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  await page.getByRole('button', { name: 'Abruf öffnen' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByLabel('Deine Abrufbegründung')).toBeFocused();
  await page.getByLabel('Deine Abrufbegründung').fill('Eigener Abruf');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).press('Enter');
  await expect(page.locator('#mein-pruefdossier')).toBeFocused();
  await page.getByRole('button', { name: 'vor', exact: true }).focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-code-output]')).toContainText('vor');
});

for (const viewport of [
  { width: 320, height: 900 },
  { width: 360, height: 640 },
  { width: 640, height: 360 },
]) {
  test(`reflows at ${viewport.width} by ${viewport.height}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await openPersistent(page, moduleUrl);
    expect(await page.evaluate(
      () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    )).toBe(true);
  });
}

test.describe('touch core path', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });
  test('edits both products without drag and drop', async ({ page }) => {
    await openPersistent(page, moduleUrl);
    await page.getByRole('button', { name: 'Pfeil vor' }).tap();
    await page.getByRole('button', { name: 'vor', exact: true }).tap();
    await expect(page.locator('[data-diagram-output]')).toContainText('vor');
    await expect(page.locator('[data-code-output]')).toContainText('vor');
    await expect(page.locator('[draggable="true"]')).toHaveCount(0);
  });
});

test('keeps visible actions at least 44 by 44 CSS pixels', async ({ page }) => {
  await openPersistent(page, moduleUrl);
  const undersized = await page.locator('[data-m06-workspace] button:visible, [data-m06-workspace] summary:visible')
    .evaluateAll((elements) => elements.map((element) => {
      const box = element.getBoundingClientRect();
      return { text: element.textContent?.trim(), width: box.width, height: box.height };
    }).filter(({ width, height }) => width < 44 || height < 44));
  expect(undersized).toEqual([]);
});
