import { readdir, readFile } from 'node:fs/promises';
import { relative, resolve, sep } from 'node:path';

export type BoundaryViolationCode =
  | 'UNKNOWN_WORKSPACE'
  | 'UNAPPROVED_DEPENDENCY'
  | 'UNPINNED_DEPENDENCY'
  | 'DEPENDENCY_CYCLE'
  | 'DIRECT_IDB_IMPORT'
  | 'FRAMEWORK_IMPORT_IN_CORE'
  | 'DOM_USAGE_IN_CORE';

export type BoundaryViolation = Readonly<{
  code: BoundaryViolationCode;
  workspace: string;
  path: string;
  detail: string;
}>;

export type BoundaryReport = Readonly<{
  workspaces: readonly string[];
  violations: readonly BoundaryViolation[];
}>;

const approvedDependencies: Readonly<Record<string, ReadonlySet<string>>> = {
  '@ium/module-contract': new Set(['ajv', 'ajv-formats']),
  '@ium/local-state': new Set(['@ium/module-contract', 'idb']),
  '@ium/export-import': new Set(['@ium/module-contract']),
  '@ium/module-runtime': new Set(['@ium/module-contract', '@ium/export-import']),
  '@ium/ui-components': new Set([
    '@ium/module-contract',
    '@ium/module-runtime',
    '@ium/export-import',
  ]),
  '@ium/lernwerk-portal': new Set([
    '@ium/module-contract',
    '@ium/local-state',
    '@ium/export-import',
    '@ium/module-runtime',
    '@ium/ui-components',
    'astro',
    'vite-plugin-pwa',
    'workbox-core',
    'workbox-precaching',
    'workbox-routing',
  ]),
};

const corePackages = new Set([
  '@ium/module-contract',
  '@ium/local-state',
  '@ium/export-import',
  '@ium/module-runtime',
]);
const ignoredDirectories = new Set(['dist', 'generated', 'node_modules']);

type Workspace = Readonly<{
  name: string;
  path: string;
  packagePath: string;
  dependencies: Readonly<Record<string, string>>;
}>;

async function exists(path: string): Promise<boolean> {
  try {
    await readFile(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return false;
    }
    throw error;
  }
}

async function discoverWorkspaces(rootDir: string): Promise<Workspace[]> {
  const workspaces: Workspace[] = [];
  for (const parentName of ['packages', 'apps']) {
    const parent = resolve(rootDir, parentName);
    let entries;
    try {
      entries = await readdir(parent, { withFileTypes: true });
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        continue;
      }
      throw error;
    }
    for (const entry of entries) {
      if (!entry.isDirectory()) {
        continue;
      }
      const path = resolve(parent, entry.name);
      const packagePath = resolve(path, 'package.json');
      if (!(await exists(packagePath))) {
        continue;
      }
      const payload = JSON.parse(await readFile(packagePath, 'utf8')) as {
        name?: unknown;
        dependencies?: Record<string, string>;
        devDependencies?: Record<string, string>;
        peerDependencies?: Record<string, string>;
      };
      workspaces.push({
        name: typeof payload.name === 'string' ? payload.name : `<${entry.name}>`,
        path,
        packagePath,
        dependencies: {
          ...(payload.dependencies ?? {}),
          ...(payload.devDependencies ?? {}),
          ...(payload.peerDependencies ?? {}),
        },
      });
    }
  }
  return workspaces.sort((left, right) => left.name.localeCompare(right.name));
}

async function sourceFiles(root: string): Promise<string[]> {
  let entries;
  try {
    entries = await readdir(root, { withFileTypes: true });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return [];
    }
    throw error;
  }
  const result: string[] = [];
  for (const entry of entries) {
    if (entry.isDirectory() && !ignoredDirectories.has(entry.name)) {
      result.push(...(await sourceFiles(resolve(root, entry.name))));
    } else if (entry.isFile() && /\.(?:ts|mts|astro)$/.test(entry.name)) {
      result.push(resolve(root, entry.name));
    }
  }
  return result;
}

function addViolation(
  violations: BoundaryViolation[],
  rootDir: string,
  workspace: string,
  path: string,
  code: BoundaryViolationCode,
  detail: string,
): void {
  violations.push({
    code,
    workspace,
    path: relative(rootDir, path).split(sep).join('/'),
    detail,
  });
}

