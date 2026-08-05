import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { describe, expect, test } from 'vitest';
import {
  adaptResilienceState,
  getSaveMessage,
  type SaveState,
  type TechnicalResilienceFact,
} from '@ium/learning-experience/controllers/resilience-adapter';

test.each([
  ['idle', 'Keine Änderungen ausstehend'],
  ['saving', 'Wird auf diesem Gerät gespeichert'],
  ['saved', 'Auf diesem Gerät gespeichert'],
  ['failed', 'Speichern nicht möglich'],
] as const)('maps save state %s to durable text', (state, label) => {
  expect(getSaveMessage(state as SaveState)).toBe(label);
});

describe('technical resilience mapping', () => {
  test.each([
    [{ type: 'save', state: 'saving', affectedWork: 'Deine Vermutung' }, 'info'],
    [{ type: 'save', state: 'failed', affectedWork: 'Deine Vermutung' }, 'block'],
    [{ type: 'connectivity', state: 'offline', affectedWork: 'Der aktuelle Lernweg' }, 'limit'],
    [{ type: 'storage', state: 'volatile', affectedWork: 'Dein Arbeitsstand' }, 'limit'],
    [{ type: 'update', state: 'available', affectedWork: 'Die aktuelle Sitzung' }, 'limit'],
  ] as const)('maps $type/$state to $1', (fact, severity) => {
    const spec = adaptResilienceState(fact as TechnicalResilienceFact);

    expect(spec.severity).toBe(severity);
    expect(spec.affectedWork).toBe(fact.affectedWork);
    expect(spec.preservedState.length).toBeGreaterThan(0);
    expect(spec.consequence.length).toBeGreaterThan(0);
    expect(spec.primaryAction.length).toBeGreaterThan(0);
    expect(spec.returnTarget.length).toBeGreaterThan(0);
  });

  test('is a pure platform mapping without DOM or IUM5 coupling', async () => {
    const source = await readFile(fileURLToPath(new URL(
      '../../packages/learning-experience/src/controllers/resilience-adapter.ts',
      import.meta.url,
    )), 'utf8');

    expect(source).not.toMatch(/\bdocument\b|\bwindow\b|ium-5-core-05/i);
  });
});

test('keeps correctness language out of semantic live regions', async () => {
  const names = ['SaveIndicator', 'ResilienceNotice'];
  const sources = await Promise.all(names.map((name) => readFile(fileURLToPath(new URL(
    `../../packages/learning-experience/src/components/${name}.astro`,
    import.meta.url,
  )), 'utf8')));

  expect(sources.join('\n')).not.toMatch(/richtig|falsch|korrekt|lösung/i);
});

test('exposes neutral platform facts and keeps their state attributes current', async () => {
  const [storage, connection, update, error, statusController, pwaController] = await Promise.all([
    readFile(fileURLToPath(new URL('../../packages/ui-components/src/components/StorageStatus.astro', import.meta.url)), 'utf8'),
    readFile(fileURLToPath(new URL('../../packages/ui-components/src/components/ConnectionStatus.astro', import.meta.url)), 'utf8'),
    readFile(fileURLToPath(new URL('../../packages/ui-components/src/components/UpdatePrompt.astro', import.meta.url)), 'utf8'),
    readFile(fileURLToPath(new URL('../../packages/ui-components/src/components/ErrorSummary.astro', import.meta.url)), 'utf8'),
    readFile(fileURLToPath(new URL('../../packages/ui-components/src/controllers/status-announcer.ts', import.meta.url)), 'utf8'),
    readFile(fileURLToPath(new URL('../../apps/lernwerk-portal/src/controllers/pwa-registration.ts', import.meta.url)), 'utf8'),
  ]);

  expect(storage).toContain('data-platform-fact="storage"');
  expect(connection).toContain('data-platform-fact="connectivity"');
  expect(update).toContain('data-platform-fact="update"');
  expect(error).toContain('data-platform-fact="error"');
  expect(statusController).toContain("summary.dataset.errorState = 'visible'");
  expect(pwaController).toContain("prompt.dataset.updateState = 'available'");
  expect(pwaController).toContain("prompt.dataset.updateState = 'hidden'");
});
