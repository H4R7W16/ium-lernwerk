import { describe, expect, test } from 'vitest';
import {
  checkGoal,
  insert,
  move,
  parseProgram,
  programSemanticsEqual,
  remove,
  run,
  turn,
  type Basic,
  type Grid,
  type Program,
} from '../../packages/v2-g5-m06/src/index.js';

const start = { position: { column: 1, row: 3 }, direction: 'east' as const };
const grid = { width: 5, height: 4, start };
const rectangleGoal = {
  checkpoints: [
    { column: 3, row: 3 },
    { column: 3, row: 2 },
    { column: 1, row: 2 },
    { column: 1, row: 3 },
  ],
  end: start,
  boundary: { left: 1, right: 3, top: 2, bottom: 3 },
};

function basic(id: number, kind: Basic['kind']): Basic {
  return { id: `cmd-${id}`, kind };
}

describe('V2 M06 program validation', () => {
  test('accepts a five-command body and rejects non-M06 or open commands', () => {
    const five = parseProgram([{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      basic(2, 'move'), basic(3, 'move'), basic(4, 'turn-left'),
      basic(5, 'move'), basic(6, 'turn-left'),
    ] }]);
    expect(five.ok).toBe(true);
    expect(parseProgram([{ id: 'cmd-1', kind: 'pick-up' }]).ok).toBe(false);
    expect(parseProgram([{ id: 'cmd-1', kind: 'move', extra: true }]).ok).toBe(false);
  });

  test.each([
    [{ id: 'cmd-1', kind: 'repeat', count: 0, body: [basic(2, 'move')] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 1, body: [basic(2, 'move')] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 10, body: [basic(2, 'move')] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      basic(2, 'move'), basic(3, 'move'), basic(4, 'move'),
      basic(5, 'move'), basic(6, 'move'), basic(7, 'move'),
    ] }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      { id: 'cmd-2', kind: 'repeat', count: 2, body: [basic(3, 'move')] },
    ] }],
  ])('rejects invalid repeat boundaries %#', (candidate) => {
    expect(parseProgram(candidate).ok).toBe(false);
  });

  test('requires globally unique, canonical command identifiers', () => {
    expect(parseProgram([basic(1, 'move'), basic(1, 'turn-left')]).ok).toBe(false);
    expect(parseProgram([{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      basic(2, 'move'), basic(1, 'turn-left'),
    ] }]).ok).toBe(false);
    expect(parseProgram([{ id: 'cmd-0', kind: 'move' }]).ok).toBe(false);
  });
});

