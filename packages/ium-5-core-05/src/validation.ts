import type {
  Algorithm,
  BasicCommand,
  BasicCommandKind,
  Command,
  Direction,
  Position,
  Scenario,
} from './model.js';

export type ParseIssue = Readonly<{ path: string; message: string }>;
export type ParseResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly ParseIssue[] }>;

type UnknownRecord = Readonly<Record<string, unknown>>;

const basicCommandKinds = new Set<BasicCommandKind>([
  'move',
  'turn-left',
  'turn-right',
  'pick-up',
  'drop',
]);
const directions = new Set<Direction>(['north', 'east', 'south', 'west']);
const commandIdPattern = /^cmd-[1-9][0-9]*$/;
const scenarioIdPattern = /^[a-z][a-z0-9-]*$/;

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function hasExactKeys(value: UnknownRecord, keys: readonly string[]): boolean {
  const expected = new Set(keys);
  const actual = Object.keys(value);
  return actual.length === expected.size && actual.every((key) => expected.has(key));
}

function issue(path: string, message: string): ParseResult<never> {
  return { ok: false, issues: [{ path, message }] };
}

function parseCommandId(value: unknown, path: string): ParseResult<string> {
  if (typeof value !== 'string' || !commandIdPattern.test(value)) {
    return issue(path, 'must match ^cmd-[1-9][0-9]*$');
  }
  return { ok: true, value };
}

function parseBasicCommand(value: unknown, path: string): ParseResult<BasicCommand> {
  if (!isRecord(value) || !hasExactKeys(value, ['id', 'kind'])) {
    return issue(path, 'must contain exactly id and kind');
  }
  const id = parseCommandId(value.id, `${path}.id`);
  if (!id.ok) {
    return id;
  }
  if (typeof value.kind !== 'string' || !basicCommandKinds.has(value.kind as BasicCommandKind)) {
    return issue(`${path}.kind`, 'must be an approved basic command');
  }
  return {
    ok: true,
    value: { id: id.value, kind: value.kind as BasicCommandKind },
  };
}

function parseCommand(value: unknown, path: string): ParseResult<Command> {
  if (!isRecord(value)) {
    return issue(path, 'must be a command object');
  }
  if (value.kind !== 'repeat') {
    return parseBasicCommand(value, path);
  }
  if (!hasExactKeys(value, ['id', 'kind', 'count', 'body'])) {
    return issue(path, 'repeat must contain exactly id, kind, count and body');
  }
  const id = parseCommandId(value.id, `${path}.id`);
  if (!id.ok) {
    return id;
  }
  if (!Number.isInteger(value.count) || (value.count as number) < 2 || (value.count as number) > 9) {
    return issue(`${path}.count`, 'must be an integer from 2 to 9');
  }
  if (!Array.isArray(value.body) || value.body.length < 1 || value.body.length > 4) {
    return issue(`${path}.body`, 'must contain one to four basic commands');
  }
  const body: BasicCommand[] = [];
  for (const [index, candidate] of value.body.entries()) {
    const command = parseBasicCommand(candidate, `${path}.body[${index}]`);
    if (!command.ok) {
      return command;
    }
    body.push(command.value);
  }
  return {
    ok: true,
    value: {
      id: id.value,
      kind: 'repeat',
      count: value.count as number,
      body,
    },
  };
}

export function parseAlgorithm(value: unknown): ParseResult<Algorithm> {
  if (!Array.isArray(value)) {
    return issue('$', 'must be an array');
  }
  const algorithm: Command[] = [];
  const identifiers = new Set<string>();
  for (const [index, candidate] of value.entries()) {
    const command = parseCommand(candidate, `$[${index}]`);
    if (!command.ok) {
      return command;
    }
    const commandIds = command.value.kind === 'repeat'
      ? [command.value.id, ...command.value.body.map((entry) => entry.id)]
      : [command.value.id];
    for (const id of commandIds) {
      if (identifiers.has(id)) {
        return issue(`$[${index}].id`, `duplicate command identifier: ${id}`);
      }
      identifiers.add(id);
    }
    algorithm.push(command.value);
  }
  return { ok: true, value: algorithm };
}

