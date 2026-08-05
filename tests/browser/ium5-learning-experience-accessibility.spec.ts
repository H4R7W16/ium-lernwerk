import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

async function assertAccessible(page: Page, label: string): Promise<void> {
  const result = await new AxeBuilder({ page }).analyze();
  expect(result.violations, `${label}: ${JSON.stringify(result.violations, null, 2)}`).toEqual([]);
  await expect(page.getByRole('main')).toHaveCount(1);
  expect(await page.locator('[tabindex]').evaluateAll((elements) =>
    elements.filter((element) => Number(element.getAttribute('tabindex')) > 0).length)).toBe(0);
  const visibleHeadingLevels = await page.locator('h1, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible')
    .evaluateAll((headings) => headings.map((heading) => Number(heading.tagName.slice(1))));
  expect(visibleHeadingLevels[0], `${label}: first visible heading`).toBe(1);
  for (let index = 1; index < visibleHeadingLevels.length; index += 1) {
    expect(
      visibleHeadingLevels[index]! - visibleHeadingLevels[index - 1]!,
      `${label}: heading jump ${visibleHeadingLevels[index - 1]} to ${visibleHeadingLevels[index]}`,
    ).toBeLessThanOrEqual(1);
  }
}

async function enterExperience(page: Page): Promise<void> {
  await page.getByRole('button', { name: /Mit der Vermutung beginnen|Weiterarbeiten/ }).click();
}

async function selectPrediction(page: Page, position: string, direction: string, success: string): Promise<void> {
  await page.getByLabel('Erwartete Endposition').selectOption(position);
  await page.getByLabel('Erwartete Blickrichtung').selectOption(direction);
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption(success);
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
}

test('keeps clean start, validation, dialogs and the complete learning cycle accessible', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await assertAccessible(page, 'clean start');
  await enterExperience(page);
  await expect(page.locator('.lx-journey-map [aria-current="step"]')).toHaveCount(1);
  expect(await page.locator('button:visible, input:visible, select:visible, textarea:visible').evaluateAll(
    (controls) => controls.filter((control) => {
      const labelled = 'labels' in control && (control as HTMLInputElement).labels?.length;
      return !labelled
        && !control.getAttribute('aria-label')?.trim()
        && !(control.textContent ?? '').trim();
    }).length,
  )).toBe(0);

  const cardStatus = page.locator('[data-evidence-card-status]');
  await expect(cardStatus).not.toBeFocused();
  await page.getByRole('button', { name: 'Belegkarte bestätigen' }).click();
  await expect(cardStatus).toHaveAttribute('role', 'alert');
  await expect(cardStatus).toBeFocused();
  await expect(page.getByLabel('Quelle', { exact: true })).toHaveAttribute('aria-describedby', /evidence-card-status/);
  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');

  await page.reload();
  await expect(page.getByRole('button', { name: 'Weiterarbeiten' })).toBeVisible();
  await page.getByRole('button', { name: 'Neu beginnen' }).click();
  const resetDialog = page.getByRole('dialog', { name: 'Diesen Modulstand neu beginnen?' });
  await expect(resetDialog).toBeVisible();
  await expect(page.getByRole('button', { name: 'Abbrechen' })).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(resetDialog.locator(':focus')).toBeVisible();
  await page.getByRole('button', { name: 'Abbrechen' }).click();
  await expect(page.getByRole('button', { name: 'Neu beginnen' })).toBeFocused();
  await page.getByRole('button', { name: 'Weiterarbeiten' }).click();

  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'prediction');
  await assertAccessible(page, 'prediction');
  await selectPrediction(page, 'E2', 'east', 'no');
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'run');
  await assertAccessible(page, 'run');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'evidence');
  await assertAccessible(page, 'evidence');
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill('Die Wiederholungszahl ist zu klein.');
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'revision');
  await assertAccessible(page, 'revision');
  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await selectPrediction(page, 'F2', 'east', 'yes');
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'transfer');

  const keyStatement = 'Die erste belegte Abweichung begründet die gezielte Revision.';
  await page.getByLabel('Quelle', { exact: true }).selectOption('error-repeat-count');
  await page.getByLabel('Beleg', { exact: true }).selectOption('trace:first-deviation');
  await page.getByLabel('Deutung', { exact: true }).fill('Die Laufspur endet vor dem Ziel.');
  await page.getByLabel('Überarbeitung', { exact: true }).fill('Die Wiederholungszahl wird auf fünf erhöht.');
  await page.getByLabel('Kernaussage', { exact: true }).fill(keyStatement);
  await page.getByLabel('Modellgrenze', { exact: true }).fill('Das Modell zeigt nur diesen deterministischen Fall.');
  await page.getByRole('button', { name: 'Belegkarte bestätigen' }).click();
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill('Feste Schritte verarbeiten Ort und Ziel.');
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-experience-stage', 'reentry');
  await assertAccessible(page, 'transfer and reentry');
  const statusText = await page.locator('[role="status"]').allTextContents();
  expect(statusText.join('\n')).not.toContain(keyStatement);
  await expect(page.locator('[data-scene-description]')).toContainText(/Start|Blickrichtung|Gut|Ziel/);
  await expect(page.locator('[data-robot]')).toHaveAttribute('aria-hidden', 'true');

  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await page.reload();
  await expect(page.getByRole('button', { name: 'Weiterarbeiten' })).toBeVisible();
  await assertAccessible(page, 'resume');
  await enterExperience(page);
  await context.setOffline(true);
  await expect(page.locator('[data-algorithm-workbench]')).toHaveAttribute('data-connectivity', 'offline');
  await expect(page.locator('[data-reentry-recall]')).toBeVisible();
  await assertAccessible(page, 'offline reentry');
  await context.setOffline(false);
});

test('preserves actions at 320 CSS pixels and 200 percent zoom', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/module/ium-5-core-05/');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  await expect(page.getByRole('button', { name: 'Mit der Vermutung beginnen' })).toBeVisible();
  await page.setViewportSize({ width: 640, height: 900 });
  await enterExperience(page);
  await page.evaluate(() => document.documentElement.style.setProperty('zoom', '2'));
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  await expect(page.getByRole('button', { name: 'Gehe einfügen' })).toBeVisible();
});

test.describe('forced colors and reduced motion', () => {
  test.use({ forcedColors: 'active', reducedMotion: 'reduce' });

  test('retains focus, textual state and immediate motion behavior', async ({ page }) => {
    await page.goto('/module/ium-5-core-05/');
    const primary = page.getByRole('button', { name: 'Mit der Vermutung beginnen' });
    await primary.focus();
    await expect(primary).toHaveCSS('outline-style', 'solid');
    await expect(page.locator('[data-storage-status]')).not.toHaveText('');
    expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
  });
});
