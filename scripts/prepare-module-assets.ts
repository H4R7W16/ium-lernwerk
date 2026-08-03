import { copyFile, mkdir, rm } from 'node:fs/promises';
import { relative, resolve, sep } from 'node:path';
import type { BuildProfile } from './build-module-registry.js';

export type PrepareModuleAssetsOptions = Readonly<{
  profile: BuildProfile;
  rootDir: string;
}>;

function assertInside(expectedParent: string, candidate: string): void {
  const relation = relative(resolve(expectedParent), resolve(candidate));
  if (relation === '..' || relation.startsWith(`..${sep}`)) {
    throw new Error(`Generated module asset path escapes public root: ${candidate}`);
  }
}

export async function prepareModuleAssets(
  options: PrepareModuleAssetsOptions,
): Promise<void> {
  const publicRoot = resolve(options.rootDir, 'apps/lernwerk-portal/public');
  const generatedRoot = resolve(publicRoot, 'generated-modules');
  assertInside(publicRoot, generatedRoot);

  await rm(generatedRoot, { recursive: true, force: true });
  await mkdir(generatedRoot, { recursive: true });

  if (options.profile === 'fixture') {
    return;
  }

  const source = resolve(
    options.rootDir,
    'modules/IUM-5-CORE-05/assets/delivery-robot.svg',
  );
  const targetDirectory = resolve(generatedRoot, 'ium-5-core-05');
  const target = resolve(targetDirectory, 'delivery-robot.svg');
  assertInside(generatedRoot, target);
  await mkdir(targetDirectory, { recursive: true });
  await copyFile(source, target);
}
