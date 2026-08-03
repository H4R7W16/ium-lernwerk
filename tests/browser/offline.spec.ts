import { createServer, type Server } from 'node:http';
import { copyFile, cp, mkdtemp, readFile, readdir, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extname, join, resolve } from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';

const repoRoot = process.cwd();
const rootOutput = resolve(repoRoot, 'apps/lernwerk-portal/dist');

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

async function publishCandidateBuild(options: {
  buildRevision: string;
  removeBeforeWorker?: string[];
}): Promise<void> {
  const candidateOutput = await mkdtemp(join(tmpdir(), 'ium-update-candidate-'));
  try {
    await buildPortalToDirectory({
      profile: 'fixture',
      base: '/',
      rootDir: repoRoot,
      outputDir: candidateOutput,
      buildRevision: options.buildRevision,
    });
    for (const entry of await readdir(candidateOutput, { withFileTypes: true })) {
      if (entry.name === 'sw.js' || entry.name === '.vite-cache') continue;
      await cp(
        resolve(candidateOutput, entry.name),
        resolve(rootOutput, entry.name),
        { recursive: entry.isDirectory(), force: true },
      );
    }
    for (const relativePath of options.removeBeforeWorker ?? []) {
      await rm(resolve(rootOutput, relativePath), { force: true });
    }
    // A static release exposes its complete assets before its update entry point.
    await copyFile(resolve(candidateOutput, 'sw.js'), resolve(rootOutput, 'sw.js'));
  } finally {
    await rm(candidateOutput, { recursive: true, force: true });
  }
}

test('confirmed online install supports offline work, export and fallback', async ({ context, page }) => {
  await page.goto('/module/test-platform-reference/');
  await waitForOfflineReady(page);

  await context.setOffline(true);
  await page.getByLabel('Synthetischer Text').fill('Offline erhalten');
  await expect(page.getByRole('status')).toContainText('Lokal gespeichert');

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Exportieren' }).click();
  const exportDownload = await downloadPromise;
  expect(await exportDownload.path()).not.toBeNull();

  await page.reload();
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Offline erhalten');
  await page.goto('/nicht-im-cache/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText(
    'Diese Seite ist gerade nicht offline verfügbar',
  );

  await context.setOffline(false);
  await page.goto('/module/test-platform-reference/');
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Offline erhalten');
});

test('copied schema-1 data is migrated and persisted as schema 2', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(async () => {
    const state = {
      format: 'ium-learning-state',
      formatVersion: 1,
      moduleId: 'TEST-PLATFORM-REFERENCE',
      moduleVersion: '1.0.0',
      stateSchemaVersion: 1,
      workspaceId: '423e4567-e89b-42d3-a456-426614174000',
      savedAt: '2026-08-03T12:00:00.000Z',
      payload: { text: 'Kopierter Altstand', choice: 'alpha' },
    };
    await new Promise<void>((accept, reject) => {
      const request = indexedDB.open('ium-lernwerk', 1);
      request.addEventListener('upgradeneeded', () => {
        request.result.createObjectStore('activeStates', { keyPath: 'moduleId' });
      });
      request.addEventListener('error', () => reject(request.error));
      request.addEventListener('success', () => {
        const transaction = request.result.transaction('activeStates', 'readwrite');
        transaction.objectStore('activeStates').put(state);
        transaction.addEventListener('complete', () => {
          request.result.close();
          accept();
        });
        transaction.addEventListener('error', () => reject(transaction.error));
      });
    });
  });

  await page.goto('/module/test-platform-reference/');
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Kopierter Altstand');
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Exportieren' }).click();
  const exportPath = await (await downloadPromise).path();
  expect(exportPath).not.toBeNull();
  const exported = JSON.parse(await readFile(exportPath!, 'utf8')) as {
    stateSchemaVersion: number;
    payload: Record<string, unknown>;
  };
  expect(exported.stateSchemaVersion).toBe(2);
  expect(exported.payload).toEqual({ text: 'Kopierter Altstand', choice: 'alpha' });
});

