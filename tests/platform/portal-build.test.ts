import { afterEach, expect, test } from 'vitest';
import {
  buildPortal,
  type BuiltPortal,
} from './helpers/build-portal.js';

const builds: BuiltPortal[] = [];

afterEach(async () => {
  await Promise.all(builds.splice(0).map((build) => build.cleanup()));
});

test('production build exposes only the working IUM5 module route', async () => {
  const output = await buildPortal('production', '/');
  builds.push(output);
  expect(await output.text('index.html')).toContain(
    'Präzise Abläufe ausführbar machen',
  );
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/ium-5-core-05/index.html',
  ]);
});

test('fixture build exposes only the synthetic route', async () => {
  const output = await buildPortal('fixture', '/');
  builds.push(output);
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/test-platform-reference/index.html',
  ]);
  expect(await output.text('index.html')).toContain('Technische Systemprobe');
});
