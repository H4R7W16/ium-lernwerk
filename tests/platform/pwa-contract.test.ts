import { readFile } from 'node:fs/promises';
import { afterEach, expect, test } from 'vitest';
import {
  buildPortal,
  type BuiltPortal,
} from './helpers/build-portal.js';

const builds: BuiltPortal[] = [];

afterEach(async () => {
  await Promise.all(builds.splice(0).map((build) => build.cleanup()));
});

test('custom worker has no unconditional skipWaiting', async () => {
  const source = await readFile('apps/lernwerk-portal/src/sw.ts', 'utf8');
  expect(source.match(/self\.skipWaiting\(/g)).toHaveLength(1);
  expect(source).toMatch(
    /if \(event\.data\?\.type === 'SKIP_WAITING'\)[\s\S]*self\.skipWaiting\(\)/,
  );
});

test('fixture precache stays inside the configured base and contains offline route', async () => {
  const build = await buildPortal('fixture', '/ium-lernwerk/');
  builds.push(build);

  expect(build.manifest.start_url).toBe('/ium-lernwerk/');
  expect(build.manifest.scope).toBe('/ium-lernwerk/');
  expect(build.serviceWorkerText).toContain('/ium-lernwerk/offline/');
  expect(build.externalUrls).toEqual([]);
});
