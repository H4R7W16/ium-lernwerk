import {
  createInitialPayload,
  insertCommand,
  moveCommand,
  nextCommandId,
  removeCommand,
  type Algorithm,
  type BasicCommandKind,
  type Command,
  type Direction,
  type Prediction,
  type WorkbenchPayload,
  type WorkbenchResources,
} from '@ium/ium-5-core-05';
import {
  renderAlgorithm,
  setExecutionEnabled,
  setPredictionStatus,
} from './workbench-view.js';

type WorkbenchBundle = Readonly<{
  content: WorkbenchResources['content'];
  scenarios: WorkbenchResources['scenarios'];
  robotAssetPath: string;
}>;

function requiredElement<T extends Element>(root: ParentNode, selector: string): T {
  const element = root.querySelector<T>(selector);
  if (!element) {
    throw new Error(`Missing workbench element: ${selector}`);
  }
  return element;
}

function readResources(root: ParentNode): WorkbenchBundle {
  const script = requiredElement<HTMLScriptElement>(root, '[data-workbench-resources]');
  return JSON.parse(script.textContent ?? '') as WorkbenchBundle;
}

function numberFromCommandId(identifier: string): number {
  return Number(identifier.slice('cmd-'.length));
}

function nextIdentifier(identifier: string): string {
  return `cmd-${numberFromCommandId(identifier) + 1}`;
}

function basicCommand(kind: BasicCommandKind, algorithm: Algorithm): Command {
  return { id: nextCommandId(algorithm), kind };
}

function commandForPalette(kind: string, algorithm: Algorithm): Command {
  if (kind === 'repeat') {
    const id = nextCommandId(algorithm);
    return {
      id,
      kind: 'repeat',
      count: 2,
      body: [{ id: nextIdentifier(id), kind: 'move' }],
    };
  }
  if (
    kind !== 'move'
    && kind !== 'turn-left'
    && kind !== 'turn-right'
    && kind !== 'pick-up'
    && kind !== 'drop'
  ) {
    throw new TypeError(`Unknown command palette kind: ${kind}`);
  }
  return basicCommand(kind, algorithm);
}

function predictionFromForm(root: ParentNode): Prediction | null {
  const position = requiredElement<HTMLSelectElement>(root, '#prediction-position').value;
  const direction = requiredElement<HTMLSelectElement>(root, '#prediction-direction').value;
  const success = requiredElement<HTMLSelectElement>(root, '#prediction-success').value;
  if (
    !/^[A-F][1-6]$/.test(position)
    || !['north', 'east', 'south', 'west'].includes(direction)
    || !['yes', 'no', 'unsure'].includes(success)
  ) {
    return null;
  }
  return {
    position: {
      column: position.charCodeAt(0) - 64,
      row: Number(position[1]),
    },
    direction: direction as Direction,
    success: success as Prediction['success'],
  };
}

function dispatch(root: Element, name: string, detail: unknown): void {
  root.dispatchEvent(new CustomEvent(name, { bubbles: true, detail }));
}

export async function connectAlgorithmWorkbench(
  parent: ParentNode = document,
): Promise<void> {
  const root = parent.querySelector<HTMLElement>('[data-algorithm-workbench]');
  if (!root || root.dataset.connected === 'true') {
    return;
  }
  root.dataset.connected = 'true';
  readResources(root);

  let payload: WorkbenchPayload = createInitialPayload();
  let algorithm: Algorithm = payload.initialAlgorithm;
  let confirmedAlgorithm = '';
  const list = requiredElement<HTMLOListElement>(root, '[data-algorithm-list]');

  const refreshGate = (): void => {
    const enabled = payload.prediction !== null
      && confirmedAlgorithm === JSON.stringify(algorithm);
    setExecutionEnabled(root, enabled);
  };

  const changeAlgorithm = (next: Algorithm): void => {
    algorithm = next;
    payload = { ...payload, initialAlgorithm: next, prediction: null };
    confirmedAlgorithm = '';
    renderAlgorithm(list, algorithm);
    setPredictionStatus(root, '');
    refreshGate();
    dispatch(root, 'ium5:algorithm-change', { algorithm });
  };

  renderAlgorithm(list, algorithm);
  refreshGate();

  root.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    const insert = target.closest<HTMLButtonElement>('[data-insert-command]');
    if (insert?.dataset.insertCommand) {
      changeAlgorithm(insertCommand(
        algorithm,
        algorithm.length,
        commandForPalette(insert.dataset.insertCommand, algorithm),
      ));
      return;
    }
    const commandControl = target.closest<HTMLButtonElement>('[data-command-action]');
    if (commandControl) {
      const index = Number(commandControl.dataset.commandIndex);
      switch (commandControl.dataset.commandAction) {
        case 'up':
          changeAlgorithm(moveCommand(algorithm, index, -1));
          break;
        case 'down':
          changeAlgorithm(moveCommand(algorithm, index, 1));
          break;
        case 'remove':
          changeAlgorithm(removeCommand(algorithm, index));
          break;
      }
      return;
    }
    if (target.closest('[data-prediction-confirm]')) {
      const prediction = predictionFromForm(root);
      if (prediction === null) {
        setPredictionStatus(root, 'Bitte fülle alle drei Vorhersagefelder aus.');
        return;
      }
      payload = { ...payload, prediction };
      confirmedAlgorithm = JSON.stringify(algorithm);
      setPredictionStatus(root, 'Vorhersage gespeichert – jetzt prüfen');
      refreshGate();
      dispatch(root, 'ium5:prediction-confirm', { prediction });
      return;
    }
    if (target.closest('[data-run-step]')) {
      dispatch(root, 'ium5:run-step', {});
    } else if (target.closest('[data-run-all]')) {
      dispatch(root, 'ium5:run-all', {});
    } else if (target.closest('[data-revision-confirm]')) {
      dispatch(root, 'ium5:revision-confirm', {});
    }
  });
}
