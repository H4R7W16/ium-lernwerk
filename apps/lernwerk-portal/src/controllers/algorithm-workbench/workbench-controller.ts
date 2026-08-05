import {
  beginExecution,
  createInitialPayload,
  finishExecution,
  insertCommand,
  missionSucceeded,
  moveCommand,
  migrateWorkbenchPayloadV1,
  nextCommandId,
  PAYLOAD_SCHEMA_VERSION,
  parseWorkbenchPayload,
  projectPersistentPayload,
  removeCommand,
  replaceRepeat,
  stepExecution,
  type Algorithm,
  type BasicCommandKind,
  type Command,
  type Direction,
  type EvidenceCardPayload,
  type EvidenceTrace,
  type ExecutionSession,
  type LearningPhaseId,
  type Prediction,
  type SelfCheckValue,
  type SystemClassification,
  type TransferCaseId,
  type WorkbenchPayload,
  type WorkbenchResources,
  type WorkbenchScenarioId,
} from '@ium/ium-5-core-05';
import { createStateRepository } from '@ium/local-state';
import type { PlatformError, StorageMode } from '@ium/module-contract';
import { createModuleRuntime } from '@ium/module-runtime';
import { focusActivatedStage } from '@ium/learning-experience/controllers/focus-stage';
import type { FlushRequestDetail } from '../pwa-registration.js';
import { createBrowserExportPort, createWorkspaceId } from './browser-ports.js';
import { deriveIum5ExperienceState } from './experience-adapter.js';
import {
  renderAlgorithm,
  renderEvidenceFeedback,
  renderExperienceEntry,
  renderExecution,
  renderExperienceState,
  renderRevisionComparison,
  renderScenarioDescription,
  setExecutionEnabled,
  setPredictionStatus,
} from './workbench-view.js';

type WorkbenchBundle = Readonly<{
  content: WorkbenchResources['content'];
  scenarios: WorkbenchResources['scenarios'];
  robotAssetPath: string;
}>;

