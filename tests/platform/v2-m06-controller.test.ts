import { describe, expect, test, vi } from 'vitest';
import {
  createInitialDossier,
  parseDossier,
  type Dossier,
  type Program,
} from '@ium/v2-g5-m06';
import {
  createM06Controller,
  type M06RuntimePort,
} from '../../apps/lernwerk-portal/src/controllers/m06/controller.js';
import { createModuleRuntime } from '@ium/module-runtime';
import { MemoryStateRepository } from '@ium/local-state';
import type { StateRepository } from '@ium/module-contract';

async function realController(mode: 'persistent' | 'volatile-selected' = 'persistent') {
  const backing = new MemoryStateRepository();
  let failWrites = false;
  let pauseWrite: Promise<void> | undefined;
  let exported = '';
  const repository: StateRepository = {
    mode,
    load: (id) => backing.load(id),
    async save(state) {
      if (pauseWrite) await pauseWrite;
      if (failWrites) return { ok: false, error: {
        code: 'STORAGE_WRITE_FAILED', message: 'Speicher voll', action: 'Exportieren',
      } };
      await backing.save(state);
      return { ok: true, mode };
    },
    deleteModule: (id) => backing.deleteModule(id),
    deleteAll: () => backing.deleteAll(),
  };
  const active = createModuleRuntime({
    moduleId: 'V2-G5-M06', moduleVersion: '0.1.0', targetStateSchemaVersion: 1,
    repository, migrations: [], clock: { now: () => new Date('2026-09-09T08:00:00Z') },
    createWorkspaceId: () => '123e4567-e89b-42d3-a456-426614174000',
    statePolicy: { supportedModuleVersions: ['0.1.0'], createInitialPayload: createInitialDossier,
      validatePayload: (payload) => parseDossier(payload).ok },
    exportPort: { download: async (_name, bytes) => {
      exported = new TextDecoder().decode(bytes); return true;
    }, copyText: async () => false },
  });
  const started = await active.start();
  if (!started.ok) throw new Error(started.error.message);
  const port: M06RuntimePort = {
    replacePayload: (dossier) => active.updatePayload(dossier),
    flush: () => active.flush(), previewImport: (bytes) => active.previewImport(bytes),
    confirmImport: async () => {
      const result = await active.confirmImport();
      return result.ok ? { ok: true, payload: result.state.payload } : result;
    },
    cancelImport: () => active.cancelImport(), deleteActive: () => active.deleteActive(),
    exportState: () => active.exportState(), prepareForReload: () => active.prepareForReload(),
    releaseReloadPreparation: () => active.releaseReloadPreparation(),
    approveDiscardForReload: () => active.approveDiscardForReload(),
  };
  return { controller: createM06Controller(createInitialDossier(), port),
    stored: () => backing.load('V2-G5-M06'), exported: () => JSON.parse(exported),
    failWrites: () => { failWrites = true; }, pauseWrites: (pending: Promise<void>) => { pauseWrite = pending; } };
}

