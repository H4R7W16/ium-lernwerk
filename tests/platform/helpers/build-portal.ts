import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  buildPortalToDirectory,
} from '../../../scripts/build-portal.js';
import type { BuildProfile } from '../../../scripts/build-module-registry.js';

const repoRoot = fileURLToPath(new URL('../../..', import.meta.url));

async function collectFiles(root: string): Promise<string[]> {
  const entries = await readdir(root, { withFileTypes: true });
  const result: string[] = [];
  for (const entry of entries) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) {
      result.push(...(await collectFiles(path)));
    } else if (entry.isFile()) {
      result.push(path);
    }
  }
  return result;
}

function globPattern(pattern: string): RegExp {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, '\\$&');
  const source = escaped
    .replaceAll('**', '\u0000')
    .replaceAll('*', '[^/]*')
    .replaceAll('\u0000', '.*');
  return new RegExp(`^${source}$`);
}

export type BuiltPortal = Readonly<{
  distDir: string;
  manifest: Readonly<Record<string, unknown>>;
  serviceWorkerText: string;
  externalUrls: readonly string[];
  text(path: string): Promise<string>;
  glob(pattern: string): Promise<string[]>;
  cleanup(): Promise<void>;
}>;

export async function buildPortal(
  profile: BuildProfile,
  base: string,
): Promise<BuiltPortal> {
  const distDir = await mkdtemp(join(tmpdir(), 'ium-portal-'));
  await buildPortalToDirectory({ profile, base, rootDir: repoRoot, outputDir: distDir });
  const files = await collectFiles(distDir);
  const relativeFiles = files
    .map((path) => relative(distDir, path).split(sep).join('/'))
    .sort();
  const manifestPath = relativeFiles.find((path) => path.endsWith('.webmanifest'));
  const serviceWorkerPath = relativeFiles.find((path) => /(?:^|\/)sw\.js$/.test(path));
  const textFiles = relativeFiles.filter((path) => /\.(?:html|css|js|json|webmanifest)$/.test(path));
  const externalUrls = new Set<string>();
  for (const path of textFiles) {
    const source = await readFile(resolve(distDir, path), 'utf8');
    for (const match of source.matchAll(/(?:https?:)?\/\/[^\s"'<>]+/g)) {
      externalUrls.add(match[0]);
    }
  }

  return {
    distDir,
    manifest: manifestPath
      ? JSON.parse(await readFile(resolve(distDir, manifestPath), 'utf8')) as Record<string, unknown>
      : {},
    serviceWorkerText: serviceWorkerPath
      ? await readFile(resolve(distDir, serviceWorkerPath), 'utf8')
      : '',
    externalUrls: [...externalUrls].sort(),
    text: (path) => readFile(resolve(distDir, path), 'utf8'),
    async glob(pattern) {
      const matcher = globPattern(pattern);
      return relativeFiles.filter((path) => matcher.test(path));
    },
    cleanup: () => rm(distDir, { recursive: true, force: true }),
  };
}
