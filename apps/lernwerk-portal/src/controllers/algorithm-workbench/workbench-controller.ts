import {
  beginExecution,
  createInitialPayload,
  finishExecution,
  insertCommand,
  missionSucceeded,
  moveCommand,
  nextCommandId,
  removeCommand,
  replaceRepeat,
  stepExecution,
  type Algorithm,
  type BasicCommandKind,
  type Command,
  type Direction,
  type EvidenceTrace,
  type ExecutionSession,
  type Prediction,
  type WorkbenchPayload,
  type WorkbenchResources,
  type WorkbenchScenarioId,
} from '@ium/ium-5-core-05';
import {
  renderAlgorithm,
  renderExecution,
  renderScenarioDescription,
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

function setText(root: ParentNode, selector: string, value: string): void {
  const element = root.querySelector<HTMLElement>(selector);
  if (element) {
    element.textContent = value;
  }
}

function setHidden(root: ParentNode, selector: string, hidden: boolean): void {
  const element = root.querySelector<HTMLElement>(selector);
  if (element) {
    element.hidden = hidden;
  }
}

function resetExecutionSurface(root: ParentNode): void {
  setText(root, '[data-execution-result]', 'Noch keine Ausführung.');
  setText(root, '[data-execution-live]', '');
  setText(root, '[data-current-command]', 'Noch nicht gestartet');
  setText(root, '[data-current-position]', '–');
  setText(root, '[data-current-direction]', '–');
  setText(root, '[data-current-carrying]', '–');
  setText(root, '[data-current-loop]', '–');
  const body = root.querySelector<HTMLTableSectionElement>('[data-trace-table] tbody');
  if (body) {
    body.replaceChildren();
    const row = body.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 6;
    cell.textContent = 'Noch keine Spur vorhanden.';
  }
  const evidence = root.querySelector<HTMLElement>('[data-evidence-options]');
  if (evidence) {
    evidence.textContent = 'Noch keine Spur zur Auswahl.';
  }
  setHidden(root, '[data-strategy-hint]', true);
  setHidden(root, '[data-strategy-content]', true);
  setHidden(root, '[data-full-example]', true);
}

export async function connectAlgorithmWorkbench(
  parent: ParentNode = document,
): Promise<void> {
  const root = parent.querySelector<HTMLElement>('[data-algorithm-workbench]');
  if (!root || root.dataset.connected === 'true') {
    return;
  }
  root.dataset.connected = 'true';
  const resources = readResources(root);
  const byScenarioId = new Map(
    resources.scenarios.map((entry) => [entry.scenario.id, entry]),
  );
  const requireScenario = (scenarioId: WorkbenchScenarioId): WorkbenchResources['scenarios'][number] => {
    const resource = byScenarioId.get(scenarioId);
    if (!resource) {
      throw new Error(`Unknown scenario: ${scenarioId}`);
    }
    return resource;
  };
  let activeResource = requireScenario('worked-sequence');

  let payload: WorkbenchPayload = createInitialPayload();
  let algorithm: Algorithm = payload.initialAlgorithm;
  let confirmedAlgorithm = '';
  let session: ExecutionSession | null = null;
  let editorValid = true;
  let usingStandardRepairCase = false;
  const list = requiredElement<HTMLOListElement>(root, '[data-algorithm-list]');

  const refreshGate = (): void => {
    const enabled = editorValid
      && payload.prediction !== null
      && confirmedAlgorithm === JSON.stringify(algorithm);
    setExecutionEnabled(root, enabled);
  };

  const changeAlgorithm = (next: Algorithm): void => {
    algorithm = next;
    const revising = payload.evidenceTrace !== null && payload.repairHypothesis.length > 0;
    payload = revising
      ? { ...payload, revisedAlgorithm: next, prediction: null }
      : { ...payload, initialAlgorithm: next, prediction: null };
    confirmedAlgorithm = '';
    session = null;
    editorValid = true;
    renderAlgorithm(list, algorithm);
    setPredictionStatus(root, '');
    const error = root.querySelector<HTMLElement>('[data-editor-error]');
    if (error) {
      error.hidden = true;
      error.textContent = '';
    }
    resetExecutionSurface(root);
    refreshGate();
    dispatch(root, 'ium5:algorithm-change', { algorithm });
  };

  const loadScenario = (scenarioId: WorkbenchScenarioId): void => {
    const resource = requireScenario(scenarioId);
    activeResource = resource;
    algorithm = structuredClone(resource.starterAlgorithm ?? []);
    payload = {
      ...createInitialPayload(),
      scenarioId,
      initialAlgorithm: algorithm,
    };
    confirmedAlgorithm = '';
    session = null;
    editorValid = true;
    usingStandardRepairCase = false;
    setHidden(root, '[data-preserved-product]', true);
    setText(root, '[data-preserved-draft]', '');
    setText(root, '[data-repair-status]', '');
    setText(root, '[data-loop-status]', '');
    requiredElement<HTMLTextAreaElement>(root, '#repair-hypothesis').value = '';
    requiredElement<HTMLTextAreaElement>(root, '#loop-decision').value = '';
    renderScenarioDescription(root, resource.scenario);
    renderAlgorithm(list, algorithm);
    setPredictionStatus(root, '');
    resetExecutionSurface(root);
    refreshGate();
  };

  const openStandardRepairCase = (): void => {
    const resource = requireScenario('repair-standard');
    const preservedDraft = list.innerText;
    activeResource = resource;
    algorithm = structuredClone(resource.starterAlgorithm ?? []);
    payload = {
      ...payload,
      scenarioId: 'repair-standard',
      prediction: null,
      evidenceTrace: null,
      repairSource: null,
      repairHypothesis: '',
      revisedAlgorithm: null,
    };
    confirmedAlgorithm = '';
    session = null;
    editorValid = true;
    usingStandardRepairCase = true;
    setText(root, '[data-preserved-draft]', preservedDraft);
    setHidden(root, '[data-preserved-product]', false);
    renderScenarioDescription(root, resource.scenario);
    renderAlgorithm(list, algorithm);
    resetExecutionSurface(root);
    setPredictionStatus(root, 'Standardfall geöffnet – neue Vorhersage erforderlich.');
    setText(
      root,
      '[data-repair-status]',
      'Eigener Entwurf erfüllt den Auftrag. Er bleibt unverändert; bearbeite nun den standardisierten Reparaturfall.',
    );
    refreshGate();
  };

  const showExecution = (next: ExecutionSession): void => {
    session = next;
    const succeeded = missionSucceeded(activeResource.scenario, next.state);
    renderExecution(root, next, succeeded, payload.prediction);
    if (next.status === 'complete' && succeeded && !usingStandardRepairCase) {
      openStandardRepairCase();
    }
  };

  const runStep = (): void => {
    if (!editorValid || payload.prediction === null) {
      return;
    }
    const start = session === null || session.status === 'complete' || session.status === 'error'
      ? beginExecution(activeResource.scenario, algorithm)
      : session;
    showExecution(stepExecution(start));
    dispatch(root, 'ium5:run-step', { session });
  };

  const runAll = (): void => {
    if (!editorValid || payload.prediction === null) {
      return;
    }
    const result = finishExecution(beginExecution(activeResource.scenario, algorithm));
    showExecution(result);
    dispatch(root, 'ium5:run-all', { session: result });
  };

  const confirmEvidence = (): void => {
    if (!session) {
      return;
    }
    const selected = root.querySelector<HTMLInputElement>('input[name="evidence-step"]:checked');
    const hypothesis = requiredElement<HTMLTextAreaElement>(root, '#repair-hypothesis').value.trim();
    if (!selected || hypothesis.length === 0 || [...hypothesis].length > 500) {
      setText(
        root,
        '[data-repair-status]',
        'Wähle eine Spurzeile und formuliere eine Hypothese mit höchstens 500 Zeichen.',
      );
      return;
    }
    const entryCount = Number(selected.value);
    const entries = session.trace.slice(0, entryCount);
    const finalState = entries.at(-1)?.after ?? session.state;
    const evidenceTrace: EvidenceTrace = {
      scenarioId: payload.scenarioId,
      entries,
      finalState,
      missionSucceeded: missionSucceeded(activeResource.scenario, finalState),
    };
    payload = {
      ...payload,
      evidenceTrace,
      repairSource: usingStandardRepairCase ? 'standard-error-case' : 'own-draft',
      repairHypothesis: hypothesis,
    };
    setText(root, '[data-repair-status]', 'Reparaturhypothese gespeichert.');
  };

  const confirmRevision = (): void => {
    if (payload.evidenceTrace === null || payload.repairHypothesis.length === 0) {
      setText(root, '[data-repair-status]', 'Bestätige zuerst Belegspur und Reparaturhypothese.');
      return;
    }
    payload = { ...payload, revisedAlgorithm: structuredClone(algorithm), prediction: null };
    confirmedAlgorithm = '';
    session = null;
    setPredictionStatus(root, 'Revision übernommen – neue Vorhersage erforderlich.');
    resetExecutionSurface(root);
    refreshGate();
    dispatch(root, 'ium5:revision-confirm', { algorithm });
  };

  const confirmLoopDecision = (): void => {
    const decision = requiredElement<HTMLTextAreaElement>(root, '#loop-decision').value.trim();
    if (decision.length === 0 || [...decision].length > 500) {
      setText(
        root,
        '[data-loop-status]',
        'Formuliere eine Begründung mit höchstens 500 Zeichen.',
      );
      return;
    }
    payload = { ...payload, loopDecision: decision };
    setText(root, '[data-loop-status]', 'Schleifenentscheidung gespeichert.');
    dispatch(root, 'ium5:loop-decision-confirm', { loopDecision: decision });
  };

  renderAlgorithm(list, algorithm);
  renderScenarioDescription(root, activeResource.scenario);
  refreshGate();

  root.addEventListener('input', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement) || target.dataset.repeatIndex === undefined) {
      return;
    }
    const index = Number(target.dataset.repeatIndex);
    const count = Number(target.value);
    const error = requiredElement<HTMLElement>(root, '[data-editor-error]');
    if (!Number.isInteger(count) || count < 2 || count > 9) {
      editorValid = false;
      error.hidden = false;
      error.textContent = `Befehl ${index + 1}: Wiederholungszahl muss zwischen 2 und 9 liegen.`;
      setExecutionEnabled(root, false);
      return;
    }
    const command = algorithm[index];
    if (command?.kind !== 'repeat') {
      return;
    }
    changeAlgorithm(replaceRepeat(algorithm, index, { ...command, count }));
  });

  root.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    const scenarioButton = target.closest<HTMLButtonElement>('[data-open-scenario]');
    if (scenarioButton?.dataset.openScenario) {
      loadScenario(scenarioButton.dataset.openScenario as WorkbenchScenarioId);
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
      runStep();
    } else if (target.closest('[data-run-all]')) {
      runAll();
    } else if (target.closest('[data-repair-confirm]')) {
      confirmEvidence();
    } else if (target.closest('[data-revision-confirm]')) {
      confirmRevision();
    } else if (target.closest('[data-loop-confirm]')) {
      confirmLoopDecision();
    } else if (target.closest('[data-strategy-hint]')) {
      setHidden(root, '[data-strategy-content]', false);
    } else if (target.closest('[data-full-example-open]')) {
      setHidden(root, '[data-full-example]', false);
      const reference = activeResource.referenceAlgorithm.map((entry) => entry.kind).join(', ');
      setText(root, '[data-full-example-text]', reference);
    }
  });
}
