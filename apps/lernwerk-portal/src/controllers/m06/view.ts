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
  const controller = await connectM06(root, resources, createBrowserM06Dependencies(root));
  let diagram: Program = controller.dossier().p3.diagram.program;
  let code: Program = controller.dossier().p3.draftProgram;
  const diagramExplanation = required<HTMLTextAreaElement>(root, '[data-diagram-explanation]');
  const diagramOutput = required<HTMLElement>(root, '[data-diagram-output]');
  const codeOutput = required<HTMLElement>(root, '[data-code-output]');
  const rationale = required<HTMLTextAreaElement>(root, '[data-rationale]');
  const render = () => {
    diagramOutput.textContent = diagram.length ? diagramText(diagram) : 'Noch keine Grafik angelegt.';
    codeOutput.textContent = code.length ? diagramText(code) : 'Noch kein Code eingegeben.';
  };
  const basic = (program: Program, kind: Basic['kind']): Basic => ({
    id: nextCommandId(program),
    kind,
  });

  for (const editor of root.querySelectorAll<HTMLElement>('[data-editor]')) {
    const editorKind = editor.dataset.editor;
    for (const button of editor.querySelectorAll<HTMLButtonElement>('[data-add]')) {
      button.addEventListener('click', () => {
        if (editorKind === 'diagram') {
          diagram = [...diagram, basic(diagram, commandKind(button.dataset.add ?? null))];
          controller.updateDiagram(diagram, diagramExplanation.value);
        } else {
          code = [...code, basic(code, commandKind(button.dataset.add ?? null))];
          controller.updateDraftProgram(code);
        }
        render();
      });
    }
    required<HTMLButtonElement>(editor, '[data-clear]').addEventListener('click', () => {
      if (editorKind === 'diagram') {
        diagram = [];
        controller.updateDiagram([], diagramExplanation.value);
      } else {
        code = [];
        controller.updateDraftProgram([]);
      }
      render();
    });
  }
  diagramExplanation.addEventListener('input', () => {
    controller.updateDiagram(diagram, diagramExplanation.value);
  });

  required<HTMLButtonElement>(root, '[data-add-repeat]').addEventListener('click', () => {
    const count = Number(required<HTMLInputElement>(root, '#m06-repeat-count').value);
    const repeatId = nextCommandId(code);
    let nextNumber = Number(repeatId.slice(4)) + 1;
    const body = [...root.querySelectorAll<HTMLSelectElement>('[data-repeat-body]')]
      .filter((field) => field.value !== '')
      .map((field): Basic => ({ id: `cmd-${nextNumber++}`, kind: commandKind(field.value) }));
    if (body.length === 0) return;
    code = [...code, { id: repeatId, kind: 'repeat', count, body }];
    controller.updateDraftProgram(code);
    render();
  });
  required<HTMLButtonElement>(root, '[data-add-diagram-repeat]').addEventListener('click', () => {
    const count = Number(required<HTMLInputElement>(root, '#m06-diagram-count').value);
    const repeatId = nextCommandId(diagram);
    let nextNumber = Number(repeatId.slice(4)) + 1;
    const body = [...root.querySelectorAll<HTMLSelectElement>('[data-diagram-repeat-body]')]
      .filter((field) => field.value !== '')
      .map((field): Basic => ({ id: `cmd-${nextNumber++}`, kind: commandKind(field.value) }));
    if (body.length === 0) return;
    diagram = [...diagram, { id: repeatId, kind: 'repeat', count, body }];
    controller.updateDiagram(diagram, diagramExplanation.value);
    render();
  });

  required<HTMLButtonElement>(root, '[data-run-code]').addEventListener('click', () => {
    const result = run(s3.grid, code);
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
      const directions = { north: 'oben', east: 'rechts', south: 'unten', west: 'links' } as const;
      const iteration = step.iteration === null ? 'ohne Wiederholung' : `Durchlauf ${step.iteration}`;
      row.append(check, ` Schritt ${step.step}, Befehl ${step.commandId}, ${iteration}: (${step.before.position.column},${step.before.position.row}) → (${step.after.position.column},${step.after.position.row}), Blick ${directions[step.after.direction]}${step.error ? `, Fehler ${step.error}` : ''}`);
      fieldset.append(row);
    }
    trace.append(fieldset);
  });

  required<HTMLButtonElement>(root, '[data-save-evidence]').addEventListener('click', () => {
    controller.recordP3Evidence(null, selectedTraceSteps(root), rationale.value);
  });
  required<HTMLInputElement>(root, '[data-prediction]').addEventListener('input', (event) => {
    controller.setTransient({ prediction: (event.currentTarget as HTMLInputElement).value });
  });
  for (const button of root.querySelectorAll<HTMLButtonElement>('[data-revision]')) {
    button.addEventListener('click', () => {
      const phase = button.dataset.revision;
      if (phase !== 'before' && phase !== 'after') return;
      controller.recordRevisionEvidence(phase, code, selectedTraceSteps(root), rationale.value);
      const value = Number(required<HTMLInputElement>(root, '[data-first-deviation]').value);
      controller.setFirstDeviation(Number.isInteger(value) && value > 0 ? value : null);
    });
  }

  const transferSequence = required<HTMLInputElement>(root, '[data-transfer-sequence]');
  const transferRationale = required<HTMLTextAreaElement>(root, '[data-transfer-rationale]');
  const saveTransfer = () => {
    const allowed = new Set(['aufnehmen', 'prüfen', 'ablegen']);
    const sequence = transferSequence.value.split(',')
      .map((value) => value.trim())
      .filter((value): value is 'aufnehmen' | 'prüfen' | 'ablegen' => allowed.has(value));
    controller.updateTransfer(sequence, transferRationale.value);
  };
  transferSequence.addEventListener('change', saveTransfer);
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
  [returnArea, returnOpen, returnNext].forEach((field) => field.addEventListener('change', saveReturn));

  required<HTMLButtonElement>(root, '[data-delete-work]').addEventListener('click', () => {
    if (window.confirm('Diesen lokalen M06-Arbeitsstand wirklich löschen?')) {
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
    if (file) await controller.importBytes(new Uint8Array(await file.arrayBuffer()));
    input.value = '';
  });
  render();
  return controller;
}
