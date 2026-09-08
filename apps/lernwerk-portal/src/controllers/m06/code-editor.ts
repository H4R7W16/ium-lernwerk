import type { Basic, Program } from '@ium/v2-g5-m06';
import { parseProgram } from '@ium/v2-g5-m06';

export function appendCodeCommand(program: Program, command: Basic): Program {
  const next = [...program, command];
  const parsed = parseProgram(next);
  if (!parsed.ok) throw new TypeError(parsed.issues.join('; '));
  return parsed.value;
}

export function replaceCodeProgram(input: unknown): Program {
  const parsed = parseProgram(input);
  if (!parsed.ok) throw new TypeError(parsed.issues.join('; '));
  return parsed.value;
}

export function nextCommandId(program: Program): string {
  const ids = program.flatMap((command) => command.kind === 'repeat'
    ? [command.id, ...command.body.map((entry) => entry.id)]
    : [command.id]);
  const maximum = ids.reduce((value, id) => Math.max(value, Number(id.slice(4)) || 0), 0);
  return `cmd-${maximum + 1}`;
}
