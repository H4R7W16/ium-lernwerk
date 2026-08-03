import { spawnSync } from 'node:child_process';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { afterEach, expect, test } from 'vitest';

const temporaryOutputs: string[] = [];

afterEach(async () => {
  await Promise.all(
    temporaryOutputs.splice(0).map((path) => rm(path, { recursive: true, force: true })),
  );
});

async function fixtureOutput(): Promise<string> {
  const outputDirectory = await mkdtemp(resolve(tmpdir(), 'ium-device-candidate-'));
  temporaryOutputs.push(outputDirectory);
  await mkdir(resolve(outputDirectory, 'offline'));
  await writeFile(resolve(outputDirectory, 'offline/index.html'), 'offline fallback\n');
  await writeFile(
    resolve(outputDirectory, 'sw.js'),
    'precacheAndRoute([{"url":"offline/index.html","revision":"fixture"}]);\n',
  );
  return outputDirectory;
}

test('broken candidate removes only the offline asset referenced by its worker', async () => {
  const outputDirectory = await fixtureOutput();
  const workerBefore = await readFile(resolve(outputDirectory, 'sw.js'), 'utf8');

  const result = spawnSync(
    process.execPath,
    [
      resolve('node_modules/tsx/dist/cli.mjs'),
      resolve('scripts/prepare-device-candidate.ts'),
      outputDirectory,
      'broken-missing-offline',
    ],
    { cwd: process.cwd(), encoding: 'utf8' },
  );

  expect(result.status, `${result.stdout}${result.stderr}`).toBe(0);
  await expect(readFile(resolve(outputDirectory, 'offline/index.html'))).rejects.toMatchObject({
    code: 'ENOENT',
  });
  await expect(readFile(resolve(outputDirectory, 'sw.js'), 'utf8')).resolves.toBe(workerBefore);
});

test('valid candidate leaves the verified build unchanged', async () => {
  const outputDirectory = await fixtureOutput();
  const workerBefore = await readFile(resolve(outputDirectory, 'sw.js'), 'utf8');
  const offlineBefore = await readFile(resolve(outputDirectory, 'offline/index.html'), 'utf8');

  const result = spawnSync(
    process.execPath,
    [
      resolve('node_modules/tsx/dist/cli.mjs'),
      resolve('scripts/prepare-device-candidate.ts'),
      outputDirectory,
      'valid',
    ],
    { cwd: process.cwd(), encoding: 'utf8' },
  );

  expect(result.status).toBe(0);
  await expect(readFile(resolve(outputDirectory, 'offline/index.html'), 'utf8')).resolves.toBe(
    offlineBefore,
  );
  await expect(readFile(resolve(outputDirectory, 'sw.js'), 'utf8')).resolves.toBe(workerBefore);
});
