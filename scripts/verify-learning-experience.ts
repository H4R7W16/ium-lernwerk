import { readdir, readFile } from 'node:fs/promises';
import { relative, resolve, sep } from 'node:path';
import { createInitialPayload } from '../packages/ium-5-core-05/src/index.js';
import { checkWorkspaceBoundaries } from './check-workspace-boundaries.js';
import { validateExperienceValue } from './validate-experience-content.js';

export interface ExperienceVerificationReport {
  readonly ok: boolean;
  readonly checks: readonly Readonly<{
    id: string;
    ok: boolean;
    detail: string;
  }>[];
}

type Check = ExperienceVerificationReport['checks'][number];

const requiredComponents = [
  'ExperienceShell',
  'StartBoard',
  'ResumePrompt',
  'JourneyMap',
  'FocusStage',
  'ActionEdge',
  'PredictionForm',
  'SemanticModelView',
  'EvidenceView',
  'EvidenceFeedback',
  'RevisionCompare',
  'EvidenceCardComposer',
  'TransferPrompt',
  'ReentryRecall',
  'SupportDisclosure',
  'RecoveryPanel',
  'ResilienceNotice',
  'TeacherCheckpoint',
  'RoleExchange',
  'SharedHold',
] as const;

const referenceTests = [
  'tests/browser/ium5-start-resume.spec.ts',
  'tests/browser/ium5-evidence-revision.spec.ts',
  'tests/browser/ium5-transfer-reentry.spec.ts',
] as const;

async function exists(path: string): Promise<boolean> {
  try {
    await readFile(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') return false;
    throw error;
  }
}

async function filesBelow(directory: string): Promise<string[]> {
  let entries;
  try {
    entries = await readdir(directory, { withFileTypes: true });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') return [];
    throw error;
  }
  const paths: string[] = [];
  for (const entry of entries) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) paths.push(...await filesBelow(path));
    else if (entry.isFile()) paths.push(path);
  }
  return paths;
}

function channel(value: number): number {
  const normalized = value / 255;
  return normalized <= 0.04045
    ? normalized / 12.92
    : ((normalized + 0.055) / 1.055) ** 2.4;
}

function luminance(hex: string): number {
  const value = hex.replace('#', '');
  const channels = [0, 2, 4].map((offset) => channel(Number.parseInt(value.slice(offset, offset + 2), 16)));
  return (0.2126 * channels[0]!) + (0.7152 * channels[1]!) + (0.0722 * channels[2]!);
}

function contrast(left: string, right: string): number {
  const [lighter, darker] = [luminance(left), luminance(right)].sort((a, b) => b - a) as [number, number];
  return (lighter + 0.05) / (darker + 0.05);
}

function keysBelow(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(keysBelow);
  if (value === null || typeof value !== 'object') return [];
  return Object.entries(value as Record<string, unknown>)
    .flatMap(([key, nested]) => [key, ...keysBelow(nested)]);
}

function display(rootDir: string, paths: readonly string[]): string {
  return paths.map((path) => relative(rootDir, path).split(sep).join('/')).join(', ');
}

