import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, expect, test } from 'vitest';
import { checkWorkspaceBoundaries } from '../../scripts/check-workspace-boundaries.js';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
const temporaryRoots: string[] = [];

afterEach(async () => {
  await Promise.all(
    temporaryRoots.splice(0).map((path) => rm(path, { recursive: true, force: true })),
  );
});

async function createWorkspace(
  workspacePath: string,
  packageJson: object,
  source: string,
): Promise<string> {
  const root = await mkdtemp(join(tmpdir(), 'ium-boundary-'));
  temporaryRoots.push(root);
  const directory = join(root, workspacePath);
  await mkdir(join(directory, 'src'), { recursive: true });
  await writeFile(join(directory, 'package.json'), `${JSON.stringify(packageJson)}\n`);
  await writeFile(join(directory, 'src', 'index.ts'), source);
  return root;
}

test('accepts the approved current workspace graph', async () => {
  const report = await checkWorkspaceBoundaries({ rootDir: repoRoot });
  expect(report.violations).toEqual([]);
});

test('rejects idb outside local-state', async () => {
  const root = await createWorkspace(
    'packages/export-import',
    {
      name: '@ium/export-import',
      version: '0.1.0',
      private: true,
      dependencies: { idb: '8.0.3' },
    },
    "import { openDB } from 'idb';\nexport { openDB };\n",
  );
  const report = await checkWorkspaceBoundaries({ rootDir: root });
  expect(report.violations.map((violation) => violation.code)).toContain(
    'DIRECT_IDB_IMPORT',
  );
});

test('recognizes IUM5 as a dependency-closed, framework-free core package', async () => {
  const root = await createWorkspace(
    'packages/ium-5-core-05',
    {
      name: '@ium/ium-5-core-05',
      version: '0.1.0',
      private: true,
      dependencies: { astro: '7.1.6' },
    },
    "import 'astro';\nexport const body = document.body;\n",
  );
  const report = await checkWorkspaceBoundaries({ rootDir: root });
  const codes = report.violations.map((violation) => violation.code);

  expect(codes).not.toContain('UNKNOWN_WORKSPACE');
  expect(codes).toContain('UNAPPROVED_DEPENDENCY');
  expect(codes).toContain('FRAMEWORK_IMPORT_IN_CORE');
  expect(codes).toContain('DOM_USAGE_IN_CORE');
});
