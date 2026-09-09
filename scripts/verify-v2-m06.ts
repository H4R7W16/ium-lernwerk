import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { buildPortalToDirectory } from './build-portal.js';

export type VerificationStep = Readonly<{
  id: string;
  label: string;
  command: string;
  args: readonly string[];
}>;

export type VerificationResult = Readonly<{
  id: string;
  label: string;
  command: readonly string[];
  exitCode: number;
  startedAt: string;
  finishedAt: string;
}>;

type RunIdentity = Readonly<{
  schemaVersion: 1;
  runId: string;
  revision: string;
  node: string;
  npm: string;
  startedAt: string;
}>;

async function runBrowser(spec?: string): Promise<number> {
  const rootDir = process.cwd();
  const appRoot = resolve(rootDir, 'apps/lernwerk-portal');
  const outputDir = resolve(appRoot, 'dist');
  await buildPortalToDirectory({
    profile: 'v2-development',
    publicationMode: 'development',
    base: '/',
    rootDir,
    outputDir,
    buildRevision: process.env.IUM_BUILD_REVISION,
  });
  process.env.IUM_BUILD_PROFILE = 'v2-development';
  process.env.IUM_PUBLICATION_MODE = 'development';
  process.env.IUM_BASE_PATH = '/';
  process.env.IUM_OUTPUT_DIR = outputDir;
  process.env.ASTRO_TELEMETRY_DISABLED = '1';
  const { preview } = await import('astro');
  const server = await preview({
    root: appRoot,
    server: { host: '127.0.0.1', port: 4324 },
  });
  if (server.port !== 4324) {
    await server.stop();
    throw new Error(`V2 M06 preview port 4324 is occupied; refused fallback port ${server.port}`);
  }
  const args = ['exec', '--', 'playwright', 'test'];
  if (spec) args.push(spec);
  args.push('--config', 'playwright.v2.config.mts');
  try {
    return await new Promise<number>((accept, reject) => {
      const child = spawn(process.execPath, [npmCli!, ...args], {
        cwd: rootDir,
        env: process.env,
        stdio: 'inherit',
        shell: false,
      });
      child.once('error', reject);
      child.once('exit', (code) => accept(code ?? 1));
    });
  } finally {
    await server.stop();
  }
}

async function runRuntimeBrowser(spec: string): Promise<number> {
  const rootDir = process.cwd();
  const appRoot = resolve(rootDir, 'apps/lernwerk-portal');
  const outputDir = resolve(appRoot, 'dist');
  await buildPortalToDirectory({
    profile: 'fixture',
    publicationMode: 'device-fixture',
    base: '/',
    rootDir,
    outputDir,
    buildRevision: process.env.IUM_BUILD_REVISION,
  });
  process.env.IUM_BUILD_PROFILE = 'fixture';
  process.env.IUM_PUBLICATION_MODE = 'device-fixture';
  process.env.IUM_BASE_PATH = '/';
  process.env.IUM_OUTPUT_DIR = outputDir;
  process.env.IUM_MANAGED_PREVIEW = '1';
  process.env.ASTRO_TELEMETRY_DISABLED = '1';
  const { preview } = await import('astro');
  const server = await preview({
    root: appRoot,
    server: { host: '127.0.0.1', port: 4321 },
  });
  if (server.port !== 4321) {
    await server.stop();
    throw new Error(`V2 runtime preview port 4321 is occupied; refused fallback port ${server.port}`);
  }
  try {
    return await new Promise<number>((accept, reject) => {
      const child = spawn(process.execPath, [npmCli!, 'exec', '--', 'playwright', 'test', spec,
        '--config', 'playwright.runtime.config.mts'], {
        cwd: rootDir,
        env: process.env,
        stdio: 'inherit',
        shell: false,
      });
      child.once('error', reject);
      child.once('exit', (code) => accept(code ?? 1));
    });
  } finally {
    await server.stop();
  }
}

