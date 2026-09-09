import {
  checkGoal,
  run,
  type Basic,
  type Goal,
  type Grid,
  type Program,
} from '@ium/v2-g5-m06';
import {
  connectM06,
  createBrowserM06Dependencies,
  type M06Controller,
  type M06Resources,
} from './controller.js';
import { diagramText } from './diagram-editor.js';
import { nextCommandId } from './code-editor.js';

type S3Case = Readonly<{ id: 'S3'; grid: Grid; goal: Goal }>;
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
  if (!s3) throw new Error('S3 resource missing');
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
    diagramOutput.textContent = diagram().length ? diagramText(diagram()) : 'Noch keine Grafik angelegt.';
    codeOutput.textContent = code().length ? diagramText(code()) : 'Noch kein Code eingegeben.';
    required<HTMLElement>(root, '[data-p1-output]').textContent = dossier.p1.diagram.program.length
      ? diagramText(dossier.p1.diagram.program) : 'Noch keine P1-Grafik angelegt.';
    if (rationale.value !== dossier.p3.evidence.rationale) rationale.value = dossier.p3.evidence.rationale;
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

  const showTrace = (program: Program, selected: readonly number[] = []) => {
    const result = run(s3.grid, program);
    const goal = checkGoal(result, s3.goal);
    required<HTMLElement>(root, '[data-goal-feedback]').textContent = goal.ok
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
      const directions = { north: 'oben', east: 'rechts', south: 'unten', west: 'links' } as const;
      const iteration = step.iteration === null ? 'ohne Wiederholung' : `Durchlauf ${step.iteration}`;
      row.append(check, ` Schritt ${step.step}, Befehl ${step.commandId}, ${iteration}: (${step.before.position.column},${step.before.position.row}) → (${step.after.position.column},${step.after.position.row}), Blick ${directions[step.after.direction]}${step.error ? `, Fehler ${step.error}` : ''}`);
      fieldset.append(row);
    }
    trace.append(fieldset);
  };
  required<HTMLButtonElement>(root, '[data-run-code]').addEventListener('click', () => {
    showTrace(code());
  });

  required<HTMLButtonElement>(root, '[data-save-evidence]').addEventListener('click', () => {
    controller.recordP3Evidence(controller.dossier().p3.evidence.predicted, selectedTraceSteps(root), rationale.value);
  });
  required<HTMLInputElement>(root, '[data-prediction]').addEventListener('input', (event) => {
    controller.setTransient({ prediction: (event.currentTarget as HTMLInputElement).value });
  });
  for (const button of root.querySelectorAll<HTMLButtonElement>('[data-revision]')) {
    button.addEventListener('click', () => {
      const phase = button.dataset.revision;
      if (phase !== 'before' && phase !== 'after') return;
      controller.recordRevisionEvidence(phase, code(), selectedTraceSteps(root), rationale.value);
      const value = Number(required<HTMLInputElement>(root, '[data-first-deviation]').value);
      controller.setFirstDeviation(Number.isInteger(value) && value > 0 ? value : null);
    });
  }
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
    }
    const predicted = evidence.predicted;
    required<HTMLElement>(root, '[data-saved-prediction]').textContent = predicted
      ? `Gesicherte Vorhersage: (${predicted.position.column},${predicted.position.row}), Blick ${
        { north: 'oben', east: 'rechts', south: 'unten', west: 'links' }[predicted.direction]}.`
      : 'Noch keine Vorhersage im Beleg gesichert.';
    render();
  };
  const originalDisabled = new Map(startupControls.map(({ control, disabled }) => [control, disabled]));
  const project = (replacement: boolean) => {
    if (replacement) importSelection += 1;
    if (replacement) hydrate();
    else render();
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
        || (control.matches('[data-export-recovery]') && !controller.hasRecovery());
    }
  };
  const unsubscribe = controller.subscribe(project);
  const dispose = controller.dispose.bind(controller);
  controller.dispose = () => { unsubscribe(); dispose(); };
  project(true);
  root.inert = false;
  root.setAttribute('aria-busy', 'false');
  return controller;
}
