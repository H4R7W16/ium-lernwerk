import type {
  Basic,
  Direction,
  Grid,
  ParseResult,
  Position,
  Program,
  State,
} from './model.js';

type UnknownRecord = Readonly<Record<string, unknown>>;

const commandIdPattern = /^cmd-[1-9][0-9]*$/;
const basicKinds = new Set<Basic['kind']>(['move', 'turn-left', 'turn-right']);
const directions = new Set<Direction>(['north', 'east', 'south', 'west']);

export function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export function hasExactKeys(value: UnknownRecord, keys: readonly string[]): boolean {
  const expected = new Set(keys);
  const actual = Object.keys(value);
  return actual.length === expected.size && actual.every((key) => expected.has(key));
}

export function failure<T = never>(path: string, message: string): ParseResult<T> {
  return { ok: false, issues: [`${path}: ${message}`] };
}

function parseId(value: unknown, path: string): ParseResult<string> {
  return typeof value === 'string' && commandIdPattern.test(value)
    ? { ok: true, value }
    : failure(path, 'must match ^cmd-[1-9][0-9]*$');
}

function parseBasic(value: unknown, path: string): ParseResult<Basic> {
  if (!isRecord(value) || !hasExactKeys(value, ['id', 'kind'])) {
    return failure(path, 'must contain exactly id and kind');
  }
  const id = parseId(value.id, `${path}.id`);
  if (!id.ok) return id;
  if (typeof value.kind !== 'string' || !basicKinds.has(value.kind as Basic['kind'])) {
    return failure(`${path}.kind`, 'must be move, turn-left or turn-right');
  }
  return { ok: true, value: { id: id.value, kind: value.kind as Basic['kind'] } };
}

export function parseProgram(input: unknown): ParseResult<Program> {
  if (!Array.isArray(input)) return failure('$', 'must be an array');
  const program: (Basic | Readonly<{
    id: string;
    kind: 'repeat';
    count: number;
    body: readonly Basic[];
  }>)[] = [];
  const identifiers = new Set<string>();

  for (const [index, candidate] of input.entries()) {
    const path = `$[${index}]`;
    if (!isRecord(candidate)) return failure(path, 'must be a command object');
    if (candidate.kind !== 'repeat') {
      const basic = parseBasic(candidate, path);
      if (!basic.ok) return basic;
      if (identifiers.has(basic.value.id)) {
        return failure(`${path}.id`, `duplicate command identifier: ${basic.value.id}`);
      }
      identifiers.add(basic.value.id);
      program.push(basic.value);
      continue;
    }

    if (!hasExactKeys(candidate, ['id', 'kind', 'count', 'body'])) {
      return failure(path, 'repeat must contain exactly id, kind, count and body');
    }
    const id = parseId(candidate.id, `${path}.id`);
    if (!id.ok) return id;
    if (identifiers.has(id.value)) {
      return failure(`${path}.id`, `duplicate command identifier: ${id.value}`);
    }
    if (!Number.isInteger(candidate.count)
      || (candidate.count as number) < 2
      || (candidate.count as number) > 9) {
      return failure(`${path}.count`, 'must be an integer from 2 to 9');
    }
    if (!Array.isArray(candidate.body)
      || candidate.body.length < 1
      || candidate.body.length > 5) {
      return failure(`${path}.body`, 'must contain one to five basic commands');
    }
    identifiers.add(id.value);
    const body: Basic[] = [];
    for (const [bodyIndex, bodyCandidate] of candidate.body.entries()) {
      const parsed = parseBasic(bodyCandidate, `${path}.body[${bodyIndex}]`);
      if (!parsed.ok) return parsed;
      if (identifiers.has(parsed.value.id)) {
        return failure(
          `${path}.body[${bodyIndex}].id`,
          `duplicate command identifier: ${parsed.value.id}`,
        );
      }
      identifiers.add(parsed.value.id);
      body.push(parsed.value);
    }
    program.push({
      id: id.value,
      kind: 'repeat',
      count: candidate.count as number,
      body,
    });
  }
  return { ok: true, value: program };
}

export function parsePosition(input: unknown, path: string): ParseResult<Position> {
  if (!isRecord(input) || !hasExactKeys(input, ['column', 'row'])) {
    return failure(path, 'must contain exactly column and row');
  }
  if (!Number.isInteger(input.column) || (input.column as number) < 1
    || !Number.isInteger(input.row) || (input.row as number) < 1) {
    return failure(path, 'coordinates must be positive integers');
  }
  return {
    ok: true,
    value: { column: input.column as number, row: input.row as number },
  };
}

export function parseState(input: unknown, path: string): ParseResult<State> {
  if (!isRecord(input) || !hasExactKeys(input, ['position', 'direction'])) {
    return failure(path, 'must contain exactly position and direction');
  }
  const position = parsePosition(input.position, `${path}.position`);
  if (!position.ok) return position;
  if (typeof input.direction !== 'string'
    || !directions.has(input.direction as Direction)) {
    return failure(`${path}.direction`, 'must be north, east, south or west');
  }
  return { ok: true, value: { position: position.value, direction: input.direction as Direction } };
}

export function parseGrid(input: unknown): ParseResult<Grid> {
  if (!isRecord(input) || !hasExactKeys(input, ['width', 'height', 'start'])) {
    return failure('$grid', 'must contain exactly width, height and start');
  }
  if (!Number.isInteger(input.width) || (input.width as number) < 1
    || !Number.isInteger(input.height) || (input.height as number) < 1) {
    return failure('$grid', 'width and height must be positive integers');
  }
  const start = parseState(input.start, '$grid.start');
  if (!start.ok) return start;
  if (start.value.position.column > (input.width as number)
    || start.value.position.row > (input.height as number)) {
    return failure('$grid.start.position', 'must lie inside the grid');
  }
  return {
    ok: true,
    value: { width: input.width as number, height: input.height as number, start: start.value },
  };
}

export function executedActionCount(program: Program): number {
  return program.reduce((total, command) => total + (
    command.kind === 'repeat' ? command.count * command.body.length : 1
  ), 0);
}

export function programSemanticsEqual(left: Program, right: Program): boolean {
  if (left.length !== right.length) return false;
  return left.every((leftCommand, index) => {
    const rightCommand = right[index];
    if (rightCommand === undefined || leftCommand.kind !== rightCommand.kind) return false;
    if (leftCommand.kind !== 'repeat' || rightCommand.kind !== 'repeat') return true;
    return leftCommand.count === rightCommand.count
      && leftCommand.body.length === rightCommand.body.length
      && leftCommand.body.every((entry, bodyIndex) =>
        entry.kind === rightCommand.body[bodyIndex]?.kind);
  });
}
