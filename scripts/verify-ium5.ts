import { spawnSync } from 'node:child_process';

type VerificationStep = Readonly<{
  label: string;
  command: string;
  args: readonly string[];
}>;

const python = process.platform === 'win32' ? 'python.exe' : 'python';
const npmCli = process.env.npm_execpath;

if (!npmCli) {
  console.error('Verifikation abgebrochen: npm_execpath fehlt. Bitte über npm run verify:ium5 starten.');
  process.exit(1);
}

const npmRun = (script: string): VerificationStep => ({
  label: script,
  command: process.execPath,
  args: [npmCli, 'run', script],
});

const pythonScript = (
  script: string,
  ...args: readonly string[]
): VerificationStep => ({
  label: `${script.replace(/^scripts\//, '').replace(/\.py$/, '')}${args.length ? ` ${args.join(' ')}` : ''}`,
  command: python,
  args: ['-B', script, ...args],
});

const steps: readonly VerificationStep[] = [
  npmRun('contracts:check'),
  npmRun('boundaries:check'),
  npmRun('typecheck'),
  npmRun('check:astro'),
  npmRun('test:platform'),
  npmRun('build'),
  npmRun('build:fixture'),
  npmRun('build:fixture:subpath'),
  npmRun('quality:build'),
  npmRun('quality:licenses'),
  npmRun('test:browser'),
  npmRun('test:offline'),
  npmRun('test:accessibility'),
  npmRun('test:ium5:browser'),
  npmRun('test:ium5:state'),
  npmRun('test:ium5:offline'),
  npmRun('test:ium5:accessibility'),
  npmRun('test:python'),
  pythonScript('scripts/build_ium11_cockpit.py', '--check'),
  pythonScript('scripts/build_ium11_publication_contract.py', '--check'),
  pythonScript('scripts/validate_ium11.py'),
  pythonScript('scripts/validate_ium10.py'),
  pythonScript('scripts/validate_ium09.py'),
  pythonScript('scripts/validate_phase0.py'),
];

for (const [index, step] of steps.entries()) {
  console.log(`\n[IUM5 ${index + 1}/${steps.length}] ${step.label}`);
  const result = spawnSync(step.command, step.args, {
    stdio: 'inherit',
    shell: false,
  });

  if (result.error) {
    console.error(`Verifikation abgebrochen: ${step.label}: ${result.error.message}`);
    process.exit(1);
  }
  if (result.status !== 0) {
    console.error(`Verifikation abgebrochen: ${step.label} (Exit ${result.status ?? 1})`);
    process.exit(result.status ?? 1);
  }
}

console.log(`\nIUM5-Verifikation vollständig: ${steps.length}/${steps.length} Schritte erfolgreich.`);
