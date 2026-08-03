import { access, cp, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, beforeEach, expect, test } from 'vitest';
import {
  buildRegistry,
  renderRegistry,
  type BuildRegistryOptions,
} from '../../scripts/build-module-registry.js';
import { prepareModuleAssets } from '../../scripts/prepare-module-assets.js';

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

test('production exposes exactly the validated working IUM5 module', async () => {
  const registry = await buildRegistry({
    profile: 'production',
    rootDir: repoRoot,
    outputDir: temporaryOutput,
  });
  expect(registry.modules.map((entry) => entry.id)).toEqual(['IUM-5-CORE-05']);
  expect(registry.modules[0]).toMatchObject({
    renderer: 'algorithm-workbench',
    publishedStatus: 'working',
    countsTowardCoverage: true,
    workbench: {
      content: { moduleId: 'IUM-5-CORE-05' },
      robotAssetPath: 'generated-modules/ium-5-core-05/delivery-robot.svg',
    },
  });
  expect(registry.modules[0]?.workbench?.scenarios).toHaveLength(10);
});

test('fixture profile yields exactly the reserved synthetic entry', async () => {
  const registry = await buildRegistry(fixtureOptions);
  expect(registry.modules.map((entry) => entry.id)).toEqual([
    'TEST-PLATFORM-REFERENCE',
  ]);
  expect(registry.modules[0]?.countsTowardCoverage).toBe(false);
  expect(registry.modules[0]?.publishedStatus).toBeNull();
  expect(registry.modules[0]?.renderer).toBe('fixture-workspace');
  expect(registry.modules[0]).not.toHaveProperty('workbench');
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

test('prepares the IUM5 asset only for production and clears it for fixture', async () => {
  const root = await mkdtemp(join(tmpdir(), 'ium-module-assets-'));
  temporaryRoots.push(root);
  const moduleRoot = join(root, 'modules', 'IUM-5-CORE-05');
  await mkdir(join(root, 'modules'), { recursive: true });
  await cp(join(repoRoot, 'modules', 'IUM-5-CORE-05'), moduleRoot, {
    recursive: true,
  });

  await prepareModuleAssets({ profile: 'production', rootDir: root });
  const generatedAsset = join(
    root,
    'apps',
    'lernwerk-portal',
    'public',
    'generated-modules',
    'ium-5-core-05',
    'delivery-robot.svg',
  );
  expect(await readFile(generatedAsset, 'utf8')).toBe(
    await readFile(join(moduleRoot, 'assets', 'delivery-robot.svg'), 'utf8'),
  );

  await prepareModuleAssets({ profile: 'fixture', rootDir: root });
  await expect(access(generatedAsset)).rejects.toMatchObject({ code: 'ENOENT' });
});
