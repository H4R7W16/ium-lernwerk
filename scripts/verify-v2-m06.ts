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

const browserArgument = process.argv.indexOf('--browser');
const browserMode = browserArgument >= 0;
const browserSpec = browserMode && process.argv[browserArgument + 1] !== 'all'
  ? process.argv[browserArgument + 1]
  : undefined;

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
}

const python = process.platform === 'win32' ? 'python.exe' : 'python';
const reports = resolve(process.cwd(), 'reports/v2-m06');
mkdirSync(reports, { recursive: true });

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
  npmRun('v2-baseline', 'verify:v2'),
  npmRun('v2-development', 'verify:v2:implementation'),
  npmRun('v2-registry', 'registry:v2'),
  direct('m06-materials', 'M06 material contract', process.execPath, npmCli!, 'exec', '--', 'tsx', 'scripts/check-v2-m06-materials.ts'),
  npmRun('build-subpath', 'build:v2:subpath'),
  npmRun('build-root', 'build:v2'),
  npmRun('browser-workbench', 'test:v2:m06:workbench'),
  npmRun('browser-state', 'test:v2:m06:state'),
  npmRun('browser-accessibility', 'test:v2:m06:accessibility'),
  npmRun('browser-offline', 'test:v2:m06:offline'),
  npmRun('licenses', 'quality:licenses'),
  npmRun('v1-integration', 'verify:ium5'),
];

if (!browserMode) {
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
  writeFileSync(resolve(reports, 'summary.json'), `${JSON.stringify(summary, null, 2)}\n`);

  if (failed.length > 0) {
    console.error(`\nV2-M06-Verifikation nicht vollständig grün: ${failed.map((result) => result.id).join(', ')}`);
    process.exitCode = 1;
  } else {
    console.log('\nV2-M06-Verifikation vollständig bestanden.');
  }
}
