import { resolve } from 'node:path';
import { buildPortalToDirectory } from './build-portal.js';
import type { BuildProfile } from './build-module-registry.js';
import { parsePublicationMode } from './publication-mode.js';

function assertProfile(value: string): asserts value is BuildProfile {
  if (value !== 'production' && value !== 'fixture' && value !== 'v2-development') {
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

  process.env.ASTRO_TELEMETRY_DISABLED = '1';
  process.env.IUM_BUILD_PROFILE = profile;
  process.env.IUM_PUBLICATION_MODE = publicationMode;
  process.env.IUM_BASE_PATH = base;
  process.env.IUM_OUTPUT_DIR = outputDir;
  const { preview } = await import('astro');
  const requestedPort = Number.parseInt(port, 10);
  if (!Number.isInteger(requestedPort)) throw new Error(`Invalid preview port: ${port}`);
  const server = await preview({
    root: appRoot,
    server: { host: '127.0.0.1', port: requestedPort },
  });
  if (server.port !== requestedPort) {
    await server.stop();
    throw new Error(`Preview port ${requestedPort} is occupied; refused fallback port ${server.port}`);
  }
  await new Promise<void>((accept, reject) => {
    let stopping = false;
    const stop = () => {
      if (stopping) return;
      stopping = true;
      void server.stop().then(accept, reject);
    };
    process.once('SIGINT', stop);
    process.once('SIGTERM', stop);
    void server.closed().then(accept, reject);
  });
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