function parseDimension(value: unknown, path: string): ParseResult<number> {
  if (!Number.isInteger(value) || (value as number) < 1 || (value as number) > 6) {
    return issue(path, 'must be an integer from 1 to 6');
  }
  return { ok: true, value: value as number };
}

function parsePosition(
  value: unknown,
  path: string,
  width: number,
  height: number,
): ParseResult<Position> {
  if (!isRecord(value) || !hasExactKeys(value, ['column', 'row'])) {
    return issue(path, 'must contain exactly column and row');
  }
  if (
    !Number.isInteger(value.column)
    || !Number.isInteger(value.row)
    || (value.column as number) < 1
    || (value.column as number) > width
    || (value.row as number) < 1
    || (value.row as number) > height
  ) {
    return issue(path, 'must be an integer position inside the grid');
  }
  return {
    ok: true,
    value: { column: value.column as number, row: value.row as number },
  };
}

function positionKey(position: Position): string {
  return `${position.column}:${position.row}`;
}

export function parseScenario(value: unknown): ParseResult<Scenario> {
  if (!isRecord(value) || !hasExactKeys(value, [
    'id',
    'title',
    'width',
    'height',
    'start',
    'itemPosition',
    'targetPosition',
    'obstacles',
  ])) {
    return issue('$', 'must contain exactly the approved scenario fields');
  }
  if (typeof value.id !== 'string' || !scenarioIdPattern.test(value.id)) {
    return issue('$.id', 'must be a lowercase kebab-case identifier');
  }
  if (typeof value.title !== 'string' || value.title.trim().length === 0) {
    return issue('$.title', 'must be a non-empty string');
  }
  const width = parseDimension(value.width, '$.width');
  if (!width.ok) {
    return width;
  }
  const height = parseDimension(value.height, '$.height');
  if (!height.ok) {
    return height;
  }
  if (!isRecord(value.start) || !hasExactKeys(value.start, [
    'position',
    'direction',
    'carrying',
  ])) {
    return issue('$.start', 'must contain exactly position, direction and carrying');
  }
  const startPosition = parsePosition(
    value.start.position,
    '$.start.position',
    width.value,
    height.value,
  );
  if (!startPosition.ok) {
    return startPosition;
  }
  if (
    typeof value.start.direction !== 'string'
    || !directions.has(value.start.direction as Direction)
  ) {
    return issue('$.start.direction', 'must be an approved direction');
  }
  if (value.start.carrying !== false) {
    return issue('$.start.carrying', 'must be false');
  }
  const itemPosition = parsePosition(
    value.itemPosition,
    '$.itemPosition',
    width.value,
    height.value,
  );
  if (!itemPosition.ok) {
    return itemPosition;
  }
  const targetPosition = parsePosition(
    value.targetPosition,
    '$.targetPosition',
    width.value,
    height.value,
  );
  if (!targetPosition.ok) {
    return targetPosition;
  }
  if (!Array.isArray(value.obstacles)) {
    return issue('$.obstacles', 'must be an array');
  }
  const obstacles: Position[] = [];
  const obstacleKeys = new Set<string>();
  for (const [index, candidate] of value.obstacles.entries()) {
    const obstacle = parsePosition(
      candidate,
      `$.obstacles[${index}]`,
      width.value,
      height.value,
    );
    if (!obstacle.ok) {
      return obstacle;
    }
    const key = positionKey(obstacle.value);
    if (obstacleKeys.has(key)) {
      return issue(`$.obstacles[${index}]`, 'must not duplicate an obstacle');
    }
    obstacleKeys.add(key);
    obstacles.push(obstacle.value);
  }
  for (const [path, position] of [
    ['$.start.position', startPosition.value],
    ['$.itemPosition', itemPosition.value],
    ['$.targetPosition', targetPosition.value],
  ] as const) {
    if (obstacleKeys.has(positionKey(position))) {
      return issue(path, 'must not overlap an obstacle');
    }
  }
  return {
    ok: true,
    value: {
      id: value.id,
      title: value.title,
      width: width.value,
      height: height.value,
      start: {
        position: startPosition.value,
        direction: value.start.direction as Direction,
        carrying: false,
      },
      itemPosition: itemPosition.value,
      targetPosition: targetPosition.value,
      obstacles,
    },
  };
}
