import { appendFile, readFile, rm, writeFile } from 'node:fs/promises';
import { afterEach, expect, test } from 'vitest';
import { inspectBuild } from '../../scripts/check-build-output.js';
import {
  buildPortal,
  type BuiltPortal,
} from './helpers/build-portal.js';

const builds: BuiltPortal[] = [];

afterEach(async () => {
  await Promise.all(builds.splice(0).map((build) => build.cleanup()));
});

test('fixture build remains inside approved budgets', async () => {
  const fixture = await buildPortal('fixture', '/');
  builds.push(fixture);
  const report = await inspectBuild(fixture.distDir);

  expect(report.coldTransferGzipBytes).toBeLessThanOrEqual(250 * 1024);
  expect(report.initialJavaScriptGzipBytes).toBeLessThanOrEqual(100 * 1024);
  expect(report.precacheDecodedBytes).toBeLessThanOrEqual(2 * 1024 * 1024);
  expect(report.thirdPartyUrls).toEqual([]);
  expect(report.violations).toEqual([]);
});

test('root and subpath builds contain only base-aware local references', async () => {
  for (const base of ['/', '/ium-lernwerk/']) {
    const fixture = await buildPortal('fixture', base);
    builds.push(fixture);
    const report = await inspectBuild(fixture.distDir);
    expect(report.basePath).toBe(base);
    expect(report.nonBaseAwarePaths, `base ${base}`).toEqual([]);
  }
});

test('production output contains no fixture identifier', async () => {
  const production = await buildPortal('production', '/');
  builds.push(production);
  const report = await inspectBuild(production.distDir);
  expect(report.testIdentifiers).toEqual([]);
  expect(report.violations).toEqual([]);
});

test('production IUM5 build stays local, licensed and inside approved budgets', async () => {
  const production = await buildPortal('production', '/');
  builds.push(production);
  const report = await inspectBuild(production.distDir);

  expect(report.coldTransferGzipBytes).toBeLessThanOrEqual(250 * 1024);
  expect(report.initialJavaScriptGzipBytes).toBeLessThanOrEqual(100 * 1024);
  expect(report.precacheDecodedBytes).toBeLessThanOrEqual(2 * 1024 * 1024);
  expect(report.thirdPartyUrls).toEqual([]);
  expect(report.testIdentifiers).toEqual([]);
  expect(report.violations).toEqual([]);
  expect(await production.glob(
    'generated-modules/ium-5-core-05/delivery-robot.svg',
  )).toEqual(['generated-modules/ium-5-core-05/delivery-robot.svg']);
  const licenses = JSON.parse(
    await production.text('asset-licenses.json'),
  ) as { assets: readonly { path: string; license: string }[] };
  expect(licenses.assets).toContainEqual(expect.objectContaining({
    path: 'generated-modules/ium-5-core-05/delivery-robot.svg',
    license: 'CC-BY-SA-4.0',
  }));
});

test('inspection fails closed on remote code, dynamic evaluation and missing evidence', async () => {
  const fixture = await buildPortal('fixture', '/');
  builds.push(fixture);
  await appendFile(
    `${fixture.distDir}/index.html`,
    '<script src="https://example.invalid/remote.js"></script>',
  );
  const indexPath = `${fixture.distDir}/index.html`;
  await writeFile(
    indexPath,
    (await readFile(indexPath, 'utf8')).replace('Inhalte CC BY-SA 4.0', 'Lizenz fehlt'),
  );
  const script = (await fixture.glob('_astro/*.js'))[0]!;
  await appendFile(`${fixture.distDir}/${script}`, '\neval("unsafe")\nnew Function("unsafe")');
  await rm(`${fixture.distDir}/asset-licenses.json`);

  const report = await inspectBuild(fixture.distDir);
  expect(report.thirdPartyUrls).toContain('https://example.invalid/remote.js');
  expect(report.violations).toEqual(expect.arrayContaining([
    expect.stringContaining('dynamic-code:eval'),
    expect.stringContaining('dynamic-code:new-function'),
    'license-evidence:missing',
    'oer-label:missing:index.html',
  ]));
});
