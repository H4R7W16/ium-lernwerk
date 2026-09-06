/** Synthetischer FU-TECH-Befundlauf, keine Produkt-Abnahmetests.
 * Aufruf im Repo: node --import tsx roadmap/v2/follow-ups/technical/probe.mts
 * Schreibt keine Dateien; verwendet ausschließlich MemoryStateRepository.
 * true bei findingObserved bedeutet: der dokumentierte Mangel besteht.
 */
import { createModuleRuntime } from '../../../../packages/module-runtime/src/index.ts';
import { MemoryStateRepository } from '../../../../packages/local-state/src/index.ts';
import { serializeState } from '../../../../packages/export-import/src/index.ts';
import { validateLearningState } from '../../../../packages/module-contract/src/index.ts';

const seed = (overrides = {}) => ({
  format: 'ium-learning-state' as const, formatVersion: 1 as const,
  moduleId: 'TEST-TECH-AUDIT', moduleVersion: '1.0.0', stateSchemaVersion: 1,
  workspaceId: '123e4567-e89b-42d3-a456-426614174000',
  savedAt: '2026-09-06T12:00:00.000Z', payload: { text: 'synthetisch' }, ...overrides,
});
const runtime = (repository: MemoryStateRepository, targetStateSchemaVersion = 1) => createModuleRuntime({
  moduleId: 'TEST-TECH-AUDIT', moduleVersion: '2.0.0',
  targetStateSchemaVersion, repository, migrations: [],
  clock: { now: () => new Date('2026-09-06T12:01:00.000Z') },
  createWorkspaceId: () => '223e4567-e89b-42d3-a456-426614174000',
  exportPort: { download: async () => true, copyText: async () => true },
});
const findings = [];

{
  const repo = new MemoryStateRepository();
  const old = seed();
  await repo.save(old);
  const app = runtime(repo);
  const started = await app.start();
  const imported = app.previewImport(serializeState(old));
  findings.push({ id: 'TECH-F01', case: 'local-version-vs-import',
    findingObserved: started.ok && !imported.ok,
    localStartAccepted: started.ok, importedVersionRejected: !imported.ok });
}
{
  const repo = new MemoryStateRepository();
  const invalid = seed({ moduleVersion: '2.0.0', savedAt: 'kein Datum' });
  await repo.save(invalid);
  const app = runtime(repo);
  const started = await app.start();
  const valid = validateLearningState(invalid);
  findings.push({ id: 'TECH-F01', case: 'invalid-local-envelope',
    findingObserved: !valid.ok && started.ok,
    schemaRejects: !valid.ok, localStartAccepted: started.ok });
}
{
  const repo = new MemoryStateRepository();
  const old = seed({ moduleVersion: '2.0.0' });
  await repo.save(old);
  const app = runtime(repo, 2);
  const started = await app.start();
  const exported = await app.exportState();
  const preserved = JSON.stringify(await repo.load(old.moduleId)) === JSON.stringify(old);
  findings.push({ id: 'TECH-F02', case: 'failed-migration-original-export',
    findingObserved: !started.ok && preserved && !exported.ok,
    originalPreserved: preserved, runtimeExportAvailable: exported.ok });
}
{
  const repo = new MemoryStateRepository();
  const app = runtime(repo);
  await app.start();
  const good = app.previewImport(serializeState(seed({ moduleVersion: '2.0.0', payload: { text: 'alter Preview' } })));
  const bad = app.previewImport(new TextEncoder().encode('{'));
  const confirmed = await app.confirmImport();
  findings.push({ id: 'TECH-F03', case: 'stale-pending-import-runtime-api',
    findingObserved: good.ok && !bad.ok && confirmed.ok,
    stalePreviewConfirmable: confirmed.ok,
    limitation: 'Der IUM5-Controller sperrt diesen UI-Pfad mit pendingPayload; generische Runtime-API bleibt offen.' });
}
{
  const repo = new MemoryStateRepository();
  const first = runtime(repo), second = runtime(repo);
  await first.start(); await second.start();
  first.updatePayload({ text: 'neuer Stand A' }); await first.flush();
  second.updatePayload({ text: 'veralteter Stand B' }); const saved = await second.flush();
  const last = await repo.load('TEST-TECH-AUDIT');
  findings.push({ id: 'TECH-F04', case: 'shared-repository-stale-writer',
    findingObserved: saved.ok && last?.payload.text === 'veralteter Stand B',
    limitation: 'Zwei Runtime-Instanzen an einem Speicherport; kein realer Mehrtab-/Gerätenachweis.' });
}
{
  const repo = new MemoryStateRepository();
  const app = runtime(repo); await app.start();
  app.updatePayload({ text: 'noch flüchtig' }); const flushed = await app.flush();
  const afterReload = new MemoryStateRepository();
  const missing = await afterReload.load('TEST-TECH-AUDIT') === null;
  findings.push({ id: 'TECH-F06', case: 'volatile-flush-is-not-reload-safe',
    findingObserved: flushed.ok && missing,
    flushSuccessful: flushed.ok, newSessionLosesState: missing,
    limitation: 'Reload wird durch einen frischen Memory-Adapter modelliert; SW-Kopplung zusätzlich per Code geprüft.' });
}
console.log(JSON.stringify({ schemaVersion: 1, taskId: 'IUM-V2-FU-TECH',
  evidenceKind: 'synthetic-diagnostic', productApproval: false, findings }, null, 2));
if (findings.some((finding) => !finding.findingObserved)) process.exitCode = 1;