export async function verifyLearningExperience(rootDir: string): Promise<ExperienceVerificationReport> {
  const root = resolve(rootDir);
  const checks: Check[] = [];
  const add = async (id: string, run: () => Promise<string>): Promise<void> => {
    try {
      checks.push({ id, ok: true, detail: await run() });
    } catch (error) {
      checks.push({ id, ok: false, detail: error instanceof Error ? error.message : String(error) });
    }
  };

  await add('content-contracts', async () => {
    const moduleRoot = resolve(root, 'modules');
    const moduleEntries = await readdir(moduleRoot, { withFileTypes: true });
    const experiencePaths = moduleEntries
      .filter((entry) => entry.isDirectory())
      .map((entry) => ({
        moduleId: entry.name,
        path: resolve(moduleRoot, entry.name, 'lernumgebung', 'experience.json'),
      }))
      .filter(({ path }) => path.endsWith('experience.json') && path);
    const present = [];
    for (const candidate of experiencePaths) {
      if (!(await exists(candidate.path))) continue;
      const value = JSON.parse(await readFile(candidate.path, 'utf8')) as unknown;
      const result = validateExperienceValue(value, candidate.moduleId);
      if (!result.ok) {
        throw new Error(`${candidate.moduleId}: ${result.errors.map((entry) => `${entry.path} ${entry.message}`).join('; ')}`);
      }
      present.push(candidate.path);
    }
    if (present.length === 0) throw new Error('No production experience.json found.');
    return `${present.length} production experience contract(s) valid: ${display(root, present)}`;
  });

  await add('component-contracts', async () => {
    const componentRoot = resolve(root, 'packages/learning-experience/src/components');
    const resolvedMissing: string[] = [];
    for (const name of requiredComponents) {
      if (!(await exists(resolve(componentRoot, `${name}.astro`)))) resolvedMissing.push(name);
    }
    if (resolvedMissing.length > 0) {
      throw new Error(`Missing component contracts: ${resolvedMissing.join(', ')}`);
    }
    return `${requiredComponents.length} semantic component contracts present.`;
  });

  await add('semantic-contrast', async () => {
    const css = await readFile(resolve(root, 'packages/learning-experience/src/styles/tokens.css'), 'utf8');
    const tokens = new Map([...css.matchAll(/--(lx-color-[a-z-]+):\s*(#[0-9a-f]{6})/gi)]
      .map((match) => [match[1]!, match[2]!.toLowerCase()] as const));
    const pairs = [
      ['ink', 'canvas', 7],
      ['ink', 'surface', 7],
      ['action', '#ffffff', 4.5],
      ['info-text', 'info-surface', 4.5],
      ['confirmed-text', 'confirmed-surface', 4.5],
      ['warning-text', 'warning-surface', 4.5],
      ['danger-text', 'danger-surface', 4.5],
      ['focus', '#ffffff', 3],
      ['focus', 'ink', 3],
    ] as const;
    const failures: string[] = [];
    for (const [foregroundName, backgroundName, minimum] of pairs) {
      const foreground = foregroundName.startsWith('#') ? foregroundName : tokens.get(`lx-color-${foregroundName}`);
      const background = backgroundName.startsWith('#') ? backgroundName : tokens.get(`lx-color-${backgroundName}`);
      if (!foreground || !background || contrast(foreground, background) < minimum) {
        failures.push(`${foregroundName}/${backgroundName} < ${minimum}:1`);
      }
    }
    if (failures.length > 0) throw new Error(failures.join('; '));
    return `${pairs.length} semantic contrast pairs meet their thresholds.`;
  });

  await add('directed-boundaries', async () => {
    const report = await checkWorkspaceBoundaries({ rootDir: root });
    if (report.violations.length > 0) {
      throw new Error(report.violations.map((entry) => `${entry.code}:${entry.path}`).join(', '));
    }
    return `${report.workspaces.length} workspace boundaries directed and cycle-free.`;
  });

  await add('local-assets-only', async () => {
    const files = (await filesBelow(resolve(root, 'packages/learning-experience/src')))
      .filter((path) => /\.(?:astro|css|ts)$/.test(path));
    const violations: string[] = [];
    for (const path of files) {
      const source = await readFile(path, 'utf8');
      if (/https?:\/\/|(?:src|href)\s*=\s*["']\/\//i.test(source)) violations.push(path);
    }
    if (violations.length > 0) throw new Error(`External assets: ${display(root, violations)}`);
    return `${files.length} experience source files use local assets and system fonts only.`;
  });

  await add('data-minimization', async () => {
    const forbidden = /^(?:analytics|telemetry|attemptCount|elapsedMs|clicks|hintUsage|playbackSpeed|userId|learnerName|studentName)$/i;
    const payloadKeys = keysBelow(createInitialPayload());
    const contentPaths = (await filesBelow(resolve(root, 'modules')))
      .filter((path) => path.endsWith(`${sep}lernumgebung${sep}experience.json`));
    const contentKeys: string[] = [];
    for (const path of contentPaths) {
      contentKeys.push(...keysBelow(JSON.parse(await readFile(path, 'utf8')) as unknown));
    }
    const violations = [...new Set([...payloadKeys, ...contentKeys].filter((key) => forbidden.test(key)))];
    if (violations.length > 0) throw new Error(`Forbidden data keys: ${violations.join(', ')}`);
    return `${payloadKeys.length} payload/content keys inspected without personal or interaction metrics.`;
  });

  await add('reference-situations', async () => {
    const missing: string[] = [];
    for (const path of referenceTests) if (!(await exists(resolve(root, path)))) missing.push(path);
    if (missing.length > 0) throw new Error(`Missing Playwright evidence: ${missing.join(', ')}`);
    return 'Three reference situations have dedicated Playwright specifications.';
  });

  await add('portability-boundaries', async () => {
    const genericFiles = (await filesBelow(resolve(root, 'packages/learning-experience/src')))
      .filter((path) => /\.(?:astro|ts|css)$/.test(path));
    const generic = (await Promise.all(genericFiles.map((path) => readFile(path, 'utf8')))).join('\n');
    const coreFiles = (await filesBelow(resolve(root, 'packages/ium-5-core-05/src')))
      .filter((path) => path.endsWith('.ts'));
    const core = (await Promise.all(coreFiles.map((path) => readFile(path, 'utf8')))).join('\n');
    const fixture = await readFile(resolve(root, 'apps/lernwerk-portal/src/pages/fixtures/learning-experience.astro'), 'utf8');
    if (/IUM-5-CORE-05|ue1-|worked-sequence|error-repeat-count|cmd-[0-9]/i.test(generic)) {
      throw new Error('Generic package contains IUM5 phase, command or scenario identity.');
    }
    if (/@ium\/learning-experience|\.astro["']|\b(?:document|window|HTMLElement)\b/.test(core)) {
      throw new Error('IUM5 core imports experience/Astro or accesses the DOM.');
    }
    for (const component of ['StartBoard', 'FocusStage', 'ActionEdge', 'EvidenceFeedback', 'RecoveryPanel']) {
      if (!fixture.includes(component)) throw new Error(`Non-IUM5 fixture does not render ${component}.`);
    }
    return 'Generic package, framework-free IUM5 core and non-IUM5 fixture remain separated.';
  });

  await add('documentation-contract', async () => {
    const documentation = [
      'docs/quality/ium5-acceptance-matrix.md',
      'docs/architecture/systemgrenzen.md',
      'docs/architecture/lokale-datenhaltung-und-resilienz.md',
      'README.md',
    ];
    let combined = '';
    const missing: string[] = [];
    for (const path of documentation) {
      const absolute = resolve(root, path);
      if (!(await exists(absolute))) missing.push(path);
      else combined += `\n${await readFile(absolute, 'utf8')}`;
    }
    if (missing.length > 0) throw new Error(`Missing documentation: ${missing.join(', ')}`);
    const required = [
      /ExperienceContentV1/,
      /stateSchemaVersion\s*1[^\n]{0,120}(?:→|nach|auf)\s*2/i,
      /evidenceCard:\s*null/,
      /Nicht-Generalisierungen/i,
      /Raster/,
      /Befehlskatalog/,
      /Laufspursemantik/,
      /Szenario-IDs/,
      /Checkpoint-Platzierung/,
    ];
    const missingMarkers = required.filter((pattern) => !pattern.test(combined)).map(String);
    if (missingMarkers.length > 0) throw new Error(`Missing documentation markers: ${missingMarkers.join(', ')}`);
    return `${documentation.length} documents record contract version, migration and non-generalizations.`;
  });

  return { ok: checks.every((check) => check.ok), checks };
}

async function main(): Promise<void> {
  const report = await verifyLearningExperience(process.cwd());
  for (const check of report.checks) {
    console.log(`${check.ok ? 'PASS' : 'FAIL'} ${check.id}: ${check.detail}`);
  }
  if (!report.ok) {
    const failed = report.checks.filter((check) => !check.ok).map((check) => check.id);
    console.error(`Experience-Verifikation: FAIL (${failed.join(', ')})`);
    process.exitCode = 1;
    return;
  }
  console.log(`Experience-Verifikation: PASS (${report.checks.length}/${report.checks.length})`);
}

if (process.argv[1]?.replaceAll('\\', '/').endsWith('/verify-learning-experience.ts')) {
  main().catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}
