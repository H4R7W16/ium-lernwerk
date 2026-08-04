import { spawnSync } from 'node:child_process';

export type GateBVerificationStep = Readonly<{
  label: string;
  command: string;
  args: readonly string[];
  environment?: Readonly<Record<string, string>>;
}>;

type SpawnResult = Readonly<{
  status: number | null;
  error?: Error;
}>;

type Spawn = (
  command: string,
  args: readonly string[],
  options: Readonly<Record<string, unknown>>,
) => SpawnResult;

export function createGateBVerificationSteps(options: {
  npmCli: string;
  node: string;
  python: string;
  buildRevision: string;
  previewId: string;
}): readonly GateBVerificationStep[] {
  const npmRun = (script: string): GateBVerificationStep => ({
    label: script,
    command: options.node,
    args: [options.npmCli, 'run', script],
  });
  const pythonValidation = (command: 'protocol' | 'synthetic'): GateBVerificationStep => ({
    label: `validate_ium5_gate_b ${command}`,
    command: options.python,
    args: ['-B', 'scripts/validate_ium5_gate_b.py', command],
  });
  return [
    npmRun('contracts:check'),
    npmRun('typecheck'),
    npmRun('check:astro'),
    npmRun('test:platform'),
    pythonValidation('protocol'),
    pythonValidation('synthetic'),
    {
      ...npmRun('build:gate-b-preview'),
      environment: {
        IUM_BUILD_REVISION: options.buildRevision,
        IUM_PREVIEW_ID: options.previewId,
      },
    },
    npmRun('quality:build'),
  ];
}

export function runGateBVerification(
  steps: readonly GateBVerificationStep[],
  spawn: Spawn = spawnSync as Spawn,
): number {
  for (const [index, step] of steps.entries()) {
    console.log(`\n[IUM5 Gate B ${index + 1}/${steps.length}] ${step.label}`);
    const environment = { ...process.env };
    delete environment.IUM_BUILD_REVISION;
    delete environment.IUM_PREVIEW_ID;
    Object.assign(environment, step.environment ?? {});
    const result = spawn(step.command, step.args, {
      stdio: 'inherit',
      shell: false,
      env: environment,
    });
    if (result.error) {
      console.error(`Gate-B-Verifikation abgebrochen: ${step.label}: ${result.error.message}`);
      return 1;
    }
    if (result.status !== 0) {
      const status = result.status ?? 1;
      console.error(`Gate-B-Verifikation abgebrochen: ${step.label} (Exit ${status})`);
      return status;
    }
  }
  console.log(`\nIUM5-Gate-B-Verifikation vollständig: ${steps.length}/${steps.length} Schritte erfolgreich.`);
  return 0;
}

function main(): void {
  const npmCli = process.env.npm_execpath;
  if (!npmCli) {
    console.error('Gate-B-Verifikation abgebrochen: npm_execpath fehlt. Bitte über npm run verify:ium5:gate-b starten.');
    process.exitCode = 1;
    return;
  }
  const steps = createGateBVerificationSteps({
    npmCli,
    node: process.execPath,
    python: process.platform === 'win32' ? 'python.exe' : 'python',
    buildRevision: process.env.IUM_BUILD_REVISION ?? '1'.repeat(40),
    previewId: process.env.IUM_PREVIEW_ID ?? 'ium5-gate-b-verification-0001',
  });
  process.exitCode = runGateBVerification(steps);
}

if (process.argv[1]?.endsWith('verify-ium5-gate-b.ts')) {
  main();
}