describe('M06 current work with the real runtime', () => {
  test('exports the current unsaved code even when local saving fails', async () => {
    const session = await realController();
    session.controller.updateDraftProgram([{ id: 'cmd-1', kind: 'move' }]);
    expect(await session.controller.exportWork()).toBe(true);
    expect(session.exported().payload.p3.draftProgram).toEqual([{ id: 'cmd-1', kind: 'move' }]);
    session.failWrites();
    expect(await session.controller.flush()).toBe(false);
    session.controller.updateDraftProgram([{ id: 'cmd-2', kind: 'turn-right' }]);
    expect(await session.controller.exportWork()).toBe(true);
    expect(session.exported().payload.p3.draftProgram).toEqual([{ id: 'cmd-2', kind: 'turn-right' }]);
    expect(session.controller.saveState().state).not.toBe('saved');
  });

  test('reload readback contains the current draft and freezes it until release', async () => {
    const session = await realController();
    session.controller.updateDraftProgram([{ id: 'cmd-1', kind: 'move' }]);
    const pending = session.controller.prepareForReload();
    session.controller.updateDraftProgram([{ id: 'cmd-2', kind: 'turn-right' }]);
    expect(await pending).toEqual({ safe: true, reason: 'persisted-readback', revision: 1 });
    expect((await session.stored())?.payload.p3).toMatchObject({ draftProgram: [{ id: 'cmd-1', kind: 'move' }] });
    expect(session.controller.dossier().p3.draftProgram).toEqual([{ id: 'cmd-1', kind: 'move' }]);
    session.controller.releaseReloadPreparation();
    session.controller.updateDraftProgram([{ id: 'cmd-3', kind: 'turn-left' }]);
    await session.controller.exportWork();
    expect(session.exported().payload.p3.draftProgram).toEqual([{ id: 'cmd-3', kind: 'turn-left' }]);
  });

  test('a completed write does not report a later draft as saved', async () => {
    const session = await realController();
    let resume!: () => void;
    session.pauseWrites(new Promise<void>((resolve) => { resume = resolve; }));
    session.controller.updateSystems({ timeControl: 'A', routeCalculation: '', boundary: '' });
    const pending = session.controller.flush();
    session.controller.updateSystems({ timeControl: 'B', routeCalculation: '', boundary: '' });
    resume();
    await pending;
    expect((await session.stored())?.payload.p6).toMatchObject({ timeControl: 'A' });
    expect(session.controller.saveState().state).toBe('changed');
    await session.controller.exportWork();
    expect(session.exported().payload.p6.timeControl).toBe('B');
  });

  test('volatile veto and a timed-out preparation release the current work', async () => {
    const session = await realController('volatile-selected');
    session.controller.updateReturnNote({ area: 'dossier', openPoint: 'A', nextAction: 'B' });
    expect(await session.controller.prepareForReload()).toEqual({ safe: false, reason: 'volatile' });
    session.controller.releaseReloadPreparation();
    session.controller.updateReturnNote({ area: 'sicherung', openPoint: 'C', nextAction: 'D' });
    await session.controller.exportWork();
    expect(session.exported().payload.returnNote.openPoint).toBe('C');
    session.controller.approveDiscardForReload();
    expect(await session.controller.prepareForReload()).toMatchObject({ safe: true, reason: 'explicit-discard' });
    session.controller.releaseReloadPreparation();
    session.controller.updateReturnNote({ area: 'auftrag', openPoint: 'E', nextAction: 'F' });
    expect(await session.controller.prepareForReload()).toEqual({ safe: false, reason: 'volatile' });
  });

  test('a late readiness result after release cannot approve newly edited work', async () => {
    const session = await realController();
    let resume!: () => void;
    session.pauseWrites(new Promise<void>((resolve) => { resume = resolve; }));
    session.controller.updateSystems({ timeControl: 'vor Timeout', routeCalculation: '', boundary: '' });
    const pending = session.controller.prepareForReload();
    session.controller.updateSystems({ timeControl: 'während Sperre', routeCalculation: '', boundary: '' });
    expect(session.controller.dossier().p6.timeControl).toBe('vor Timeout');
    session.controller.releaseReloadPreparation();
    session.controller.updateSystems({ timeControl: 'nach Timeout', routeCalculation: '', boundary: '' });
    resume();
    expect(await pending).toEqual({ safe: false, reason: 'readback-failed' });
    await session.controller.exportWork();
    expect(session.exported().payload.p6.timeControl).toBe('nach Timeout');
  });

  test('invalid drafts veto reload and never export a previous valid dossier', async () => {
    const session = await realController();
    session.controller.updateSystems({ timeControl: 'gültig', routeCalculation: '', boundary: '' });
    expect(await session.controller.flush()).toBe(true);
    session.controller.updateSystems({ timeControl: 'x'.repeat(501), routeCalculation: '', boundary: '' });
    expect(await session.controller.exportWork()).toBe(false);
    expect(await session.controller.prepareForReload()).toEqual({ safe: false, reason: 'write-failed' });
    expect(session.controller.saveState().state).toBe('unsaved');
    expect(session.controller.dossier().p6.timeControl).toHaveLength(501);
  });

  test('pending import and pending writes cannot authorize reload', async () => {
    const session = await realController();
    await session.controller.exportWork();
    expect(await session.controller.previewImport(new TextEncoder().encode(JSON.stringify(session.exported())))).toBe(true);
    expect(await session.controller.prepareForReload()).toEqual({ safe: false, reason: 'volatile' });
    session.controller.releaseReloadPreparation();
    const writer = await realController();
    let resume!: () => void;
    writer.pauseWrites(new Promise<void>((resolve) => { resume = resolve; }));
    const pending = writer.controller.flush();
    expect(await writer.controller.prepareForReload()).toEqual({ safe: false, reason: 'write-failed' });
    resume();
    await pending;
  });
});

