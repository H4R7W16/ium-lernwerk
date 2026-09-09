import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';
import { openPersistent } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';
const targets = [
  '[data-m06-workspace] a[href]:visible',
  '[data-m06-workspace] button:visible',
  '[data-m06-workspace] summary:visible',
  '[data-m06-workspace] input:not([type="hidden"]):visible',
  '[data-m06-workspace] select:visible',
  '[data-m06-workspace] textarea:visible',
].join(', ');

async function openReadyWorkspace(page: Page): Promise<void> {
  await openPersistent(page, moduleUrl);
  await expect(page.locator('[data-m06-workspace]')).toHaveAttribute('aria-busy', 'false');
}

async function expectMinimumTargets(page: Page, state: string): Promise<void> {
  const undersized = await page.locator(targets).evaluateAll((elements) => elements.map((element) => {
    const box = element.getBoundingClientRect();
    const control = element as HTMLInputElement;
    return {
      target: element.getAttribute('aria-label') ?? element.textContent?.trim() ?? control.name ?? control.type,
      tag: element.tagName.toLowerCase(),
      type: control.type || null,
      width: box.width,
      height: box.height,
    };
  }).filter(({ width, height }) => width < 44 || height < 44));
  expect(undersized, state).toEqual([]);
}

async function exposeDynamicControls(page: Page): Promise<void> {
  await page.locator('details').evaluateAll((details) => details.forEach((entry) => { entry.open = true; }));
  await page.locator('[data-p1-starter]').click();
  await page.locator('[data-p1-body-kind]').selectOption('turn-left');
  await page.locator('[data-p1-body-add]').click();
  await page.locator('[data-editor="diagram"] [data-add="move"]').click();
  await page.locator('[data-editor="diagram"] [data-add="turn-left"]').click();
  await page.locator('[data-editor="code"] [data-add="move"]').click();
  await page.locator('[data-run-code]').click();
}

test('has no automatically detectable accessibility violations', async ({ page }) => {
  await openReadyWorkspace(page);
  await exposeDynamicControls(page);
  const result = await new AxeBuilder({ page }).analyze();
  expect(result.violations, JSON.stringify(result.violations, null, 2)).toEqual([]);
});

test('supports the core path and focus transitions by keyboard', async ({ page }) => {
  await openReadyWorkspace(page);
  await page.getByRole('button', { name: 'Abruf öffnen' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByLabel('Deine Abrufbegründung')).toBeFocused();
  await page.getByLabel('Deine Abrufbegründung').fill('Eigener Abruf');
  await page.getByRole('button', { name: 'Zum eigenen Entwurf' }).press('Enter');
  await expect(page.locator('#mein-pruefdossier')).toBeFocused();
  await page.getByRole('button', { name: 'vor', exact: true }).focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-code-output]')).toContainText('vor');
  await page.locator('[data-run-scenario]').focus();
  expect(await page.locator('[data-run-scenario]').evaluate((element) => getComputedStyle(element).outlineStyle)).not.toBe('none');
  await page.locator('[data-diagram-explanation]').focus();
  expect(await page.locator('[data-diagram-explanation]').evaluate((element) => getComputedStyle(element).outlineStyle)).not.toBe('none');
  await page.getByText('Daten verwalten', { exact: true }).focus();
  expect(await page.getByText('Daten verwalten', { exact: true }).evaluate((element) => getComputedStyle(element).outlineStyle)).not.toBe('none');
});

for (const viewport of [
  { width: 320, height: 900 },
  { width: 360, height: 640 },
  { width: 640, height: 360 },
]) {
  test(`reflows at ${viewport.width} by ${viewport.height}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await openReadyWorkspace(page);
    await exposeDynamicControls(page);
    expect(await page.evaluate(
      () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    )).toBe(true);
  });
}

test.describe('touch core path', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });
  test('edits both products without drag and drop', async ({ page }) => {
    await openReadyWorkspace(page);
    await page.getByRole('button', { name: 'Pfeil vor' }).tap();
    await page.getByRole('button', { name: 'vor', exact: true }).tap();
    await expect(page.locator('[data-diagram-output]')).toContainText('vor');
    await expect(page.locator('[data-code-output]')).toContainText('vor');
    await page.locator('[data-editor="diagram"] [data-add="turn-left"]').tap();
    await page.locator('[data-graphic="diagram"] [data-move-up]').nth(1).tap();
    await expect(page.locator('[data-diagram-output]')).toHaveText('links\nvor');
    await expect(page.locator('[draggable="true"]')).toHaveCount(0);
  });
});

test('keeps every initial and expanded target at least 44 by 44 CSS pixels', async ({ page }) => {
  await openReadyWorkspace(page);
  await expectMinimumTargets(page, 'initial state');
  await exposeDynamicControls(page);
  await expectMinimumTargets(page, 'expanded diagrams, trace, help and data management');
});

test('keeps retrieval and import-preview targets at least 44 by 44 CSS pixels', async ({ page }) => {
  await openReadyWorkspace(page);
  await page.locator('[data-m06-open-retrieval]').click();
  await page.locator('[data-m06-retrieval]').fill('vor; links; zwei Durchläufe; Blick oben; Ort unsicher');
  await page.locator('[data-retrieval-compare]').click();
  await expectMinimumTargets(page, 'retrieval and deliberate comparison');
  await page.locator('[data-m06-own-draft]').click();
  await page.locator('[data-m06-management] summary').click();
  const download = page.waitForEvent('download');
  await page.locator('[data-export-work]').click();
  const path = await (await download).path();
  if (!path) throw new Error('Export file unavailable');
  await page.locator('[data-import-work]').setInputFiles(path);
  await expect(page.locator('[data-import-preview]')).toBeVisible();
  await expectMinimumTargets(page, 'data management and import preview');
});
