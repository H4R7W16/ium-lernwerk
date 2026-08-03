import { describe, expect, test } from 'vitest';
import {
  insertCommand,
  moveCommand,
  nextCommandId,
  removeCommand,
  replaceRepeat,
} from '../../packages/ium-5-core-05/src/index.js';

describe('immutable command editor', () => {
  test('inserts, moves and removes without mutating the source', () => {
    const source = [{ id: 'cmd-1', kind: 'move' }] as const;
    const inserted = insertCommand(
      source,
      1,
      { id: 'cmd-2', kind: 'turn-right' },
    );
    expect(inserted.map((command) => command.id)).toEqual(['cmd-1', 'cmd-2']);
    expect(moveCommand(inserted, 1, -1).map((command) => command.id))
      .toEqual(['cmd-2', 'cmd-1']);
    expect(removeCommand(inserted, 0).map((command) => command.id))
      .toEqual(['cmd-2']);
    expect(source).toEqual([{ id: 'cmd-1', kind: 'move' }]);
  });

  test('rejects an invalid repeat edit instead of normalizing it', () => {
    const source = [{
      id: 'cmd-1',
      kind: 'repeat',
      count: 2,
      body: [{ id: 'cmd-2', kind: 'move' }],
    }] as const;
    expect(() => replaceRepeat(source, 0, {
      id: 'cmd-1',
      kind: 'repeat',
      count: 1,
      body: [{ id: 'cmd-2', kind: 'move' }],
    })).toThrow('Invalid algorithm');
  });

  test('continues identifiers after imported top-level and loop commands', () => {
    expect(nextCommandId([
      { id: 'cmd-2', kind: 'move' },
      {
        id: 'cmd-4',
        kind: 'repeat',
        count: 2,
        body: [{ id: 'cmd-7', kind: 'move' }],
      },
    ])).toBe('cmd-8');
  });

  test('returns a new copy for a boundary move and rejects invalid deltas', () => {
    const source = [{ id: 'cmd-1', kind: 'move' }] as const;
    const unchanged = moveCommand(source, 0, -1);
    expect(unchanged).toEqual(source);
    expect(unchanged).not.toBe(source);
    expect(() => moveCommand(source, 0, 2)).toThrow(RangeError);
  });
});