function runtime(overrides: Partial<M06RuntimePort> = {}): M06RuntimePort {
  return {
    replacePayload: vi.fn((payload: Dossier) => ({ ok: true as const, payload })),
    flush: vi.fn(async () => ({ ok: true as const, mode: 'persistent' as const })),
    previewImport: vi.fn(() => ({ ok: false as const, error: { message: 'ungültig' } })),
    confirmImport: vi.fn(async () => ({ ok: true as const })),
    cancelImport: vi.fn(),
    deleteActive: vi.fn(async () => ({ ok: true as const })),
    prepareForReload: vi.fn(async () => ({ safe: true as const, reason: 'persisted-readback' as const, revision: 1 })),
    ...overrides,
  };
}

describe('M06 controller state machine', () => {
  test('flushes exactly the dossier and never transient P0/P4 answers', async () => {
    const port = runtime();
    const controller = createM06Controller(createInitialDossier(), port);
    controller.setTransient({ prediction: 'Osten', retrievalReason: 'Körper und Anzahl' });
    controller.updateReturnNote({ area: 'dossier', openPoint: 'Spur wählen', nextAction: 'Schritt 3 prüfen' });
    await controller.flush();
    expect(port.replacePayload).toHaveBeenCalledWith(controller.dossier());
    expect(JSON.stringify(vi.mocked(port.replacePayload).mock.calls[0]?.[0])).not.toMatch(/Osten|Körper und Anzahl/);
  });

  test('does not confirm an invalid import and marks failed saves as unsecured', async () => {
    const port = runtime({
      flush: vi.fn(async () => ({ ok: false as const, error: { message: 'Speichern fehlgeschlagen' } })),
    });
    const controller = createM06Controller(createInitialDossier(), port);
    expect(await controller.importBytes(new Uint8Array([1, 2, 3]))).toBe(false);
    expect(port.confirmImport).not.toHaveBeenCalled();
    await expect(controller.flush()).resolves.toBe(false);
    expect(controller.saveState()).toEqual({ state: 'unsaved', message: 'Speichern fehlgeschlagen' });
  });

  test('a code change invalidates old trace evidence but preserves the own diagram', () => {
    const original: Program = [{ id: 'cmd-1', kind: 'move' }];
    const dossier = createInitialDossier();
    const seeded: Dossier = {
      ...dossier,
      p3: {
        diagram: { program: original, explanation: 'Mein eigener Pfeil' },
        draftProgram: original,
        evidence: { program: original, predicted: null, steps: [1], rationale: 'Schritt 1' },
      },
    };
    const controller = createM06Controller(seeded, runtime());
    controller.updateDraftProgram([{ id: 'cmd-2', kind: 'turn-left' }]);
    expect(controller.dossier().p3.diagram.explanation).toBe('Mein eigener Pfeil');
    expect(controller.dossier().p3.evidence.steps).toEqual([]);
    expect(controller.dossier().p3.evidence.program).toEqual([]);
  });

  test('deleting clears dossier, transient answers and a pending import', async () => {
    const port = runtime({ previewImport: vi.fn(() => ({ ok: true as const })) });
    const controller = createM06Controller(createInitialDossier(), port);
    controller.setTransient({ prediction: 'Nord', retrievalReason: 'Abruf' });
    await controller.previewImport(new Uint8Array([1]));
    expect(await controller.deleteAllWork()).toBe(true);
    expect(port.cancelImport).toHaveBeenCalled();
    expect(controller.dossier()).toEqual(createInitialDossier());
    expect(controller.transient()).toEqual({ prediction: '', retrievalReason: '' });
  });
});
