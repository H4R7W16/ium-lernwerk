import { readFile, rm } from 'node:fs/promises';
import { resolve } from 'node:path';

async function prepareBrokenCandidate(outputDirectory: string): Promise<void> {
  const workerPath = resolve(outputDirectory, 'sw.js');
  const offlinePath = resolve(outputDirectory, 'offline/index.html');
  const worker = await readFile(workerPath, 'utf8');
  if (!worker.includes('offline/index.html')) {
    throw new Error('Service worker does not reference offline/index.html');
  }
  await rm(offlinePath);
}

async function main(): Promise<void> {
  const outputDirectory = process.argv[2];
  const mode = process.argv[3];
  if (!outputDirectory || (mode !== 'valid' && mode !== 'broken-missing-offline')) {
    throw new Error('Expected output directory and a supported candidate mode');
  }
  if (mode === 'valid') {
    return;
  }
  await prepareBrokenCandidate(resolve(outputDirectory));
}

if (process.argv[1]?.endsWith('prepare-device-candidate.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
