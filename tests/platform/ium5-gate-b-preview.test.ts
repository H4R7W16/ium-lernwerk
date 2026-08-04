import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, expect, test } from 'vitest';
import { buildPortalToDirectory } from '../../scripts/build-portal.js';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
const outputs: string[] = [];

async function collectFiles(root: string): Promise<string[]> {
  const files: string[] = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) files.push(...await collectFiles(path));
    if (entry.isFile()) files.push(path);
  }
  return files;
}

afterEach(async () => {
  await Promise.all(outputs.splice(0).map((path) => rm(path, { recursive: true, force: true })));
});

test('every Gate-B HTML page carries the complete non-release contract', async () => {
  const output = await mkdtemp(join(repoRoot, '.ium-gate-b-test-'));
  outputs.push(output);
  const sha = '1'.repeat(40);
  const previewId = 'ium5-gate-b-test-0001';
  await buildPortalToDirectory({
    profile: 'production',
    publicationMode: 'gate-b-preview',
    base: '/ium-lernwerk/',
    rootDir: repoRoot,
    outputDir: output,
    buildRevision: sha,
    previewId,
  });

  const files = await collectFiles(output);
  const htmlFiles = files.filter((path) => path.endsWith('.html'));
  expect(htmlFiles.length).toBeGreaterThan(1);
  for (const path of htmlFiles) {
    const html = await readFile(path, 'utf8');
    expect(html, relative(output, path)).toContain(
      '<meta name="robots" content="noindex,nofollow,noarchive">',
    );
    expect(html).toContain('<meta name="ium-publication-mode" content="gate-b-preview">');
    expect(html).toContain(`<meta name="ium-build-revision" content="${sha}">`);
    expect(html).toContain(`<meta name="ium-preview-id" content="${previewId}">`);
    expect(html).toContain('<meta name="ium-product-status" content="working">');
    expect(html).toContain('<meta name="ium-device-verified" content="not-run">');
    expect(html).toContain('data-gate-b-preview');
    expect(html).toContain('Gate-B-Prüffassung – keine Unterrichts- oder Produktfreigabe');
  }

  const robots = await readFile(resolve(output, 'robots.txt'), 'utf8');
  expect(robots).toContain('User-agent: *');
  expect(robots).toContain('Disallow: /');
});

test('Gate-B preview remains production-only and adds no collection channel', async () => {
  const output = await mkdtemp(join(repoRoot, '.ium-gate-b-isolation-'));
  outputs.push(output);
  await buildPortalToDirectory({
    profile: 'production',
    publicationMode: 'gate-b-preview',
    base: '/ium-lernwerk/',
    rootDir: repoRoot,
    outputDir: output,
    buildRevision: '1'.repeat(40),
    previewId: 'ium5-gate-b-test-0001',
  });

  const outputFiles = await collectFiles(output);
  const searchableOutput = (
    await Promise.all(
      outputFiles
        .filter((path) => /\.(?:html|css|js|json|txt)$/.test(path))
        .map((path) => readFile(path, 'utf8')),
    )
  ).join('\n');
  expect(searchableOutput).toContain('IUM-5-CORE-05');
  expect(searchableOutput).not.toContain('TEST-PLATFORM-REFERENCE');
  expect(searchableOutput).not.toMatch(
    /google-analytics|googletagmanager|plausible\.io|matomo|mixpanel|segment\.com/i,
  );

  const sourceFiles = (await collectFiles(resolve(repoRoot, 'apps/lernwerk-portal/src')))
    .filter((path) => /\.(?:astro|ts|tsx|js)$/.test(path));
  const source = (await Promise.all(sourceFiles.map((path) => readFile(path, 'utf8')))).join('\n');
  expect(source).not.toMatch(
    /(?:localStorage\.(?:getItem|setItem)|indexedDB\.open)\([^)]*gate-b/i,
  );
  expect(source).not.toMatch(/fetch\([^)]*(?:collect|telemetry|analytics)/i);
});
