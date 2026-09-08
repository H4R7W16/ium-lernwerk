import { describe, expect, test, vi } from 'vitest';
import {
  createInitialDossier,
  type Dossier,
  type Program,
} from '@ium/v2-g5-m06';
import {
  createM06Controller,
  type M06RuntimePort,
} from '../../apps/lernwerk-portal/src/controllers/m06/controller.js';

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
