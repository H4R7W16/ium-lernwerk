import { readFile } from 'node:fs/promises';
import { describe, expect, test } from 'vitest';
import {
  beginExecution,
  finishExecution,
  missionSucceeded,
  parseWorkbenchResources,
  stepExecution,
  type Algorithm,
  type Direction,
  type Scenario,
} from '../../packages/ium-5-core-05/src/index.js';

const straight: Scenario = {
  id: 'straight',
  title: 'Gerade Lieferung',
  width: 6,
  height: 3,
  start: {
    position: { column: 1, row: 2 },
    direction: 'east',
    carrying: false,
  },
  itemPosition: { column: 1, row: 2 },
  targetPosition: { column: 6, row: 2 },
  obstacles: [],
};

const algorithm: Algorithm = [
  { id: 'cmd-1', kind: 'pick-up' },
  {
    id: 'cmd-2',
    kind: 'repeat',
    count: 5,
    body: [{ id: 'cmd-3', kind: 'move' }],
  },
  { id: 'cmd-4', kind: 'drop' },
];

describe('deterministic interpreter', () => {
  test('step and full run produce the same trace and final state', () => {
    let stepped = beginExecution(straight, algorithm);
    while (stepped.status === 'ready' || stepped.status === 'running') {
      stepped = stepExecution(stepped);
    }
    const full = finishExecution(beginExecution(straight, algorithm));

    expect(stepped).toEqual(full);
    expect(missionSucceeded(straight, full.state)).toBe(true);
    expect(full.trace).toHaveLength(7);
    expect(full.trace[1]?.loop).toEqual({ iteration: 1, total: 5 });
  });

  test('identical inputs produce an identical semantic session', () => {
    const first = finishExecution(beginExecution(straight, algorithm));
    const second = finishExecution(beginExecution(straight, algorithm));
    expect(second).toEqual(first);
  });

  test('continues deterministically from a structured-cloned transient session', () => {
    const cloned = structuredClone(beginExecution(straight, algorithm));
    const result = finishExecution(cloned);

    expect(result.status).toBe('complete');
    expect(missionSucceeded(straight, result.state)).toBe(true);
  });

  test('fails closed before execution when the scenario is invalid', () => {
    const invalid = { ...straight, width: 0 } as Scenario;
    expect(() => beginExecution(invalid, algorithm)).toThrow('Invalid scenario');
  });

  test.each([
    ['OBSTACLE', [{ id: 'cmd-1', kind: 'move' }]],
    ['OUT_OF_BOUNDS', [
      { id: 'cmd-1', kind: 'turn-left' },
      { id: 'cmd-2', kind: 'move' },
      { id: 'cmd-3', kind: 'move' },
    ]],
    ['INVALID_PICK_UP', [
      { id: 'cmd-1', kind: 'move' },
      { id: 'cmd-2', kind: 'pick-up' },
    ]],
    ['INVALID_DROP', [{ id: 'cmd-1', kind: 'drop' }]],
  ] as const)(
    'stops with %s and leaves the failed state unchanged',
    (code, commands) => {
      const scenario = code === 'OBSTACLE'
        ? { ...straight, obstacles: [{ column: 2, row: 2 }] }
        : straight;
      const result = finishExecution(beginExecution(scenario, commands));

      expect(result.status).toBe('error');
      expect(result.error).toBe(code);
      expect(result.trace.at(-1)?.before).toEqual(result.trace.at(-1)?.after);
    },
  );

  test('rejects picking up while carrying and dropping outside the target', () => {
    const duplicatePick = finishExecution(beginExecution(straight, [
      { id: 'cmd-1', kind: 'pick-up' },
      { id: 'cmd-2', kind: 'pick-up' },
    ]));
    expect(duplicatePick.error).toBe('INVALID_PICK_UP');
    expect(duplicatePick.trace.at(-1)?.before)
      .toEqual(duplicatePick.trace.at(-1)?.after);

    const earlyDrop = finishExecution(beginExecution(straight, [
      { id: 'cmd-1', kind: 'pick-up' },
      { id: 'cmd-2', kind: 'move' },
      { id: 'cmd-3', kind: 'drop' },
    ]));
    expect(earlyDrop.error).toBe('INVALID_DROP');
    expect(earlyDrop.trace.at(-1)?.before)
      .toEqual(earlyDrop.trace.at(-1)?.after);
  });

  test.each([
    ['north', 'turn-left', 'west'],
    ['north', 'turn-right', 'east'],
    ['east', 'turn-left', 'north'],
    ['east', 'turn-right', 'south'],
    ['south', 'turn-left', 'east'],
    ['south', 'turn-right', 'west'],
    ['west', 'turn-left', 'south'],
    ['west', 'turn-right', 'north'],
  ] as const)(
    'turns from %s with %s toward %s',
    (startDirection, commandKind, expectedDirection) => {
      const scenario: Scenario = {
        ...straight,
        start: { ...straight.start, direction: startDirection },
      };
      const result = finishExecution(beginExecution(scenario, [
        { id: 'cmd-1', kind: commandKind },
      ]));

      expect(result.status).toBe('complete');
      expect(result.state.direction).toBe(expectedDirection satisfies Direction);
    },
  );

  test('reports INVALID_REPEAT before moving', () => {
    const unsafe = [{
      id: 'cmd-1',
      kind: 'repeat',
      count: 1,
      body: [{ id: 'cmd-2', kind: 'move' }],
    }];
    const result = beginExecution(straight, unsafe as Algorithm);

    expect(result.status).toBe('error');
    expect(result.error).toBe('INVALID_REPEAT');
    expect(result.trace).toHaveLength(1);
    expect(result.trace[0]?.before).toEqual(result.trace[0]?.after);
  });

  test('executes 100 basic steps and stops before step 101', () => {
    const many = Array.from({ length: 101 }, (_, index) => ({
      id: `cmd-${index + 1}`,
      kind: index % 2 === 0 ? 'turn-left' : 'turn-right',
    })) as Algorithm;
    const result = finishExecution(beginExecution(straight, many));

    expect(result.status).toBe('error');
    expect(result.error).toBe('STEP_LIMIT');
    expect(result.trace).toHaveLength(101);
    expect(result.trace.at(-1)?.step).toBe(101);
    expect(result.trace.at(-1)?.before).toEqual(result.trace.at(-1)?.after);
  });

  test('does not mutate scenario or algorithm', () => {
    const scenarioBefore = structuredClone(straight);
    const algorithmBefore = structuredClone(algorithm);
    finishExecution(beginExecution(straight, algorithm));

    expect(straight).toEqual(scenarioBefore);
    expect(algorithm).toEqual(algorithmBefore);
  });

  test('every module reference algorithm completes its declared mission', async () => {
    const content = JSON.parse(await readFile(
      'modules/IUM-5-CORE-05/lernumgebung/content.json',
      'utf8',
    )) as unknown;
    const scenarios = JSON.parse(await readFile(
      'modules/IUM-5-CORE-05/lernumgebung/scenarios.json',
      'utf8',
    )) as unknown;
    const resources = parseWorkbenchResources(content, scenarios);
    expect(resources.ok).toBe(true);
    if (!resources.ok) {
      return;
    }

    for (const entry of resources.value.scenarios) {
      const result = finishExecution(beginExecution(
        entry.scenario,
        entry.referenceAlgorithm,
      ));
      expect(result.status, entry.scenario.id).toBe('complete');
      expect(
        missionSucceeded(entry.scenario, result.state),
        entry.scenario.id,
      ).toBe(true);
    }
  });
});
