import { beforeEach, describe, expect, test, vi } from 'vitest';
import {
  assertPublicationCombination,
  parseBuildRevision,
  parsePreviewId,
  parsePublicationMode,
  type PublicationMode,
} from '../../scripts/publication-mode.js';
import type { BuildProfile } from '../../scripts/build-module-registry.js';

const boundaries = vi.hoisted(() => ({
  buildRegistry: vi.fn(async () => undefined),
  finalizeServiceWorker: vi.fn(async () => undefined),
  prepareModuleAssets: vi.fn(async () => undefined),
  spawnSync: vi.fn(() => ({ status: 0, stdout: '', stderr: '' })),
}));

vi.mock('node:child_process', () => ({ spawnSync: boundaries.spawnSync }));
vi.mock('../../scripts/build-module-registry.js', () => ({
  buildRegistry: boundaries.buildRegistry,
}));
vi.mock('../../scripts/finalize-service-worker.js', () => ({
  finalizeServiceWorker: boundaries.finalizeServiceWorker,
}));
vi.mock('../../scripts/prepare-module-assets.js', () => ({
  prepareModuleAssets: boundaries.prepareModuleAssets,
}));

beforeEach(() => {
  vi.clearAllMocks();
});

describe('publication/profile compatibility', () => {
  const cases: ReadonlyArray<readonly [BuildProfile, PublicationMode, boolean]> = [
    ['production', 'development', true],
    ['production', 'gate-b-preview', true],
    ['production', 'device-fixture', false],
    ['fixture', 'development', false],
    ['fixture', 'gate-b-preview', false],
    ['fixture', 'device-fixture', true],
  ];

  test.each(cases)('%s with %s has the fixed compatibility result', (profile, mode, allowed) => {
    const action = () => assertPublicationCombination(profile, mode);
    if (allowed) {
      expect(action).not.toThrow();
    } else {
      expect(action).toThrow(/combination/i);
    }
  });
});

test('publication mode parser accepts only the closed enumeration', () => {
  expect(parsePublicationMode('development')).toBe('development');
  expect(parsePublicationMode('device-fixture')).toBe('device-fixture');
  expect(parsePublicationMode('gate-b-preview')).toBe('gate-b-preview');
  expect(() => parsePublicationMode('preview')).toThrow(/mode/i);
  expect(() => parsePublicationMode('gate-b-preview\n')).toThrow(/mode/i);
});

test('gate-b revision is exactly one lowercase full Git SHA', () => {
  const sha = 'abcdef0123456789'.repeat(2) + 'abcdef01';
  expect(parseBuildRevision(sha, 'gate-b-preview')).toBe(sha);
  expect(() => parseBuildRevision('abc123', 'gate-b-preview')).toThrow(/revision/i);
  expect(() => parseBuildRevision('G'.repeat(40), 'gate-b-preview')).toThrow(/revision/i);
});

test('development and device revisions remain optional but path-safe', () => {
  expect(parseBuildRevision('', 'development')).toBe('stable');
  expect(parseBuildRevision('', 'device-fixture')).toBe('stable');
  expect(parseBuildRevision('device-update-test', 'device-fixture')).toBe('device-update-test');
  for (const value of ['../secret', 'folder/revision', 'bad\\revision', 'bad\nrevision']) {
    expect(() => parseBuildRevision(value, 'device-fixture')).toThrow(/revision/i);
  }
});

test('preview ID is mandatory only for Gate B and rejects path or control characters', () => {
  expect(parsePreviewId('ium5-gate-b-test-0001', 'gate-b-preview')).toBe(
    'ium5-gate-b-test-0001',
  );
  expect(() => parsePreviewId('', 'gate-b-preview')).toThrow(/preview/i);
  expect(() => parsePreviewId('ium5-gate-b-../secret', 'gate-b-preview')).toThrow(/preview/i);
  expect(() => parsePreviewId('ium5-gate-b-test\n0001', 'gate-b-preview')).toThrow(/preview/i);
  expect(parsePreviewId('', 'development')).toBe('');
  expect(parsePreviewId('', 'device-fixture')).toBe('');
  expect(() => parsePreviewId('ium5-gate-b-test-0001', 'development')).toThrow(/preview/i);
});

test('Gate-B build passes the closed publication contract to Astro', async () => {
  const { buildPortalToDirectory } = await import('../../scripts/build-portal.js');
  const sha = '1'.repeat(40);
  await buildPortalToDirectory({
    profile: 'production',
    publicationMode: 'gate-b-preview',
    base: '/ium-lernwerk/',
    rootDir: '/repo',
    outputDir: '/output',
    buildRevision: sha,
    previewId: 'ium5-gate-b-test-0001',
  });

  const spawnOptions = boundaries.spawnSync.mock.calls[0]?.[2];
  expect(spawnOptions?.env).toMatchObject({
    PUBLIC_IUM_PUBLICATION_MODE: 'gate-b-preview',
    PUBLIC_IUM_BUILD_REVISION: sha,
    PUBLIC_IUM_PREVIEW_ID: 'ium5-gate-b-test-0001',
  });
});

test('invalid combination fails before registry, assets or Astro are touched', async () => {
  const { buildPortalToDirectory } = await import('../../scripts/build-portal.js');
  await expect(buildPortalToDirectory({
    profile: 'fixture',
    publicationMode: 'gate-b-preview',
    base: '/',
    rootDir: '/repo',
    outputDir: '/output',
    buildRevision: '1'.repeat(40),
    previewId: 'ium5-gate-b-test-0001',
  })).rejects.toThrow(/combination/i);

  expect(boundaries.buildRegistry).not.toHaveBeenCalled();
  expect(boundaries.prepareModuleAssets).not.toHaveBeenCalled();
  expect(boundaries.spawnSync).not.toHaveBeenCalled();
});
