import type {
  Algorithm,
  Command,
  RepeatCommand,
} from './model.js';
import { parseAlgorithm } from './validation.js';

function cloneCommand(command: Command): Command {
  if (command.kind !== 'repeat') {
    return { id: command.id, kind: command.kind };
  }
  return {
    id: command.id,
    kind: 'repeat',
    count: command.count,
    body: command.body.map((entry) => ({ id: entry.id, kind: entry.kind })),
  };
}

function cloneAlgorithm(algorithm: Algorithm): Command[] {
  return algorithm.map(cloneCommand);
}

function validAlgorithm(value: readonly Command[]): Algorithm {
  const parsed = parseAlgorithm(value);
  if (!parsed.ok) {
    throw new TypeError(`Invalid algorithm edit: ${JSON.stringify(parsed.issues)}`);
  }
  return parsed.value;
}

function assertIndex(index: number, length: number, allowEnd = false): void {
  const upperBound = allowEnd ? length : length - 1;
  if (!Number.isInteger(index) || index < 0 || index > upperBound) {
    throw new RangeError(`Command index ${index} is outside 0..${upperBound}`);
  }
}

export function insertCommand(
  algorithm: Algorithm,
  index: number,
  command: Command,
): Algorithm {
  assertIndex(index, algorithm.length, true);
  const next = cloneAlgorithm(algorithm);
  next.splice(index, 0, cloneCommand(command));
  return validAlgorithm(next);
}

export function moveCommand(
  algorithm: Algorithm,
  index: number,
  delta: -1 | 1,
): Algorithm {
  assertIndex(index, algorithm.length);
  if (delta !== -1 && delta !== 1) {
    throw new RangeError('Command move delta must be -1 or 1');
  }
  const next = cloneAlgorithm(algorithm);
  const target = index + delta;
  if (target < 0 || target >= next.length) {
    return validAlgorithm(next);
  }
  const [command] = next.splice(index, 1);
  if (command === undefined) {
    throw new RangeError(`No command exists at index ${index}`);
  }
  next.splice(target, 0, command);
  return validAlgorithm(next);
}

export function removeCommand(
  algorithm: Algorithm,
  index: number,
): Algorithm {
  assertIndex(index, algorithm.length);
  const next = cloneAlgorithm(algorithm);
  next.splice(index, 1);
  return validAlgorithm(next);
}

export function replaceRepeat(
  algorithm: Algorithm,
  index: number,
  replacement: RepeatCommand,
): Algorithm {
  assertIndex(index, algorithm.length);
  if (algorithm[index]?.kind !== 'repeat') {
    throw new TypeError(`Command at index ${index} is not a repeat block`);
  }
  const next = cloneAlgorithm(algorithm);
  next[index] = cloneCommand(replacement);
  return validAlgorithm(next);
}

export function nextCommandId(algorithm: Algorithm): string {
  let maximum = 0;
  for (const command of algorithm) {
    const identifiers = command.kind === 'repeat'
      ? [command.id, ...command.body.map((entry) => entry.id)]
      : [command.id];
    for (const identifier of identifiers) {
      const match = /^cmd-([1-9][0-9]*)$/.exec(identifier);
      if (match?.[1] !== undefined) {
        maximum = Math.max(maximum, Number(match[1]));
      }
    }
  }
  return `cmd-${maximum + 1}`;
}
