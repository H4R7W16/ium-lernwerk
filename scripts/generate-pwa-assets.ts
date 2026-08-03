import { spawnSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const root = process.cwd();
mkdirSync(resolve(root, 'apps/lernwerk-portal/public/icons'), { recursive: true });

const result = spawnSync(
  process.execPath,
  [
    resolve(root, 'node_modules/@vite-pwa/assets-generator/bin/pwa-assets-generator.mjs'),
    '--config',
    'pwa-assets.config.ts',
  ],
  { cwd: root, stdio: 'inherit' },
);

if (result.error) {
  throw result.error;
}
process.exitCode = result.status ?? 1;