const SAVE_DELAY_MS = 250;

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
  setHidden(root, '[data-evidence-feedback]', true);
  setHidden(root, '[data-revision-compare]', true);
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
  const moduleId = root.dataset.moduleId;
  const moduleVersion = root.dataset.moduleVersion;
  if (!moduleId || !moduleVersion) {
    throw new Error('Missing module identity for workbench state');
  }

  const stateError = requiredElement<HTMLElement>(root, '[data-state-error]');
  const showStateError = (message: string, error?: PlatformError): void => {
    stateError.hidden = false;
    stateError.textContent = error
      ? `${message} ${error.message} ${error.action}`
      : message;
  };
  const clearStateError = (): void => {
    stateError.hidden = true;
    stateError.textContent = '';
  };
  const setSaveStatus = (message: string): void => {
    setText(root, '[data-save-status]', message);
  };
  const selection = await createStateRepository({
    preferredMode: new URLSearchParams(location.search).get('storage') === 'volatile'
      ? 'volatile-selected'
      : 'persistent',
  });
  const runtime = createModuleRuntime({
    moduleId,
    moduleVersion,
    targetStateSchemaVersion: PAYLOAD_SCHEMA_VERSION,
    repository: selection.repository,
    migrations: [{
      from: 1,
      to: 2,
      migrate: (value) => ({ ...migrateWorkbenchPayloadV1(value) }),
    }],
    clock: { now: () => new Date() },
    createWorkspaceId,
    exportPort: createBrowserExportPort(root),
  });
  let runtimeReady = false;
  let stateBlocked = false;
  let hasStoredState = false;
  let validationFailed = false;
  let importFailed = false;
  let persistenceAvailable = selection.mode !== 'volatile-fallback';
  let saveState: 'idle' | 'saving' | 'saved' | 'failed' = 'idle';
  if (selection.warning) {
    showStateError('', selection.warning);
  }
  const started = await runtime.start();
  if (!started.ok) {
    persistenceAvailable = false;
    showStateError('Der lokale Arbeitsstand konnte nicht geöffnet werden.', started.error);
    stateBlocked = true;
  } else if (Object.keys(started.state.payload).length === 0) {
    runtime.updatePayload({ ...projectPersistentPayload(payload) });
    const initialSave = await runtime.flush();
    if (!initialSave.ok) {
      persistenceAvailable = false;
      showStateError('Der initiale Arbeitsstand konnte nicht gespeichert werden.', initialSave.error);
      stateBlocked = true;
    } else {
      runtimeReady = true;
    }
  } else {
    const parsed = parseWorkbenchPayload(started.state.payload);
    if (!parsed.ok) {
      validationFailed = true;
      showStateError(
        'Der gespeicherte Arbeitsstand ist ungültig und wurde nicht überschrieben. Lösche ihn oder importiere eine gültige Datei.',
      );
      stateBlocked = true;
    } else {
      hasStoredState = true;
      payload = parsed.value;
      activeResource = requireScenario(payload.scenarioId);
      usingStandardRepairCase = payload.scenarioId === 'repair-standard';
      algorithm = usingStandardRepairCase
        ? structuredClone(payload.revisedAlgorithm ?? activeResource.starterAlgorithm ?? [])
        : structuredClone(payload.revisedAlgorithm ?? payload.initialAlgorithm);
      confirmedAlgorithm = payload.prediction === null ? '' : JSON.stringify(algorithm);
      runtimeReady = true;
    }
  }

  let experienceEntered = false;
  let experienceState = deriveIum5ExperienceState(payload, {
    hasStoredState,
    saveState,
    connectivity: navigator.onLine ? 'online' : 'offline',
    persistenceAvailable,
    validationFailed,
    importFailed,
  });
  const syncExperienceState = (userTriggered: boolean): void => {
    const next = deriveIum5ExperienceState(payload, {
      hasStoredState,
      saveState,
      connectivity: navigator.onLine ? 'online' : 'offline',
      persistenceAvailable,
      validationFailed,
      importFailed,
    });
    const stageChanged = next.stage !== experienceState.stage;
    renderExperienceState(root, next);
    renderExperienceEntry(root, next, experienceEntered);
    setHidden(root, '[data-reentry-recall]', next.stage !== 'reentry');
    const stage = root.querySelector<HTMLElement>('[data-lx-focus-stage]');
    if (stage) {
      stage.dataset.focusOnActivation = String(userTriggered && stageChanged);
    }
    experienceState = next;
    if (userTriggered && stageChanged) {
      focusActivatedStage(root);
    }
  };

  const statusForMode = (mode: StorageMode): string => mode === 'persistent'
    ? 'Lokal gespeichert'
    : 'Nur für diese Sitzung gespeichert';
  let saveTimer: ReturnType<typeof setTimeout> | undefined;
  const flush = async (): Promise<boolean> => {
    if (!runtimeReady || stateBlocked) {
      return false;
    }
    if (saveTimer !== undefined) {
      clearTimeout(saveTimer);
      saveTimer = undefined;
    }
    try {
      runtime.updatePayload({ ...projectPersistentPayload(payload) });
    } catch (error) {
      showStateError(`Der Arbeitsstand ist ungültig und wurde nicht gespeichert. ${String(error)}`);
      return false;
    }
    saveState = 'saving';
    setSaveStatus('Wird lokal gespeichert');
    experienceState = { ...experienceState, saveState };
    renderExperienceState(root, experienceState);
    const result = await runtime.flush();
    if (!result.ok) {
      saveState = 'failed';
      persistenceAvailable = false;
      showStateError('Der Arbeitsstand konnte nicht gespeichert werden.', result.error);
      syncExperienceState(false);
      return false;
    }
    clearStateError();
    saveState = 'saved';
    setSaveStatus(statusForMode(selection.mode));
    syncExperienceState(false);
    return true;
  };
  const scheduleSave = (): void => {
    if (!runtimeReady || stateBlocked) {
      return;
    }
    if (saveTimer !== undefined) {
      clearTimeout(saveTimer);
    }
    saveState = 'saving';
    setSaveStatus('Wird lokal gespeichert');
    experienceState = { ...experienceState, saveState };
    renderExperienceState(root, experienceState);
    saveTimer = setTimeout(() => void flush(), SAVE_DELAY_MS);
  };

  const refreshGate = (): void => {
    const enabled = editorValid
      && payload.prediction !== null
      && confirmedAlgorithm === JSON.stringify(algorithm);
    setExecutionEnabled(root, enabled);
  };

  const changeAlgorithm = (next: Algorithm, focusIndex?: number): void => {
    algorithm = next;
    const revising = payload.evidenceTrace !== null && payload.repairHypothesis.length > 0;
    payload = revising
      ? { ...payload, prediction: null, evidenceCard: null, systemClassifications: [] }
      : { ...payload, initialAlgorithm: next, prediction: null };
    confirmedAlgorithm = '';
    session = null;
    editorValid = true;
    renderAlgorithm(list, algorithm);
    if (focusIndex !== undefined) {
      const item = list.children.item(Math.min(focusIndex, Math.max(0, algorithm.length - 1)));
      if (item instanceof HTMLElement && algorithm.length > 0) {
        item.focus();
      } else {
        root.querySelector<HTMLButtonElement>('[data-insert-command]')?.focus();
      }
    }
    setPredictionStatus(root, '');
    const error = root.querySelector<HTMLElement>('[data-editor-error]');
    if (error) {
      error.hidden = true;
      error.textContent = '';
    }
    resetExecutionSurface(root);
    refreshGate();
    scheduleSave();
    dispatch(root, 'ium5:algorithm-change', { algorithm });
    syncExperienceState(true);
  };

  const loadScenario = (scenarioId: WorkbenchScenarioId): void => {
    const resource = requireScenario(scenarioId);
    const currentPhase = payload.phaseId;
    activeResource = resource;
    algorithm = structuredClone(resource.starterAlgorithm ?? []);
    payload = {
      ...createInitialPayload(),
      phaseId: currentPhase,
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
    scheduleSave();
    syncExperienceState(true);
  };

  const scenarioDialog = requiredElement<HTMLDialogElement>(root, '[data-scenario-dialog]');
  let pendingScenario: WorkbenchScenarioId | null = null;
  const requestScenario = (scenarioId: WorkbenchScenarioId): void => {
    if (scenarioId === payload.scenarioId && algorithm.length > 0) {
      return;
    }
    if (payload.prediction !== null) {
      pendingScenario = scenarioId;
      scenarioDialog.showModal();
      return;
    }
    loadScenario(scenarioId);
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
      evidenceCard: null,
      systemClassifications: [],
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
    scheduleSave();
  };

  const showExecution = (next: ExecutionSession): void => {
    session = next;
    const succeeded = missionSucceeded(activeResource.scenario, next.state);
    renderExecution(root, next, succeeded, payload.prediction);
    const terminal = next.status === 'complete' || next.status === 'error';
    if (terminal && (!succeeded || usingStandardRepairCase)) {
      payload = {
        ...payload,
        evidenceTrace: {
          scenarioId: payload.scenarioId,
          entries: next.trace,
          finalState: next.state,
          missionSucceeded: succeeded,
        },
      };
      const first = next.trace[0];
      renderEvidenceFeedback(
        root,
        first ? `Schritt ${first.step} · ${first.sourceCommandId}` : 'Ausführung ohne Laufspurschritt',
      );
      scheduleSave();
      syncExperienceState(true);
    }
    const ownProductScenario = ['product-a', 'product-b', 'product-c'].includes(payload.scenarioId);
    if (next.status === 'complete' && succeeded && ownProductScenario && !usingStandardRepairCase) {
      openStandardRepairCase();
    }
  };

  const runStep = (): void => {
    if (!editorValid || payload.prediction === null) {
      setPredictionStatus(root, 'Vorhersage erforderlich: Halte zuerst Position, Blickrichtung und Auftragserfolg fest.');
      root.querySelector<HTMLElement>('#prediction-position')?.focus();
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
      setPredictionStatus(root, 'Vorhersage erforderlich: Halte zuerst Position, Blickrichtung und Auftragserfolg fest.');
      root.querySelector<HTMLElement>('#prediction-position')?.focus();
      return;
    }
    const result = finishExecution(beginExecution(activeResource.scenario, algorithm));
    showExecution(result);
    dispatch(root, 'ium5:run-all', { session: result });
  };

  const confirmEvidence = (): void => {
    if (!session) {
      setText(root, '[data-repair-status]', 'Führe zuerst den bestätigten Algorithmus aus und wähle danach einen Beleg.');
      root.querySelector<HTMLElement>('[data-run-all]')?.focus();
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
      (selected
        ? root.querySelector<HTMLElement>('#repair-hypothesis')
        : root.querySelector<HTMLElement>('[data-evidence-options] input'))?.focus();
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
    for (const row of root.querySelectorAll<HTMLTableRowElement>('[data-trace-step]')) {
      if (row.dataset.traceStep === selected.value) row.setAttribute('aria-current', 'step');
      else row.removeAttribute('aria-current');
    }
    renderEvidenceFeedback(root, `Schritt ${selected.value} der sichtbaren Laufspur`);
    setText(root, '[data-repair-status]', 'Reparaturhypothese gespeichert.');
    scheduleSave();
    syncExperienceState(true);
  };

  const confirmRevision = (): void => {
    if (payload.evidenceTrace === null || payload.repairHypothesis.length === 0) {
      setText(root, '[data-repair-status]', 'Bestätige zuerst Belegspur und Reparaturhypothese.');
      root.querySelector<HTMLElement>('[data-evidence-options]')?.focus();
      return;
    }
    payload = {
      ...payload,
      revisedAlgorithm: structuredClone(algorithm),
      prediction: null,
      evidenceCard: null,
      systemClassifications: [],
    };
    confirmedAlgorithm = '';
    session = null;
    setPredictionStatus(root, 'Revision übernommen – neue Vorhersage erforderlich.');
    resetExecutionSurface(root);
    renderRevisionComparison(root, payload.initialAlgorithm, algorithm);
    refreshGate();
    scheduleSave();
    dispatch(root, 'ium5:revision-confirm', { algorithm });
    syncExperienceState(true);
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
    scheduleSave();
    dispatch(root, 'ium5:loop-decision-confirm', { loopDecision: decision });
  };

  const extendedPath = new URLSearchParams(location.search).get('path') === 'extended';
  const renderActivePhase = (phaseId: LearningPhaseId, focus = false): void => {
    const visiblePhaseId = phaseId === 'ue6-extension' && !extendedPath
      ? 'ue5-consolidation'
      : phaseId;
    const segment = resources.content.segments.find((entry) => entry.id === visiblePhaseId);
    if (!segment) {
      return;
    }
    setText(root, '[data-active-phase-heading]', segment.title);
    setText(root, '[data-active-phase-function]', segment.learningFunction);
    for (const button of root.querySelectorAll<HTMLButtonElement>('[data-phase-id]')) {
      const item = button.closest('li');
      if (button.dataset.phaseId === visiblePhaseId) {
        item?.setAttribute('aria-current', 'step');
      } else {
        item?.removeAttribute('aria-current');
      }
    }
    if (focus) {
      root.querySelector<HTMLElement>('[data-active-phase-heading]')?.focus();
    }
  };

  const transferCaseOrder = resources.content.transferCases.map((entry) => entry.id);
  const updateTransferCase = (caseId: TransferCaseId): void => {
    const select = requiredElement<HTMLSelectElement>(root, `[data-classification-case-id="${caseId}"]`);
    const field = requiredElement<HTMLTextAreaElement>(root, `[data-rationale-case-id="${caseId}"]`);
    const rationale = field.value.trim();
    const withoutCurrent = payload.systemClassifications.filter((entry) => entry.caseId !== caseId);
    if ([...rationale].length > 500) {
      payload = { ...payload, systemClassifications: withoutCurrent };
      const status = requiredElement<HTMLElement>(root, '[data-transfer-status]');
      status.hidden = false;
      status.textContent = 'Begründungen dürfen höchstens 500 Zeichen enthalten.';
      scheduleSave();
      syncExperienceState(true);
      return;
    }
    const classification = select.value;
    if (
      rationale.length === 0
      || !['algorithmic', 'not-algorithmic', 'needs-information'].includes(classification)
    ) {
      payload = { ...payload, systemClassifications: withoutCurrent };
      scheduleSave();
      syncExperienceState(true);
      return;
    }
    const nextEntry: SystemClassification = {
      caseId,
      classification: classification as SystemClassification['classification'],
      rationale,
    };
    const next = [...withoutCurrent, nextEntry].sort(
      (left, right) => transferCaseOrder.indexOf(left.caseId) - transferCaseOrder.indexOf(right.caseId),
    );
    payload = { ...payload, systemClassifications: next };
    const status = requiredElement<HTMLElement>(root, '[data-transfer-status]');
    status.hidden = true;
    status.textContent = '';
    scheduleSave();
    syncExperienceState(true);
  };

  const selfCheckKey = (id: string): keyof WorkbenchPayload['selfCheck'] | null => ({
    'unambiguous-instruction': 'unambiguous',
    'trace-matches-prediction': 'traceMatches',
    'repair-follows-evidence': 'repairJustified',
    'repeat-is-appropriate': 'loopAppropriate',
  } as const)[id] ?? null;

  const showTransferCase = (caseId: string): void => {
    for (const transferCase of root.querySelectorAll<HTMLElement>('[data-transfer-case-id]')) {
      transferCase.hidden = transferCase.dataset.transferCaseId !== caseId;
    }
  };

  const renderEvidenceCardState = (next: WorkbenchPayload): void => {
    const card = next.evidenceCard;
    requiredElement<HTMLSelectElement>(root, '#evidence-card-source-ref').value = card?.sourceRef ?? '';
    requiredElement<HTMLSelectElement>(root, '#evidence-card-evidence-ref').value = card?.evidenceRef ?? '';
    for (const key of ['interpretation', 'revision', 'keyStatement', 'modelBoundary'] as const) {
      requiredElement<HTMLTextAreaElement>(root, `[data-evidence-card-field="${key}"]`).value = card?.[key] ?? '';
    }
    setText(
      root,
      '[data-transfer-card-link]',
      card === null
        ? 'Bestätige zuerst eine Belegkarte, damit der Transfer an deine Kernaussage anschließt.'
        : `Deine Kernaussage für den Transfer: ${card.keyStatement}`,
    );
    setText(root, '[data-evidence-card-status]', card === null ? '' : 'Belegkarte aus lokalem Arbeitsstand geladen.');
    requiredElement<HTMLTextAreaElement>(root, '#reentry-free-recall').value = '';
    setText(root, '[data-reentry-recall-status]', '');
    setText(root, '[data-reentry-key-statement]', '');
    setHidden(root, '[data-reentry-compare]', true);
    setHidden(root, '[data-reentry-card]', true);
    setHidden(
      root,
      '[data-reentry-recall]',
      card === null || next.systemClassifications.length === 0,
    );
  };

  const confirmEvidenceCard = (): void => {
    const sourceRef = requiredElement<HTMLSelectElement>(root, '#evidence-card-source-ref').value;
    const evidenceRef = requiredElement<HTMLSelectElement>(root, '#evidence-card-evidence-ref').value;
    const field = (key: keyof Pick<
      EvidenceCardPayload,
      'interpretation' | 'revision' | 'keyStatement' | 'modelBoundary'
    >): string => requiredElement<HTMLTextAreaElement>(
      root,
      `[data-evidence-card-field="${key}"]`,
    ).value;
    const evidenceCard: EvidenceCardPayload = {
      sourceRef,
      evidenceRef,
      interpretation: field('interpretation'),
      revision: field('revision'),
      keyStatement: field('keyStatement'),
      modelBoundary: field('modelBoundary'),
    };
    const parsed = parseWorkbenchPayload({ ...payload, evidenceCard });
    if (!parsed.ok) {
      const status = requiredElement<HTMLElement>(root, '[data-evidence-card-status]');
      setText(
        root,
        '[data-evidence-card-status]',
        'Fülle alle sechs Felder mit jeweils höchstens 500 Zeichen aus.',
      );
      status.setAttribute('role', 'alert');
      status.tabIndex = -1;
      status.focus();
      return;
    }
    payload = parsed.value;
    const status = requiredElement<HTMLElement>(root, '[data-evidence-card-status]');
    status.setAttribute('role', 'status');
    status.removeAttribute('tabindex');
    setText(root, '[data-evidence-card-status]', 'Belegkarte lokal vorgemerkt.');
    setText(root, '[data-transfer-card-link]', `Deine Kernaussage für den Transfer: ${evidenceCard.keyStatement}`);
    scheduleSave();
    dispatch(root, 'ium5:evidence-card-confirm', { evidenceCard });
    syncExperienceState(true);
  };

  const setDomainInteractionsBlocked = (blocked: boolean): void => {
    for (const control of root.querySelectorAll<
      HTMLButtonElement | HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >('button, input, select, textarea')) {
      const recoveryControl = control.matches([
        '[data-workbench-import]',
        '[data-workbench-delete]',
        '[data-import-confirm]',
        '[data-import-cancel]',
        '[data-delete-confirm]',
        '[data-delete-cancel]',
      ].join(', '));
      if (!recoveryControl) {
        control.disabled = blocked;
      }
    }
  };

  const renderPayloadState = (next: WorkbenchPayload, activateStage = false): void => {
    payload = next;
    activeResource = requireScenario(next.scenarioId);
    usingStandardRepairCase = next.scenarioId === 'repair-standard';
    algorithm = usingStandardRepairCase
      ? structuredClone(next.revisedAlgorithm ?? activeResource.starterAlgorithm ?? [])
      : structuredClone(next.revisedAlgorithm ?? next.initialAlgorithm);
    confirmedAlgorithm = next.prediction === null ? '' : JSON.stringify(algorithm);
    session = null;
    editorValid = true;
    renderScenarioDescription(root, activeResource.scenario);
    renderAlgorithm(list, algorithm);
    resetExecutionSurface(root);
    const position = requiredElement<HTMLSelectElement>(root, '#prediction-position');
    const direction = requiredElement<HTMLSelectElement>(root, '#prediction-direction');
    const success = requiredElement<HTMLSelectElement>(root, '#prediction-success');
    position.value = next.prediction === null
      ? ''
      : `${String.fromCharCode(64 + next.prediction.position.column)}${next.prediction.position.row}`;
    direction.value = next.prediction?.direction ?? '';
    success.value = next.prediction?.success ?? '';
    requiredElement<HTMLTextAreaElement>(root, '#repair-hypothesis').value = next.repairHypothesis;
    requiredElement<HTMLTextAreaElement>(root, '#loop-decision').value = next.loopDecision;
    for (const transferCase of resources.content.transferCases) {
      const saved = next.systemClassifications.find((entry) => entry.caseId === transferCase.id);
      requiredElement<HTMLSelectElement>(
        root,
        `[data-classification-case-id="${transferCase.id}"]`,
      ).value = saved?.classification ?? '';
      requiredElement<HTMLTextAreaElement>(
        root,
        `[data-rationale-case-id="${transferCase.id}"]`,
      ).value = saved?.rationale ?? '';
    }
    const selectedTransferCase = next.systemClassifications[0]?.caseId
      ?? resources.content.transferCases[0]?.id;
    if (selectedTransferCase) {
      requiredElement<HTMLSelectElement>(root, '[data-transfer-case-picker]').value = selectedTransferCase;
      showTransferCase(selectedTransferCase);
    }
    renderEvidenceCardState(next);
    for (const select of root.querySelectorAll<HTMLSelectElement>('[data-self-check-id]')) {
      const key = selfCheckKey(select.dataset.selfCheckId ?? '');
      if (key) {
        select.value = next.selfCheck[key];
      }
    }
    setHidden(root, '[data-preserved-product]', !usingStandardRepairCase);
    if (usingStandardRepairCase) {
      setText(root, '[data-preserved-draft]', JSON.stringify(next.initialAlgorithm, null, 2));
    } else {
      setText(root, '[data-preserved-draft]', '');
    }
    setPredictionStatus(
      root,
      next.prediction === null ? '' : 'Vorhersage aus lokalem Arbeitsstand geladen.',
    );
    renderActivePhase(next.phaseId);
    refreshGate();
    syncExperienceState(activateStage);
  };

  const enterExperience = (): void => {
    experienceEntered = true;
    syncExperienceState(false);
    const stage = root.querySelector<HTMLElement>('[data-lx-focus-stage]');
    if (stage) stage.dataset.focusOnActivation = 'true';
    focusActivatedStage(root);
  };

  setText(
    root,
    '[data-path-summary]',
    extendedPath ? '270 Minuten · 6 Unterrichtseinheiten' : '225 Minuten · 5 Unterrichtseinheiten',
  );
  setHidden(root, '[data-extended-workshop]', !extendedPath);
  for (const item of root.querySelectorAll<HTMLElement>('[data-extended-phase]')) {
    item.hidden = !extendedPath;
  }
  renderPayloadState(payload);
  setDomainInteractionsBlocked(stateBlocked);
  setSaveStatus(stateBlocked ? 'Lokales Speichern gesperrt' : statusForMode(selection.mode));

  document.addEventListener('ium:flush-request', ((event: CustomEvent<FlushRequestDetail>) => {
    event.detail.add(flush());
  }) as EventListener);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      void flush();
    }
  });
  window.addEventListener('online', () => syncExperienceState(false));
  window.addEventListener('offline', () => syncExperienceState(false));

  const exportButton = requiredElement<HTMLButtonElement>(root, '[data-workbench-export]');
  const importInput = requiredElement<HTMLInputElement>(root, '[data-workbench-import]');
  const importDialog = requiredElement<HTMLDialogElement>(root, '[data-import-dialog]');
  const deleteButton = requiredElement<HTMLButtonElement>(root, '[data-workbench-delete]');
  const deleteDialog = requiredElement<HTMLDialogElement>(root, '[data-delete-dialog]');
  let pendingPayload: WorkbenchPayload | null = null;

  const resetActiveModule = async (returnToStart: boolean): Promise<boolean> => {
    if (saveTimer !== undefined) {
      clearTimeout(saveTimer);
      saveTimer = undefined;
    }
    const deleted = await runtime.deleteActive();
    if (!deleted.ok) {
      showStateError('Der Arbeitsstand konnte nicht gelöscht werden.', deleted.error);
      return false;
    }
    const restarted = await runtime.start();
    if (!restarted.ok) {
      showStateError('Nach dem Löschen konnte kein neuer Arbeitsstand angelegt werden.', restarted.error);
      return false;
    }
    const initial = createInitialPayload();
    runtime.updatePayload({ ...projectPersistentPayload(initial) });
    const saved = await runtime.flush();
    if (!saved.ok) {
      showStateError('Der neue leere Arbeitsstand konnte nicht gespeichert werden.', saved.error);
      return false;
    }
    runtimeReady = true;
    stateBlocked = false;
    hasStoredState = false;
    validationFailed = false;
    importFailed = false;
    saveState = 'saved';
    experienceEntered = !returnToStart;
    renderPayloadState(initial, !returnToStart);
    setDomainInteractionsBlocked(false);
    clearStateError();
    setSaveStatus('Arbeitsstand gelöscht');
    return true;
  };

  const startPrimary = requiredElement<HTMLButtonElement>(root, '[data-start-primary]');
  const resumePrimary = requiredElement<HTMLButtonElement>(root, '[data-resume-primary]');
  const startReset = requiredElement<HTMLButtonElement>(root, '[data-start-reset]');
  const startResetDialog = requiredElement<HTMLDialogElement>(root, '#start-reset-dialog');
  const startResetCancel = requiredElement<HTMLButtonElement>(startResetDialog, '[data-data-action-cancel]');
  const startResetConfirm = requiredElement<HTMLButtonElement>(startResetDialog, '[data-data-action-confirm]');

  startPrimary.addEventListener('click', enterExperience);
  resumePrimary.addEventListener('click', enterExperience);
  startReset.addEventListener('click', () => {
    startResetDialog.showModal();
    startResetCancel.focus();
  });
  startResetCancel.addEventListener('click', () => startResetDialog.close('cancel'));
  startResetDialog.addEventListener('close', () => {
    if (startResetDialog.returnValue !== 'confirm') startReset.focus();
  });
  startResetConfirm.addEventListener('click', async () => {
    startResetDialog.close('confirm');
    if (await resetActiveModule(true)) {
      startPrimary.focus();
    }
  });

  exportButton.addEventListener('click', async () => {
    if (!(await flush())) {
      return;
    }
    const result = await runtime.exportState();
    if (!result.ok) {
      showStateError('Der Arbeitsstand konnte nicht exportiert werden.', result.error);
    }
  });

  importInput.addEventListener('change', async () => {
    const file = importInput.files?.[0];
    if (!file) {
      return;
    }
    const preview = runtime.previewImport(new Uint8Array(await file.arrayBuffer()));
    if (!preview.ok) {
      importFailed = true;
      showStateError('Import nicht übernommen.', preview.error);
      importInput.value = '';
      pendingPayload = null;
      syncExperienceState(false);
      return;
    }
    const parsed = parseWorkbenchPayload(preview.state.payload);
    if (!parsed.ok) {
      importFailed = true;
      showStateError('Import nicht übernommen. Der Modulinhalt ist ungültig.');
      importInput.value = '';
      pendingPayload = null;
      syncExperienceState(false);
      return;
    }
    pendingPayload = parsed.value;
    clearStateError();
    setText(root, '[data-preview-module]', preview.preview.moduleId);
    setText(root, '[data-preview-version]', preview.preview.moduleVersion);
    setText(root, '[data-preview-saved]', preview.preview.savedAt);
    setText(root, '[data-preview-fields]', preview.preview.payloadFields.join(', '));
    importDialog.showModal();
  });

  requiredElement<HTMLButtonElement>(root, '[data-import-cancel]').addEventListener('click', () => {
    importDialog.close();
    importInput.value = '';
    pendingPayload = null;
    importInput.focus();
  });
  requiredElement<HTMLButtonElement>(root, '[data-import-confirm]').addEventListener('click', async () => {
    if (pendingPayload === null) {
      showStateError('Import nicht übernommen. Es liegt kein geprüfter Import vor.');
      return;
    }
    const result = await runtime.confirmImport();
    if (!result.ok) {
      importFailed = true;
      syncExperienceState(false);
      showStateError('Import nicht übernommen.', result.error);
      return;
    }
    const parsed = parseWorkbenchPayload(result.state.payload);
    if (!parsed.ok) {
      importFailed = true;
      syncExperienceState(false);
      showStateError('Import nicht übernommen. Der bestätigte Modulinhalt ist ungültig.');
      return;
    }
    runtimeReady = true;
    stateBlocked = false;
    importFailed = false;
    hasStoredState = true;
    renderPayloadState(parsed.value, true);
    setDomainInteractionsBlocked(false);
    importDialog.close();
    importInput.value = '';
    pendingPayload = null;
    clearStateError();
    setSaveStatus('Import lokal gespeichert');
    root.querySelector<HTMLElement>('#workbench-title')?.focus();
  });

  deleteButton.addEventListener('click', () => deleteDialog.showModal());
  requiredElement<HTMLButtonElement>(root, '[data-delete-cancel]').addEventListener('click', () => {
    deleteDialog.close();
    deleteButton.focus();
  });
  requiredElement<HTMLButtonElement>(root, '[data-delete-confirm]').addEventListener('click', async () => {
    if (await resetActiveModule(false)) {
      deleteDialog.close();
      root.querySelector<HTMLElement>('#workbench-title')?.focus();
    }
  });

  requiredElement<HTMLButtonElement>(root, '[data-scenario-cancel]').addEventListener('click', () => {
    pendingScenario = null;
    scenarioDialog.close();
  });
  requiredElement<HTMLButtonElement>(root, '[data-scenario-confirm]').addEventListener('click', () => {
    if (pendingScenario !== null) {
      loadScenario(pendingScenario);
    }
    pendingScenario = null;
    scenarioDialog.close();
  });

  root.addEventListener('input', (event) => {
    if (stateBlocked) {
      return;
    }
    const target = event.target;
    if (target instanceof HTMLTextAreaElement && target.dataset.rationaleCaseId) {
      updateTransferCase(target.dataset.rationaleCaseId as TransferCaseId);
      return;
    }
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
    changeAlgorithm(replaceRepeat(algorithm, index, { ...command, count }), index);
  });

  root.addEventListener('change', (event) => {
    if (stateBlocked) {
      return;
    }
    const target = event.target;
    if (target instanceof HTMLSelectElement && target.dataset.classificationCaseId) {
      updateTransferCase(target.dataset.classificationCaseId as TransferCaseId);
      return;
    }
    if (target instanceof HTMLSelectElement && target.matches('[data-transfer-case-picker]')) {
      showTransferCase(target.value);
      return;
    }
    if (target instanceof HTMLSelectElement && target.dataset.selfCheckId) {
      const key = selfCheckKey(target.dataset.selfCheckId);
      if (
        key
        && ['yes', 'review', 'not-applicable'].includes(target.value)
      ) {
        payload = {
          ...payload,
          selfCheck: {
            ...payload.selfCheck,
            [key]: target.value as SelfCheckValue,
          },
        };
        scheduleSave();
      }
    }
  });

  root.addEventListener('click', (event) => {
    if (stateBlocked) {
      return;
    }
    const target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    const phaseButton = target.closest<HTMLButtonElement>('[data-phase-id]');
    if (phaseButton?.dataset.phaseId) {
      const phaseId = phaseButton.dataset.phaseId as LearningPhaseId;
      payload = { ...payload, phaseId };
      renderActivePhase(phaseId, true);
      scheduleSave();
      return;
    }
    const roleSwap = target.closest<HTMLButtonElement>('[data-role-swap]');
    if (roleSwap) {
      const exchange = roleSwap.closest<HTMLElement>('[data-role-exchange]');
      const primary = exchange?.querySelector<HTMLElement>('[data-role-primary]');
      const secondary = exchange?.querySelector<HTMLElement>('[data-role-secondary]');
      const status = exchange?.querySelector<HTMLElement>('[data-role-status]');
      if (primary && secondary && status) {
        const previous = primary.textContent ?? '';
        primary.textContent = secondary.textContent;
        secondary.textContent = previous;
        status.textContent = `Person A ${primary.textContent?.toLocaleLowerCase('de-DE')}, Person B ${secondary.textContent?.toLocaleLowerCase('de-DE')}.`;
      }
      return;
    }
    const holdChoice = target.closest<HTMLButtonElement>('[data-shared-hold-choice]');
    if (holdChoice) {
      const hold = holdChoice.closest<HTMLElement>('[data-shared-hold]');
      const status = hold?.querySelector<HTMLElement>('[data-shared-hold-status]');
      if (hold && status) {
        const shared = holdChoice.dataset.sharedHoldChoice === 'shared';
        hold.dataset.choice = shared ? 'shared' : 'independent';
        status.textContent = shared
          ? 'Die gemeinsame Besprechung ist gewählt; der lokale Arbeitsstand bleibt erhalten.'
          : 'Du fährst selbstständig fort; der lokale Arbeitsstand bleibt erhalten.';
      }
      return;
    }
    const familyButton = target.closest<HTMLButtonElement>('[data-task-family-open]');
    if (familyButton?.dataset.taskFamilyOpen) {
      setHidden(root, `[data-task-family-panel="${familyButton.dataset.taskFamilyOpen}"]`, false);
      if (familyButton.dataset.taskFamilyOpen === 'active-example') {
        requestScenario('worked-sequence');
      }
      return;
    }
    const supportButton = target.closest<HTMLButtonElement>('[data-support-toggle]');
    if (supportButton?.dataset.supportToggle) {
      const panel = requiredElement<HTMLElement>(
        root,
        `[data-support-panel="${supportButton.dataset.supportToggle}"]`,
      );
      const expanded = supportButton.getAttribute('aria-expanded') === 'true';
      supportButton.setAttribute('aria-expanded', String(!expanded));
      panel.hidden = expanded;
      return;
    }
    const scenarioButton = target.closest<HTMLButtonElement>('[data-open-scenario]');
    if (scenarioButton?.dataset.openScenario) {
      requestScenario(scenarioButton.dataset.openScenario as WorkbenchScenarioId);
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
          changeAlgorithm(moveCommand(algorithm, index, -1), Math.max(0, index - 1));
          break;
        case 'down':
          changeAlgorithm(
            moveCommand(algorithm, index, 1),
            Math.min(algorithm.length - 1, index + 1),
          );
          break;
        case 'remove': {
          const next = removeCommand(algorithm, index);
          changeAlgorithm(next, Math.min(index, Math.max(0, next.length - 1)));
          break;
        }
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
      scheduleSave();
      dispatch(root, 'ium5:prediction-confirm', { prediction });
      syncExperienceState(true);
      return;
    }
    if (target.closest('[data-evidence-card-confirm]')) {
      confirmEvidenceCard();
      return;
    }
    if (target.closest('[data-reentry-confirm]')) {
      const recall = requiredElement<HTMLTextAreaElement>(root, '#reentry-free-recall').value.trim();
      if (recall.length === 0 || [...recall].length > 500) {
        setText(root, '[data-reentry-recall-status]', 'Formuliere zuerst deine eigene Erinnerung mit höchstens 500 Zeichen.');
        root.querySelector<HTMLElement>('#reentry-free-recall')?.focus();
        return;
      }
      setText(root, '[data-reentry-recall-status]', 'Eigene Erinnerung festgehalten. Jetzt kannst du vergleichen.');
      setHidden(root, '[data-reentry-compare]', false);
      root.querySelector<HTMLElement>('[data-reentry-compare]')?.focus();
      return;
    }
    if (target.closest('[data-reentry-compare]')) {
      setText(root, '[data-reentry-key-statement]', payload.evidenceCard?.keyStatement ?? '');
      setHidden(root, '[data-reentry-card]', false);
      root.querySelector<HTMLElement>('[data-reentry-card]')?.focus();
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

  root.inert = false;
  root.setAttribute('aria-busy', 'false');
  root.dataset.initializationState = stateBlocked ? 'blocked' : 'ready';
}
