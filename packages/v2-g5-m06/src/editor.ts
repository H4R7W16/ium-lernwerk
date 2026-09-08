import type { Basic, Program, Repeat } from './model.js';
import { parseProgram } from './validation.js';

function valid(program: unknown): Program {
  const parsed = parseProgram(program);
  if (!parsed.ok) throw new TypeError(`Invalid program: ${parsed.issues.join('; ')}`);
  return parsed.value;
}

function insertionIndex(index: number, length: number): void {
  if (!Number.isInteger(index) || index < 0 || index > length) {
    throw new RangeError(`Invalid insertion index: ${index}`);
  }
}

function movementIndex(index: number, length: number): void {
  if (!Number.isInteger(index) || index < 0 || index >= length) {
    throw new RangeError(`Invalid movement index: ${index}`);
  }
}

export function insert(
  programInput: Program,
  index: number,
  command: Basic | Repeat,
): Program {
  const program = valid(programInput);
  insertionIndex(index, program.length);
  return valid([...program.slice(0, index), command, ...program.slice(index)]);
}

export function remove(programInput: Program, id: string): Program {
  const program = valid(programInput);
  const index = program.findIndex((command) => command.id === id);
  if (index < 0) throw new RangeError(`Unknown command identifier: ${id}`);
  return valid([...program.slice(0, index), ...program.slice(index + 1)]);
}

export function move(programInput: Program, id: string, index: number): Program {
  const program = valid(programInput);
  movementIndex(index, program.length);
  const current = program.findIndex((command) => command.id === id);
  if (current < 0) throw new RangeError(`Unknown command identifier: ${id}`);
  const command = program[current]!;
  const without = [...program.slice(0, current), ...program.slice(current + 1)];
  without.splice(index, 0, command);
  return valid(without);
}