async function runPortalBrowser(values: readonly string[]): Promise<number> {
  const [profile, publicationMode, portValue, config, spec, project] = values;
  if (!['fixture', 'production'].includes(profile ?? '')
    || !['device-fixture', 'development'].includes(publicationMode ?? '')
    || !config || !spec) throw new Error('Invalid managed portal browser arguments');
  const port = Number.parseInt(portValue ?? '', 10);
  if (!Number.isInteger(port)) throw new Error(`Invalid managed portal port: ${portValue}`);
  const rootDir = process.cwd();
  const appRoot = resolve(rootDir, 'apps/lernwerk-portal');
  const outputDir = resolve(appRoot, 'dist');
  await buildPortalToDirectory({
    profile: profile as 'fixture' | 'production',
    publicationMode: publicationMode as 'device-fixture' | 'development',
    base: '/', rootDir, outputDir, buildRevision: process.env.IUM_BUILD_REVISION,
  });
  process.env.IUM_BUILD_PROFILE = profile;
  process.env.IUM_PUBLICATION_MODE = publicationMode;
  process.env.IUM_BASE_PATH = '/';
  process.env.IUM_OUTPUT_DIR = outputDir;
  process.env.IUM_MANAGED_PREVIEW = '1';
  process.env.ASTRO_TELEMETRY_DISABLED = '1';
  const { preview } = await import('astro');
  const server = await preview({ root: appRoot, server: { host: '127.0.0.1', port } });
  if (server.port !== port) {
    await server.stop();
    throw new Error(`Managed preview port ${port} is occupied; refused fallback port ${server.port}`);
  }
  const args = [npmCli!, 'exec', '--', 'playwright', 'test', spec, '--config', config];
  if (project) args.push(`--project=${project}`);
  try {
    return await new Promise<number>((accept, reject) => {
      const child = spawn(process.execPath, args, {
        cwd: rootDir, env: process.env, stdio: 'inherit', shell: false,
      });
      child.once('error', reject);
      child.once('exit', (code) => accept(code ?? 1));
    });
  } finally {
    await server.stop();
  }
}

const browserArgument = process.argv.indexOf('--browser');
const browserMode = browserArgument >= 0;
const browserSpec = browserMode && process.argv[browserArgument + 1] !== 'all'
  ? process.argv[browserArgument + 1]
  : undefined;
const runtimeBrowserArgument = process.argv.indexOf('--runtime-browser');
const runtimeBrowserMode = runtimeBrowserArgument >= 0;
const runtimeBrowserSpec = runtimeBrowserMode ? process.argv[runtimeBrowserArgument + 1] : undefined;
const portalBrowserArgument = process.argv.indexOf('--portal-browser');
const portalBrowserMode = portalBrowserArgument >= 0;

const npmCli = process.env.npm_execpath;
if (!npmCli) {
  console.error('Verifikation abgebrochen: npm_execpath fehlt. Bitte über ein npm-Skript starten.');
  process.exit(1);
}

if (browserMode) {
  void runBrowser(browserSpec).then((exitCode) => {
    process.exitCode = exitCode;
  }).catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
} else if (runtimeBrowserMode && runtimeBrowserSpec) {
  void runRuntimeBrowser(runtimeBrowserSpec).then((exitCode) => {
    process.exitCode = exitCode;
  }).catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
} else if (portalBrowserMode) {
  void runPortalBrowser(process.argv.slice(portalBrowserArgument + 1)).then((exitCode) => {
    process.exitCode = exitCode;
  }).catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  });
}

const python = process.platform === 'win32' ? 'python.exe' : 'python';
const reports = resolve(process.cwd(), 'reports/v2-m06');
mkdirSync(reports, { recursive: true });

function readCommand(command: string, args: readonly string[]): string {
  const result = spawnSync(command, [...args], {
    cwd: process.cwd(), encoding: 'utf8', shell: false,
  });
  return result.status === 0 ? result.stdout.trim() : 'unavailable';
}

const runIdentity: RunIdentity = {
  schemaVersion: 1,
  runId: process.env.IUM_VERIFICATION_RUN_ID ?? `local-${process.pid}`,
  revision: process.env.IUM_BUILD_REVISION ?? readCommand('git', ['rev-parse', 'HEAD']),
  node: process.version,
  npm: readCommand(process.execPath, [npmCli, '--version']),
  startedAt: new Date().toISOString(),
};

