import { createServer, type Server } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import { openPersistent, reloadPersistent } from './helpers/storage-choice.js';

const moduleUrl = '/module/v2-g5-m06/';

const contentTypes: Record<string, string> = {
  '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.webmanifest': 'application/manifest+json',
};

async function startStaticPortal(): Promise<{ origin: string; stop: () => Promise<void> }> {
  const root = resolve('apps/lernwerk-portal/dist');
  const server: Server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url ?? '/', 'http://localhost').pathname);
      const relative = pathname.endsWith('/') ? `${pathname}index.html` : pathname;
      const target = resolve(root, `.${relative}`);
      if (target !== root && !target.startsWith(`${root}${sep}`)) {
        response.writeHead(403).end();
        return;
      }
      const body = await readFile(target);
      response.writeHead(200, { 'content-type': contentTypes[extname(target)] ?? 'application/octet-stream' });
      response.end(body);
    } catch {
      response.writeHead(404).end();
    }
  });
  await new Promise<void>((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('Static test server has no TCP address');
  let stopped = false;
  return {
    origin: `http://127.0.0.1:${address.port}`,
    stop: async () => {
      if (stopped) return;
      stopped = true;
      await new Promise<void>((accept, reject) => server.close((error) => error ? reject(error) : accept()));
    },
  };
}

async function waitForOfflineReady(page: Page): Promise<void> {
  await expect(page.locator('[data-connection-status]')).toHaveAttribute('data-pwa-state', 'ready', {
    timeout: 20_000,
  });
  await reloadPersistent(page);
  await expect.poll(() => page.evaluate(() => navigator.serviceWorker.controller !== null)).toBe(true);
}

test('reopens the persistent M06 route offline with its dossier', async ({ browser, browserName, context, page }) => {
  if (browserName === 'webkit' && process.platform === 'win32') {
    const localServer = await startStaticPortal();
    const localContext = await browser.newContext({ baseURL: localServer.origin });
    const localPage = await localContext.newPage();
    try {
      await openPersistent(localPage, moduleUrl);
      await localPage.getByLabel('Begründung der Prüffahrt').fill('OFFLINE-P3');
      await localPage.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
      await waitForOfflineReady(localPage);
      const materialLinks = await localPage.locator('[data-materials] a')
        .evaluateAll((nodes) => nodes.map((node) => (node as HTMLAnchorElement).href));
      expect(materialLinks).toHaveLength(11);
      await localServer.stop();
      await reloadPersistent(localPage);
      await expect(localPage.getByRole('heading', { name: 'Präzise Abläufe entwickeln und prüfen' })).toBeVisible();
      await expect(localPage.getByLabel('Begründung der Prüffahrt')).toHaveValue('OFFLINE-P3');
      for (const href of materialLinks) {
        await localPage.goto(href);
        await expect(localPage.locator('body')).toContainText(/MAT-|M06|Prüf|Briefing/);
      }
    } finally {
      await localServer.stop();
      await localContext.close();
    }
    return;
  }
  await openPersistent(page, moduleUrl);
  await page.getByLabel('Begründung der Prüffahrt').fill('OFFLINE-P3');
  await page.getByRole('button', { name: 'Arbeitsstand speichern' }).click();
  await waitForOfflineReady(page);
  await context.setOffline(true);
  await reloadPersistent(page);
  await expect(page.getByRole('heading', { name: 'Präzise Abläufe entwickeln und prüfen' })).toBeVisible();
  await expect(page.getByLabel('Begründung der Prüffahrt')).toHaveValue('OFFLINE-P3');
  await context.setOffline(false);
});

test('does not claim an uncached first visit works offline', async ({ browser }) => {
  const context = await browser.newContext({ baseURL: 'http://127.0.0.1:4324', offline: true });
  try {
    const page = await context.newPage();
    await expect(page.goto(moduleUrl, { waitUntil: 'domcontentloaded', timeout: 5_000 })).rejects.toThrow();
  } finally {
    await context.close();
  }
});

test('loads no third-party runtime resources', async ({ page }) => {
  const external: string[] = [];
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.origin !== 'http://127.0.0.1:4324') external.push(request.url());
  });
  await openPersistent(page, moduleUrl);
  expect(external).toEqual([]);
});
