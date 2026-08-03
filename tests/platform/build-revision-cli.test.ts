import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { afterEach, expect, test } from 'vitest';

const temporaryOutputs: string[] = [];

afterEach(async () => {
  await Promise.all(
    temporaryOutputs.splice(0).map((path) => rm(path, { recursive: true, force: true })),
  );
});

test('the CLI embeds an explicit revision in a real subpath fixture build', async () => {
  const outputDirectory = await mkdtemp(resolve(tmpdir(), 'ium-build-revision-'));
  temporaryOutputs.push(outputDirectory);

  const result = spawnSync(
    process.execPath,
    [
      resolve('node_modules/tsx/dist/cli.mjs'),
      resolve('scripts/build-portal.ts'),
      'fixture',
      '/ium-lernwerk/',
      outputDirectory,
    ],
    {
      cwd: process.cwd(),
      encoding: 'utf8',
      env: {
        ...process.env,
        IUM_BUILD_REVISION: 'device-update-test',
      },
    },
  );

  expect(result.status, `${result.stdout}${result.stderr}`).toBe(0);
  const html = await readFile(resolve(outputDirectory, 'index.html'), 'utf8');
  expect(html).toContain(
    '<meta name="ium-build-revision" content="device-update-test">',
  );
});
