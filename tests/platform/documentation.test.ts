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
    expect(source).not.toMatch(/\b(deploy|release|secret|student|learner-data)\b/i);
  });
});
