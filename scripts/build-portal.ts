import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
import { buildRegistry, type BuildProfile } from './build-module-registry.js';

function normalizeBase(value: string): string {
  if (
    !value.startsWith('/')
    || !value.endsWith('/')
    || value.includes('..')
    || value.includes('?')
    || value.includes('#')
    || value.includes('://')
    || value.includes('\\')
  ) {
    throw new Error(`Invalid portal base path: ${value}`);
  }
  return value.replace(/\/{2,}/g, '/');
}

function assertProfile(value: string): asserts value is BuildProfile {
  if (value !== 'production' && value !== 'fixture') {
    throw new Error(`Unknown portal build profile: ${value}`);
  }
}

export async function buildPortalToDirectory(options: {
  profile: BuildProfile;
  base: string;
  rootDir: string;
  outputDir: string;
  buildRevision?: string;
}): Promise<void> {
  const base = normalizeBase(options.base);
  const appRoot = resolve(options.rootDir, 'apps/lernwerk-portal');
  await buildRegistry({
    profile: options.profile,
    rootDir: options.rootDir,
    outputDir: resolve(appRoot, 'src/generated'),
  });
  const result = spawnSync(
    process.execPath,
    [
      resolve(options.rootDir, 'node_modules/astro/bin/astro.mjs'),
      'build',
      '--root',
      appRoot,
      '--silent',
    ],
    {
      cwd: options.rootDir,
      encoding: 'utf8',
      env: {
        ...process.env,
        ASTRO_TELEMETRY_DISABLED: '1',
        IUM_BUILD_PROFILE: options.profile,
        IUM_BASE_PATH: base,
        IUM_OUTPUT_DIR: resolve(options.outputDir),
        PUBLIC_IUM_BUILD_REVISION: options.buildRevision ?? 'stable',
      },
    },
  );
  if (result.status !== 0) {
    throw new Error(
      `Astro build failed (${result.status ?? 'no status'}):\n${result.stdout}${result.stderr}`,
    );
  }
}

async function main(): Promise<void> {
  const profile = process.argv[2] ?? '';
  assertProfile(profile);
  const rootDir = process.cwd();
  await buildPortalToDirectory({
    profile,
    base: process.argv[3] ?? '/',
    rootDir,
    outputDir: process.argv[4] ?? resolve(rootDir, 'apps/lernwerk-portal/dist'),
  });
}

if (process.argv[1]?.endsWith('build-portal.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
