import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, expect, test } from 'vitest';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';
import {
  buildPortal,
  type BuiltPortal,
} from './helpers/build-portal.js';

const builds: BuiltPortal[] = [];
const repoRoot = fileURLToPath(new URL('../..', import.meta.url));

async function collectFiles(root: string): Promise<string[]> {
  const entries = await readdir(root, { withFileTypes: true });
  const result: string[] = [];
  for (const entry of entries) {
    const path = resolve(root, entry.name);
    result.push(...(entry.isDirectory() ? await collectFiles(path) : [path]));
  }
  return result;
}

function globPattern(pattern: string): RegExp {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, '\\$&');
  const source = escaped
    .replaceAll('**', '\u0000')
    .replaceAll('*', '[^/]*')
    .replaceAll('\u0000', '.*');
  return new RegExp(`^${source}$`);
}

async function buildV2Portal(base: string): Promise<BuiltPortal> {
  const distDir = await mkdtemp(join(repoRoot, '.ium-v2-portal-test-'));
  await buildPortalToDirectory({
    profile: 'v2-development',
    publicationMode: 'development',
    base,
    rootDir: repoRoot,
    outputDir: distDir,
  });
  const relativeFiles = (await collectFiles(distDir))
    .map((path) => relative(distDir, path).split(sep).join('/'))
    .sort();
  return {
    distDir,
    manifest: {},
    serviceWorkerText: '',
    externalUrls: [],
    text: (path) => readFile(resolve(distDir, path), 'utf8'),
    async glob(pattern) {
      const matcher = globPattern(pattern);
      return relativeFiles.filter((path) => matcher.test(path));
    },
    cleanup: () => rm(distDir, { recursive: true, force: true }),
  };
}

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
  expect(await output.glob('tests/**/index.html')).toEqual([]);
  expect(await output.glob('_astro/*RuntimeProbe*')).toEqual([]);
  expect(await output.glob('_astro/*runtime-probe*')).toEqual([]);
  const productionJavaScript = await Promise.all(
    (await output.glob('_astro/*.js')).map((path) => output.text(path)),
  );
  expect(productionJavaScript.join('\n')).not.toContain('data-runtime-probe');
  expect(productionJavaScript.join('\n')).not.toContain('V2-Runtime-Prüfhülle');
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
  expect(await output.glob('tests/**/index.html')).toEqual([
    'tests/v2-runtime/index.html',
  ]);
  expect(await output.text('tests/v2-runtime/index.html')).toContain('data-runtime-probe');
});

test('V2 development build exposes only M06 at root and subpath', async () => {
  for (const base of ['/', '/ium-lernwerk/']) {
    const output = await buildV2Portal(base);
    builds.push(output);
    expect(await output.glob('module/**/index.html')).toEqual([
      'module/v2-g5-m06/index.html',
    ]);
    const indexHtml = await output.text('index.html');
    const moduleHtml = await output.text('module/v2-g5-m06/index.html');
    expect(`${indexHtml}\n${moduleHtml}`).toContain(
      'V2-Entwicklungskandidat – noch nicht für Unterrichtseinsatz freigegeben',
    );
    expect(moduleHtml).toContain('data-m06-workspace');
    expect(moduleHtml).toContain('Curriculum: unassessed');
    expect(moduleHtml).toContain('Pilot: not-started');
    expect(moduleHtml).toContain('Veröffentlichung: closed');
    expect(moduleHtml).toContain('Deine Abrufbegründung');
    expect(moduleHtml).toContain('Begründung der Prüffahrt');
    const packet = JSON.parse(await readFile(join(repoRoot, 'modules-v2/V2-G5-M06/content.json'), 'utf8'));
    for (const material of [...packet.materials, { path: 'teacher/briefing.md' }]) {
      const path = `generated-modules/v2-g5-m06/${material.path.replace(/\.md$/, '.html')}`;
      expect(moduleHtml).toContain(`${base}${path}`);
      expect(await output.text(path)).toContain('<html');
      expect(await output.text('sw.js')).toContain(path);
    }
    const scripts = await Promise.all(
      (await output.glob('_astro/*.js')).map((path) => output.text(path)),
    );
    expect(scripts.join('\n')).toContain('Auf diesem Gerät speichern');
    expect(scripts.join('\n')).toContain('Nur in dieser Sitzung arbeiten');
    expect(await output.glob('_astro/*FixtureWorkspace*')).toEqual([]);
    expect(await output.glob('_astro/*AlgorithmWorkbench*')).toEqual([]);
    expect(await output.glob('_astro/*RuntimeProbe*')).toEqual([]);
    expect(await output.glob('tests/**/index.html')).toEqual([]);
  }
});
