import { cp, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, beforeEach, expect, test } from 'vitest';
import {
  buildRegistry,
  renderRegistry,
  type BuildRegistryOptions,
} from '../../scripts/build-module-registry.js';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
let temporaryOutput = '';
let fixtureOptions: BuildRegistryOptions;
const temporaryRoots: string[] = [];

beforeEach(async () => {
  temporaryOutput = await mkdtemp(join(tmpdir(), 'ium-registry-'));
  fixtureOptions = {
    profile: 'fixture',
    rootDir: repoRoot,
    outputDir: temporaryOutput,
  };
});

afterEach(async () => {
  await rm(temporaryOutput, { recursive: true, force: true });
  await Promise.all(
    temporaryRoots.splice(0).map((path) => rm(path, { recursive: true, force: true })),
  );
});

test('production ignores every fixture source', async () => {
  const registry = await buildRegistry({
    profile: 'production',
    rootDir: repoRoot,
    outputDir: temporaryOutput,
  });
  expect(registry.modules).toEqual([]);
});

test('fixture profile yields exactly the reserved synthetic entry', async () => {
  const registry = await buildRegistry(fixtureOptions);
  expect(registry.modules.map((entry) => entry.id)).toEqual([
    'TEST-PLATFORM-REFERENCE',
  ]);
  expect(registry.modules[0]?.countsTowardCoverage).toBe(false);
  expect(registry.modules[0]?.publishedStatus).toBeNull();
});

test('equal inputs produce byte-identical registry bytes', async () => {
  const first = renderRegistry(await buildRegistry(fixtureOptions));
  const second = renderRegistry(await buildRegistry(fixtureOptions));
  expect(second).toEqual(first);
});

test('fixture rejects a real coverage reference', async () => {
  const root = await mkdtemp(join(tmpdir(), 'ium-registry-root-'));
  temporaryRoots.push(root);
  await cp(join(repoRoot, 'tests', 'fixtures'), join(root, 'tests', 'fixtures'), {
    recursive: true,
  });
  const manifestPath = join(root, 'tests', 'fixtures', 'reference-module', 'module.yaml');
  const source = await readFile(manifestPath, 'utf8');
  await writeFile(manifestPath, source.replace('TEST-COV-001', 'REAL-COV-001'));

  await expect(
    buildRegistry({
      profile: 'fixture',
      rootDir: root,
      outputDir: join(root, 'generated'),
    }),
  ).rejects.toThrow('Fixture profile contains a real coverage reference');
});
