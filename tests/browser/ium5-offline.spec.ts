import { createHash } from 'node:crypto';
import { copyFile, cp, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';

const repoRoot = process.cwd();
const productionOutput = resolve(repoRoot, 'apps/lernwerk-portal/dist');

test.describe.configure({ mode: 'serial' });

async function waitForOfflineReady(page: Page): Promise<void> {
  await expect(page.locator('[data-connection-status]')).toHaveAttribute(
    'data-pwa-state',
    'ready',
    { timeout: 20_000 },
  );
  await page.reload();
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
}

async function publishIum5Candidate(options: {
  buildRevision: string;
  removeBeforeWorker?: readonly string[];
}): Promise<void> {
  const candidate = await mkdtemp(join(tmpdir(), 'ium5-update-candidate-'));
  try {
    await buildPortalToDirectory({
      profile: 'production',
      publicationMode: 'development',
      base: '/',
      rootDir: repoRoot,
      outputDir: candidate,
      buildRevision: options.buildRevision,
    });
    const workerPath = resolve(candidate, 'sw.js');
    let worker = await readFile(workerPath, 'utf8');
    for (const relativePath of options.removeBeforeWorker ?? []) {
      const urlMarker = `"url":"/${relativePath}"`;
      const markerIndex = worker.indexOf(urlMarker);
      const entryStart = worker.lastIndexOf('{', markerIndex);
      const entryEnd = worker.indexOf('}', markerIndex);
      if (markerIndex < 0 || entryStart < 0 || entryEnd < 0) {
        throw new Error(`Missing precache entry for broken candidate: ${relativePath}`);
      }
      const entry = worker.slice(entryStart, entryEnd + 1);
      const missingFingerprint = `changed-but-missing:${options.buildRevision}:${relativePath}`;
      const mismatchingDigest = createHash('sha384').update(missingFingerprint).digest('base64');
      const mismatchingRevision = createHash('md5').update(missingFingerprint).digest('hex');
      const changedEntry = entry
        .replace(
          /"integrity":"sha384-[A-Za-z0-9+/=]+"/,
          `"integrity":"sha384-${mismatchingDigest}"`,
        )
        .replace(/"revision":"[a-f0-9]+"/, `"revision":"${mismatchingRevision}"`);
      if (changedEntry === entry) {
        throw new Error(`Missing integrity evidence for broken candidate: ${relativePath}`);
      }
      worker = `${worker.slice(0, entryStart)}${changedEntry}${worker.slice(entryEnd + 1)}`;
    }
    await writeFile(workerPath, worker, 'utf8');
    for (const entry of await readdir(candidate, { withFileTypes: true })) {
      if (entry.name === 'sw.js' || entry.name === '.vite-cache') continue;
      await cp(resolve(candidate, entry.name), resolve(productionOutput, entry.name), {
        recursive: entry.isDirectory(),
        force: true,
      });
    }
    for (const relativePath of options.removeBeforeWorker ?? []) {
      await rm(resolve(productionOutput, relativePath), { force: true });
    }
    await copyFile(resolve(candidate, 'sw.js'), resolve(productionOutput, 'sw.js'));
  } finally {
    await rm(candidate, { recursive: true, force: true });
  }
}

test('completes the installed IUM5 core path offline with local state', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await page.getByRole('button', { name: 'Fehlerfall Wiederholungszahl öffnen' }).click();
  await page.getByLabel('Erwartete Endposition').selectOption('E2');
  await page.getByLabel('Erwartete Blickrichtung').selectOption('east');
  await page.getByLabel('Erwarteter Auftragserfolg').selectOption('no');
  await page.getByRole('button', { name: 'Vorhersage bestätigen' }).click();
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await waitForOfflineReady(page);

  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Präzise Abläufe ausführbar machen' }))
    .toBeVisible();
  await page.getByRole('button', { name: 'Vollständig ausführen' }).click();
  await expect(page.getByRole('table', { name: 'Laufspur' })).toBeVisible();
  await page.getByRole('radio', { name: /erster abweichender Schritt/i }).first().check();
  await page.getByLabel('Reparaturhypothese').fill(
    'Die Wiederholungszahl ist zu klein; ein weiterer Schritt führt zum Ziel.',
  );
  await page.getByRole('button', { name: 'Reparaturhypothese bestätigen' }).click();
  await page.getByLabel('Wiederholungszahl').fill('5');
  await page.getByRole('button', { name: 'Revision übernehmen' }).click();
  await page.getByRole('button', { name: 'UE 5 · Transfer' }).click();
  await page.getByLabel('Navigation einordnen').selectOption('algorithmic');
  await page.getByLabel('Begründung zu Navigation').fill(
    'Eine präzise Folge von Anweisungen bestimmt die Route.',
  );
  await page.getByLabel('Sind alle Anweisungen eindeutig?').selectOption('yes');
  await expect(page.locator('[data-save-status]')).toHaveText('Lokal gespeichert');
  await context.setOffline(false);
});

test('activates a complete update only after flushing the IUM5 runtime', async ({ page }) => {
  await page.goto('/module/ium-5-core-05/');
  await waitForOfflineReady(page);

  await publishIum5Candidate({ buildRevision: 'ium5-candidate-2' });
  await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    await registration.update();
  });
  await expect(page.locator('[data-update-prompt]')).toBeVisible({ timeout: 20_000 });

  await page.getByRole('button', { name: 'Gehe einfügen' }).click();
  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('meta[name="ium-build-revision"]')).toHaveAttribute(
    'content',
    'ium5-candidate-2',
    { timeout: 20_000 },
  );
  await expect(page.getByRole('list', { name: 'Algorithmus' }).getByRole('listitem'))
    .toHaveCount(1);
});

test('rejects an incomplete candidate and keeps the active IUM5 path offline', async ({ context, page }) => {
  await page.goto('/module/ium-5-core-05/');
  await waitForOfflineReady(page);

  await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    const scope = globalThis as typeof globalThis & {
      __ium5ActiveBefore?: ServiceWorker | null;
      __ium5Candidate?: Promise<ServiceWorker | null>;
    };
    scope.__ium5ActiveBefore = registration.active;
    scope.__ium5Candidate = new Promise<ServiceWorker | null>((accept) => {
      registration.addEventListener('updatefound', () => accept(registration.installing), { once: true });
    });
  });

  await publishIum5Candidate({
    buildRevision: 'ium5-broken',
    removeBeforeWorker: ['generated-modules/ium-5-core-05/delivery-robot.svg'],
  });
  const result = await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    const scope = globalThis as typeof globalThis & {
      __ium5ActiveBefore?: ServiceWorker | null;
      __ium5Candidate?: Promise<ServiceWorker | null>;
    };
    await registration.update();
    const candidate = registration.installing
      ?? registration.waiting
      ?? await scope.__ium5Candidate;
    if (candidate) {
      await new Promise<void>((accept) => {
        const acceptTerminalState = () => {
          if (
            candidate.state === 'redundant'
            || candidate.state === 'activated'
            || candidate.state === 'installed'
          ) accept();
        };
        candidate.addEventListener('statechange', acceptTerminalState);
        acceptTerminalState();
      });
    }
    return {
      candidateState: candidate?.state ?? null,
      activeUnchanged: registration.active === scope.__ium5ActiveBefore,
      hasWaiting: registration.waiting !== null,
    };
  });
  expect(result).toEqual({
    candidateState: 'redundant',
    activeUnchanged: true,
    hasWaiting: false,
  });
  await expect(page.locator('[data-update-prompt]')).toBeHidden();

  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Präzise Abläufe ausführbar machen' }))
    .toBeVisible();
  await context.setOffline(false);
});