describe('V2 M06 interpreter and goal semantics', () => {
  test('five-command body executes the required rectangle; empty code does not', () => {
    const parsed = parseProgram([{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      { id: 'cmd-2', kind: 'move' }, { id: 'cmd-3', kind: 'move' },
      { id: 'cmd-4', kind: 'turn-left' }, { id: 'cmd-5', kind: 'move' },
      { id: 'cmd-6', kind: 'turn-left' },
    ] }]);
    expect(parsed.ok).toBe(true);
    if (!parsed.ok) throw new Error('Reference must parse');
    const result = run(grid, parsed.value);
    expect(result.trace).toHaveLength(10);
    expect(result.state).toEqual(start);
    expect(checkGoal(result, rectangleGoal).ok).toBe(true);
    expect(checkGoal(run(grid, []), rectangleGoal).ok).toBe(false);
  });

  test('executes S0 and S1 with the specified direction changes', () => {
    const s0Grid = { width: 3, height: 3, start: {
      position: { column: 1, row: 3 }, direction: 'north' as const,
    } };
    const s0 = run(s0Grid, [basic(1, 'move'), basic(2, 'turn-right'), basic(3, 'move')]);
    expect(s0.trace.map((entry) => entry.after)).toEqual([
      { position: { column: 1, row: 2 }, direction: 'north' },
      { position: { column: 1, row: 2 }, direction: 'east' },
      { position: { column: 2, row: 2 }, direction: 'east' },
    ]);

    const s1Start = { position: { column: 2, row: 3 }, direction: 'east' as const };
    const s1 = run({ width: 4, height: 4, start: s1Start }, [{
      id: 'cmd-1', kind: 'repeat', count: 4,
      body: [basic(2, 'move'), basic(3, 'turn-left')],
    }]);
    expect(s1.trace).toHaveLength(8);
    expect(s1.state).toEqual(s1Start);
    expect(s1.status).toBe('complete');
  });

  test('keeps the failed S2 move unchanged and identifies action three', () => {
    const s2Grid = { width: 4, height: 4, start: {
      position: { column: 2, row: 3 }, direction: 'east' as const,
    } };
    const result = run(s2Grid, [
      { id: 'cmd-1', kind: 'repeat', count: 4, body: [basic(2, 'move')] },
      basic(3, 'turn-left'),
    ]);
    expect(result.status).toBe('OUT_OF_BOUNDS');
    expect(result.trace).toHaveLength(3);
    expect(result.trace[2]).toMatchObject({
      step: 3, commandId: 'cmd-2', iteration: 3, error: 'OUT_OF_BOUNDS',
      before: { position: { column: 4, row: 3 }, direction: 'east' },
      after: { position: { column: 4, row: 3 }, direction: 'east' },
    });
  });

  test('permits exactly 100 actions and stops before action 101', () => {
    const hundred: Program = Array.from({ length: 100 }, (_, index) =>
      basic(index + 1, 'turn-left'));
    const oneHundredOne: Program = [...hundred, basic(101, 'turn-left')];
    expect(run(grid, hundred)).toMatchObject({ status: 'complete' });
    const limited = run(grid, oneHundredOne);
    expect(limited.status).toBe('STEP_LIMIT');
    expect(limited.trace).toHaveLength(100);
    expect(limited.trace[99]).toMatchObject({ step: 100, commandId: 'cmd-100' });
  });

  test('validates positive integral grids and an in-grid start', () => {
    expect(() => run({ ...grid, width: 0 }, [])).toThrow(/grid/i);
    expect(() => run({ ...grid, height: 1.5 }, [])).toThrow(/grid/i);
    expect(() => run({ ...grid, start: {
      ...start, position: { column: 6, row: 3 },
    } }, [])).toThrow(/grid/i);
  });

  test('requires ordered checkpoints, correct end and movement on the boundary', () => {
    const correct = run(grid, [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [
      basic(2, 'move'), basic(3, 'move'), basic(4, 'turn-left'),
      basic(5, 'move'), basic(6, 'turn-left'),
    ] }]);
    expect(checkGoal(correct, { ...rectangleGoal, checkpoints: [
      rectangleGoal.checkpoints[1]!, rectangleGoal.checkpoints[0]!,
    ] }).reason).toBe('missing-checkpoint');
    expect(checkGoal(correct, { ...rectangleGoal, end: {
      ...start, direction: 'north',
    } }).reason).toBe('wrong-end');

    const throughInterior = run({ width: 4, height: 4, start: {
      position: { column: 1, row: 2 }, direction: 'east' as const,
    } }, [basic(1, 'move'), basic(2, 'move'), basic(3, 'move')]);
    expect(checkGoal(throughInterior, {
      checkpoints: [{ column: 4, row: 2 }],
      end: throughInterior.state,
      boundary: { left: 1, right: 4, top: 1, bottom: 4 },
    }).reason).toBe('off-boundary');

    const entersFromOutside = run({ width: 5, height: 4, start: {
      position: { column: 4, row: 3 }, direction: 'west' as const,
    } }, [basic(1, 'move')]);
    expect(checkGoal(entersFromOutside, {
      checkpoints: [{ column: 3, row: 3 }],
      end: entersFromOutside.state,
      boundary: rectangleGoal.boundary,
    }).reason).toBe('off-boundary');

    const twoCorrectLaps = run(grid, [{ id: 'cmd-1', kind: 'repeat', count: 4, body: [
      basic(2, 'move'), basic(3, 'move'), basic(4, 'turn-left'),
      basic(5, 'move'), basic(6, 'turn-left'),
    ] }]);
    expect(checkGoal(twoCorrectLaps, rectangleGoal)).toEqual({ ok: true, reason: 'complete' });
  });

  test('keeps semantic comparison separate from command identifiers', () => {
    expect(programSemanticsEqual(
      [basic(1, 'move'), basic(2, 'turn-left')],
      [basic(8, 'move'), basic(9, 'turn-left')],
    )).toBe(true);
    expect(programSemanticsEqual(
      [basic(1, 'move')],
      [basic(8, 'turn-left')],
    )).toBe(false);
    expect(turn('north', -1)).toBe('west');
    expect(turn('west', 1)).toBe('north');
  });
});

describe('V2 M06 editor operations', () => {
  test('insert, remove and move return validated immutable programs', () => {
    const original: Program = [basic(1, 'move'), basic(2, 'turn-left')];
    expect(insert(original, 1, basic(3, 'turn-right'))).toEqual([
      basic(1, 'move'), basic(3, 'turn-right'), basic(2, 'turn-left'),
    ]);
    expect(remove(original, 'cmd-1')).toEqual([basic(2, 'turn-left')]);
    expect(move(original, 'cmd-1', 1)).toEqual([basic(2, 'turn-left'), basic(1, 'move')]);
    expect(original).toEqual([basic(1, 'move'), basic(2, 'turn-left')]);
  });

  test('rejects missing IDs, invalid indices and invalid results', () => {
    const original: Program = [basic(1, 'move')];
    expect(() => insert(original, 2, basic(2, 'move'))).toThrow();
    expect(() => insert(original, 1, basic(1, 'move'))).toThrow();
    expect(() => remove(original, 'cmd-9')).toThrow();
    expect(() => move(original, 'cmd-9', 0)).toThrow();
    expect(() => move(original, 'cmd-1', -1)).toThrow();
  });
});
