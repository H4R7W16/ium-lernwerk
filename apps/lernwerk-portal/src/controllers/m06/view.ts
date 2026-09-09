import {
  checkGoal,
  run,
  type Basic,
  type Goal,
  type Grid,
  type Program,
  type Direction,
} from '@ium/v2-g5-m06';
import {
  connectM06,
  createBrowserM06Dependencies,
  type M06Controller,
  type M06Run,
  type M06Resources,
} from './controller.js';
import { diagramText, renderEditableProgram } from './diagram-editor.js';
import { nextCommandId } from './code-editor.js';

type S3Case = Readonly<{ id: 'S0' | 'S1' | 'S2' | 'S3'; grid: Grid; goal?: Goal; program: Program }>;
type BrowserResources = M06Resources & Readonly<{
  cases: Readonly<{ gridCases: readonly S3Case[] }>;
}>;

function required<T extends Element>(root: ParentNode, selector: string): T {
  const value = root.querySelector<T>(selector);
  if (!value) throw new Error(`Missing M06 control: ${selector}`);
  return value;
}

function commandKind(value: string | null): Basic['kind'] {
  if (value === 'move' || value === 'turn-left' || value === 'turn-right') return value;
  throw new Error(`Unknown command kind: ${String(value)}`);
}

function selectedTraceSteps(root: ParentNode): number[] {
  return [...root.querySelectorAll<HTMLInputElement>('[data-trace-output] input:checked')]
    .map((field) => Number(field.value));
}

export function renderProgramSummary(controller: M06Controller): string {
  const program = controller.dossier().p3.draftProgram;
  return program.length === 0 ? 'Noch kein Code eingegeben.' : diagramText(program);
}

export function firstDifference(left: string, right: string): number | null {
  const leftParts = left.split(/\s+/).filter(Boolean);
  const rightParts = right.split(/\s+/).filter(Boolean);
  const length = Math.max(leftParts.length, rightParts.length);
  for (let index = 0; index < length; index += 1) {
    if (leftParts[index] !== rightParts[index]) return index + 1;
  }
  return null;
}