function cycleViolations(
  workspaces: readonly Workspace[],
  rootDir: string,
): BoundaryViolation[] {
  const byName = new Map(workspaces.map((workspace) => [workspace.name, workspace]));
  const visiting = new Set<string>();
  const visited = new Set<string>();
  const violations: BoundaryViolation[] = [];

  function visit(name: string, chain: readonly string[]): void {
    if (visiting.has(name)) {
      const workspace = byName.get(name);
      if (workspace) {
        addViolation(
          violations,
          rootDir,
          name,
          workspace.packagePath,
          'DEPENDENCY_CYCLE',
          [...chain, name].join(' -> '),
        );
      }
      return;
    }
    if (visited.has(name)) {
      return;
    }
    const workspace = byName.get(name);
    if (!workspace) {
      return;
    }
    visiting.add(name);
    for (const dependency of Object.keys(workspace.dependencies)) {
      if (byName.has(dependency)) {
        visit(dependency, [...chain, name]);
      }
    }
    visiting.delete(name);
    visited.add(name);
  }

  for (const workspace of workspaces) {
    visit(workspace.name, []);
  }
  return violations;
}

export async function checkWorkspaceBoundaries(options: {
  rootDir: string;
}): Promise<BoundaryReport> {
  const rootDir = resolve(options.rootDir);
  const workspaces = await discoverWorkspaces(rootDir);
  const violations: BoundaryViolation[] = [];

  for (const workspace of workspaces) {
    const approved = approvedDependencies[workspace.name];
    if (!approved) {
      addViolation(
        violations,
        rootDir,
        workspace.name,
        workspace.packagePath,
        'UNKNOWN_WORKSPACE',
        'Workspace is not part of the approved Phase-1 graph',
      );
      continue;
    }
    for (const [dependency, version] of Object.entries(workspace.dependencies)) {
      if (!approved.has(dependency)) {
        addViolation(
          violations,
          rootDir,
          workspace.name,
          workspace.packagePath,
          'UNAPPROVED_DEPENDENCY',
          dependency,
        );
      }
      if (/^[~^]|\*|\bx\b|\bX\b/.test(version)) {
        addViolation(
          violations,
          rootDir,
          workspace.name,
          workspace.packagePath,
          'UNPINNED_DEPENDENCY',
          `${dependency}@${version}`,
        );
      }
    }

    for (const path of await sourceFiles(resolve(workspace.path, 'src'))) {
      const source = await readFile(path, 'utf8');
      const imports = [...source.matchAll(
        /(?:from\s+|import\s*\(\s*|import\s+)["']([^"']+)["']/g,
      )].map((match) => match[1]);
      if (workspace.name !== '@ium/local-state' && imports.includes('idb')) {
        addViolation(
          violations,
          rootDir,
          workspace.name,
          path,
          'DIRECT_IDB_IMPORT',
          'Only @ium/local-state may import idb',
        );
      }
      if (corePackages.has(workspace.name) && imports.some((value) =>
        value === 'astro' || value.startsWith('astro/'))) {
        addViolation(
          violations,
          rootDir,
          workspace.name,
          path,
          'FRAMEWORK_IMPORT_IN_CORE',
          'Core packages must remain framework-free',
        );
      }
      if (
        corePackages.has(workspace.name)
        && /\b(?:window|document|navigator|HTMLElement|customElements)\b/.test(source)
      ) {
        addViolation(
          violations,
          rootDir,
          workspace.name,
          path,
          'DOM_USAGE_IN_CORE',
          'Core packages must not access browser DOM globals',
        );
      }
    }
  }

  violations.push(...cycleViolations(workspaces, rootDir));
  violations.sort((left, right) =>
    `${left.workspace}\0${left.path}\0${left.code}`.localeCompare(
      `${right.workspace}\0${right.path}\0${right.code}`,
    ));
  return {
    workspaces: workspaces.map((workspace) => workspace.name),
    violations,
  };
}

async function main(): Promise<void> {
  const report = await checkWorkspaceBoundaries({ rootDir: process.cwd() });
  if (report.violations.length > 0) {
    for (const violation of report.violations) {
      console.error(
        `${violation.code} ${violation.workspace} ${violation.path}: ${violation.detail}`,
      );
    }
    process.exitCode = 1;
    return;
  }
  console.log(`Workspace boundaries passed: ${report.workspaces.length} workspaces`);
}

if (process.argv[1]?.endsWith('check-workspace-boundaries.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
