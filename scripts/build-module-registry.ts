import { createHash } from 'node:crypto';
import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, isAbsolute, relative, resolve, sep } from 'node:path';
import { parse } from 'yaml';
import {
  validateModuleManifest,
  type ModuleManifest,
} from '../packages/module-contract/src/index.js';
import {
  parseWorkbenchResources,
  type WorkbenchResources,
} from '../packages/ium-5-core-05/src/index.js';

export type BuildProfile = 'production' | 'fixture';

export type BuildRegistryOptions = Readonly<{
  profile: BuildProfile;
  rootDir: string;
  outputDir: string;
}>;

export type ModuleRegistryEntry = Readonly<{
  id: string;
  version: string;
  title: string;
  grade: number;
  kind: string;
  strands: readonly string[];
  time: ModuleManifest['time'];
  centralQuestion: string;
  entryPath: string;
  countsTowardCoverage: boolean;
  publishedStatus: ModuleManifest['status'] | null;
  renderer: 'fixture-workspace' | 'algorithm-workbench';
  workbench?: Readonly<{
    content: WorkbenchResources['content'];
    scenarios: WorkbenchResources['scenarios'];
    robotAssetPath: 'generated-modules/ium-5-core-05/delivery-robot.svg';
  }>;
}>;

export type ModuleRegistry = Readonly<{
  schemaVersion: 1;
  profile: BuildProfile;
  releaseId: string;
  modules: readonly ModuleRegistryEntry[];
}>;

const profileRoots = {
  production: {
    modules: 'modules',
    curriculum: [
      'curriculum/lesehilfe-2026-27/competencies.json',
      'curriculum/basiskurs-medienbildung/competencies.json',
      'curriculum/aufbaukurs-informatik/competencies.json',
    ],
  },
  fixture: {
    modules: 'tests/fixtures/reference-module',
    curriculum: ['tests/fixtures/curriculum/competencies.json'],
  },
} as const;

function assertProfile(value: string): asserts value is BuildProfile {
  if (value !== 'production' && value !== 'fixture') {
    throw new Error(`Unknown registry profile: ${value}`);
  }
}

function insideRoot(rootDir: string, candidate: string): string {
  if (isAbsolute(candidate)) {
    throw new Error(`Absolute paths are not allowed: ${candidate}`);
  }
  const root = resolve(rootDir);
  const target = resolve(root, candidate);
  const relation = relative(root, target);
  if (relation === '..' || relation.startsWith(`..${sep}`)) {
    throw new Error(`Path escapes repository root: ${candidate}`);
  }
  return target;
}

async function fileExists(path: string): Promise<boolean> {
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

async function collectFiles(root: string): Promise<string[]> {
  let entries;
  try {
    entries = await readdir(root, { withFileTypes: true });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      return [];
    }
    throw error;
  }
  const paths: string[] = [];
  for (const entry of entries.sort((left, right) => left.name.localeCompare(right.name))) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) {
      paths.push(...(await collectFiles(path)));
    } else if (entry.isFile()) {
      paths.push(path);
    }
  }
  return paths;
}

function normalizeRelative(rootDir: string, path: string): string {
  return relative(resolve(rootDir), resolve(path)).split(sep).join('/');
}

export async function computeReleaseId(
  paths: readonly string[],
  rootDir: string,
  profile: BuildProfile,
): Promise<string> {
  const hash = createHash('sha256');
  hash.update(`profile\0${profile}\0`, 'utf8');
  for (const path of [...paths].sort((left, right) =>
    normalizeRelative(rootDir, left).localeCompare(normalizeRelative(rootDir, right)))) {
    hash.update(normalizeRelative(rootDir, path), 'utf8');
    hash.update('\0', 'utf8');
    hash.update(await readFile(path));
    hash.update('\0', 'utf8');
  }
  return `ium-${hash.digest('hex').slice(0, 16)}`;
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(canonicalize);
  }
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([key, entry]) => [key, canonicalize(entry)]),
    );
  }
  return value;
}

export function renderRegistry(registry: ModuleRegistry): Uint8Array {
  return new TextEncoder().encode(
    `${JSON.stringify(canonicalize(registry), null, 2)}\n`,
  );
}

async function loadCompetencyIds(paths: readonly string[]): Promise<Set<string>> {
  const ids = new Set<string>();
  for (const path of paths) {
    const payload = JSON.parse(await readFile(path, 'utf8')) as {
      records?: readonly { id?: unknown }[];
    };
    for (const record of payload.records ?? []) {
      if (typeof record.id === 'string') {
        ids.add(record.id);
      }
    }
  }
  return ids;
}

async function loadManifest(path: string): Promise<ModuleManifest> {
  const raw = parse(await readFile(path, 'utf8')) as unknown;
  if (raw !== null && typeof raw === 'object') {
    const authorFields = raw as Record<string, unknown>;
    if ('countsTowardCoverage' in authorFields || 'publishedStatus' in authorFields) {
      throw new Error(`Manifest contains generated-only status fields: ${path}`);
    }
  }
  const result = validateModuleManifest(raw);
  if (!result.ok) {
    throw new Error(`Invalid module manifest ${path}: ${JSON.stringify(result.issues)}`);
  }
  return result.value;
}

function rendererFor(
  manifest: ModuleManifest,
  profile: BuildProfile,
): 'fixture-workspace' | 'algorithm-workbench' {
  if (
    profile === 'fixture'
    && manifest.id === 'TEST-PLATFORM-REFERENCE'
    && manifest.components.length === 1
    && manifest.components[0] === 'fixture-workspace'
  ) {
    return 'fixture-workspace';
  }
  if (
    profile === 'production'
    && manifest.id === 'IUM-5-CORE-05'
    && manifest.components.length === 1
    && manifest.components[0] === 'algorithm-workbench'
  ) {
    return 'algorithm-workbench';
  }
  throw new Error(`No static renderer contract for ${manifest.id}`);
}