test('a waiting update activates only after the active runtime flushes', async ({ page }) => {
  await page.goto('/module/test-platform-reference/');
  await waitForOfflineReady(page);

  await publishCandidateBuild({ buildRevision: 'candidate-2' });
  await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    await registration.update();
  });
  await expect(page.locator('[data-update-prompt]')).toBeVisible({ timeout: 20_000 });

  await page.getByLabel('Synthetischer Text').fill('Vor Update bestätigt');
  await page.getByRole('button', { name: 'Speichern und aktualisieren' }).click();
  await expect(page.locator('meta[name="ium-build-revision"]')).toHaveAttribute(
    'content',
    'candidate-2',
    { timeout: 20_000 },
  );
  await expect(page.getByLabel('Synthetischer Text')).toHaveValue('Vor Update bestätigt');
});

test('a candidate with a missing precache asset fails closed', async ({ context, page }) => {
  await page.goto('/module/test-platform-reference/');
  await waitForOfflineReady(page);

  await publishCandidateBuild({
    buildRevision: 'candidate-broken',
    removeBeforeWorker: ['offline/index.html'],
  });

  const result = await page.evaluate(async () => {
    const registration = await navigator.serviceWorker.ready;
    const activeBefore = registration.active;
    const updateFound = new Promise<ServiceWorker | null>((accept) => {
      registration.addEventListener('updatefound', () => accept(registration.installing), { once: true });
    });
    await registration.update();
    const candidate = registration.installing ?? await updateFound;
    if (candidate && candidate.state !== 'redundant') {
      await new Promise<void>((accept) => {
        candidate.addEventListener('statechange', () => {
          if (candidate.state === 'redundant' || candidate.state === 'activated') accept();
        });
      });
    }
    return {
      candidateState: candidate?.state ?? null,
      activeUnchanged: registration.active === activeBefore,
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
  await expect(page.getByLabel('Synthetischer Text')).toBeVisible();
  await context.setOffline(false);
});

test('subpath build confirms its exact service-worker scope and offline reload', async ({ context, page }) => {
  const output = await mkdtemp(join(tmpdir(), 'ium-subpath-'));
  let server: Server | undefined;
  try {
    await buildPortalToDirectory({
      profile: 'fixture',
      base: '/ium-lernwerk/',
      rootDir: repoRoot,
      outputDir: output,
      buildRevision: 'subpath',
    });
    server = createServer(async (request, response) => {
      try {
        const pathname = new URL(request.url ?? '/', 'http://localhost').pathname;
        if (!pathname.startsWith('/ium-lernwerk/')) {
          response.writeHead(404).end();
          return;
        }
        const relativePath = decodeURIComponent(pathname.slice('/ium-lernwerk/'.length));
        let filePath = resolve(output, relativePath || 'index.html');
        if (!filePath.startsWith(resolve(output))) {
          response.writeHead(403).end();
          return;
        }
        if ((await stat(filePath)).isDirectory()) filePath = resolve(filePath, 'index.html');
        const mediaTypes: Record<string, string> = {
          '.css': 'text/css; charset=utf-8',
          '.html': 'text/html; charset=utf-8',
          '.js': 'text/javascript; charset=utf-8',
          '.json': 'application/json; charset=utf-8',
          '.png': 'image/png',
          '.svg': 'image/svg+xml',
          '.webmanifest': 'application/manifest+json',
        };
        response.writeHead(200, {
          'content-type': mediaTypes[extname(filePath)] ?? 'application/octet-stream',
        });
        response.end(await readFile(filePath));
      } catch {
        response.writeHead(404).end();
      }
    });
    await new Promise<void>((accept, reject) => {
      server!.once('error', reject);
      server!.listen(0, '127.0.0.1', accept);
    });
    const address = server.address();
    if (!address || typeof address === 'string') throw new Error('Missing static server address');
    const origin = `http://127.0.0.1:${address.port}`;

    await page.goto(`${origin}/ium-lernwerk/module/test-platform-reference/`);
    await waitForOfflineReady(page);
    await expect.poll(() => page.evaluate(async () => (await navigator.serviceWorker.ready).scope))
      .toBe(`${origin}/ium-lernwerk/`);
    await context.setOffline(true);
    await page.reload();
    await expect(page.getByLabel('Synthetischer Text')).toBeVisible();
    await context.setOffline(false);
  } finally {
    if (server) await new Promise<void>((accept) => server!.close(() => accept()));
    await rm(output, { recursive: true, force: true });
  }
});
