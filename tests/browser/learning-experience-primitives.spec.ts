import { expect, test } from '@playwright/test';

test('keeps one learning focus and moves focus after advance', async ({ page }) => {
  await page.goto('/fixtures/learning-experience/');

  await expect(page.getByRole('main')).toHaveCount(1);
  await expect(page.getByRole('region', { name: 'Orientierung' })).toBeVisible();
  await expect(page.getByRole('list', { name: 'Lernweg' })
    .locator('[aria-current="step"]')).toHaveText('Orientierung');

  await page.getByRole('button', { name: 'Weiter zur Vermutung' }).click();

  await expect(page.getByRole('region', { name: 'Vermutung bilden' })).toBeFocused();
  await expect(page.getByRole('list', { name: 'Lernweg' })
    .locator('[aria-current="step"]')).toHaveText('Vermutung');
});

test('remains operable at 320 CSS pixels and simulated 200 percent zoom', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 844 });
  await page.goto('/fixtures/learning-experience/');

  await expect(page.getByRole('button', { name: 'Weiter zur Vermutung' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);

  await page.setViewportSize({ width: 640, height: 900 });
  await page.evaluate(() => {
    document.documentElement.style.zoom = '2';
  });
  await expect(page.getByRole('button', { name: 'Weiter zur Vermutung' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
});

test('preserves keyboard order and has no positive tabindex', async ({ page }) => {
  await page.goto('/fixtures/learning-experience/');

  await expect(page.locator('[tabindex]').evaluateAll((nodes) =>
    nodes.every((node) => Number(node.getAttribute('tabindex')) <= 0))).resolves.toBe(true);

  await page.getByRole('button', { name: 'Weiter zur Vermutung' }).focus();
  await expect(page.getByRole('button', { name: 'Weiter zur Vermutung' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('region', { name: 'Vermutung bilden' })).toBeFocused();
});

test('honors reduced motion during stage activation', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/fixtures/learning-experience/');
  await page.getByRole('button', { name: 'Weiter zur Vermutung' }).click();

  const stage = page.getByRole('region', { name: 'Vermutung bilden' });
  await expect(stage).toBeFocused();
  const transitionSeconds = await stage.evaluate((element) =>
    Number.parseFloat(getComputedStyle(element).transitionDuration));
  expect(transitionSeconds).toBeLessThanOrEqual(0.00001);
});
