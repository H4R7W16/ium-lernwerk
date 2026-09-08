import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { isAbsolute, relative, resolve, sep } from 'node:path';

export type M06Candidate = Readonly<{
  schemaVersion: 2;
  baseline: 'v2';
  id: 'V2-G5-M06';
  version: '0.1.0';
  renderer: 'v2-m06';
  payloadSchemaVersion: 1;
  status: 'draft';
  curriculumCoverage: 'unassessed';
  pilot: 'not-started';
  publication: 'closed';
  specPath: string;
  materialRevision: string;
  curriculumRecordIds: readonly string[];
  lxfGateIds: readonly string[];
  minutes: 225;
}>;

export type V2ModuleRegistryEntry = M06Candidate & Readonly<{
  grade: 5;
  title: 'Präzise Abläufe entwickeln und prüfen';
  contextTitle: 'Prüffahrt im Raster';
  centralQuestion: 'Wie entwickle und prüfe ich eine präzise Wiederholung?';
  entryPath: 'modules-v2/V2-G5-M06/materials/start.md';
  countsTowardCoverage: false;
  publishedStatus: null;
  resources: Readonly<{ content: unknown; cases: unknown }>;
}>;

export type V2ModuleRegistry = Readonly<{
  schemaVersion: 2;
  profile: 'v2-development';
  buildRevision: string;
  releaseId: string;
  modules: readonly V2ModuleRegistryEntry[];
}>;

export type BuildV2RegistryOptions = Readonly<{
  rootDir: string;
  outputDir: string;
  buildRevision?: string;
}>;

const candidateKeys = [
  'schemaVersion', 'baseline', 'id', 'version', 'renderer', 'payloadSchemaVersion',
  'status', 'curriculumCoverage', 'pilot', 'publication', 'specPath',
  'materialRevision', 'curriculumRecordIds', 'lxfGateIds', 'minutes',
] as const;
const curriculumIds = [
  'BMB16-GYM-PK-SK-001', 'LH26-E-ALG-001', 'LH26-E-ALG-002',
  'LH26-E-ALG-003', 'LH26-E-ALG-004', 'LH26-E-ALG-005', 'LH26-E-ALG-006',
] as const;
const lxfGateIds = [
  'evidence-integrity', 'goal-action-evidence-alignment', 'cognitive-economy',
  'disciplinary-learning-action', 'representation-coherence',
  'support-without-task-removal', 'feedback-and-next-action',
  'orientation-and-recovery', 'accessibility-and-equivalence',
  'teacher-orchestration', 'privacy-and-emotional-safety', 'pilot-boundary',
] as const;

function exactStrings(value: unknown, expected: readonly string[]): boolean {
  return Array.isArray(value)
    && value.length === expected.length
    && [...value].sort().every((entry, index) => entry === [...expected].sort()[index]);
}

export function parseV2Candidate(input: unknown):
  | Readonly<{ ok: true; value: M06Candidate }>
  | Readonly<{ ok: false; issues: readonly string[] }> {
  if (input === null || typeof input !== 'object' || Array.isArray(input)) {
    return { ok: false, issues: ['$ must be an object'] };
  }
  const value = input as Record<string, unknown>;
  const keys = Object.keys(value).sort();
  if (keys.length !== candidateKeys.length
    || !keys.every((key, index) => key === [...candidateKeys].sort()[index])) {
    return { ok: false, issues: ['$ must contain exactly the candidate fields'] };
  }
  const constants: Readonly<Record<string, unknown>> = {
    schemaVersion: 2, baseline: 'v2', id: 'V2-G5-M06', version: '0.1.0',
    renderer: 'v2-m06', payloadSchemaVersion: 1, status: 'draft',
    curriculumCoverage: 'unassessed', pilot: 'not-started', publication: 'closed',
    specPath: 'docs/superpowers/specs/2026-09-07-ium-v2-g5-m06-referenzmodul-design.md',
    materialRevision: '0.1.0', minutes: 225,
  };
  const issues = Object.entries(constants)
    .filter(([key, expected]) => value[key] !== expected)
    .map(([key]) => `$.${key} has the wrong value`);
  if (!exactStrings(value.curriculumRecordIds, curriculumIds)) {
    issues.push('$.curriculumRecordIds must contain the seven approved records');
  }
  if (!exactStrings(value.lxfGateIds, lxfGateIds)) {
    issues.push('$.lxfGateIds must contain all twelve approved gates');
  }
  return issues.length === 0
    ? { ok: true, value: value as M06Candidate }
    : { ok: false, issues };
}

