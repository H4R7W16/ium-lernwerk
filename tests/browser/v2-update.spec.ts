import { copyFile, cp, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';
import { choosePersistent, chooseVolatile } from './helpers/storage-choice.js';

const repoRoot = process.cwd();
const outputDirectory = resolve(repoRoot, 'apps/lernwerk-portal/dist');
const probeUrl = '/tests/v2-runtime/';

test.describe.configure({ mode: 'serial' });

async function openControlled(page: Page, mode: 'persistent' | 'volatile'): Promise<void> {
  await page.goto(probeUrl);
  await (mode === 'persistent' ? choosePersistent(page) : chooseVolatile(page));
  if (await page.evaluate(() => navigator.serviceWorker.controller !== null)) return;
  await expect(page.locator('[data-connection-status]')).toHaveAttribute(
    'data-pwa-state',
    'ready',
    { timeout: 20_000 },
  );
  await page.reload();
  await (mode === 'persistent' ? choosePersistent(page) : chooseVolatile(page));
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
}

async function publishCandidate(buildRevision: string, broken = false): Promise<void> {
  const candidate = await mkdtemp(join(tmpdir(), 'ium-v2-update-candidate-'));
  try {
    await buildPortalToDirectory({
      profile: 'fixture',
      publicationMode: 'device-fixture',
      base: '/',
      rootDir: repoRoot,
      outputDir: candidate,
      buildRevision,
    });
    const workerPath = resolve(candidate, 'sw.js');
    if (broken) {
      const worker = await readFile(workerPath, 'utf8');
      const corrupted = worker.replace(
        /"integrity":"sha384-[A-Za-z0-9+/=]+"/,
        '"integrity":"sha384-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"',
      );
      if (corrupted === worker) throw new Error('Candidate has no integrity entry to corrupt');
      await writeFile(workerPath, corrupted, 'utf8');
    }
    for (const entry of await readdir(candidate, { withFileTypes: true })) {
      if (entry.name === 'sw.js' || entry.name === '.vite-cache') continue;
      await cp(resolve(candidate, entry.name), resolve(outputDirectory, entry.name), {
        recursive: entry.isDirectory(),
        force: true,
      });
    }
    await copyFile(workerPath, resolve(outputDirectory, 'sw.js'));
  } finally {
    await rm(candidate, { recursive: true, force: true });
  }
}

async function requestUpdate(page: Page): Promise<void> {
  await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    await registration.update();
  });
}

test('keeps a defective candidate deferred without reloading clients', async ({ page }) => {
  await openControlled(page, 'persistent');
  const activeRevision = await page.locator('meta[name="ium-build-revision"]').getAttribute('content');
  await publishCandidate(`v2-broken-candidate-${Date.now()}`, true);

  await requestUpdate(page);
  await expect.poll(() => page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    return registration.installing?.state ?? (registration.waiting ? 'waiting' : 'redundant');
  }), { timeout: 20_000 }).toBe('redundant');
  await expect(page.locator('[data-update-prompt]')).toBeHidden();
  await expect(page.locator('meta[name="ium-build-revision"]')).toHaveAttribute(
    'content',
    activeRevision ?? 'stable',
  );

  await publishCandidate(`v2-restored-baseline-${Date.now()}`);
});

test('coordinates volatile, missing, changed and recoverable controlled clients', async ({ context, page }) => {
  await openControlled(page, 'persistent');
  await page.getByLabel('Synthetischer Text').fill('persistenter Stand');
  await page.getByRole('button', { name: 'Speichern' }).click();

  const volatile = await context.newPage();
  await openControlled(volatile, 'volatile');
  await volatile.getByLabel('Synthetischer Text').fill('ungesicherter Stand');
  await volatile.getByRole('button', { name: 'Speichern' }).click();

  const candidateRevision = `v2-coordinated-candidate-${Date.now()}`;
  await publishCandidate(candidateRevision);
  await requestUpdate(page);
  await expect(page.locator('[data-update-prompt]')).toBeVisible({ timeout: 20_000 });

  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('[data-update-prompt]')).toHaveAttribute('data-update-attempt', '1');
  await expect(page.locator('[data-update-status]')).toContainText('ungesicherter Sitzungsstand');
  await expect(volatile.locator('[data-runtime-probe]')).toHaveAttribute('data-reload-preparing', 'false');
  expect(await page.evaluate(async () => (await navigator.serviceWorker.ready).waiting !== null)).toBe(true);

  page.once('dialog', (dialog) => dialog.accept());
  await page.getByRole('button', {
    name: 'Diesen ungesicherten Stand verwerfen und aktualisieren',
  }).click();
  await expect(page.locator('[data-update-prompt]')).toHaveAttribute('data-update-attempt', '2');
  await expect(page.locator('[data-update-status]')).toContainText('ungesicherter Sitzungsstand');
  await volatile.close();

  const legacy = await context.newPage();
  await legacy.goto('/app-icon.svg');
  await expect.poll(() => legacy.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('[data-update-prompt]')).toHaveAttribute('data-update-attempt', '3');
  await expect(page.locator('[data-update-status]')).toContainText(
    'Nicht alle offenen Seiten',
    { timeout: 10_000 },
  );
  await legacy.close();

  await page.evaluate(() => {
    document.addEventListener('ium:reload-request', ((event: CustomEvent<{
      add(task: Promise<{ safe: true; reason: 'no-work'; revision: number }>): void;
    }>) => {
      event.detail.add(new Promise((resolve) => {
        setTimeout(() => resolve({ safe: true, reason: 'no-work', revision: 0 }), 1_000);
      }));
    }) as EventListener, { once: true });
  });
  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('[data-update-prompt]')).toHaveAttribute('data-update-attempt', '4');
  await expect(page.locator('[data-runtime-probe]')).toHaveAttribute('data-reload-preparing', 'true');
  const newcomer = await context.newPage();
  await newcomer.goto('/app-icon.svg');
  await expect(page.locator('[data-update-status]')).toContainText(
    'Nicht alle offenen Seiten',
    { timeout: 10_000 },
  );
  await newcomer.close();

  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('meta[name="ium-build-revision"]')).toHaveAttribute(
    'content',
    candidateRevision,
    { timeout: 20_000 },
  );
  await choosePersistent(page);
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('persistenter Stand');
});
