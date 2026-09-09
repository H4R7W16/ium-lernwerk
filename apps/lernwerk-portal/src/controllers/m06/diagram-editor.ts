import type { Basic, Program } from '@ium/v2-g5-m06';
import { parseProgram } from '@ium/v2-g5-m06';

export type DiagramCommandKind = Basic['kind'];

/** Reject form drafts before they can replace a valid dossier program. */
export function validateRepeatCount(field: HTMLInputElement, feedback: HTMLElement): number | null {
  const value = field.valueAsNumber;
  const valid = field.value !== '' && Number.isInteger(value) && value >= 2 && value <= 9;
  field.setAttribute('aria-invalid', String(!valid));
  feedback.textContent = valid ? '' : 'Gib eine ganze Anzahl von 2 bis 9 ein.';
  return valid ? value : null;
}

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

export function renderEditableProgram(root: HTMLElement, program: Program, change: (next: Program) => void): void {
  const signature = JSON.stringify(program);
  if (root.dataset.program === signature) return;
  root.dataset.program = signature;
  root.replaceChildren();
  const marker = (text: string) => {
    const node = document.createElement('p'); node.className = 'm06-flow-marker'; node.textContent = text; return node;
  };
  const label = { move: 'vor', 'turn-left': 'links', 'turn-right': 'rechts' } as const;
  const list = (commands: Program, parent?: number): HTMLOListElement => {
    const ordered = document.createElement('ol');
    commands.forEach((command, index) => {
      const item = document.createElement('li');
      const name = command.kind === 'repeat' ? `wiederhole ${command.count}` : label[command.kind];
      const text = document.createElement('span'); text.textContent = `${index + 1}. ${name}`; item.append(text);
      const update = (next: Program) => {
        if (parent === undefined) change(next);
        else change(program.map((entry, position) => position === parent && entry.kind === 'repeat'
          ? { ...entry, body: next as readonly Basic[] } : entry));
      };
      for (const [action, offset] of [['up', -1], ['down', 1], ['remove', 0]] as const) {
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset[action === 'remove' ? 'removeCommand' : action === 'up' ? 'moveUp' : 'moveDown'] = '';
        const title = action === 'remove' ? 'entfernen' : action === 'up' ? 'nach oben' : 'nach unten';
        button.textContent = title;
        button.setAttribute('aria-label', `${name}, Position ${index + 1} ${title}`);
        const fixed = action === 'remove' ? parent !== undefined && commands.length === 1
          : index + offset < 0 || index + offset >= commands.length;
        button.dataset.fixedDisabled = String(fixed); button.disabled = fixed;
        button.addEventListener('click', () => {
          const next = [...commands];
          if (action === 'remove') next.splice(index, 1);
          else [next[index], next[index + offset]] = [next[index + offset], next[index]];
          update(next);
          root.querySelector<HTMLButtonElement>('button:not(:disabled)')?.focus();
        });
        item.append(button);
      }
      if (command.kind === 'repeat') {
        const frame = document.createElement('fieldset'); frame.className = 'm06-body-frame';
        const legend = document.createElement('legend'); legend.textContent = 'Ganzer Wiederholungskörper';
        const countLabel = document.createElement('label'); countLabel.textContent = 'Anzahl 2 bis 9';
        const count = document.createElement('input'); count.type = 'number'; count.min = '2'; count.max = '9'; count.value = String(command.count);
        const feedback = document.createElement('p');
        feedback.id = `m06-${root.dataset.graphic}-${command.id}-count-error`;
        feedback.setAttribute('role', 'status');
        count.setAttribute('aria-describedby', feedback.id);
        count.addEventListener('change', () => {
          const value = validateRepeatCount(count, feedback);
          if (value === null) return;
          change(program.map((entry, position) => position === index ? { ...command, count: value } : entry));
        });
        countLabel.append(count); frame.append(legend, countLabel, feedback, list(command.body, index), marker('Körperende · zurück zum Körperanfang, bis die Anzahl erreicht ist'));
        item.append(frame);
      }
      ordered.append(item);
    });
    return ordered;
  };
  root.append(marker('Start'), list(program), marker('Ende'));
}