async function files(root: string): Promise<string[]> {
  const result: string[] = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) result.push(...await files(path));
    else if (entry.isFile()) result.push(path);
  }
  return result.sort();
}

function inside(rootDir: string, candidate: string): string {
  if (isAbsolute(candidate)) throw new Error(`Absolute path is forbidden: ${candidate}`);
  const target = resolve(rootDir, candidate);
  const rel = relative(resolve(rootDir), target);
  if (rel === '..' || rel.startsWith(`..${sep}`)) throw new Error(`Path escapes root: ${candidate}`);
  return target;
}

function revision(rootDir: string, supplied?: string): string {
  const value = supplied ?? execFileSync('git', ['rev-parse', 'HEAD'], {
    cwd: rootDir,
    encoding: 'utf8',
  }).trim();
  if (!/^[0-9a-f]{40}$/.test(value)) throw new Error('V2 development build needs a full lowercase Git SHA');
  return value;
}

export async function buildV2Registry(options: BuildV2RegistryOptions): Promise<V2ModuleRegistry> {
  const moduleRoot = inside(options.rootDir, 'modules-v2/V2-G5-M06');
  const manifestPath = resolve(moduleRoot, 'module.json');
  const parsed = parseV2Candidate(JSON.parse(await readFile(manifestPath, 'utf8')) as unknown);
  if (!parsed.ok) throw new Error(`Invalid V2 candidate: ${parsed.issues.join('; ')}`);
  const specPath = inside(options.rootDir, parsed.value.specPath);
  await readFile(specPath);
  const content = JSON.parse(await readFile(resolve(moduleRoot, 'content.json'), 'utf8')) as unknown;
  const cases = JSON.parse(await readFile(resolve(moduleRoot, 'cases.json'), 'utf8')) as unknown;
  const buildRevision = revision(options.rootDir, options.buildRevision);
  const sourceFiles = [...await files(moduleRoot), specPath, inside(options.rootDir, 'schemas/v2/module-candidate.schema.json')];
  const hash = createHash('sha256');
  hash.update(`v2-development\0${buildRevision}\0`);
  for (const path of sourceFiles.sort()) {
    hash.update(relative(resolve(options.rootDir), path).split(sep).join('/'));
    hash.update('\0');
    hash.update(await readFile(path));
    hash.update('\0');
  }
  const registry: V2ModuleRegistry = {
    schemaVersion: 2,
    profile: 'v2-development',
    buildRevision,
    releaseId: `ium-v2-${hash.digest('hex').slice(0, 16)}`,
    modules: [{
      ...parsed.value,
      grade: 5,
      title: 'Präzise Abläufe entwickeln und prüfen',
      contextTitle: 'Prüffahrt im Raster',
      centralQuestion: 'Wie entwickle und prüfe ich eine präzise Wiederholung?',
      entryPath: 'modules-v2/V2-G5-M06/materials/start.md',
      countsTowardCoverage: false,
      publishedStatus: null,
      resources: { content, cases },
    }],
  };
  await mkdir(options.outputDir, { recursive: true });
  await writeFile(resolve(options.outputDir, 'module-registry.json'), `${JSON.stringify(registry, null, 2)}\n`);
  await writeFile(resolve(options.outputDir, 'build-info.json'), `${JSON.stringify({
    schemaVersion: 2,
    profile: registry.profile,
    buildRevision,
    releaseId: registry.releaseId,
    moduleCount: 1,
  }, null, 2)}\n`);
  return registry;
}

async function main(): Promise<void> {
  await buildV2Registry({
    rootDir: process.cwd(),
    outputDir: resolve('apps/lernwerk-portal/src/generated'),
    buildRevision: process.env.IUM_BUILD_REVISION,
  });
}

if (process.argv[1]?.endsWith('build-v2-module-registry.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