export async function buildRegistry(
  options: BuildRegistryOptions,
): Promise<ModuleRegistry> {
  assertProfile(options.profile);
  const roots = profileRoots[options.profile];
  const moduleRoot = insideRoot(options.rootDir, roots.modules);
  const curriculumPaths = roots.curriculum.map((path) => insideRoot(options.rootDir, path));
  for (const path of curriculumPaths) {
    if (!(await fileExists(path))) {
      throw new Error(`Missing curriculum source: ${normalizeRelative(options.rootDir, path)}`);
    }
  }
  const competencyIds = await loadCompetencyIds(curriculumPaths);
  const moduleFiles = (await collectFiles(moduleRoot)).filter((path) => path.endsWith(`${sep}module.yaml`) || path === resolve(moduleRoot, 'module.yaml'));
  const sourceFiles = [...curriculumPaths, ...(await collectFiles(moduleRoot))];
  const entries: ModuleRegistryEntry[] = [];
  const seenIds = new Set<string>();

  for (const manifestPath of moduleFiles) {
    const manifest = await loadManifest(manifestPath);
    if (seenIds.has(manifest.id)) {
      throw new Error(`Duplicate module ID: ${manifest.id}`);
    }
    seenIds.add(manifest.id);
    const fixtureId = manifest.id.startsWith('TEST-');
    if (options.profile === 'fixture' && !fixtureId) {
      throw new Error(`Fixture profile contains a real module ID: ${manifest.id}`);
    }
    if (options.profile === 'production' && fixtureId) {
      throw new Error(`Production profile contains a TEST module ID: ${manifest.id}`);
    }
    for (const competencyId of manifest.curriculum.competencyIds) {
      if (!competencyIds.has(competencyId)) {
        throw new Error(`Unresolved competency ${competencyId} in ${manifest.id}`);
      }
      if (options.profile === 'fixture' && !competencyId.startsWith('TEST-')) {
        throw new Error(`Fixture profile contains a real competency ID: ${competencyId}`);
      }
    }
    for (const evidenceId of manifest.curriculum.coverageEvidenceIds) {
      const fixtureReference = evidenceId.startsWith('TEST-');
      if (options.profile === 'fixture' && !fixtureReference) {
        throw new Error(
          `Fixture profile contains a real coverage reference: ${evidenceId}`,
        );
      }
      if (options.profile === 'production' && fixtureReference) {
        throw new Error(
          `Production profile contains a TEST coverage reference: ${evidenceId}`,
        );
      }
    }
    const manifestRoot = dirname(manifestPath);
    const entryPath = insideRoot(manifestRoot, 'lernumgebung/index.md');
    const licensePath = insideRoot(manifestRoot, manifest.licenses.assetEvidencePath);
    for (const requiredPath of [entryPath, licensePath]) {
      if (!(await fileExists(requiredPath))) {
        throw new Error(`Missing referenced module file: ${normalizeRelative(options.rootDir, requiredPath)}`);
      }
    }
    const renderer = rendererFor(manifest, options.profile);
    const baseEntry = {
      id: manifest.id,
      version: manifest.version,
      title: manifest.title,
      grade: manifest.grade,
      kind: manifest.kind,
      strands: manifest.strands,
      time: manifest.time,
      centralQuestion: manifest.learningDesign.centralQuestion,
      entryPath: normalizeRelative(options.rootDir, entryPath),
      countsTowardCoverage: options.profile === 'production',
      publishedStatus: options.profile === 'production' ? manifest.status : null,
      renderer,
    } as const;
    if (renderer === 'algorithm-workbench') {
      const contentPath = insideRoot(manifestRoot, 'lernumgebung/content.json');
      const scenariosPath = insideRoot(manifestRoot, 'lernumgebung/scenarios.json');
      const resources = parseWorkbenchResources(
        JSON.parse(await readFile(contentPath, 'utf8')) as unknown,
        JSON.parse(await readFile(scenariosPath, 'utf8')) as unknown,
      );
      if (!resources.ok) {
        throw new Error(
          `Invalid workbench resources for ${manifest.id}: ${JSON.stringify(resources.issues)}`,
        );
      }
      entries.push({
        ...baseEntry,
        workbench: {
          content: resources.value.content,
          scenarios: resources.value.scenarios,
          robotAssetPath: 'generated-modules/ium-5-core-05/delivery-robot.svg',
        },
      });
    } else {
      entries.push(baseEntry);
    }
  }

  entries.sort((left, right) => left.id.localeCompare(right.id));
  const registry: ModuleRegistry = {
    schemaVersion: 1,
    profile: options.profile,
    releaseId: await computeReleaseId(sourceFiles, options.rootDir, options.profile),
    modules: entries,
  };
  await mkdir(options.outputDir, { recursive: true });
  await writeFile(resolve(options.outputDir, 'module-registry.json'), renderRegistry(registry));
  const buildInfo = canonicalize({
    schemaVersion: 1,
    profile: options.profile,
    releaseId: registry.releaseId,
    moduleCount: registry.modules.length,
  });
  await writeFile(
    resolve(options.outputDir, 'build-info.json'),
    `${JSON.stringify(buildInfo, null, 2)}\n`,
    'utf8',
  );
  return registry;
}

async function main(): Promise<void> {
  const profile = process.argv[2] ?? '';
  assertProfile(profile);
  await buildRegistry({
    profile,
    rootDir: process.cwd(),
    outputDir: resolve('apps/lernwerk-portal/src/generated'),
  });
}

if (process.argv[1]?.endsWith('build-module-registry.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
