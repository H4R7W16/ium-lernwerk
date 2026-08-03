import { describe, expect, test } from 'vitest';
import {
  MAX_EXECUTED_STEPS,
  MODULE_ID,
  parseAlgorithm,
  parseScenario,
} from '../../packages/ium-5-core-05/src/index.js';

describe('IUM-5-CORE-05 closed model', () => {
  test('exports the fixed module and execution limits', () => {
    expect(MODULE_ID).toBe('IUM-5-CORE-05');
    expect(MAX_EXECUTED_STEPS).toBe(100);
  });

  test('accepts basic commands and one fixed repeat', () => {
    expect(parseAlgorithm([
      { id: 'cmd-1', kind: 'pick-up' },
      {
        id: 'cmd-2',
        kind: 'repeat',
        count: 4,
        body: [{ id: 'cmd-3', kind: 'move' }],
      },
      { id: 'cmd-4', kind: 'drop' },
    ]).ok).toBe(true);
  });

  test.each([
    [{ id: 'cmd-1', kind: 'branch' }],
    [{
      id: 'cmd-1',
      kind: 'repeat',
      count: 1,
      body: [{ id: 'cmd-2', kind: 'move' }],
    }],
    [{
      id: 'cmd-1',
      kind: 'repeat',
      count: 10,
      body: [{ id: 'cmd-2', kind: 'move' }],
    }],
    [{ id: 'cmd-1', kind: 'repeat', count: 2, body: [] }],
    [{
      id: 'cmd-1',
      kind: 'repeat',
      count: 2,
      body: [{
        id: 'cmd-2',
        kind: 'repeat',
        count: 2,
        body: [{ id: 'cmd-3', kind: 'move' }],
      }],
    }],
  ])('rejects a forbidden command shape', (algorithm) => {
    expect(parseAlgorithm(algorithm).ok).toBe(false);
  });

  test('rejects duplicate command identifiers and unknown fields', () => {
    expect(parseAlgorithm([
      { id: 'cmd-1', kind: 'move' },
      { id: 'cmd-1', kind: 'turn-left' },
    ]).ok).toBe(false);
    expect(parseAlgorithm([
      { id: 'cmd-1', kind: 'move', score: 10 },
    ]).ok).toBe(false);
  });

  test('rejects a grid larger than six by six or positions outside it', () => {
    expect(parseScenario({
      id: 'oversized',
      title: 'Zu groß',
      width: 7,
      height: 6,
      start: {
        position: { column: 1, row: 1 },
        direction: 'east',
        carrying: false,
      },
      itemPosition: { column: 1, row: 1 },
      targetPosition: { column: 6, row: 6 },
      obstacles: [],
    }).ok).toBe(false);

    expect(parseScenario({
      id: 'outside',
      title: 'Außerhalb',
      width: 6,
      height: 6,
      start: {
        position: { column: 0, row: 1 },
        direction: 'east',
        carrying: false,
      },
      itemPosition: { column: 1, row: 1 },
      targetPosition: { column: 6, row: 6 },
      obstacles: [],
    }).ok).toBe(false);
  });
});
