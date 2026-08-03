import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

async function openRepeatError(page: import('@playwright/test').Page): Promise<void> {
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
}

test('has no automatically detectable accessibility violations', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  const result = await new AxeBuilder({ page }).analyze();
  expect(result.violations, JSON.stringify(result.violations, null, 2)).toEqual([]);
});

test('completes the core learning cycle by keyboard', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).focus();
  await page.keyboard.press('Enter');
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).press('Enter');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).press('Enter');
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().press('Space');
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).press('Enter');
  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).press('Enter');
  await expect(page.getByRole('button', { name: 'Schritt ausführen' })).toBeDisabled();
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).press('Enter');
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Eine präzise Folge von Anweisungen bestimmt die Route.',
  );
  await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
});

test('provides a complete textual scene and trace without the visual image', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await expect(page.getByRole('region', { name: 'Szenenbeschreibung' }))
    .toContainText(/Start|Blickrichtung|Gut|Ziel|Hindernisse/);
  await expect(page.getByRole('table', { name: 'Laufspur' })).toBeVisible();
  await expect(page.locator('[data-robot]')).toHaveAttribute('aria-hidden', 'true');
});

for (const viewport of [
  { width: 320, height: 900 },
  { width: 360, height: 640 },
  { width: 640, height: 360 },
]) {
  test(`reflows at ${viewport.width} by ${viewport.height} without horizontal page scroll`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto('/module/ium-5-core-05/');
    expect(await page.evaluate(
      () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    )).toBe(true);
  });
}

test('remains usable at 200 percent zoom', async ({ page }) => {
  await page.setViewportSize({ width: 640, height: 900 });
  await page.goto('/module/ium-5-core-05/');
  await page.evaluate(() => document.documentElement.style.setProperty('zoom', '2'));
  expect(await page.evaluate(
    () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
  )).toBe(true);
  await expect(page.getByRole('button', { name: 'Gehe einfügen' })).toBeVisible();
});

test('focuses only actionable summaries after errors and phase changes', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await openRepeatError(page);
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('status', { name: 'Ausführungsergebnis' })).toBeFocused();
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).click();
  await expect(page.locator('[data-active-phase-heading]')).toBeFocused();
});

test('keeps focus usable after editor insert, move and delete operations', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  const insertMove = page.getByRole('button', { name: 'Gehe einfügen' });
  await insertMove.click();
  await expect(insertMove).toBeFocused();
  await page.getByRole('button', { name: 'Rechts drehen einfügen' }).click();
  await page.getByRole('button', { name: 'Befehl 2 nach oben' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem').first())
    .toBeFocused();
  await page.getByRole('button', { name: 'Befehl 1 löschen' }).click();
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem').first())
    .toBeFocused();
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });
  test('uses immediate state changes', async ({ page }) => {
    await page.goto('/module/ium-5-core-05/');
    await expect(page.locator('[data-robot]')).toHaveCSS('transition-duration', '0s');
  });
});

test.describe('touch-only core path', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });

  test('edits, predicts, executes, repairs and transfers by touch controls', async ({ page }) => {
    await page.goto('/module/ium-5-core-05/');
    await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).tap();
    await page.getByLabel('Erwartete Endposition').selectOption('E2');
    await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
    await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
    await page.getByRole('button', { name: 'Vorhersage bestätigen' }).tap();
    await page.getByRole('button', { name: 'Vollständig ausführen' }).tap();
    await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().tap();
    await page.getByLabel('Reparaturhypothese').fill(
      'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
    );
    await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).tap();
    await page.getByLabel('Wiederholungszahl').fill('5');
    await page.getByRole('button', { name: 'Revision übernehmen' }).tap();
    await page.getByRole('button', { name: 'UE 5 · Transfer' }).tap();
    await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
    await page.getByLabel('Begründung zu Navigation').fill(
      'Eine präzise Folge von Anweisungen bestimmt die Route.',
    );
    await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
    await expect(page.locator('[draggable="true"]')).toHaveCount(0);
  });
});

test('all visible actions meet the 44 by 44 CSS pixel target', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  const undersized = await page.locator('button:visible, .file-action:visible').evaluateAll(
    (elements) => elements
      .map((element) => {
        const box = element.getBoundingClientRect();
        return { text: element.textContent?.trim(), width: box.width, height: box.height };
      })
      .filter(({ width, height }) => width < 44 || height < 44),
  );
  expect(undersized).toEqual([]);
});
