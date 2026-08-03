import {
  MAX_EXECUTED_STEPS,
  type Algorithm,
  type BasicCommandKind,
  type Direction,
  type InterpreterErrorCode,
  type Position,
  type Scenario,
  type TraceEntry,
  type WorldState,
} from './model.js';
import { parseAlgorithm, parseScenario } from './validation.js';

export type ExecutionStatus = 'ready' | 'running' | 'complete' | 'error';

type ProgramEntry = Readonly<{
  sourceCommandId: string;
  commandKind: BasicCommandKind;
  loop: Readonly<{ iteration: number; total: number }> | null;
}>;

export type ExecutionSession = Readonly<{
  scenarioId: string;
  scenario: Scenario;
  status: ExecutionStatus;
  state: WorldState;
  program: readonly ProgramEntry[];
  cursor: number;
  trace: readonly TraceEntry[];
  error: InterpreterErrorCode | null;
}>;

const leftTurns: Readonly<Record<Direction, Direction>> = {
  north: 'west',
  west: 'south',
  south: 'east',
  east: 'north',
};
const rightTurns: Readonly<Record<Direction, Direction>> = {
  north: 'east',
  east: 'south',
  south: 'west',
  west: 'north',
};

function clonePosition(position: Position): Position {
  return { column: position.column, row: position.row };
}

function cloneState(state: WorldState): WorldState {
  return {
    position: clonePosition(state.position),
    direction: state.direction,
    carrying: state.carrying,
    itemPosition: state.itemPosition === null
      ? null
      : clonePosition(state.itemPosition),
    delivered: state.delivered,
  };
}

function cloneScenario(scenario: Scenario): Scenario {
  return {
    id: scenario.id,
    title: scenario.title,
    width: scenario.width,
    height: scenario.height,
    start: {
      position: clonePosition(scenario.start.position),
      direction: scenario.start.direction,
      carrying: false,
    },
    itemPosition: clonePosition(scenario.itemPosition),
    targetPosition: clonePosition(scenario.targetPosition),
    obstacles: scenario.obstacles.map(clonePosition),
  };
}

function cloneProgramEntry(entry: ProgramEntry): ProgramEntry {
  return {
    sourceCommandId: entry.sourceCommandId,
    commandKind: entry.commandKind,
    loop: entry.loop === null
      ? null
      : { iteration: entry.loop.iteration, total: entry.loop.total },
  };
}

function cloneTraceEntry(entry: TraceEntry): TraceEntry {
  return {
    step: entry.step,
    sourceCommandId: entry.sourceCommandId,
    commandKind: entry.commandKind,
    loop: entry.loop === null
      ? null
      : { iteration: entry.loop.iteration, total: entry.loop.total },
    before: cloneState(entry.before),
    after: cloneState(entry.after),
    outcome: entry.outcome,
    error: entry.error,
  };
}

function cloneSession(session: ExecutionSession): ExecutionSession {
  return {
    scenarioId: session.scenarioId,
    scenario: cloneScenario(session.scenario),
    status: session.status,
    state: cloneState(session.state),
    program: session.program.map(cloneProgramEntry),
    cursor: session.cursor,
    trace: session.trace.map(cloneTraceEntry),
    error: session.error,
  };
}

function initialState(scenario: Scenario): WorldState {
  return {
    position: clonePosition(scenario.start.position),
    direction: scenario.start.direction,
    carrying: false,
    itemPosition: clonePosition(scenario.itemPosition),
    delivered: false,
  };
}

function positionsEqual(left: Position, right: Position): boolean {
  return left.column === right.column && left.row === right.row;
}

function invalidRepeatSession(scenario: Scenario, algorithm: Algorithm): ExecutionSession {
  const state = initialState(scenario);
  const first = algorithm[0] as Readonly<Record<string, unknown>> | undefined;
  const sourceCommandId = typeof first?.id === 'string' ? first.id : 'cmd-1';
  return {
    scenarioId: scenario.id,
    scenario: cloneScenario(scenario),
    status: 'error',
    state: cloneState(state),
    program: [],
    cursor: 0,
    trace: [{
      step: 1,
      sourceCommandId,
      commandKind: 'repeat',
      loop: null,
      before: cloneState(state),
      after: cloneState(state),
      outcome: 'error',
      error: 'INVALID_REPEAT',
    }],
    error: 'INVALID_REPEAT',
  };
}

function expandAlgorithm(algorithm: Algorithm): readonly ProgramEntry[] {
  const program: ProgramEntry[] = [];
  outer: for (const command of algorithm) {
    if (command.kind !== 'repeat') {
      program.push({
        sourceCommandId: command.id,
        commandKind: command.kind,
        loop: null,
      });
      if (program.length >= MAX_EXECUTED_STEPS + 1) {
        break;
      }
      continue;
    }
    for (let iteration = 1; iteration <= command.count; iteration += 1) {
      for (const bodyCommand of command.body) {
        program.push({
          sourceCommandId: bodyCommand.id,
          commandKind: bodyCommand.kind,
          loop: { iteration, total: command.count },
        });
        if (program.length >= MAX_EXECUTED_STEPS + 1) {
          break outer;
        }
      }
    }
  }
  return program;
}

