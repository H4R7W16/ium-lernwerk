import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { buildPortalToDirectory } from './build-portal.js';
import type { BuildProfile } from './build-module-registry.js';
import { parsePublicationMode } from './publication-mode.js';

function assertProfile(value: string): asserts value is BuildProfile {
  if (value !== 'production' && value !== 'fixture') {
    throw new Error(`Unknown portal preview profile: ${value}`);
  }
}

async function main(): Promise<void> {
  const profile = process.argv[2] ?? '';
  assertProfile(profile);
  const publicationMode = parsePublicationMode(process.argv[3] ?? '');
  const base = process.argv[4] ?? '/';
  const port = process.argv[5] ?? '4321';
  const rootDir = process.cwd();
  const appRoot = resolve(rootDir, 'apps/lernwerk-portal');
  const outputDir = resolve(appRoot, 'dist');
  await buildPortalToDirectory({
    profile,
    publicationMode,
    base,
    rootDir,
    outputDir,
    buildRevision: process.env.IUM_BUILD_REVISION,
    previewId: process.env.IUM_PREVIEW_ID,
  });

  const child = spawn(
    process.execPath,
    [
      resolve(rootDir, 'node_modules/astro/bin/astro.mjs'),
      'preview',
      '--root',
      appRoot,
      '--host',
      '127.0.0.1',
      '--port',
      port,
    ],
    {
      cwd: rootDir,
      stdio: 'inherit',
      env: {
        ...process.env,
        ASTRO_TELEMETRY_DISABLED: '1',
        IUM_BUILD_PROFILE: profile,
        IUM_PUBLICATION_MODE: publicationMode,
        IUM_BASE_PATH: base,
        IUM_OUTPUT_DIR: outputDir,
      },
    },
  );
  const stop = () => child.kill();
  process.once('SIGINT', stop);
  process.once('SIGTERM', stop);
  const code = await new Promise<number>((accept, reject) => {
    child.once('error', reject);
    child.once('exit', (exitCode) => accept(exitCode ?? 1));
  });
  process.exitCode = code;
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
