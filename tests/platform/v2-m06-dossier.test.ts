import { describe, expect, test } from 'vitest';
import {
  createInitialDossier,
  evidenceBelongsToProgram,
  parseDossier,
  projectDossier,
  type Dossier,
  type Program,
  type SessionState,
} from '../../packages/v2-g5-m06/src/index.js';

const oldProgram: Program = [{ id: 'cmd-1', kind: 'move' }];
const newProgram: Program = [{ id: 'cmd-2', kind: 'turn-left' }];

function filledDossier(): Dossier {
  return {
    schemaVersion: 1,
    p1: { diagram: { program: oldProgram, explanation: 'Körper erklärt' } },
    p2: {
      before: { program: oldProgram, predicted: null, steps: [1], rationale: 'Vorher' },
      after: { program: newProgram, predicted: {
        position: { column: 1, row: 3 }, direction: 'north',
      }, steps: [1], rationale: 'Nachher' },
      firstDeviation: 1,
    },
    p3: {
      diagram: { program: oldProgram, explanation: 'Eigener Entwurf' },
      draftProgram: newProgram,
      evidence: { program: oldProgram, predicted: null, steps: [1], rationale: 'Spur' },
    },
    p5: { sequence: ['aufnehmen', 'prüfen', 'ablegen'], rationale: 'Zustandsfolge' },
    p6: {
      timeControl: 'Verarbeitet Zeitpunkte.',
      routeCalculation: 'Verarbeitet Start und Ziel.',
      boundary: 'Ein Standbild reicht nicht.',
    },
    returnNote: { area: 'dossier', openPoint: 'Beleg erneuern', nextAction: 'Neu ausführen' },
  };
}

describe('V2 M06 dossier validation', () => {
  test('creates a valid but unfinished product dossier', () => {
    const dossier = createInitialDossier();
    expect(parseDossier(dossier)).toEqual({ ok: true, value: dossier });
    expect(dossier.p3.diagram.program).toEqual([]);
    expect(dossier.p3.draftProgram).toEqual([]);
    expect(dossier.p3.evidence.program).toEqual([]);
  });

  test('accepts all and only P1, P2, P3, P5, P6 plus the return note', () => {
    expect(parseDossier(filledDossier()).ok).toBe(true);
    expect(parseDossier({ ...filledDossier(), p0: 'PRIVATE-P0' }).ok).toBe(false);
    expect(parseDossier({ ...filledDossier(), p4: 'PRIVATE-P4' }).ok).toBe(false);
    expect(parseDossier({ ...filledDossier(), helpHistory: ['H1'] }).ok).toBe(false);
  });

  test('enforces Unicode-codepoint limits without truncation', () => {
    const valid = filledDossier();
    valid.p1.diagram.explanation = '😀'.repeat(500);
    valid.returnNote.openPoint = 'ö'.repeat(200);
    expect(parseDossier(valid).ok).toBe(true);

    const tooLongExplanation = filledDossier();
    tooLongExplanation.p1.diagram.explanation = '😀'.repeat(501);
    expect(parseDossier(tooLongExplanation).ok).toBe(false);
    const tooLongReturn = filledDossier();
    tooLongReturn.returnNote.nextAction = 'x'.repeat(201);
    expect(parseDossier(tooLongReturn).ok).toBe(false);
  });

  test('binds selected evidence steps to its own program and the 100-action cap', () => {
    const invalidStep = filledDossier();
    invalidStep.p3.evidence.steps = [2];
    expect(parseDossier(invalidStep).ok).toBe(false);

    const hundredTurns: Program = Array.from({ length: 100 }, (_, index) => ({
      id: `cmd-${index + 1}`, kind: 'turn-left' as const,
    }));
    const capped = filledDossier();
    capped.p3.evidence = {
      program: hundredTurns, predicted: null, steps: [1, 100], rationale: '',
    };
    expect(parseDossier(capped).ok).toBe(true);
    capped.p3.evidence.steps = [101];
    expect(parseDossier(capped).ok).toBe(false);
  });

  test('rejects malformed predictions, products and S4 sequences', () => {
    expect(parseDossier({ ...filledDossier(), schemaVersion: 2 }).ok).toBe(false);
    expect(parseDossier({ ...filledDossier(), p5: {
      sequence: ['aufnehmen', 'ablegen'], rationale: '',
    } }).ok).toBe(true);
    expect(parseDossier({ ...filledDossier(), p5: {
      sequence: ['aufnehmen', 'scannen'], rationale: '',
    } }).ok).toBe(false);
    const malformed = filledDossier();
    malformed.p2.after.predicted = {
      position: { column: 0, row: 1 }, direction: 'north',
    };
    expect(parseDossier(malformed).ok).toBe(false);
  });
});

describe('V2 M06 dossier projection and code binding', () => {
  test('projects only the explicit dossier and deep-copies its products', () => {
    const dossier = filledDossier();
    const session: SessionState = {
      dossier,
      p0: 'PRIVATE-P0',
      p4: 'PRIVATE-P4',
      selectedHelp: 'H3',
      currentRun: null,
    };
    const projected = projectDossier(session);
    expect(JSON.stringify(projected)).not.toContain('PRIVATE-P0');
    expect(JSON.stringify(projected)).not.toContain('PRIVATE-P4');
    expect(JSON.stringify(projected)).not.toContain('H3');
    expect(projected).toEqual(dossier);
    expect(projected).not.toBe(dossier);
    expect(projected.p3.draftProgram).not.toBe(dossier.p3.draftProgram);
  });

  test('keeps the editable diagram, draft code and selected evidence distinct', () => {
    const dossier = filledDossier();
    expect(dossier.p3.diagram.program).toEqual(oldProgram);
    expect(dossier.p3.draftProgram).toEqual(newProgram);
    expect(dossier.p3.evidence.program).toEqual(oldProgram);
    expect(evidenceBelongsToProgram(dossier.p3.evidence, dossier.p3.draftProgram)).toBe(false);
    expect(evidenceBelongsToProgram(dossier.p3.evidence, oldProgram)).toBe(true);
  });

  test('does not bind an old trace to semantically equal code with different IDs', () => {
    const evidence = { program: oldProgram, predicted: null, steps: [1], rationale: '' };
    expect(evidenceBelongsToProgram(evidence, [{ id: 'cmd-9', kind: 'move' }])).toBe(false);
  });

  test('rejects an invalid dossier instead of silently dropping fields', () => {
    const session = {
      dossier: { ...filledDossier(), trialHistory: ['PRIVATE'] },
      p0: '', p4: '', selectedHelp: null, currentRun: null,
    } as unknown as SessionState;
    expect(() => projectDossier(session)).toThrow(/dossier/i);
  });
});
