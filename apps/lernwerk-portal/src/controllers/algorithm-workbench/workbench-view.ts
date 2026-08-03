import type { Algorithm, Command } from '@ium/ium-5-core-05';

const commandLabels: Readonly<Record<Exclude<Command['kind'], 'repeat'>, string>> = {
  move: 'Gehe',
  'turn-left': 'Links drehen',
  'turn-right': 'Rechts drehen',
  'pick-up': 'Nimm auf',
  drop: 'Lege ab',
};

function control(label: string, action: string, index: number): HTMLButtonElement {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = label;
  button.dataset.commandAction = action;
  button.dataset.commandIndex = String(index);
  return button;
}

function commandDescription(command: Command): string {
  if (command.kind !== 'repeat') {
    return commandLabels[command.kind];
  }
  const body = command.body.map((entry) => commandLabels[entry.kind]).join(', ');
  return `Wiederhole ${command.count} mal: ${body}`;
}

export function renderAlgorithm(
  list: HTMLOListElement,
  algorithm: Algorithm,
): void {
  list.replaceChildren();
  if (algorithm.length === 0) {
    const empty = document.createElement('li');
    empty.textContent = 'Noch keine Anweisung eingefügt.';
    empty.dataset.emptyAlgorithm = '';
    list.append(empty);
    return;
  }

  algorithm.forEach((command, index) => {
    const item = document.createElement('li');
    item.dataset.commandId = command.id;
    const description = document.createElement('span');
    description.textContent = `Befehl ${index + 1}: ${commandDescription(command)}`;
    item.append(description);

    if (command.kind === 'repeat') {
      const field = document.createElement('div');
      field.className = 'field';
      const inputId = `repeat-count-${command.id}`;
      const label = document.createElement('label');
      label.htmlFor = inputId;
      label.textContent = 'Wiederholungszahl';
      const input = document.createElement('input');
      input.id = inputId;
      input.type = 'number';
      input.min = '1';
      input.max = '9';
      input.value = String(command.count);
      input.inputMode = 'numeric';
      input.dataset.repeatIndex = String(index);
      field.append(label, input);
      item.append(field);
    }

    const actions = document.createElement('div');
    actions.className = 'actions';
    actions.append(
      control(`Befehl ${index + 1} nach oben`, 'up', index),
      control(`Befehl ${index + 1} nach unten`, 'down', index),
      control(`Befehl ${index + 1} löschen`, 'remove', index),
    );
    item.append(actions);
    list.append(item);
  });
}

export function setExecutionEnabled(root: ParentNode, enabled: boolean): void {
  for (const selector of ['[data-run-step]', '[data-run-all]']) {
    const button = root.querySelector<HTMLButtonElement>(selector);
    if (button) {
      button.disabled = !enabled;
    }
  }
}

export function setPredictionStatus(root: ParentNode, message: string): void {
  const status = root.querySelector<HTMLElement>('[data-prediction-status]');
  if (status) {
    status.textContent = message;
  }
}
