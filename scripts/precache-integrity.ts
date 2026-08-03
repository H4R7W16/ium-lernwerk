import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { resolve, sep } from 'node:path';

type ManifestEntry = Readonly<{
  integrity?: string;
  revision?: string | null;
  url: string;
}>;

type ManifestTransformResult = Readonly<{
  manifest: readonly ManifestEntry[];
  warnings: readonly string[];
}>;

export function createPrecacheIntegrityTransform(outputDir: string, base: string) {
  const outputRoot = resolve(outputDir);
  const basePrefix = base.replace(/^\/+|\/+$/g, '');

  return async (entries: readonly ManifestEntry[]): Promise<ManifestTransformResult> => ({
    manifest: await Promise.all(entries.map(async (entry) => {
      const pathname = decodeURIComponent(
        new URL(entry.url, 'https://ium.invalid').pathname,
      ).replace(/^\/+/, '');
      const relativePath = basePrefix && pathname.startsWith(`${basePrefix}/`)
        ? pathname.slice(basePrefix.length + 1)
        : pathname;
      const assetPath = resolve(outputRoot, relativePath);
      if (assetPath !== outputRoot && !assetPath.startsWith(`${outputRoot}${sep}`)) {
        throw new Error(`Precache asset escapes output directory: ${entry.url}`);
      }
      const digest = createHash('sha384')
        .update(await readFile(assetPath))
        .digest('base64');
      return { ...entry, integrity: `sha384-${digest}` };
    })),
    warnings: [],
  });
}
