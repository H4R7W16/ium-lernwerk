import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, describe, expect, test } from 'vitest';
import {
  buildV2Registry,
  parseV2Candidate,
} from '../../scripts/build-v2-module-registry.js';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
const temporaryPaths: string[] = [];
const candidate = JSON.parse(
  await readFile(join(repoRoot, 'modules-v2', 'V2-G5-M06', 'module.json'), 'utf8'),
) as Record<string, unknown>;

afterEach(async () => {
  await Promise.all(temporaryPaths.splice(0).map((path) => rm(path, { recursive: true, force: true })));
});

describe('V2 development candidate registry', () => {
  test('accepts only the closed M06 candidate contract', () => {
    expect(parseV2Candidate(candidate)).toMatchObject({ ok: true });
    for (const mutation of [
      { baseline: undefined },
      { schemaVersion: 1 },
      { renderer: 'algorithm-workbench' },
      { payloadSchemaVersion: 2 },
      { curriculumCoverage: true },
      { lxfGateIds: (candidate.lxfGateIds as string[]).slice(1) },
      { curriculumRecordIds: ['LH26-E-ALG-001'] },
    ]) {
      const changed = { ...candidate, ...mutation };
      if (mutation.baseline === undefined) delete changed.baseline;
      expect(parseV2Candidate(changed), JSON.stringify(mutation)).toMatchObject({ ok: false });
    }
  });

  test('builds one unassessed V2 entry and binds release identity to material bytes', async () => {
    const output = await mkdtemp(join(tmpdir(), 'ium-v2-registry-'));
    temporaryPaths.push(output);
    const first = await buildV2Registry({ rootDir: repoRoot, outputDir: output });
    expect(first.profile).toBe('v2-development');
    expect(first.modules).toEqual([
      expect.objectContaining({
        id: 'V2-G5-M06',
        renderer: 'v2-m06',
        countsTowardCoverage: false,
        publishedStatus: null,
        curriculumCoverage: 'unassessed',
        pilot: 'not-started',
        publication: 'closed',
      }),
    ]);

    const root = await mkdtemp(join(tmpdir(), 'ium-v2-registry-root-'));
    temporaryPaths.push(root);
    await import('node:fs/promises').then(({ cp }) => cp(repoRoot, root, {
      recursive: true,
      filter: (source) => !source.includes(`${join(repoRoot, '.git')}`)
        && !source.includes(`${join(repoRoot, 'node_modules')}`),
    }));
    const material = join(root, 'modules-v2', 'V2-G5-M06', 'materials', 'start.md');
    await writeFile(material, `${await readFile(material, 'utf8')}\n`);
    const second = await buildV2Registry({
      rootDir: root,
      outputDir: join(root, 'generated'),
      buildRevision: 'a'.repeat(40),
    });
    expect(second.releaseId).not.toBe(first.releaseId);
  });
});