export async function connectM06BrowserWorkspace(): Promise<M06Controller> {
  const root = required<HTMLElement>(document, '[data-m06-workspace]');
  const resourceNode = required<HTMLScriptElement>(document, '[data-m06-resources]');
  const resources = JSON.parse(resourceNode.textContent ?? '{}') as BrowserResources;
  const s3 = resources.cases.gridCases.find((entry) => entry.id === 'S3');
  if (!s3?.goal) throw new Error('S3 resource missing');
  const s3Goal = s3.goal;
  const s2 = resources.cases.gridCases.find((entry) => entry.id === 'S2');
  if (!s2) throw new Error('S2 resource missing');
  const s0 = resources.cases.gridCases.find((entry) => entry.id === 'S0');
  const s1 = resources.cases.gridCases.find((entry) => entry.id === 'S1');
  if (!s0 || !s1) throw new Error('S0/S1 resource missing');
  const startupControls = [...root.querySelectorAll<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | HTMLButtonElement>('input, textarea, select, button')]
    .map((control) => ({ control, disabled: control.disabled }));
  for (const { control } of startupControls) control.disabled = true;
  const controller = await connectM06(root, resources, createBrowserM06Dependencies(root));
  const diagram = () => controller.dossier().p3.diagram.program;
  const code = () => controller.dossier().p3.draftProgram;
  const diagramExplanation = required<HTMLTextAreaElement>(root, '[data-diagram-explanation]');
  const diagramOutput = required<HTMLElement>(root, '[data-diagram-output]');
  const codeOutput = required<HTMLElement>(root, '[data-code-output]');
  const rationale = required<HTMLTextAreaElement>(root, '[data-rationale]');
  const p1Explanation = required<HTMLTextAreaElement>(root, '[data-p1-explanation]');
  const render = () => {
    const dossier = controller.dossier();
    renderEditableProgram(required<HTMLElement>(root, '[data-graphic="p1"]'), dossier.p1.diagram.program,
      (next) => controller.updateP1Diagram(next, p1Explanation.value));
    renderEditableProgram(required<HTMLElement>(root, '[data-graphic="diagram"]'), diagram(),
      (next) => controller.updateDiagram(next, diagramExplanation.value));
    renderEditableProgram(required<HTMLElement>(root, '[data-graphic="code"]'), code(),
      (next) => controller.updateDraftProgram(next));
    const grid = controller.scenario() === 'S2' ? s2.grid : s3.grid;
    required<HTMLElement>(root, '[data-grid-context]').textContent = `${controller.scenario()} · Raster ${grid.width} × ${grid.height}, Start (${grid.start.position.column},${grid.start.position.row}), Blick rechts.`;
    diagramOutput.textContent = diagram().length ? diagramText(diagram()) : 'Noch keine Grafik angelegt.';
    codeOutput.textContent = code().length ? diagramText(code()) : 'Noch kein Code eingegeben.';
    required<HTMLElement>(root, '[data-p1-output]').textContent = dossier.p1.diagram.program.length
      ? diagramText(dossier.p1.diagram.program) : 'Noch keine P1-Grafik angelegt.';
    if (rationale.value !== dossier.p3.evidence.rationale) rationale.value = dossier.p3.evidence.rationale;
    const predicted = dossier.p3.evidence.predicted;
    required<HTMLElement>(root, '[data-saved-prediction]').textContent = predicted
      ? `Gesicherte Vorhersage: (${predicted.position.column},${predicted.position.row}), Blick ${
        { north: 'oben', east: 'rechts', south: 'unten', west: 'links' }[predicted.direction]}.`
      : 'Noch keine Vorhersage im Beleg gesichert.';

    for (const phase of ['before', 'after'] as const) {
      const evidence = dossier.p2[phase];
      const predicted = evidence.predicted;
      const prediction = predicted
        ? `Vorhersage: (${predicted.position.column},${predicted.position.row}), Blick ${
          { north: 'oben', east: 'rechts', south: 'unten', west: 'links' }[predicted.direction]}`
        : 'Keine Vorhersage gesichert.';
      required<HTMLElement>(root, `[data-revision-output="${phase}"]`).textContent = evidence.program.length
        ? `${diagramText(evidence.program)}\n${prediction}\nAusgewählte Schritte: ${evidence.steps.join(', ') || 'keine'}`
        : 'Noch kein Vergleichsbeleg gesichert.';
      const field = required<HTMLTextAreaElement>(root, `[data-revision-rationale="${phase}"]`);
      if (field.value !== evidence.rationale) field.value = evidence.rationale;
    }
  };
  const basic = (program: Program, kind: Basic['kind']): Basic => ({
    id: nextCommandId(program),
    kind,
  });

  for (const editor of root.querySelectorAll<HTMLElement>('[data-editor]')) {
    const editorKind = editor.dataset.editor;
    for (const button of editor.querySelectorAll<HTMLButtonElement>('[data-add]')) {
      button.addEventListener('click', () => {
        if (controller.reloadPreparing()) return;
        if (editorKind === 'diagram') {
          controller.updateDiagram([...diagram(), basic(diagram(), commandKind(button.dataset.add ?? null))], diagramExplanation.value);
        } else if (editorKind === 'p1') {
          const program = controller.dossier().p1.diagram.program;
          controller.updateP1Diagram([...program, basic(program, commandKind(button.dataset.add ?? null))], p1Explanation.value);
        } else {
          controller.updateDraftProgram([...code(), basic(code(), commandKind(button.dataset.add ?? null))]);
        }
        render();
      });
    }
    required<HTMLButtonElement>(editor, '[data-clear]').addEventListener('click', () => {
      if (editorKind === 'diagram') {
        controller.updateDiagram([], diagramExplanation.value);
      } else if (editorKind === 'p1') {
        controller.updateP1Diagram([], p1Explanation.value);
      } else {
        controller.updateDraftProgram([]);
      }
      render();
    });
  }
  diagramExplanation.addEventListener('input', () => {
    controller.updateDiagram(diagram(), diagramExplanation.value);
  });
  p1Explanation.addEventListener('input', () => controller.updateP1Diagram(
    controller.dossier().p1.diagram.program, p1Explanation.value,
  ));
  rationale.addEventListener('input', () => controller.updateP3Rationale(rationale.value));
  for (const phase of ['before', 'after'] as const) {
    const field = required<HTMLTextAreaElement>(root, `[data-revision-rationale="${phase}"]`);
    field.addEventListener('input', () => controller.updateRevisionRationale(phase, field.value));
  }

  required<HTMLButtonElement>(root, '[data-add-repeat]').addEventListener('click', () => {
    const count = Number(required<HTMLInputElement>(root, '#m06-repeat-count').value);
    const repeatId = nextCommandId(code());
    let nextNumber = Number(repeatId.slice(4)) + 1;
    const body = [...root.querySelectorAll<HTMLSelectElement>('[data-repeat-body]')]
      .filter((field) => field.value !== '')
      .map((field): Basic => ({ id: `cmd-${nextNumber++}`, kind: commandKind(field.value) }));
    if (body.length === 0) return;
    controller.updateDraftProgram([...code(), { id: repeatId, kind: 'repeat', count, body }]);
    render();
  });
  required<HTMLButtonElement>(root, '[data-add-diagram-repeat]').addEventListener('click', () => {
    const count = Number(required<HTMLInputElement>(root, '#m06-diagram-count').value);
    const repeatId = nextCommandId(diagram());
    let nextNumber = Number(repeatId.slice(4)) + 1;
    const body = [...root.querySelectorAll<HTMLSelectElement>('[data-diagram-repeat-body]')]
      .filter((field) => field.value !== '')
      .map((field): Basic => ({ id: `cmd-${nextNumber++}`, kind: commandKind(field.value) }));
    if (body.length === 0) return;
    controller.updateDiagram([...diagram(), { id: repeatId, kind: 'repeat', count, body }], diagramExplanation.value);
    render();
  });

  const directions = { north: 'oben', east: 'rechts', south: 'unten', west: 'links' } as const;
  const describeTrace = (result: ReturnType<typeof run>, limit = result.trace.length) => result.trace.slice(0, limit).map((step) =>
    `Aktion ${step.step}: (${step.before.position.column},${step.before.position.row}) → (${step.after.position.column},${step.after.position.row}), Blick ${directions[step.after.direction]}${step.error ? `, Rastergrenze: ${step.error}` : ''}`).join('\n');
  const exampleSteps = new Map<string, number>();
  for (const example of [s0, s1]) {
    const output = required<HTMLElement>(root, `[data-example-trace="${example.id}"]`);
    required<HTMLButtonElement>(root, `[data-example-next="${example.id}"]`).addEventListener('click', () => {
      const result = run(example.grid, example.program);
      const count = Math.min((exampleSteps.get(example.id) ?? 0) + 1, result.trace.length);
      exampleSteps.set(example.id, count);
      output.textContent = describeTrace(result, count) + (example.id === 'S1' && (count === 2 || count === 4)
        ? '\nVerarbeitungsstopp: Erkläre Ort und Blick; sage die nächste Anweisung voraus.' : '');
    });
    required<HTMLButtonElement>(root, `[data-example-reset="${example.id}"]`).addEventListener('click', () => {
      exampleSteps.delete(example.id); output.textContent = 'Noch nicht ausgeführt.';
    });
  }
  required<HTMLButtonElement>(root, '[data-p1-starter]').addEventListener('click', () => {
    if (controller.dossier().p1.diagram.program.length && !window.confirm('Die vorhandene P1-Grafik durch die unvollständige S1-Grafik ersetzen?')) return;
    controller.updateP1Diagram([{ id: 'cmd-1', kind: 'repeat', count: 4, body: [{ id: 'cmd-2', kind: 'move' }] }], p1Explanation.value);
  });
  required<HTMLButtonElement>(root, '[data-p1-body-add]').addEventListener('click', () => {
    const program = controller.dossier().p1.diagram.program;
    const repeatIndex = program.findIndex((entry) => entry.kind === 'repeat');
    if (repeatIndex < 0) return;
    const kind = commandKind(required<HTMLSelectElement>(root, '[data-p1-body-kind]').value);
    controller.updateP1Diagram(program.map((entry, index) => index === repeatIndex && entry.kind === 'repeat' && entry.body.length < 5
      ? { ...entry, body: [...entry.body, basic(program, kind)] } : entry), p1Explanation.value);
  });
  required<HTMLButtonElement>(root, '[data-load-s2]').addEventListener('click', () => {
    if (code().length && !window.confirm('Den aktuellen Code und seinen P3-Spurbeleg durch die S2-Fehlfassung ersetzen? Exportiere deinen Entwurf vorher, wenn du ihn behalten möchtest.')) return;
    controller.selectScenario('S2');
    scenario.value = 'S2';
    controller.updateDraftProgram(s2.program);
    required<HTMLElement>(root, '#code-title').scrollIntoView();
  });
  required<HTMLButtonElement>(root, '[data-compare-s2]').addEventListener('click', () => {
    const intended = run(s1.grid, s1.program), faulty = run(s2.grid, s2.program);
    const first = faulty.trace.find((step, index) => JSON.stringify(step.after) !== JSON.stringify(intended.trace[index]?.after));
    const boundary = faulty.trace.find((step) => step.error);
    const output = required<HTMLElement>(root, '[data-s2-comparison]');
    output.hidden = false;
    output.textContent = `Erste fachliche Abweichung: Aktion ${first?.step}. Wieder vor statt links: Die Drehung steht außerhalb des Körpers.\nRastergrenze: Aktion ${boundary?.step}. Vergleiche danach deine eigene Revision.\nSoll S1:\n${describeTrace(intended, 3)}\nIst S2:\n${describeTrace(faulty)}`;
  });
  const retrievalPanel = required<HTMLElement>(root, '[data-m06-retrieval-panel]');
  const comparison = required<HTMLElement>(root, '[data-retrieval-comparison]');
  const conceal = (hidden: boolean) => {
    for (const panel of root.querySelectorAll<HTMLElement>('[data-learning-examples], [data-learning-helps], #mein-pruefdossier, [data-materials]')) panel.hidden = hidden;
  };
  required<HTMLButtonElement>(root, '[data-m06-open-retrieval]').addEventListener('click', () => {
    comparison.hidden = true;
    required<HTMLElement>(root, '[data-retrieval-solution]').textContent = '';
    conceal(true); project(false);
    required<HTMLTextAreaElement>(root, '[data-m06-retrieval]').focus();
  });
  required<HTMLButtonElement>(root, '[data-retrieval-compare]').addEventListener('click', () => {
    if (!controller.transient().retrievalReason.trim()) return;
    const dossier = controller.dossier();
    required<HTMLElement>(root, '[data-retrieval-solution]').textContent =
      `S1-Beispiel:\n${diagramText(s1.program)}\n${describeTrace(run(s1.grid, s1.program), 4)}\nDeine gesicherte/aktuelle P1-Grafik:\n${diagramText(dossier.p1.diagram.program) || 'Noch keine'}\nDeine P3-Grafik:\n${diagramText(diagram()) || 'Noch keine'}\nDein P3-Code:\n${diagramText(code()) || 'Noch keiner'}`;
    comparison.hidden = false;
  });
  required<HTMLButtonElement>(root, '[data-m06-own-draft]').addEventListener('click', () => {
    retrievalPanel.hidden = true; conceal(false);
    required<HTMLElement>(root, '#mein-pruefdossier').focus();
  });

  let displayedRun: number | null = null;
  const showTrace = (program: Program, selected: readonly number[] = [], snapshot?: M06Run) => {
    const result = snapshot?.result ?? run(s3.grid, program);
    const goal = checkGoal(result, s3Goal);
    required<HTMLElement>(root, '[data-goal-feedback]').textContent = snapshot?.scenario === 'S2'
      ? `S2: ${result.trace.length} Schritte ausgeführt; ${result.status === 'complete' ? 'Ausführung beendet' : 'Rastergrenze oder Schrittgrenze erreicht'}. Vergleiche Ursache und erste Abweichung.`
      : goal.ok
      ? 'Ziel, Prüfpunkte und Randfahrt sind erfüllt. Begründe jetzt eine relevante Spurstelle.'
      : `Prüfung noch offen: ${goal.reason}. Ändere eine begründete Stelle.`;
    const trace = required<HTMLElement>(root, '[data-trace-output]');
    trace.replaceChildren();
    const fieldset = document.createElement('fieldset');
    const legend = document.createElement('legend');
    legend.textContent = 'Relevante Spurstellen auswählen';
    fieldset.append(legend);
    for (const step of result.trace) {
      const row = document.createElement('label');
      row.className = 'm06-trace-step';
      const check = document.createElement('input');
      check.type = 'checkbox';
      check.value = String(step.step);
      check.checked = selected.includes(step.step);
      if (!snapshot) check.dataset.savedTrace = 'true';
      const directions = { north: 'oben', east: 'rechts', south: 'unten', west: 'links' } as const;
      const iteration = step.iteration === null ? 'ohne Wiederholung' : `Durchlauf ${step.iteration}`;
      row.append(check, ` Schritt ${step.step}, Befehl ${step.commandId}, ${iteration}: (${step.before.position.column},${step.before.position.row}) → (${step.after.position.column},${step.after.position.row}), Blick ${directions[step.after.direction]}${step.error ? `, Fehler ${step.error}` : ''}`);
      fieldset.append(row);
    }
    trace.append(fieldset);
    required<HTMLElement>(root, '[data-run-context]').textContent = snapshot
      ? `${snapshot.scenario} · Aktuelle Ausführung ab (${snapshot.grid.start.position.column},${snapshot.grid.start.position.row}). ${snapshot.predicted
        ? 'Mit eigener Vorhersage vor diesem Lauf. Wähle passende Spurstellen aus.'
        : 'Freie Ausführung ohne Vorhersage; keine Übernahme als vorhersagegebundener Beleg.'}`
      : 'Gespeicherter P3-Beleg zu S3. Für einen neuen Beleg eine eigene Vorhersage abgeben und erneut ausführen.';
  };
  required<HTMLButtonElement>(root, '[data-run-code]').addEventListener('click', () => {
    controller.runProgram(controller.scenario() === 'S2' ? s2.grid : s3.grid);
  });

  required<HTMLButtonElement>(root, '[data-save-evidence]').addEventListener('click', () => {
    controller.recordP3Evidence(controller.currentRun()?.id ?? -1, selectedTraceSteps(root), rationale.value);
  });
  required<HTMLInputElement>(root, '[data-prediction]').addEventListener('input', (event) => {
    controller.setTransient({ prediction: (event.currentTarget as HTMLInputElement).value });
  });
  for (const button of root.querySelectorAll<HTMLButtonElement>('[data-revision]')) {
    button.addEventListener('click', () => {
      const phase = button.dataset.revision;
      if (phase !== 'before' && phase !== 'after') return;
      if (!controller.recordRevisionEvidence(phase, controller.currentRun()?.id ?? -1, selectedTraceSteps(root), rationale.value)) return;
      const value = Number(required<HTMLInputElement>(root, '[data-first-deviation]').value);
      controller.setFirstDeviation(Number.isInteger(value) && value > 0 ? value : null);
    });
  }
  const scenario = required<HTMLSelectElement>(root, '[data-run-scenario]');
  scenario.addEventListener('change', () => controller.selectScenario(scenario.value === 'S2' ? 'S2' : 'S3'));
  const predictedColumn = required<HTMLInputElement>(root, '[data-run-prediction-column]');
  const predictedRow = required<HTMLInputElement>(root, '[data-run-prediction-row]');
  const predictedDirection = required<HTMLSelectElement>(root, '[data-run-prediction-direction]');
  const updatePrediction = () => controller.setRunPrediction(
    predictedColumn.value && predictedRow.value && predictedDirection.value
      ? { position: { column: Number(predictedColumn.value), row: Number(predictedRow.value) }, direction: predictedDirection.value as Direction }
      : null,
  );
  [predictedColumn, predictedRow, predictedDirection].forEach((field) => field.addEventListener('input', updatePrediction));
  const resetPrediction = () => { predictedColumn.value = ''; predictedRow.value = ''; predictedDirection.value = ''; };
  let predictionProgram = JSON.stringify(code());
  let predictionScenario = controller.scenario();

  const deviation = required<HTMLInputElement>(root, '[data-first-deviation]');
  deviation.addEventListener('input', () => {
    const value = Number(deviation.value);
    controller.setFirstDeviation(Number.isInteger(value) && value > 0 ? value : null);
  });

  const transferSequence = required<HTMLInputElement>(root, '[data-transfer-sequence]');
  const transferRationale = required<HTMLTextAreaElement>(root, '[data-transfer-rationale]');
  const saveTransfer = () => {
    const allowed = new Set(['aufnehmen', 'prüfen', 'ablegen']);
    const sequence = transferSequence.value.split(',')
      .map((value) => value.trim())
      .filter((value): value is 'aufnehmen' | 'prüfen' | 'ablegen' => allowed.has(value));
    controller.updateTransfer(sequence, transferRationale.value);
  };
  transferSequence.addEventListener('input', saveTransfer);
  transferRationale.addEventListener('input', saveTransfer);

  const systemFields = [...root.querySelectorAll<HTMLTextAreaElement>('[data-system]')];
  const saveSystems = () => controller.updateSystems({
    timeControl: required<HTMLTextAreaElement>(root, '[data-system="timeControl"]').value,
    routeCalculation: required<HTMLTextAreaElement>(root, '[data-system="routeCalculation"]').value,
    boundary: required<HTMLTextAreaElement>(root, '[data-system="boundary"]').value,
  });
  systemFields.forEach((field) => field.addEventListener('input', saveSystems));

  const returnArea = required<HTMLSelectElement>(root, '[data-return-area]');
  const returnOpen = required<HTMLInputElement>(root, '[data-return-open]');
  const returnNext = required<HTMLInputElement>(root, '[data-return-next]');
  const saveReturn = () => controller.updateReturnNote({
    area: returnArea.value as 'auftrag' | 'dossier' | 'sicherung',
    openPoint: returnOpen.value,
    nextAction: returnNext.value,
  });
  [returnArea, returnOpen, returnNext].forEach((field) => field.addEventListener('input', saveReturn));

  let importSelection = 0;
  const cancelSelection = () => { importSelection += 1; controller.cancelImport(); };
  required<HTMLButtonElement>(root, '[data-retry-start]').addEventListener('click', () => {
    if (!controller.workspaceReady() && !controller.replacingWork() && !controller.reloadPreparing()) window.location.reload();
  });
  required<HTMLButtonElement>(root, '[data-cancel-import]').addEventListener('click', () => {
    cancelSelection();
    required<HTMLInputElement>(root, '[data-import-work]').focus();
  });
  required<HTMLButtonElement>(root, '[data-confirm-import]').addEventListener('click', async () => {
    importSelection += 1;
    const imported = await controller.confirmImport();
    if (imported) required<HTMLElement>(root, '#mein-pruefdossier').focus();
  });
  required<HTMLButtonElement>(root, '[data-start-new]').addEventListener('click', async () => {
    if (window.confirm('Den bisherigen lokalen Stand und das gesicherte Original durch einen leeren Arbeitsstand ersetzen? Exportiere das Original vorher, wenn du es behalten möchtest.')) {
      cancelSelection();
      if (await controller.startNew()) required<HTMLElement>(root, '#mein-pruefdossier').focus();
    }
  });
  required<HTMLButtonElement>(root, '[data-delete-work]').addEventListener('click', () => {
    if (window.confirm('Diesen lokalen M06-Arbeitsstand wirklich löschen?')) {
      cancelSelection();
      void controller.deleteAllWork();
    }
  });
  required<HTMLButtonElement>(root, '[data-export-work]').addEventListener('click', () => {
    void controller.exportWork(false);
  });
  required<HTMLButtonElement>(root, '[data-export-recovery]').addEventListener('click', () => {
    void controller.exportWork(true);
  });
  required<HTMLInputElement>(root, '[data-import-work]').addEventListener('change', async (event) => {
    const input = event.currentTarget as HTMLInputElement;
    const file = input.files?.[0];
    cancelSelection();
    const selection = importSelection;
    input.value = '';
    if (!file) return;
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      if (selection !== importSelection) return;
      if (await controller.previewImport(bytes)) required<HTMLElement>(root, '[data-import-preview]').focus();
    } catch {
      if (selection === importSelection) controller.cancelImport('Die ausgewählte Datei konnte nicht gelesen werden. Wähle sie erneut aus.');
    }
  });
  const hydrate = () => {
    const dossier = controller.dossier();
    diagramExplanation.value = dossier.p3.diagram.explanation;
    p1Explanation.value = dossier.p1.diagram.explanation;
    deviation.value = dossier.p2.firstDeviation === null ? '' : String(dossier.p2.firstDeviation);
    transferSequence.value = dossier.p5.sequence.join(', ');
    transferRationale.value = dossier.p5.rationale;
    for (const key of ['timeControl', 'routeCalculation', 'boundary'] as const) {
      required<HTMLTextAreaElement>(root, `[data-system="${key}"]`).value = dossier.p6[key];
    }
    returnArea.value = dossier.returnNote.area;
    returnOpen.value = dossier.returnNote.openPoint;
    returnNext.value = dossier.returnNote.nextAction;
    required<HTMLInputElement>(root, '[data-prediction]').value = controller.transient().prediction;
    required<HTMLTextAreaElement>(root, '[data-m06-retrieval]').value = controller.transient().retrievalReason;
    const evidence = dossier.p3.evidence;
    if (evidence.program.length) showTrace(evidence.program, evidence.steps);
    else {
      required<HTMLElement>(root, '[data-trace-output]').replaceChildren();
      required<HTMLElement>(root, '[data-goal-feedback]').textContent = 'Noch nicht ausgeführt.';
      required<HTMLElement>(root, '[data-run-context]').textContent = 'Noch kein aktueller Prüflauf.';
    }
    render();
  };
  const originalDisabled = new Map(startupControls.map(({ control, disabled }) => [control, disabled]));
  const project = (replacement: boolean) => {
    if (replacement) importSelection += 1;
    if (replacement) {
      displayedRun = null;
      resetPrediction();
      scenario.value = controller.scenario();
      hydrate();
      retrievalPanel.hidden = true; comparison.hidden = true; conceal(false);
      required<HTMLTextAreaElement>(root, '[data-s1-prediction]').value = '';
      exampleSteps.clear();
      for (const node of root.querySelectorAll<HTMLElement>('[data-example-trace]')) node.textContent = 'Noch nicht ausgeführt.';
      required<HTMLElement>(root, '[data-s2-comparison]').hidden = true;
    } else render();
    const contextChanged = predictionProgram !== JSON.stringify(code()) || predictionScenario !== controller.scenario();
    if (contextChanged) {
      resetPrediction();
      predictionProgram = JSON.stringify(code());
      predictionScenario = controller.scenario();
    }
    const snapshot = controller.currentRun();
    if (snapshot && displayedRun !== snapshot.id) {
      showTrace(snapshot.program, [], snapshot);
      displayedRun = snapshot.id;
    } else if (!snapshot && (displayedRun !== null || (contextChanged && !replacement))) {
      required<HTMLElement>(root, '[data-trace-output]').replaceChildren();
      required<HTMLElement>(root, '[data-goal-feedback]').textContent = 'Die vorige Ausführung ist nicht mehr aktuell.';
      required<HTMLElement>(root, '[data-run-context]').textContent = 'Auswahl verworfen. Vorhersage prüfen und den aktuellen Code erneut ausführen.';
      displayedRun = null;
    }
    root.dataset.reloadPreparing = String(controller.reloadPreparing());
    const ready = controller.workspaceReady();
    const preview = controller.importPreview();
    required<HTMLElement>(root, '[data-import-preview]').hidden = preview === null;
    required<HTMLElement>(root, '[data-import-summary]').textContent = preview ? [
      `P1 · Grafik: ${preview.p1.diagram.explanation || 'keine Erklärung'}\n${diagramText(preview.p1.diagram.program)}`,
      `P2 · Vorher: ${preview.p2.before.rationale || 'keine Begründung'}\nNachher: ${preview.p2.after.rationale || 'keine Begründung'}`,
      `P3 · Eigener Code: ${diagramText(preview.p3.draftProgram)}\nBegründung: ${preview.p3.evidence.rationale || 'keine'}`,
      `P5 · Transfer: ${preview.p5.sequence.join(', ')}\n${preview.p5.rationale}`,
      `P6 · Systeme: ${preview.p6.timeControl}\n${preview.p6.routeCalculation}\n${preview.p6.boundary}`,
      `Rückkehr: ${preview.returnNote.openPoint}\nNächste Handlung: ${preview.returnNote.nextAction}`,
    ].join('\n\n') : '';
    required<HTMLElement>(root, '[data-m06-start-error]').hidden = ready;
    required<HTMLElement>(root, '[data-m06-start-message]').textContent = ready ? '' : controller.saveState().message;
    if (!ready) required<HTMLDetailsElement>(root, '[data-m06-management]').open = true;
    for (const control of root.querySelectorAll<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | HTMLButtonElement>('input, textarea, select, button')) {
      const management = control.closest('[data-m06-management]') !== null;
      const exportControl = control.matches('[data-export-work], [data-export-recovery], [data-copy-fallback-text]');
      control.disabled = (originalDisabled.get(control) ?? false)
        || (controller.reloadPreparing() && !exportControl)
        || (controller.replacingWork() && !control.matches('[data-export-recovery], [data-copy-fallback-text]'))
        || (!ready && (!management || control.matches('[data-export-work], [data-delete-work]')))
        || (control.matches('[data-confirm-import], [data-cancel-import]') && preview === null)
        || (control.matches('[data-export-recovery]') && !controller.hasRecovery())
        || control.dataset.fixedDisabled === 'true'
        || (control.matches('[data-retrieval-compare]') && !controller.transient().retrievalReason.trim())
        || control.matches('[data-saved-trace]')
        || (control.matches('[data-save-evidence]') && (!controller.canRecordEvidence('S3') || selectedTraceSteps(root).length === 0))
        || (control.matches('[data-revision]') && (!controller.canRecordEvidence('S2') || selectedTraceSteps(root).length === 0));
    }
  };
  required<HTMLElement>(root, '[data-trace-output]').addEventListener('change', () => project(false));
  const unsubscribe = controller.subscribe(project);
  const dispose = controller.dispose.bind(controller);
  controller.dispose = () => { unsubscribe(); dispose(); };
  project(true);
  root.inert = false;
  root.setAttribute('aria-busy', 'false');
  return controller;
}
