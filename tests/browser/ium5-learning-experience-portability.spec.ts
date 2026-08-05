import { readFile, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { expect, test } from '@playwright/test';

async function sourceBelow(directory: string): Promise<string> {
  const chunks: string[] = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) chunks.push(await sourceBelow(path));
    else if (/\.(?:astro|ts|css)$/.test(entry.name)) chunks.push(await readFile(path, 'utf8'));
  }
  return chunks.join('\n');
}

test('keeps the generic package independent and renders it with non-IUM5 content', async ({ page }) => {
  const generic = await sourceBelow(resolve('packages/learning-experience/src'));
  const core = await sourceBelow(resolve('packages/ium-5-core-05/src'));
  const experience = JSON.parse(await readFile(
    resolve('modules/IUM-5-CORE-05/lernumgebung/experience.json'),
    'utf8',
  ));

  expect(generic).not.toMatch(/IUM-5-CORE-05|ue1-|worked-sequence|error-repeat-count|cmd-[0-9]/i);
  expect(core).not.toMatch(/@ium\/learning-experience|\.astro['"]|\b(?:document|window|HTMLElement)\b/);
  expect(experience).toMatchObject({ schemaVersion: 1, moduleId: 'IUM-5-CORE-05' });

  await page.goto('/fixtures/learning-experience/');
  await expect(page.locator('[data-start-board]')).toContainText('historische Entscheidung');
  await expect(page.locator('[data-lx-focus-stage]')).toContainText('Quelle');
  await expect(page.locator('[data-lx-primary-action]')).toHaveText('Weiter zur Vermutung');
  await expect(page.locator('[data-evidence-feedback]')).toHaveCount(1);
  await expect(page.locator('.lx-recovery-panel')).toContainText('Quellennotiz');
  await expect(page.locator('body')).not.toContainText(/Algorithmus|Roboter|Laufspur/);
});

test('keeps IUM5 trace and editor views injected by the portal composition root', async ({ page }) => {
  await page.goto('/fixtures/ium5-semantic-adapter/');
  await expect(page.locator('[data-semantic-adapter="fake"] [data-lx-experience-shell]')).toBeVisible();
  await expect(page.locator('[data-fake-ium5-editor]')).toContainText('Befehl');
  await expect(page.locator('[data-fake-ium5-trace]')).toContainText('Vorherzustand');
  await expect(page.locator('[data-fake-ium5-editor]')).not.toHaveAttribute('data-lx-component');
});