export function beginExecution(
  scenarioValue: Scenario,
  algorithmValue: Algorithm,
): ExecutionSession {
  const scenario = parseScenario(scenarioValue);
  if (!scenario.ok) {
    throw new TypeError(`Invalid scenario: ${JSON.stringify(scenario.issues)}`);
  }
  const algorithm = parseAlgorithm(algorithmValue);
  if (!algorithm.ok) {
    return invalidRepeatSession(scenario.value, algorithmValue);
  }
  const program = expandAlgorithm(algorithm.value);
  return {
    scenarioId: scenario.value.id,
    scenario: cloneScenario(scenario.value),
    status: program.length === 0 ? 'complete' : 'ready',
    state: initialState(scenario.value),
    program,
    cursor: 0,
    trace: [],
    error: null,
  };
}

function movePosition(position: Position, direction: Direction): Position {
  switch (direction) {
    case 'north':
      return { column: position.column, row: position.row - 1 };
    case 'east':
      return { column: position.column + 1, row: position.row };
    case 'south':
      return { column: position.column, row: position.row + 1 };
    case 'west':
      return { column: position.column - 1, row: position.row };
  }
}

function failedStep(
  session: ExecutionSession,
  entry: ProgramEntry,
  error: InterpreterErrorCode,
): ExecutionSession {
  const state = cloneState(session.state);
  const traceEntry: TraceEntry = {
    step: session.trace.length + 1,
    sourceCommandId: entry.sourceCommandId,
    commandKind: entry.commandKind,
    loop: entry.loop === null
      ? null
      : { iteration: entry.loop.iteration, total: entry.loop.total },
    before: cloneState(state),
    after: cloneState(state),
    outcome: 'error',
    error,
  };
  return {
    scenarioId: session.scenarioId,
    scenario: cloneScenario(session.scenario),
    status: 'error',
    state,
    program: session.program.map(cloneProgramEntry),
    cursor: session.cursor,
    trace: [...session.trace.map(cloneTraceEntry), traceEntry],
    error,
  };
}

function successfulStep(
  session: ExecutionSession,
  entry: ProgramEntry,
  nextState: WorldState,
): ExecutionSession {
  const nextCursor = session.cursor + 1;
  const traceEntry: TraceEntry = {
    step: session.trace.length + 1,
    sourceCommandId: entry.sourceCommandId,
    commandKind: entry.commandKind,
    loop: entry.loop === null
      ? null
      : { iteration: entry.loop.iteration, total: entry.loop.total },
    before: cloneState(session.state),
    after: cloneState(nextState),
    outcome: 'ok',
    error: null,
  };
  return {
    scenarioId: session.scenarioId,
    scenario: cloneScenario(session.scenario),
    status: nextCursor >= session.program.length ? 'complete' : 'running',
    state: cloneState(nextState),
    program: session.program.map(cloneProgramEntry),
    cursor: nextCursor,
    trace: [...session.trace.map(cloneTraceEntry), traceEntry],
    error: null,
  };
}

export function stepExecution(session: ExecutionSession): ExecutionSession {
  if (session.status === 'complete' || session.status === 'error') {
    return cloneSession(session);
  }
  const entry = session.program[session.cursor];
  if (entry === undefined) {
    return { ...cloneSession(session), status: 'complete' };
  }
  if (session.cursor >= MAX_EXECUTED_STEPS) {
    return failedStep(session, entry, 'STEP_LIMIT');
  }

  const state = cloneState(session.state);
  switch (entry.commandKind) {
    case 'turn-left':
      return successfulStep(session, entry, {
        ...state,
        direction: leftTurns[state.direction],
      });
    case 'turn-right':
      return successfulStep(session, entry, {
        ...state,
        direction: rightTurns[state.direction],
      });
    case 'move': {
      const position = movePosition(state.position, state.direction);
      if (
        position.column < 1
        || position.column > session.scenario.width
        || position.row < 1
        || position.row > session.scenario.height
      ) {
        return failedStep(session, entry, 'OUT_OF_BOUNDS');
      }
      if (session.scenario.obstacles.some((obstacle) =>
        positionsEqual(obstacle, position))) {
        return failedStep(session, entry, 'OBSTACLE');
      }
      return successfulStep(session, entry, { ...state, position });
    }
    case 'pick-up':
      if (
        state.carrying
        || state.itemPosition === null
        || !positionsEqual(state.position, state.itemPosition)
      ) {
        return failedStep(session, entry, 'INVALID_PICK_UP');
      }
      return successfulStep(session, entry, {
        ...state,
        carrying: true,
        itemPosition: null,
        delivered: false,
      });
    case 'drop':
      if (
        !state.carrying
        || !positionsEqual(state.position, session.scenario.targetPosition)
      ) {
        return failedStep(session, entry, 'INVALID_DROP');
      }
      return successfulStep(session, entry, {
        ...state,
        carrying: false,
        itemPosition: clonePosition(session.scenario.targetPosition),
        delivered: true,
      });
  }
}

export function finishExecution(session: ExecutionSession): ExecutionSession {
  let current = cloneSession(session);
  while (current.status === 'ready' || current.status === 'running') {
    current = stepExecution(current);
  }
  return current;
}

export function missionSucceeded(scenario: Scenario, state: WorldState): boolean {
  return state.delivered
    && !state.carrying
    && state.itemPosition !== null
    && positionsEqual(state.itemPosition, scenario.targetPosition)
    && positionsEqual(state.position, scenario.targetPosition);
}
