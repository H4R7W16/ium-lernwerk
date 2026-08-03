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
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/ium-5-core-05/index.html',
  ]);
  const indexHtml = await output.text('index.html');
  expect(indexHtml).not.toContain('data-gate-b-preview');
  expect(indexHtml).not.toContain('ium-publication-mode');
  expect(indexHtml).toContain('Präzise Abläufe ausführbar machen');
  expect(indexHtml).toContain('Arbeitsstand · nicht für Unterrichtseinsatz');
  const moduleHtml = await output.text('module/ium-5-core-05/index.html');
  expect(moduleHtml).toContain('Präzise Abläufe ausführbar machen');
  expect(moduleHtml).toContain('Status working');
  expect(moduleHtml).toContain('data-algorithm-workbench');
  expect(moduleHtml).not.toContain('Synthetische technische Referenz');
  expect(await output.glob('_astro/*FixtureWorkspace*')).toEqual([]);
});

test('fixture build contains no IUM5 renderer or identifier', async () => {
  const output = await buildPortal('fixture', '/');
  builds.push(output);
  expect(await output.glob('module/**/index.html')).toEqual([
    'module/test-platform-reference/index.html',
  ]);
  const combined = `${await output.text('index.html')}\n${
    await output.text('module/test-platform-reference/index.html')
  }`;
  expect(combined).not.toContain('data-gate-b-preview');
  expect(combined).not.toContain('ium-publication-mode');
  expect(combined).toContain('Technische Systemprobe');
  expect(combined).not.toContain('IUM-5-CORE-05');
  expect(combined).not.toContain('algorithm-workbench');
  expect(await output.glob('_astro/*AlgorithmWorkbench*')).toEqual([]);
  expect(await output.glob('_astro/*algorithm-workbench*')).toEqual([]);
});