const npmRun = (id: string, script: string): VerificationStep => ({
  id,
  label: script,
  command: process.execPath,
  args: [npmCli!, 'run', script],
});

const direct = (
  id: string,
  label: string,
  command: string,
  ...args: readonly string[]
): VerificationStep => ({ id, label, command, args });

export function runCheck(step: VerificationStep): VerificationResult {
  const startedAt = new Date().toISOString();
  const result = spawnSync(step.command, [...step.args], {
    cwd: process.cwd(),
    stdio: 'inherit',
    shell: false,
  });
  const exitCode = result.status ?? 1;
  const record: VerificationResult = {
    id: step.id,
    label: step.label,
    command: [step.command, ...step.args],
    exitCode,
    startedAt,
    finishedAt: new Date().toISOString(),
  };
  writeFileSync(resolve(reports, `${step.id}.json`), `${JSON.stringify(record, null, 2)}\n`);
  if (result.error) console.error(result.error.message);
  return record;
}

const steps: readonly VerificationStep[] = [
  npmRun('contracts', 'contracts:check'),
  npmRun('boundaries', 'boundaries:check'),
  npmRun('typecheck', 'typecheck'),
  npmRun('astro', 'check:astro'),
  npmRun('platform', 'test:platform'),
  npmRun('python', 'test:python'),
  npmRun('v2-historical-activation', 'verify:v2:activation:historical'),
  npmRun('v2-development', 'verify:v2:implementation'),
  npmRun('v2-registry', 'registry:v2'),
  direct('m06-materials', 'M06 material contract', process.execPath, npmCli!, 'exec', '--', 'tsx', 'scripts/check-v2-m06-materials.ts'),
  npmRun('build-subpath', 'build:v2:subpath'),
  npmRun('build-root', 'build:v2'),
  npmRun('browser-workbench', 'test:v2:m06:workbench'),
  npmRun('browser-state', 'test:v2:m06:state'),
  npmRun('browser-accessibility', 'test:v2:m06:accessibility'),
  npmRun('browser-offline', 'test:v2:m06:offline'),
  direct('browser-runtime', 'V2 profile, quota, CAS and recovery paths', process.execPath, npmCli!,
    'exec', '--', 'tsx', 'scripts/verify-v2-m06.ts', '--runtime-browser', 'tests/browser/v2-storage.spec.ts'),
  direct('browser-update', 'V2 multi-client update paths', process.execPath, npmCli!,
    'exec', '--', 'tsx', 'scripts/verify-v2-m06.ts', '--runtime-browser', 'tests/browser/v2-update.spec.ts'),
  npmRun('licenses', 'quality:licenses'),
  npmRun('v1-integration', 'verify:ium5'),
];

if (!browserMode && !runtimeBrowserMode && !portalBrowserMode) {
  const results: VerificationResult[] = [];
  for (const [index, step] of steps.entries()) {
    console.log(`\n[V2 M06 ${index + 1}/${steps.length}] ${step.label}`);
    results.push(runCheck(step));
  }

  const failed = results.filter((result) => result.exitCode !== 0);
  const summary = {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    status: failed.length === 0 ? 'passed' : 'failed',
    counts: { total: results.length, passed: results.length - failed.length, failed: failed.length },
    failedStepIds: failed.map((result) => result.id),
    run: runIdentity,
    results,
    limits: {
      scope: 'synthetic-development-candidate',
      realDevices: 'not-run',
      usage: 'not-started',
      pilot: 'not-started',
      curriculumCoverage: 'unassessed',
      publication: 'closed',
    },
  };
  writeFileSync(resolve(reports, 'run-identity.json'), `${JSON.stringify(runIdentity, null, 2)}\n`);
  writeFileSync(resolve(reports, 'summary.json'), `${JSON.stringify(summary, null, 2)}\n`);

  if (failed.length > 0) {
    console.error(`\nV2-M06-Verifikation nicht vollständig grün: ${failed.map((result) => result.id).join(', ')}`);
    process.exitCode = 1;
  } else {
    console.log('\nV2-M06-Verifikation vollständig bestanden.');
  }
}
