import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { afterEach, expect, test } from 'vitest';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';
import {
  buildPortal,
  type BuiltPortal,
} from './helpers/build-portal.js';

const builds: BuiltPortal[] = [];

afterEach(async () => {
  await Promise.all(builds.splice(0).map((build) => build.cleanup()));
});

test('custom worker activates only through the versioned update coordinator', async () => {
  const source = await readFile('apps/lernwerk-portal/src/sw.ts', 'utf8');
  expect(source.match(/self\.skipWaiting\(/g)).toHaveLength(1);
  expect(source).toMatch(
    /type === 'IUM_UPDATE_ACTIVATE'[\s\S]*protocol === UPDATE_PROTOCOL[\s\S]*self\.skipWaiting\(\)/,
  );
  expect(source).not.toContain("type === 'SKIP_WAITING'");
  expect(source).not.toContain('clients.claim(');
});

test('active worker inventories controlled windows twice and releases prepared clients', async () => {
  const source = await readFile('apps/lernwerk-portal/src/sw.ts', 'utf8');
  expect(source).toContain("type === 'IUM_UPDATE_PREPARE'");
  expect(source).toContain("type === 'IUM_UPDATE_COMMIT'");
  expect(source).toContain("type: 'IUM_RELOAD_PREPARE'");
  expect(source).toContain("type: 'IUM_RELOAD_RELEASE'");
  expect(source.match(/clients\.matchAll\(/g)?.length ?? 0).toBeGreaterThanOrEqual(2);
  expect(source).toContain('5_000');
});

test('fixture precache stays inside the configured base and contains offline route', async () => {
  const build = await buildPortal('fixture', '/ium-lernwerk/');
  builds.push(build);

  expect(build.manifest.start_url).toBe('/ium-lernwerk/');
  expect(build.manifest.scope).toBe('/ium-lernwerk/');
  expect(build.serviceWorkerText).toContain('/ium-lernwerk/offline/');
  expect(build.externalUrls).toEqual([]);
});

test('V2 M06 subpath precache contains its route and no production module', async () => {
  const output = await mkdtemp(join(tmpdir(), 'ium-v2-m06-pwa-'));
  try {
    await buildPortalToDirectory({
      profile: 'v2-development',
      publicationMode: 'development',
      base: '/ium-lernwerk/',
      rootDir: process.cwd(),
      outputDir: output,
      buildRevision: '2222222222222222222222222222222222222222',
    });
    const worker = await readFile(resolve(output, 'sw.js'), 'utf8');
    expect(worker).toContain('/ium-lernwerk/module/v2-g5-m06/');
    expect(worker).toContain('/ium-lernwerk/offline/');
    expect(worker).not.toContain('ium-5-core-05');
    expect(worker).not.toContain('test-platform-reference');
  } finally {
    await rm(output, { recursive: true, force: true });
  }
});
