import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, expect, test } from 'vitest';
import { finalizeServiceWorker } from '../../scripts/finalize-service-worker.js';

const temporaryDirectories: string[] = [];

afterEach(async () => {
  await Promise.all(temporaryDirectories.splice(0).map(
    (path) => rm(path, { recursive: true, force: true }),
  ));
});

test('injects a remaining Workbox marker after the Astro build', async () => {
  const output = await mkdtemp(join(tmpdir(), 'ium-sw-finalizer-'));
  temporaryDirectories.push(output);
  await writeFile(join(output, 'index.html'), '<h1>Offline shell</h1>');
  await writeFile(
    join(output, 'sw.js'),
    'const manifest = self.__WB_MANIFEST; self.marker = manifest.length;\n',
  );

  const result = await finalizeServiceWorker(output, '/ium-lernwerk/');
  const serviceWorker = await readFile(join(output, 'sw.js'), 'utf8');

  expect(result).toEqual({ repaired: true, entryCount: 1 });
  expect(serviceWorker).not.toContain('self.__WB_MANIFEST');
  expect(serviceWorker).toContain('/ium-lernwerk/index.html');
});

test('leaves an already injected worker byte-identical', async () => {
  const output = await mkdtemp(join(tmpdir(), 'ium-sw-finalizer-'));
  temporaryDirectories.push(output);
  const injected = 'const manifest = [{ url: "/index.html", revision: "x" }];\n';
  await writeFile(join(output, 'sw.js'), injected);

  expect(await finalizeServiceWorker(output, '/')).toEqual({
    repaired: false,
    entryCount: 0,
  });
  expect(await readFile(join(output, 'sw.js'), 'utf8')).toBe(injected);
});
