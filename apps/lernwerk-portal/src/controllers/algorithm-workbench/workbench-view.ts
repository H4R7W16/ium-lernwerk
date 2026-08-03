import type {
  Algorithm,
  Command,
  ExecutionSession,
  Prediction,
  Scenario,
  TraceEntry,
} from '@ium/ium-5-core-05';

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
  const empty = list.parentElement?.querySelector<HTMLElement>('[data-empty-algorithm]');
  if (empty) {
    empty.hidden = algorithm.length > 0;
  }
  if (algorithm.length === 0) {
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

function coordinate(column: number, row: number): string {
  return `${String.fromCharCode(64 + column)}${row}`;
}

function stateText(entry: TraceEntry['before']): string {
  return `${coordinate(entry.position.column, entry.position.row)}, Blick ${entry.direction}, ${
    entry.carrying ? 'trägt das Gut' : 'trägt kein Gut'
  }`;
}

const errorLabels: Readonly<Record<NonNullable<TraceEntry['error']>, string>> = {
  OBSTACLE: 'Hindernis im nächsten Feld',
  OUT_OF_BOUNDS: 'Rastergrenze überschritten',
  INVALID_PICK_UP: 'Aufnahme ungültig',
  INVALID_DROP: 'Ablage ungültig',
  INVALID_REPEAT: 'Wiederholungszahl ungültig',
  STEP_LIMIT: 'Schrittgrenze erreicht',
};

export function renderScenarioDescription(root: ParentNode, scenario: Scenario): void {
  const description = root.querySelector<HTMLElement>('[data-scene-description]');
  if (description) {
    const obstacles = scenario.obstacles.length === 0
      ? 'keine Hindernisse'
      : `Hindernisse bei ${scenario.obstacles.map((entry) =>
        coordinate(entry.column, entry.row)).join(', ')}`;
    description.textContent = `Raster ${scenario.width} mal ${scenario.height}. Start ${
      coordinate(scenario.start.position.column, scenario.start.position.row)
    }, Blickrichtung ${scenario.start.direction}. Gut ${
      coordinate(scenario.itemPosition.column, scenario.itemPosition.row)
    }, Ziel ${coordinate(scenario.targetPosition.column, scenario.targetPosition.row)}, ${obstacles}.`;
  }
  const active = root.querySelector<HTMLElement>('[data-active-scenario]');
  if (active) {
    active.textContent = `${scenario.title} · ${scenario.id}`;
  }
}

function renderTrace(root: ParentNode, session: ExecutionSession): void {
  const table = root.querySelector<HTMLTableElement>('[data-trace-table]');
  const body = table?.tBodies[0];
  if (!body) {
    return;
  }
  body.replaceChildren();
  if (session.trace.length === 0) {
    const row = body.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 6;
    cell.textContent = 'Noch keine Spur vorhanden.';
    return;
  }
  for (const entry of session.trace) {
    const row = body.insertRow();
    const values = [
      String(entry.step),
      entry.sourceCommandId,
      entry.loop === null ? '–' : `${entry.loop.iteration} von ${entry.loop.total}`,
      stateText(entry.before),
      stateText(entry.after),
      entry.error === null ? 'ausgeführt' : errorLabels[entry.error],
    ];
    for (const value of values) {
      const cell = row.insertCell();
      cell.textContent = value;
    }
  }
}

function renderEvidenceOptions(root: ParentNode, session: ExecutionSession): void {
  const container = root.querySelector<HTMLElement>('[data-evidence-options]');
  if (!container) {
    return;
  }
  container.replaceChildren();
  for (const entry of session.trace) {
    const wrapper = document.createElement('span');
    wrapper.className = 'evidence-option';
    const id = `evidence-step-${entry.step}`;
    const input = document.createElement('input');
    input.type = 'radio';
    input.name = 'evidence-step';
    input.id = id;
    input.value = String(entry.step);
    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = `Erster abweichender Schritt ${entry.step}`;
    wrapper.append(input, label);
    container.append(wrapper);
  }
}

function setText(root: ParentNode, selector: string, value: string): void {
  const element = root.querySelector<HTMLElement>(selector);
  if (element) {
    element.textContent = value;
  }
}

export function renderExecution(
  root: ParentNode,
  session: ExecutionSession,
  succeeded: boolean,
  prediction: Prediction | null,
): void {
  const last = session.trace.at(-1);
  const current = last?.after ?? session.state;
  setText(root, '[data-current-command]', last?.sourceCommandId ?? 'Noch nicht gestartet');
  setText(root, '[data-current-position]', coordinate(current.position.column, current.position.row));
  setText(root, '[data-current-direction]', current.direction);
  setText(root, '[data-current-carrying]', current.carrying ? 'trägt das Gut' : 'trägt kein Gut');
  setText(
    root,
    '[data-current-loop]',
    last?.loop === null || last?.loop === undefined
      ? 'keine'
      : `${last.loop.iteration} von ${last.loop.total}`,
  );

  let result = session.status === 'complete'
    ? (succeeded ? 'Auftrag erfüllt.' : 'Auftrag noch nicht erfüllt.')
    : 'Ausführung läuft.';
  if (session.status === 'error' && last?.error) {
    result = `Auftrag noch nicht erfüllt. Schritt ${last.step}: ${errorLabels[last.error]}. Position ${
      coordinate(last.before.position.column, last.before.position.row)
    }, Blickrichtung ${last.before.direction}, ${
      last.before.carrying ? 'Gut wird getragen' : 'Gut wird nicht getragen'
    }.`;
  }
  if (prediction && (session.status === 'complete' || session.status === 'error')) {
    result += ` Vorhersage: ${coordinate(
      prediction.position.column,
      prediction.position.row,
    )}, Blickrichtung ${prediction.direction}, Auftrag ${prediction.success}.`;
  }
  setText(root, '[data-execution-result]', result);
  setText(root, '[data-execution-live]', result);
  renderTrace(root, session);
  renderEvidenceOptions(root, session);

  const strategy = root.querySelector<HTMLButtonElement>('[data-strategy-hint]');
  if (strategy) {
    strategy.hidden = session.status !== 'complete' && session.status !== 'error';
  }
}
