import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
import { buildRegistry } from './build-module-registry.js';

async function main(): Promise<void> {
  const rootDir = process.cwd();
  const appRoot = resolve(rootDir, 'apps/lernwerk-portal');
  await buildRegistry({
    profile: 'fixture',
    rootDir,
    outputDir: resolve(appRoot, 'src/generated'),
  });
  const result = spawnSync(
    process.execPath,
    [
      resolve(rootDir, 'node_modules/astro/bin/astro.mjs'),
      'check',
      '--root',
      appRoot,
    ],
    {
      cwd: rootDir,
      encoding: 'utf8',
      env: {
        ...process.env,
        ASTRO_TELEMETRY_DISABLED: '1',
        IUM_BUILD_PROFILE: 'fixture',
        IUM_BASE_PATH: '/',
      },
    },
  );
  process.stdout.write(result.stdout);
  process.stderr.write(result.stderr);
  if (result.status !== 0) {
    process.exitCode = result.status ?? 1;
  }
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
