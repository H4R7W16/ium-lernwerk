import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const routes = [
  '/',
  '/daten/',
  '/offline/',
  '/module/test-platform-reference/',
];

for (const route of routes) {
  test(`axe finds no automatically detectable issue on ${route}`, async ({ page }) => {
    const externalRequests: string[] = [];
    page.on('request', (request) => {
      const url = new URL(request.url());
      if (url.origin !== 'http://127.0.0.1:4321') externalRequests.push(request.url());
    });
    await page.goto(route);
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
    expect(externalRequests).toEqual([]);
  });
}

test('skip link, logical keyboard order and live save status work', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Zum Hauptinhalt' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('main')).toBeFocused();

  const reached: string[] = [];
  for (let index = 0; index < 20 && reached.length < 3; index += 1) {
    await page.keyboard.press('Tab');
    const id = await page.evaluate(() => document.activeElement?.id ?? '');
    if (['fixture-text', 'fixture-choice'].includes(id)) reached.push(id);
    if (await page.locator('[data-fixture-export]').evaluate(
      (element) => element === document.activeElement,
    )) reached.push('fixture-export');
  }
  expect(reached).toEqual(['fixture-text', 'fixture-choice', 'fixture-export']);
  await page.getByLabel('Synthetischer Text').fill('Live gespeichert');
  await expect(page.getByRole('status')).toContainText('Lokal gespeichert');
});

test('visible error moves focus to the summary', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await page.setInputFiles('input[type=file]', {
    name: 'wrong-module.json',
    mimeType: 'application/json',
    buffer: Buffer.from(JSON.stringify({
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'TEST-OTHER-MODULE',
      moduleVersion: '1.0.0',
      stateSchemaVersion: 2,
      workspaceId: '423e4567-e89b-42d3-a456-426614174000',
      savedAt: '2026-08-03T12:00:00.000Z',
      payload: {},
    })),
  });
  const summary = page.getByRole('alert');
  await expect(summary).toBeVisible();
  await expect(summary).toBeFocused();
  await expect(summary.getByText('anderen Lernmodul')).toBeVisible();
});

for (const viewport of [
  { width: 320, height: 640, label: '320px reflow' },
  { width: 640, height: 720, label: '200 percent zoom equivalent' },
]) {
  test(`${viewport.label} has no horizontal page scroll`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto('/module/test-platform-reference/');
    expect(await page.evaluate(() => document.documentElement.scrollWidth))
      .toBeLessThanOrEqual(viewport.width);
  });
}

test('reduced motion disables the only transition', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Zum Hauptinhalt' })).toBeFocused();
  expect(await page.getByRole('link', { name: 'Zum Hauptinhalt' }).evaluate(
    (element) => getComputedStyle(element).transitionDuration,
  )).toBe('0s');
});

test('all visible actions meet 44 by 44 CSS pixel target size', async ({ page }) => {
  for (const route of ['/daten/', '/module/test-platform-reference/']) {
    await page.goto(route);
    const undersized = await page.locator('button:visible, .file-action:visible').evaluateAll(
      (elements) => elements
        .map((element) => {
          const box = element.getBoundingClientRect();
          return { text: element.textContent?.trim(), width: box.width, height: box.height };
        })
        .filter(({ width, height }) => width < 44 || height < 44),
    );
    expect(undersized, `${route}: ${JSON.stringify(undersized)}`).toEqual([]);
  }
});

test('storage and connection states always expose text, not color alone', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  for (const selector of ['[data-storage-status]', '[data-connection-status]']) {
    const target = page.locator(selector);
    await expect(target).not.toHaveText('');
  }
});

test('export notice is visible and programmatically describes the direct action', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  const notice = page.locator('#export-sensitivity-hint');
  await expect(notice).toHaveText(
    'Exportdateien können Freitext oder Lernprodukte enthalten. Prüfe sie vor dem Teilen und veröffentliche sie nicht ungeprüft.',
  );
  await expect(notice).toBeVisible();
  await expect(page.getByRole('button', { name: 'Exportieren' })).toHaveAttribute(
    'aria-describedby',
    'export-sensitivity-hint',
  );
});
