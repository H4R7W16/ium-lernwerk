import { readFile } from 'node:fs/promises';
import { parseDocument } from 'yaml';
import { describe, expect, test } from 'vitest';

const read = (path: string) => readFile(path, 'utf8');

describe('Phase 1 operations documentation', () => {
  test('links every approved Phase 1 entry point from the root README', async () => {
    const readme = await read('README.md');

    expect(readme).toContain('docs/superpowers/specs/2026-08-03-ium-phase1-plattformfundament-design.md');
    expect(readme).toContain('docs/superpowers/plans/2026-08-03-ium-phase1-plattformfundament-implementation.md');
    expect(readme).toContain('docs/platform/README.md');
    expect(readme).toContain('docs/platform/device-verification.md');
    expect(readme).toContain('npm run verify:phase1');
  });

  test('links the IUM5 working module without overstating its release status', async () => {
    const readme = await read('README.md');

    for (const required of [
      'docs/superpowers/specs/2026-08-03-ium-5-core-05-moduldesign.md',
      'docs/superpowers/plans/2026-08-03-ium-5-core-05-implementation.md',
      'docs/modules/ium-5-core-05.md',
      'npm run verify:ium5',
      'working',
      'nicht für Unterrichtseinsatz',
      'Gate B',
      'device-verified: not-run',
    ]) {
      expect(readme).toContain(required);
    }
  });

  test('distinguishes the Phase 1 empty baseline from the local IUM5 build', async () => {
    const operations = await read('docs/platform/README.md');

    for (const required of [
      'Phase-1-Ausgangsstand',
      'production-empty',
      'IUM-5-CORE-05',
      'working',
      'nicht deployt',
    ]) {
      expect(operations).toContain(required);
    }
  });

  test('documents operation, Local-First boundaries and honest status', async () => {
    const operations = await read('docs/platform/README.md');

    for (const required of [
      'production-empty',
      'fixture',
      'bestätigte Speicherung',
      'flüchtige Sitzung',
      'sensiblen Export',
      'global löschen',
      'ersten Offline-Aufruf',
      'kontrollierte Aktualisierung',
      'Einbettung',
      '/ium-lernwerk/',
      'asset-licenses.json',
      'npm run verify:phase1',
      'implemented',
      'device-verified',
    ]) {
      expect(operations).toContain(required);
    }
    expect(operations).toContain('not-run');
  });

  test('keeps the real-device protocol explicitly not-run and evidence-driven', async () => {
    const protocol = await read('docs/platform/device-verification.md');
    const frontMatter = protocol.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1];

    expect(frontMatter).toBeDefined();
    expect(parseDocument(frontMatter!).get('device-verified')).toBe('not-run');
    for (const field of [
      'Datum',
      'Prüfperson',
      'Gerät',
      'Betriebssystem',
      'Browser-Version',
      'MDM',
      'Web-Clip',
      'Speicherrichtlinie',
      'Filterrichtlinie',
      'VoiceOver',
      'Chromium',
      'Firefox',
      'Online',
      'Offline',
      'Import',
      'Export',
      'Aktualisierung',
      'Ergebnis',
      'Befund',
      'Evidenzpfad',
    ]) {
      expect(protocol).toContain(field);
    }
    expect(protocol).not.toMatch(/- \[[xX]\]/);
  });
});

describe('Phase 1 verification entry points', () => {
  test('exposes one cross-platform fail-fast root command', async () => {
    const packageJson = JSON.parse(await read('package.json')) as {
      scripts: Record<string, string>;
    };
    const verifier = await read('scripts/verify-phase1.ts');

    expect(packageJson.scripts['verify:phase1']).toBe('tsx scripts/verify-phase1.ts');
    expect(verifier).toContain('spawnSync');
    expect(verifier).toContain("stdio: 'inherit'");
    expect(verifier).toContain('contracts:check');
    expect(verifier.indexOf('contracts:check')).toBeLessThan(verifier.indexOf('validate_phase0'));
  });

  test('exposes the fail-fast IUM5 verification chain in the approved order', async () => {
    const packageJson = JSON.parse(await read('package.json')) as {
      scripts: Record<string, string>;
    };
    const verifier = await read('scripts/verify-ium5.ts');

    expect(packageJson.scripts).toMatchObject({
      'test:ium5:browser': 'playwright test tests/browser/ium5-workbench.spec.ts --config playwright.ium5.config.mts',
      'test:ium5:state': 'playwright test tests/browser/ium5-state.spec.ts --config playwright.ium5.config.mts --project=chromium',
      'test:ium5:accessibility': 'playwright test tests/browser/ium5-accessibility.spec.ts --config playwright.ium5.config.mts --project=chromium',
      'test:ium5:offline': 'playwright test tests/browser/ium5-offline.spec.ts --config playwright.ium5.config.mts --project=chromium',
      'verify:ium5': 'tsx scripts/verify-ium5.ts',
    });
    expect(verifier).toContain('spawnSync');
    expect(verifier).toContain("stdio: 'inherit'");
    expect(verifier).toContain('shell: false');

    const orderedCommands = [
      'contracts:check',
      'boundaries:check',
      'typecheck',
      'check:astro',
      'test:platform',
      'build',
      'build:fixture',
      'build:fixture:subpath',
      'quality:build',
      'quality:licenses',
      'test:browser',
      'test:offline',
      'test:accessibility',
      'test:ium5:browser',
      'test:ium5:state',
      'test:ium5:offline',
      'test:ium5:accessibility',
      'test:python',
      'build_ium11_cockpit.py',
      'build_ium11_publication_contract.py',
      'validate_ium11.py',
      'validate_ium10.py',
      'validate_ium09.py',
      'validate_phase0.py',
    ];
    let cursor = -1;
    for (const command of orderedCommands) {
      const next = verifier.indexOf(command, cursor + 1);
      expect(next, `${command} is missing or out of order`).toBeGreaterThan(cursor);
      cursor = next;
    }
    expect(verifier).not.toMatch(/device-verified[^\n]*(?:pass|true|complete)/i);
  });

  test('bootstraps ignored generated contracts before byte comparison', async () => {
    const packageJson = JSON.parse(await read('package.json')) as {
      scripts: Record<string, string>;
    };

    expect(packageJson.scripts['contracts:check']).toBe(
      'npm run contracts:generate && tsx scripts/generate-contract-types.ts --check',
    );
  });

  test('defines the four bounded CI jobs with pinned runtime and approved actions', async () => {
    const source = await read('.github/workflows/ci.yml');
    const document = parseDocument(source);
    expect(document.errors).toEqual([]);
    const workflow = document.toJS() as {
      jobs: Record<string, unknown>;
    };

    expect(Object.keys(workflow.jobs)).toEqual([
      'legacy',
      'contracts-build',
      'browser',
      'offline-quality',
    ]);
    expect(source).toContain('actions/checkout@v5');
    expect(source).toContain('actions/setup-node@v5');
    expect(source).toContain('actions/upload-artifact@v4');
    expect(source).toContain('node-version: 22.20.0');
    expect(source).toContain('cache: npm');
    expect(source).toContain('npm ci');
    expect(source).toContain('playwright install --with-deps');
    for (const command of [
      'npm run check:astro',
      'npm run test:ium5:browser',
      'npm run test:ium5:state',
      'npm run test:ium5:offline',
      'npm run test:ium5:accessibility',
    ]) {
      expect(source).toContain(command);
    }
    expect(source).not.toMatch(/\b(deploy|release|secret|student|learner-data)\b/i);
  });
});
