import type { Basic, Program } from '@ium/v2-g5-m06';
import { parseProgram } from '@ium/v2-g5-m06';

export type DiagramCommandKind = Basic['kind'];

export function appendDiagramCommand(
  program: Program,
  command: Basic,
): Program {
  const next = [...program, command];
  const parsed = parseProgram(next);
  if (!parsed.ok) throw new TypeError(parsed.issues.join('; '));
  return parsed.value;
}

export function diagramText(program: Program): string {
  const label = { move: 'vor', 'turn-left': 'links', 'turn-right': 'rechts' } as const;
  return program.flatMap((command) => command.kind === 'repeat'
    ? [`wiederhole ${command.count}`, ...command.body.map((entry) => `  ${label[entry.kind]}`)]
    : [label[command.kind]]).join('\n');
}
