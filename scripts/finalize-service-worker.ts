import { readFile, rm, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { injectManifest } from 'workbox-build';
import { createPrecacheIntegrityTransform } from './precache-integrity.js';

const INJECTION_POINT = 'self.__WB_MANIFEST';
const MAXIMUM_FILE_SIZE_TO_CACHE = 2 * 1024 * 1024;

export type ServiceWorkerFinalization = {
  repaired: boolean;
  entryCount: number;
};

export async function finalizeServiceWorker(
  outputDir: string,
  base: string,
): Promise<ServiceWorkerFinalization> {
  const serviceWorkerPath = resolve(outputDir, 'sw.js');
  const source = await readFile(serviceWorkerPath, 'utf8');
  const injectionPoints = source.match(/self\.__WB_MANIFEST/g) ?? [];

  if (injectionPoints.length === 0) {
    return { repaired: false, entryCount: 0 };
  }
  if (injectionPoints.length !== 1) {
    throw new Error(
      `Expected exactly one Workbox injection point, found ${injectionPoints.length}.`,
    );
  }

  const temporarySourcePath = resolve(outputDir, '.ium-sw-source.js');
  await writeFile(temporarySourcePath, source, 'utf8');

  try {
    const result = await injectManifest({
      swSrc: temporarySourcePath,
      swDest: serviceWorkerPath,
      globDirectory: outputDir,
      globPatterns: ['**/*.{html,css,js,png,svg,webmanifest,json}'],
      globIgnores: ['sw.js', '.ium-sw-source.js', '.vite-cache/**'],
      modifyURLPrefix: { '': base },
      maximumFileSizeToCacheInBytes: MAXIMUM_FILE_SIZE_TO_CACHE,
      injectionPoint: INJECTION_POINT,
      manifestTransforms: [createPrecacheIntegrityTransform(outputDir, base)],
    });
    const finalizedSource = await readFile(serviceWorkerPath, 'utf8');
    if (finalizedSource.includes(INJECTION_POINT)) {
      throw new Error('Workbox injection point remained after service-worker finalization.');
    }
    return { repaired: true, entryCount: result.count };
  } finally {
    await rm(temporarySourcePath, { force: true });
  }
}
