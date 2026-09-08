import { MAX_EXECUTED_ACTIONS, type Basic, type Direction, type Grid, type Program, type Run, type State, type TraceStep } from './model.js';
import { parseGrid, parseProgram } from './validation.js';

const directions: readonly Direction[] = ['north', 'east', 'south', 'west'];

export function turn(direction: Direction, delta: -1 | 1): Direction {
  return directions[(directions.indexOf(direction) + delta + 4) % 4]!;
}

function cloneState(state: State): State {
  return {
    position: { column: state.position.column, row: state.position.row },
    direction: state.direction,
  };
}

function moved(state: State): State {
  const { column, row } = state.position;
  const position = state.direction === 'north' ? { column, row: row - 1 }
    : state.direction === 'east' ? { column: column + 1, row }
      : state.direction === 'south' ? { column, row: row + 1 }
        : { column: column - 1, row };
  return { position, direction: state.direction };
}

function apply(state: State, command: Basic): State {
  if (command.kind === 'move') return moved(state);
  return {
    position: { ...state.position },
    direction: turn(state.direction, command.kind === 'turn-left' ? -1 : 1),
  };
}

function inside(state: State, grid: Grid): boolean {
  return state.position.column >= 1 && state.position.column <= grid.width
    && state.position.row >= 1 && state.position.row <= grid.height;
}

type Action = Readonly<{ command: Basic; iteration: number | null }>;

function actions(program: Program): Action[] {
  const result: Action[] = [];
  outer: for (const command of program) {
    if (command.kind !== 'repeat') {
      result.push({ command, iteration: null });
      if (result.length > MAX_EXECUTED_ACTIONS) break;
      continue;
    }
    for (let iteration = 1; iteration <= command.count; iteration += 1) {
      for (const bodyCommand of command.body) {
        result.push({ command: bodyCommand, iteration });
        if (result.length > MAX_EXECUTED_ACTIONS) break outer;
      }
    }
  }
  return result;
}

export function run(gridInput: Grid, programInput: Program): Run {
  const grid = parseGrid(gridInput);
  if (!grid.ok) throw new TypeError(`Invalid grid: ${grid.issues.join('; ')}`);
  const program = parseProgram(programInput);
  if (!program.ok) throw new TypeError(`Invalid program: ${program.issues.join('; ')}`);

  let state = cloneState(grid.value.start);
  const trace: TraceStep[] = [];
  for (const [index, action] of actions(program.value).entries()) {
    const before = cloneState(state);
    if (index >= MAX_EXECUTED_ACTIONS) {
      return { state: cloneState(state), trace, status: 'STEP_LIMIT' };
    }
    const after = apply(before, action.command);
    if (!inside(after, grid.value)) {
      trace.push({
        step: index + 1,
        commandId: action.command.id,
        iteration: action.iteration,
        before,
        after: cloneState(before),
        error: 'OUT_OF_BOUNDS',
      });
      return { state: cloneState(state), trace, status: 'OUT_OF_BOUNDS' };
    }
    state = after;
    trace.push({
      step: index + 1,
      commandId: action.command.id,
      iteration: action.iteration,
      before,
      after: cloneState(after),
      error: null,
    });
  }
  return { state: cloneState(state), trace, status: 'complete' };
}
